import datetime as dt
import json
import logging
import multiprocessing
import os
import pprint as pp
import shutil
from multiprocessing import Pool, Manager
from pathlib import Path
from typing import Dict, Optional

import psutil
import tensorflow as tf
from fastapi import UploadFile
from loguru import logger

from api.model import CodebookModel, TrainingResponse, TrainingRequest, TrainingState, TrainingStatus
from logger import backend_logger
from .model_factory import ModelFactory
from ..data_handler import DataHandler
from ..exceptions import ErroneousDatasetException
from ..model_manager import ModelManager


class Trainer(object):
    _singleton = None
    # TODO persist in redis or similar
    _status_dict: Dict[str, TrainingStatus] = None
    _pool: Pool = None
    _manager: Manager = None

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            backend_logger.info('Instantiating Trainer!')

            # load config file
            config = json.load(open("config.json", "r"))

            # make sure GPU is available for ModelTrainer (if there is one)
            if not bool(config['backend']['use_gpu_for_training']):
                backend_logger.info("GPU support for training disabled!")
                os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
            else:
                backend_logger.info("GPU support for training enabled!")

            cls._singleton = super(Trainer, cls).__new__(cls)
            cls._manager = Manager()
            cls._status_dict = cls._manager.dict()
            cls._pool = Pool(processes=config['backend']['num_training_workers'])

        return cls._singleton

    @staticmethod
    def shutdown():
        Trainer._pool.close()
        Trainer._manager.shutdown()

    @staticmethod
    def train(request: TrainingRequest) -> TrainingResponse:
        # TODO
        #  - how to assign GPU(s)

        backend_logger.info(f"Spawning new process for train-eval-export cycle for Codebook <{request.cb.name}>")
        res = Trainer._pool.apply_async(train_eval_export, args=(request, Trainer._status_dict,))

        model_id = ModelFactory.get_model_id(req=request)
        return TrainingResponse(model_id=model_id)

    @staticmethod
    def get_train_log(resp: TrainingResponse) -> Path:
        return ModelFactory.get_training_log_file(resp.model_id)

    @staticmethod
    def get_train_status(resp: TrainingResponse) -> Optional[TrainingStatus]:
        try:
            return Trainer._status_dict[resp.model_id]
        except Exception:
            return None

    @staticmethod
    @logger.catch
    def dataset_is_available(cb: CodebookModel, dataset_version: str) -> bool:
        return ModelFactory.dataset_is_available(cb, dataset_version=dataset_version)

    @staticmethod
    def store_uploaded_dataset(cb: CodebookModel, dataset_version: str, dataset_archive: UploadFile) -> bool:
        backend_logger.info(f"Successfully received dataset archive for Codebook {cb.name}")

        try:
            path = DataHandler.store_dataset(cb=cb, dataset_archive=dataset_archive, dataset_version=dataset_version)
        except Exception as e:
            raise ErroneousDatasetException(dataset_version, cb,
                                            f"Error while persisting dataset for Codebook {cb.name}!",
                                            caused_by=str(e))
        if not ModelFactory.dataset_is_available(cb, dataset_version=dataset_version):
            raise ErroneousDatasetException(dataset_version, cb,
                                            f"Error while persisting dataset for Codebook {cb.name} under {str(path)}")
        backend_logger.info(
            f"Successfully persisted dataset '{dataset_version}' for Codebook <{cb.name}> under {str(path)}")
        return True


"""
The following methods are outside of the class because they have to be pickled for multi-processing and pickling 
methods of classes is not trivial.. (have to be specially registered to the python interpreted and custom pickling 
functions have to be implemented.
"""


def input_fn(r: TrainingRequest, train: bool = False):
    # note that TF is not in EagerExecution mode when this method gets called
    # https://www.tensorflow.org/api_docs/python/tf/estimator/Estimator#eager_compatibility

    # create tf datasets (we have to load them in the input fn otherwise we get an EagerExecution problem)
    train_ds, test_ds, label_categories = ModelFactory.create_datasets(r.cb, r.dataset_version)
    if train:
        train_ds = train_ds.shuffle(256).batch(r.batch_size_train).repeat()
        return train_ds
    else:
        test_ds = test_ds.shuffle(256).batch(r.batch_size_test)
        return test_ds


def generate_model_metadata(r: TrainingRequest, model_id: str, eval_results: Dict[str, float]) -> Path:
    backend_logger.info(f"Generating model metadata file for model<{model_id}>")
    label_categories = ModelFactory.create_datasets(r.cb, r.dataset_version, get_labels_only=True)

    metadata = {}
    metadata.update(eval_results)
    metadata['labels'] = dict(enumerate(label_categories))
    metadata['model_type'] = 'DNNClassifier'
    metadata['model_config'] = r.model_config.dict()
    metadata['timestamp'] = str(dt.datetime.now())

    # make sure strings are in dict
    metadata = {str(key): str(val) for key, val in metadata.items()}

    # persist
    metadata_dst = ModelFactory.get_metadata_file(model_id)
    with open(metadata_dst, 'w') as fp:
        json.dump(metadata, fp, indent=2)
    assert metadata_dst.exists()
    backend_logger.info(f"Model metadata for model <{model_id}> persisted at {str(metadata_dst)}")

    return metadata_dst


def update_training_status(status_dict: Dict[str, TrainingStatus], mid: str, state: TrainingState, pid: int):
    status = TrainingStatus()
    status.state = state
    status.process_status = psutil.Process(pid).status()
    status_dict[mid] = status


@logger.catch
def train_eval_export(req: TrainingRequest, status_dict: Dict[str, TrainingStatus]):
    # TODO use redis or similar to persist this dict
    mid = ModelFactory.get_model_id(req)
    proc = multiprocessing.current_process()
    backend_logger.info(f"Started train-eval-export cycle process with PID <{str(proc.pid)}>")

    # init training status
    training_status = TrainingStatus()
    status_dict[mid] = training_status

    # intercept logs to loguru sink
    intercept_handler = LoggingInterceptHandler()
    try:

        update_training_status(status_dict, mid, TrainingState.preparing, proc.pid)

        # create log file
        log_file = ModelFactory.get_training_log_file(mid, create=True)
        backend_logger.info(f"Setting up logging for process with PID <{str(proc.pid)}> at <{str(log_file)}>")
        # create loguru sink
        logger.add(str(log_file), rotation="500 MB", enqueue=True)
        tf.get_logger().addHandler(intercept_handler)
        backend_logger.addHandler(intercept_handler)

        # create model
        mid = ModelFactory.get_model_id(req)
        backend_logger.info(f"Building model <{req.model_version}> for Codebook <{req.cb.name}> with model config"
                            f"<{req.model_config}>. ModelID: <{mid}>")
        # TODO
        #  n_classes could be another value than len(request.cb.tags) !!!
        #  => get this info efficiently (w/o loading the DS)
        model, embedding_layer, mid = ModelFactory.build_model(req, n_classes=len(req.cb.tags))

        # train model
        backend_logger.info(f"Starting training of model <{mid}>")
        # updating training status
        update_training_status(status_dict, mid, TrainingState.training, proc.pid)
        model.train(input_fn=lambda: input_fn(req, train=True), max_steps=req.max_steps_train)

        # evaluate model
        backend_logger.info(f"Starting evaluation of model <{mid}>")
        # updating training status
        update_training_status(status_dict, mid, TrainingState.evaluating, proc.pid)
        results = model.evaluate(input_fn=lambda: input_fn(req, train=False), steps=req.max_steps_test)
        res_pp = pp.pformat(results)
        backend_logger.info(f"Evaluation results of model <{mid}>:\n {res_pp}")

        # export # TODO this should be moved to DataHandler
        backend_logger.info(f"Starting export of model <{mid}>")
        # updating training status
        update_training_status(status_dict, mid, TrainingState.training, proc.pid)
        # create serving function
        serving_input_fn = tf.estimator.export.build_parsing_serving_input_receiver_fn(
            tf.feature_column.make_parse_example_spec([embedding_layer]))
        # create model meta data
        metadata_path = generate_model_metadata(r=req, model_id=mid, eval_results=results)
        # finally, persist model
        dst = ModelFactory.get_model_dir(model_id=mid)
        estimator_path = model.export_saved_model(str(dst),
                                                  serving_input_fn,
                                                  assets_extra={'model_metadata.json': str(metadata_path)})
        estimator_path = estimator_path.decode('utf-8')
        backend_logger.info(f"Tensorflow exported model successfully at {estimator_path}")
        # move the exported model files to the mode dir (see export_saved_model docs)
        backend_logger.info(f"Moving <{mid}> to <{str(dst)}>")
        files = [f for f in Path(estimator_path).iterdir()]
        for f in files:
            shutil.move(str(f), str(f.parent.parent))

        # TODO exception if fails
        assert ModelManager.model_is_available(req.cb, req.model_version)
        backend_logger.info(f"Successfully exported model <{mid}> at {estimator_path}")

        backend_logger.info(f"Completed train-eval-export cycle for model <{mid}>")
        backend_logger.info(f"Model <{mid}> stored at {str(dst)}")
        # updating training status
        update_training_status(status_dict, mid, TrainingState.finished, proc.pid)
    except Exception as e:
        update_training_status(status_dict, mid, TrainingState.error, proc.pid)
        raise e
    finally:
        tf.get_logger().removeHandler(intercept_handler)
        backend_logger.removeHandler(intercept_handler)


class LoggingInterceptHandler(logging.Handler):
    def emit(self, record):
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())

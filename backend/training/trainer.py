import datetime as dt
import json
import logging
import os
import shutil
import sys
from multiprocessing import Process
from pathlib import Path
from typing import Dict

import tensorflow as tf
from fastapi import UploadFile

from api.model import CodebookModel, TrainingResponse, TrainingRequest, TrainingState, TrainingStatus
from logger import backend_logger
from .model_factory import ModelFactory
from ..data_handler import DataHandler
from ..exceptions import ErroneousDatasetException
from ..model_manager import ModelManager


class Trainer(object):
    _singleton = None

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
            cls._dh = DataHandler()
            cls._mm = ModelManager()
            cls._mf = ModelFactory()

        return cls._singleton

    def __init__(self):
        self._proc_dict: Dict[str, Process] = {}

    def train(self, request: TrainingRequest) -> TrainingResponse:
        # TODO
        #  - max_steps in config file
        #  - make sure training is running in background (own process(s))
        #  - how to assign GPU(s)

        def train_eval_export(req: TrainingRequest):

            def input_fn(r: TrainingRequest, train: bool = False):
                # note that TF is not in EagerExecution mode when this method gets called
                # https://www.tensorflow.org/api_docs/python/tf/estimator/Estimator#eager_compatibility

                # create tf datasets (we have to load them in the input fn otherwise we get an EagerExecution problem)
                train_ds, test_ds, label_categories = self._mf.create_datasets(r.cb, r.dataset_version)
                if train:
                    train_ds = train_ds.shuffle(256).batch(r.batch_size_train).repeat()
                    return train_ds
                else:
                    test_ds = test_ds.shuffle(256).batch(r.batch_size_test)
                    return test_ds

            def generate_model_metadata(r: TrainingRequest, model_id: str, eval_results: Dict[str, float]) -> Path:
                backend_logger.info(f"Generating model metadata file for model<{model_id}>")
                label_categories = self._mf.create_datasets(req.cb, req.dataset_version, get_labels_only=True)

                metadata = {}
                metadata.update(eval_results)
                metadata['labels'] = dict(enumerate(label_categories))
                metadata['model_type'] = 'DNNClassifier'
                metadata['model_config'] = r.model_config.dict()
                metadata['timestamp'] = str(dt.datetime.now())

                # make sure strings are in dict
                metadata = {str(key): str(val) for key, val in metadata.items()}

                # persist
                metadata_dst = self._mf.get_metadata_file(model_id)
                with open(metadata_dst, 'w') as fp:
                    json.dump(metadata, fp, indent=2)
                assert metadata_dst.exists()
                backend_logger.info(f"Model metadata for model <{model_id}> persisted at {str(metadata_dst)}")

                return metadata_dst

            # create model
            mid = self._mf.get_model_id(req)
            backend_logger.info(f"Building model <{req.model_version}> for Codebook <{req.cb.name}> with model config"
                                f"<{req.model_config}>. ModelID: <{mid}>")
            # TODO
            #  n_classes could be another value than len(request.cb.tags) !!!
            #  => get this info efficiently (w/o loading the DS)
            model, embedding_layer, mid = self._mf.build_model(req, n_classes=len(req.cb.tags))

            # train model
            backend_logger.info(f"Starting training of model <{mid}>")
            model.train(input_fn=lambda: input_fn(req, train=True), max_steps=req.max_steps_train)

            # evaluate model
            backend_logger.info(f"Starting evaluation of model <{mid}>")
            results = model.evaluate(input_fn=lambda: input_fn(req, train=False), steps=req.max_steps_test)

            # export
            backend_logger.info(f"Starting export of model <{mid}>")
            # create serving function
            serving_input_fn = tf.estimator.export.build_parsing_serving_input_receiver_fn(
                tf.feature_column.make_parse_example_spec([embedding_layer]))
            # create model meta data
            metadata_path = generate_model_metadata(r=req, model_id=mid, eval_results=results)
            # finally, persist model
            dst = self._mf.get_model_dir(model_id=mid).joinpath("exported")
            estimator_path = model.export_saved_model(str(dst),
                                                      serving_input_fn,
                                                      assets_extra={'model_metadata.json': str(metadata_path)})
            estimator_path = estimator_path.decode('utf-8')
            backend_logger.info(f"Tensorflow exported model successfully at {estimator_path}")
            # move the exported model files to the mode dir (see export_saved_model docs)
            backend_logger.info(f"Moving <{model_id}> to <{str(dst)}>")
            files = [f for f in Path(estimator_path).iterdir()]
            for f in files:
                shutil.move(str(f), str(f.parent.parent.parent))

            # TODO exception if fails
            assert self._mm.model_is_available(request.cb, request.model_version)
            backend_logger.info(f"Successfully exported model <{model_id}> at {estimator_path}")

            backend_logger.info(f"Completed train-eval-export cycle for model <{mid}>")
            backend_logger.info(f"Model <{mid}> stored at {str(estimator_path)}")

        model_id = self._mf.get_model_id(req=request)
        # create log file
        # TODO
        #  - use loguru to catch all error msgs etc and log to a logfile that contains all info about the training
        log_file = self._mf.get_log_file(model_id, create=True)

        proc = Process(target=self.redirect_output(open(str(log_file), "w"))(train_eval_export), args=(request,))
        try:
            backend_logger.info(f"Spawning new process for train-eval-export cycle for Codebook <{request.cb.name}>")
            proc.start()
            backend_logger.info(f"Started train-eval-export cycle process with PID <{str(proc.pid)}>")

            # TODO use redis or similar to persist this dict
            self._proc_dict[model_id] = proc

        except Exception as e:
            proc.terminate()
            print(e)

        return TrainingResponse(model_id=model_id)

    def get_train_log(self, resp: TrainingResponse):
        return self._mf.get_log_file(resp.model_id)

    def get_train_status(self, resp: TrainingResponse) -> TrainingStatus:
        proc = self._proc_dict.get(resp.model_id)
        status = TrainingStatus(state=TrainingState.unknown, process_alive=proc.is_alive())
        return status

    def store_uploaded_dataset(self, cb: CodebookModel, dataset_version: str, dataset_archive: UploadFile) -> bool:
        # TODO
        # - make sure that a valid CSV dataset was extracted -> dataset_is_available
        backend_logger.info(f"Successfully received dataset archive for Codebook {cb.name}")

        try:
            path = self._dh.store_dataset(cb=cb, dataset_archive=dataset_archive, dataset_version=dataset_version)
        except Exception as e:
            raise ErroneousDatasetException(dataset_version, cb,
                                            f"Error while persisting dataset for Codebook {cb.name}!",
                                            caused_by=str(e))
        if not self._mf.dataset_is_available(cb, dataset_version=dataset_version):
            raise ErroneousDatasetException(dataset_version, cb,
                                            f"Error while persisting dataset for Codebook {cb.name} under {str(path)}")
        backend_logger.info(
            f"Successfully persisted dataset '{dataset_version}' for Codebook <{cb.name}> under {str(path)}")
        return True

    # decorator to redirect outputs to a file
    @staticmethod
    def redirect_output(output_stream):
        def wrap(f):
            def new_f(*args, **kwargs):
                old_stderr, old_stdout = sys.stderr, sys.stdout
                sys.stderr = output_stream
                sys.stdout = output_stream

                output_stream_handler = logging.StreamHandler(output_stream)
                tf_logger = tf.get_logger()
                tf_logger.setLevel("NOTSET")

                backend_logger.addHandler(output_stream_handler)
                tf_logger.addHandler(output_stream_handler)

                try:
                    return f(*args, **kwargs)
                finally:
                    backend_logger.removeHandler(output_stream_handler)
                    tf_logger.removeHandler(output_stream_handler)
                    sys.stderr, sys.stdout = old_stderr, old_stdout
                    output_stream.close()

            return new_f

        return wrap

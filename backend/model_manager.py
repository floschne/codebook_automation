# this class will be responsible for loading models, fetching metadata, check availability
# etc.
import hashlib
import json
import os

from api.model import CodebookModel
from logger import backend_logger


class ModelNotAvailableException(Exception):
    pass


class ModelManager(object):
    _singleton = None
    _BASE_PATH = None

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:

            # load config file
            config = json.load(open("config.json", "r"))

            backend_logger.info('Instantiating ModelManager!')
            cls._singleton = super(ModelManager, cls).__new__(cls)

            # read the model base path from config and 'validate' it
            env_var = config['backend']['model_base_path_env_var']
            cls._BASE_PATH = os.getenv(env_var, None).strip()
            assert cls._BASE_PATH is not None and cls._BASE_PATH != ""

            # create the BASE_PATH if it doesn't exist
            if not os.path.exists(cls._BASE_PATH):
                os.makedirs(cls._BASE_PATH)

        return cls._singleton

    def __init__(self):
        assert self._BASE_PATH is not None and self._BASE_PATH != ""
        # create the BASE_PATH if it doesn't exist
        if not os.path.exists(self._BASE_PATH):
            os.makedirs(ModelManager._BASE_PATH)

        self.a = "a"

    def model_is_available(self, cb: CodebookModel) -> bool:
        """
        Checks if the model for the given codebook is available
        :param cb: the codebook
        :return: True if the model for the codebook is available and False otherwise
        """
        model_id = self.compute_model_id(cb)
        # TODO dont just check on the existence of the path but of the real model and if its possible to predict
        return os.path.exists(os.path.join(self._BASE_PATH, model_id))

    def _model_is_available(self, m_id: str) -> bool:
        """
        Checks if the model with the given id is available
        :param m_id: the id of the model
        :return: True if the model with the id is available and False otherwise
        """
        # TODO dont just check on the existence of the path but of the real model and if its possible to predict
        return os.path.exists(os.path.join(self._BASE_PATH, m_id))

    def init_model(self, cb: CodebookModel) -> str:
        """
        Initializes a model for a given codebook
        :param cb: the codebook
        :return: the id of the model
        """
        # TODO implement logic to accomplish matching tags and labels
        if not self.model_is_available(cb):
            ModelManager._create_model_directory(cb)
            assert self.model_is_available(cb)
        return ModelManager.compute_model_id(cb)

    def get_model_path(self, cb: CodebookModel) -> str:
        """
        Returns the path of the model of the given Codebook
        :param cb: the codebook
        :return: path to the model of the codebook
        :raises: ModelNotAvailableException if the model is not available
        """
        if self.model_is_available(cb):
            model_id = self.compute_model_id(cb)
            return str(os.path.join(self._BASE_PATH, model_id))
        else:
            raise ModelNotAvailableException("Model for Codebook %s is not available!" % cb.name)

    @staticmethod
    def compute_model_id(cb: CodebookModel) -> str:
        """
        Computes the model id for the given Codebook by MD5-hashing it's JSON representation.
        Note that this is just an identifier and does not ensure that the model exists.
        :param cb: The codebook model!
        :return: The model ID as a string
        """
        return hashlib.md5(cb.json().encode('utf-8')).hexdigest()

    @staticmethod
    def _create_model_directory(cb: CodebookModel) -> str:
        """
        Creates the model directory and returns the path as string
        :param cb: the codebook the model directory gets created for
        :return: the path of the model directory
        """
        m_id = ModelManager.compute_model_id(cb)
        m_dir = os.path.join(ModelManager._BASE_PATH, m_id)
        os.makedirs(m_dir)
        return str(m_dir)

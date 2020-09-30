# this class will be responsible for loading models, fetching metadata, check availability
# etc.
import hashlib
import os

from api.model import CodebookModel
from logger import backend_logger
from main import config


class ModelManager(object):
    _singleton = None
    _BASE_PATH = None

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            backend_logger.info('Instantiating ModelManager!')
            cls._singleton = super(ModelManager, cls).__new__(cls)

            # read the model base path from config and 'validate' it
            cls._BASE_PATH = config['model_base_path']
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
        model_id = self.compute_model_id(cb)
        return os.path.exists(os.path.join(self._BASE_PATH, model_id))

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
        m_id = ModelManager.compute_model_id(cb)
        m_dir = os.path.join(ModelManager._BASE_PATH, m_id)
        os.makedirs(m_dir)
        return str(m_dir)

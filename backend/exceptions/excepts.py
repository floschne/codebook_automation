class NoDataForCodebookException(Exception):
    def __init__(self, cb_name: str = None):
        self.codebook = cb_name
        self.message = f"No data for Codebook <{cb_name}> found!"


class ErroneousDatasetException(Exception):
    def __init__(self, dataset_version: str = None, cb_name: str = None, msg: str = None, caused_by: str = None):
        self.codebook = cb_name
        self.caused_by = caused_by
        if msg is None:
            self.message = f"Dataset <{dataset_version}> for Codebook <{cb_name}> is erroneous!"
        else:
            self.message = msg


class DatasetNotAvailableException(Exception):
    def __init__(self, dataset_version: str = None, cb_name: str = None):
        self.dataset_version = dataset_version,
        self.codebook = cb_name

        self.message = f"Dataset <{dataset_version}> for Codebook <{cb_name}> not available!"


class InvalidModelIdException(Exception):
    def __init__(self, model_id: str):
        self.model_id = model_id
        self.message = f"Model ID <{model_id}> is invalid!"


class ErroneousModelException(Exception):
    def __init__(self, model_version: str = None, cb_name: str = None, msg: str = None):
        self.codebook = cb_name
        if msg is None:
            self.message = f"Model <{model_version}> for Codebook <{cb_name}> is erroneous!"
        else:
            self.message = msg


class ErroneousMappingException(Exception):
    def __init__(self, cb_name: str = None):
        self.codebook = cb_name
        self.message = f"Tag-Label-Mapping is erroneous!"


class ModelNotAvailableException(Exception):
    def __init__(self, model_version: str = None, cb_name: str = None, model_id: str = None):
        self.model_version = model_version,
        self.model_id = model_id
        self.codebook = cb_name

        if model_id:
            self.message = f"Model with id <{model_id}> not available!"
        else:
            self.message = f"Model <{model_version}> for Codebook <{cb_name}> not available!"


class ModelInitializationException(Exception):
    def __init__(self, cb_name: str, path: str, caused_by: str = None):
        self.cb_name = cb_name
        self.path = path
        self.caused_by = caused_by
        self.message = f"Could not initialize Model Environment for Codebook <{self.cb_name}> at {self.path}!"


class PredictionError(Exception):
    def __init__(self):
        self.message = "Critical internal error occurred during prediction!"


class TFHubEmbeddingException(Exception):
    def __init__(self, embedding_type: str):
        self.message = f"Cannot load embedding layer of type <{embedding_type}> from TF Hub!"

from api.model import CodebookDTO


class NoDataForCodebookException(Exception):
    def __init__(self, cb: CodebookDTO = None):
        self.codebook = cb
        self.message = f"No data for Codebook <{cb}> found!"


class ErroneousDatasetException(Exception):
    def __init__(self, dataset_version: str = None, cb: CodebookDTO = None, msg: str = None, caused_by: str = None):
        self.codebook = cb
        self.caused_by = caused_by
        if msg is None:
            self.message = f"Dataset <{dataset_version}> for Codebook <{cb.name}> is erroneous!"
        else:
            self.message = msg


class DatasetNotAvailableException(Exception):
    def __init__(self, dataset_version: str = None, cb: CodebookDTO = None):
        self.dataset_version = dataset_version,
        self.codebook = cb

        self.message = f"Dataset <{dataset_version}> for Codebook <{cb.name}> not available!"


class InvalidModelIdException(Exception):
    def __init__(self, model_id: str):
        self.model_id = model_id
        self.message = f"Model ID <{model_id}> is invalid!"


class ErroneousModelException(Exception):
    def __init__(self, model_version: str = None, cb: CodebookDTO = None, msg: str = None):
        self.codebook = cb
        if msg is None:
            self.message = f"Model <{model_version}> for Codebook <{cb.name}> is erroneous!"
        else:
            self.message = msg


class ErroneousMappingException(Exception):
    def __init__(self, cb: CodebookDTO = None):
        self.codebook = cb
        self.message = f"Tag-Label-Mapping is erroneous!"


class ModelNotAvailableException(Exception):
    def __init__(self, model_version: str = None, cb: CodebookDTO = None, model_id: str = None):
        self.model_version = model_version,
        self.model_id = model_id
        self.codebook = cb

        if model_id:
            self.message = f"Model with id <{model_id}> not available!"
        else:
            self.message = f"Model <{model_version}> for Codebook <{cb.name}> not available!"


class ModelMetadataNotAvailableException(Exception):
    def __init__(self, cb: CodebookDTO, model_version: str = None):
        self.model_id = model_version
        self.message = f"Model Metadata for Model <{model_version}> of Codebook <{cb.name}> not available!"


class ModelInitializationException(Exception):
    def __init__(self, cb: CodebookDTO, path: str, caused_by: str = None):
        self.cb = cb
        self.path = path
        self.caused_by = caused_by
        self.message = f"Could not initialize Model Environment for Codebook <{self.cb.name}> at {self.path}!"


class PredictionError(Exception):
    def __init__(self):
        self.message = "Critical internal error occurred during prediction!"


class TFHubEmbeddingException(Exception):
    def __init__(self, embedding_type: str):
        self.message = f"Cannot load embedding layer of type <{embedding_type}> from TF Hub!"

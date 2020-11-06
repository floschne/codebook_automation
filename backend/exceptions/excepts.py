from api.model import CodebookModel


class ErroneousModelException(Exception):
    def __init__(self, model_version: str = None, cb: CodebookModel = None, msg: str = None):
        self.codebook = cb
        if msg is None:
            self.message = f"Model <{model_version}> for Codebook <{cb.name}> is erroneous!"
        else:
            self.message = msg


class ErroneousDatasetException(Exception):
    def __init__(self, dataset_version: str = None, cb: CodebookModel = None, msg: str = None):
        self.codebook = cb
        if msg is None:
            self.message = f"Dataset <{dataset_version}> for Codebook <{cb.name}> is erroneous!"
        else:
            self.message = msg


class ErroneousMappingException(Exception):
    def __init__(self, cb: CodebookModel = None):
        self.codebook = cb
        self.message = f"Tag-Label-Mapping is erroneous!"


class ModelNotAvailableException(Exception):
    def __init__(self, model_version: str = None, cb: CodebookModel = None):
        self.model_id = model_version,
        self.codebook = cb
        self.message = f"Model <{model_version}> for Codebook <{cb.name}> not available!"


class ModelMetadataNotAvailableException(Exception):
    def __init__(self, cb: CodebookModel, model_version: str = None):
        self.model_id = model_version
        self.message = f"Model Metadata for Model <{model_version}> of Codebook <{cb.name}> not available!"


class ModelInitializationException(Exception):
    def __init__(self, cb: CodebookModel, path: str, cause_msg: str = None):
        self.cb = cb
        self.path = path
        self.cause_message = cause_msg
        self.message = f"Could not initialize Model Environment for Codebook <{self.cb.name}> at {self.path}!"


class PredictionError(Exception):
    def __init__(self):
        self.message = "Critical internal error occurred during prediction!"

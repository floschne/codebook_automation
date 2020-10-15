from api.model import CodebookModel


class ErroneousModelException(Exception):
    def __init__(self, model_id: str = None, cb: CodebookModel = None):
        self.model_id = model_id,
        self.codebook = cb
        self.message = f"Model <{model_id}> for Codebook <{cb.name}> is erroneous!"


class ErroneousMappingException(Exception):
    def __init__(self, cb: CodebookModel = None):
        self.codebook = cb
        self.message = f"Tag-Label-Mapping is erroneous!"


class ModelNotAvailableException(Exception):
    def __init__(self, model_id: str = None, cb: CodebookModel = None):
        self.model_id = model_id,
        self.codebook = cb
        self.message = f"Model <{model_id}> for Codebook <{cb.name}> not available!"


class ModelMetadataNotAvailableException(Exception):
    def __init__(self, model_id: str = None):
        self.model_id = model_id
        self.message = f"Model Metadata for Model <{model_id}> not available!"

class CBAException(Exception):
    def __init__(self, *args, **kwargs):
        super(CBAException, self).__init__(args, kwargs)
        self.message = None

    def __str__(self):
        return self.message


class NoDataForCodebookException(CBAException):
    def __init__(self, cb_name: str = None):
        super(NoDataForCodebookException, self).__init__(cb_name)
        self.codebook = cb_name
        self.message = f"No data for Codebook <{cb_name}> found!"


class ErroneousDatasetException(CBAException):
    def __init__(self, dataset_version: str = None, cb_name: str = None, msg: str = None, caused_by: str = None):
        super(ErroneousDatasetException, self).__init__(dataset_version, cb_name, msg, caused_by)
        self.codebook = cb_name
        self.caused_by = caused_by
        if msg is None:
            self.message = f"Dataset <{dataset_version}> for Codebook <{cb_name}> is erroneous!"
        else:
            self.message = msg

        if caused_by is not None:
            self.message = self.message + f"\n\tDue to: {caused_by}"


class DatasetNotAvailableException(CBAException):
    def __init__(self, dataset_version: str = None, cb_name: str = None):
        super(DatasetNotAvailableException, self).__init__(dataset_version, cb_name)
        self.dataset_version = dataset_version
        self.codebook = cb_name

        self.message = f"Dataset <{dataset_version}> for Codebook <{cb_name}> not available!"


class DatasetMetadataNotAvailableException(CBAException):
    def __init__(self, dataset_version: str = None, cb_name: str = None):
        super(DatasetMetadataNotAvailableException, self).__init__(dataset_version, cb_name)
        self.dataset_version = dataset_version
        self.codebook = cb_name

        self.message = f"Metadata for Dataset <{dataset_version}> for Codebook <{cb_name}> not available!"


class TagLabelMappingNotAvailableException(CBAException):
    def __init__(self, model_version: str = None, cb_name: str = None):
        super(TagLabelMappingNotAvailableException, self).__init__(model_version, cb_name)
        self.model_version = model_version
        self.codebook = cb_name

        self.message = f"TagLabelMapping with version <{model_version}> for Codebook <{cb_name}> not available!"


class InvalidModelIdException(CBAException):
    def __init__(self, model_id: str):
        super(InvalidModelIdException, self).__init__(model_id)
        self.model_id = model_id
        self.message = f"Model ID <{model_id}> is invalid!"


class ErroneousModelException(CBAException):
    def __init__(self, model_version: str = None, cb_name: str = None, msg: str = None):
        super(ErroneousModelException, self).__init__(model_version, cb_name, msg)
        self.codebook = cb_name
        if msg is None:
            self.message = f"Model <{model_version}> for Codebook <{cb_name}> is erroneous!"
        else:
            self.message = msg


class ErroneousMappingException(CBAException):
    def __init__(self, cb_name: str = None):
        super(ErroneousMappingException, self).__init__(cb_name)
        self.codebook = cb_name
        self.message = f"Tag-Label-Mapping is erroneous!"


class ModelNotAvailableException(CBAException):
    def __init__(self, model_version: str = None, cb_name: str = None, model_id: str = None):
        super(ModelNotAvailableException, self).__init__(model_version, cb_name, model_id)
        self.model_version = model_version,
        self.model_id = model_id
        self.codebook = cb_name

        if model_id:
            self.message = f"Model with id <{model_id}> not available!"
        else:
            self.message = f"Model <{model_version}> for Codebook <{cb_name}> not available!"


class ModelMetadataNotAvailableException(CBAException):
    def __init__(self, model_version: str = None, cb_name: str = None, model_id: str = None):
        super(ModelMetadataNotAvailableException, self).__init__(model_version, cb_name, model_id)
        self.model_version = model_version,
        self.model_id = model_id
        self.codebook = cb_name

        if model_id:
            self.message = f"Metadata for Model with id <{model_id}> not available!"
        else:
            self.message = f"Metadata for Model <{model_version}> for Codebook <{cb_name}> not available!"


class ModelInitializationException(CBAException):
    def __init__(self, cb_name: str, path: str, caused_by: str = None):
        super(ModelInitializationException, self).__init__(cb_name, path, caused_by)
        self.cb_name = cb_name
        self.path = path
        self.caused_by = caused_by
        self.message = f"Could not initialize Model Environment for Codebook <{self.cb_name}> at {self.path}!"

        if caused_by is not None:
            self.message = self.message + f"\n\tDue to: {caused_by}"


class PredictionError(CBAException):
    def __init__(self, msg: str = None, ):
        super(PredictionError, self).__init__(msg)
        if msg is None:
            self.message = "Critical internal error occurred during prediction!"
        else:
            self.message = msg


class TFHubEmbeddingException(CBAException):
    def __init__(self, embedding_type: str):
        super(TFHubEmbeddingException, self).__init__(embedding_type)
        self.message = f"Cannot load embedding layer of type <{embedding_type}> from TF Hub!"


class StoringError(CBAException):
    def __init__(self, msg: str = None, caused_by: str = None):
        super(StoringError, self).__init__(msg, caused_by)
        if msg is None:
            self.message = f"Serverside error while storing data!"
        else:
            self.message = msg

        if caused_by is not None:
            self.message = self.message + "\n\tDue to: {caused_by}"


class RedisError(CBAException):
    def __init__(self, msg: str = None):
        super(RedisError, self).__init__(msg)
        self.message = msg

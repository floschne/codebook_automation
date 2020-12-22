export default () => {
  // eslint-disable-next-line no-unused-vars
  class DatasetMetadata {
    constructor (respData) {
      this.codebookName = respData.codebook_name
      this.version = respData.version
      this.labels = respData.labels
      this.numTrainingSamples = respData.num_training_samples
      this.numTestSamples = respData.num_test_samples
    }
  }

  class ModelConfig {
    constructor (respData) {
      this.embeddingType = respData.embedding_type
      this.hiddenUnits = respData.hidden_units
      this.dropout = respData.dropout
      this.ptimizer = respData.optimizer
      this.earlyStopping = respData.early_stopping
      this.activationFn = respData.activation_fn
    }
  }

  // eslint-disable-next-line no-unused-vars
  class ModelMetadata {
    constructor (respData) {
      this.codebookName = respData.codebook_name
      this.version = respData.version
      this.datasetVersion = respData.dataset_version
      this.labels = respData.labels
      this.modelType = respData.model_type
      this.evaluation = respData.evaluation
      this.modelConfig = new ModelConfig(respData.model_config)
    }
  }
}

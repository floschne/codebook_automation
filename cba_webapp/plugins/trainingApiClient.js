export default ({
  app,
  axios
}, inject) => {
  const jsonHeaderConfig = {
    headers: {
      Accept: 'application/json'
    }
  }
  // define the methods
  const trainingApiClient = {
    // TODO refactor signature to be more expressive and readable
    train: async (formData) => {
      let trainingResponse
      try {
        const resp = await app.$axios.post('/api/training/train/', formData, jsonHeaderConfig)
        if (resp.status === 200) {
          trainingResponse = resp.data
        } else {
          trainingResponse = null
        }
      } catch (error) {
        console.error(error)
        trainingResponse = null
      }
      return trainingResponse
    },
    getLog: async (modelId) => {
      let trainingLog
      try {
        const resp = await app.$axios.post('/api/training/log/', {
          model_id: modelId
        }, jsonHeaderConfig)
        if (resp.status === 200) {
          trainingLog = resp.data
        } else {
          trainingLog = null
        }
      } catch (err) {
        console.error(err)
        trainingLog = null
      }
      return trainingLog
    },
    getStatus: async (modelId) => {
      let trainingStatus
      try {
        const resp = await app.$axios.post('/api/training/status/', {
          model_id: modelId
        }, jsonHeaderConfig)
        if (resp.status === 200) {
          trainingStatus = resp.data
        } else {
          trainingStatus = null
        }
      } catch (err) {
        console.error(err)
        trainingStatus = null
      }
      return trainingStatus
    }
  }

  // inject methods so that they can be called in any component or function with this.$modelApiClient.
  inject('trainingApiClient', trainingApiClient)
}

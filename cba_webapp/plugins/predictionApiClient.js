export default ({
                  app,
                  axios
                }, inject) => {
  const jsonHeaderConfig = {
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json;charset=UTF-8',
      "Access-Control-Allow-Origin": "*",
    }
  }
  // define the methods
  const predictionApiClient = {
    // TODO refactor signature to be more expressive and readable
    predictSingleDocument: async (formData) => {
      let predictionResp
      try {
        const resp = await app.$axios.post(`${app.$config.ctxPath}api/prediction/single`, formData, jsonHeaderConfig)
        if (resp.status === 200) {
          predictionResp = resp.data
        } else {
          predictionResp = null
        }
      } catch (error) {
        console.error(error)
        predictionResp = null
      }
      return predictionResp
    }
  }

  // inject methods so that they can be called in any component or function with this.predictionApiClient.
  inject('predictionApiClient', predictionApiClient)
}

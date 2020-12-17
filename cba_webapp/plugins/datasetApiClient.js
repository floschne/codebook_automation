export default ({
  app,
  axios
}, inject) => {
  const jsonHeaderConfig = {
    headers: {
      Accept: 'application/json'
    }
  }
  const multipartHeaderConfig = {
    headers: {
      Accept: 'application/json',
      'content-type': 'multipart/form-data'
    }
  }

  // define the methods
  const datasetApiClient = {
    upload: async (modelFormData) => {
      let success
      try {
        // create form data
        const formData = new FormData()
        formData.append('codebook_name', modelFormData.name)
        formData.append('codebook_tag_list', modelFormData.tags) // TODO
        formData.append('dataset_version', modelFormData.version)
        formData.append('dataset_archive', modelFormData.archive, modelFormData.archive.name)

        const resp = await app.$axios.put('/api/dataset/upload/', formData, multipartHeaderConfig)
        success = resp.data.value
      } catch (err) {
        success = false
        console.error(err)
      }
      return success
    },
    available: async (reqData) => {
      let datasetAvailable
      const dsAvailableReqData = {
        dataset_version: reqData.dataset_version,
        cb: reqData.cb
      }
      try {
        const resp = await app.$axios.post('/api/dataset/available/', dsAvailableReqData, jsonHeaderConfig)
        if (resp.status === 200) {
          datasetAvailable = resp.data.value
        } else {
          datasetAvailable = false
        }
      } catch (error) {
        datasetAvailable = false
        console.error(error)
      }
      return datasetAvailable
    },
    remove: dsFormData => false // TODO
  }

  // inject methods so that they can be called in any component or function with app.$datasetApiClient.
  inject('datasetApiClient', datasetApiClient)
}

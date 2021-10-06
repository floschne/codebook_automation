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
      let metadata = null
      try {
        // create form data
        const formData = new FormData()
        formData.append('cb_name', modelFormData.name)
        formData.append('dataset_version', modelFormData.version)
        formData.append('dataset_archive', modelFormData.archive, modelFormData.archive.name)

        const resp = await app.$axios.put(`${app.$config.ctxPath}api/dataset/upload/`, formData, multipartHeaderConfig)
        metadata = resp.data
      } catch (err) {
        metadata = null
        console.error(err)
      }
      return metadata
    },
    available: async (cbName, dsVersion) => {
      let datasetAvailable = false
      try {
        const resp = await app.$axios.get(`${app.$config.ctxPath}api/dataset/available/?cb_name=${cbName}&dataset_version=${dsVersion}`, jsonHeaderConfig)
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
    metadata: async (cbName, dsVersion) => {
      let metadata = null
      try {
        const resp = await app.$axios.get(`${app.$config.ctxPath}api/dataset/metadata/?cb_name=${cbName}&dataset_version=${dsVersion}`, jsonHeaderConfig)
        if (resp.status === 200) {
          metadata = resp.data
        } else {
          metadata = null
        }
      } catch (error) {
        metadata = false
        console.error(error)
      }
      return metadata
    },
    list: async (cbName) => {
      let datasets = []
      try {
        const resp = await app.$axios.get(`${app.$config.ctxPath}api/dataset/list/?cb_name=${cbName}`, jsonHeaderConfig)
        if (resp.status === 200) {
          datasets = resp.data
        } else {
          datasets = []
        }
      } catch (error) {
        datasets = []
        console.error(error)
      }
      return datasets
    },
    remove: async (cbName, dsVersion) => {
      let success = false
      try {
        const resp = await app.$axios.delete(`${app.$config.ctxPath}api/dataset/remove/?cb_name=${cbName}&dataset_version=${dsVersion}`, jsonHeaderConfig)
        if (resp.status === 200) {
          success = resp.data.value
        } else {
          success = false
        }
      } catch (error) {
        success = false
        console.error(error)
      }
      return success
    }
  }

  // inject methods so that they can be called in any component or function with app.$datasetApiClient.
  inject('datasetApiClient', datasetApiClient)
}

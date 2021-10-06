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
  const modelApiClient = {
    upload: async (modelFormData) => {
      let metadata = null
      try {
        // create form data
        const formData = new FormData()
        formData.append('cb_name', modelFormData.name)
        formData.append('model_version', modelFormData.version)
        formData.append('model_archive', modelFormData.archive, modelFormData.archive.name)

        const resp = await app.$axios.put(`${app.$config.ctxPath}api/models/upload/`, formData, multipartHeaderConfig)
        metadata = resp.data
      } catch (err) {
        metadata = null
        console.error(err)
      }
      return metadata
    },
    available: async (cbName, mVersion) => {
      let modelAvailable = false
      try {
        const resp = await app.$axios.get(`${app.$config.ctxPath}api/model/available/?cb_name=${cbName}&model_version=${mVersion}`, jsonHeaderConfig)
        if (resp.status === 200) {
          modelAvailable = resp.data.value
        } else {
          modelAvailable = false
        }
      } catch (error) {
        modelAvailable = false
        console.error(error)
      }
      return modelAvailable
    },
    metadata: async (cbName, mVersion) => {
      let metadata = null
      try {
        const resp = await app.$axios.get(`${app.$config.ctxPath}api/model/metadata/?cb_name=${cbName}&model_version=${mVersion}`, jsonHeaderConfig)
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
        const resp = await app.$axios.get(`${app.$config.ctxPath}api/model/list/?cb_name=${cbName}`, jsonHeaderConfig)
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
    remove: async (cbName, mVersion) => {
      let success = false
      try {
        const resp = await app.$axios.delete(`${app.$config.ctxPath}api/model/remove/?cb_name=${cbName}&model_version=${mVersion}`, jsonHeaderConfig)
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

  // inject methods so that they can be called in any component or function with this.$modelApiClient.
  inject('modelApiClient', modelApiClient)
}

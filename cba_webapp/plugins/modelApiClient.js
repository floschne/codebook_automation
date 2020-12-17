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
    // TODO refactor signature to be more expressive and readable
    upload: async (formData) => {
      let modelId
      try {
        // create form data
        const reqData = new FormData()
        reqData.append('codebook_name', formData.name)
        reqData.append('codebook_tag_list', formData.tags)
        reqData.append('model_version', formData.version)
        reqData.append('model_archive', formData.archive, formData.archive.name)

        const resp = await app.$axios.put('/api/dataset/upload/', reqData, multipartHeaderConfig)
        if (resp.status === 200) {
          modelId = resp.data.value
        } else {
          modelId = null
        }
      } catch (err) {
        modelId = null
        console.error(err)
      }
      return modelId
    },
    available: async (formData) => {
      let modelAvailable
      try {
        const resp = await app.$axios.post(`/api/model/available/?model_version=${formData.version}`, {
          name: formData.name,
          tags: formData.tags
        }, jsonHeaderConfig)
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
    metadata: async (formData) => {
      try {
        const resp = await app.$axios.post(`/api/model/metadata/?model_version=${formData.version}`, {
          name: formData.name,
          tags: formData.tags
        }, jsonHeaderConfig)
        console.log('akk')
        console.log(JSON.stringify(resp))

        // TODO error handling if not 200
        if (resp.status === 200) {
          return resp.data
        } else {
          return null
        }
      } catch (err) {
        console.error(err) // TODO 404 is not an error in the case there is no model.. change this!
        return null
      }
    },
    remove: formData => false // TODO
  }

  // inject methods so that they can be called in any component or function with this.$modelApiClient.
  inject('modelApiClient', modelApiClient)
}

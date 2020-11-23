<template>
  <div>
    <b-alert v-model="success" variant="success" show dismissible>
      Successfully uploaded dataset!
    </b-alert>
    <b-alert v-model="err" variant="danger" show dismissible>
      Couldn't find Model!
    </b-alert>
    <b-row no-gutters>
      <ModelForm :show-model-upload="true" @model-form-submit="uploadModel" @model-form-reset="reset" />
    </b-row>
  </div>
</template>

<script>
import ModelForm from '@/components/ModelForm'

export default {
  name: 'ModelUpload',
  components: { ModelForm },
  data () {
    return {
      success: Boolean(false),
      err: Boolean(false)
    }
  },
  methods: {
    async uploadModel (modelFormData) {
      // upload file
      const formData = new FormData()
      formData.append('codebook_name', modelFormData.name)
      formData.append('codebook_tag_list', modelFormData.tags)
      formData.append('model_version', modelFormData.version)
      formData.append('model_archive', modelFormData.archive, modelFormData.archive.name)

      const config = {
        headers: {
          Accept: 'application/json',
          'content-type': 'multipart/form-data'
        }
      }
      try {
        const resp = await this.$axios.put('/api/model/upload_for_codebook/', formData, config)
        if (resp.status === 200) { this.success = true } else { this.err = true }
        // TODO handle http 500 etc
      } catch (error) {
        this.err = true
        console.error(error)
      }
    },
    reset () {
      this.success = false
      this.error = false
    }
  }
}
</script>

<style scoped>

</style>

<template>
  <b-card
    header="Dataset Upload"
  >
    <b-alert v-model="success" variant="success" show dismissible>
      Successfully uploaded dataset!
    </b-alert>
    <b-alert v-model="err" variant="danger" show dismissible>
      Couldn't upload dataset!
    </b-alert>
    <ModelForm :show-dataset-upload="true" @model-form-submit="uploadDataset" @model-form-reset="reset" />
  </b-card>
</template>

<script>
import ModelForm from '@/components/ModelForm'

export default {
  name: 'DatasetUpload',
  components: { ModelForm },
  data () {
    return {
      success: Boolean(false),
      err: Boolean(false)
    }
  },
  methods: {
    async uploadDataset (modelFormData) {
      // upload file
      const formData = new FormData()
      formData.append('codebook_name', modelFormData.name)
      formData.append('codebook_tag_list', modelFormData.tags) // TODO
      formData.append('dataset_version', modelFormData.version)
      formData.append('dataset_archive', modelFormData.archive, modelFormData.archive.name)

      console.log(JSON.stringify(formData))
      const config = {
        headers: {
          Accept: 'application/json',
          'content-type': 'multipart/form-data'
        }
      }
      try {
        const resp = await this.$axios.put('/api/training/upload_dataset/', formData, config)
        this.success = resp.data.value
      } catch (error) {
        this.err = true
        console.error(error)
      }
    },
    reset () {
      this.success = false
      this.err = false
    }
  }
}
</script>

<style scoped>

</style>

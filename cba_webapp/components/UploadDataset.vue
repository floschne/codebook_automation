<template>
  <div>
    <b-alert v-model="success" variant="success" show dismissible>
      Successfully uploaded dataset!
    </b-alert>
    <b-alert v-model="error" variant="danger" show dismissible>
      Couldn't upload dataset!
    </b-alert>
    <ModelForm :show-dataset-upload="true" @model-form-submit="uploadDataset" @model-form-reset="reset" />
  </div>
</template>

<script>
import ModelForm from '@/components/ModelForm'

export default {
  name: 'DatasetUpload',
  components: { ModelForm },
  data () {
    return {
      success: Boolean(false)
    }
  },
  computed: {
    error: {
      get () {
        return !this.success
      },
      set (err) {
        this.success = !err
      }
    }
  },
  methods: {
    uploadDataset (modelFormData) {
      this.success = this.$datasetApiClient.upload(modelFormData)
    },
    reset () {
      this.success = false
    }
  }
}
</script>

<style scoped>

</style>

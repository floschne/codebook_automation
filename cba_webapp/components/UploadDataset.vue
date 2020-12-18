<template>
  <div>
    <div v-if="showAlert">
      <b-alert v-model="success" variant="success">
        Successfully uploaded dataset!
      </b-alert>
      <b-alert v-model="error" variant="danger">
        Couldn't upload dataset!
      </b-alert>
    </div>
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
      success: Boolean(false),
      showAlert: Boolean(false)
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
    async uploadDataset (modelFormData) {
      this.success = await this.$datasetApiClient.upload(modelFormData)
      this.showAlert = true
    },
    reset () {
      this.success = false
      this.showAlert = false
    }
  }
}
</script>

<style scoped>

</style>

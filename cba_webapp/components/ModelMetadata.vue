<template>
  <b-card
    header="Model Metadata"
  >
    <b-card-body class="row mt-0 ml-0 pt-0 pl-0">
      <ModelForm class="col-md-6" @model-form-submit="getModelMetadata" @model-form-reset="reset" />
      <div class="col-md-6">
        <pre v-if="show && !error"><code>{{ modelMetaData }}</code></pre>
        <b-alert v-if="!show && !error" variant="info" class="text-center" show>
          Enter Model Data
        </b-alert>

        <b-alert v-if="error" variant="danger" show>
          Cannot find Model!
        </b-alert>
      </div>

      <b-card-body />
    </b-card-body>
  </b-card>
</template>

<script>
import ModelForm from '@/components/ModelForm'

export default {
  name: 'ModelMetadata',
  components: { ModelForm },
  data () {
    return {
      show: Boolean(false),
      error: Boolean(false),
      modelMetaData: Object
    }
  },
  methods: {
    async getModelMetadata (modelFormData) {
      const config = {
        headers: {
          Accept: 'application/json'
        }
      }
      try {
        const resp = await this.$axios.post(`/api/model/get_metadata/?=model_version=${modelFormData.model_version}`, {
          name: modelFormData.name,
          tags: modelFormData.tags
        }, config)
        this.modelMetaData = resp.data
        this.show = true
        this.error = false
      } catch (error) {
        this.show = false
        this.error = true
      }
      this.show = true
    },
    reset () {
      this.show = false
      this.error = false
    }
  }
}
</script>

<style scoped>

</style>

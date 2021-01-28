<template>
  <div>
    <div v-if="showAlert">
      <b-alert v-model="success" variant="success">
        Successfully uploaded {{ model ? 'Model' : 'Dataset' }}!
      </b-alert>
      <b-alert v-model="error" variant="danger">
        Couldn't upload {{ model ? 'Model' : 'Dataset' }}!
      </b-alert>
    </div>

    <b-row>
      <b-col :md="metadata ? 4 : 12">
        <RequestForm
          :model="model"
          :show-version-select="false"
          :show-upload="true"
          :show-version="true"
          @request-form-submit="upload"
          @request-form-reset="reset"
        />
      </b-col>
      <b-col v-if="metadata" md="8">
        <pre class="border border-dark rounded"><code>{{ metadata }}</code></pre>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import RequestForm from '@/components/RequestForm'

export default {
  name: 'Upload',
  components: { RequestForm },
  props: {
    model: {
      type: Boolean,
      default: true
    }
  },
  data () {
    return {
      success: false,
      showAlert: false,
      metadata: null
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
    async upload (modelFormData) {
      this.reset()

      if (this.model === true) {
        this.metadata = await this.$modelApiClient.upload(modelFormData)
      } else {
        this.metadata = await this.$datasetApiClient.upload(modelFormData)
      }

      this.success = this.metaData !== null
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

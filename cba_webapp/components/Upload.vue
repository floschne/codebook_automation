<template>
  <div>
    <div v-if="showAlert">
      <b-alert v-model="success" variant="success">
        Successfully uploaded {{ model ? 'Model' : 'Dataset' }}! <br>
        <i> {{ errorMessage }}</i>
      </b-alert>
      <b-alert v-model="error" variant="danger">
        Couldn't upload {{ model ? 'Model' : 'Dataset' }}! <br>
        <i> {{ errorMessage }}</i>
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
  components: {RequestForm},
  props: {
    model: {
      type: Boolean,
      default: true
    }
  },
  data() {
    return {
      success: false,
      showAlert: false,
      metadata: null,
      errorMessage: null,
    }
  },
  computed: {
    error: {
      get() {
        return !this.success
      },
      set(err) {
        this.success = !err
      }
    }
  },
  methods: {
    async upload(modelFormData) {
      this.reset()

      if (this.model === true) {
        this.metadata = await this.$modelApiClient.upload(modelFormData)
      } else {
        this.metadata = await this.$datasetApiClient.upload(modelFormData)
      }

      if (this.metadata !== null && this.metadata !== undefined) {
        if ('message' in this.metadata) {
          this.success = false
          this.errorMessage = this.metadata.message
        } else
          this.success = true
      } else {
        this.success = false
      }

      this.showAlert = true
    },
    reset() {
      this.success = false
      this.showAlert = false
      this.metadata = null
      this.errorMessage = null
    }
  }
}
</script>

<style scoped>

</style>

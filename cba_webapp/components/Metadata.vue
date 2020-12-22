<template>
  <div>
    <div v-if="showAlarm">
      <b-alert v-model="success" variant="success" class="text-center">
        Successfully retrieved Metadata!
      </b-alert>
      <b-alert v-model="error" variant="danger">
        Cannot find {{ model ? 'Model' : 'Dataset' }} Dataset!
      </b-alert>
    </div>
    <b-row>
      <b-col :md="success ? 6 : 12">
        <RequestForm
          :model="model"
          :show-upload="false"
          :show-version="true"
          :show-version-select="true"
          @request-form-submit="getMetadata"
          @request-form-reset="reset"
        />
      </b-col>

      <b-col v-if="success" md="6" class="mt-sm-2 mt-md-0">
        <pre class="bg-light text-dark p-2 rounded border border-dark"><code>{{ metaData }}</code></pre>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import RequestForm from '@/components/RequestForm'

export default {
  name: 'Metadata',
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
      showAlarm: false,
      metaData: null
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
    async getMetadata (reqFromData) {
      this.reset()
      if (this.model === true) {
        console.log('asdhuoasbdpaähundesphn')
        this.metaData = await this.$modelApiClient.metadata(reqFromData.name, reqFromData.version)
      } else {
        this.metaData = await this.$datasetApiClient.metadata(reqFromData.name, reqFromData.version)
      }

      this.success = this.metaData !== null && this.metaData !== undefined
      this.showAlarm = true
    },
    reset () {
      this.success = false
      this.showAlarm = true
    }
  }
}
</script>

<style scoped>

</style>

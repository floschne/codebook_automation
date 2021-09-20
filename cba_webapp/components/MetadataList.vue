<template>
  <div>
    <div v-if="showAlarm">
      <b-alert v-model="error" variant="danger">
        Cannot find {{ model ? 'Models' : 'Datasets' }} for the provided Codebook name!
      </b-alert>
    </div>
    <b-row>
      <b-col :md="success ? 4 : 12" lg="6">
        <RequestForm
          :model="model"
          :show-upload="false"
          :show-version="false"
          @request-form-submit="getMetadata"
          @request-form-reset="reset"
        />
      </b-col>

      <b-col v-if="success" md="8" lg="6" class="mt-sm-2 mt-md-0 vh-100 overflow-auto">
        <b-row v-for="metaData in metaDataList" :key="metaData.version">
          <pre class="bg-light text-dark p-2 rounded border border-dark w-100"><code>{{ metaData }}</code></pre>
        </b-row>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import RequestForm from '@/components/RequestForm'

export default {
  name: 'MetadataList',
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
      metaDataList: []
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
        this.metaDataList = await this.$modelApiClient.list(reqFromData.name)
      } else {
        this.metaDataList = await this.$datasetApiClient.list(reqFromData.name)
      }

      this.success = this.metaDataList !== null && this.metaDataList !== undefined && this.metaDataList.length > 0
      this.showAlarm = !this.success;
    },
    reset () {
      this.success = false
      this.showAlarm = false
    }
  }
}
</script>

<style scoped>

</style>

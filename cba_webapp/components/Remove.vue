<template>
  <div>
    <div v-if="showAlarm">
      <b-alert v-model="success" variant="success" class="text-center">
        Successfully removed {{ model ? 'Model' : 'Dataset' }}!
      </b-alert>
      <b-alert v-model="error" variant="danger">
        Cannot find {{ model ? 'Model' : 'Dataset' }} Dataset!
      </b-alert>
    </div>
    <b-row>
      <RequestForm
        :model="model"
        :show-version-select="true"
        :show-version="true"
        :show-upload="false"
        @request-form-submit="remove"
        @request-form-reset="reset"
      />
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
      success: Boolean(false),
      showAlarm: Boolean(false),
      metaData: Object
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
    async remove (reqFromData) {
      this.reset()
      if (this.model === true) {
        this.metaData = await this.$modelApiClient.remove(reqFromData.name, reqFromData.version)
      } else {
        this.metaData = await this.$datasetApiClient.remove(reqFromData.name, reqFromData.version)
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

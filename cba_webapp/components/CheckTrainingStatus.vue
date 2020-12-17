<template>
  <div class="container-fluid">
    <div v-if="showAlert">
      <b-alert v-if="error" variant="danger" class="w-100" show dismissible>
        Couldn't find Model-Id!
      </b-alert>
    </div>
    <b-row no-gutters>
      <ModelIdForm @model-id-submit="getTrainingStatus" />
    </b-row>
    <b-row v-if="success">
      <pre class="border border-dark rounded p-1"><code>{{ trainingStatus }}</code></pre>
    </b-row>
  </div>
</template>

<script>
import ModelIdForm from '@/components/ModelIdForm'

export default {
  name: 'CheckTrainingStatus',
  components: { ModelIdForm },
  data () {
    return {
      trainingStatus: null,
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
    async getTrainingStatus (modelId) {
      this.trainingStatus = await this.$trainingApiClient.getStatus(modelId)
      this.success = this.trainingStatus !== null && this.trainingStatus !== undefined
      this.showAlert = true
    }
  }
}
</script>

<style scoped>

</style>

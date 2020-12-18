<template>
  <div>
    <div v-if="showAlert">
      <b-alert v-model="trainingRequestError" variant="danger">
        Couldn't start training!
      </b-alert>
      <b-alert v-model="showDatasetAlert" variant="danger">
        Couldn't find dataset!
      </b-alert>
      <b-alert v-model="showTrainingResponseAlert" variant="success">
        Successfully started training! Use this ID to check Logs or Status:
        <code>{{ trainingResponse }}</code>
      </b-alert>
    </div>
    <b-row>
      <b-col :md="trainingFormData ? 4 : 12">
        <TrainingForm @training-form-submit="setTrainingFromData" />
      </b-col>
      <b-col v-if="trainingFormData" md="8">
        <pre class="border border-dark rounded"><code>{{ trainingFormData }}</code></pre>
      </b-col>
    </b-row>
    <b-row v-if="trainingFormData && datasetAvailable">
      <b-button variant="warning" block @click="startTraining">
        Start Training!
      </b-button>
    </b-row>
  </div>
</template>

<script>
import TrainingForm from '@/components/TrainingForm'
export default {
  name: 'TrainModel',
  components: {
    TrainingForm
  },
  data () {
    return {
      trainingFormData: null,
      trainingResponse: null,
      training_started: Boolean(false),
      trainingRequestError: Boolean(false),
      datasetAvailable: Boolean(false),
      showAlert: Boolean(false)
    }
  },
  computed: {
    showDatasetAlert: {
      get () {
        return this.trainingFormData !== null && !this.datasetAvailable
      },
      set (show) {
        this.showAlert = show
      }
    },
    showTrainingResponseAlert: {
      get () {
        return this.trainingResponse !== null && this.trainingResponse !== undefined && !this.trainingRequestError
      },
      set (show) {
        this.showAlert = show
      }
    }
  },
  methods: {
    async setTrainingFromData (fromData) {
      this.trainingFormData = fromData
      await this.checkDatasetAvailable()
    },
    async checkDatasetAvailable () {
      this.datasetAvailable = await this.$datasetApiClient.available(this.trainingFormData)
      this.showAlert = true
    },
    async startTraining () {
      this.trainingResponse = await this.$trainingApiClient.train(this.trainingFormData)
      this.showAlert = true
      console.log('startTraining+ ' + JSON.stringify(this.trainingResponse) + '   asdasd ' + JSON.stringify(this.showAlert))
      if (this.trainingResponse === null || this.trainingResponse === undefined) {
        this.trainingRequestError = true
        this.trainingFormData = null
      }
    }
  }
}
</script>

<style scoped>

</style>

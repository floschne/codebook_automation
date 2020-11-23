<template>
  <div>
    <b-alert v-if="training_request_error" variant="danger" show>
      Couldn't start training!
    </b-alert>
    <b-alert v-if="training_form_data && !dataset_available" variant="danger" show>
      Couldn't find dataset!
    </b-alert>
    <b-alert v-if="training_response" variant="success" show>
      Successfully started training! Use this ID to check Logs or Status:
      <code>{{ training_response }}</code>
    </b-alert>
    <b-row>
      <b-col :md="training_form_data ? 4 : 12">
        <TrainingForm @training-form-submit="setTrainingFromData" />
      </b-col>
      <b-col v-if="training_form_data" md="8">
        <pre class="border border-dark rounded"><code>{{ training_form_data }}</code></pre>
      </b-col>
    </b-row>
    <b-row v-if="training_form_data && dataset_available">
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
      training_form_data: null,
      training_response: null,
      training_started: false,
      training_request_error: false,
      dataset_available: false
    }
  },
  methods: {
    setTrainingFromData (fromData) {
      this.training_form_data = fromData
      this.checkDatasetAvailable()
    },
    async checkDatasetAvailable () {
      const config = {
        headers: {
          Accept: 'application/json'
        }
      }
      const dsAvailableData = {
        dataset_version_tag: this.training_form_data.dataset_version,
        cb: this.training_form_data.cb
      }
      try {
        const resp = await this.$axios.post('/api/training/dataset_is_available/', dsAvailableData, config)
        if (resp.status === 200) {
          this.dataset_available = resp.data
        } else {
          this.dataset_available = false
        }
      } catch (error) {
        this.dataset_available = false
        console.error(error)
      }
    },
    async startTraining () {
      const config = {
        headers: {
          Accept: 'application/json'
        }
      }
      try {
        const resp = await this.$axios.post('/api/training/train/', this.training_form_data, config)
        if (resp.status === 200) {
          this.training_response = resp.data
        } else {
          this.training_request_error = true
          this.training_form_data = null
        }
      } catch (error) {
        this.training_request_error = true
        this.training_form_data = null
        console.error(error)
      }
    }
  }
}
</script>

<style scoped>

</style>

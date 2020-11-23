<template>
  <div class="container-fluid">
    <b-row no-gutters>
      <b-alert v-if="err" variant="danger" class="w-100" show dismissible>
        Couldn't find Model-Id!
      </b-alert>
      <ModelIdForm @model-id-submit="getTrainingStatus" />
    </b-row>
    <b-row v-if="success">
      <pre class="border border-dark rounded p-1"><code>{{ training_status }}</code></pre>
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
      training_status: null,
      model_id: '',
      success: false,
      err: false
    }
  },
  methods: {
    async getTrainingStatus (modelId) {
      this.model_id = modelId
      const config = {
        headers: {
          Accept: 'application/json'
        }
      }
      try {
        const resp = await this.$axios.post('/api/training/get_training_status/', {
          model_id: this.model_id
        }, config)

        // TODO error handling if not 200
        if (resp.status === 200) {
          this.training_status = resp.data
          this.success = true
          this.err = false
        } else {
          this.training_status = null
          this.success = false
          this.err = true
        }
        console.log(resp)
      } catch (err) {
        console.error(err)
        this.success = false
        this.training_status = null
        this.err = true
      }
    }
  }
}
</script>

<style scoped>

</style>

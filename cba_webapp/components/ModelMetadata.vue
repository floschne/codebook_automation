<template>
  <div>
    <b-alert
      variant="success"
      class="text-center"
      dismissible
      :show="dismissCountdown"
      @dismiss-count-down="countDownChanged"
    >
      Successfully retrieved model data!
    </b-alert>

    <b-alert v-model="err" variant="danger" show dismissible>
      Cannot find Model!
    </b-alert>
    <b-row>
      <b-col :md="success ? 6 : 12">
        <ModelForm @model-form-submit="getModelMetadata" @model-form-reset="reset" />
      </b-col>

      <b-col v-if="success" md="6" class="mt-sm-2 mt-md-0">
        <pre class="bg-light text-dark p-2 rounded border border-dark"><code>{{ metaData }}</code></pre>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import ModelForm from '@/components/ModelForm'

export default {
  name: 'ModelMetadata',
  components: { ModelForm },
  data () {
    return {
      success: Boolean(false),
      err: Boolean(false),
      dismissCountdown: Number(0),
      metaData: Object
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
        this.reset()
        const resp = await this.$axios.post(`/api/model/get_metadata/?=model_version=${modelFormData.version}`, {
          name: modelFormData.name,
          tags: modelFormData.tags
        }, config)

        // TODO error handling if not 200
        if (resp.status === 200) {
          this.metaData = resp.data
          this.success = true
          this.dismissCountdown = 3
        } else {
          this.success = false
          this.err = true
        }
      } catch (error) {
        this.success = false
        this.err = true
      }
    },
    reset () {
      this.success = false
      this.err = false
      this.dismissCountdown = 0
    },
    countDownChanged (dismissCountDown) {
      this.dismissCountdown = dismissCountDown
    }
  }
}
</script>

<style scoped>

</style>

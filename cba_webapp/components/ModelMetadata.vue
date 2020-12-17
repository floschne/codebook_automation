<template>
  <div>
    <div v-if="showAlarm">
      <b-alert v-model="success" variant="success" class="text-center" dismissible>
        Successfully retrieved model data!
      </b-alert>
      <b-alert v-model="error" variant="danger" dismissible>
        Cannot find Model!
      </b-alert>
    </div>
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
    async getModelMetadata (modelFormData) {
      this.reset()
      this.metaData = await this.$modelApiClient.metadata(modelFormData)
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

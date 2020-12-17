<template>
  <div>
    <b-row v-if="showAlarm">
      <b-alert v-model="success" variant="success" dismissible>
        Successfully uploaded model! ModelId: {{ this.modelId }}
      </b-alert>
      <b-alert v-model="error" variant="danger" dismissible>
        Couldn't upload Model!
      </b-alert>
    </b-row>
    <b-row no-gutters>
      <ModelForm :show-model-upload="true" @model-form-submit="uploadModel" @model-form-reset="reset" />
    </b-row>
  </div>
</template>

<script>
import ModelForm from '@/components/ModelForm'

export default {
  name: 'ModelUpload',
  components: { ModelForm },
  data () {
    return {
      modelId: String(''),
      success: Boolean(false),
      showAlarm: Boolean(false)
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
    async uploadModel (modelFormData) {
      this.modelId = await this.$modelApiClient.upload(modelFormData)
      this.success = this.modelId !== null
      this.showAlarm = true
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

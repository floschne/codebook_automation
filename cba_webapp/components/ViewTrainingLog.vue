<template>
  <div class="container-fluid">
    <b-row no-gutters>
      <div v-if="showAlert">
        <b-alert v-model="error" variant="danger" class="w-100">
          Couldn't find Model-Id!
        </b-alert>
      </div>
      <ModelIdForm @model-id-submit="getTrainingLog" />
    </b-row>
    <b-row v-if="success && trainingLog !== null">
      <prism-editor
        v-model="trainingLog"
        class="border border-danger rounded train-log-editor"
        :highlight="highlighter"
        line-numbers
        readonly="true"
      />
    </b-row>
  </div>
</template>

<script>
// import Prism Editor
import { PrismEditor } from 'vue-prism-editor'
import 'vue-prism-editor/dist/prismeditor.min.css' // import the styles somewhere

// import highlighting library (you can use any library you want just return html string)
import { highlight, languages } from 'prismjs/components/prism-core'
import 'prismjs/components/prism-json'
import 'prismjs/themes/prism-twilight.css'
import ModelIdForm from '@/components/ModelIdForm'

export default {
  name: 'ViewTrainingLog',
  components: {
    ModelIdForm,
    PrismEditor
  },
  data () {
    return {
      success: Boolean(false),
      showAlert: Boolean(false),
      trainingLog: null
    }
  },
  computed: {
    error: {
      get () {
        return !this.success
      },
      set (err) {
        this.error = err
      }
    }
  },
  methods: {
    highlighter (code) {
      return highlight(code, languages.json, 'json')
    },
    async getTrainingLog (modelId) {
      this.trainingLog = await this.$trainingApiClient.getLog(modelId)
      this.success = this.trainingLog !== null
      this.showAlert = true
    }
  }
}
</script>

<style scoped>

</style>

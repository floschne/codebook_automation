<template>
  <div class="container-fluid">
    <b-row no-gutters>
      <b-alert v-if="error" variant="danger" class="w-100" show dismissible>
        Couldn't find Model-Id!
      </b-alert>
      <ModelIdForm @model-id-submit="getTrainingLog" />
    </b-row>
    <b-row v-if="success">
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
      success: false,
      trainingLog: null
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
    highlighter (code) {
      return highlight(code, languages.json, 'json')
    },
    getTrainingLog (modelId) {
      this.trainingLog = this.$trainingApiClient.getLog(modelId)
      this.success = this.trainingLog !== null
    }
  }
}
</script>

<style scoped>

</style>

<template>
  <div class="container-fluid">
    <b-row no-gutters>
      <b-alert v-if="err" variant="danger" class="w-100" show dismissible>
        Couldn't find Model-Id!
      </b-alert>
      <ModelIdForm @model-id-submit="getTrainingLog" />
    </b-row>
    <b-row v-if="success">
      <prism-editor
        v-model="training_log"
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
      err: false,
      model_id: '',
      training_log: null,
      training_status: null
    }
  },
  methods: {
    highlighter (code) {
      return highlight(code, languages.json, 'json')
    },
    async getTrainingLog (modelId) {
      this.model_id = modelId
      const config = {
        headers: {
          Accept: 'application/json'
        }
      }
      try {
        const resp = await this.$axios.post('/api/training/get_train_log/', {
          model_id: this.model_id
        }, config)

        // TODO error handling if not 200
        if (resp.status === 200) {
          this.training_log = resp.data
          this.success = true
          this.err = false
        } else {
          this.training_log = null
          this.success = false
          this.err = true
        }
        console.log(resp)
      } catch (err) {
        console.error(err)
        this.success = false
        this.training_log = null
        this.err = true
      }
    }
  }
}
</script>

<style scoped>

</style>

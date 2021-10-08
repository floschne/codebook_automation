<template>
  <b-row>
    <b-col md="12">
      <b-alert v-model="error" variant="danger">
        Error during prediction!
      </b-alert>
    </b-col>

    <b-col v-if="loading" md="12" class="text-center vh-100">
      <b-spinner style="width: 3rem; height: 3rem;" label="Predicting..." variant="primary" class="mt-5"></b-spinner>
      <h3>Prediction in progress...</h3>
    </b-col>
    <b-col v-else :md="success ? 6 : 12">
      <b-form @submit="predict" @reset="reset">
        <!--      CODEBOOK NAME-->
        <b-form-group
          id="label-name"
          label="Name"
          label-for="input-name"
          description="Name of the model/Codebook"
          label-cols-md="4"
          label-cols-lg="2"
        >
          <b-form-input
            id="input-name"
            v-model="form.cb_name"
            placeholder="Enter Codebook name"
            aria-describedby="input-model-name-feedback"
            required
            trim
            :state="nameState"
            @blur="getModelsForCodebook"
          />

          <b-form-invalid-feedback id="input-model-name-feedback">
            Enter at least one character and no whitespaces allowed!
          </b-form-invalid-feedback>
        </b-form-group>

        <!--            MODEL VERSION   -->
        <b-form-group
          id="label-model-version"
          label="Model Version"
          label-for="input-model-version"
          description="Version of the model that will be used for prediction."
          label-cols-md="4"
          label-cols-lg="2"
        >
          <b-form-select
            id="input-model-version"
            v-model="form.model_version"
            :options="modelVersions"
            :state="modelVersionState"
            aria-describedby="input-dataset-version-feedback"
          >
            <!-- This slot appears above the options from 'options' prop -->
            <template #first>
              <b-form-select-option :value="null" disabled>
                -- Please set the Codebook name to show the available Models --
              </b-form-select-option>
            </template>
          </b-form-select>

          <b-form-invalid-feedback id="input-model-version-feedback">
            No whitespaces allowed!
          </b-form-invalid-feedback>
        </b-form-group>

        <!--            DOC TEXT   -->
        <b-form-group
          id="label-doc-text"
          label="Document Text"
          label-for="input-doc-text"
          description="Content of the document for which the labels get predicted!"
          label-cols-md="4"
          label-cols-lg="2"
        >
          <b-form-textarea
            id="input-doc-text"
            v-model="form.doc.text"
            placeholder="Enter some text..."
            rows="5"
            max-rows="10"
          ></b-form-textarea>
        </b-form-group>

        <!--            SUBMIT AND RESET   -->
        <b-button-group size="sm">
          <b-button
            type="submit"
            variant="primary"
            :disabled="!(modelVersionState && nameState)"
          >
            Start Prediction
          </b-button>
          <b-button type="reset" variant="danger">
            Reset
          </b-button>
        </b-button-group>
      </b-form>
    </b-col>
    <b-col v-if="success" md="6" class="mt-sm-2 mt-md-0">
      <pre class="bg-light text-dark p-2 rounded border border-dark"><code>{{ predictions }}</code></pre>
    </b-col>
  </b-row>
</template>

<script>
export default {
  name: "PredictionForm",
  data() {
    return {
      success: false,
      error: false,
      loading: false,
      predictions: null,
      form: {
        cb_name: "",
        model_version: "default",
        doc: {
          doc_id: 0,
          proj_id: 0,
          text: ""
        },
        mapping: null,
      },
      modelsMetadata: []
    }
  },
  computed: {
    modelVersions() {
      return this.modelsMetadata.map(md => md.version)
    },
    modelVersionState() {
      return this.form.model_version.search('\\s') < 0
    },
    nameState() {
      return this.form.cb_name.search('\\s') < 0 && this.form.cb_name.length >= 1
    },
  },
  methods: {
    async predict(evt) {
      evt.preventDefault()

      this.loading = true
      this.predictions = await this.$predictionApiClient.predictSingleDocument(this.form)
      this.loading = false

      this.success = this.predictions !== null && this.predictions !== undefined
      this.error = !this.success
    },
    reset() {
      this.success = false
      this.loading = false
      this.error = false
      this.predictions = null
      this.form = {
        cb_name: "",
        model_version: "default",
        doc: {
          doc_id: 0,
          proj_id: 0,
          text: ""
        },
        mapping: null,
      }
      this.modelsMetadata = []
    },
    async getModelsForCodebook() {
      this.modelsMetadata = await this.$modelApiClient.list(this.form.cb_name)
      if (this.modelsMetadata.length >= 1) {
        this.form.model_version = this.modelsMetadata[0].version
      }
    }
  }
}
</script>

<style scoped>

</style>

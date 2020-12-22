<template>
  <div class="w-100">
    <b-form @submit="onSubmit" @reset="onReset">
      <b-form-group
        id="label-name"
        label="Name:"
        label-for="input-name"
        description="Name of the Codebook"
        label-cols-md="4"
        label-cols-lg="2"
      >
        <b-form-input
          id="input-name"
          v-model="form.name"
          placeholder="Enter Codebook name"
          aria-describedby="input-name-feedback"
          required
          trim
          :state="nameInputState"
          @blur="getMetadata"
        />

        <b-form-invalid-feedback id="input-name-feedback">
          Enter at least one character and no whitespaces allowed!
        </b-form-invalid-feedback>
      </b-form-group>

      <b-form-group
        v-if="showVersionInput && showVersion"
        id="label-version"
        label="Version"
        label-for="input-version"
        description="Version of the model or dataset."
        label-cols-md="4"
        label-cols-lg="2"
      >
        <b-form-input
          id="input-version"
          v-model="form.version"
          type="text"
          placeholder="default"
          aria-describedby="input-version-feedback"
          trim
          :state="versionInputState"
        />

        <b-form-invalid-feedback id="input-version-feedback">
          No whitespaces allowed!
        </b-form-invalid-feedback>
      </b-form-group>

      <b-form-group
        v-if="showVersionSelect && showVersion"
        id="label-dataset-version"
        label="Dataset Version"
        label-for="input-dataset-version"
        description="Version of the model or dataset."
        label-cols-md="4"
        label-cols-lg="2"
      >
        <b-form-select
          id="input-dataset-version"
          v-model="form.version"
          :options="model ? modelVersions : datasetVersions"
          :state="versionInputState"
          aria-describedby="input-dataset-version-feedback"
        >
          <!-- This slot appears above the options from 'options' prop -->
          <template #first>
            <b-form-select-option :value="null" disabled>
              -- Please set the Name to show the available Datasets --
            </b-form-select-option>
          </template>
        </b-form-select>

        <b-form-invalid-feedback id="input-dataset-version-feedback">
          No whitespaces allowed!
        </b-form-invalid-feedback>
      </b-form-group>

      <b-form-group
        v-if="showUpload"
        id="label-upload"
        :label="model ? 'Model Archive' : 'Dataset Archive'"
        label-for="input-upload"
        label-cols-md="4"
        label-cols-lg="2"
      >
        <b-form-file
          v-model="form.archive"
          :state="form.archive"
          placeholder="Choose an archive file or drop it here..."
          drop-placeholder="Drop archive here..."
          accept=".zip, .tar.gz"
          required
        />
        <div v-if="form.archive" class="mt-2 text-muted small">
          Selected file: {{ form.archive ? form.archive.name : '' }}
        </div>

        <b-form-invalid-feedback id="input-upload-feedback">
          Select {{ model ? 'pretrained model' : 'dataset' }} archive!
        </b-form-invalid-feedback>
      </b-form-group>

      <b-button-group size="sm">
        <b-button
          type="submit"
          variant="primary"
          :disabled="!(versionInputState && nameInputState)"
        >
          {{ submitButtonText }}
        </b-button>

        <b-button type="reset" variant="danger">
          Reset
        </b-button>
      </b-button-group>
    </b-form>
  </div>
</template>

<script>
export default {
  name: 'RequestForm',
  emits: ['request-form-data'],
  props: {
    showUpload: {
      type: Boolean,
      default: false
    },
    showVersion: {
      type: Boolean,
      default: true
    },
    showVersionSelect: {
      type: Boolean,
      default: true
    },
    model: {
      type: Boolean,
      default: true
    }
  },
  data () {
    return {
      form: {
        version: 'default',
        name: '',
        archive: null
      },
      datasetsMetadata: [],
      modelsMetadata: []
    }
  },
  computed: {
    showVersionInput () {
      return !this.showVersionSelect
    },
    versionInputState () {
      if (!this.showVersionInput) {
        return true
      } else {
        return this.form.version.search('\\s') < 0 && this.form.version.length >= 1
      }
    },
    nameInputState () {
      return this.form.name.search('\\s') < 0 && this.form.name.length >= 1
    },
    submitButtonText () {
      if (this.showDatasetUpload) {
        return 'Upload Dataset'
      } else if (this.showModelUpload) {
        return 'Upload Model'
      } else {
        return 'Submit'
      }
    },
    datasetVersions () {
      return this.datasetsMetadata.map(md => md.version)
    },
    modelVersions () {
      return this.modelsMetadata.map(md => md.version)
    }
  },
  methods: {
    onSubmit (evt) {
      evt.preventDefault()
      this.$emit('request-form-submit', this.form)
    },
    onReset (evt) {
      evt.preventDefault()
      // Reset form values
      this.form.version = 'default'
      this.form.name = ''
      // Trick to reset/clear native browser form validation state
      this.show = false
      this.$nextTick(() => {
        this.show = true
      })
      this.$emit('request-form-reset', this.form)
    },
    async getDatasetsForCodebook () {
      if (this.showVersionSelect === false) {
        return []
      } else {
        this.datasetsMetadata = await this.$datasetApiClient.list(this.form.name)
        if (this.datasetsMetadata.length >= 1) {
          this.form.version = this.datasetsMetadata[0].version
        }
      }
    },
    async getModelsForCodebook () {
      if (this.showVersionSelect === false) {
        return []
      } else {
        this.modelsMetadata = await this.$modelApiClient.list(this.form.name)
        if (this.modelsMetadata.length >= 1) {
          this.form.version = this.modelsMetadata[0].version
        }
      }
    },
    async getMetadata () {
      if (this.model === true) {
        return await this.getModelsForCodebook()
      } else {
        return await this.getDatasetsForCodebook()
      }
    }
  }
}
</script>

<style scoped>

</style>

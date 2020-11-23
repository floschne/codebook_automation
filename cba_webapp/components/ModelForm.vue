<template>
  <div class="w-100">
    <b-form v-if="show" @submit="onSubmit" @reset="onReset">
      <b-form-group
        id="label-version"
        label="Version"
        label-for="input-version"
        description="Version of the model/dataset."
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
        id="label-name"
        label="Name:"
        label-for="input-name"
        description="Name of the model/Codebook"
        label-cols-md="4"
        label-cols-lg="2"
      >
        <b-form-input
          id="input-name"
          v-model="form.name"
          placeholder="Enter model/Codebook name"
          aria-describedby="input-model-name-feedback"
          required
          trim
          :state="nameInputState"
        />

        <b-form-invalid-feedback id="input-model-name-feedback">
          Enter at least one character and no whitespaces allowed!
        </b-form-invalid-feedback>
      </b-form-group>

      <b-form-group
        id="label-tags"
        label="Tags/Labels"
        label-for="input-tags"
        label-cols-md="4"
        label-cols-lg="2"
        description="Labels of the model / Tags of the Codebook"
      >
        <b-form-tags
          id="input-tags"
          v-model="form.tags"
          input-id="input-tags"
          separator=" ,;"
          placeholder="Enter Tags/Labels separated by comma, semicolon or space"
          aria-describedby="input-tags-feedback"
          :state="tagsInputState"
          remove-on-delete
          required
        />

        <b-form-invalid-feedback id="input-tags-feedback">
          Enter at least two tags!
        </b-form-invalid-feedback>
      </b-form-group>

      <b-form-group
        v-if="showDatasetUpload || showModelUpload"
        id="label-upload"
        :label="showModelUpload ? 'Model Archive' : 'Dataset Archive'"
        label-for="input-upload"
        label-cols-md="4"
        label-cols-lg="2"
      >
        <b-form-file
          v-model="form.archive"
          :state="Boolean(form.archive)"
          placeholder="Choose an archive file or drop it here..."
          drop-placeholder="Drop archive here..."
          accept=".zip, .tar.gz"
          required
        />
        <div v-if="Boolean(form.archive)" class="mt-2 text-muted small">
          Selected file: {{ form.archive ? form.archive.name : '' }}
        </div>

        <b-form-invalid-feedback id="input-upload-feedback">
          Select {{ showModelUpload ? 'pretrained model' : 'dataset' }} archive!
        </b-form-invalid-feedback>
      </b-form-group>

      <b-button-group size="sm">
        <b-button
          type="submit"
          variant="primary"
          :disabled="!(versionInputState && nameInputState && tagsInputState)"
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
  name: 'ModelForm',
  emits: ['model-form-data'],
  props: {
    showModelUpload: Boolean(false),
    showDatasetUpload: Boolean(false)
  },
  data () {
    return {
      form: {
        version: String('default'),
        name: String(''),
        tags: [],
        archive: null
      },
      show: true
    }
  },
  computed: {
    versionInputState () {
      return this.form.version.search('\\s') < 0
    },
    nameInputState () {
      return this.form.name.search('\\s') < 0 && this.form.name.length >= 1
    },
    tagsInputState () {
      return this.form.tags.length >= 2
    },
    submitButtonText () {
      if (this.showDatasetUpload) { return 'Upload Dataset' } else if (this.showModelUpload) { return 'Upload Model' } else { return 'Submit' }
    }
  },
  methods: {
    onSubmit (evt) {
      evt.preventDefault()
      this.$emit('model-form-submit', this.form)
    },
    onReset (evt) {
      evt.preventDefault()
      // Reset form values
      this.form.version = 'default'
      this.form.name = ''
      this.form.tags = []
      // Trick to reset/clear native browser form validation state
      this.show = false
      this.$nextTick(() => {
        this.show = true
      })
      this.$emit('model-form-reset', this.form)
    }
  }
}
</script>

<style scoped>

</style>

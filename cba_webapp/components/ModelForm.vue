<template>
  <div>
    <b-form v-if="show" @submit="onSubmit" @reset="onReset">
      <b-form-group
        id="label-model-version"
        label="Model Version"
        label-for="input-model-version"
        description="Version of the model."
        label-cols-md="4"
        label-cols-lg="2"
      >
        <b-form-input
          id="input-model-version"
          v-model="form.model_version"
          type="text"
          placeholder="default"
          aria-describedby="input-model-version-feedback"
          trim
          :state="noSpaceStateMV"
        />

        <b-form-invalid-feedback id="input-model-version-feedback">
          No whitespaces allowed!
        </b-form-invalid-feedback>
      </b-form-group>

      <b-form-group
        id="label-name"
        label="Name:"
        label-for="input-name"
        description="Name of the model"
        label-cols-md="4"
        label-cols-lg="2"
      >
        <b-form-input
          id="input-name"
          v-model="form.name"
          placeholder="Enter model name"
          aria-describedby="input-model-name-feedback"
          required
          trim
          :state="noSpaceStateN"
        />

        <b-form-invalid-feedback id="input-model-name-feedback">
          Enter at least one character and no whitespaces allowed!
        </b-form-invalid-feedback>
      </b-form-group>

      <b-form-group
        id="label-tags"
        label="Tags"
        label-for="input-tags"
        label-cols-md="4"
        label-cols-lg="2"
      >
        <b-form-tags
          id="input-tags"
          v-model="form.tags"
          input-id="input-tags"
          separator=" ,;"
          placeholder="Enter Tags separated by comma, semicolon or space"
          :state="noSpaceStateT"
          remove-on-delete
          required
        />

        <b-form-invalid-feedback id="input-tags-feedback">
          Enter at least two tags!
        </b-form-invalid-feedback>
      </b-form-group>

      <b-button
        type="submit"
        variant="primary"
        :disabled="!(noSpaceStateMV && noSpaceStateN && noSpaceStateT)"
      >
        Get Metadata
      </b-button>
      <b-button type="reset" variant="danger">
        Reset
      </b-button>
    </b-form>
  </div>
</template>

<script>
export default {
  name: 'ModelForm',
  emits: ['model-form-data'],
  data () {
    return {
      form: {
        model_version: String('default'),
        name: String(''),
        tags: []
      },
      show: true,
      init: true
    }
  },
  computed: {
    noSpaceStateMV () {
      return this.form.model_version.search('\\s') < 0
    },
    noSpaceStateN () {
      return this.form.name.search('\\s') < 0 && this.form.name.length >= 1
    },
    noSpaceStateT () {
      return this.form.tags.length >= 2
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
      this.form.model_version = 'default'
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

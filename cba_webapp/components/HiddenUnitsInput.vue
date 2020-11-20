<template>
  <div>
    <!--      number input + add button-->
    <b-form>
      <b-input-group>
        <b-form-input
          v-model="num_hidden"
          type="number"
          placeholder="Add layer with n hidden units"
          :state="hiddenLayerState"
          @keydown.enter="addLayer"
        />
        <b-input-group-append>
          <b-button variant="primary" @click="addLayer">
            Add
          </b-button>
          <b-button variant="danger" @click="resetLayers">
            Clear
          </b-button>
        </b-input-group-append>

        <b-form-invalid-feedback id="input-hidden-units-feedback">
          Add at least one layer!
        </b-form-invalid-feedback>
      </b-input-group>
    </b-form>

    <!--    layers-->
    <b-badge v-for="(h, idx) in reversed" :key="`layer-${idx}`" variant="secondary" class="mt-1 d-block" pill>
      FC-Layer {{ hidden_units.length - 1 - idx }} with {{ h }} hidden units
    </b-badge>
  </div>
</template>

<script>
export default {
  name: 'HiddenUnitsInput',
  emits: ['added-layer'],
  data () {
    return {
      num_hidden: null,
      hidden_units: [1024, 1024, 512, 64]
    }
  },
  computed: {
    reversed () {
      return this.hidden_units.slice().reverse()
    },
    hiddenLayerState () {
      return this.hidden_units.length >= 1
    }
  },
  methods: {
    addLayer (evt) {
      evt.preventDefault()
      const num = Number.parseInt(this.num_hidden)
      if (Number.isInteger(num)) { this.hidden_units.push(num) }
      this.$emit('added-layer', this.hidden_units)
    },
    resetLayers (evt) {
      evt.preventDefault()
      this.hidden_units = []
      this.num_hidden = null
    }
  }
}
</script>

<style scoped>

</style>

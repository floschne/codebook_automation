<template>
  <div>
    <b-card no-body>
      <b-tabs card class="p-0">
        <b-tab title="Upload Dataset" active>
          <DatasetUpload />
        </b-tab>
        <b-tab title="Train">
          <b-row>
            <b-col :md="training_form_data ? 4 : 12">
              <TrainingForm @training-form-submit="setTrainingFromData" />
            </b-col>
            <b-col v-if="training_form_data" md="8">
              <pre class="border border-dark rounded"><code>{{ training_form_data }}</code></pre>
            </b-col>
          </b-row>
        </b-tab>
      </b-tabs>
    </b-card>
  </div>
</template>

<script>
import DatasetUpload from '@/components/DatasetUpload'
import TrainingForm from '@/components/TrainingForm'
export default {
  name: 'Index',
  components: { TrainingForm, DatasetUpload },
  data () {
    return {
      training_form_data: null
    }
  },
  methods: {
    setTrainingFromData (fromData) {
      this.training_form_data = fromData
    }
  }
}
</script>

<style scoped>

</style>

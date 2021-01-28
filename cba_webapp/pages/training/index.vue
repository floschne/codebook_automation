<template>
  <b-card no-body class="h-100">
    <b-tabs card class="p-0">
      <b-tab title="Train Model" active>
        <TrainModel />
      </b-tab>
      <b-tab title="Training Log">
        <TrainingLog />
      </b-tab>
      <b-tab title="Training Status">
        <TrainingStatus />
      </b-tab>
    </b-tabs>
  </b-card>
</template>

<script>
import TrainModel from '@/components/TrainModel'
import TrainingLog from '@/components/TrainingLog'
import TrainingStatus from '@/components/TrainingStatus'

export default {
  name: 'Index',
  components: {
    TrainingStatus,
    TrainingLog,
    TrainModel
  }
}
</script>

<style scoped>

</style>

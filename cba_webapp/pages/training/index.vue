<template>
  <b-card no-body class="h-100">
    <b-tabs card class="p-0">
      <b-tab title="Upload Dataset" active>
        <UploadDataset />
      </b-tab>
      <b-tab title="Train Model">
        <TrainModel />
      </b-tab>
      <b-tab title="View Training Log">
        <ViewTrainingLog />
      </b-tab>
      <b-tab title="Check Training Status">
        <CheckTrainingStatus />
      </b-tab>
    </b-tabs>
  </b-card>
</template>

<script>
import UploadDataset from '@/components/UploadDataset'
import TrainModel from '@/components/TrainModel'
import ViewTrainingLog from '@/components/ViewTrainingLog'
import CheckTrainingStatus from '@/components/CheckTrainingStatus'

export default {
  name: 'Index',
  components: {
    CheckTrainingStatus,
    ViewTrainingLog,
    TrainModel,
    UploadDataset
  }
}
</script>

<style scoped>

</style>

<template>
  <b-card no-body class="h-100">
    <b-tabs card class="p-0">
      <b-tab title="Metadata" active>
        <ModelMetadata />
      </b-tab>
      <b-tab title="Upload">
        <ModelUpload />
      </b-tab>
    </b-tabs>
  </b-card>
</template>

<script>
import ModelMetadata from '@/components/ModelMetadata'
import ModelUpload from '@/components/ModelUpload'
export default {
  name: 'Index',
  components: { ModelUpload, ModelMetadata }
}
</script>

<style scoped>

</style>

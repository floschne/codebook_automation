<template>
  <div>
    <b-card no-body>
      <b-tabs card class="p-0">
        <b-tab title="Inspect" active>
          <ModelMetadata />
        </b-tab>
        <b-tab title="Upload">
          <ModelUpload />
        </b-tab>
      </b-tabs>
    </b-card>
  </div>
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

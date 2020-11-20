<template>
  <b-card no-body>
    <b-tabs card class="p-0">
      <b-tab title="Inspect" active>
        <b-card-text>
          <ModelMetadata />
        </b-card-text>
      </b-tab>
      <b-tab title="Upload">
        <b-card-text class="p-0 m-0">
          upload model
        </b-card-text>
      </b-tab>
    </b-tabs>
  </b-card>
</template>
<script>
import ModelMetadata from '@/components/ModelMetadata'
export default {
  components: { ModelMetadata }
}
</script>

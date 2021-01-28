<template>
  <b-card no-body class="h-100">
    <b-tabs card class="p-0">
      <b-tab title="Metadata" active>
        <Metadata :model="true" />
      </b-tab>
      <b-tab title="List">
        <MetadataList :model="true" />
      </b-tab>
      <b-tab title="Upload">
        <Upload :model="true" />
      </b-tab>
    </b-tabs>
  </b-card>
</template>

<script>
import Metadata from '@/components/Metadata'
import Upload from '@/components/Upload'
import MetadataList from '@/components/MetadataList'
export default {
  name: 'Index',
  components: { Upload, Metadata, MetadataList }
}
</script>

<style scoped>

</style>

<template>
  <b-card no-body class="h-100">
    <b-tabs card class="p-0">
      <b-tab title="Upload" active>
        <Upload :model="false" />
      </b-tab>
      <b-tab title="Metadata">
        <Metadata :model="false" />
      </b-tab>
      <b-tab title="List">
        <MetadataList :model="false" />
      </b-tab>
      <b-tab title="Remove">
        <Remove :model="false" />
      </b-tab>
    </b-tabs>
  </b-card>
</template>

<script>
import Metadata from '@/components/Metadata'
import Upload from '@/components/Upload'
import MetadataList from '@/components/MetadataList'
import Remove from '@/components/Remove'

export default {
  name: 'Index',
  components: {
    MetadataList,
    Upload,
    Metadata,
    Remove
  }
}
</script>

<style scoped>

</style>

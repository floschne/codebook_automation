<template>
  <div class="container-fluid">
    <h1>Hello from {{ $route.fullPath }}</h1>
    <ModelTabs />
  </div>
</template>

<script>
import ModelTabs from '@/components/ModelTabs'
export default {
  name: 'Index',
  components: { ModelTabs }
}
</script>

<style scoped>

</style>

<template>
  <div>
    <b-button size="sm" pill :variant="heartbeat ? 'success' : 'danger'" @click="checkHeartbeat">
      API Status:
      <span v-if="heartbeat">alive</span>
      <span v-else>dead <b-icon-arrow-repeat /></span>
    </b-button>
  </div>
</template>

<script>
export default {
  name: 'HeartbeatCheck',
  data () {
    return {
      heartbeat: Boolean(false)
    }
  },
  created () {
    this.checkHeartbeat()
  },
  methods: {
    async checkHeartbeat (evt) {
      if (evt !== undefined) { evt.preventDefault() }
      const config = {
        headers: {
          Accept: 'application/json'
        }
      }
      try {
        const resp = await this.$axios.get('/api/heartbeat', config)
        this.heartbeat = resp.data.value
        console.info(`API Heartbeat: ${this.heartbeat}`)
      } catch (error) {
        console.error(error)
      }
    }
  }
}
</script>

<style scoped>

</style>

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
  emits: ['api-dead'],
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
        if (resp.status === 200) { this.heartbeat = resp.data.value } else { this.heartbeat = false }
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

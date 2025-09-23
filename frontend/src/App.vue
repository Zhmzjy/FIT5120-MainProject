<template>
  <div id="app">
    <PasswordProtection
      v-if="!isAuthenticated"
      @authenticated="handleAuthentication"
    />
    <router-view v-else />
  </div>
</template>

<script>
import PasswordProtection from './components/common/PasswordProtection.vue'

export default {
  name: 'App',
  components: {
    PasswordProtection
  },
  data() {
    return {
      isAuthenticated: false
    }
  },
  mounted() {
    this.checkAuthentication()
  },
  methods: {
    checkAuthentication() {
      const authStatus = localStorage.getItem('wildlife_academy_auth')
      const authTime = localStorage.getItem('wildlife_academy_auth_time')

      if (authStatus === 'true' && authTime) {
        const currentTime = Date.now()
        const timeDiff = currentTime - parseInt(authTime)
        const sessionDuration = 24 * 60 * 60 * 1000

        if (timeDiff < sessionDuration) {
          this.isAuthenticated = true
        } else {
          this.clearAuthentication()
        }
      }
    },
    handleAuthentication() {
      this.isAuthenticated = true
    },
    clearAuthentication() {
      localStorage.removeItem('wildlife_academy_auth')
      localStorage.removeItem('wildlife_academy_auth_time')
      this.isAuthenticated = false
    }
  }
}
</script>

<style>
#app {
  width: 100%;
  min-height: 100vh;
  position: relative;
}
</style>

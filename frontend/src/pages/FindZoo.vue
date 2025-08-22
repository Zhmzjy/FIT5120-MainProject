<template>
  <Layout>
    <div class="find-zoo-page">
      <div class="container">
        <h1>Find Zoo</h1>
        <p>This page will feature postcode search functionality to find nearby zoos.</p>
        <Button @click="goHome">Back to Home</Button>
      </div>
    </div>
  </Layout>
</template>

<script>
import Layout from '../components/common/Layout.vue'
import Button from '../components/common/Button.vue'

export default {
  name: 'FindZoo',
  components: {
    Layout,
    Button
  },
  methods: {
    goHome() {
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.find-zoo-page {
  padding: var(--spacing-2xl) 0;
  min-height: 100vh;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 var(--spacing-md);
  text-align: center;
}

h1 {
  color: var(--accent-blue);
  margin-bottom: var(--spacing-lg);
}

p {
  font-size: var(--font-size-lg);
  margin-bottom: var(--spacing-xl);
  color: var(--text-gray);
}
</style>

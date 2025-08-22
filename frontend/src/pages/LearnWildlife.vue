<template>
  <Layout>
    <div class="learn-wildlife-page">
      <div class="container">
        <h1>Learn Wildlife</h1>
        <p>This page will feature the 3D Australia map and wildlife learning content.</p>
        <Button @click="goHome">Back to Home</Button>
      </div>
    </div>
  </Layout>
</template>

<script>
import Layout from '../components/common/Layout.vue'
import Button from '../components/common/Button.vue'

export default {
  name: 'LearnWildlife',
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
.learn-wildlife-page {
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
  color: var(--primary-green);
  margin-bottom: var(--spacing-lg);
}

p {
  font-size: var(--font-size-lg);
  margin-bottom: var(--spacing-xl);
  color: var(--text-gray);
}
</style>

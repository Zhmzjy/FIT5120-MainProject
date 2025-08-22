<template>
  <div class="layout">
    <main class="main-content">
      <slot />
    </main>
  </div>
</template>

<script>
export default {
  name: 'Layout'
}
</script>

<style scoped>
.layout {
  width: 100%;
  min-height: 100vh;
  position: relative;
}

.main-content {
  width: 100%;
  min-height: 100vh;
}
</style>

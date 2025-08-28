<template>
  <div class="right-drawer" :class="{ 'drawer-open': isOpen }">
    <div class="drawer-header">
      <h3>Wildlife Details</h3>
      <button @click="toggleDrawer" class="close-btn">×</button>
    </div>
    <div class="drawer-content">
      <div class="animal-info">
        <div class="animal-placeholder">
          <p>Select an animal to view details</p>
        </div>
      </div>
    </div>
  </div>
  <div v-if="isOpen" class="drawer-overlay" @click="closeDrawer"></div>
</template>

<script>
export default {
  name: 'RightDrawer',
  data() {
    return {
      isOpen: false
    }
  },
  methods: {
    toggleDrawer() {
      this.isOpen = !this.isOpen
    },
    closeDrawer() {
      this.isOpen = false
    }
  }
}
</script>

<style scoped>
.right-drawer {
  position: fixed;
  top: 0;
  right: -400px;
  width: 400px;
  height: 100vh;
  background: white;
  box-shadow: -2px 0 10px rgba(0, 0, 0, 0.1);
  transition: right 0.3s ease;
  z-index: 1000;
  padding: 20px;
}

.drawer-open {
  right: 0;
}

.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #e0e0e0;
}

.drawer-header h3 {
  margin: 0;
  color: #333;
  font-size: 18px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  padding: 0;
  width: 30px;
  height: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.animal-placeholder {
  text-align: center;
  padding: 40px 20px;
  color: #666;
}

.drawer-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
}

@media (max-width: 768px) {
  .right-drawer {
    right: -100vw;
    width: 100vw;
    top: auto;
    bottom: -100vh;
    height: 60vh;
    border-radius: 20px 20px 0 0;
  }

  .drawer-open {
    right: 0;
    bottom: 0;
  }
}
</style>

<template>
  <div class="conservation-header">
    <div class="header-content">
      <h1 class="main-title">Conservation Matters</h1>
      <p class="subtitle">Learn how to protect Australian wildlife</p>

      <div class="intro-section">
        <div class="intro-card">
          <div class="intro-icon">🌿</div>
          <div class="intro-text">
            <h3>Why Conservation is Important</h3>
            <p>Every animal plays a special role in nature. When we protect wildlife, we help keep our planet healthy and beautiful for everyone!</p>
          </div>
        </div>

        <div class="intro-card">
          <div class="intro-icon">🤝</div>
          <div class="intro-text">
            <h3>How You Can Help</h3>
            <p>Even kids can make a big difference! Small actions like recycling, planting trees, and learning about animals help protect wildlife.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ConservationHeader'
}
</script>

<style scoped>
.conservation-header {
  margin-bottom: 48px;
  text-align: center;
}

.header-content {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
}

.main-title {
  font-size: 48px;
  color: #2E7D32;
  margin: 0 0 16px 0;
  font-family: 'Comic Sans MS', cursive, sans-serif;
  font-weight: bold;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
}

.subtitle {
  font-size: 20px;
  color: #1B5E20;
  margin: 0 0 32px 0;
  font-weight: 500;
}

.intro-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  margin-top: 32px;
}

.intro-card {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  text-align: left;
  padding: 20px;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 16px;
  border: 2px solid #E8F5E8;
}

.intro-icon {
  font-size: 32px;
  flex-shrink: 0;
  margin-top: 4px;
}

.intro-text h3 {
  font-size: 18px;
  color: #2E7D32;
  margin: 0 0 8px 0;
  font-family: 'Comic Sans MS', cursive, sans-serif;
}

.intro-text p {
  font-size: 14px;
  color: #424242;
  margin: 0;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .header-content {
    padding: 24px;
  }

  .main-title {
    font-size: 36px;
  }

  .intro-section {
    grid-template-columns: 1fr;
  }

  .intro-card {
    flex-direction: column;
    text-align: center;
    gap: 12px;
  }
}
</style>

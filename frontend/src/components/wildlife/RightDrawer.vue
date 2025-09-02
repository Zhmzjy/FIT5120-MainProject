<template>
  <div class="right-drawer" :class="{ 'drawer-open': isOpen }">
    <div class="drawer-header">
      <h3>Wildlife Explorer</h3>
      <button @click="toggleDrawer" class="close-btn">✕</button>
    </div>
    <div class="drawer-content">
      <div v-if="selectedAnimal" class="animal-info">
        <div class="animal-header">
          <div class="animal-image-container">
            <img 
              v-if="selectedAnimal.image_url" 
              :src="selectedAnimal.image_url" 
              :alt="selectedAnimal.common_name"
              class="animal-image"
              @error="handleImageError"
            />
            <div 
              v-else 
              class="no-image-placeholder"
            >
              <span class="animal-emoji">🐾</span>
              <p>No Image Available</p>
            </div>
            <div 
              class="image-error-placeholder"
              style="display: none;"
            >
              <span class="animal-emoji">📷</span>
              <p>Image Failed to Load</p>
            </div>
          </div>
          <h4>{{ selectedAnimal.common_name }}</h4>
          <p class="scientific-name">{{ selectedAnimal.scientific_name }}</p>
          <div class="conservation-status" :class="getStatusClass(selectedAnimal.conservation_status)">
            {{ selectedAnimal.conservation_status || 'Unknown' }}
          </div>
        </div>
        <div class="animal-details">
          <div class="detail-item">
            <span class="detail-label">Location:</span>
            <span class="detail-value">{{ selectedAnimal.region || selectedAnimal.ibra_region || 'Not specified' }}, {{ selectedAnimal.state || selectedAnimal.state_territory }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Animal Type:</span>
            <span class="detail-value">{{ selectedAnimal.animal_type || 'Unknown' }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Locations Found:</span>
            <span class="detail-value">{{ selectedAnimal.location_count || 'Not recorded' }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Total Observations:</span>
            <span class="detail-value">{{ selectedAnimal.total_observations || 'Not recorded' }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">IBRA Region:</span>
            <span class="detail-value">{{ selectedAnimal.region || selectedAnimal.ibra_region || 'Not specified' }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">State/Territory:</span>
            <span class="detail-value">{{ selectedAnimal.state || selectedAnimal.state_territory || 'Unknown' }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Coordinates:</span>
            <span class="detail-value">
              {{ selectedAnimal.coordinates ? 
                selectedAnimal.coordinates[1].toFixed(4) + ', ' + selectedAnimal.coordinates[0].toFixed(4) : 
                (selectedAnimal.lat && selectedAnimal.lon ? 
                  parseFloat(selectedAnimal.lat).toFixed(4) + ', ' + parseFloat(selectedAnimal.lon).toFixed(4) : 
                  'Not available')
              }}
            </span>
          </div>
        </div>
      </div>
      <div v-else class="animal-placeholder">
        <div class="placeholder-icon">🐾</div>
        <p>Click on a wildlife ping to explore animal data!</p>
        <div class="fun-facts">
          <h4>Discover Australian Wildlife</h4>
          <ul>
            <li>Learn about native species</li>
            <li>Check conservation status</li>
            <li>Explore sighting locations</li>
            <li>View detailed information</li>
          </ul>
        </div>
      </div>
    </div>
    <button v-if="!isOpen" @click="toggleDrawer" class="drawer-toggle">
      Wildlife
    </button>
  </div>
  <div v-if="isOpen" class="drawer-overlay" @click="closeDrawer"></div>
</template>

<script>
export default {
  name: 'RightDrawer',
  props: {
    selectedAnimal: {
      type: Object,
      default: null
    }
  },
  data() {
    return {
      isOpen: false
    }
  },
  watch: {
    selectedAnimal(newAnimal) {
      if (newAnimal) {
        this.isOpen = true
      }
    }
  },
  methods: {
    toggleDrawer() {
      this.isOpen = !this.isOpen
    },
    closeDrawer() {
      this.isOpen = false
      this.$emit('closeDrawer')
    },
    getStatusClass(status) {
      const statusMap = {
        'Critically Endangered': 'status-critical',
        'Endangered': 'status-endangered', 
        'Vulnerable': 'status-vulnerable',
        'Near Threatened': 'status-near-threatened',
        'Least Concern': 'status-least-concern'
      }
      return statusMap[status] || 'status-unknown'
    },
    handleImageError(event) {
      event.target.style.display = 'none'
      const placeholder = event.target.parentElement.querySelector('.image-error-placeholder')
      if (placeholder) {
        placeholder.style.display = 'flex'
      }
    }
  }
}
</script>

<style scoped>
.right-drawer {
  position: fixed;
  top: 0;
  right: -450px;
  width: 450px;
  height: 100vh;
  background-image: url('/images/backformap.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  box-shadow: -4px 0 20px rgba(0, 0, 0, 0.3);
  transition: right 0.3s ease-in-out;
  z-index: 1000;
  padding: 20px;
  font-family: Arial, sans-serif;
  overflow-y: auto;
}

.right-drawer::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(10px);
  z-index: -1;
}

.drawer-open {
  right: 0;
}

.drawer-toggle {
  position: fixed;
  top: 50%;
  right: 16px;
  transform: translateY(-50%);
  background: linear-gradient(135deg, #4a90e2, #27ae60);
  color: white;
  border: none;
  padding: 12px 16px;
  border-radius: 25px;
  font-family: Arial, sans-serif;
  font-weight: bold;
  cursor: pointer;
  z-index: 1001;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  writing-mode: vertical-rl;
  text-orientation: mixed;
}

.drawer-toggle:hover {
  transform: translateY(-50%) scale(1.1);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
}

.drawer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 16px;
  border-bottom: 3px solid #e74c3c;
  background: linear-gradient(90deg, #e74c3c, #f39c12, #3498db);
  background-size: 200% 200%;
  animation: gradientShift 3s ease infinite;
  border-radius: 12px;
}

@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.drawer-header h3 {
  margin: 0;
  color: white;
  font-size: 20px;
  font-weight: bold;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
}

.close-btn {
  background: white;
  border: 2px solid #e74c3c;
  font-size: 18px;
  cursor: pointer;
  padding: 4px;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  color: #e74c3c;
  font-weight: bold;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background: #e74c3c;
  color: white;
  transform: rotate(90deg) scale(1.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.animal-info {
  padding: 20px;
}

.animal-header h4 {
  color: #27ae60;
  margin-bottom: 8px;
  font-size: 24px;
  font-weight: bold;
}

.animal-image-container {
  width: 100%;
  height: 200px;
  margin-bottom: 16px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.animal-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 12px;
}

.no-image-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  border: 2px dashed #dee2e6;
  border-radius: 12px;
}

.animal-emoji {
  font-size: 48px;
  margin-bottom: 8px;
}

.no-image-placeholder p {
  color: #6c757d;
  font-size: 14px;
  margin: 0;
}

.image-error-placeholder {
  width: 100%;
  height: 100%;
  display: none;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  border: 2px dashed #dee2e6;
  border-radius: 12px;
}

.scientific-name {
  color: #7f8c8d;
  font-style: italic;
  margin-bottom: 16px;
  font-size: 16px;
}

.conservation-status {
  display: inline-block;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 20px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-critical {
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  color: white;
}

.status-endangered {
  background: linear-gradient(135deg, #f39c12, #d68910);
  color: white;
}

.status-vulnerable {
  background: linear-gradient(135deg, #f1c40f, #d4ac0d);
  color: #2c3e50;
}

.status-near-threatened {
  background: linear-gradient(135deg, #58d68d, #239b56);
  color: white;
}

.status-least-concern {
  background: linear-gradient(135deg, #27ae60, #1e8449);
  color: white;
}

.status-unknown {
  background: linear-gradient(135deg, #95a5a6, #7f8c8d);
  color: white;
}

.animal-details {
  background: rgba(255, 255, 255, 0.9);
  padding: 20px;
  border-radius: 12px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.detail-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.5);
  border-radius: 8px;
  border-left: 4px solid #27ae60;
}

.detail-label {
  font-weight: bold;
  color: #27ae60;
  min-width: 100px;
  flex-shrink: 0;
}

.detail-value {
  color: #2c3e50;
  text-align: right;
  flex-grow: 1;
  margin-left: 12px;
}

.animal-placeholder {
  text-align: center;
  padding: 40px 20px;
  color: #7f8c8d;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 16px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  border: 2px dashed #3498db;
}

.placeholder-icon {
  font-size: 64px;
  margin-bottom: 20px;
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
  40% { transform: translateY(-10px); }
  60% { transform: translateY(-5px); }
}

.animal-placeholder p {
  font-size: 18px;
  margin-bottom: 24px;
  color: #2c3e50;
  font-weight: bold;
}

.fun-facts {
  text-align: left;
  background: linear-gradient(135deg, #d5f4e6, #fbeee6);
  padding: 20px;
  border-radius: 12px;
  border: 2px solid #27ae60;
}

.fun-facts h4 {
  color: #2c3e50;
  margin: 0 0 16px 0;
  font-size: 18px;
}

.fun-facts ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.fun-facts li {
  margin-bottom: 8px;
  padding: 6px 12px;
  background: white;
  border-radius: 8px;
  border-left: 4px solid #f1c40f;
  font-size: 14px;
  color: #2c3e50;
  transition: all 0.3s ease;
}

.fun-facts li:hover {
  transform: translateX(5px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.drawer-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.3);
  z-index: 999;
  backdrop-filter: blur(2px);
}

@media (max-width: 768px) {
  .right-drawer {
    right: -100vw;
    width: 100vw;
    top: auto;
    bottom: 0;
    height: 70vh;
    border-radius: 16px 16px 0 0;
  }
  
  .drawer-open {
    right: 0;
  }
  
  .drawer-toggle {
    bottom: 20px;
    top: auto;
    transform: none;
    writing-mode: initial;
    text-orientation: initial;
  }
}
</style>

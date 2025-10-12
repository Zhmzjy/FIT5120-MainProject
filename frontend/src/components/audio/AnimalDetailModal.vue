<template>
  <div v-if="isOpen" class="modal-overlay" @click="closeModal">
    <div class="modal-content" @click.stop>
      <button class="close-button" @click="closeModal">×</button>

      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading animal details...</p>
      </div>

      <div v-else-if="error" class="error-state">
        <p>{{ error }}</p>
        <Button @click="closeModal" type="secondary">Close</Button>
      </div>

      <div v-else-if="animalDetails" class="detail-content">
        <div class="detail-header">
          <div class="animal-image">
            <img :src="imageUrl" :alt="animalDetails.commonName" @error="handleImageError" />
          </div>
          <div class="animal-title">
            <h2>{{ animalDetails.commonName }}</h2>
            <p class="scientific-name">{{ animalDetails.scientificName }}</p>
            <span v-if="animalDetails.conservationStatus" class="status-badge">
              {{ animalDetails.conservationStatus }}
            </span>
          </div>
        </div>

        <div class="detail-body">
          <div v-if="animalDetails.description" class="info-section">
            <h3>Description</h3>
            <p>{{ animalDetails.description }}</p>
          </div>

          <div v-if="animalDetails.habitat" class="info-section">
            <h3>Habitat</h3>
            <p>{{ animalDetails.habitat }}</p>
          </div>

          <div v-if="animalDetails.diet" class="info-section">
            <h3>Diet</h3>
            <p>{{ animalDetails.diet }}</p>
          </div>

          <div v-if="animalDetails.funFact" class="info-section fun-fact">
            <h3>Fun Fact</h3>
            <p>{{ animalDetails.funFact }}</p>
          </div>
        </div>

        <div class="modal-actions">
          <Button @click="closeModal" type="primary" size="large">Close</Button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Button from '../common/Button.vue'
import api from '@/services/api'
import { getWikipediaImage } from '@/utils/wikipediaImage.js'

export default {
  name: 'AnimalDetailModal',
  components: {
    Button
  },
  props: {
    isOpen: {
      type: Boolean,
      default: false
    },
    animal: {
      type: Object,
      default: null
    }
  },
  emits: ['close'],
  data() {
    return {
      animalDetails: null,
      imageUrl: null,
      loading: false,
      error: null
    }
  },
  watch: {
    animal: {
      immediate: true,
      async handler(newAnimal) {
        if (newAnimal && this.isOpen) {
          await this.loadAnimalDetails()
        }
      }
    },
    isOpen(newVal) {
      if (newVal && this.animal) {
        this.loadAnimalDetails()
      }
    }
  },
  methods: {
    async loadAnimalDetails() {
      if (!this.animal) return

      this.loading = true
      this.error = null

      try {
        const response = await api.getAnimalDetails(this.animal.commonName)
        this.animalDetails = response

        if (this.animal.imageUrl) {
          this.imageUrl = this.animal.imageUrl
        } else {
          const wikiImage = await getWikipediaImage(this.animal.commonName)
          this.imageUrl = wikiImage || '/images/koala.png'
        }
      } catch (err) {
        console.error('Error loading animal details:', err)
        this.error = 'Failed to load animal details. Please try again.'
      } finally {
        this.loading = false
      }
    },
    handleImageError(event) {
      event.target.src = '/images/koala.png'
    },
    closeModal() {
      this.$emit('close')
    }
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: white;
  border-radius: 16px;
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
}

.close-button {
  position: absolute;
  top: 16px;
  right: 16px;
  width: 40px;
  height: 40px;
  border: none;
  background: rgba(0, 0, 0, 0.1);
  border-radius: 50%;
  font-size: 24px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.3s;
  z-index: 10;
}

.close-button:hover {
  background: rgba(0, 0, 0, 0.2);
}

.loading-state,
.error-state {
  padding: 60px 40px;
  text-align: center;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid #f3f3f3;
  border-top: 4px solid #4299e1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.detail-content {
  padding: 40px;
}

.detail-header {
  display: flex;
  gap: 30px;
  margin-bottom: 30px;
  padding-bottom: 30px;
  border-bottom: 2px solid #e2e8f0;
}

.animal-image {
  flex-shrink: 0;
  width: 200px;
  height: 200px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.animal-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.animal-title {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.animal-title h2 {
  font-size: 2rem;
  color: #2d3748;
  margin: 0 0 8px 0;
}

.scientific-name {
  font-style: italic;
  color: #718096;
  font-size: 1.1rem;
  margin: 0 0 12px 0;
}

.status-badge {
  display: inline-block;
  padding: 6px 12px;
  background: #edf2f7;
  color: #2d3748;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 500;
}

.detail-body {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.info-section {
  background: #f7fafc;
  padding: 20px;
  border-radius: 8px;
}

.info-section h3 {
  font-size: 1.2rem;
  color: #2d3748;
  margin: 0 0 12px 0;
  font-weight: 600;
}

.info-section p {
  color: #4a5568;
  line-height: 1.6;
  margin: 0;
}

.fun-fact {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.fun-fact h3 {
  color: white;
}

.fun-fact p {
  color: rgba(255, 255, 255, 0.95);
}

.modal-actions {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}

@media (max-width: 768px) {
  .modal-content {
    max-height: 95vh;
  }

  .detail-content {
    padding: 30px 20px;
  }

  .detail-header {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .animal-image {
    width: 150px;
    height: 150px;
  }

  .animal-title h2 {
    font-size: 1.5rem;
  }

  .info-section {
    padding: 16px;
  }
}
</style>

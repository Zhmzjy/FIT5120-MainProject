<template>
  <div class="game-result">
    <div class="result-header">
      <div class="result-status" :class="{ correct: isCorrect, incorrect: !isCorrect }">
        <span class="result-icon">{{ isCorrect ? '✅' : '❌' }}</span>
        <h3>{{ isCorrect ? 'Correct!' : 'Incorrect!' }}</h3>
      </div>
    </div>

    <div class="animal-reveal">
      <div class="animal-card">
        <div class="animal-image">
          <img :src="correctAnimal.imageUrl" :alt="correctAnimal.commonName" @click="expandImage" />
        </div>
        <div class="animal-info">
          <h4 class="animal-name">{{ correctAnimal.commonName }}</h4>
          <p class="animal-scientific">{{ correctAnimal.scientificName }}</p>
          <div v-if="!isCorrect && selectedAnimal" class="selected-info">
            <p class="selected-text">You selected: <strong>{{ selectedAnimal.commonName }}</strong></p>
          </div>
        </div>
      </div>
    </div>

    <div class="action-buttons">
      <Button @click="handleNextRound" type="primary" size="large">
        {{ currentRound === totalRounds ? 'End Game' : 'Next Round' }}
      </Button>
      <Button @click="$emit('view-animal', correctAnimal)" type="secondary" size="medium">
        Learn More
      </Button>
    </div>

    <div v-if="showExpandedImage" class="image-modal" @click="closeExpandedImage">
      <div class="modal-content" @click.stop>
        <img :src="correctAnimal.imageUrl" :alt="correctAnimal.commonName" />
        <button class="close-button" @click="closeExpandedImage">×</button>
      </div>
    </div>
  </div>
</template>

<script>
import Button from '../common/Button.vue'

export default {
  name: 'GameResult',
  components: {
    Button
  },
  props: {
    isCorrect: {
      type: Boolean,
      required: true
    },
    correctAnimal: {
      type: Object,
      required: true
    },
    selectedAnimal: {
      type: Object,
      default: null
    },
    currentRound: {
      type: Number,
      required: true
    },
    totalRounds: {
      type: Number,
      required: true
    }
  },
  emits: ['next-round', 'view-animal'],
  data() {
    return {
      showExpandedImage: false,
      nextRoundClicked: false
    }
  },
  methods: {
    expandImage() {
      this.showExpandedImage = true
    },
    closeExpandedImage() {
      this.showExpandedImage = false
    },
    handleNextRound() {
      if (this.nextRoundClicked) return
      this.nextRoundClicked = true
      this.$emit('next-round')

      setTimeout(() => {
        this.nextRoundClicked = false
      }, 1000)
    }
  }
}
</script>

<style scoped>
.game-result {
  background: white;
  border-radius: 12px;
  padding: 24px;
  text-align: center;
}

.result-header {
  margin-bottom: 24px;
}

.result-status {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 16px;
}

.result-status.correct {
  background: #f0fff4;
  border: 2px solid #38a169;
}

.result-status.incorrect {
  background: #fed7d7;
  border: 2px solid #e53e3e;
}

.result-status h3 {
  margin: 0;
  color: #2d3748;
  font-size: 1.3rem;
}

.result-icon {
  font-size: 2rem;
}

.animal-reveal {
  margin-bottom: 24px;
}

.animal-card {
  background: #f7fafc;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 20px;
  max-width: 400px;
  margin: 0 auto;
}

.animal-image {
  flex-shrink: 0;
}

.animal-image img {
  width: 100px;
  height: 100px;
  border-radius: 12px;
  object-fit: cover;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.animal-image img:hover {
  transform: scale(1.05);
}

.animal-info {
  flex: 1;
  text-align: left;
}

.animal-name {
  color: #2d3748;
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 4px;
}

.animal-scientific {
  color: #718096;
  font-style: italic;
  margin-bottom: 8px;
}

.selected-info {
  margin-top: 8px;
}

.selected-text {
  color: #e53e3e;
  font-size: 0.9rem;
  margin: 0;
}

.action-buttons {
  display: flex;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
}

.image-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  position: relative;
  max-width: 90%;
  max-height: 90%;
}

.modal-content img {
  width: 100%;
  height: auto;
  border-radius: 8px;
}

.close-button {
  position: absolute;
  top: -10px;
  right: -10px;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: white;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
}

@media (max-width: 768px) {
  .animal-card {
    flex-direction: column;
    text-align: center;
  }

  .animal-info {
    text-align: center;
  }

  .action-buttons {
    flex-direction: column;
    align-items: center;
  }
}
</style>

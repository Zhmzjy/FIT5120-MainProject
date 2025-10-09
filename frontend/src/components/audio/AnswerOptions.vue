<template>
  <div class="answer-options">
    <h3>Which animal makes this sound?</h3>
    <div class="options-grid">
      <div
        v-for="option in options"
        :key="option.id"
        @click="selectOption(option.id)"
        class="option-card"
        :class="{
          selected: selectedOption === option.id,
          correct: showResult && option.id === correctAnswer,
          incorrect: showResult && selectedOption === option.id && option.id !== correctAnswer,
          disabled: showResult
        }"
      >
        <div class="option-image">
          <img :src="option.imageUrl" :alt="option.commonName" />
        </div>
        <div class="option-info">
          <h4 class="common-name">{{ option.commonName }}</h4>
          <p class="scientific-name">{{ option.scientificName }}</p>
        </div>
        <div v-if="showResult && option.id === correctAnswer" class="result-indicator correct-indicator">
          ✓
        </div>
        <div v-else-if="showResult && selectedOption === option.id && option.id !== correctAnswer" class="result-indicator incorrect-indicator">
          ✗
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AnswerOptions',
  props: {
    options: {
      type: Array,
      required: true
    },
    selectedOption: {
      type: Number,
      default: null
    },
    showResult: {
      type: Boolean,
      default: false
    },
    correctAnswer: {
      type: Number,
      required: true
    }
  },
  emits: ['option-selected'],
  methods: {
    selectOption(optionId) {
      if (this.showResult) return
      this.$emit('option-selected', optionId)
    }
  }
}
</script>

<style scoped>
.answer-options {
  margin-bottom: 24px;
}

.answer-options h3 {
  text-align: center;
  color: #2d3748;
  font-size: 1.3rem;
  margin-bottom: 24px;
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.option-card {
  background: white;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  padding: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  text-align: center;
}

.option-card:hover:not(.disabled) {
  border-color: #4299e1;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(66, 153, 225, 0.15);
}

.option-card.selected {
  border-color: #4299e1;
  background: #ebf8ff;
}

.option-card.correct {
  border-color: #38a169;
  background: #f0fff4;
}

.option-card.incorrect {
  border-color: #e53e3e;
  background: #fed7d7;
}

.option-card.disabled {
  cursor: not-allowed;
}

.option-image {
  width: 80px;
  height: 80px;
  margin: 0 auto 12px;
  border-radius: 8px;
  overflow: hidden;
}

.option-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.option-info {
  text-align: center;
}

.common-name {
  color: #2d3748;
  font-size: 1rem;
  font-weight: 600;
  margin-bottom: 4px;
}

.scientific-name {
  color: #718096;
  font-size: 0.85rem;
  font-style: italic;
  margin: 0;
}

.result-indicator {
  position: absolute;
  top: 8px;
  right: 8px;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  font-weight: bold;
  color: white;
}

.correct-indicator {
  background: #38a169;
}

.incorrect-indicator {
  background: #e53e3e;
}

@media (max-width: 768px) {
  .options-grid {
    grid-template-columns: 1fr;
    gap: 12px;
  }

  .option-card {
    display: flex;
    align-items: center;
    text-align: left;
    padding: 12px;
  }

  .option-image {
    width: 60px;
    height: 60px;
    margin: 0 12px 0 0;
    flex-shrink: 0;
  }

  .option-info {
    flex: 1;
    text-align: left;
  }
}
</style>

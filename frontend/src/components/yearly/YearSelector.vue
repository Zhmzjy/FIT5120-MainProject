<template>
  <div class="year-selector-container">
    <div class="selector-header">
      <div class="mode-toggle">
        <Button
          :class="{ active: mode === 'single' }"
          @click="$emit('mode-changed', 'single')"
          type="secondary"
          size="medium"
        >
          Single Year Analysis
        </Button>
        <Button
          :class="{ active: mode === 'compare' }"
          @click="$emit('mode-changed', 'compare')"
          type="secondary"
          size="medium"
        >
          Compare Years
        </Button>
      </div>
    </div>

    <div class="year-controls">
      <div v-if="mode === 'single'" class="single-year-control">
        <div class="year-input-group">
          <label for="selectedYear">Select Year:</label>
          <select
            id="selectedYear"
            :value="selectedYear"
            @change="$emit('year-changed', parseInt($event.target.value))"
            class="year-select"
          >
            <option v-for="year in availableYears" :key="year" :value="year">
              {{ year }}
            </option>
          </select>
        </div>
      </div>

      <div v-else class="compare-years-control">
        <div class="year-input-group">
          <label for="firstYear">First Year:</label>
          <select
            id="firstYear"
            :value="selectedYear"
            @change="$emit('year-changed', parseInt($event.target.value))"
            class="year-select"
          >
            <option v-for="year in availableYears" :key="year" :value="year">
              {{ year }}
            </option>
          </select>
        </div>

        <div class="vs-indicator">VS</div>

        <div class="year-input-group">
          <label for="secondYear">Second Year:</label>
          <select
            id="secondYear"
            :value="compareYear"
            @change="$emit('compare-year-changed', parseInt($event.target.value))"
            class="year-select"
          >
            <option v-for="year in availableYears" :key="year" :value="year" :disabled="year === selectedYear">
              {{ year }}
            </option>
          </select>
        </div>
      </div>
    </div>

    <div class="action-buttons">
      <Button
        @click="handleAnalyze"
        type="primary"
        size="large"
      >
        Analyze Data
      </Button>
      <Button
        @click="handleReset"
        type="secondary"
        size="medium"
      >
        Reset
      </Button>
    </div>
  </div>
</template>

<script>
import Button from '../common/Button.vue'

export default {
  name: 'YearSelector',
  components: {
    Button
  },
  props: {
    selectedYear: {
      type: Number,
      required: true
    },
    compareYear: {
      type: Number,
      default: null
    },
    mode: {
      type: String,
      default: 'single',
      validator: value => ['single', 'compare'].includes(value)
    },
    availableYears: {
      type: Array,
      required: true
    }
  },
  emits: ['year-changed', 'compare-year-changed', 'mode-changed', 'analyze', 'reset'],
  methods: {
    handleAnalyze() {
      this.$emit('analyze', {
        mode: this.mode,
        selectedYear: this.selectedYear,
        compareYear: this.compareYear
      })
    },
    handleReset() {
      this.$emit('reset')
    }
  }
}
</script>

<style scoped>
.year-selector-container {
  background: rgba(255, 255, 255, 0.95);
  border-radius: var(--border-radius-lg);
  padding: var(--spacing-xl);
  margin-bottom: var(--spacing-xl);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.selector-header {
  margin-bottom: var(--spacing-lg);
}

.mode-toggle {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
}

.mode-toggle .active {
  background: #1e293b !important;
  color: white !important;
  opacity: 1;
}

.year-controls {
  margin-bottom: var(--spacing-xl);
}

.single-year-control {
  display: flex;
  justify-content: center;
}

.compare-years-control {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-lg);
}

.year-input-group {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: var(--spacing-sm);
}

.year-input-group label {
  font-weight: bold;
  color: var(--color-primary);
  font-size: 0.9rem;
}

.year-select {
  padding: var(--spacing-sm) var(--spacing-md);
  border: 2px solid #e2e8f0;
  border-radius: var(--border-radius-md);
  font-size: 1rem;
  background: white;
  cursor: pointer;
  transition: all 0.2s ease;
  min-width: 120px;
}

.year-select:hover {
  border-color: var(--color-primary);
}

.year-select:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.vs-indicator {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--color-primary);
  padding: var(--spacing-sm);
  background: #f1f5f9;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-buttons {
  display: flex;
  gap: var(--spacing-md);
  justify-content: center;
}

@media (max-width: 768px) {
  .mode-toggle {
    flex-direction: column;
    align-items: center;
  }

  .compare-years-control {
    flex-direction: column;
    gap: var(--spacing-md);
  }

  .vs-indicator {
    transform: rotate(90deg);
  }

  .action-buttons {
    flex-direction: column;
    align-items: center;
  }
}
</style>

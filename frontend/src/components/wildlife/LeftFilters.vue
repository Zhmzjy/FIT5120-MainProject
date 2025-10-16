<template>
  <div class="left-filters">
    <div class="filters-header">
      <div class="search-container">
        <input 
          type="text" 
          v-model="searchQuery" 
          @input="onSearchInput"
          @keydown.enter="applyFilters"
          maxlength="30"
          placeholder="Search animals..."
          class="search-bar"
        />
      </div>
    </div>
    <div class="filters-content">
      <div class="filter-group">
        <label>State/Territory</label>
        <select v-model="selectedState" class="cartoon-select" @change="onStateChange">
          <option value="">All States</option>
          <option value="NSW">New South Wales</option>
          <option value="VIC">Victoria</option>
          <option value="QLD">Queensland</option>
          <option value="SA">South Australia</option>
          <option value="WA">Western Australia</option>
          <option value="TAS">Tasmania</option>
          <option value="NT">Northern Territory</option>
          <option value="ACT">Australian Capital Territory</option>
        </select>
      </div>
      <div class="filter-group">
        <label>Conservation Status</label>
        <select v-model="selectedConservationStatus" class="cartoon-select" @change="onConservationChange">
          <option value="">All Status</option>
          <option value="Critically Endangered">Critically Endangered</option>
          <option value="Endangered">Endangered</option>
          <option value="Vulnerable">Vulnerable</option>
          <option value="Present">Present</option>
        </select>
      </div>
      <div class="filter-actions">
        <button class="reset-btn" @click="resetFilters">Reset All</button>
        <button class="apply-btn" @click="applyFilters">Apply Filters</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LeftFilters',
  data() {
    return {
      searchQuery: '',
      selectedState: '',
      selectedConservationStatus: ''
    }
  },
  methods: {
    onSearchInput() {
    },
    onStateChange() {
    },
    onConservationChange() {
    },
    emitCurrentFilters() {
    },
    resetFilters() {
      this.searchQuery = ''
      this.selectedState = ''
      this.selectedConservationStatus = ''
      this.$emit('resetFilters')
    },
    applyFilters() {
      this.$emit('applyFilters', {
        search: this.searchQuery,
        state: this.selectedState,
        conservation: this.selectedConservationStatus
      })
    }
  }
}
</script>

<style scoped>
.left-filters {
  width: 100%;
  height: 100%;
  background: url('/images/backformap.jpg');
  background-size: cover;
  background-position: center;
  background-attachment: fixed;
  filter: brightness(0.8) contrast(1.1);
  padding: var(--spacing-xl);
  font-family: var(--font-family-primary);
  position: relative;
  overflow-y: auto;
}

.filters-header {
  margin-bottom: 3rem;
}

.search-container {
  position: relative;
}

.search-bar {
  width: 100%;
  padding: var(--spacing-md) var(--spacing-lg);
  border: 3px solid #2c5f2d;
  border-radius: var(--border-radius-pill);
  font-size: var(--font-size-md);
  font-family: var(--font-family-primary);
  background: rgba(255, 255, 255, 0.95);
  color: #2d3436;
  cursor: text;
  transition: all 0.3s ease;
  outline: none;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4), 0 2px 8px rgba(0, 0, 0, 0.2);
  font-weight: 600;
}

.search-bar::placeholder {
  color: #636e72;
  font-weight: 500;
}

.search-bar:focus {
  border-color: #4a90e2;
  background: rgba(255, 255, 255, 1);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(74, 144, 226, 0.4), 0 4px 12px rgba(0, 0, 0, 0.3);
}

.search-bar:hover {
  border-color: #357abd;
  background: rgba(255, 255, 255, 0.98);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.35), 0 4px 10px rgba(0, 0, 0, 0.25);
}

.filter-group {
  margin-bottom: 2.5rem;
  background: rgba(255, 255, 255, 0.92);
  padding: var(--spacing-lg);
  border-radius: 12px;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35), 0 3px 10px rgba(0, 0, 0, 0.25);
  border: 3px solid rgba(44, 95, 45, 0.8);
  transition: all 0.3s ease;
}

.filter-group:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4), 0 6px 15px rgba(0, 0, 0, 0.3);
  border-color: #2c5f2d;
  background: rgba(255, 255, 255, 0.96);
}

.filter-group label {
  display: block;
  margin-bottom: var(--spacing-sm);
  font-weight: 700;
  color: #ffffff;
  font-size: 0.85rem;
  text-transform: uppercase;
  letter-spacing: 1px;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
  background: linear-gradient(135deg, #2c5f2d 0%, #1e4620 100%);
  padding: var(--spacing-xs) var(--spacing-md);
  border-radius: 6px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
  border-left: 4px solid #4a7c4e;
}

.cartoon-select {
  width: 100%;
  padding: var(--spacing-sm) var(--spacing-md);
  border: 3px solid rgba(44, 95, 45, 0.6);
  border-radius: var(--border-radius-pill);
  font-size: var(--font-size-sm);
  font-family: var(--font-family-primary);
  background: rgba(255, 255, 255, 0.95);
  color: #2d3436;
  cursor: pointer;
  transition: all 0.3s ease;
  outline: none;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
  font-weight: 600;
}

.cartoon-select:hover {
  border-color: #2c5f2d;
  background: rgba(255, 255, 255, 1);
  transform: translateY(-1px);
  box-shadow: 0 4px 14px rgba(0, 0, 0, 0.3);
}

.cartoon-select:focus {
  border-color: #4a90e2;
  box-shadow: 0 0 0 3px rgba(74, 144, 226, 0.3), 0 4px 14px rgba(0, 0, 0, 0.3);
}

.cartoon-select option {
  background: #ffffff;
  color: #2d3436;
  padding: var(--spacing-sm);
  font-weight: 500;
}

.filter-actions {
  margin-top: 3rem;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
  padding-top: var(--spacing-xl);
}

.reset-btn, .apply-btn {
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: var(--border-radius-pill);
  font-family: var(--font-family-primary);
  font-weight: 700;
  font-size: var(--font-size-sm);
  cursor: pointer;
  transition: all 0.3s ease;
  text-transform: uppercase;
  letter-spacing: 1px;
  border: none;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.reset-btn {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a6f 100%);
  color: #ffffff;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

.reset-btn:hover {
  background: linear-gradient(135deg, #ff5252 0%, #e53e5a 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(255, 107, 107, 0.5);
}

.reset-btn:active {
  transform: translateY(0);
  box-shadow: 0 4px 15px rgba(255, 107, 107, 0.4);
}

.apply-btn {
  background: linear-gradient(135deg, #51cf66 0%, #37b24d 100%);
  color: #ffffff;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);
}

.apply-btn:hover {
  background: linear-gradient(135deg, #40c057 0%, #2f9e44 100%);
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(81, 207, 102, 0.5);
}

.apply-btn:active {
  transform: translateY(0);
  box-shadow: 0 4px 15px rgba(81, 207, 102, 0.4);
}

@media (max-width: 768px) {
  .left-filters {
    padding: var(--spacing-md);
  }
  
  .filter-actions {
    flex-direction: row;
  }
  
  .reset-btn, .apply-btn {
    flex: 1;
  }
}
</style>

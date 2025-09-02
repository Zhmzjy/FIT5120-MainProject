<template>
  <div class="left-filters">
    <div class="filters-header">
      <div class="search-container">
        <input 
          type="text" 
          v-model="searchQuery" 
          @input="onSearchInput"
          placeholder="🔍 Search animals..."
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
        <label>Animal Type</label>
        <select v-model="selectedAnimalType" class="cartoon-select" @change="onAnimalTypeChange">
          <option value="">All Animals</option>
          <option value="Aves">Birds</option>
          <option value="Mammalia">Mammals</option>
          <option value="Insecta">Insects</option>
          <option value="Reptilia">Reptiles</option>
          <option value="Amphibia">Amphibians</option>
          <option value="Plantae">Plants</option>
          <option value="Fungi">Fungi</option>
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
      <div class="filter-group">
        <label>IBRA Region</label>
        <select v-model="selectedRegion" class="cartoon-select" @change="onRegionChange">
          <option value="">All Regions</option>
          <option value="Australian Alps">Australian Alps</option>
          <option value="Sydney Basin">Sydney Basin</option>
          <option value="South Eastern Highlands">South Eastern Highlands</option>
          <option value="NSW North Coast">NSW North Coast</option>
          <option value="Murray Darling Depression">Murray Darling Depression</option>
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
      selectedAnimalType: '',
      selectedConservationStatus: '',
      selectedRegion: ''
    }
  },
  methods: {
    onSearchInput() {
      this.$emit('search', this.searchQuery)
    },
    onStateChange() {
      this.$emit('stateFilter', this.selectedState)
    },
    onAnimalTypeChange() {
      this.$emit('animalTypeFilter', this.selectedAnimalType)
    },
    onConservationChange() {
      this.$emit('conservationFilter', this.selectedConservationStatus)
    },
    onRegionChange() {
      this.$emit('regionFilter', this.selectedRegion)
    },
    resetFilters() {
      this.searchQuery = ''
      this.selectedState = ''
      this.selectedAnimalType = ''
      this.selectedConservationStatus = ''
      this.selectedRegion = ''
      this.$emit('resetFilters')
    },
    applyFilters() {
      this.$emit('applyFilters', {
        search: this.searchQuery,
        state: this.selectedState,
        animalType: this.selectedAnimalType,
        conservation: this.selectedConservationStatus,
        region: this.selectedRegion
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
  padding: var(--spacing-md);
  border: 2px solid rgba(255, 255, 255, 0.6);
  border-radius: var(--border-radius-pill);
  font-size: var(--font-size-md);
  font-family: var(--font-family-primary);
  background: rgba(255, 255, 255, 0.3);
  color: var(--text-dark);
  cursor: text;
  transition: all var(--transition-bounce);
  outline: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  font-weight: bold;
  backdrop-filter: blur(5px);
}

.search-bar::placeholder {
  color: rgba(100, 100, 100, 0.8);
  font-weight: normal;
}

.search-bar:focus {
  border-color: var(--accent-blue);
  background: rgba(255, 255, 255, 0.4);
  transform: scale(1.02);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
}

.search-bar:hover {
  border-color: var(--accent-pink);
  background: rgba(255, 255, 255, 0.35);
}

.filter-group {
  margin-bottom: 2.5rem;
  background: rgba(255, 255, 255, 0.25);
  padding: var(--spacing-lg);
  border-radius: var(--border-radius-lg);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
  border: 2px solid rgba(255, 255, 255, 0.3);
  transition: all var(--transition-bounce);
  backdrop-filter: blur(10px);
}

.filter-group:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px var(--shadow-colorful);
  border-color: var(--accent-pink);
}

.filter-group label {
  display: block;
  margin-bottom: var(--spacing-sm);
  font-weight: bold;
  color: var(--text-white);
  font-size: var(--font-size-sm);
  text-transform: uppercase;
  letter-spacing: 0.5px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
  background: rgba(0, 0, 0, 0.7);
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: var(--border-radius-sm);
}

.cartoon-select {
  width: 100%;
  padding: var(--spacing-sm) var(--spacing-md);
  border: 2px solid rgba(255, 255, 255, 0.4);
  border-radius: var(--border-radius-pill);
  font-size: var(--font-size-sm);
  font-family: var(--font-family-primary);
  background: rgba(255, 255, 255, 0.3);
  color: var(--text-dark);
  cursor: pointer;
  transition: all var(--transition-bounce);
  outline: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  backdrop-filter: blur(5px);
}

.cartoon-select:hover {
  border-color: var(--accent-pink);
  background: rgba(255, 255, 255, 0.4);
  transform: scale(1.02);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.cartoon-select:focus {
  border-color: var(--accent-yellow);
  box-shadow: 0 0 0 3px rgba(255, 211, 61, 0.3);
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
  font-weight: bold;
  font-size: var(--font-size-sm);
  cursor: pointer;
  transition: all var(--transition-bounce);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.reset-btn {
  background: rgba(255, 144, 101, 0.3);
  color: var(--text-white);
  border: 2px solid rgba(255, 144, 101, 0.6);
  box-shadow: 0 4px 12px rgba(255, 144, 101, 0.3);
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(5px);
}

.reset-btn:hover {
  background: rgba(255, 144, 101, 0.5);
  border-color: rgba(255, 144, 101, 0.8);
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 8px 20px rgba(255, 144, 101, 0.4);
}

.apply-btn {
  background: rgba(78, 205, 196, 0.3);
  color: var(--text-white);
  border: 2px solid rgba(78, 205, 196, 0.6);
  box-shadow: 0 4px 12px rgba(78, 205, 196, 0.3);
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(5px);
}

.apply-btn:hover {
  background: rgba(78, 205, 196, 0.5);
  border-color: rgba(78, 205, 196, 0.8);
  transform: translateY(-2px) scale(1.05);
  box-shadow: 0 8px 20px rgba(78, 205, 196, 0.4);
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

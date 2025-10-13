<template>
  <div class="species-search">
    <div class="search-header">
      <h3>Search Species Trend</h3>
      <p>Enter a species name to view its population trend over time</p>
    </div>

    <div class="search-input-container">
      <input
        v-model="searchQuery"
        @input="handleSearch"
        @focus="showSuggestions = true"
        type="text"
        placeholder="Type species name (e.g., Koala, Rainbow Lorikeet)"
        class="search-input"
        maxlength="30"
      />

      <div v-if="showSuggestions && filteredSpecies.length > 0" class="suggestions-dropdown">
        <div
          v-for="species in filteredSpecies"
          :key="species.taxonId"
          @click="selectSpecies(species)"
          class="suggestion-item"
        >
          <img :src="species.imageUrl" :alt="species.commonName" class="species-thumb" />
          <div class="species-info">
            <div class="common-name">{{ species.commonName }}</div>
            <div class="scientific-name">{{ species.scientificName }}</div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="loading" class="search-loading">
      <div class="loading-spinner"></div>
      <p>Searching species...</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SpeciesSearch',
  emits: ['species-selected'],
  data() {
    return {
      searchQuery: '',
      showSuggestions: false,
      loading: false,
      allSpecies: [
        {
          taxonId: 1,
          commonName: 'Rainbow Lorikeet',
          scientificName: 'Trichoglossus moluccanus',
          imageUrl: '/images/koala.png'
        },
        {
          taxonId: 2,
          commonName: 'Australian Magpie',
          scientificName: 'Gymnorhina tibicen',
          imageUrl: '/images/kangaroo.png'
        },
        {
          taxonId: 3,
          commonName: 'Koala',
          scientificName: 'Phascolarctos cinereus',
          imageUrl: '/images/koala.png'
        },
        {
          taxonId: 4,
          commonName: 'Kangaroo',
          scientificName: 'Osphranter rufus',
          imageUrl: '/images/kangaroo.png'
        },
        {
          taxonId: 5,
          commonName: 'Tasmanian Devil',
          scientificName: 'Sarcophilus harrisii',
          imageUrl: '/images/koala.png'
        },
        {
          taxonId: 6,
          commonName: 'Bilby',
          scientificName: 'Macrotis lagotis',
          imageUrl: '/images/kangaroo.png'
        }
      ]
    }
  },
  computed: {
    filteredSpecies() {
      if (!this.searchQuery.trim()) return []

      const query = this.searchQuery.toLowerCase()
      return this.allSpecies.filter(species =>
        species.commonName.toLowerCase().includes(query) ||
        species.scientificName.toLowerCase().includes(query)
      ).slice(0, 5)
    }
  },
  methods: {
    handleSearch() {
      this.showSuggestions = true
    },
    selectSpecies(species) {
      this.searchQuery = species.commonName
      this.showSuggestions = false
      this.$emit('species-selected', species)
    }
  },
  mounted() {
    document.addEventListener('click', (e) => {
      if (!this.$el.contains(e.target)) {
        this.showSuggestions = false
      }
    })
  }
}
</script>

<style scoped>
.species-search {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  position: relative;
  border: 2px solid transparent;
  background-image: linear-gradient(white, white), linear-gradient(135deg, #A2E2A2, #DFF8DF);
  background-origin: border-box;
  background-clip: padding-box, border-box;
}

.search-header h3 {
  margin: 0 0 8px 0;
  color: #2d3748;
  font-size: 20px;
  font-weight: 600;
}

.search-header p {
  margin: 0 0 20px 0;
  color: #718096;
  font-size: 14px;
}

.search-input-container {
  position: relative;
}

.search-input {
  width: 100%;
  padding: 12px 16px;
  border: 2px solid #A2E2A2;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #77BFA3;
  box-shadow: 0 0 0 3px rgba(119, 191, 163, 0.2);
}

.suggestions-dropdown {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border: 2px solid #A2E2A2;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 1000;
  max-height: 300px;
  overflow-y: auto;
  margin-top: 4px;
}

.suggestion-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.suggestion-item:hover {
  background-color: #EAF6EA;
}

.species-thumb {
  width: 40px;
  height: 40px;
  border-radius: 6px;
  object-fit: cover;
  margin-right: 12px;
  border: 1px solid #A2E2A2;
}

.species-info {
  flex: 1;
}

.common-name {
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 2px;
}

.scientific-name {
  font-size: 12px;
  color: #718096;
  font-style: italic;
}

.search-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid #A2E2A2;
  border-top: 2px solid #77BFA3;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-right: 8px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>

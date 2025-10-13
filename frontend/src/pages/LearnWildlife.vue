<template>
  <div class="wildlife-app">
    <div class="background-wrapper">
      <img src="/images/backformap.jpg" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1; filter: brightness(0.8) contrast(1.1);" alt="background">
    </div>

    <TopNavigation @toggleMobileMenu="toggleMobileSidebar" />

    <div class="main-layout">
      <aside class="left-sidebar" :class="{ 'mobile-open': mobileMenuOpen }">
        <LeftFilters 
          @applyFilters="handleApplyFilters"
          @resetFilters="handleResetFilters"
        />
      </aside>

      <main class="center-content">
        <MapView 
          ref="mapViewRef"
          :filters="activeFilters"
          :isLoading="isLoading"
          @regionSelected="handleRegionSelection"
          @loadingStateChange="handleLoadingStateChange"
        />
      </main>

      <RightDrawer 
        :regionData="selectedRegion"
        @closeDrawer="handleCloseDrawer"
      />
    </div>

    <div v-if="mobileMenuOpen" class="mobile-overlay" @click="closeMobileSidebar"></div>
  </div>
</template>

<script>
import MapView from '../components/wildlife/MapView.vue'
import LeftFilters from '../components/wildlife/LeftFilters.vue'
import RightDrawer from '../components/wildlife/RightDrawer.vue'
import Button from '../components/common/Button.vue'
import TopNavigation from '../components/common/TopNavigation.vue'

export default {
  name: 'LearnWildlife',
  components: {
    MapView,
    LeftFilters,
    RightDrawer,
    Button,
    TopNavigation
  },
  data() {
    return {
      mobileMenuOpen: false,
      activeFilters: {
        search: '',
        state: '',
        conservation: '',
        region: ''
      },
      selectedRegion: null,
      isLoading: false
    }
  },
  methods: {
    goHome() {
      this.$router.push('/')
    },
    showSeasonalWildlife() {
      this.$router.push('/seasonal')
    },
    toggleMobileSidebar() {
      this.mobileMenuOpen = !this.mobileMenuOpen
    },
    closeMobileSidebar() {
      this.mobileMenuOpen = false
    },
    handleResetFilters() {
      this.activeFilters = {
        search: '',
        state: '',
        conservation: '',
        region: ''
      }
      this.selectedRegion = null
      this.$nextTick(() => {
        if (this.$refs.mapViewRef) {
          this.$refs.mapViewRef.loadData()
        }
      })
    },
    handleApplyFilters(filters) {
      this.activeFilters = { ...filters }
      this.$nextTick(() => {
        if (this.$refs.mapViewRef) {
          this.$refs.mapViewRef.loadData()
        }
      })
    },
    handleRegionSelection(regionInfo) {
      this.selectedRegion = regionInfo
    },
    handleCloseDrawer() {
      this.selectedRegion = null
    },
    handleLoadingStateChange(loading) {
      this.isLoading = loading
    },
    goToWildlife() {
      if (this.$route.path === '/learn-wildlife') {
        return;
      }
      this.$router.push('/learn-wildlife')
    },
    goToSeasonal() {
      this.$router.push('/seasonal')
    },
    goToAIChallenge() {
      this.$router.push('/ai-challenge')
    },
    goToDailyWildle() {
      this.$router.push('/daily-wildle')
    },
    goToConservation() {
      this.$router.push('/conservation')
    }
  }
}
</script>

<style scoped>
.wildlife-app {
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  gap: 0;
  border: none;
  margin: 0;
  padding: 0;
}

.background-wrapper {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
  z-index: -1;
}

.main-layout {
  flex: 1;
  display: flex;
  overflow: hidden;
  gap: 0;
  border: none;
}

.left-sidebar {
  width: 320px;
  flex-shrink: 0;
  background: transparent;
  overflow-y: auto;
  border: none;
}

.center-content {
  flex: 1;
  background: transparent;
  overflow: hidden;
  padding: 20px;
}

.mobile-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  z-index: 150;
}

@media (max-width: 768px) {
  .left-sidebar {
    position: fixed;
    top: 70px;
    left: -320px;
    height: calc(100vh - 70px);
    z-index: 200;
    transition: left 0.3s ease;
    box-shadow: 2px 0 10px rgba(0, 0, 0, 0.1);
  }

  .left-sidebar.mobile-open {
    left: 0;
  }

  .center-content {
    width: 100%;
    padding: 10px;
  }
}

@media (max-width: 480px) {
  .center-content {
    padding: 5px;
  }
}
</style>

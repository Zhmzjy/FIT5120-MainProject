<template>
  <div class="map-view">
    <div v-if="errorMessage" class="error-container">
      <div class="error-content">
        <h3>Map Unavailable</h3>
        <p>{{ errorMessage }}</p>
        <small>Please check your Mapbox configuration</small>
      </div>
    </div>
    <div v-else class="map-wrapper">
      <div id="mapbox-container" ref="mapContainer" class="map-container"></div>
    </div>
  </div>
</template>

<script>
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'

export default {
  name: 'MapView',
  data() {
    return {
      map: null,
      errorMessage: null
    }
  },
  mounted() {
    this.initializeMap()
  },
  beforeUnmount() {
    if (this.map) {
      this.map.remove()
    }
  },
  methods: {
    initializeMap() {
      const token = import.meta.env.VITE_MAPBOX_TOKEN

      if (!token || token === 'your_mapbox_access_token_here') {
        this.errorMessage = 'Mapbox access token is not configured. Please add your token to the .env file.'
        return
      }

      try {
        mapboxgl.accessToken = token

        this.map = new mapboxgl.Map({
          container: this.$refs.mapContainer,
          style: 'mapbox://styles/jzhu0117/cmf1y5jkk005i01r498d1dzpe',
          projection: 'globe',
          center: [134.5, -25],
          zoom: 3.5
        })

        this.map.addControl(new mapboxgl.NavigationControl(), 'top-right')

        this.map.on('error', (error) => {
          console.error('Mapbox error:', error)
          this.errorMessage = 'Failed to load the map. Please check your internet connection and Mapbox token.'
        })

      } catch (error) {
        console.error('Map initialization error:', error)
        this.errorMessage = 'Failed to initialize the map. Please check your Mapbox configuration.'
      }
    }
  }
}
</script>

<style scoped>
.map-view {
  width: 100%;
  height: 100%;
  position: relative;
}

.map-wrapper {
  width: 100%;
  height: 100%;
  position: relative;
}

.map-container {
  width: 100%;
  height: 100%;
  border-radius: 8px;
  overflow: hidden;
}

.error-container {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
  border-radius: 8px;
  border: 2px dashed #dee2e6;
}

.error-content {
  text-align: center;
  padding: 40px 20px;
  max-width: 400px;
}

.error-content h3 {
  margin: 0 0 12px 0;
  color: #6c757d;
  font-size: 18px;
}

.error-content p {
  margin: 0 0 8px 0;
  color: #6c757d;
  font-size: 14px;
  line-height: 1.5;
}

.error-content small {
  color: #adb5bd;
  font-size: 12px;
}
</style>

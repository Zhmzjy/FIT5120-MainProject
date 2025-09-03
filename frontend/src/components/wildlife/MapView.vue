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
import ApiService from '@/services/api.js'

export default {
  name: 'MapView',
  props: {
    filters: {
      type: Object,
      default: () => ({})
    }
  },
  emits: ['animalSelected'],
  data() {
    return {
      map: null,
      errorMessage: null,
      observations: []
    }
  },
  watch: {
    filters: {
      handler() {
        this.loadMapData()
      },
      deep: true
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
    async initializeMap() {
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

        this.map.on('load', () => {
          this.loadMapData()
        })

        this.map.on('error', (error) => {
          console.error('Mapbox error:', error)
          this.errorMessage = 'Failed to load the map. Please check your internet connection and Mapbox token.'
        })

      } catch (error) {
        console.error('Map initialization error:', error)
        this.errorMessage = 'Failed to initialize the map. Please check your Mapbox configuration.'
      }
    },

    async loadMapData() {
      if (!this.map || !this.map.isStyleLoaded()) return

      try {
        await this.loadObservations()
      } catch (error) {
        console.error('Failed to load map data:', error)
      }
    },

    async loadObservations() {
      try {
        const params = {
          limit: 200000
        }

        if (this.filters.state) params.state = this.filters.state
        if (this.filters.animalType) params.animal_type = this.filters.animalType
        if (this.filters.conservation) params.conservation_status = this.filters.conservation
        if (this.filters.region) params.region = this.filters.region
        if (this.filters.search) params.search = this.filters.search

        const response = await ApiService.getObservations(params)
        console.log("backend back:", response.total, response.observations.length)  
        const observations = response.observations || []

        this.observations = observations
        this.addObservationMarkers()
      } catch (error) {
        console.error('Failed to load observations:', error)
      }
    },

    aggregateBySpecies(observations) {
      const speciesMap = new Map()
      
      observations.forEach(obs => {
        const speciesKey = `${obs.scientific_name}|${obs.animal_type}|${obs.conservation_status}`
        
        if (speciesMap.has(speciesKey)) {
          const existing = speciesMap.get(speciesKey)
          existing.location_count += 1
          existing.total_observations += obs.occurrence_count || 1
          
          if (!existing.locations.some(loc => 
            Math.abs(parseFloat(loc.lat) - parseFloat(obs.lat)) < 0.005 && 
            Math.abs(parseFloat(loc.lon) - parseFloat(obs.lon)) < 0.005
          )) {
            existing.locations.push({
              lat: obs.lat,
              lon: obs.lon,
              state_territory: obs.state_territory,
              ibra_region: obs.ibra_region,
              conservation_status: obs.conservation_status,
              animal_type: obs.animal_type
            })
          }
        } else {
          speciesMap.set(speciesKey, {
            scientific_name: obs.scientific_name,
            common_name: obs.common_name,
            animal_type: obs.animal_type,
            conservation_status: obs.conservation_status,
            image_url: obs.image_url,
            location_count: 1,
            total_observations: obs.occurrence_count || 1,
            locations: [{
              lat: obs.lat,
              lon: obs.lon,
              state_territory: obs.state_territory,
              ibra_region: obs.ibra_region,
              conservation_status: obs.conservation_status,
              animal_type: obs.animal_type
            }]
          })
        }
      })
      
      return Array.from(speciesMap.values()).flatMap(species => 
        species.locations.map(location => ({
          scientific_name: species.scientific_name,
          common_name: species.common_name,
          animal_type: location.animal_type,
          conservation_status: location.conservation_status,
          image_url: species.image_url,
          lat: location.lat,
          lon: location.lon,
          state_territory: location.state_territory,
          ibra_region: location.ibra_region,
          location_count: species.location_count,
          total_observations: species.total_observations
        }))
      )
    },

    addObservationMarkers() {
      try {
        const layersToRemove = ['animal-points', 'animal-labels']
        
        layersToRemove.forEach(layerId => {
          if (this.map.getLayer(layerId)) {
            this.map.removeLayer(layerId)
          }
        })
        
        if (this.map.getSource('observations')) {
          this.map.removeSource('observations')
        }

        if (!this.observations || this.observations.length === 0) {
          return
        }

        const geojson = {
          type: 'FeatureCollection',
          features: this.observations.map((obs, index) => {
            const baseCoords = [parseFloat(obs.lon), parseFloat(obs.lat)]
            const offset = 0.002
            const randomOffset = [
              (Math.random() - 0.5) * offset,
              (Math.random() - 0.5) * offset
            ]
            
            return {
              type: 'Feature',
              geometry: {
                type: 'Point',
                coordinates: [
                  baseCoords[0] + randomOffset[0],
                  baseCoords[1] + randomOffset[1]
                ]
              },
              properties: {
                common_name: obs.common_name,
                scientific_name: obs.scientific_name,
                conservation_status: obs.conservation_status,
                state: obs.state_territory,
                state_territory: obs.state_territory,
                region: obs.ibra_region,
                ibra_region: obs.ibra_region,
                location_count: obs.location_count,
                total_observations: obs.total_observations,
                animal_type: obs.animal_type,
                image_url: obs.image_url,
                lat: parseFloat(obs.lat),
                lon: parseFloat(obs.lon)
              }
            }
          })
        }

        this.map.addSource('observations', {
          type: 'geojson',
          data: geojson
        })

        this.map.addLayer({
          id: 'animal-points',
          type: 'circle',
          source: 'observations',
          paint: {
            'circle-radius': [
              'interpolate',
              ['linear'],
              ['zoom'],
              5, 4,
              10, 8,
              15, 12
            ],
            'circle-color': [
              'case',
              ['==', ['get', 'conservation_status'], 'Critically Endangered'], '#ff4444',
              ['==', ['get', 'conservation_status'], 'Endangered'], '#ff8800',
              ['==', ['get', 'conservation_status'], 'Vulnerable'], '#ffcc00',
              '#44aa44'
            ],
            'circle-stroke-width': 3,
            'circle-stroke-color': '#ffffff',
            'circle-opacity': 0.9
          }
        })

        this.map.addLayer({
          id: 'animal-labels',
          type: 'symbol',
          source: 'observations',
          layout: {
            'text-field': '🐾',
            'text-size': [
              'interpolate',
              ['linear'],
              ['zoom'],
              5, 10,
              10, 14,
              15, 18
            ],
            'text-allow-overlap': true,
            'text-ignore-placement': true
          },
          paint: {
            'text-opacity': 0.8
          }
        })

        this.setupClickHandlers()
      } catch (error) {
        console.error('Error adding observation markers:', error)
      }
    },

    setupClickHandlers() {
      this.map.off('click', 'animal-points')
      this.map.off('mouseenter', 'animal-points')
      this.map.off('mouseleave', 'animal-points')
      
      this.map.on('click', 'animal-points', (e) => {
        const clickedProperties = e.features[0].properties
        const clickedCoordinates = e.features[0].geometry.coordinates
        const searchRadius = 0.01
        
        const nearbyAnimals = this.observations.filter(obs => {
          const distance = Math.sqrt(
            Math.pow(parseFloat(obs.lat) - clickedCoordinates[1], 2) + 
            Math.pow(parseFloat(obs.lon) - clickedCoordinates[0], 2)
          )
          return distance <= searchRadius
        })
        
        const regionInfo = {
          clickedAnimal: {
            common_name: clickedProperties.common_name,
            scientific_name: clickedProperties.scientific_name,
            conservation_status: clickedProperties.conservation_status,
            animal_type: clickedProperties.animal_type,
            image_url: clickedProperties.image_url
          },
          location: {
            lat: clickedCoordinates[1],
            lon: clickedCoordinates[0],
            region: clickedProperties.region,
            state: clickedProperties.state
          },
          animals: nearbyAnimals.map(animal => ({
            common_name: animal.common_name,
            scientific_name: animal.scientific_name,
            conservation_status: animal.conservation_status,
            animal_type: animal.animal_type,
            image_url: animal.image_url,
            total_observations: animal.total_observations,
            latitude: animal.lat,
            longitude: animal.lon,
            count: animal.total_observations
          })),
          totalSpecies: nearbyAnimals.length,
          uniqueSpecies: new Set(nearbyAnimals.map(a => a.scientific_name)).size
        }
        
        this.$emit('regionSelected', regionInfo)
      })

      this.map.on('mouseenter', 'animal-points', () => {
        this.map.getCanvas().style.cursor = 'pointer'
      })

      this.map.on('mouseleave', 'animal-points', () => {
        this.map.getCanvas().style.cursor = ''
      })
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
  display: flex;
  align-items: center;
  justify-content: center;
}

.map-container {
  width: 90%;
  height: 90%;
  max-width: 1200px;
  max-height: 800px;
  border-radius: var(--border-radius-xl);
  overflow: hidden;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
  position: relative;
  margin: auto;
}

.error-container {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.1);
}

.error-content {
  text-align: center;
  padding: var(--spacing-xl);
  background: white;
  border-radius: var(--border-radius-lg);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.error-content h3 {
  margin: 0 0 var(--spacing-md) 0;
  color: var(--color-error);
}

.error-content p {
  margin: 0 0 var(--spacing-sm) 0;
  color: var(--color-text-secondary);
}

.error-content small {
  color: var(--color-text-muted);
}
</style>
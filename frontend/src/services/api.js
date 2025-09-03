const API_BASE_URL = 'https://fit5120-backend.onrender.com/api'

class ApiService {
  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      },
      ...options
    }

    try {
      const response = await fetch(url, config)
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      return await response.json()
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  }

  async getSeasonKPI() {
    return this.request('/season/kpi')
  }

  async getSeasonActivity() {
    return this.request('/season/activity')
  }

  async getTopSpecies(season) {
    return this.request(`/season/top?season=${season}`)
  }

  async getSpeciesTrend(taxonId) {
    return this.request(`/trends?taxon_id=${taxonId}`)
  }

  async getSeasonalTrend(season) {
    return this.request(`/trends?season=${season}`)
  }

  async getMapStats() {
    return this.request('/map/stats')
  }

  async getObservations(params = {}) {
    const queryString = new URLSearchParams(params).toString()
    return this.request(`/map/observations?${queryString}`)
  }

  async getRegions() {
    return this.request('/map/regions')
  }

  async getStates() {
    return this.request('/map/states')
  }

  async searchSpecies(query, limit = 20) {
    return this.request(`/map/search?q=${encodeURIComponent(query)}&limit=${limit}`)
  }
}

export default new ApiService()

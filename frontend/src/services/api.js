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

  async getSeasonMonthlyTrends(season) {
    return this.request(`/season/monthly-trends?season=${season}`)
  }

 async getTopSpecies(season) {
  return this.request(`/top/top?season=${season}`)
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

  async getObservations(params = {}, options = {}) {
    if (!params.limit) {
      params.limit = 5000
    }
    const queryString = new URLSearchParams(params).toString()
    return this.request(`/map/observations?${queryString}`, options)
  }

  async getRegions() {
    return this.request('/map/regions')
  }

  async getRegionDetails(regionName) {
    return this.request(`/map/regions/${encodeURIComponent(regionName)}`)
  }

  async getStates() {
    return this.request('/map/states')
  }

  async searchSpecies(query, limit = 20) {
    return this.request(`/map/search?q=${encodeURIComponent(query)}&limit=${limit}`)
  }

  async getConservationSpecies() {
    return this.request('/conservation/species')
  }

  async getDailyWildleAnimal() {
    return this.request('/conservation/daily-animal')
  }

  async createAISession() {
    return this.request('/ai-challenge/session/new', {
      method: 'POST'
    })
  }

  async getNextQuestion(sessionId) {
    return this.request(`/ai-challenge/next_question?session_id=${sessionId}`)
  }

  async submitAnswer(sessionId, questionId, answer) {
    return this.request('/ai-challenge/answer', {
      method: 'POST',
      body: JSON.stringify({
        session_id: sessionId,
        question_id: questionId,
        answer: answer
      })
    })
  }

  async getCurrentGuess(sessionId) {
    return this.request(`/ai-challenge/guess?session_id=${sessionId}`)
  }

  async resetAISession(sessionId) {
    return this.request('/ai-challenge/reset', {
      method: 'POST',
      body: JSON.stringify({
        session_id: sessionId
      })
    })
  }
}

export default new ApiService()

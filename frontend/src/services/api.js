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

  async getYearlyMostCommon(year) {
    return this.request(`/yearly/most-common?year=${year}`)
  }

  async getYearlyLeastCommon(year) {
    return this.request(`/yearly/least-common?year=${year}`)
  }

  async compareYears(year1, year2) {
    return this.request(`/yearly/compare?year1=${year1}&year2=${year2}`)
  }

  async getSpeciesYearlyTrend(taxonId, startYear, endYear) {
    return this.request(`/yearly/species-trend?taxon_id=${taxonId}&start_year=${startYear}&end_year=${endYear}`)
  }

  async getYearlySpeciesList(year) {
    return this.request(`/yearly/species-list${year ? '?year=' + year : ''}`)
  }

  async getAvailableYears() {
    return this.request('/yearly/available-years')
  }

  async getDailyWildleAnimal() {
    return this.request('/daily-wildle/today')
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

  async getDailyWildleToday() {
    return this.request('/daily-wildle/today')
  }

  async submitDailyGuess(guess, guessCount = 1) {
    return this.request('/daily-wildle/guess', {
      method: 'POST',
      body: JSON.stringify({
        guess_name: guess,
        guess_count: guessCount
      })
    })
  }

  async getDailyWildleHistory(limit = 30) {
    return this.request(`/daily-wildle/history?limit=${limit}`)
  }

  async getAllAnimalSounds() {
    return this.request('/audio/sounds')
  }

  async getRandomAnimalSounds(count = 5) {
    return this.request(`/audio/random?count=${count}`)
  }

  async getAnimalDetails(name) {
    return this.request(`/audio/details/name/${encodeURIComponent(name)}`)
  }

  async getSpeciesTrendData(commonName, startYear, endYear) {
    return this.request(`/yearly/species-trend?common_name=${encodeURIComponent(commonName)}&start_year=${startYear}&end_year=${endYear}`)
  }
}

export default new ApiService()

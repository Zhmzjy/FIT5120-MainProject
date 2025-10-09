<template>
  <div class="audio-game-page">
    <img src="/images/v2osk-1Z2niiBPg5A-unsplash.jpg" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; object-fit: cover; z-index: -1;" alt="background">

    <TopNavigation @toggleMobileMenu="toggleMobileMenu" />

    <div class="main-content">
      <div class="page-header">
        <h1 class="page-title">Audio Matching Game</h1>
        <p class="page-subtitle">Listen to animal sounds and test your recognition skills</p>
      </div>

      <div class="game-container">
        <div v-if="!gameStarted" class="welcome-screen">
          <h2>Welcome to the Audio Challenge!</h2>
          <p>Listen carefully to animal sounds and try to identify which animal makes each sound.</p>
          <div class="game-info">
            <div class="info-item">
              <img src="/images/listening.png" alt="listening" class="info-icon-img" />
              <span>Listen to animal sounds</span>
            </div>
            <div class="info-item">
              <img src="https://img.icons8.com/plasticine/100/rick-sanchez.png" alt="rick-sanchez" class="info-icon-img" />
              <span>Choose the correct animal</span>
            </div>
            <div class="info-item">
              <img src="https://img.icons8.com/plasticine/100/morty-smith.png" alt="morty-smith" class="info-icon-img" />
              <span>Learn about Australian wildlife</span>
            </div>
          </div>
          <Button @click="startGame" type="primary" size="large">
            Start Game
          </Button>
        </div>

        <div v-else class="game-screen">
          <AudioPlayer
            v-if="currentAnimal"
            :audioUrl="currentAnimal.audioUrl"
            :animalName="currentAnimal.commonName"
            @audio-ready="handleAudioReady"
          />

          <div class="game-progress">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: progressPercentage + '%' }"></div>
            </div>
            <span class="progress-text">Round {{ currentRound }} of {{ totalRounds }}</span>
          </div>

          <AnswerOptions
            v-if="currentOptions.length > 0 && audioReady"
            :options="currentOptions"
            :selectedOption="selectedOption"
            :showResult="showResult"
            :correctAnswer="correctAnswer"
            @option-selected="handleOptionSelected"
          />

          <div v-if="showResult" class="result-section">
            <GameResult
              :isCorrect="isCorrect"
              :correctAnimal="currentAnimal"
              :selectedAnimal="selectedAnimal"
              :currentRound="currentRound"
              :totalRounds="totalRounds"
              @next-round="nextRound"
              @view-animal="viewAnimalDetails"
            />
          </div>
        </div>

        <div v-if="gameCompleted" class="summary-screen">
          <GameSummary
            :totalRounds="totalRounds"
            :correctAnswers="correctAnswers"
            :results="gameResults"
            @play-again="resetGame"
            @go-home="goHome"
          />
        </div>
      </div>
    </div>

    <div v-if="mobileMenuOpen" class="mobile-overlay" @click="closeMobileMenu"></div>
  </div>
</template>

<script>
import TopNavigation from '../components/common/TopNavigation.vue'
import Button from '../components/common/Button.vue'
import AudioPlayer from '../components/audio/AudioPlayer.vue'
import AnswerOptions from '../components/audio/AnswerOptions.vue'
import GameResult from '../components/audio/GameResult.vue'
import GameSummary from '../components/audio/GameSummary.vue'

export default {
  name: 'AudioMatchingGame',
  components: {
    TopNavigation,
    Button,
    AudioPlayer,
    AnswerOptions,
    GameResult,
    GameSummary
  },
  data() {
    return {
      mobileMenuOpen: false,
      gameStarted: false,
      gameCompleted: false,
      currentRound: 1,
      totalRounds: 5,
      correctAnswers: 0,
      audioReady: false,
      selectedOption: null,
      showResult: false,
      isCorrect: false,
      gameResults: [],
      animals: [
        {
          id: 1,
          commonName: 'Koala',
          scientificName: 'Phascolarctos cinereus',
          imageUrl: '/images/koala.png',
          audioUrl: '/audio/koala.mp3'
        },
        {
          id: 2,
          commonName: 'Kangaroo',
          scientificName: 'Osphranter rufus',
          imageUrl: '/images/kangaroo.png',
          audioUrl: '/audio/kangaroo.mp3'
        },
        {
          id: 3,
          commonName: 'Rainbow Lorikeet',
          scientificName: 'Trichoglossus moluccanus',
          imageUrl: '/images/koala.png',
          audioUrl: '/audio/lorikeet.mp3'
        },
        {
          id: 4,
          commonName: 'Australian Magpie',
          scientificName: 'Gymnorhina tibicen',
          imageUrl: '/images/kangaroo.png',
          audioUrl: '/audio/magpie.mp3'
        },
        {
          id: 5,
          commonName: 'Tasmanian Devil',
          scientificName: 'Sarcophilus harrisii',
          imageUrl: '/images/koala.png',
          audioUrl: '/audio/devil.mp3'
        },
        {
          id: 6,
          commonName: 'Bilby',
          scientificName: 'Macrotis lagotis',
          imageUrl: '/images/kangaroo.png',
          audioUrl: '/audio/bilby.mp3'
        }
      ],
      currentAnimal: null,
      currentOptions: [],
      usedAnimals: []
    }
  },
  computed: {
    progressPercentage() {
      return (this.currentRound / this.totalRounds) * 100
    },
    correctAnswer() {
      return this.currentAnimal ? this.currentAnimal.id : null
    },
    selectedAnimal() {
      return this.currentOptions.find(option => option.id === this.selectedOption)
    }
  },
  methods: {
    toggleMobileMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen
    },
    closeMobileMenu() {
      this.mobileMenuOpen = false
    },
    startGame() {
      this.gameStarted = true
      this.resetGameState()
      this.loadNextRound()
    },
    resetGameState() {
      this.currentRound = 1
      this.correctAnswers = 0
      this.gameResults = []
      this.usedAnimals = []
      this.gameCompleted = false
    },
    loadNextRound() {
      this.audioReady = false
      this.selectedOption = null
      this.showResult = false
      this.isCorrect = false

      const availableAnimals = this.animals.filter(animal => !this.usedAnimals.includes(animal.id))

      if (availableAnimals.length === 0) {
        this.completeGame()
        return
      }

      const randomIndex = Math.floor(Math.random() * availableAnimals.length)
      this.currentAnimal = availableAnimals[randomIndex]
      this.usedAnimals.push(this.currentAnimal.id)

      this.generateOptions()
    },
    generateOptions() {
      const options = [this.currentAnimal]
      const otherAnimals = this.animals.filter(animal => animal.id !== this.currentAnimal.id)

      while (options.length < 4 && otherAnimals.length > 0) {
        const randomIndex = Math.floor(Math.random() * otherAnimals.length)
        const selectedAnimal = otherAnimals.splice(randomIndex, 1)[0]
        options.push(selectedAnimal)
      }

      this.currentOptions = this.shuffleArray(options)
    },
    shuffleArray(array) {
      const shuffled = [...array]
      for (let i = shuffled.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]]
      }
      return shuffled
    },
    handleAudioReady() {
      this.audioReady = true
    },
    handleOptionSelected(optionId) {
      if (this.showResult) return

      this.selectedOption = optionId
      this.isCorrect = optionId === this.currentAnimal.id

      if (this.isCorrect) {
        this.correctAnswers++
      }

      this.gameResults.push({
        round: this.currentRound,
        animal: this.currentAnimal,
        selectedOption: optionId,
        isCorrect: this.isCorrect
      })

      setTimeout(() => {
        this.showResult = true
      }, 500)
    },
    nextRound() {
      console.log('nextRound called, current round before increment:', this.currentRound)
      if (this.currentRound >= this.totalRounds) {
        this.completeGame()
      } else {
        this.currentRound++
        console.log('Round incremented to:', this.currentRound)
        this.loadNextRound()
      }
    },
    completeGame() {
      this.gameCompleted = true
      this.gameStarted = false
    },
    resetGame() {
      this.gameCompleted = false
      this.startGame()
    },
    viewAnimalDetails(animal) {
      console.log('View animal details:', animal)
    },
    goHome() {
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
.audio-game-page {
  min-height: 100vh;
  position: relative;
}

.main-content {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  padding-top: 100px;
}

.page-header {
  text-align: center;
  margin-bottom: 32px;
}

.page-title {
  color: #2d3748;
  font-size: 2.5rem;
  font-weight: bold;
  margin-bottom: 12px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
}

.page-subtitle {
  color: #4a5568;
  font-size: 1.2rem;
  margin: 0;
}

.game-container {
  background: rgba(255, 255, 255, 0.95);
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.welcome-screen {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  min-height: 400px;
  text-align: center;
  max-width: 500px;
  margin: 0 auto;
  padding: 40px;
}

.welcome-screen h2 {
  color: #2d3748;
  font-size: 1.8rem;
  margin-bottom: 16px;
}

.welcome-screen p {
  color: #4a5568;
  font-size: 1.1rem;
  margin-bottom: 32px;
  line-height: 1.6;
}

.game-info {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 32px;
  width: 100%;
}

.info-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  background: #f7fafc;
  border-radius: 8px;
  text-align: left;
}

.info-icon {
  font-size: 1.5rem;
  width: 40px;
  display: flex;
  justify-content: center;
  flex-shrink: 0;
}

.info-icon-img {
  width: 32px;
  height: 32px;
  object-fit: contain;
}

.game-screen {
  max-width: 800px;
  margin: 0 auto;
}

.game-progress {
  margin-bottom: 24px;
  text-align: center;
}

.progress-bar {
  width: 100%;
  height: 8px;
  background: #e2e8f0;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 8px;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #4299e1, #63b3ed);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.progress-text {
  color: #4a5568;
  font-size: 1rem;
  font-weight: 500;
}

.result-section {
  margin-top: 24px;
}

.summary-screen {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 500px;
}

.mobile-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  z-index: 998;
}

@media (max-width: 768px) {
  .main-content {
    padding: 16px;
    padding-top: 80px;
  }

  .page-title {
    font-size: 2rem;
  }

  .page-subtitle {
    font-size: 1rem;
  }

  .game-container {
    padding: 16px;
  }

  .welcome-screen {
    padding: 24px 16px;
  }

  .welcome-screen h2 {
    font-size: 1.5rem;
  }

  .game-info {
    gap: 12px;
  }

  .info-item {
    padding: 8px;
    font-size: 0.9rem;
  }

  .info-icon {
    font-size: 1.2rem;
    width: 32px;
  }
}

@media (max-width: 480px) {
  .page-title {
    font-size: 1.8rem;
  }

  .welcome-screen p {
    font-size: 1rem;
  }
}
</style>

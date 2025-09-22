<template>
  <div class="completed-daily">
    <div class="completion-header">
      <h1 class="completion-title">
        {{ gameState.won ? 'Congratulations!' : 'Game Over!' }}
      </h1>
      <p class="completion-subtitle">
        {{ gameState.won ? 'You found the correct animal!' : 'Better luck next time!' }}
      </p>
    </div>

    <div class="result-section">
      <div class="correct-answer-card">
        <h3>{{ gameState.won ? 'You guessed correctly:' : 'The correct answer was:' }}</h3>
        <div class="animal-display">
          <div class="animal-name">{{ getCorrectAnswer() }}</div>
          <div class="animal-image-container" v-if="animalImage">
            <img :src="animalImage" :alt="getCorrectAnswer()" class="animal-image" />
          </div>
        </div>
        <div class="attempts-info">
          {{ gameState.won ? `You got it in ${gameState.attempts} attempts!` : `You used all ${gameState.maxAttempts} attempts.` }}
        </div>
      </div>
    </div>

    <div class="completion-message">
      <div class="message-card">
        <h3>{{ gameState.won ? 'Well Done!' : 'Thanks for Playing!' }}</h3>
        <p>{{ gameState.won ? "Great job learning about Australian wildlife!" : "You learned about Australian wildlife today!" }}</p>
        <p>Come back tomorrow for a new animal challenge!</p>
      </div>
    </div>

    <div class="completion-actions">
      <button @click="$emit('exit')" class="action-button">
        Back to Home
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CompletedDaily',
  props: {
    gameState: {
      type: Object,
      required: true
    },
    gameData: {
      type: Object,
      default: null
    }
  },
  emits: ['playAgain', 'exit'],
  data() {
    return {
      animalImage: null,
      loadingImage: false
    }
  },
  mounted() {
    this.fetchAnimalImage()
  },
  methods: {
    getCorrectAnswer() {
      if (this.gameState.feedback && this.gameState.feedback.correct_answer) {
        return this.gameState.feedback.correct_answer
      }

      if (this.gameState.won && this.gameState.guesses.length > 0) {
        const lastGuess = this.gameState.guesses[this.gameState.guesses.length - 1]
        return lastGuess.guess?.CommonName || 'Unknown'
      }

      if (this.gameData && this.gameData.animal_name) {
        return this.gameData.animal_name
      }

      return 'Unknown Animal'
    },
    async fetchAnimalImage() {
      const animalName = this.getCorrectAnswer()
      if (!animalName || animalName === 'Unknown Animal') return

      try {
        this.loadingImage = true

        const searchResponse = await fetch(
          `https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(animalName)}`
        )

        if (searchResponse.ok) {
          const searchData = await searchResponse.json()

          if (searchData.thumbnail && searchData.thumbnail.source) {
            this.animalImage = searchData.thumbnail.source.replace(/\/\d+px-/, '/400px-')
          } else {
            await this.searchWikipediaImages(animalName)
          }
        } else {
          await this.searchWikipediaImages(animalName)
        }
      } catch (error) {
        console.error('Error fetching animal image:', error)
        await this.searchWikipediaImages(animalName)
      } finally {
        this.loadingImage = false
      }
    },
    async searchWikipediaImages(animalName) {
      try {
        const searchTerms = [
          animalName,
          `${animalName} Australia`,
          `Australian ${animalName}`
        ]

        for (const term of searchTerms) {
          const searchResponse = await fetch(
            `https://en.wikipedia.org/w/api.php?action=query&format=json&origin=*&list=search&srsearch=${encodeURIComponent(term)}&srlimit=3`
          )

          if (searchResponse.ok) {
            const searchData = await searchResponse.json()

            if (searchData.query && searchData.query.search && searchData.query.search.length > 0) {
              for (const result of searchData.query.search) {
                const pageTitle = result.title

                const pageResponse = await fetch(
                  `https://en.wikipedia.org/api/rest_v1/page/summary/${encodeURIComponent(pageTitle)}`
                )

                if (pageResponse.ok) {
                  const pageData = await pageResponse.json()

                  if (pageData.thumbnail && pageData.thumbnail.source) {
                    this.animalImage = pageData.thumbnail.source.replace(/\/\d+px-/, '/400px-')
                    return
                  }
                }
              }
            }
          }
        }
      } catch (error) {
        console.error('Error searching Wikipedia images:', error)
      }
    }
  }
}
</script>

<style scoped>
.completed-daily {
  text-align: center;
  padding: 32px;
}

.completion-header {
  margin-bottom: 32px;
}

.completion-title {
  font-size: 36px;
  color: #4CAF50;
  margin: 0 0 16px 0;
  font-family: 'Comic Sans MS', cursive, sans-serif;
  font-weight: bold;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
}

.completion-subtitle {
  font-size: 18px;
  color: black;
  margin: 0;
  font-weight: 500;
}

.result-section {
  margin-bottom: 32px;
}

.correct-answer-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  margin: 0 auto;
  border: 3px solid #4CAF50;
}

.correct-answer-card h3 {
  font-size: 18px;
  color: #333;
  margin: 0 0 16px 0;
  font-weight: 600;
}

.animal-display {
  margin: 16px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.animal-image-container {
  margin: 16px 0;
  display: flex;
  justify-content: center;
}

.animal-image {
  width: 200px;
  height: 200px;
  object-fit: cover;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.animal-name {
  font-size: 24px;
  color: #4CAF50;
  font-weight: bold;
  margin: 0 0 12px 0;
  font-family: 'Comic Sans MS', cursive, sans-serif;
  text-align: center;
}

.attempts-info {
  font-size: 14px;
  color: #666;
  font-style: italic;
  margin-bottom: 16px;
}

.completion-message {
  margin-bottom: 32px;
}

.message-card {
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
  max-width: 400px;
  margin: 0 auto;
}

.message-card h3 {
  font-size: 24px;
  color: black;
  margin: 0 0 16px 0;
  font-family: 'Comic Sans MS', cursive, sans-serif;
}

.message-card p {
  font-size: 16px;
  color: #666;
  margin: 0 0 12px 0;
  line-height: 1.5;
}

.completion-actions {
  display: flex;
  justify-content: center;
}

.action-button {
  background: #4CAF50;
  color: white;
  border: none;
  padding: 16px 32px;
  font-size: 16px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.2s;
  font-family: 'Comic Sans MS', cursive, sans-serif;
  font-weight: bold;
}

.action-button:hover {
  background: #45a049;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

@media (max-width: 768px) {
  .completed-daily {
    padding: 24px 16px;
  }

  .completion-title {
    font-size: 28px;
  }

  .correct-answer-card,
  .message-card {
    margin: 0 16px;
    max-width: none;
  }

  .animal-image {
    width: 150px;
    height: 150px;
  }
}
</style>

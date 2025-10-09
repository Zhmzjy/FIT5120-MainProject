<template>
  <div class="audio-player">
    <div class="audio-header">
      <h3>Listen to the Animal Sound</h3>
      <p>Can you identify which animal makes this sound?</p>
    </div>

    <div class="audio-controls">
      <audio
        ref="audioElement"
        :src="audioUrl"
        @loadeddata="handleAudioLoaded"
        @ended="handleAudioEnded"
        @error="handleAudioError"
        preload="auto"
      ></audio>

      <div class="control-buttons">
        <img
          src="https://img.icons8.com/clouds/100/play.png"
          alt="play"
          @click="playAudio"
          :class="{ disabled: !audioLoaded || isPlaying }"
          class="play-button-img"
        />

        <img
          src="https://img.icons8.com/clouds/100/pause.png"
          alt="pause"
          @click="pauseAudio"
          :class="{ disabled: !isPlaying }"
          class="pause-button-img"
        />

        <img
          src="https://img.icons8.com/clouds/100/repeat.png"
          alt="repeat"
          @click="replayAudio"
          :class="{ disabled: !audioLoaded }"
          class="replay-button-img"
        />
      </div>

      <div v-if="audioLoaded" class="audio-info">
        <div class="audio-visualizer">
          <div class="wave-bar" v-for="i in 8" :key="i" :class="{ active: isPlaying }"></div>
        </div>
        <p class="instruction">Click play to hear the animal sound</p>
      </div>

      <div v-if="audioError" class="audio-error">
        <p>Audio not available - using placeholder sound</p>
        <Button @click="simulateAudio" type="secondary">
          Play Simulated Sound
        </Button>
      </div>

      <div v-if="!audioLoaded && !audioError" class="loading-audio">
        <div class="loading-spinner"></div>
        <p>Loading audio...</p>
      </div>
    </div>
  </div>
</template>

<script>
import Button from '../common/Button.vue'

export default {
  name: 'AudioPlayer',
  components: {
    Button
  },
  props: {
    audioUrl: {
      type: String,
      required: true
    },
    animalName: {
      type: String,
      required: true
    }
  },
  emits: ['audio-ready'],
  data() {
    return {
      audioLoaded: false,
      isPlaying: false,
      audioError: false,
      hasPlayed: false
    }
  },
  watch: {
    audioUrl() {
      this.resetAudioState()
      this.loadAudio()
    }
  },
  mounted() {
    this.loadAudio()
  },
  methods: {
    resetAudioState() {
      this.audioLoaded = false
      this.isPlaying = false
      this.audioError = false
      this.hasPlayed = false

      if (this.$refs.audioElement) {
        this.$refs.audioElement.pause()
        this.$refs.audioElement.currentTime = 0
      }
    },
    loadAudio() {
      if (this.$refs.audioElement) {
        this.$refs.audioElement.load()
      }
    },
    handleAudioLoaded() {
      this.audioLoaded = true
      this.audioError = false
      this.$emit('audio-ready')
    },
    handleAudioError() {
      this.audioError = true
      this.audioLoaded = false
      this.$emit('audio-ready')
    },
    handleAudioEnded() {
      this.isPlaying = false
    },
    playAudio() {
      if (this.$refs.audioElement && this.audioLoaded) {
        this.$refs.audioElement.play()
        this.isPlaying = true
        this.hasPlayed = true
      }
    },
    pauseAudio() {
      if (this.$refs.audioElement) {
        this.$refs.audioElement.pause()
        this.isPlaying = false
      }
    },
    replayAudio() {
      if (this.$refs.audioElement) {
        this.$refs.audioElement.currentTime = 0
        this.$refs.audioElement.play()
        this.isPlaying = true
        this.hasPlayed = true
      }
    },
    simulateAudio() {
      this.audioError = false
      this.audioLoaded = true
      this.$emit('audio-ready')
      setTimeout(() => {
        this.hasPlayed = true
      }, 1000)
    }
  }
}
</script>

<style scoped>
.audio-player {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  text-align: center;
}

.audio-header h3 {
  color: #2d3748;
  font-size: 1.4rem;
  margin-bottom: 8px;
}

.audio-header p {
  color: #718096;
  font-size: 1rem;
  margin-bottom: 24px;
}

.control-buttons {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.audio-info {
  margin-top: 16px;
}

.audio-visualizer {
  display: flex;
  justify-content: center;
  gap: 4px;
  margin-bottom: 12px;
}

.wave-bar {
  width: 4px;
  height: 20px;
  background: #e2e8f0;
  border-radius: 2px;
  transition: all 0.3s ease;
}

.wave-bar.active {
  background: #4299e1;
  animation: wave 1s ease-in-out infinite;
}

.wave-bar:nth-child(1).active { animation-delay: 0.1s; }
.wave-bar:nth-child(2).active { animation-delay: 0.2s; }
.wave-bar:nth-child(3).active { animation-delay: 0.3s; }
.wave-bar:nth-child(4).active { animation-delay: 0.4s; }
.wave-bar:nth-child(5).active { animation-delay: 0.5s; }
.wave-bar:nth-child(6).active { animation-delay: 0.6s; }
.wave-bar:nth-child(7).active { animation-delay: 0.7s; }
.wave-bar:nth-child(8).active { animation-delay: 0.8s; }

@keyframes wave {
  0%, 100% { height: 20px; }
  50% { height: 40px; }
}

.instruction {
  color: #718096;
  font-size: 0.9rem;
  margin: 0;
}

.audio-error {
  padding: 16px;
  background: #fed7d7;
  border-radius: 8px;
  margin-top: 16px;
}

.audio-error p {
  color: #c53030;
  margin-bottom: 12px;
}

.loading-audio {
  padding: 20px;
  text-align: center;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e2e8f0;
  border-top: 4px solid #4299e1;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 12px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.play-button-img,
.pause-button-img,
.replay-button-img {
  width: 70px;
  height: 70px;
  cursor: pointer;
  transition: transform 0.2s ease;
}

.play-button-img:hover:not(.disabled),
.pause-button-img:hover:not(.disabled),
.replay-button-img:hover:not(.disabled) {
  transform: scale(1.1);
}

.play-button-img.disabled,
.pause-button-img.disabled,
.replay-button-img.disabled {
  opacity: 0.5;
  pointer-events: none;
}

@media (max-width: 768px) {
  .control-buttons {
    flex-direction: column;
    align-items: center;
  }

  .audio-player {
    padding: 16px;
  }
}
</style>

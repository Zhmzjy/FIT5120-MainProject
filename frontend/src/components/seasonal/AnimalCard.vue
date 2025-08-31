<template>
  <div class="animal-card bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
    <div class="relative">
      <img
        :src="animal.image"
        :alt="animal.name"
        class="w-full h-48 object-cover"
        @error="handleImageError"
      />
      <div class="absolute top-2 right-2 bg-white rounded-full px-2 py-1 text-xs font-bold text-gray-700">
        {{ animal.count }}
      </div>
    </div>

    <div class="p-4">
      <h3 class="text-lg font-bold text-gray-800 mb-2">{{ animal.name }}</h3>

      <div class="flex items-center mb-2">
        <div class="flex space-x-1">
          <span
            v-for="star in 5"
            :key="star"
            :class="star <= animal.score ? 'text-yellow-400' : 'text-gray-300'"
            class="text-sm"
          >
            ⭐
          </span>
        </div>
        <span class="ml-2 text-xs text-gray-600">({{ animal.score }}/5)</span>
      </div>

      <p class="text-sm text-gray-600 mb-4">{{ animal.activity }}</p>

      <div class="flex space-x-2">
        <button
          @click="playSound"
          class="flex-1 bg-blue-500 text-white px-3 py-2 rounded text-sm font-medium hover:bg-blue-600 transition-colors duration-200 flex items-center justify-center"
        >
          🔊 Sound
        </button>
        <button
          @click="showDetails"
          class="flex-1 bg-green-500 text-white px-3 py-2 rounded text-sm font-medium hover:bg-green-600 transition-colors duration-200 flex items-center justify-center"
        >
          📖 Details
        </button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AnimalCard',
  props: {
    animal: {
      type: Object,
      required: true
    }
  },
  methods: {
    playSound() {
      console.log(`Playing sound for ${this.animal.name}`)

      const audio = new Audio(`/sounds/${this.animal.name.toLowerCase()}.mp3`)
      audio.play().catch(() => {
        alert(`Sound not available for ${this.animal.name}`)
      })
    },
    showDetails() {
      console.log(`Showing details for ${this.animal.name}`)
      alert(`Learn more about ${this.animal.name}!\n\nActivity: ${this.animal.activity}\nRating: ${this.animal.score}/5 stars\nCount: ${this.animal.count} spotted`)
    },
    handleImageError(event) {
      event.target.src = '/images/placeholder-animal.jpg'
    }
  }
}
</script>

<style scoped>
.animal-card {
  min-height: 350px;
}

.animal-card:hover {
  transform: translateY(-2px);
}

button:active {
  transform: scale(0.98);
}
</style>

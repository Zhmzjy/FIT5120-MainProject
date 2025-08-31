<template>
  <div class="season-tile relative overflow-hidden bg-white rounded-xl shadow-lg border-2 border-gray-200 p-6 cursor-pointer transition-all duration-300 hover:shadow-xl hover:border-green-400 group">
    <div class="text-center relative z-10">
      <div class="text-5xl mb-3">{{ emoji }}</div>
      <h3 class="text-xl font-bold text-gray-800 mb-2">{{ title }}</h3>
      <p class="text-sm text-gray-600">{{ subtitle }}</p>
    </div>

    <div class="grass-container absolute bottom-0 left-0 w-full h-0 group-hover:h-8 transition-all duration-500 overflow-hidden">
      <div class="grass-blade grass-1"></div>
      <div class="grass-blade grass-2"></div>
      <div class="grass-blade grass-3"></div>
      <div class="grass-blade grass-4"></div>
      <div class="grass-blade grass-5"></div>
      <div class="grass-blade grass-6"></div>
      <div class="grass-blade grass-7"></div>
      <div class="grass-blade grass-8"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SeasonTile',
  props: {
    emoji: {
      type: String,
      required: true
    },
    title: {
      type: String,
      required: true
    },
    subtitle: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>
.season-tile {
  min-height: 180px;
  transform: translateY(0);
}

.season-tile:hover {
  transform: translateY(-4px);
}

.grass-container {
  background: linear-gradient(to top, #22c55e, #16a34a);
}

.grass-blade {
  position: absolute;
  bottom: 0;
  width: 3px;
  background: linear-gradient(to top, #15803d, #22c55e, #4ade80);
  border-radius: 1.5px 1.5px 0 0;
  transform-origin: bottom center;
  opacity: 0;
  animation: growGrass 0.6s ease-out forwards;
}

.group:hover .grass-blade {
  animation: growGrass 0.6s ease-out forwards, swayGrass 2s ease-in-out infinite;
}

.grass-1 {
  left: 10%;
  height: 20px;
  animation-delay: 0.1s;
}

.grass-2 {
  left: 20%;
  height: 24px;
  animation-delay: 0.2s;
}

.grass-3 {
  left: 30%;
  height: 18px;
  animation-delay: 0.3s;
}

.grass-4 {
  left: 45%;
  height: 22px;
  animation-delay: 0.4s;
}

.grass-5 {
  left: 60%;
  height: 26px;
  animation-delay: 0.5s;
}

.grass-6 {
  left: 75%;
  height: 20px;
  animation-delay: 0.6s;
}

.grass-7 {
  left: 85%;
  height: 16px;
  animation-delay: 0.7s;
}

.grass-8 {
  left: 95%;
  height: 24px;
  animation-delay: 0.8s;
}

@keyframes growGrass {
  0% {
    opacity: 0;
    transform: scaleY(0) rotate(0deg);
  }
  50% {
    opacity: 0.7;
    transform: scaleY(0.8) rotate(2deg);
  }
  100% {
    opacity: 1;
    transform: scaleY(1) rotate(0deg);
  }
}

@keyframes swayGrass {
  0%, 100% {
    transform: scaleY(1) rotate(0deg);
  }
  25% {
    transform: scaleY(1) rotate(3deg);
  }
  75% {
    transform: scaleY(1) rotate(-3deg);
  }
}
</style>

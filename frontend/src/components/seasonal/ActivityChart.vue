
<template>
  <div class="activity-chart">
    <div class="space-y-4">
      <div
        v-for="activity in activities"
        :key="activity.name"
        class="activity-bar-container"
      >
        <div class="flex justify-between items-center mb-2">
          <span class="text-sm font-medium text-gray-700">{{ activity.name }}</span>
          <span class="text-sm text-gray-500">{{ activity.value }}%</span>
        </div>
        <div class="activity-bar-background">
          <div
            class="activity-bar-fill"
            :style="{ width: activity.value + '%' }"
            :class="getBarColor(activity.value)"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ActivityChart',
  props: {
    activities: {
      type: Array,
      default: () => []
    }
  },
  methods: {
    getBarColor(value) {
      if (value >= 70) return 'bg-green-500'
      if (value >= 40) return 'bg-yellow-500'
      return 'bg-red-500'
    }
  }
}
</script>

<style scoped>
.activity-bar-background {
  width: 100%;
  height: 20px;
  background-color: #f3f4f6;
  border-radius: 10px;
  overflow: hidden;
}

.activity-bar-fill {
  height: 100%;
  border-radius: 10px;
  transition: width 0.8s ease-in-out;
  position: relative;
}

.activity-bar-fill::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.2) 50%, transparent 100%);
  animation: shimmer 2s infinite;
}

@keyframes shimmer {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(100%); }
}

.activity-bar-container:hover .activity-bar-fill {
  filter: brightness(1.1);
}
</style>

<template>
  <div class="action-tips">
    <div class="section-header">
      <h2 class="section-title">How You Can Help Wildlife</h2>
      <p class="section-subtitle">Simple things you can do at home and school to protect animals</p>
    </div>

    <div class="tips-grid">
      <div v-for="tip in actionTips" :key="tip.id" class="tip-card">
        <div class="tip-icon">{{ tip.icon }}</div>
        <div class="tip-content">
          <h3 class="tip-title">{{ tip.title }}</h3>
          <p class="tip-description">{{ tip.description }}</p>
          <div class="tip-examples">
            <div class="example-item" v-for="example in tip.examples" :key="example">
              <span class="example-bullet">•</span>
              <span class="example-text">{{ example }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ActionTips',
  data() {
    return {
      actionTips: [
        {
          id: 1,
          icon: '♻️',
          title: 'Reduce, Reuse, Recycle',
          description: 'Help keep our environment clean by using less and recycling more.',
          examples: [
            'Use both sides of paper',
            'Recycle plastic bottles and cans',
            'Bring reusable bags to the store'
          ]
        },
        {
          id: 2,
          icon: '🌱',
          title: 'Plant Native Plants',
          description: 'Grow plants that Australian animals love to eat and live in.',
          examples: [
            'Plant eucalyptus trees for koalas',
            'Grow native flowers for birds',
            'Create a small garden at school'
          ]
        },
        {
          id: 3,
          icon: '💧',
          title: 'Save Water',
          description: 'Animals need clean water to drink and live in.',
          examples: [
            'Turn off taps when brushing teeth',
            'Take shorter showers',
            'Fix leaky taps at home'
          ]
        },
        {
          id: 4,
          icon: '🚗',
          title: 'Walk or Bike More',
          description: 'Less car pollution means cleaner air for all animals.',
          examples: [
            'Walk to school when possible',
            'Ride your bike to nearby places',
            'Use public transport'
          ]
        },
        {
          id: 5,
          icon: '📚',
          title: 'Learn and Share',
          description: 'Knowledge is power! Learn about animals and teach others.',
          examples: [
            'Read books about Australian wildlife',
            'Tell friends what you learned',
            'Join wildlife clubs at school'
          ]
        },
        {
          id: 6,
          icon: '🏠',
          title: 'Make Wildlife-Friendly Spaces',
          description: 'Create safe places for animals in your yard or community.',
          examples: [
            'Put up bird houses',
            'Leave water bowls for animals',
            'Keep cats indoors at night'
          ]
        }
      ]
    }
  }
}
</script>

<style scoped>
.action-tips {
  margin-bottom: 48px;
}

.section-header {
  text-align: center;
  margin-bottom: 32px;
}

.section-title {
  font-size: 32px;
  color: #2E7D32;
  margin: 0 0 8px 0;
  font-family: 'Comic Sans MS', cursive, sans-serif;
  font-weight: bold;
}

.section-subtitle {
  font-size: 16px;
  color: black;
  margin: 0;
}

.tips-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.tip-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
  border-left: 4px solid #4CAF50;
}

.tip-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.tip-icon {
  font-size: 48px;
  text-align: center;
  margin-bottom: 16px;
}

.tip-content {
  text-align: left;
}

.tip-title {
  font-size: 20px;
  color: #2E7D32;
  margin: 0 0 8px 0;
  font-family: 'Comic Sans MS', cursive, sans-serif;
  text-align: center;
}

.tip-description {
  font-size: 14px;
  color: #424242;
  margin: 0 0 16px 0;
  line-height: 1.4;
  text-align: center;
}

.tip-examples {
  background: #F1F8E9;
  border-radius: 8px;
  padding: 12px;
}

.example-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  margin-bottom: 4px;
}

.example-item:last-child {
  margin-bottom: 0;
}

.example-bullet {
  color: #4CAF50;
  font-weight: bold;
  margin-top: 2px;
}

.example-text {
  font-size: 12px;
  color: #2E7D32;
  line-height: 1.3;
}

@media (max-width: 768px) {
  .tips-grid {
    grid-template-columns: 1fr;
  }
}
</style>

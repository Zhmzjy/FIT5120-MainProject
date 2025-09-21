<template>
  <div class="climate-impact">
    <div class="section-header">
      <h2 class="section-title">How Climate Change Affects Animals</h2>
      <p class="section-subtitle">Understanding why we need to act now to protect wildlife</p>
    </div>

    <div class="impact-examples">
      <div v-for="impact in climateImpacts" :key="impact.id" class="impact-card">
        <div class="impact-visual">
          <div class="impact-icon">{{ impact.icon }}</div>
          <div class="impact-indicator" :class="impact.severity">
            {{ impact.severity.toUpperCase() }}
          </div>
        </div>

        <div class="impact-content">
          <h3 class="impact-title">{{ impact.title }}</h3>
          <p class="impact-description">{{ impact.description }}</p>

          <div class="affected-animals">
            <h4>Animals Affected:</h4>
            <div class="animal-tags">
              <span v-for="animal in impact.affectedAnimals" :key="animal" class="animal-tag">
                {{ animal }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="solution-section">
      <div class="solution-content">
        <h3>Good News!</h3>
        <p>People around the world are working together to help animals adapt to climate change. Here's what's being done:</p>

        <div class="solution-grid">
          <div v-for="solution in solutions" :key="solution.id" class="solution-item">
            <div class="solution-icon">{{ solution.icon }}</div>
            <div class="solution-text">
              <h4>{{ solution.title }}</h4>
              <p>{{ solution.description }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ClimateImpact',
  data() {
    return {
      climateImpacts: [
        {
          id: 1,
          icon: '🔥',
          title: 'Rising Temperatures',
          description: 'Hotter weather makes it harder for some animals to find cool places to rest and stay healthy.',
          severity: 'high',
          affectedAnimals: ['Koalas', 'Kangaroos', 'Desert Animals']
        },
        {
          id: 2,
          icon: '🌊',
          title: 'Sea Level Rise',
          description: 'Rising ocean waters flood the beaches where sea turtles lay their eggs.',
          severity: 'high',
          affectedAnimals: ['Sea Turtles', 'Penguins', 'Coastal Birds']
        },
        {
          id: 3,
          icon: '🌧️',
          title: 'Changing Rainfall',
          description: 'Some places get too much rain while others become very dry, affecting where animals can live.',
          severity: 'medium',
          affectedAnimals: ['Frogs', 'Bilbies', 'Rainforest Animals']
        },
        {
          id: 4,
          icon: '❄️',
          title: 'Extreme Weather',
          description: 'Stronger storms, longer droughts, and unusual cold snaps can hurt animal homes.',
          severity: 'high',
          affectedAnimals: ['All Wildlife', 'Migratory Birds', 'Marine Life']
        }
      ],
      solutions: [
        {
          id: 1,
          icon: '🌳',
          title: 'Protecting Habitats',
          description: 'Creating safe parks and reserves where animals can live safely.'
        },
        {
          id: 2,
          icon: '🔬',
          title: 'Scientific Research',
          description: 'Scientists study animals to understand how to help them better.'
        },
        {
          id: 3,
          icon: '🏥',
          title: 'Wildlife Hospitals',
          description: 'Special places where sick or injured animals can get better.'
        },
        {
          id: 4,
          icon: '🌱',
          title: 'Renewable Energy',
          description: 'Using clean energy like solar and wind power instead of pollution.'
        }
      ]
    }
  }
}
</script>

<style scoped>
.climate-impact {
  margin-bottom: 48px;
}

.section-header {
  text-align: center;
  margin-bottom: 32px;
}

.section-title {
  font-size: 32px;
  color: #FF6B35;
  margin: 0 0 8px 0;
  font-family: 'Comic Sans MS', cursive, sans-serif;
  font-weight: bold;
}

.section-subtitle {
  font-size: 16px;
  color: black;
  margin: 0;
}

.impact-examples {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.impact-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  border-left: 4px solid #FF6B35;
}

.impact-visual {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.impact-icon {
  font-size: 32px;
}

.impact-indicator {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 10px;
  font-weight: bold;
  color: white;
}

.impact-indicator.high {
  background: #D32F2F;
}

.impact-indicator.medium {
  background: #F57C00;
}

.impact-indicator.low {
  background: #388E3C;
}

.impact-content {
  text-align: left;
}

.impact-title {
  font-size: 18px;
  color: #FF6B35;
  margin: 0 0 8px 0;
  font-family: 'Comic Sans MS', cursive, sans-serif;
}

.impact-description {
  font-size: 14px;
  color: #424242;
  margin: 0 0 16px 0;
  line-height: 1.4;
}

.affected-animals h4 {
  font-size: 12px;
  color: #666;
  margin: 0 0 8px 0;
  font-family: 'Comic Sans MS', cursive, sans-serif;
}

.animal-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.animal-tag {
  background: #FFF3E0;
  color: #E65100;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 10px;
  font-weight: 500;
}

.solution-section {
  background: linear-gradient(135deg, #E8F5E8, #C8E6C9);
  border-radius: 16px;
  padding: 32px;
  text-align: center;
}

.solution-content h3 {
  font-size: 28px;
  color: #2E7D32;
  margin: 0 0 16px 0;
  font-family: 'Comic Sans MS', cursive, sans-serif;
}

.solution-content p {
  font-size: 16px;
  color: #1B5E20;
  margin: 0 0 24px 0;
  line-height: 1.5;
}

.solution-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.solution-item {
  background: white;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.solution-icon {
  font-size: 32px;
  margin-bottom: 12px;
}

.solution-text h4 {
  font-size: 16px;
  color: #2E7D32;
  margin: 0 0 8px 0;
  font-family: 'Comic Sans MS', cursive, sans-serif;
}

.solution-text p {
  font-size: 12px;
  color: #424242;
  margin: 0;
  line-height: 1.3;
}

@media (max-width: 768px) {
  .impact-examples {
    grid-template-columns: 1fr;
  }

  .solution-grid {
    grid-template-columns: 1fr;
  }

  .solution-section {
    padding: 24px;
  }
}
</style>

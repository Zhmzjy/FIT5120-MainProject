<template>
  <div class="endangered-species">
    <div class="section-header">
      <h2 class="section-title">Animals That Need Our Help</h2>
      <p class="section-subtitle">These Australian animals are in danger and need protection</p>
    </div>

    <div class="species-grid">
      <div v-for="animal in endangeredAnimals" :key="animal.id" class="species-card">
        <div class="species-image-container">
          <img :src="animal.image" :alt="animal.name" class="species-image" />
          <div class="status-badge" :class="animal.statusClass">
            {{ animal.status }}
          </div>
        </div>

        <div class="species-info">
          <h3 class="species-name">{{ animal.name }}</h3>
          <p class="species-description">{{ animal.description }}</p>

          <div class="threat-info">
            <div class="threat-icon">⚠️</div>
            <span class="threat-text">{{ animal.threat }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="legend">
      <h4>Conservation Status Guide:</h4>
      <div class="legend-items">
        <div class="legend-item">
          <div class="legend-badge critically-endangered"></div>
          <span>Critically Endangered</span>
        </div>
        <div class="legend-item">
          <div class="legend-badge endangered"></div>
          <span>Endangered</span>
        </div>
        <div class="legend-item">
          <div class="legend-badge vulnerable"></div>
          <span>Vulnerable</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'EndangeredSpecies',
  data() {
    return {
      endangeredAnimals: [
        {
          id: 1,
          name: 'Tasmanian Devil',
          image: '/images/koala.png',
          status: 'Endangered',
          statusClass: 'endangered',
          description: 'These fierce little animals live only in Tasmania and are known for their loud screeches.',
          threat: 'Disease and habitat loss'
        },
        {
          id: 2,
          name: 'Northern Hairy-nosed Wombat',
          image: '/images/koala.png',
          status: 'Critically Endangered',
          statusClass: 'critically-endangered',
          description: 'Only about 300 of these special wombats are left in the wild.',
          threat: 'Very small population'
        },
        {
          id: 3,
          name: 'Great Barrier Reef Marine Turtle',
          image: '/images/koala.png',
          status: 'Vulnerable',
          statusClass: 'vulnerable',
          description: 'These ancient sea creatures have been swimming in our oceans for millions of years.',
          threat: 'Plastic pollution and warming seas'
        },
        {
          id: 4,
          name: 'Bilby',
          image: '/images/koala.png',
          status: 'Vulnerable',
          statusClass: 'vulnerable',
          description: 'These cute animals have long ears and dig burrows in the desert.',
          threat: 'Habitat loss and introduced predators'
        },
        {
          id: 5,
          name: 'Orange-bellied Parrot',
          image: '/images/koala.png',
          status: 'Critically Endangered',
          statusClass: 'critically-endangered',
          description: 'Less than 50 of these colorful birds are left in the wild.',
          threat: 'Habitat destruction'
        },
        {
          id: 6,
          name: 'Koala',
          image: '/images/koala.png',
          status: 'Vulnerable',
          statusClass: 'vulnerable',
          description: 'These sleepy marsupials spend most of their time in eucalyptus trees.',
          threat: 'Deforestation and bushfires'
        }
      ]
    }
  }
}
</script>

<style scoped>
.endangered-species {
  margin-bottom: 48px;
}

.section-header {
  text-align: center;
  margin-bottom: 32px;
}

.section-title {
  font-size: 32px;
  color: #D32F2F;
  margin: 0 0 8px 0;
  font-family: 'Comic Sans MS', cursive, sans-serif;
  font-weight: bold;
}

.section-subtitle {
  font-size: 16px;
  color: black;
  margin: 0;
}

.species-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 24px;
  margin-bottom: 32px;
}

.species-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.species-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.species-image-container {
  position: relative;
  margin-bottom: 16px;
}

.species-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 12px;
}

.status-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: bold;
  color: white;
}

.status-badge.critically-endangered {
  background: #B71C1C;
}

.status-badge.endangered {
  background: #D32F2F;
}

.status-badge.vulnerable {
  background: #F57C00;
}

.species-info {
  text-align: left;
}

.species-name {
  font-size: 20px;
  color: black;
  margin: 0 0 8px 0;
  font-family: 'Comic Sans MS', cursive, sans-serif;
}

.species-description {
  font-size: 14px;
  color: #424242;
  margin: 0 0 12px 0;
  line-height: 1.4;
}

.threat-info {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 12px;
  background: #FFF3E0;
  border-radius: 8px;
  border-left: 4px solid #FF9800;
}

.threat-icon {
  font-size: 16px;
}

.threat-text {
  font-size: 12px;
  color: #E65100;
  font-weight: 500;
}

.legend {
  background: rgba(255, 255, 255, 0.9);
  border-radius: 12px;
  padding: 20px;
  text-align: center;
}

.legend h4 {
  font-size: 18px;
  color: black;
  margin: 0 0 16px 0;
  font-family: 'Comic Sans MS', cursive, sans-serif;
}

.legend-items {
  display: flex;
  justify-content: center;
  gap: 24px;
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.legend-badge {
  width: 20px;
  height: 20px;
  border-radius: 50%;
}

.legend-badge.critically-endangered {
  background: #B71C1C;
}

.legend-badge.endangered {
  background: #D32F2F;
}

.legend-badge.vulnerable {
  background: #F57C00;
}

.legend-item span {
  font-size: 14px;
  color: black;
  font-weight: 500;
}

@media (max-width: 768px) {
  .species-grid {
    grid-template-columns: 1fr;
  }

  .legend-items {
    flex-direction: column;
    align-items: center;
    gap: 12px;
  }
}
</style>

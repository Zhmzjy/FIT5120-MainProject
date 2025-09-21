<template>
  <div class="conservation-organizations">
    <div class="section-header">
      <h2 class="section-title">Heroes Protecting Wildlife</h2>
      <p class="section-subtitle">Meet the amazing people and organizations working to save Australian animals</p>
    </div>

    <div class="organizations-grid">
      <div v-for="org in organizations" :key="org.id" class="org-card">
        <div class="org-header">
          <div class="org-logo">{{ org.logo }}</div>
          <div class="org-basic-info">
            <h3 class="org-name">{{ org.name }}</h3>
            <p class="org-type">{{ org.type }}</p>
          </div>
        </div>

        <div class="org-content">
          <p class="org-description">{{ org.description }}</p>

          <div class="org-focus">
            <h4>What they do:</h4>
            <ul class="focus-list">
              <li v-for="focus in org.focuses" :key="focus">{{ focus }}</li>
            </ul>
          </div>

          <div class="org-impact">
            <div class="impact-stat">
              <span class="stat-number">{{ org.impact.number }}</span>
              <span class="stat-label">{{ org.impact.label }}</span>
            </div>
          </div>
        </div>

        <div class="org-actions">
          <button
            @click="openExternalLink(org.website)"
            class="learn-more-btn"
            :aria-label="`Learn more about ${org.name}`"
          >
            Learn More
          </button>
          <div class="org-social">
            <span class="social-label">Follow them:</span>
            <div class="social-icons">
              <button
                v-for="social in org.social"
                :key="social.platform"
                @click="openExternalLink(social.url)"
                class="social-btn"
                :aria-label="`Follow ${org.name} on ${social.platform}`"
              >
                {{ social.icon }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="get-involved">
      <div class="involvement-content">
        <h3>How You Can Get Involved</h3>
        <div class="involvement-options">
          <div class="involvement-item">
            <div class="involvement-icon">👨‍👩‍👧‍👦</div>
            <div class="involvement-text">
              <h4>Visit with Family</h4>
              <p>Ask your parents to visit wildlife parks and conservation centers</p>
            </div>
          </div>
          <div class="involvement-item">
            <div class="involvement-icon">📧</div>
            <div class="involvement-text">
              <h4>Follow Their Work</h4>
              <p>Subscribe to newsletters to learn about their latest animal rescues</p>
            </div>
          </div>
          <div class="involvement-item">
            <div class="involvement-icon">🎒</div>
            <div class="involvement-text">
              <h4>School Projects</h4>
              <p>Use their websites for school reports about Australian wildlife</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ConservationOrganizations',
  data() {
    return {
      organizations: [
        {
          id: 1,
          name: 'Australian Wildlife Conservancy',
          type: 'Conservation Organization',
          logo: '🦘',
          description: 'The largest private owner of land for conservation in Australia, protecting endangered species across the continent.',
          focuses: [
            'Protecting endangered species',
            'Managing wildlife sanctuaries',
            'Breeding programs for rare animals'
          ],
          impact: {
            number: '8.5M',
            label: 'hectares protected'
          },
          website: 'https://www.australianwildlife.org',
          social: [
            { platform: 'Facebook', icon: '📘', url: 'https://facebook.com/australianwildlife' },
            { platform: 'Instagram', icon: '📷', url: 'https://instagram.com/australianwildlife' }
          ]
        },
        {
          id: 2,
          name: 'WIRES Wildlife Rescue',
          type: 'Wildlife Rescue',
          logo: '🏥',
          description: 'Australia\'s largest wildlife rescue organization, helping injured and orphaned native animals.',
          focuses: [
            'Rescuing injured wildlife',
            'Caring for orphaned animals',
            'Educating the community'
          ],
          impact: {
            number: '100K+',
            label: 'animals rescued yearly'
          },
          website: 'https://www.wires.org.au',
          social: [
            { platform: 'Facebook', icon: '📘', url: 'https://facebook.com/wires.org.au' },
            { platform: 'Instagram', icon: '📷', url: 'https://instagram.com/wires_wildlife_rescue' }
          ]
        },
        {
          id: 3,
          name: 'WWF Australia',
          type: 'Global Conservation',
          logo: '🐼',
          description: 'Working to conserve nature and reduce threats to the diversity of life on Earth.',
          focuses: [
            'Protecting the Great Barrier Reef',
            'Fighting climate change',
            'Saving endangered species'
          ],
          impact: {
            number: '50+',
            label: 'conservation projects'
          },
          website: 'https://www.wwf.org.au',
          social: [
            { platform: 'Facebook', icon: '📘', url: 'https://facebook.com/WWFAustralia' },
            { platform: 'Instagram', icon: '📷', url: 'https://instagram.com/wwf_australia' }
          ]
        },
        {
          id: 4,
          name: 'Taronga Conservation Society',
          type: 'Zoo & Research',
          logo: '🦁',
          description: 'Connecting people with wildlife and committing to conservation action.',
          focuses: [
            'Breeding endangered species',
            'Wildlife research',
            'Education programs'
          ],
          impact: {
            number: '30+',
            label: 'breeding programs'
          },
          website: 'https://taronga.org.au',
          social: [
            { platform: 'Facebook', icon: '📘', url: 'https://facebook.com/tarongazoo' },
            { platform: 'Instagram', icon: '📷', url: 'https://instagram.com/tarongazoo' }
          ]
        }
      ]
    }
  },
  methods: {
    openExternalLink(url) {
      if (url) {
        window.open(url, '_blank', 'noopener,noreferrer')
      }
    }
  }
}
</script>

<style scoped>
.conservation-organizations {
  margin-bottom: 48px;
}

.section-header {
  text-align: center;
  margin-bottom: 32px;
}

.section-title {
  font-size: 32px;
  color: #1976D2;
  margin: 0 0 8px 0;
  font-family: 'Comic Sans MS', cursive, sans-serif;
  font-weight: bold;
}

.section-subtitle {
  font-size: 16px;
  color: black;
  margin: 0;
}

.organizations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.org-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
  border-top: 4px solid #1976D2;
}

.org-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.15);
}

.org-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 16px;
}

.org-logo {
  font-size: 32px;
  background: #E3F2FD;
  padding: 12px;
  border-radius: 50%;
  flex-shrink: 0;
}

.org-basic-info {
  flex: 1;
}

.org-name {
  font-size: 18px;
  color: #1976D2;
  margin: 0 0 4px 0;
  font-family: 'Comic Sans MS', cursive, sans-serif;
}

.org-type {
  font-size: 12px;
  color: #666;
  margin: 0;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.org-content {
  margin-bottom: 20px;
}

.org-description {
  font-size: 14px;
  color: #424242;
  margin: 0 0 16px 0;
  line-height: 1.4;
}

.org-focus h4 {
  font-size: 14px;
  color: #1976D2;
  margin: 0 0 8px 0;
  font-family: 'Comic Sans MS', cursive, sans-serif;
}

.focus-list {
  margin: 0 0 16px 0;
  padding-left: 16px;
}

.focus-list li {
  font-size: 12px;
  color: #424242;
  margin-bottom: 4px;
  line-height: 1.3;
}

.org-impact {
  background: #E3F2FD;
  border-radius: 8px;
  padding: 12px;
  text-align: center;
}

.impact-stat {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-number {
  font-size: 20px;
  font-weight: bold;
  color: #1976D2;
  font-family: 'Comic Sans MS', cursive, sans-serif;
}

.stat-label {
  font-size: 10px;
  color: #666;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.org-actions {
  border-top: 1px solid #E0E0E0;
  padding-top: 16px;
}

.learn-more-btn {
  background: #1976D2;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
  margin-bottom: 12px;
}

.learn-more-btn:hover {
  background: #1565C0;
}

.org-social {
  display: flex;
  align-items: center;
  gap: 8px;
}

.social-label {
  font-size: 10px;
  color: #666;
  font-weight: 500;
}

.social-icons {
  display: flex;
  gap: 4px;
}

.social-btn {
  background: none;
  border: none;
  font-size: 16px;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: background-color 0.3s;
}

.social-btn:hover {
  background: #F5F5F5;
}

.get-involved {
  background: linear-gradient(135deg, #E1F5FE, #B3E5FC);
  border-radius: 16px;
  padding: 32px;
  text-align: center;
}

.involvement-content h3 {
  font-size: 28px;
  color: #0277BD;
  margin: 0 0 24px 0;
  font-family: 'Comic Sans MS', cursive, sans-serif;
}

.involvement-options {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.involvement-item {
  background: white;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.involvement-icon {
  font-size: 32px;
  margin-bottom: 12px;
}

.involvement-text h4 {
  font-size: 16px;
  color: #0277BD;
  margin: 0 0 8px 0;
  font-family: 'Comic Sans MS', cursive, sans-serif;
}

.involvement-text p {
  font-size: 12px;
  color: #424242;
  margin: 0;
  line-height: 1.3;
}

@media (max-width: 768px) {
  .organizations-grid {
    grid-template-columns: 1fr;
  }

  .involvement-options {
    grid-template-columns: 1fr;
  }

  .get-involved {
    padding: 24px;
  }
}
</style>

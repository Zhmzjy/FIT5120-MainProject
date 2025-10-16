<template>
  <footer class="site-footer">
    <div class="footer-content">
      <div class="footer-section">
        <h3 class="footer-title">Dondig's Wildlife Seminary</h3>
        <p class="footer-description">
          Empowering children and families to learn about and protect Australian wildlife through interactive education.
        </p>
      </div>

      <div class="footer-section">
        <h4 class="section-title">Quick Links</h4>
        <ul class="footer-links">
          <li><a href="/" @click.prevent="navigateTo('/')">Home</a></li>
          <li><a href="/learn-wildlife" @click.prevent="navigateTo('/learn-wildlife')">Learn Wildlife</a></li>
          <li><a href="/seasonal" @click.prevent="navigateTo('/seasonal')">Seasonal Activities</a></li>
          <li><a href="/conservation" @click.prevent="navigateTo('/conservation')">Conservation</a></li>
        </ul>
      </div>

      <div class="footer-section">
        <h4 class="section-title">Interactive Games</h4>
        <ul class="footer-links">
          <li><a href="/ai-challenge" @click.prevent="navigateTo('/ai-challenge')">AI Challenge</a></li>
          <li><a href="/daily-wildle" @click.prevent="navigateTo('/daily-wildle')">Daily Wildle</a></li>
          <li><a href="/audio-game" @click.prevent="navigateTo('/audio-game')">Audio Game</a></li>
          <li><a href="/yearly-analysis" @click.prevent="navigateTo('/yearly-analysis')">Yearly Analysis</a></li>
        </ul>
      </div>

      <div class="footer-section">
        <h4 class="section-title">About Us</h4>
        <p class="team-info">Created by Team <strong>Dondig</strong></p>
        <p class="copyright">&copy; 2025 Dondig's Wildlife Seminary. All rights reserved.</p>
      </div>
    </div>

    <div class="footer-bottom">
      <p>Made with care for Australian wildlife conservation education</p>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer',
  methods: {
    navigateTo(path) {
      if (this.$route.path !== path) {
        this.$router.push(path)
      }
    }
  }
}
</script>

<style scoped>
.site-footer {
  background: linear-gradient(135deg, #2d3748 0%, #1a202c 100%);
  color: #e2e8f0;
  padding: 24px 20px 16px;
  margin-top: auto;
}

.footer-content {
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 16px;
}

.footer-section {
  display: flex;
  flex-direction: column;
}

.footer-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: #fff;
  margin: 0 0 8px 0;
  font-family: var(--font-cartoon, 'Comic Sans MS', cursive);
}

.footer-description {
  color: #cbd5e0;
  line-height: 1.5;
  margin: 0;
  font-size: 0.85rem;
}

.section-title {
  font-size: 0.95rem;
  font-weight: 600;
  color: #fff;
  margin: 0 0 10px 0;
  border-bottom: 2px solid #4a5568;
  padding-bottom: 6px;
}

.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
}

.footer-links li {
  margin-bottom: 6px;
}

.footer-links a {
  color: #cbd5e0;
  text-decoration: none;
  transition: color 0.3s ease, padding-left 0.3s ease;
  display: inline-block;
  font-size: 0.85rem;
}

.footer-links a:hover {
  color: #48bb78;
  padding-left: 4px;
}

.team-info {
  color: #cbd5e0;
  margin: 0 0 6px 0;
  font-size: 0.85rem;
}

.team-info strong {
  color: #48bb78;
  font-weight: 700;
}

.copyright {
  color: #a0aec0;
  font-size: 0.75rem;
  margin: 0;
}

.footer-bottom {
  text-align: center;
  padding-top: 12px;
  border-top: 1px solid #4a5568;
  max-width: 1400px;
  margin: 0 auto;
}

.footer-bottom p {
  color: #a0aec0;
  font-size: 0.8rem;
  margin: 0;
}

@media (max-width: 768px) {
  .site-footer {
    padding: 20px 16px 12px;
  }

  .footer-content {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .footer-title {
    font-size: 1rem;
  }

  .section-title {
    font-size: 0.9rem;
  }
}
</style>

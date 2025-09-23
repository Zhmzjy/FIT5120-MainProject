<template>
  <div class="password-protection">
    <div class="password-overlay">
      <div class="password-container">
        <div class="password-header">
          <div class="logo-section">
            <h1 class="app-title">Wildlife Academy</h1>
          </div>
          <p class="welcome-text">Welcome to the Wildlife Academy Portal</p>
        </div>

        <div class="password-form">
          <div class="form-group">
            <label for="password" class="password-label">Access Code</label>
            <input
              id="password"
              v-model="enteredPassword"
              @keyup.enter="verifyPassword"
              type="password"
              placeholder="Enter access code..."
              class="password-input"
              :class="{ 'error': hasError }"
              autocomplete="off"
            />
          </div>

          <div v-if="hasError" class="error-message">
            <span class="error-icon">!</span>
            Incorrect access code. Please try again.
          </div>

          <button
            @click="verifyPassword"
            class="submit-button"
            :disabled="!enteredPassword.trim()"
          >
            <span class="button-text">Access Wildlife Academy</span>
          </button>
        </div>

        <div class="footer-info">
          <p class="info-text">This is a secure educational platform for wildlife conservation learning</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PasswordProtection',
  emits: ['authenticated'],
  data() {
    return {
      enteredPassword: '',
      hasError: false,
      correctPassword: 'ITDINGOS'
    }
  },
  methods: {
    verifyPassword() {
      if (this.enteredPassword.trim() === this.correctPassword) {
        this.hasError = false
        localStorage.setItem('wildlife_academy_auth', 'true')
        localStorage.setItem('wildlife_academy_auth_time', Date.now().toString())
        this.$emit('authenticated')
      } else {
        this.hasError = true
        this.enteredPassword = ''
        setTimeout(() => {
          this.hasError = false
        }, 3000)
      }
    }
  }
}
</script>

<style scoped>
.password-protection {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.password-overlay {
  background: rgba(0, 0, 0, 0.3);
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(10px);
}

.password-container {
  background: white;
  padding: 48px;
  border-radius: 24px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  max-width: 500px;
  width: 90%;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.password-header {
  margin-bottom: 40px;
}

.logo-section {
  margin-bottom: 24px;
}

.logo-icon {
  font-size: 64px;
  margin-bottom: 16px;
  font-weight: bold;
  color: #667eea;
  background: linear-gradient(45deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-family: 'Arial', sans-serif;
}

.app-title {
  font-size: 32px;
  font-weight: bold;
  color: #2c3e50;
  margin: 0;
  background: linear-gradient(45deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.welcome-text {
  font-size: 16px;
  color: #666;
  margin: 0;
  font-weight: 500;
}

.password-form {
  margin-bottom: 32px;
}

.form-group {
  margin-bottom: 24px;
}

.password-label {
  display: block;
  font-size: 16px;
  font-weight: 600;
  color: #2c3e50;
  margin-bottom: 8px;
  text-align: left;
}

.password-input {
  width: 100%;
  padding: 16px 20px;
  font-size: 16px;
  border: 2px solid #e1e8ed;
  border-radius: 12px;
  outline: none;
  transition: all 0.3s ease;
  background: #f8f9fa;
  letter-spacing: 2px;
  box-sizing: border-box;
}

.password-input:focus {
  border-color: #667eea;
  background: white;
  box-shadow: 0 0 20px rgba(102, 126, 234, 0.1);
  transform: translateY(-2px);
}

.password-input.error {
  border-color: #e74c3c;
  background: #fdf2f2;
  animation: shake 0.5s ease-in-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-5px); }
  75% { transform: translateX(5px); }
}

.error-message {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  color: #e74c3c;
  font-size: 14px;
  font-weight: 500;
  margin-bottom: 16px;
  padding: 12px;
  background: #fdf2f2;
  border-radius: 8px;
  border: 1px solid #fadbd8;
}

.error-icon {
  font-size: 16px;
  font-weight: bold;
  background: #e74c3c;
  color: white;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
}

.submit-button {
  width: 100%;
  padding: 16px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  position: relative;
  overflow: hidden;
}

.submit-button:hover:not(:disabled) {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
}

.submit-button:active {
  transform: translateY(-1px);
}

.submit-button:disabled {
  background: #bdc3c7;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.button-text {
  font-size: 16px;
}

.footer-info {
  border-top: 1px solid #e1e8ed;
  padding-top: 24px;
}

.info-text {
  font-size: 13px;
  color: #95a5a6;
  margin: 0;
  line-height: 1.5;
}

@media (max-width: 768px) {
  .password-container {
    padding: 32px 24px;
    margin: 16px;
  }

  .app-title {
    font-size: 28px;
  }

  .logo-icon {
    font-size: 48px;
  }

  .password-input {
    padding: 14px 16px;
    font-size: 16px;
  }

  .submit-button {
    padding: 14px 20px;
    font-size: 15px;
  }
}
</style>

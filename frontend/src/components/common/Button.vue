<template>
  <button
    :class="buttonClasses"
    @click="handleClick"
    :disabled="disabled"
  >
    <slot />
  </button>
</template>

<script>
export default {
  name: 'Button',
  props: {
    type: {
      type: String,
      default: 'primary',
      validator: value => ['primary', 'secondary'].includes(value)
    },
    size: {
      type: String,
      default: 'medium',
      validator: value => ['small', 'medium', 'large'].includes(value)
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },
  computed: {
    buttonClasses() {
      return [
        'btn',
        `btn-${this.type}`,
        `btn-${this.size}`,
        {
          'btn-disabled': this.disabled
        }
      ]
    }
  },
  methods: {
    handleClick(event) {
      if (!this.disabled) {
        this.$emit('click', event)
      }
    }
  }
}
</script>

<style scoped>
.btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: var(--border-radius-lg);
  font-weight: 600;
  text-decoration: none;
  transition: all var(--transition-normal);
  cursor: pointer;
  font-family: var(--font-family-primary);
  outline: none;
  position: relative;
  overflow: hidden;
}

.btn:focus {
  outline: 2px solid rgba(255, 255, 255, 0.5);
  outline-offset: 2px;
}

.btn-small {
  padding: var(--spacing-sm) var(--spacing-md);
  font-size: var(--font-size-sm);
  min-height: 36px;
}

.btn-medium {
  padding: var(--spacing-md) var(--spacing-lg);
  font-size: var(--font-size-base);
  min-height: 44px;
}

.btn-large {
  padding: var(--spacing-lg) var(--spacing-2xl);
  font-size: var(--font-size-lg);
  min-height: 56px;
  min-width: 180px;
}

.btn-primary {
  background-color: var(--primary-green);
  color: var(--text-white);
  box-shadow: 0 2px 8px var(--shadow-light);
}

.btn-primary:hover:not(.btn-disabled) {
  background-color: var(--secondary-green);
  transform: translateY(-2px);
  box-shadow: 0 6px 20px var(--shadow-medium);
}

.btn-primary:active:not(.btn-disabled) {
  transform: translateY(0);
  box-shadow: 0 2px 8px var(--shadow-light);
}

.btn-secondary {
  background-color: var(--accent-blue);
  color: var(--text-white);
  box-shadow: 0 2px 8px var(--shadow-light);
}

.btn-secondary:hover:not(.btn-disabled) {
  background-color: #005577;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px var(--shadow-medium);
}

.btn-secondary:active:not(.btn-disabled) {
  transform: translateY(0);
  box-shadow: 0 2px 8px var(--shadow-light);
}

.btn-disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none !important;
  box-shadow: none !important;
}

@media (max-width: 768px) {
  .btn-large {
    min-width: 160px;
    padding: var(--spacing-md) var(--spacing-xl);
  }
}
</style>

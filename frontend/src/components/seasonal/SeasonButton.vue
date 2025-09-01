<template>
  <div
    class="season-button"
    :class="[seasonClass, { 'selected': isSelected }]"
    @click="handleClick"
  >
    <div class="season-background" :style="backgroundStyle"></div>
    <div class="season-overlay"></div>
    <span class="season-text">{{ season }}</span>
  </div>
</template>

<script>
export default {
  name: 'SeasonButton',
  props: {
    season: {
      type: String,
      required: true,
      validator: (value) => ['Spring', 'Summer', 'Autumn', 'Winter'].includes(value)
    },
    isSelected: {
      type: Boolean,
      default: false
    },
    size: {
      type: String,
      default: 'medium',
      validator: (value) => ['small', 'medium', 'large'].includes(value)
    }
  },
  emits: ['select'],
  computed: {
    seasonClass() {
      const classes = {
        Spring: 'spring-btn',
        Summer: 'summer-btn',
        Autumn: 'autumn-btn',
        Winter: 'winter-btn'
      }
      return classes[this.season]
    },
    backgroundStyle() {
      const images = {
        Spring: '/images/Spring.jpg',
        Summer: '/images/Summer.jpg',
        Autumn: '/images/Autumn.jpg',
        Winter: '/images/Winter.jpg'
      }
      return {
        backgroundImage: `url(${images[this.season]})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center'
      }
    }
  },
  methods: {
    handleClick() {
      this.$emit('select', this.season)
    }
  }
}
</script>

<style scoped>
.season-button {
  position: relative;
  width: 200px;
  height: 80px;
  border-radius: 12px;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.season-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.season-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

.season-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 2;
  transition: background-color 0.3s ease;
}

.season-text {
  position: relative;
  z-index: 3;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  font-weight: bold;
  font-size: 1.1rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
  color: white;
}

.spring-btn .season-overlay {
  background-color: rgba(34, 197, 94, 0.3);
}

.summer-btn .season-overlay {
  background-color: rgba(234, 179, 8, 0.3);
}

.autumn-btn .season-overlay {
  background-color: rgba(249, 115, 22, 0.3);
}

.winter-btn .season-overlay {
  background-color: rgba(59, 130, 246, 0.3);
}

.selected {
  border-color: #22c55e;
  box-shadow: 0 0 0 3px rgba(34, 197, 94, 0.3);
}

.selected .season-overlay {
  background-color: rgba(255, 255, 255, 0.2);
}

@media (max-width: 768px) {
  .season-button {
    width: 150px;
    height: 60px;
  }

  .season-text {
    font-size: 0.9rem;
  }
}
</style>

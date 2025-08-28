<template>
  <div class="legend-bar">
    <div class="legend-content">
      <div class="legend-section">
        <h4>Map Legend</h4>
        <div class="legend-items">
          <div class="legend-item">
            <span class="legend-icon mammal"></span>
            <span>Mammals</span>
          </div>
          <div class="legend-item">
            <span class="legend-icon bird"></span>
            <span>Birds</span>
          </div>
          <div class="legend-item">
            <span class="legend-icon reptile"></span>
            <span>Reptiles</span>
          </div>
          <div class="legend-item">
            <span class="legend-icon endangered"></span>
            <span>Endangered</span>
          </div>
        </div>
      </div>
      <div class="legend-controls">
        <button class="toggle-btn">Toggle 3D View</button>
        <button class="reset-btn">Reset View</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LegendBar'
}
</script>

<style scoped>
.legend-bar {
  width: 100%;
  background: white;
  border-top: 1px solid #e0e0e0;
  padding: 15px 20px;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.05);
}

.legend-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 100%;
}

.legend-section h4 {
  margin: 0 0 10px 0;
  font-size: 14px;
  color: #333;
  font-weight: 600;
}

.legend-items {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #555;
}

.legend-icon {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  display: inline-block;
}

.legend-icon.mammal {
  background: #ff6b6b;
}

.legend-icon.bird {
  background: #4ecdc4;
}

.legend-icon.reptile {
  background: #45b7d1;
}

.legend-icon.endangered {
  background: #f9ca24;
  border: 2px solid #f0932b;
}

.legend-controls {
  display: flex;
  gap: 10px;
}

.toggle-btn, .reset-btn {
  padding: 8px 16px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: all 0.2s;
}

.toggle-btn:hover, .reset-btn:hover {
  background: #f5f5f5;
  border-color: #bbb;
}

@media (max-width: 768px) {
  .legend-content {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }

  .legend-items {
    gap: 15px;
  }

  .legend-controls {
    width: 100%;
    justify-content: center;
  }
}
</style>

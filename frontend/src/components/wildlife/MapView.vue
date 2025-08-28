<template>
  <div class="map-view">
    <div id="mapbox-container" class="map-container">
      <div class="map-placeholder">
        <p>Mapbox Map Container</p>
        <small>Wildlife locations will be displayed here</small>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MapView'
}
</script>

<style scoped>
.map-view {
  width: 100%;
  height: 100%;
  position: relative;
}

.map-container {
  width: 100%;
  height: 100%;
  background: #f5f5f5;
  border-radius: 8px;
  overflow: hidden;
}

.map-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #666;
  background: linear-gradient(45deg, #e8f5e8, #f0f8f0);
}

.map-placeholder p {
  margin: 0 0 8px 0;
  font-size: 18px;
  font-weight: 500;
}

.map-placeholder small {
  font-size: 14px;
  opacity: 0.7;
}
</style>

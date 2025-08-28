<template>
  <div class="left-filters">
    <div class="filters-header">
      <h3>Filters</h3>
    </div>
    <div class="filters-content">
      <div class="filter-group">
        <label>Animal Type</label>
        <select>
          <option>All Animals</option>
          <option>Mammals</option>
          <option>Birds</option>
          <option>Reptiles</option>
        </select>
      </div>
      <div class="filter-group">
        <label>Habitat</label>
        <select>
          <option>All Habitats</option>
          <option>Forest</option>
          <option>Desert</option>
          <option>Ocean</option>
        </select>
      </div>
      <div class="filter-group">
        <label>Conservation Status</label>
        <select>
          <option>All Status</option>
          <option>Endangered</option>
          <option>Vulnerable</option>
          <option>Least Concern</option>
        </select>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LeftFilters'
}
</script>

<style scoped>
.left-filters {
  width: 100%;
  height: 100%;
  background: white;
  border-right: 1px solid #e0e0e0;
  padding: 20px;
}

.filters-header h3 {
  margin: 0 0 20px 0;
  color: #333;
  font-size: 18px;
}

.filter-group {
  margin-bottom: 20px;
}

.filter-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
  color: #555;
}

.filter-group select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

@media (max-width: 768px) {
  .left-filters {
    border-right: none;
    border-bottom: 1px solid #e0e0e0;
  }
}
</style>

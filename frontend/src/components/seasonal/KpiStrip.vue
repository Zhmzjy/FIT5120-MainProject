<template>
  <div class="kpi-strip mb-8">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <div class="kpi-tile bg-white rounded-lg shadow-md p-6 text-center border-l-4 border-blue-500">
        <div class="text-3xl font-bold text-blue-600 mb-2">{{ data.totalAnimals }}</div>
        <div class="text-sm font-medium text-gray-700 uppercase tracking-wide">Total Animals</div>
        <div class="text-xs text-gray-500 mt-1">Species spotted this season</div>
      </div>

      <div class="kpi-tile bg-white rounded-lg shadow-md p-6 text-center border-l-4 border-green-500">
        <div class="text-3xl font-bold text-green-600 mb-2">{{ data.activeSpecies }}</div>
        <div class="text-sm font-medium text-gray-700 uppercase tracking-wide">Active Species</div>
        <div class="text-xs text-gray-500 mt-1">Currently active in season</div>
      </div>

      <div class="kpi-tile bg-white rounded-lg shadow-md p-6 text-center border-l-4 border-orange-500">
        <div class="text-3xl font-bold text-orange-600 mb-2">{{ data.migrationCount }}</div>
        <div class="text-sm font-medium text-gray-700 uppercase tracking-wide">Migration Count</div>
        <div class="text-xs text-gray-500 mt-1">Animals migrating now</div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'KpiStrip',
  props: {
    data: {
      type: Object,
      default: () => ({
        totalAnimals: 0,
        activeSpecies: 0,
        migrationCount: 0
      })
    }
  }
}
</script>

<style scoped>
.kpi-tile {
  transition: transform 0.2s ease-in-out;
}

.kpi-tile:hover {
  transform: translateY(-2px);
}
</style>

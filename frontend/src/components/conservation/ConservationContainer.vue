<template>
  <div class="conservation-container">
    <ConservationHeader />
    <EndangeredSpecies />
    <ActionTips />
    <ClimateImpact />
    <ConservationOrganizations />
  </div>
</template>

<script>
import ConservationHeader from './ConservationHeader.vue'
import EndangeredSpecies from './EndangeredSpecies.vue'
import ActionTips from './ActionTips.vue'
import ClimateImpact from './ClimateImpact.vue'
import ConservationOrganizations from './ConservationOrganizations.vue'

export default {
  name: 'ConservationContainer',
  components: {
    ConservationHeader,
    EndangeredSpecies,
    ActionTips,
    ClimateImpact,
    ConservationOrganizations
  }
}
</script>

<style scoped>
.conservation-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

@media (max-width: 768px) {
  .conservation-container {
    padding: 0 16px;
  }
}
</style>

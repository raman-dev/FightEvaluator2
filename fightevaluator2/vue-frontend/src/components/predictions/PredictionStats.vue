<script setup>
import { inject } from 'vue';
defineProps({
  stats: {
    type: Object,
    required: true
  }
});

const toPercent = inject('toPercent');
const capitalize = (text) => text.charAt(0).toUpperCase() + text.slice(1);
</script>

<template>
  <div class="stat-container container-fluid col col-md-12 col-lg-10 col-xl-8 col-xxl-6 my-4">
    <div
      v-for="(stat, index) in stats.general"
      :key="index"
      class="general-stat-row row my-2"
      style="max-width: 42ch;"
    >
      <div class="row">
        <div class="col stat-label">Total Ratio</div>
        <div class="col"><strong>{{ stat.count }}/{{ stat.total }}</strong></div>
      </div>
      <div class="row">
        <div class="col stat-label">Accuracy</div>
        <div class="col"><strong>{{ toPercent(stat.ratio) }}</strong></div>
      </div>
    </div>

    <div class="prediction-type-stats stats-row my-1">
      <div
        v-for="(stat, index) in stats.fight_outcome"
        :key="index"
        class="prediction-type-stat-container"
      >
        <div class="prediction-type-stat-label">
          <p>{{ capitalize(stat.label) }}</p>
        </div>
        <div class="prediction-type-stat d-flex justify-content-between mt-auto">
          <span class="stat-label">ratio</span>
          <span class="stat-val"><strong>{{ stat.count }}/{{ stat.total }}</strong></span>
        </div>
        <div class="prediction-type-stat d-flex justify-content-between">
          <span class="stat-label">accuracy</span>
          <span class="stat-val"><strong>{{ toPercent(stat.ratio) }}</strong></span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
@media(max-width: 992px){
  .stats-row{
    grid-template-columns: 1fr 1fr !important;
  }
}

.stat-container{
  border: 2px solid #131b23;
  
  .stat-label{
    text-transform: uppercase;
  }
  
  .stats-row{
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 0.4rem;
    .prediction-type-stat-container{
      padding: 0.4rem;
      padding-left: 0.6rem;
      padding-right: 0.6rem;
      background-color: #12161A;
      border-radius: 0.4rem;

      display: flex;
      flex-direction: column;

      .prediction-type-stat-label{
        border-bottom: 1px solid lavender;
        margin-bottom: 0.8rem;
        margin-top: 0.4rem;
        p{
          margin: 0px;
        }
      }
    }
  }
}
</style>


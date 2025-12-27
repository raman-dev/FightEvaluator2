<script setup>
import PredictionStats from "@/components/predictions/PredictionStats.vue";
import PredictionTable from "@/components/predictions/PredictionTable.vue";
import { storeToRefs } from "pinia";
import { usePredictionsStore } from "@/stores/predictionsStore";

import { onMounted, ref } from "vue";
import { onBeforeRouteUpdate } from "vue-router";


const predictionsStore = usePredictionsStore();
const { stats,eventPredictions,eventPredictionsByYearMonth,eventPicks,eventPicksByYearMonth  } = storeToRefs(predictionsStore);

//only for parameter changes
// onBeforeRouteUpdate((to, from) => {
//     console.log ("Route updated, fetching predictions...");
//     // predictionsStore.getStats();
//     // predictionsStore.getPredictions();
// });

</script>

<template>
  <div class="prediction-table-container container-fluid py-2">
    <!-- <h2>okay working update on refresh</h2> -->
    <PredictionStats :stats="stats" />
    <PredictionTable 
    :eventPredictions="eventPredictions"
    :eventPredictionsByYearMonth="eventPredictionsByYearMonth"
    :eventPicks="eventPicks"
    :eventPicksByYearMonth="eventPicksByYearMonth"
    />
  </div>
</template>
<style lang="scss" scoped>
  .prediction-table-container{
    overflow-y: auto;
  }
</style>



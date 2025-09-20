<script setup>
import { onMounted, ref, watch } from "vue";
import OutcomeCard from "./OutcomeCard.vue";
import { storeToRefs } from "pinia";
import { useMatchupDetailStore } from "@/stores/matchupDetailStore";

const props = defineProps({
  standardEvents: Array,
  fighter_a: Object,
  fighter_b: Object,
  matchup: Object,
  predictions: Object,
});

const matchupDetailStore = useMatchupDetailStore();
const { predictions } = storeToRefs(matchupDetailStore);

onMounted(()=>{
  console.log ('predictions',props.predictions.WIN);
});

watch (predictions, (newVal,oldVal)=>{
  console.log ('predictions changed',newVal,oldVal);
});

</script>

<template>
  <div class="outcomes-container my-4">
    <h2>Event Likelihood</h2>
    <div class="outcomes-wrapper events-wrapper row">
      <template v-for="(event,idx) in standardEvents" :key="idx">
        <template v-if="event.value ==='WIN'">
          <OutcomeCard
            :event="event.value"
            :fighter="fighter_a"
            :matchup="matchup"
            v-model:likelihood="predictions[event.value][props.fighter_a.id].likelihood"
            v-model:justification="predictions[event.value][props.fighter_a.id].justification"
            >
          </OutcomeCard>  
          <OutcomeCard
            :event="event.value"
            :fighter="fighter_b"
            :matchup="matchup"
            v-model:likelihood="predictions[event.value][props.fighter_b.id].likelihood"
            v-model:justification="predictions[event.value][props.fighter_b.id].justification"
            >
          </OutcomeCard>  
        </template>
        <template v-else>
          <OutcomeCard
            :event="event.value"
            :matchup="matchup"
            :label="event.name"
            v-model:likelihood="predictions[event.value].likelihood"
            v-model:justifcation="predictions[event.value].justification"
            >
          </OutcomeCard>  
        </template>
      </template>
    </div>
  </div>
</template>

<style scoped lang="scss">
.outcomes-wrapper {
    display: flex;
    justify-content: space-evenly;
    gap: 0.6rem;

    .outcome.occurred{
      .wrapper{
        outline-color: #00FF00;
      }
    }

    .outcome.not-occurred{
      .wrapper{
        outline-color: #FF0000;
      }
    }
}
</style>

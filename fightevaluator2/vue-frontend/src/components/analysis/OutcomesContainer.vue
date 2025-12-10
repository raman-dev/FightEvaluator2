<script setup>
import { onMounted, ref, watch } from "vue";
import OutcomeCard from "./OutcomeCard.vue";
import { storeToRefs } from "pinia";
import { useMatchupDetailStore } from "@/stores/matchupDetailStore";

const props = defineProps({
  standardEvents: Array,
});

const matchupDetailStore = useMatchupDetailStore();
const { 
  predictions,
  matchup,
  fighter_a,
  fighter_b
} = storeToRefs(matchupDetailStore);

onMounted(()=>{
  // console.log ('predictions',props.predictions.WIN);
});

watch (predictions, (newVal,oldVal)=>{
  console.log ('predictions changed',newVal,oldVal);
});

</script>

<template>
  <div class="outcomes-container my-4">
    <h3>Outcome Likelihood</h3>
    <div class="outcomes-wrapper events-wrapper row">
      <template v-for="(event,idx) in standardEvents" :key="idx">
        <template v-if="event.value ==='WIN'">
          <OutcomeCard
            :event="event.value"
            :fighter="fighter_a"
            :matchup="matchup"
            v-model:likelihood="predictions[event.value][fighter_a.id].likelihood"
            v-model:justification="predictions[event.value][fighter_a.id].justification"
            >
          </OutcomeCard>  
          <OutcomeCard
            :event="event.value"
            :fighter="fighter_b"
            :matchup="matchup"
            v-model:likelihood="predictions[event.value][fighter_b.id].likelihood"
            v-model:justification="predictions[event.value][fighter_b.id].justification"
            >
          </OutcomeCard>  
        </template>
        <template v-else>
          <OutcomeCard
            :event="event.value"
            :matchup="matchup"
            :label="event.name"
            v-model:likelihood="predictions[event.value].likelihood"
            v-model:justification="predictions[event.value].justification"
            >
          </OutcomeCard>  
        </template>
      </template>
    </div>
  </div>
</template>

<style scoped lang="scss">
.outcomes-container{
  border: 2px solid #12161A;
  padding: 1.2rem;
}
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

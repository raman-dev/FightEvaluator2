<script setup>
import { ref } from "vue";
import OutcomeCard from "./OutcomeCard.vue";

defineProps({
  standardEvents: Array,
  fighter_a: Object,
  fighter_b: Object,
  matchup: Object,
});

// state maps by event name
const selectedLikelihoods = ref({});
const justifications = ref({});

function handleLikelihoodUpdate({ event, value }) {
  selectedLikelihoods.value[event] = value;
}

function handleJustificationUpdate({ event, value }) {
  justifications.value[event] = value;
}
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
            @update:likelihood="handleLikelihoodUpdate"
            @update:justification="handleJustificationUpdate">
          </OutcomeCard>  
          <OutcomeCard
            :event="event.value"
            :fighter="fighter_b"
            :matchup="matchup"
            @update:likelihood="handleLikelihoodUpdate"
            @update:justification="handleJustificationUpdate">
          </OutcomeCard>  
        </template>
        <template v-else>
          <OutcomeCard
            :event="event.value"
            :matchup="matchup"
            :label="event.name"
            @update:likelihood="handleLikelihoodUpdate"
            @update:justification="handleJustificationUpdate">
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

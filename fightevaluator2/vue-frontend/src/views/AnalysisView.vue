<script setup>
import { onMounted, ref } from 'vue';
import { useMatchupDetailStore } from '@/stores/matchupDetailStore';
import { useMatchupStore } from '@/stores/matchupStore';
import CompactFighterCard from '@/components/assessment/CompactFighterCard.vue';
import { storeToRefs } from 'pinia';
import PredictionSelector from '@/components/analysis/PredictionSelector.vue';
import OutcomesContainer from '@/components/analysis/OutcomesContainer.vue';


const matchupDetailStore = useMatchupDetailStore();
const matchupStore = useMatchupStore();
const { matchupId } = defineProps(['matchupId'])
const { matchup,fighter_a,fighter_b,standardEvents,predictions,pick } = storeToRefs(matchupDetailStore);

onMounted(() => {
    matchupDetailStore.fetchMatchupDetails(matchupId);
})

</script>
<template>
    <div class="container-fluid">
        <h3 class="text-center text-capitalize">{{ matchup.weight_class }} | {{ matchup.rounds }} rounds</h3>
        <div class="matchup-container justify-content-center">
            <!--contains information about each fighter including fighter img-->
            <div class="fighter-container">  
                <CompactFighterCard :fighter="fighter_a"></CompactFighterCard>
                <div class="vs-wrapper">
                    <h4>vs</h4>
                </div>
                <CompactFighterCard :fighter="fighter_b"></CompactFighterCard>
            </div>
        </div>
       <PredictionSelector 
        :standardEvents="standardEvents" 
        :fighter_a="fighter_a"
        :fighter_b="fighter_b"
        :serverPredictions="predictions"
        :serverPick="pick" >

       </PredictionSelector>

       <OutcomesContainer 
          :standardEvents="standardEvents" 
          :fighter_a="fighter_a" 
          :fighter_b="fighter_b" 
          :matchup="matchup"
          :predictions="predictions"
          >
       </OutcomesContainer>

    </div>
</template>

<style lang="scss">

.likely-5 {
  background-color: #dc3545;
}

.likely-4 {
  background-color: #ed7b26;
}

.likely-3 {
  background-color: #ffc107;
}

.likely-2 {
  background-color: #80ff00;
}

.likely-1 {
  background-color: #00ff00;
}

.likely-0{
  background-color: #52565A;
}

.confidence-selector{
  border: 1px solid lavender;
  border-radius: 0.4rem;
  padding: 0.3rem;

  .current-confidence{
    margin-bottom: 0.1rem;
    margin-top: 0.1rem;
  }
}
.fighter-container {
    display: flex;
    // flex-direction: column;
    align-items: center;
    justify-content: center;
    margin-top: 1rem;
    margin-bottom: 1rem;

    .vs-wrapper {
        margin: 1rem;
    }
}
</style>
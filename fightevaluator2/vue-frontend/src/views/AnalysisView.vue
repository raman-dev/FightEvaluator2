<script setup>
import { inject } from 'vue';
import { useMatchupDetailStore } from '@/stores/matchupDetailStore';
import { storeToRefs } from 'pinia';
import { onBeforeRouteUpdate } from 'vue-router';
// import { useMatchupStore } from '@/stores/matchupStore';
import CompactFighterCard from '@/components/assessment/CompactFighterCard.vue';
import PredictionSelector from '@/components/analysis/PredictionSelector.vue';
import OutcomesContainer from '@/components/analysis/OutcomesContainer.vue';
import AttribCompareTable from '@/components/analysis/AttribCompareTable.vue';



const matchupDetailStore = useMatchupDetailStore();
// const matchupStore = useMatchupStore();
const { matchupId } = defineProps(['matchupId'])
const { matchup,fighter_a,fighter_b,standardEvents,predictions,pick,attribComparison } = storeToRefs(matchupDetailStore);

const replaceUnderscoreSpace = inject('replaceUnderscoreSpace');

onBeforeRouteUpdate((a,b)=>{
  console.log('onBeforeRouteUpdate',a,b);
});

</script>
<template>
    <div class="container-fluid">
        <h3 class="text-center text-capitalize">{{ replaceUnderscoreSpace(matchup.weight_class) }} | {{ matchup.rounds }} rounds</h3>
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

       <div class="content-grid">
            <AttribCompareTable :attribComparison="attribComparison"></AttribCompareTable>
        </div>

    </div>
</template>

<style lang="scss">

/*data-polarity color variables*/
$positiveBg: #0d6efd; 
$negativeBg: #dc3545;
$neutralBg: #ffc107; 

.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;

  .notes-section {
    .fighter-name {
      text-transform: capitalize;
    }
    .notes {
      border-radius: 0.4rem;
      list-style: none;
      padding: 0.5rem;
      background-color: #12161A;

      li p {
        max-width: 36ch;
      }
      .note {
        background-color: #212529;
        border: 2px solid lavender;
        border-radius: 0.6rem;
        list-style: None;
        display: flex;
        padding: 1rem;
        margin: 0.6rem;
        p {
          word-break: break-word;
          text-wrap: wrap;
          max-width: 32ch;
          margin: 0px;
        }
      }
      .note[data-tag="positive"]{
        border: 3px solid $positiveBg; 
      }

      .note[data-tag="negative"]{
        border: 3px solid $negativeBg; 
      }
    }
  }

  .notes-left {
    // grid-row: 1;
    grid-column: span 1;
  }

  .notes-right {
    // grid-row: 1;
    grid-column: 4;
  }

  .attrib-compare-table {
    // grid-row: 1;
    grid-column: 2/4;
  }
}

.content-grid > * {
  grid-row: 1;
}

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
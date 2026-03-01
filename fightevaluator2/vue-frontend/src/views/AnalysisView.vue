<script setup>
import { inject,onMounted,ref,watch } from 'vue';
import { useMatchupDetailStore } from '@/stores/matchupDetailStore';
import { storeToRefs } from 'pinia';
import { onBeforeRouteUpdate } from 'vue-router';
// import { useMatchupStore } from '@/stores/matchupStore';
import CompactFighterCard from '@/components/assessment/CompactFighterCard.vue';
import PredictionSelector from '@/components/analysis/PredictionSelector.vue';
import OutcomesContainer from '@/components/analysis/OutcomesContainer.vue';
import AttribCompareTable from '@/components/analysis/AttribCompareTable.vue';
import NotesSection from '@/components/analysis/NotesSection.vue';
import AnalysisCompleteCheckBox from '@/components/analysis/AnalysisCompleteCheckBox.vue';



const matchupDetailStore = useMatchupDetailStore();
// const matchupStore = useMatchupStore();
const { matchupId } = defineProps(['matchupId'])
const { 
    matchup,
    fighter_a,
    fighter_b,
    standardEvents,
    attribComparison, 
    fighter_a_notes,
    fighter_b_notes 
} = storeToRefs(matchupDetailStore);

onMounted(() => {
  console.log("AnalyisView.onMounted");
  
})

const replaceUnderscoreSpace = inject('replaceUnderscoreSpace');

onBeforeRouteUpdate((a,b)=>{
  console.log('AnalysisView.onBeforeRouteUpdate',a,b);
});



</script>
<template>
    <div class="container-fluid main-content-container main-container">
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
        :standardEvents="standardEvents" >
       </PredictionSelector>
       <AnalysisCompleteCheckBox></AnalysisCompleteCheckBox>
       <OutcomesContainer :standardEvents="standardEvents"></OutcomesContainer>

       <div class="content-grid">
          <NotesSection 
            :fighter_name="`${fighter_a.first_name} ${fighter_a.last_name}`" 
            :notes="fighter_a_notes"> </NotesSection>
          <AttribCompareTable :attribComparison="attribComparison"></AttribCompareTable>
          <NotesSection 
            :fighter_name="`${fighter_b.first_name} ${fighter_b.last_name}`" 
            :notes="fighter_b_notes"> 
          </NotesSection>
       </div>

    </div>
</template>

<style lang="scss">
.main-content-container {
    overflow-y: auto;
}

/*data-polarity color variables*/
$positiveBg: #0d6efd; 
$negativeBg: #dc3545;
$neutralBg: #ffc107; 

.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr 1fr;

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

@media (max-width: 1280px) {
  .content-grid {
    grid-template-columns: 1fr 1fr 1fr 1fr;
    column-gap: 0.5rem;
    .attrib-compare-table {
      grid-row: 1;
      grid-column: span 4;
    }
    .notes-section {
      grid-row: 2;
      grid-column: span 2;
    }
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
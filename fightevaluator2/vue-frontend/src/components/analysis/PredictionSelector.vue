
<!-- <script>function defaultPickValue (){ return {event:null,fighter:null};} </script> -->
<script setup>
import { useMatchupDetailStore } from "@/stores/matchupDetailStore";
import { ref, computed, onMounted,watch } from "vue";
import PredictionSelectOption from "@/components/analysis/PredictionSelectOption.vue"
import { storeToRefs } from "pinia";

const props = defineProps({
  result: { type: Boolean, default: false },
  standardEvents: { type: Array, default: () => [] }, // [{ name, label, fighter_id }]
  matchup: { type: Object, default: () => ({ fighter_a: {}, fighter_b: {} }) },
});

function defaultPickValue()  { 
  return {event: null, fighter: null} ;
}
// local state
const selectorPick = ref(defaultPickValue());

const likelihood = computed(() => {
  //get the likelihood for the selectorPick
  const  {event,fighter} = selectorPick.value;
  if (event === null) {
    return 0;
  }
  //fighter is always an id 
  const serverEventPrediction = serverPredictions.value[event];
  if (event === 'WIN'){
    return serverEventPrediction[fighter].likelihood;
  }
  return serverEventPrediction.likelihood;
});
// derived text for likelihood (you can extend styling/logic here)
const likelihoodText = computed(() => {
    const  {event,fighter} = selectorPick.value;
    if (event === null) {
        return `Likelihood`;
    }
    const serverEventPrediction = serverPredictions.value[event];
    if (event === 'WIN'){
      return `${serverEventPrediction[fighter].label}` ;
    }
    return `${serverEventPrediction.label}`;
});

const matchupDetailStore = useMatchupDetailStore();
const { selectOutcome } = matchupDetailStore;//functions can be destructured from stores
const { 
  fighter_a,
  fighter_b,
  predictions: serverPredictions,
  pick: serverPick,
} = storeToRefs(matchupDetailStore);

onMounted(()=>{
    const { event, fighter } = serverPick.value;
    selectorPick.value.event = event;
    if (event === 'WIN'){
      //need fighter Id
      selectorPick.value.fighter = fighter;
    }
});

watch(serverPick, (newPick,oldPick)=>{
  // console.log('PredictionSelector.serverPick changed:', newPick,oldPick);
  selectorPick.value.event = newPick.event;
  if (newPick.event === 'WIN'){
    selectorPick.value.fighter = newPick.fighter;
  } else {
    selectorPick.value.fighter = null;
  }
});


function savePrediction() {
  console.log("Saving prediction:", selectorPick.value);
  selectOutcome(selectorPick.value);
}

function isPickSame(){
    
    if (selectorPick.value.event !== serverPick.value.event){
      return false;
    }

    if (selectorPick.value.event === 'WIN'){
      return selectorPick.value.fighter === serverPick.value.fighter;
    }

    return true;
}


</script>

<template>
  <div class="prediction-result-container my-4">
    <div class="reveal-result-container">
      <template v-if="result">
        <p>Results Available!</p>
        <button class="btn btn-secondary reveal-result-btn">Reveal</button>
      </template>
      <template v-else>
        <p>Results not available yet</p>
        <button class="btn disabled btn-secondary reveal-result-btn">Reveal</button>
      </template>
    </div>

    <div class="prediction-selector" data-outcome-prediction-id="0" >
      <div class="title-container d-flex justify-content-between">
        <h3>Pick Outcome</h3>
        <button class="save-prediction-btn btn btn-primary" 
          :class="{ disabled: isPickSame() }" 
          @click="savePrediction">
            Save
        </button>
      </div>

      <!-- Bootstrap dropdown -->
      <div class="form-select-container">
        <form @submit.prevent class="m-0">
          <select class="form-select" v-model="selectorPick" name="pick" style="text-transform: capitalize;">
            <option :value="defaultPickValue()" data-event-type="NA" data-fighter-id="0">Choose Outcome</option>

            <template v-for="(event, idx) in standardEvents" :key="idx">
              <template v-if="event.value == 'WIN'">
                <PredictionSelectOption :fighter="fighter_a" :event="event.value" :label="event.name"></PredictionSelectOption>
                <PredictionSelectOption :fighter="fighter_b" :event="event.value" :label="event.name"></PredictionSelectOption>
              </template>
              <template v-else>
                <PredictionSelectOption :event="event.value" :label="event.name"></PredictionSelectOption>
              </template>
            </template>

          </select>
        </form>

        <div class="current-confidence d-flex align-items-center current-likelihood" :data-likelihood="likelihood">
          <p class="prediction-likelihood-text confidence my-0 w-100" :class="`likely-${likelihood}`" style="color:black;">
            {{ likelihoodText }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped lang="scss">
.prediction-result-container {
  display: flex;
  flex-direction: column;
  align-items: center;

  .form-select-container form select {
    border-bottom-left-radius: 0rem;
    border-bottom-right-radius: 0rem;
  }

  .prediction-selector {
    background-color: #12161A;
    border-radius: 0.8rem;
    outline: 3px solid transparent;
    outline-offset: 1px;

    padding: 1.2rem;
    height: fit-content;
    width: fit-content;

    .title-container {
      position: relative;
      margin-bottom: 0.5rem;
    }

    .title-container .save-prediction-btn {
      position: absolute;
      right: 0px;
      top: 0px;
    }

    .confidence {
      min-width: fit-content;
      border-radius: 0.4rem;
      border-top-left-radius: 0rem;
      border-top-right-radius: 0rem;
      padding: 0.3rem;
      text-align: center;
      text-transform: capitalize;
      font-family: PoppinsSemiBold;
    }
  }

  .prediction-selector.correct {
    outline-color: #00FF00;
  }

  .prediction-selector.incorrect {
    outline-color: #FF0000;
  }

  .reveal-result-container {
    display: flex;
    align-items: baseline;
    justify-content: space-between;

    p {
      margin-right: 1rem;
    }
  }
}
</style>

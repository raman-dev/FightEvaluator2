<script setup>
import { useMatchupDetailStore } from "@/stores/matchupDetailStore";
import { ref, computed, watch } from "vue";

// props for dynamic data (you can change based on your setup)
const props = defineProps({
  result: { type: Boolean, default: false },
  standardEvents: { type: Array, default: () => [] }, // [{ name, label, fighter_id }]
  matchup: { type: Object, default: () => ({ fighter_a: {}, fighter_b: {} }) },
  fighter_a: { type: Object, default: () => ({ last_name: "" }) },
  fighter_b: { type: Object, default: () => ({ last_name: "" }) },
  serverPick : { type: Object, default: () => null }
});


// local state
const selectorPick = ref(null);
const predictions = ref({});
const likelihood = ref(0);

// derived text for likelihood (you can extend styling/logic here)
const likelihoodText = computed(() => `Likelihood: ${likelihood.value}%`);
const { pickOutcome } = useMatchupDetailStore();//functions can be destructured from stores

watch (props.serverPick,(newVal,oldVal) => {
    console.log('serverPick:',newVal,oldVal);
    const event = newVal.event;
    if (event === 'WIN'){
      //need fighter Id
      selectorPick.value = {fighterId:newVal.fighter,value:event}
    }
    selectorPick.value = {value:newVal.event};
});

function savePrediction() {
  console.log("Saving prediction:", selectorPick.value);
  pickOutcome(selectorPick.value);
}

function isPickDifferent(){
  if (selectorPick.value !== null){
    if (props.serverPick == null){
      return true;
    }
    
    if (selectorPick.value.value === props.serverPick.event){
      if (props.serverPick.event === 'WIN'){
        return selectorPick.value.fighterId === props.serverPick.fighter;
      }
    }
    return false;
  }
  
  return selectorPick.value === (props.serverPick === null);
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

    <div class="prediction-selector" data-outcome-prediction-id="0" :data-prediction="selectorPick">
      <div class="title-container d-flex justify-content-between">
        <h2>Pick Outcome</h2>
        <button class="save-prediction-btn btn btn-primary" 
          :class="{ disabled: isPickDifferent() }" 
          @click="savePrediction">
            Save
        </button>
      </div>

      <!-- Bootstrap dropdown -->
      <div class="form-select-container">
        <form @submit.prevent class="m-0">
          <select class="form-select" v-model="selectorPick" name="pick" style="text-transform: capitalize;">
            <option :value="null" data-event-type="NA" data-fighter-id="0">Choose Outcome</option>

            <template v-for="(event, idx) in standardEvents" :key="idx">
              <template v-if="event.value == 'WIN'">
                <option :value="{fighterId:fighter_a.id,value:event.value}" style="text-transform: capitalize;">
                  {{ fighter_a.last_name }} Wins
                </option>
                <option :value="{fighterId:fighter_b.id,value:event.value}" style="text-transform: capitalize;">
                  {{ fighter_b.last_name }} Wins
                </option>
              </template>
              <template v-else>
                <option :value="{value:event.value}" style="text-transform: capitalize;">
                    {{ event.name }}
                </option>
              </template>
            </template>

          </select>
        </form>

        <div class="current-confidence d-flex align-items-center current-likelihood" :data-likelihood="likelihood">
          <p class="prediction-likelihood-text confidence my-0 w-100" :class="`likely-${likelihood}`"
            style="color:black;">
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

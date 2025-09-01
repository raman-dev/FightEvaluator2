<script setup>
import { ref, computed } from "vue";

// props for dynamic data (you can change based on your setup)
const props = defineProps({
  result: { type: Boolean, default: false },
  standardEvents: { type: Array, default: () => [] }, // [{ name, label, fighter_id }]
  matchup: { type: Object, default: () => ({ fighter_a: {}, fighter_b: {} }) },
  fighter_a: { type: Object, default: () => ({ last_name: "" }) },
  fighter_b: { type: Object, default: () => ({ last_name: "" }) },
});

// local state
const prediction = ref("NA");
const likelihood = ref(0);

// derived text for likelihood (you can extend styling/logic here)
const likelihoodText = computed(() => `Likelihood: ${likelihood.value}%`);

function savePrediction() {
  console.log("Saving prediction:", prediction.value);
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

    <div class="prediction-selector" data-outcome-prediction-id="0" :data-prediction="prediction">
      <div class="title-container d-flex justify-content-between">
        <h2>Prediction</h2>
        <button class="save-prediction-btn btn btn-primary" :class="{ disabled: prediction === 'NA' }"
          @click="savePrediction">
          Save
        </button>
      </div>

      <!-- Bootstrap dropdown -->
      <div class="form-select-container">
        <form @submit.prevent>
          <select class="form-select" v-model="prediction" name="prediction" style="text-transform: capitalize;">
            <option value="NA" data-event-type="NA" data-fighter-id="0">Choose Outcome</option>

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

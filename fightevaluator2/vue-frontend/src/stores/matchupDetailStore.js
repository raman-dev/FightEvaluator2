import { ref, inject } from 'vue';
import { defineStore, storeToRefs } from 'pinia';
import { useMatchupStore } from '@/stores/matchupStore.js';
import { useRoute } from 'vue-router';
import server from '@/plugins/server';

export const useMatchupDetailStore = defineStore('matchupDetail', () => {
  //from the current url grab the corresponding matchup details from the 
  /*
  
  */
  const server = inject('server');

  const matchup = ref({});
  const fighter_a = ref({});
  const fighter_b = ref({});
  const standardEvents = ref([]);
  const pick = ref({event:null,fighter:null});
  const predictions = ref({});

  function onReceiveMatchupAnalysis(matchupComparison) {
    matchup.value = matchupComparison['matchup']
    fighter_a.value = matchupComparison['fighter_a'];
    fighter_b.value = matchupComparison['fighter_b'];
    standardEvents.value = matchupComparison['standardEvents'];
    if ('pick' in matchupComparison) {
      pick.value = matchupComparison['pick'];
    }
    // console.log (standardEvents.value);
    if ('predictions' in matchupComparison) {
      predictions.value = matchupComparison['predictions'];
    }
  }

  function fetchMatchupDetails(matchupId) {
    console.log (`fetchMatchupDetails.${matchupId}`);
    server.get_matchup_analysis(matchupId,onReceiveMatchupAnalysis);
    // onReceiveMatchupAnalysis(sampleFetchResult);
  }

  function onReceivePick(data) {
    console.log(data);
    pick.value = data.pick;
    /*
    
    "pick": {
        "id": 3,
        "matchup": 1415,
        "fighter": 975,
        "prediction": null,
        "event": "WIN",
        "isGamble": false,
        "isCorrect": null
    }
    */
  }

  function pickOutcome(outcome) {
    
    const data = {event:outcome.event};
    if (outcome.event !== null){
      if (outcome.event === 'WIN'){
        data.fighter = outcome.fighter;
      }
    }

    server.make_pick(data, matchup.value.id, onReceivePick);
  }

  function onReceivePrediction(data){ 
    const prediction = data.prediction;
    const event = prediction.event;
    if (event === 'WIN'){
      predictions.value[event][prediction.fighter] = prediction;
    }else{
      predictions.value[event] = prediction;
    } 
    console.log('Received Prediction => ',predictions.value[prediction.event]);
  }

  function updateOutcomePrediction(data){
    console.log(data);
    data.matchup = matchup.value.id;
    server.make_prediction(data,matchup.value.id,onReceivePrediction);
  }

  return { matchup, fighter_a, fighter_b, predictions, pick,  standardEvents, pickOutcome, fetchMatchupDetails, updateOutcomePrediction };
});
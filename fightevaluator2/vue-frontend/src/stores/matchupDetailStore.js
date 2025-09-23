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
  const sampleFetchResult = {"matchup":{"id":1411,"event":127,"fighter_a":1474,"fighter_b":354,"weight_class":"middleweight","rounds":5,"isprelim":false,"outcome":860,"inWatchList":true,"analysisComplete":false},"fighter_a":{"id":1474,"first_name":"nassourdine","middle_name":null,"last_name":"imavov","nick_name":"N/A","weight_class":"middleweight","height":75,"reach":75,"wins":13,"losses":4,"draws":0,"stance":"orthodox","date_of_birth":null,"data_api_link":null,"img_link":"https://images.tapology.com/headshot_images/125404/large/IMG_20201021_074458.jpg?1603259229","name_index":"nassourdine-imavov"},"fighter_a_assessment":{"id":1473,"fighter":1474,"head_movement":2,"gas_tank":2,"aggression":3,"desire_to_win":3,"striking":2,"chinny":3,"grappling_offense":3,"grappling_defense":3},"fighter_b":{"id":354,"first_name":"caio","middle_name":null,"last_name":"borralho","nick_name":"N/A","weight_class":"middleweight","height":70,"reach":75,"wins":16,"losses":2,"draws":0,"stance":"southpaw","date_of_birth":"1993-01-16","data_api_link":null,"img_link":"https://images.tapology.com/headshot_images/107316/large/borralho2.jpg?1642020546","name_index":"caio-borralho"},"fighter_b_assessment":{"id":353,"fighter":354,"head_movement":2,"gas_tank":2,"aggression":2,"desire_to_win":3,"striking":2,"chinny":3,"grappling_offense":3,"grappling_defense":0},"standardEvents":[{"name":"Fighter wins","value":"WIN"},{"name":"Fight lasts more than 1.5 rounds","value":"ROUNDS_GEQ_ONE_AND_HALF"},{"name":"Fight Does Not Go the Distance","value":"DOES_NOT_GO_THE_DISTANCE"}],"predictions":{"WIN":{"1474":{"likelihood":3,"label":"Neutral","justification":""},"354":{"likelihood":3,"label":"Neutral","justification":""}},"ROUNDS_GEQ_ONE_AND_HALF":{"likelihood":3,"label":"Neutral","justification":""},"DOES_NOT_GO_THE_DISTANCE":{"likelihood":3,"label":"Neutral","justification":""}},"prediction":{"id":299,"matchup":1411,"prediction":983,"isGamble":false,"isCorrect":true},"pick":{"id":13,"matchup":1411,"fighter":1474,"prediction":null,"event":"DOES_NOT_GO_THE_DISTANCE","isGamble":false,"isCorrect":null},"attribComparison":[["head_movement",2,2],["gas_tank",2,2],["aggression",3,2],["desire_to_win",3,3],["striking",2,2],["chinny",3,3],["grappling_offense",3,3],["grappling_defense",3,0]]};

  const matchup = ref({});
  const fighter_a = ref({});
  const fighter_b = ref({});
  const standardEvents = ref([]);
  const pick = ref({event:null,fighter:null});
  const predictions = ref({});
  const attribComparison = ref([]);

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
    if ('attribComparison' in matchupComparison) {
      attribComparison.value = matchupComparison['attribComparison'];
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

  return { matchup, fighter_a, fighter_b, predictions, pick,  standardEvents,attribComparison, pickOutcome, fetchMatchupDetails, updateOutcomePrediction };
});
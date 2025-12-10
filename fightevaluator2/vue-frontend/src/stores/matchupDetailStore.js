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
  const sampleFetchResult = {"matchup": {"id": 1470, "event": 131, "fighter_a": 2014, "fighter_b": 1916, "weight_class": "welterweight", "rounds": 3, "isprelim": false, "outcome": null, "inWatchList": true, "analysisComplete": false}, "fighter_a": {"id": 2014, "first_name": "jake", "middle_name": null, "last_name": "matthews", "nick_name": "N/A", "weight_class": "Welterweight", "height": 71, "reach": 73, "wins": 21, "losses": 7, "draws": 0, "stance": "Orthodox", "date_of_birth": "1994-08-19", "data_api_link": "https://www.tapology.com/fightcenter/fighters/45260-jake-matthews", "img_link": "https://images.tapology.com/headshot_images/45260/large/Jake_Matthews-hs.jpg?1529750944", "name_index": "jake-matthews"}, "fighter_a_assessment": {"id": 2013, "fighter": 2014, "head_movement": 3, "gas_tank": 3, "aggression": 2, "desire_to_win": 3, "striking": 3, "chinny": 1, "grappling_offense": 3, "grappling_defense": 3}, "fighter_b": {"id": 1916, "first_name": "neil", "middle_name": null, "last_name": "magny", "nick_name": "N/A", "weight_class": "welterweight", "height": 75, "reach": 80, "wins": 30, "losses": 12, "draws": 0, "stance": "orthodox", "date_of_birth": "1987-08-03", "data_api_link": null, "img_link": "https://images.tapology.com/headshot_images/16456/large/Magny-Neil-UFC157-1-hs.jpg?1422914695", "name_index": "neil-magny"}, "fighter_b_assessment": {"id": 1915, "fighter": 1916, "head_movement": 2, "gas_tank": 3, "aggression": 2, "desire_to_win": 1, "striking": 2, "chinny": 2, "grappling_offense": 3, "grappling_defense": 1}, "fighter_a_notes": [], "fighter_b_notes": [{"id": 139, "assessment": 1915, "data": "Not looking to win but looking to survive for some reason.", "tag": 2}, {"id": 138, "assessment": 1915, "data": "Mirrors his opponent always; if opponent is aggressive he is aggressive, vice versa; if opponent wants to clinch he will clinch, etc.", "tag": 2}, {"id": 137, "assessment": 1915, "data": "Doesn't check leg kicks.", "tag": 2}], "standardEvents": [{"name": "Fighter wins", "value": "WIN"}, {"name": "Fight lasts more than 1.5 rounds", "value": "ROUNDS_GEQ_ONE_AND_HALF"}, {"name": "Fight Does Not Go the Distance", "value": "DOES_NOT_GO_THE_DISTANCE"}], "predictions": {"WIN": {"2014": {"likelihood": 3, "label": "Neutral", "justification": ""}, "1916": {"likelihood": 3, "label": "Neutral", "justification": ""}}, "ROUNDS_GEQ_ONE_AND_HALF": {"likelihood": 3, "label": "Neutral", "justification": ""}, "DOES_NOT_GO_THE_DISTANCE": {"likelihood": 3, "label": "Neutral", "justification": ""}}, "prediction": {}, "pick": {"event": null, "fighter": null}, "attribComparison": [["head_movement", 3, 2], ["gas_tank", 3, 3], ["aggression", 2, 2], ["desire_to_win", 3, 1], ["striking", 3, 2], ["chinny", 1, 2], ["grappling_offense", 3, 3], ["grappling_defense", 3, 1]]};

  const matchup = ref({});
  const fighter_a = ref({});
  const fighter_b = ref({});
  const standardEvents = ref([]);
  const pick = ref({event:null,fighter:null});
  const predictions = ref({});
  const attribComparison = ref([]);
  const fighter_a_notes = ref([]);
  const fighter_b_notes = ref([]);

  function onReceiveMatchupAnalysis(matchupComparison) {
    console.log('onReceiveMatchupAnalysis',matchupComparison)
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
    if ('fighter_a_notes' in matchupComparison) {
      fighter_a_notes.value = matchupComparison['fighter_a_notes'];
      // console.log('fighter_a_notes',fighter_a_notes.value);
    }
    if ('fighter_b_notes' in matchupComparison) {
      fighter_b_notes.value = matchupComparison['fighter_b_notes'];
      // console.log('fighter_b_notes',fighter_b_notes.value);
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

  function selectOutcome(outcome) {
    
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

  return { 
    matchup, 
    fighter_a, 
    fighter_b, 
    predictions, 
    pick,  
    standardEvents,
    attribComparison,
    fighter_a_notes, 
    fighter_b_notes, selectOutcome, fetchMatchupDetails, updateOutcomePrediction 
  };

});
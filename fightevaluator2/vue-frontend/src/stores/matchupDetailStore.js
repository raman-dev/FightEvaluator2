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
  // const sampleFetchResult = {"matchup":{"id":1331,"event":120,"fighter_a":118,"fighter_b":3614,"weight_class":"middleweight","rounds":3,"isprelim":false,"outcome":831,"inWatchList":true,"analysisComplete":true},"fighter_a":{"id":118,"first_name":"eryk","middle_name":null,"last_name":"anders","nick_name":"N/A","weight_class":"middleweight","height":73,"reach":75,"wins":17,"losses":9,"draws":0,"stance":"Southpaw","date_of_birth":"1987-04-21","data_api_link":"https://www.tapology.com/fightcenter/fighters/30666-eryk-anders","img_link":"https://images.tapology.com/headshot_images/30666/large/Eryk_Anders.jpg?1517462939","name_index":"eryk-anders"},"fighter_a_assessment":{"id":117,"fighter":118,"head_movement":0,"gas_tank":2,"aggression":2,"desire_to_win":2,"striking":2,"chinny":2,"grappling_offense":3,"grappling_defense":0},"fighter_b":{"id":3614,"first_name":"christian","middle_name":"leroy","last_name":"duncan","nick_name":"cld","weight_class":"middleweight","height":73,"reach":79,"wins":12,"losses":2,"draws":0,"stance":"orthodox","date_of_birth":"1995-07-24","data_api_link":"https://www.tapology.com/fightcenter/fighters/116334-christian-duncan","img_link":"https://images.tapology.com/headshot_images/116334/large/cld2.jpg?1700662938","name_index":"christian-leroy-duncan"},"fighter_b_assessment":{"id":3613,"fighter":3614,"head_movement":2,"gas_tank":3,"aggression":3,"desire_to_win":2,"striking":2,"chinny":3,"grappling_offense":0,"grappling_defense":3},"standardEvents":[{"name":"Fighter wins","value":"WIN"},{"name":"Fight lasts more than 1.5 rounds","value":"ROUNDS_GEQ_ONE_AND_HALF"},{"name":"Fight Does Not Go the Distance","value":"DOES_NOT_GO_THE_DISTANCE"}],"predictions":[{"id":944,"matchup":1331,"event":"WIN","eventType":"WIN","likelihood":1,"justification":"- Win Via KO/Decision using striking, faster more dangerous, better chin\n- fought more dangerous opponents and survived","fighter":3614},{"id":945,"matchup":1331,"event":"WIN","eventType":"WIN","likelihood":4,"justification":"- Unlikely Win Via TKO/KO slow Down duncan through grappling then generate enough power to kO him","fighter":118},{"id":946,"matchup":1331,"event":"DOES_NOT_GO_THE_DISTANCE","eventType":"DOES_NOT_GO_THE_DISTANCE","likelihood":1,"justification":"- Anders has gotten dropped in his last 2 fights from short shots, duncan hits hard and fast and if anders gets dropped he'll get finished","fighter":null}],"prediction":{"id":277,"matchup":1331,"prediction":944,"isGamble":false,"isCorrect":true},"pick":{"id":4,"matchup":1331,"fighter":3614,"prediction":null,"event":"WIN","isGamble":false,"isCorrect":null}}
  const sampleFetchResult = {"matchup": {"id": 1331, "event": 120, "fighter_a": 118, "fighter_b": 3614, "weight_class": "middleweight", "rounds": 3, "isprelim": false, "outcome": 831, "inWatchList": true, "analysisComplete": true}, "fighter_a": {"id": 118, "first_name": "eryk", "middle_name": null, "last_name": "anders", "nick_name": "N/A", "weight_class": "middleweight", "height": 73, "reach": 75, "wins": 17, "losses": 9, "draws": 0, "stance": "Southpaw", "date_of_birth": "1987-04-21", "data_api_link": "https://www.tapology.com/fightcenter/fighters/30666-eryk-anders", "img_link": "https://images.tapology.com/headshot_images/30666/large/Eryk_Anders.jpg?1517462939", "name_index": "eryk-anders"}, "fighter_a_assessment": {"id": 117, "fighter": 118, "head_movement": 0, "gas_tank": 2, "aggression": 2, "desire_to_win": 2, "striking": 2, "chinny": 2, "grappling_offense": 3, "grappling_defense": 0}, "fighter_b": {"id": 3614, "first_name": "christian", "middle_name": "leroy", "last_name": "duncan", "nick_name": "cld", "weight_class": "middleweight", "height": 73, "reach": 79, "wins": 12, "losses": 2, "draws": 0, "stance": "orthodox", "date_of_birth": "1995-07-24", "data_api_link": "https://www.tapology.com/fightcenter/fighters/116334-christian-duncan", "img_link": "https://images.tapology.com/headshot_images/116334/large/cld2.jpg?1700662938", "name_index": "christian-leroy-duncan"}, "fighter_b_assessment": {"id": 3613, "fighter": 3614, "head_movement": 2, "gas_tank": 3, "aggression": 3, "desire_to_win": 2, "striking": 2, "chinny": 3, "grappling_offense": 0, "grappling_defense": 3}, "standardEvents": [{"name": "Fighter wins", "value": "WIN"}, {"name": "Fight lasts more than 1.5 rounds", "value": "ROUNDS_GEQ_ONE_AND_HALF"}, {"name": "Fight Does Not Go the Distance", "value": "DOES_NOT_GO_THE_DISTANCE"}], "predictions": {"WIN": {"3614": {"likelihood": 1, "label": "Very Likely", "justification": "- Win Via KO/Decision using striking, faster more dangerous, better chin\n- fought more dangerous opponents and survived"}, "118": {"likelihood": 4, "label": "Somewhat Unlikely", "justification": "- Unlikely Win Via TKO/KO slow Down duncan through grappling then generate enough power to kO him"}}, "DOES_NOT_GO_THE_DISTANCE": {"likelihood": 1, "label": "Very Likely", "justification": "- Anders has gotten dropped in his last 2 fights from short shots, duncan hits hard and fast and if anders gets dropped he'll get finished"}, "ROUNDS_GEQ_ONE_AND_HALF": {"likelihood": 3, "label": "Neutral", "justification": ""}}, "prediction": {"id": 277, "matchup": 1331, "prediction": 944, "isGamble": false, "isCorrect": true}, "pick": {"event": null, "fighter": null}}

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
    //console.log (route.path);
    // server.get_matchup_analysis(matchupId,onReceiveMatchupAnalysis);
    onReceiveMatchupAnalysis(sampleFetchResult);
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

  function updateOutcomePrediction(data){
    console.log(data);
    
  }

  return { matchup, fighter_a, fighter_b, predictions, pick,  standardEvents, pickOutcome, fetchMatchupDetails, updateOutcomePrediction }
});
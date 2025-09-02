import { ref,inject } from 'vue';
import { defineStore,storeToRefs } from 'pinia';
import { useMatchupStore } from '@/stores/matchupStore.js';
import { useRoute } from 'vue-router';
import server from '@/plugins/server';

export const useMatchupDetailStore = defineStore('matchupDetail', () => {
    //from the current url grab the corresponding matchup details from the 
    /*
    
    */
   const server = inject('server');
   const sampleFetchResult = {"matchup": {"id": 1415, "event": 127, "fighter_a": 3604, "fighter_b": 975, "weight_class": "lightweight", "rounds": 3, "isprelim": false, "outcome": null, "inWatchList": true, "analysisComplete": false}, "fighter_a": {"id": 3604, "first_name": "fares", "middle_name": null, "last_name": "ziam", "nick_name": "N/A", "weight_class": "lightweight", "height": 73, "reach": 75, "wins": 16, "losses": 4, "draws": 0, "stance": "orthodox", "date_of_birth": "1997-03-21", "data_api_link": null, "img_link": "https://images.tapology.com/headshot_images/119061/large/Fares_Ziam-hs.jpg?1667400450", "name_index": "fares-ziam"}, "fighter_a_assessment": {"id": 3603, "fighter": 3604, "head_movement": 3, "gas_tank": 3, "aggression": 2, "desire_to_win": 3, "striking": 3, "chinny": 0, "grappling_offense": 0, "grappling_defense": 3}, "fighter_b": {"id": 975, "first_name": "kaue", "middle_name": null, "last_name": "fernandes", "nick_name": "N/A", "weight_class": "lightweight", "height": 69, "reach": 73, "wins": 9, "losses": 2, "draws": 0, "stance": "Orthodox", "date_of_birth": "1995-03-17", "data_api_link": "https://www.tapology.com/fightcenter/fighters/173680-kau-fernandes", "img_link": "https://images.tapology.com/headshot_images/173680/large/Screenshot.png?1719502542", "name_index": "kaue-fernandes"}, "fighter_b_assessment": {"id": 974, "fighter": 975, "head_movement": 3, "gas_tank": 0, "aggression": 2, "desire_to_win": 0, "striking": 0, "chinny": 0, "grappling_offense": 0, "grappling_defense": 0}, "standardEvents": [{"name": "Fighter wins", "value": "WIN"}, {"name": "Fight lasts more than 1.5 rounds", "value": "ROUNDS_GEQ_ONE_AND_HALF"}, {"name": "Fight Does Not Go the Distance", "value": "DOES_NOT_GO_THE_DISTANCE"}], "eventLikelihoods": [], "prediction": null}
   
   const matchup = ref({});
   const fighter_a = ref({});
   const fighter_b = ref({});
   const standardEvents = ref([]);
   const pick = ref({});
   const predictions = ref([]);

   function onReceiveMatchupAnalysis(matchupComparison) {
        matchup.value = matchupComparison['matchup']
        fighter_a.value = matchupComparison['fighter_a'];
        fighter_b.value = matchupComparison['fighter_b'];
        standardEvents.value = matchupComparison['standardEvents'];
        if ('pick' in matchupComparison){
          pick.value = matchupComparison['pick']
        }
        // console.log (standardEvents.value);
        if ('predictions' in matchupComparison) {
          predictions.value = matchupComparison['predictions'];
        }
   }

   function fetchMatchupDetails(matchupId){
    //console.log (route.path);
    //server.get_matchup_analysis(matchupId,onReceiveMatchupAnalysis);
     onReceiveMatchupAnalysis(sampleFetchResult);
   }

   function onReceivePick(data) {
      console.log (data);
      pick.value = data;
   }

   function pickOutcome(outcome){

      const data = {'event':outcome.value};
      if (outcome.value === 'WIN'){
        data.fighter = outcome.fighterId;
      }
      
      server.make_pick(data,matchup.value.id,onReceivePick);

   }

   return { matchup,fighter_a,fighter_b,predictions,pick,fetchMatchupDetails,standardEvents,pickOutcome }
});
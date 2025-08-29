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
   
   const matchup = ref({});
   const fighter_a = ref({});
   const fighter_b = ref({});

   function onReceiveMatchupAnalysis(matchupComparison) {
        matchup.value = matchupComparison['matchup']
        fighter_a.value = matchupComparison['fighter_a'];
        fighter_b.value = matchupComparison['fighter_b'];
   }

   function fetchMatchupDetails(matchupId){
    // console.log (route.path);
    server.get_matchup_analysis(matchupId,onReceiveMatchupAnalysis)
   }

   return { matchup,fighter_a,fighter_b,fetchMatchupDetails }
});
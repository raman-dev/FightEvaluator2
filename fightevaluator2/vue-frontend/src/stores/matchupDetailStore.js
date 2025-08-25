import { ref } from 'vue';
import { defineStore,storeToRefs } from 'pinia';
import { useMatchupStore } from '@/stores/matchupStore.js';
import { useRoute } from 'vue-router';

export const useMatchupDetailStore = defineStore('matchupDetail', () => {
    //from the current url grab the corresponding matchup details from the 
    /*
    
    */
   const route = useRoute();

   function fetchMatchupDetails(){
    console.log (route.path);
   }

   return { fetchMatchupDetails }
});
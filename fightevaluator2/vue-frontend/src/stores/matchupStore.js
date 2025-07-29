import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

export const useMatchupStore = defineStore('matchup', () => {
  //3 tables
  //only show 1 action menu when right clicked 
  //right click only possible after row is active 
  //map of matchupId to matchupObjects
  //query server for matchups 
  const matchups = ref({
    'mainCard':{},
    'prelims':{}
});
  return { matchups }
  
})

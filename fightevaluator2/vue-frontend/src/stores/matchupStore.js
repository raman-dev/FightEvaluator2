import { ref, inject } from 'vue'
import { defineStore } from 'pinia'
import server from '../plugins/server.js'

export const useMatchupStore = defineStore('matchup', () => {
  //3 tables
  //only show 1 action menu when right clicked 
  //right click only possible after row is active 
  //map of matchupId to matchupObjects
  //query server for matchups 
  const server = inject('server');
  
  const event = ref ({});
  const mainCard = ref({});
  const prelims = ref({});

  function onReceiveEvent(eventData){
    console.log("Received event data:", eventData);
    //do what populate event and matchups 
    eventData.mainCardMatchups.forEach((matchup) => {
        mainCard.value[matchup.id] = matchup;
    });
    eventData.prelimMatchups.forEach((matchup) => {
        prelims.value[matchup.id] = matchup;
    });
    event.value = eventData.event;
  }

  async function fetchEvent(eventId){
    if (eventId === undefined || eventId === null) {
       server.get_next_event(onReceiveEvent);
    }
  }

  return { event,mainCard,prelims,fetchEvent }
  
})

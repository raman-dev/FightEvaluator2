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
  const event = ref({});
  const mainCard = ref({});
  const prelims = ref({});
  const watchlist = ref({});

  const defaultActiveMatchup = {table:null,id:-1,matchup:null};
  const activeMatchup = ref(defaultActiveMatchup);

  function onReceiveEvent(eventData) {
    console.log("Received event data: ", eventData.event.id);
    //do what populate event and matchups 
    event.value = {};
    mainCard.value = {};
    prelims.value = {};
    watchlist.value = {};
    activeMatchup.value = structuredClone(defaultActiveMatchup);

    eventData.mainCardMatchups.forEach((matchup) => {
      matchup['active'] = false;
      mainCard.value[matchup.id] = matchup;
      if (matchup.inWatchList) {
        watchlist.value[matchup.id] = structuredClone(matchup);
      }
    });
    eventData.prelimMatchups.forEach((matchup) => {
      matchup['active'] = false;
      prelims.value[matchup.id] = matchup;
      if (matchup.inWatchList) {
        watchlist.value[matchup.id] = structuredClone(matchup);
      }
    });
    event.value = eventData.event;
    // console.log(watchlist.value);
  }

  function getTableByName (tableName){
    if (tableName === 'MainCard') {
      return mainCard.value;
    } else if (tableName === 'Prelims') {
      return prelims.value;
    } else {
      return watchlist.value;
    }
  }

  function toggleActiveMatchUp(matchupId, tableName) {
    let table = getTableByName(tableName);
    // console.log (matchupId,tableName,activeMatchup.value);
    //prev active is clicked again to deactive
    if (activeMatchup.value.id === parseInt(matchupId) && activeMatchup.value.table === tableName){
        //deactive and return
        activeMatchup.value.id = -1;
        activeMatchup.value.table = null;
        activeMatchup.value.matchup = null;
        table[matchupId].active = false;
        return;
    }
    //any previous must be deactivated
    if (activeMatchup.value.id != -1){
      //deactivate
      let oldActive = getTableByName(activeMatchup.value.table);
      oldActive[activeMatchup.value.id].active = false;
      
      activeMatchup.value.table = null;
      activeMatchup.value.id = -1;
      activeMatchup.value.matchup = null;
    }
    let m = table[matchupId];
    m.active = !m.active;
    if (m.active){
      activeMatchup.value.id = m.id;
      activeMatchup.value.table = tableName;
      activeMatchup.value.matchup = m;
    }
  }

  async function fetchEvent(eventId) {
    if (eventId === undefined || eventId === null) {
      console.log('fetching next event');
      server.get_next_event(onReceiveEvent);
      // onReceiveEvent(sampleFetchResult);
    }else{
      console.log ('fetching event-specific',eventId);
      server.get_event(eventId,onReceiveEvent);
      // onReceiveEvent(sampleFetchResult);
    }
  }

  function getMatchup(matchupId){
    //return matchup data if in maincard or prelims
    console.log(`getMatchup.${matchupId}`);
    console.log (Object.keys(mainCard.value));
    if (matchupId in mainCard.value){
      return mainCard.value[matchupId];
    }

    if (matchupId in prelims.value){
      return prelims.value[matchupId];
    }

    return null;
  }

  return { event, mainCard, prelims, watchlist, activeMatchup, fetchEvent, toggleActiveMatchUp, getMatchup }

})
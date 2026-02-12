import { ref, inject } from 'vue'
import { defineStore } from 'pinia'
import server from '../plugins/server.js'
import { useIntervalFn, useTimeoutPoll } from '@vueuse/core'

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

  const defaultActiveMatchup = { table: null, id: -1, matchup: null };
  const activeMatchup = ref(defaultActiveMatchup);

  const poller = ref (null);

  function onReceiveEvent(eventData) {
    
    if (eventData.available === false){
      console.log("No event data available");
      return;
    }
    if (poller.value !== null){
      poller.value.pause();
      poller.value = null;
    }
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
      if (matchup['inWatchList'] === true) {
        watchlist.value[matchup.id] = structuredClone(matchup);
      }
    });
    eventData.prelimMatchups.forEach((matchup) => {
      matchup['active'] = false;
      prelims.value[matchup.id] = matchup;
      if (matchup['inWatchList'] === true) {
        watchlist.value[matchup.id] = structuredClone(matchup);
      }
    });
    event.value = eventData.event;
    // console.log('watchlist',watchlist.value);
  }

  function getTableByName(tableName) {
    if (tableName === 'MainCard') {
      return mainCard.value;
    } else if (tableName === 'Prelims') {
      return prelims.value;
    } else {
      return watchlist.value;
    }
  }

  function onReceiveToggleWatchListResult(data) {
    // should return the matchup with updated inWatchList status
    //if in watchlist is false
    //that means it was removed from watchlist
    //update watchlist table and active matchup if needed

    const matchup = getMatchup(data.id);
    matchup.inWatchList = data.inWatchList;
    if (matchup.inWatchList === true) {

      //create copy
      const copy = {};
      for (const key in matchup) {
        copy[key] = matchup[key];
      }
      watchlist.value[matchup.id] = copy;
    } else {
      //remove from watchlist
      delete watchlist.value[matchup.id];
    }

    //reset activeMatchup
    activeMatchup.value = structuredClone(defaultActiveMatchup);
  }

  function toggleWatchList() {
    if (activeMatchup.value.id === -1 || activeMatchup.value.table === null) {
      // console.log ('no active matchup to toggle watchlist');
      return;
    }

    //remove from watchlist
    server.toggle_watchlist(activeMatchup.value.id, onReceiveToggleWatchListResult);
    toggleActiveMatchUp(activeMatchup.value.id, activeMatchup.value.table);
  }

  function toggleActiveMatchUp(matchupId, tableName) {
    let table = getTableByName(tableName);
    // console.log (matchupId,tableName,activeMatchup.value);
    //prev active is clicked again to deactive
    if (activeMatchup.value.id === parseInt(matchupId) && activeMatchup.value.table === tableName) {
      //deactive and return
      activeMatchup.value.id = -1;
      activeMatchup.value.table = null;
      activeMatchup.value.matchup = null;
      table[matchupId].active = false;
      return;
    }
    //any previous must be deactivated
    if (activeMatchup.value.id != -1) {
      //deactivate
      let oldActive = getTableByName(activeMatchup.value.table);
      oldActive[activeMatchup.value.id].active = false;

      activeMatchup.value.table = null;
      activeMatchup.value.id = -1;
      activeMatchup.value.matchup = null;
    }
    let m = table[matchupId];
    m.active = !m.active;
    if (m.active) {
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
    } else {
      console.log('fetching event-specific', eventId);
      server.get_event(eventId, onReceiveEvent);
      // onReceiveEvent(sampleFetchResult);
    }
  }

  async function fetchEvent2(eventId){
    if (eventId === undefined || eventId === null) {
      console.log('fetching next event');
      server.get_next_event(onReceiveEvent);
    }
    else{
      console.log('fetching event-specific', eventId);
      server.get_event(eventId, onReceiveEvent);
    }
  }

  async function pollEvent(eventId){
    fetchEvent2(eventId);
    //doesn't run immediately even with option {immediate:true}
    const { isActive, pause, resume } = useTimeoutPoll(fetchEvent2.bind({},eventId),3000);

    poller.value = {isActive, pause, resume};
    poller.value['count'] = 0;

  }

  function getMatchup(matchupId) {
    //return matchup data if in maincard or prelims
    // console.log(`getMatchup.${matchupId}`);
    // console.log (Object.keys(mainCard.value));
    if (matchupId in mainCard.value) {
      return mainCard.value[matchupId];
    }

    if (matchupId in prelims.value) {
      return prelims.value[matchupId];
    }

    return null;
  }

  function onCreateMatchupResult(data) {
    console.log("Created matchup result:", data);
    const matchup = data;
    if (matchup.isprelim === true) {
      prelims.value[matchup.id] = matchup;
    } else {
      mainCard.value[matchup.id] = matchup;
    }
  }

  function createMatchup(matchupData) {
    server.create_matchup(matchupData, onCreateMatchupResult);
  }

  function onUpdateMatchupResult(data) {
    console.log("Updated matchup result:", data);
    const matchup = data;
    let existing = null;
    if (matchup.isprelim === true) {
      existing = prelims.value[matchup.id];
      //update existing fields with updated fields
    } else {
      existing = mainCard.value[matchup.id];
    }
    for (const key in matchup) {
      if (key in existing) {
        existing[key] = matchup[key];
      }
    }
  }

  function updateMatchup(matchupData) {
    server.update_matchup(matchupData, onUpdateMatchupResult, matchupData.id);
  }

  function onReceiveMatchupDeleteResult(data){
    console.log("Deleted matchup result:", data);
    const matchupId = data.id;
    if (matchupId in mainCard.value){
      delete mainCard.value[matchupId];
    }
    if (matchupId in prelims.value){
      delete prelims.value[matchupId];
    }
    if (matchupId in watchlist.value){
      delete watchlist.value[matchupId];
    }
    activeMatchup.value = structuredClone(defaultActiveMatchup);
  }

  function deleteMatchup(matchupId){
    server.delete_matchup(matchupId,onReceiveMatchupDeleteResult)
  }

  return {
    event,
    mainCard,
    prelims,
    watchlist,
    activeMatchup,
    fetchEvent,
    toggleActiveMatchUp,
    getMatchup,
    toggleWatchList,
    createMatchup,
    updateMatchup,
    deleteMatchup,
    pollEvent
  }

})
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

  const sampleFetchResult = { "event": { "id": 118, "title": "UFC Fight Night: Whittaker vs. de Ridder", "date": "2025-07-26", "location": null, "link": "https://www.tapology.com/fightcenter/events/125931-ufc-fight-night", "hasResults": false }, "mainCardMatchups": [{ "id": 1302, "event": 118, "fighter_a": 3507, "fighter_b": 3854, "weight_class": "middleweight", "rounds": 5, "isprelim": false, "outcome": null, "inWatchList": true, "analysisComplete": false, "fighter_a_name": "Robert Whittaker", "fighter_b_name": "Reinier De ridder" }, { "id": 1303, "event": 118, "fighter_a": 3569, "fighter_b": 3639, "weight_class": "bantamweight", "rounds": 3, "isprelim": false, "outcome": null, "inWatchList": true, "analysisComplete": false, "fighter_a_name": "Petr Yan", "fighter_b_name": "Marcus Mcghee" }, { "id": 1304, "event": 118, "fighter_a": 1922, "fighter_b": 236, "weight_class": "middleweight", "rounds": 3, "isprelim": false, "outcome": null, "inWatchList": true, "analysisComplete": false, "fighter_a_name": "Shara Magomedov", "fighter_b_name": "Marc-andre Barriault" }, { "id": 1305, "event": 118, "fighter_a": 3776, "fighter_b": 3797, "weight_class": "flyweight", "rounds": 3, "isprelim": false, "outcome": null, "inWatchList": true, "analysisComplete": false, "fighter_a_name": "Asu Almabayev", "fighter_b_name": "Jose Ochoa" }, { "id": 1306, "event": 118, "fighter_a": 1715, "fighter_b": 1270, "weight_class": "light_heavyweight", "rounds": 3, "isprelim": false, "outcome": null, "inWatchList": null, "analysisComplete": false, "fighter_a_name": "Nikita Krylov", "fighter_b_name": "Bogdan Guskov" }], "prelimMatchups": [{ "id": 1307, "event": 118, "fighter_a": 2148, "fighter_b": 3777, "weight_class": "bantamweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": true, "analysisComplete": false, "fighter_a_name": "Bryce Mitchell", "fighter_b_name": "Said Nurmagomedov" }, { "id": 1308, "event": 118, "fighter_a": 2846, "fighter_b": 3779, "weight_class": "welterweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": true, "analysisComplete": false, "fighter_a_name": "Muslim Salikhov", "fighter_b_name": "Carlos Leal" }, { "id": 1309, "event": 118, "fighter_a": 320, "fighter_b": 1226, "weight_class": "bantamweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": true, "analysisComplete": false, "fighter_a_name": "Da'mon Blackshear", "fighter_b_name": "Davey Grant" }, { "id": 1310, "event": 118, "fighter_a": 2699, "fighter_b": 2706, "weight_class": "strawweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": null, "analysisComplete": false, "fighter_a_name": "Amanda Ribas", "fighter_b_name": "Tabatha Ricci" }, { "id": 1311, "event": 118, "fighter_a": 179, "fighter_b": 3810, "weight_class": "light_heavyweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": null, "analysisComplete": false, "fighter_a_name": "Ibo Aslan", "fighter_b_name": "Billy Elekana" }, { "id": 1312, "event": 118, "fighter_a": 3558, "fighter_b": 2316, "weight_class": "featherweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": null, "analysisComplete": false, "fighter_a_name": "Mohammad Yahya", "fighter_b_name": "Steven Nguyen" }, { "id": 1313, "event": 118, "fighter_a": 434, "fighter_b": 3874, "weight_class": "heavyweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": null, "analysisComplete": false, "fighter_a_name": "Martin Buday", "fighter_b_name": "Marcus Buchecha" }] };
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
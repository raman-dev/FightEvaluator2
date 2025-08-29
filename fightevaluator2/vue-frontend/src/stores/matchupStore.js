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

  const sampleFetchResult = {"event": {"id": 127, "title": "UFC Fight Night: Imavov vs. Borralho", "date": "2025-09-06", "location": null, "link": "https://www.tapology.com/fightcenter/events/129146-ufc-fight-night", "hasResults": false}, "mainCardMatchups": [{"id": 1411, "event": 127, "fighter_a": 1474, "fighter_b": 354, "weight_class": "middleweight", "rounds": 5, "isprelim": false, "outcome": null, "inWatchList": true, "analysisComplete": false, "fighter_a_name": "Nassourdine Imavov", "fighter_b_name": "Caio Borralho"}, {"id": 1412, "event": 127, "fighter_a": 2830, "fighter_b": 3720, "weight_class": "lightweight", "rounds": 3, "isprelim": false, "outcome": null, "inWatchList": true, "analysisComplete": false, "fighter_a_name": "Benoit Saint-denis", "fighter_b_name": "Mauricio Ruffy"}, {"id": 1413, "event": 127, "fighter_a": 2378, "fighter_b": 1573, "weight_class": "lightweight", "rounds": 3, "isprelim": false, "outcome": null, "inWatchList": true, "analysisComplete": false, "fighter_a_name": "Bolaji Oki", "fighter_b_name": "Mason Jones"}, {"id": 1414, "event": 127, "fighter_a": 441, "fighter_b": 690, "weight_class": "light_heavyweight", "rounds": 3, "isprelim": false, "outcome": null, "inWatchList": true, "analysisComplete": false, "fighter_a_name": "Modestas Bukauskas", "fighter_b_name": "Paul Craig"}, {"id": 1415, "event": 127, "fighter_a": 3604, "fighter_b": 975, "weight_class": "lightweight", "rounds": 3, "isprelim": false, "outcome": null, "inWatchList": true, "analysisComplete": false, "fighter_a_name": "Fares Ziam", "fighter_b_name": "Kaue Fernandes"}, {"id": 1416, "event": 127, "fighter_a": 3851, "fighter_b": 3881, "weight_class": "featherweight", "rounds": 3, "isprelim": false, "outcome": null, "inWatchList": null, "analysisComplete": false, "fighter_a_name": "Patricio Pitbull", "fighter_b_name": "Losene Keita"}], "prelimMatchups": [{"id": 1417, "event": 127, "fighter_a": 3724, "fighter_b": 2702, "weight_class": "light_heavyweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": null, "analysisComplete": false, "fighter_a_name": "Oumar Sy", "fighter_b_name": "Brendson Ribeiro"}, {"id": 1418, "event": 127, "fighter_a": 3692, "fighter_b": 776, "weight_class": "heavyweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": null, "analysisComplete": false, "fighter_a_name": "Marcin Tybura", "fighter_b_name": "Ante Delija"}, {"id": 1419, "event": 127, "fighter_a": 953, "fighter_b": 3805, "weight_class": "welterweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": true, "analysisComplete": false, "fighter_a_name": "Rinat Fakhretdinov", "fighter_b_name": "Andreas Gustafsson"}, {"id": 1420, "event": 127, "fighter_a": 1172, "fighter_b": 3882, "weight_class": "featherweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": true, "analysisComplete": false, "fighter_a_name": "William Gomis", "fighter_b_name": "Robert Ruchaa"}, {"id": 1421, "event": 127, "fighter_a": 2486, "fighter_b": 3473, "weight_class": "welterweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": null, "analysisComplete": false, "fighter_a_name": "Sam Patterson", "fighter_b_name": "Trey Waters"}, {"id": 1422, "event": 127, "fighter_a": 3257, "fighter_b": 428, "weight_class": "middleweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": null, "analysisComplete": false, "fighter_a_name": "Brad Tavares", "fighter_b_name": "Robert Bryczek"}, {"id": 1423, "event": 127, "fighter_a": 213, "fighter_b": 3670, "weight_class": "strawweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": null, "analysisComplete": false, "fighter_a_name": "Shauna Bannon", "fighter_b_name": "Sam Hughes"}]}
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
      // server.get_next_event(onReceiveEvent);
      onReceiveEvent(sampleFetchResult);
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
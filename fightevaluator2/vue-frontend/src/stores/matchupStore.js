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
  
  //const sampleFetchResult = { "event": { "id": 118, "title": "UFC Fight Night: Whittaker vs. de Ridder", "date": "2025-07-26", "location": null, "link": "https://www.tapology.com/fightcenter/events/125931-ufc-fight-night", "hasResults": false }, "mainCardMatchups": [{ "id": 1302, "event": 118, "fighter_a": 3507, "fighter_b": 3854, "weight_class": "middleweight", "rounds": 5, "isprelim": false, "outcome": null, "inWatchList": true, "analysisComplete": false, "fighter_a_name": "Robert Whittaker", "fighter_b_name": "Reinier De ridder" }, { "id": 1303, "event": 118, "fighter_a": 3569, "fighter_b": 3639, "weight_class": "bantamweight", "rounds": 3, "isprelim": false, "outcome": null, "inWatchList": true, "analysisComplete": false, "fighter_a_name": "Petr Yan", "fighter_b_name": "Marcus Mcghee" }, { "id": 1304, "event": 118, "fighter_a": 1922, "fighter_b": 236, "weight_class": "middleweight", "rounds": 3, "isprelim": false, "outcome": null, "inWatchList": true, "analysisComplete": false, "fighter_a_name": "Shara Magomedov", "fighter_b_name": "Marc-andre Barriault" }, { "id": 1305, "event": 118, "fighter_a": 3776, "fighter_b": 3797, "weight_class": "flyweight", "rounds": 3, "isprelim": false, "outcome": null, "inWatchList": true, "analysisComplete": false, "fighter_a_name": "Asu Almabayev", "fighter_b_name": "Jose Ochoa" }, { "id": 1306, "event": 118, "fighter_a": 1715, "fighter_b": 1270, "weight_class": "light_heavyweight", "rounds": 3, "isprelim": false, "outcome": null, "inWatchList": null, "analysisComplete": false, "fighter_a_name": "Nikita Krylov", "fighter_b_name": "Bogdan Guskov" }], "prelimMatchups": [{ "id": 1307, "event": 118, "fighter_a": 2148, "fighter_b": 3777, "weight_class": "bantamweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": true, "analysisComplete": false, "fighter_a_name": "Bryce Mitchell", "fighter_b_name": "Said Nurmagomedov" }, { "id": 1308, "event": 118, "fighter_a": 2846, "fighter_b": 3779, "weight_class": "welterweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": true, "analysisComplete": false, "fighter_a_name": "Muslim Salikhov", "fighter_b_name": "Carlos Leal" }, { "id": 1309, "event": 118, "fighter_a": 320, "fighter_b": 1226, "weight_class": "bantamweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": true, "analysisComplete": false, "fighter_a_name": "Da'mon Blackshear", "fighter_b_name": "Davey Grant" }, { "id": 1310, "event": 118, "fighter_a": 2699, "fighter_b": 2706, "weight_class": "strawweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": null, "analysisComplete": false, "fighter_a_name": "Amanda Ribas", "fighter_b_name": "Tabatha Ricci" }, { "id": 1311, "event": 118, "fighter_a": 179, "fighter_b": 3810, "weight_class": "light_heavyweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": null, "analysisComplete": false, "fighter_a_name": "Ibo Aslan", "fighter_b_name": "Billy Elekana" }, { "id": 1312, "event": 118, "fighter_a": 3558, "fighter_b": 2316, "weight_class": "featherweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": null, "analysisComplete": false, "fighter_a_name": "Mohammad Yahya", "fighter_b_name": "Steven Nguyen" }, { "id": 1313, "event": 118, "fighter_a": 434, "fighter_b": 3874, "weight_class": "heavyweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": null, "analysisComplete": false, "fighter_a_name": "Martin Buday", "fighter_b_name": "Marcus Buchecha" }] };
  const event = ref({});
  const mainCard = ref({});
  const prelims = ref({});
  const watchlist = ref({});

  function onReceiveEvent(eventData){
    console.log("Received event data:", eventData);
    //do what populate event and matchups 
    eventData.mainCardMatchups.forEach((matchup) => {
        matchup['active'] = false;  
        mainCard.value[matchup.id] = matchup;
        if (matchup.inWatchList){
          watchlist.value[matchup.id] = matchup;
        }
    });
    eventData.prelimMatchups.forEach((matchup) => {
        matchup['active'] = false;
        prelims.value[matchup.id] = matchup;
        if (matchup.inWatchList){
          watchlist.value[matchup.id] = matchup;
        }
    });
    event.value = eventData.event;
    // console.log(watchlist.value);
  }

  function toggleActiveMatchUp(matchupId){
    
  }

  async function fetchEvent(eventId){
    if (eventId === undefined || eventId === null) {
       server.get_next_event(onReceiveEvent);
    }
  }

  return { event,mainCard,prelims,watchlist,fetchEvent, toggleActiveMatchUp }
  
})

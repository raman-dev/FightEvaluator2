import { ref, computed } from 'vue'
import { defineStore } from 'pinia'

import { useEventLikelihoodsStore } from './event_likelihoods';

export const useSelectedEventsStore = defineStore('selectedEvents',()=>{
    const events = ref({});
    
    function addEvent (matchupId,eventData,type,matchupTitle){
      if (!(matchupId in events.value)){
        events.value[matchupId] = {
          count:0,
          title:matchupTitle
        };

      }
      events.value[matchupId][type] = eventData;
      events.value[matchupId].count += 1;
    }
  
    function removeEvent(matchupId,type){
      if (matchupId in events.value){
        delete events.value[matchupId][type];
        events.value[matchupId].count -= 1;
        if (events.value[matchupId].count == 0){
            delete events.value[matchupId];
        }
      }
    }

    function clearEvents(){
        //remove all events
        delete events.value;
        events.value = {};
    }

    function getSelectedEvents(){
        return events.value;
    }
  
    return  {events,addEvent, removeEvent, clearEvents, getSelectedEvents} ;
  });
  
  
  export const useLinesStore = defineStore('lines',() => {
    const eventLikelihoodStore = useEventLikelihoodsStore();
    const lines = ref ([]) ;
    /*
      what are lines? lines - list of lines
        line ->
          map containing mathcup keys
            keys map to events that can become 
            true for a matchup
        line
          matchup_0
            event_0, likelihood, likelihood_val
            event_1, 
            .
            .
            .
          matchup_1
            event_0, likelihood, likelihood_val
            event_1, 
            .
            .
            .
        
            
    */
    function createLine(){  
      //needs current selections
      /*
         need input data
         as list
      */
         const result  = eventLikelihoodStore.getSelectedEvents();
         
         if (result.count > 0){
            lines.value.push(result.line);
         }
         eventLikelihoodStore.clearSelectedEvents()
    }

    function removeLine(){
  
    }

    function getLines() {
      return lines.value;
    }  

    return { lines,createLine,removeLine, getLines }
  
  })
  
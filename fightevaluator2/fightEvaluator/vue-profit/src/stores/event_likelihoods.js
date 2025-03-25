import { defineStore } from "pinia";
import { ref } from "vue";

export const useEventLikelihoodsStore = defineStore('eventLikelihoods',()=>{
    /*
        store eventlikelihoods here

        how to store?

        matchup_id
        title
        events:
            event_x
                likelihood
                likelihood_val
                justification
                //other stuff
            event_x_win
                []special case
        
        matchup_id:
            title
            events
                
    */
   const matchupLikelihoodData = ref({});

   function getData(){
    return matchupLikelihoodData.value;
   }

   function getSelectedEventsFromMap(eventMap,resultMap){
        for (const type in eventMap) {
            const event = eventMap[type];
            if (type == 'win'){
                for (const fighterEvent of event) {
                    if (fighterEvent.selected){
                        resultMap[type] = fighterEvent;
                        resultMap.count++;
                    }
                }
            }else{
                if (event.selected){
                    resultMap[type]= event;
                    resultMap.count++;
                }
            }
        }
   }

   function getSelectedEvents(){
        const line = {};
        let count = 0;
        for (const matchupId in matchupLikelihoodData.value) {
            const data = matchupLikelihoodData.value[matchupId];
            const eventMap = data.events;
            const selectedEventMap = {count:0};
            getSelectedEventsFromMap(eventMap,selectedEventMap);
            if (selectedEventMap.count > 0){
                line[matchupId] = {
                    matchupId : matchupId,
                    eventMap:selectedEventMap,
                    title:data.title
                };
                count++;
            }
        }
        return { line, count };
   }

   function clearSelectedEvents(){
    for (const matchupId in matchupLikelihoodData.value) {
        const data = matchupLikelihoodData.value[matchupId];
        const events = data.events;
        for (const type in events) {
            if (type == 'win'){
                for (const fighterEvent of events[type]) {
                    fighterEvent.selected = false;
                }
            }else{
                events[type].selected = false;
            }
        }
    }
   }

   function populateData(eventLikelihoodMap){
        // console.log(eventLikelihoodMap);
        for (const x in eventLikelihoodMap){
            const clone = structuredClone(eventLikelihoodMap[x]);
            // console.log(x);
            // x['selected'] = false;
            for (const eventType in clone['events']) {
                if (eventType == 'win'){
                    for (const fighterWin of clone['events'][eventType]) {
                        fighterWin['selected'] = false;
                    }
                }else{
                    clone['events'][eventType]['selected'] = false;
                }
            }
            matchupLikelihoodData.value[x] = clone;
        }
   }

   return  { matchupLikelihoodData,getData, populateData, getSelectedEvents, clearSelectedEvents };
});
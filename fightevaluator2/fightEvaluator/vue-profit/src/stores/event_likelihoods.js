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

   function populateData(eventLikelihoodMap){
        console.log(eventLikelihoodMap);
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

   return  { matchupLikelihoodData,getData, populateData };
});
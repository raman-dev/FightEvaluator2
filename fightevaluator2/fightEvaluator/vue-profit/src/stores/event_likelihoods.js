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
    */
   const matchupLikelihoodData = ref([]);

   function getData(){
    return matchupLikelihoodData.value;
   }

   function populateData(eventLikelihoodDataList){
        console.log(eventLikelihoodDataList);
        for (const data of eventLikelihoodDataList){
            const x = structuredClone(data);
            // console.log(x);
            x['selected'] = false;
            matchupLikelihoodData.value.push(x);
        }
   }

   return  { matchupLikelihoodData,getData, populateData };
});
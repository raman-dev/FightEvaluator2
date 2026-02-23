import { defineStore } from "pinia";
import { ref,inject } from "vue";

export const useEventLikelihoodStore = defineStore("eventLikelihood",()=>{
    const fightEvent = ref({});
    const eventTypes = ref([]);
    const eventLikelihoods = ref([]);

    const server = inject('server');

    function onReceiveEventLikelihoods(result){
        console.log('onReceiveEventlikelihoods',result.data);
        const data = result.data;
        
        fightEvent.value = data.fightEvent;
        eventTypes.value = data.eventTypes;
        eventLikelihoods.value = data.eventLikelihoods;
    }

    async function fetchEventLikelihoods(eventId){
        //grab likelihoods for specific event or latest event
        let id = eventId;
        const reIsInt = /^\d+$/; 
        if (typeof(id) !== 'string' || !reIsInt.test(eventId)){
            id = "";
        }
        
        console.log(`id = ${id}`);
        server.get_event_likelihoods(id,onReceiveEventLikelihoods);
    }

    return  {
        fetchEventLikelihoods,
        fightEvent,
        eventTypes,
        eventLikelihoods,
    }
});
import { defineStore } from "pinia";
import { ref,inject } from "vue";

export const useEventLikelihoodStore = defineStore("eventLikelihood",()=>{
    const fightEvent = ref({});
    const eventTypes = ref([]);
    const eventLikelihoods = ref([]);

    const server = inject('server');

    const sampleResult = {"data": {"fightEvent": {"id": 159, "title": "UFC Fight Night: Adesanya vs. Pyfer", "date": "2026-03-28", "location": null, "link": "https://www.tapology.com/fightcenter/events/136873-ufc-fight-night", "hasResults": false}, "eventLikelihoods": [{"matchup": 1847, "title": "Adesanya vs Pyfer", "likelihoods": {"WIN": [{"fighter_a": {"id": 19, "name": "Israel Adesanya"}, "likelihood": 0, "justification": ""}, {"fighter_b": {"id": 3662, "name": "Joe Pyfer"}, "likelihood": 0, "justification": ""}], "ROUNDS_GEQ_ONE_AND_HALF": {"likelihood": 0, "justification": ""}, "DOES_NOT_GO_THE_DISTANCE": {"likelihood": 0, "justification": ""}}}, {"matchup": 1849, "title": "Chiesa vs Price", "likelihoods": {"WIN": [{"fighter_a": {"id": 581, "name": "Michael Chiesa"}, "likelihood": 0, "justification": ""}, {"fighter_b": {"id": 2611, "name": "Niko Price"}, "likelihood": 0, "justification": ""}], "ROUNDS_GEQ_ONE_AND_HALF": {"likelihood": 0, "justification": ""}, "DOES_NOT_GO_THE_DISTANCE": {"likelihood": 0, "justification": ""}}}, {"matchup": 1850, "title": "Erosa vs Douglas", "likelihoods": {"WIN": [{"fighter_a": {"id": 930, "name": "Julian Erosa"}, "likelihood": 0, "justification": ""}, {"fighter_b": {"id": 3953, "name": "Lerryan Douglas"}, "likelihood": 0, "justification": ""}], "ROUNDS_GEQ_ONE_AND_HALF": {"likelihood": 0, "justification": ""}, "DOES_NOT_GO_THE_DISTANCE": {"likelihood": 0, "justification": ""}}}, {"matchup": 1851, "title": "Abdul-malik vs Belgaroui", "likelihoods": {"WIN": [{"fighter_a": {"id": 3783, "name": "Mansur Abdul-malik"}, "likelihood": 0, "justification": ""}, {"fighter_b": {"id": 268, "name": "Yousri Belgaroui"}, "likelihood": 0, "justification": ""}], "ROUNDS_GEQ_ONE_AND_HALF": {"likelihood": 0, "justification": ""}, "DOES_NOT_GO_THE_DISTANCE": {"likelihood": 0, "justification": ""}}}, {"matchup": 1852, "title": "Mckinney vs Nelson", "likelihoods": {"WIN": [{"fighter_a": {"id": 2058, "name": "Terrance Mckinney"}, "likelihood": 0, "justification": ""}, {"fighter_b": {"id": 2304, "name": "Kyle Nelson"}, "likelihood": 0, "justification": ""}], "ROUNDS_GEQ_ONE_AND_HALF": {"likelihood": 0, "justification": ""}, "DOES_NOT_GO_THE_DISTANCE": {"likelihood": 0, "justification": ""}}}, {"matchup": 1853, "title": "Bahamondes vs Musayev", "likelihoods": {"WIN": [{"fighter_a": {"id": 200, "name": "Ignacio Bahamondes"}, "likelihood": 0, "justification": ""}, {"fighter_b": {"id": 3867, "name": "Tofiq Musayev"}, "likelihood": 0, "justification": ""}], "ROUNDS_GEQ_ONE_AND_HALF": {"likelihood": 0, "justification": ""}, "DOES_NOT_GO_THE_DISTANCE": {"likelihood": 0, "justification": ""}}}, {"matchup": 1857, "title": "Stirling vs Lopes", "likelihoods": {"WIN": [{"fighter_a": {"id": 3800, "name": "Navajo Stirling"}, "likelihood": 0, "justification": ""}, {"fighter_b": {"id": 1871, "name": "Bruno Lopes"}, "likelihood": 0, "justification": ""}], "ROUNDS_GEQ_ONE_AND_HALF": {"likelihood": 0, "justification": ""}, "DOES_NOT_GO_THE_DISTANCE": {"likelihood": 0, "justification": ""}}}, {"matchup": 1858, "title": "Simon vs Yanez", "likelihoods": {"WIN": [{"fighter_a": {"id": 3052, "name": "Ricky Simon"}, "likelihood": 0, "justification": ""}, {"fighter_b": {"id": 3572, "name": "Adrian Yanez"}, "likelihood": 0, "justification": ""}], "ROUNDS_GEQ_ONE_AND_HALF": {"likelihood": 0, "justification": ""}, "DOES_NOT_GO_THE_DISTANCE": {"likelihood": 0, "justification": ""}}}], "eventTypes": [{"type": "WIN", "label": "Fighter wins"}, {"type": "ROUNDS_GEQ_ONE_AND_HALF", "label": "Fight lasts more than 1.5 rounds"}, {"type": "DOES_NOT_GO_THE_DISTANCE", "label": "Fight Does Not Go the Distance"}]}};

    function onReceiveEventLikelihoods(result){
        console.log('onReceiveEventlikelihoods',result.data);
        const data = result.data;
        
        fightEvent.value = data.fightEvent;
        eventTypes.value = data.eventTypes;
        eventLikelihoods.value = data.eventLikelihoods;
    }

    async function fetchEventLikelihoods(eventId){
        // onReceiveEventLikelihoods(sampleResult);
        //grab likelihoods for specific event or latest event
        let id = eventId;        
        const reIsInt = /^\d+$/; 
        if (typeof(id) !== 'number'){
            if (typeof(id) !== 'string' || !reIsInt.test(eventId)){
                id = "";
            }
        }
        
        console.log(`filtered.id = ${id}, received.id = ${eventId}`);
        server.get_event_likelihoods(id,onReceiveEventLikelihoods);
    }

    return  {
        fetchEventLikelihoods,
        fightEvent,
        eventTypes,
        eventLikelihoods,
    }
});
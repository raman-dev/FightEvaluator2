import { defineStore } from "pinia";
import { ref } from "vue";
import { useLinesStore } from "./lines";
import { DataSet } from "vis-data";

export const useGraphStore = defineStore('graph',()=>{
    const show = ref(false);
    const linesStore = useLinesStore();

    const nodes = new DataSet([]);
    const edges = new DataSet([]);

    function toggleGraph(){

        const lines = linesStore.getLines();
        console.log(lines);
        /*
        
            a node is what?
                matchup_id is unique, events are unique
                matchup_id.event_a0
                matchup_id.event_a1
                matchup_id.event_a2

        */
        for (const line of lines) {
            //what is  a line
            //line is a map 
            /*
                create a node for every event for every matchup

            */
           for (const matchupId in line) {
            
           }

            
        }
        show.value = !show.value;

        return show.value;
    }

    return  { show,toggleGraph }
});
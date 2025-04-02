import { defineStore } from "pinia";
import { ref } from "vue";
import { useLinesStore } from "./lines";
import { DataSet } from "vis-data";
import { Network } from "vis-network";

export const useGraphStore = defineStore('graph',()=>{
    const show = ref(false);
    const linesStore = useLinesStore();

    const nodes = new DataSet([]);
    const edges = new DataSet([]);
    const options = {
        // physics: {
        //     barnesHut: {
        //       avoidOverlap: 1 // Prevents nodes from overlapping
        //     }
        // },
        // autoResize: false,
        // layout:{
        //     // hierarchical:{
        //         // enabled:true,
        //         // direction:"LR",
        //         // levelSeparation: 150,
                nodeSpacing: 150,
            // },
        // },
        // interaction:{
            // dragNodes:false,
        // },
        edges:{
            arrows:'to'
        },
        nodes: {
            shape: "box",
            font: {
              bold: {
                color: "#0077aa",
              },
            },
          },
    };

    function toggleGraph(){

        const lines = linesStore.getLines();
        console.log(nodes);
        /*
        
            a node is what?
                matchup_id is unique, events are unique
                matchup_id.event_a0
                matchup_id.event_a1
                matchup_id.event_a2

        */
        let prev = null;
        for (const line of lines) {
            //what is  a line
            //line is a map 
            /*
                create a node for every event for every matchup

            */
           for (const matchupId in line) {
                const { eventMap, title } = line[matchupId];
                for (const type in eventMap) {
                    if (type == 'count'){
                        continue;
                    }
                    const nodeId = `${matchupId}|${type}`;
                    let node = nodes.get(nodeId);
                    let nodeLabel = `${title}\n${type}`;
                    if (node == null || node == undefined){
                        node = {
                            id: nodeId,
                            label : nodeLabel,
                        }
                        console.log ('creating node => ',node);
                        nodes.add(node);
                    }
                    if (prev != null){
                        edges.add({
                            from: prev.id, to: node.id
                        });
                    }
                    prev = node;
                }
                prev = null;
           }
        }
        show.value = !show.value;
        
        return show.value;
    }

    function getVisNetwork(container){
        if (show.value == false){
            return null;
        }
        const data = {
            nodes: nodes,
            edges: edges
        };
        return new Network(container,data,options);
    }

    return  { show,toggleGraph,getVisNetwork }
});
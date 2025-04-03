import { defineStore } from "pinia";
import { ref } from "vue";
import { useLinesStore } from "./lines";
import { DataSet } from "vis-data";
import { Network } from "vis-network";

export const useGraphStore = defineStore('graph',()=>{
    const show = ref(false);
    const linesStore = useLinesStore();

    const nodes = new DataSet([]);
    let edges = new DataSet([]);

    const options = {
        physics:{
            hierarchicalRepulsion : {
                avoidOverlap:1
            }
        },
        layout:{
            hierarchical: {
                direction:"DU"
            }
        },
        edges:{
            arrows:'to'
        },
        nodes: {
            shape: "box",
            font: {
              bold: {
                color: "#000000",
              },
            },
          },
    };

    function styleNode(node,type,data){
        const {likelihood,fighter} = data;
        let label = '';
        let color = ''
        if (type == 'win'){
            label = `${fighter} wins`;
        }else if (type=='rounds_geq_one_half') {
            label = 'Rounds >= 1.5';
        }else { 
            label = 'Does Not Go The Distance';
        }

        switch (likelihood){
            case 'very likely':
                color = '#00ff00';
                break;
            case 'somewhat likely':
                color = '#80ff00';
                break;
            case 'neutral':
                color = '#ffc107';
                break;
            case 'somewhat unlikely':
                color = '#ed7b26';
                break;
            case 'very unlikely':
                color = '#dc3545';
                break;
            default://not predicted
                color = '#52565a';
                break;
        }

        node.label = '<b>'+ label + '</b>';
        node.color = color;
        node.font = {
            multi:true
        }
    }

    function toggleGraph(){

        const lines = linesStore.getLines();
        edges = new DataSet([]);
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
                for (const eventType in eventMap) {
                    if (eventType == 'count'){
                        continue;
                    }
                    const nodeId = `${matchupId}|${eventType}`;
                    let node = nodes.get(nodeId);
                    let nodeLabel = `${title}\n${eventType}`;
                    if (node == null || node == undefined){
                        node = {
                            id: nodeId,
                            label : nodeLabel,
                        }
                        console.log ('creating node => ',node);
                        nodes.add(node);
                        styleNode(node,eventType,eventMap[eventType]);
                    }
                    if (prev != null){
                        edges.add({
                            from: prev.id, to: node.id
                        });
                    }
                    prev = node;
                }
           }
           prev = null;
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
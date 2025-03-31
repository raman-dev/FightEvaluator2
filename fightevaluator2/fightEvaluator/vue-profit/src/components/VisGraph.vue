<script setup>
import { useGraphStore } from '@/stores/graphs';
import { storeToRefs } from 'pinia';
import { Network} from 'vis-network';
import { DataSet } from 'vis-data';
import { onMounted, useTemplateRef } from 'vue';

const graphStore = useGraphStore();
const { show } = storeToRefs(graphStore);

const graphRef = useTemplateRef('mGraph');


onMounted(()=>{
    // create an array with nodes
    const nodes = new DataSet([
        {id: 1, label: 'Node 1'},
        {id: 2, label: 'Node 2'},
        {id: 3, label: 'Node 3'},
        {id: 4, label: 'Node 4'},
        {id: 5, label: 'Node 5'}
    ]);
     // create an array with edges
     const edges = new DataSet([
        {from: 1, to: 3,id:0},
        {from: 1, to: 3,id:1},
        {from: 1, to: 2},
        {from: 2, to: 4},
        {from: 2, to: 5}
    ]);

     // create a network
    const container = graphRef.value;//document.getElementById('mGraph');
    // provide the data in the vis format
    console.log(container);
    const data = {
        nodes: nodes,
        edges: edges
    };
    const options = {
        // autoResize: false,
        layout:{
            hierarchical:{
                enabled:true,
                // direction:"LR",
                levelSeparation: 150,
                nodeSpacing: 150,
            },
        },
        // interaction:{
            // dragNodes:false,
        // },
        edges:{
            arrows:'to'
        }
    };

    // initialize your network!
    const network = new Network(container, data, options);
    console.log(network);
    // function updateGraph(nodeList){
    //     /*
    //         graph can be changed by adding nodes to nodes list
    //         and connected by adding edges to edges list
    //     */
    //    nodeList.sort((a,b) => {return a.order - b.order});
    //    let prev = null;
    //    let prevOdds = 1;
    //    for (let i = 0;i < nodeList.length;i++){
    //         let { order,name,odds } =  nodeList[i]; //destructure the object literal
    //         odds = parseFloat(odds);
    //         let node = nodes.get(order);    
    //         if (node == undefined || node == null){
    //             node = {
    //                 id:order,
    //                 label:name,
    //                 value:odds,
    //             };
    //             nodes.add(node);
    //         }
    //         if (prev != null){
    //             //create an edge between current and prev
    //             edges.add({
    //                 from: prev.id,
    //                 to: node.id,
    //                 label: `${(prevOdds * odds).toFixed(2)}` 
    //             });
    //         }
    //         prev = node;
    //         prevOdds *= odds;
    //    }
    // }
});


</script>
<template>
    <div class="content d-flex flex-column justify-content-center align-items-center" v-if="show">
        <div class="graph-container border">
            <div class="graph-controls d-flex justify-content-end">
                <button class="btn btn-danger" @click="show = !show">close</button>
            </div>
            <div class="graph" ref="mGraph" id="mynetwork">
            </div>
        </div>
    </div>
    
</template>

<style scoped lang="scss">

.content{
    position: absolute;
    left: 0%;
    top: 0%;
    width: 100%;
    height: 100%;    

    background-color: rgba(0,0,0,0.2);
}


.graph-container{
    .graph{
        height: 100%;
        width: 100%;
        background-color: blue;
    }
    height: 60%;
    width: 80%;
}

</style>
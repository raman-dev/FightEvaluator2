<script setup>
import { useGraphStore } from '@/stores/graphs';
import { storeToRefs } from 'pinia';
import { Network} from 'vis-network';
import { onMounted, ref, useTemplateRef, watch } from 'vue';

const graphStore = useGraphStore();
const { show } = storeToRefs(graphStore);

const graphRef = useTemplateRef('mGraph');
const network = ref(null);

watch (graphRef,async (newVal,oldVal) => {
    if(newVal != null){
        network.value = graphStore.getVisNetwork(newVal);//new Network(newVal,data,options);
    }else{
        network.value = null;//release memory type shit
    }
});

onMounted(()=>{

     // create a network
    // const container = graphRef.value;//document.getElementById('mGraph');
    // provide the data in the vis format
    // console.log(container);
    // // initialize your network!
    // network.value = new Network(container, data, options);
    // console.log(network);
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
        background-color: lavender;
    }
    height: 60%;
    width: 80%;
}

</style>
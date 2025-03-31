<script setup>

import { useGraphStore } from '@/stores/graphs';
import { useLinesStore } from '@/stores/lines';
import { storeToRefs } from 'pinia';
import { ref } from 'vue';

const linesStore = useLinesStore();
const graphStore = useGraphStore();

const { show } = storeToRefs(graphStore);

function createLine(){
    linesStore.createLine();
}

</script>

<template>
     <div class="d-flex justify-content-between my-1">
        <button class="btn btn-outline-secondary" @click="deselectAll()">deselect all</button>
        <button class="btn btn-outline-info" @click="createLine()">line +</button>
        <button class="btn btn-outline-info toggle-graph" @click="graphStore.toggleGraph()">
            <span class="d-flex" v-if="!show">show</span>
            <span class="d-flex" v-else>hide</span>
        </button>
    </div>
</template>

<style scoped lang="scss">

.toggle-graph{
    span{
        width: 5ch;
        justify-content: center;
    }
}

</style>
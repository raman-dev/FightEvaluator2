<script setup>

import { useLinesStore } from '@/stores/lines';

const linesStore = useLinesStore();

function createLine(){
    linesStore.createLine();
}

</script>

<template>
     <div class="d-flex justify-content-between my-1">
        <button class="btn btn-outline-secondary" @click="deselectAll()">deselect all</button>
        <button class="btn btn-outline-info" @click="createLine()">line +</button>
    </div>
</template>
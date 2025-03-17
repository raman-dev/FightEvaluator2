<script setup>
import { useLinesStore } from '@/stores/lines';
import { storeToRefs } from 'pinia';
import Line from './Line.vue';


const linesStore = useLinesStore();
const  { lines } = storeToRefs(linesStore);

</script>
<!--  
    line is a map
        matchup_id_0 -> events
        matchup_id_1 -> events
        matchup_id_2 -> events 
-->
<template>
    <div>
        <h3>Lines</h3>
        <div class="line-container d-flex flex-wrap">
            <template v-for="line in lines">
                <Line :line="line" />
            </template>
        </div>
    </div>
</template>

<style scoped lang="scss">
    .line-container {
        width: 100%;
        flex-direction: column;
        gap: 0.6rem;
    }
</style>
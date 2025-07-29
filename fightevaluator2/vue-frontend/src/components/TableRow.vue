<script setup>
import {defineModel} from 'vue';

const matchup = defineModel ('matchup',{
    default : {
        id: null,
        fighter_a : -1,
        fighter_b: -1,
        fighter_a_name: '',
        fighter_b_name: '',
        weight_class: '',
        rounds: 0,
        analysisComplete: false,
        inWatchList: false
    }
});


const props = defineProps(['tableName']); 

</script>
<template>
    <tr >
        <td>{{ matchup.fighter_a_name }} vs {{ matchup.fighter_b_name }}</td>
        <td>{{ matchup.weight_class }}</td>
        <td>{{ matchup.rounds }}</td>
        <td v-if="props.tableName === 'WatchList'"> {{ matchup.analysisComplete ? 'Yes' : 'No' }}</td>
    </tr>
</template>
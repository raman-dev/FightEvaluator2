<script setup>
import {defineModel} from 'vue';

const matchup = defineModel ('matchup',{});
//     default : {
//         id: null,
//         fighter_a : -1,
//         fighter_b: -1,
//         fighter_a_name: '',
//         fighter_b_name: '',
//         weight_class: '',
//         rounds: 0,
//         analysisComplete: false,
//         inWatchList: false
//     }
// });


const props = defineProps(['tableName']); 

</script>
<template>
    <tr :class="{active:matchup.active}" class="matchup">
        <td>{{ matchup.fighter_a_name }} vs {{ matchup.fighter_b_name }}</td>
        <td class="weightclass">{{ matchup.weight_class }}</td>
        <td>{{ matchup.rounds }}</td>
        <td v-if="props.tableName === 'WatchList'"> {{ matchup.analysisComplete ? 'Yes' : 'No' }}</td>
    </tr>
</template>

<style lang="scss" scoped>
    .matchup{
        user-select: none;
    }
    
    .matchup:hover{
        background-color: hsl(200, 56%, 12%);
        cursor: pointer;
    }
    //hover active order matters to not change active color when hover and active
    .matchup.active{
        background-color: hsl(175, 61.57%, 24.95%);
    }

    td.weightclass{
        text-transform: capitalize;
    }

</style>
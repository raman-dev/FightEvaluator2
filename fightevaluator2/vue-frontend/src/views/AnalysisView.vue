<script setup>
import { onMounted,ref } from 'vue';
import { useMatchupDetailStore } from '@/stores/matchupDetailStore';
import { onBeforeRouteUpdate, useRoute } from 'vue-router';
import { useMatchupStore } from '@/stores/matchupStore';
import { storeToRefs } from 'pinia';

const matchupDetailStore = useMatchupDetailStore();
const matchupStore = useMatchupStore();
const route = { useRoute }
const { matchupId } = defineProps(['matchupId'])
const matchup = ref({});

onMounted(()=>{
    // matchupDetailStore.fetchMatchupDetails()
    console.log(matchupId);
    
    matchup.value = matchupStore.getMatchup("" + matchupId);
})

</script> 
<template>
    <div class="">
        <h1>AnalysisView : {{ matchupId }}</h1>
        <ul>
            <li>
                <RouterLink :to="'/v-assessment/' + matchup.fighter_a">{{matchup.fighter_a}}</RouterLink>
            </li>
            <li>
                <RouterLink :to="'/v-assessment/' + matchup.fighter_b">{{ matchup.fighter_b }}</RouterLink>
            </li>
        </ul>
    </div>
</template>
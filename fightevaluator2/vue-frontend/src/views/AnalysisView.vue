<script setup>
import { onMounted,ref } from 'vue';
import { useMatchupDetailStore } from '@/stores/matchupDetailStore';
import { useMatchupStore } from '@/stores/matchupStore';
import FighterCard from '@/components/assessment/FighterCard.vue';


const matchupDetailStore = useMatchupDetailStore();
const matchupStore = useMatchupStore();
const { matchupId } = defineProps(['matchupId'])
const matchup = ref({});

onMounted(()=>{
    matchupDetailStore.fetchMatchupDetails(matchupId);
})

</script> 
<template>
    <div class="container-fluid">
        <h1>AnalysisView : {{ matchupId }}</h1>
        <div class="d-flex mx-auto">
            <FighterCard 
                v-model:fighter="matchupDetailStore.fighter_a" 
                :fullSize="false"></FighterCard>
            <FighterCard 
                v-model:fighter="matchupDetailStore.fighter_b" 
                :fullSize="false"
                :rtlImage="true"
                ></FighterCard>
        </div>
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
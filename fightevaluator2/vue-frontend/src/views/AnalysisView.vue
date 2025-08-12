<script setup>
import { onMounted } from 'vue';
import { useMatchupDetailStore } from '@/stores/matchupDetailStore';

const matchupDetailStore = useMatchupDetailStore();

onMounted(()=>{
    matchupDetailStore.fetchMatchupDetails()
})

</script> 
<template>
    <div class="">
        <h1>AnalysisView</h1>
    </div>
</template>
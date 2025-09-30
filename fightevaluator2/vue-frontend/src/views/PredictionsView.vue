<script setup>
import { usePredictionStore } from '@/stores/predictionsStore';
import { onMounted } from 'vue';


const predictionStore = usePredictionStore();

onMounted(()=>{
    predictionStore.getPredictions();
});
</script>

<template>
    <h1>predictions</h1>
</template>
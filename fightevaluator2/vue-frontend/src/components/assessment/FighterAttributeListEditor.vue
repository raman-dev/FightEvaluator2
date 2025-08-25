<script setup>
import { useAssessmentStore } from '@/stores/assessmentStore';
import { storeToRefs } from 'pinia';


const { assessment } = storeToRefs(useAssessmentStore);

</script>

<template>
    <h2>AttrListEditor</h2>
</template>
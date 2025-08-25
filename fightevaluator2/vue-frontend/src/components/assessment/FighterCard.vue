<script setup>
import { useAssessmentStore } from '@/stores/assessmentStore';
import { storeToRefs } from 'pinia';

const { bio } = storeToRefs(useAssessmentStore());

</script>
<template>
    <h2>FighterCard</h2>
</template>
<script setup>

import FighterCard from '@/components/assessment/FighterCard.vue';
import FighterAttributeListEditor from '@/components/assessment/FighterAttributeListEditor.vue';
import NotesEditor from '@/components/assessment/NotesEditor.vue';
import NotesList from '@/components/assessment/NotesList.vue';
import { useAssessmentStore } from '@/stores/assessmentStore';
import { onMounted } from 'vue';

/*
    
*/

const assessmentStore = useAssessmentStore(); 

onMounted(()=>{
    assessmentStore.fetchAssessment();
});
</script>


<template>
    <FighterCard :fighter="assessmentStore.fighter"></FighterCard>
    <FighterAttributeListEditor></FighterAttributeListEditor>
    <NotesEditor></NotesEditor>
    <NotesList :notes="assessmentStore.notes"></NotesList>
</template>
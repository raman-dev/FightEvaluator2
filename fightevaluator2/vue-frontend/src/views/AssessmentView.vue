<script setup>

import FighterCard from '@/components/assessment/FighterCard.vue';
import FighterAttributeListEditor from '@/components/assessment/attributeEditor/FighterAttributeListEditor.vue';
import NotesEditor from '@/components/assessment/noteEditor/NotesEditor.vue';
import NotesList from '@/components/assessment/noteEditor/NotesList.vue';
import { useAssessmentStore } from '@/stores/assessmentStore';
import { onMounted,ref, provide } from 'vue';
import { useRoute } from 'vue-router';

/*
    
*/

const assessmentStore = useAssessmentStore();
const activeNote = ref(null);

const route = useRoute();

provide ('activeNote',activeNote);
const fighterId = ref(0);

onMounted(() => {
    console.log ('calling assessment.onMounted')
    fighterId.value = route.params.fighterId;
    assessmentStore.fetchAssessment(fighterId.value);
});

</script>


<template>
    <FighterCard :fighter="assessmentStore.fighter"></FighterCard>
    <FighterAttributeListEditor></FighterAttributeListEditor>
    <div class="fighter-notes list-group-item d-flex flex-column">
        <NotesEditor v-model:activeNote="activeNote"></NotesEditor>
        <NotesList :notes="assessmentStore.notes" v-model:activeNote="activeNote"></NotesList>
    </div>
</template>

<style lang="scss">
$positiveBg: #0d6efd;
$negativeBg: #dc3545;
$neutralBg: #ffc107;
$outlineColor : #3d7efd;

$backgroundColor: #212529;
// $cardColor: #242a34;
$cardBorderColor: #131b23;
$cardColor: #12161A;

$color-0: #01161E;
$color-1: #124559;
$color-2: #598392;
$color-3: #AEC3B0;
$color-4: #EFF6E0;

// $backgroundColor: #01121E;
// $cardColor: #124554;

$btnBackgroundColor: #598392;
$btnBorderColor: black;
$btnBorderRadius: 0.6rem;
$btnClickBackground: #5983928f;

button:hover{               
    box-shadow: black 4px 4px 0 0;
}

.fighter-notes {
    max-width: 48ch;
    padding: 1rem !important;
    margin: 0.5rem;
    height: fit-content;

    margin-bottom: 1rem;
    background-color: $cardColor;
}

.list-group-item {
  margin-bottom: 1rem;
  background-color: $cardColor !important;
  // border: 2px solid #242a30 !important;
  outline: 3px solid transparent !important;
  outline-offset: 2px !important;
  border-radius: 0.5rem !important;  
}

</style>
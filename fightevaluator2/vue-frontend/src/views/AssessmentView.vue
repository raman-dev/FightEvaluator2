<script setup>

import FighterCard from '@/components/assessment/FighterCard.vue';
import FighterAttributeListEditor from '@/components/assessment/attributeEditor/FighterAttributeListEditor.vue';
import NotesEditor from '@/components/assessment/noteEditor/NotesEditor.vue';
import NotesList from '@/components/assessment/noteEditor/NotesList.vue';
import FighterEditor from '@/components/assessment/FighterEditor.vue';

import { useAssessmentStore } from '@/stores/assessmentStore';
import { onMounted, ref, provide } from 'vue';
import { useRoute } from 'vue-router';


const assessmentStore = useAssessmentStore();
const activeNote = ref(null);

const route = useRoute();
const showModal = ref(false);
provide('activeNote', activeNote);
const fighterId = ref(0);

onMounted(() => {
    console.log('calling assessment.onMounted')
    fighterId.value = route.params.fighterId;
    assessmentStore.fetchAssessment(fighterId.value);
});

function onClickFighterEdit() {
    console.log('onClickFighterEdit');
    showModal.value = true;
}

function onFighterEditorClose() {
    showModal.value = false;
}

function onFighterEditorSave(changes) {
    console.log('onFighterEditorSave',changes);
    assessmentStore.updateFighter(changes);
}

function onAttributeChange(changes) {
    console.log('onAttributeChange',changes);
    assessmentStore.updateAssessment(changes);
}

</script>


<template>
    <div class="main-container transition-wrapper-root">
        <div class="content-container">
            <FighterCard 
                v-model:fighter="assessmentStore.fighter"
                v-model:nextMatchup="assessmentStore.nextMatchup"
                @edit-click="onClickFighterEdit">
            </FighterCard>
            <div class="grid-container">
                <FighterAttributeListEditor @attribute-change="onAttributeChange"></FighterAttributeListEditor>
                <div class="fighter-notes list-group-item d-flex flex-column">
                    <NotesEditor v-model:activeNote="activeNote"></NotesEditor>
                    <NotesList :notes="assessmentStore.notes" v-model:activeNote="activeNote"></NotesList>
                </div>
            </div>
            
        </div>
        <FighterEditor 
            v-model:showModal="showModal" 
            :fighterServer="assessmentStore.fighter"
            @update-fighter="onFighterEditorSave">
        </FighterEditor>
    </div>
</template>

<style lang="scss" scoped>
$positiveBg: #0d6efd;
$negativeBg: #dc3545;
$neutralBg: #ffc107;
$outlineColor : #3d7efd;

$cardColor: #12161A;
$btnBorderRadius: 0.6rem;


.fighter-notes {
    max-width: 48ch;
    padding: 1rem !important;
    // margin: 0.5rem;
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

.transition-wrapper-root {
    overflow-y: auto;
}

.content-container{
  margin: auto;
  width: 72%;
  padding: 0.4rem;
}

.grid-container{
  display: flex; 
  column-gap: 1rem;
  width: 100%;
  max-width: 100%;
}

@media (max-width: 1280px) {
    .content-container {
        margin: 0px;
        width: 100%;
    }
}

@media (max-width: 1024px) {
    .grid-container {
        flex-direction: column;
    }

    .fighter-notes {
        max-width: 100%;
    }
}

</style>
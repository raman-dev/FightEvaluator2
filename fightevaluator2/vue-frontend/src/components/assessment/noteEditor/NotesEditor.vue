<script setup>
import { useAssessmentStore } from '@/stores/assessmentStore';
import { useTemplateRef } from 'vue';

const noteEditorRef = useTemplateRef('noteEditor');
const activeNote = defineModel('activeNote');
const assessmentStore = useAssessmentStore();


function addNote(){
    const editor = noteEditorRef.value;
    const noteText = editor.textContent.trim();
    editor.textContent = '';//empty editor
    assessmentStore.addNote(noteText);
}

function deleteNote(){
    if (activeNote.value != null){
        const noteId = activeNote.value.id;
        activeNote.value = null;
        console.log(`deleting note.${noteId}`)
        assessmentStore.deleteNote(noteId);
        
    }
}

// function hasActive(){
//     return activeNote.value === null;
// }
</script>

<template>
    <div class="notes-title">
        <h4>Notes - Things to consider about this fighter...</h4>
    </div>
    <!--unordered scrollable list of p tags wrapped in li-->
    <!--textarea made with div and contenteditable -->
    <div class="note-editor-container d-flex flex-column">
        <div class="note-editor-actions">
            <div class="action-wrapper">
                <button class="btn btn-success note-submit-btn mx-2" @click="addNote">
                    submit
                </button>
            </div>
            <div class="action-wrapper">
                <button class="btn btn-danger note-delete-btn" :class="{'disabled': activeNote == null}" @click="deleteNote">
                    delete
                </button>
            </div>

        </div>
        <div class="note-editor align-self-center" :data-tag="NEUTRAL" contenteditable="plaintext-only" ref="noteEditor"></div>
    </div>
</template>

<style lang="scss" scoped>

.note-editor-actions button:hover {
    box-shadow: black 4px 4px 0 0;
}

.notes-title {
    padding: 0.5rem;
}

.note-editor-container {
    row-gap: 0.5rem;

    .note-submit-btn {
        margin-left: auto;
        max-width: fit-content;
    }

    .note-editor {
        overflow: hidden;
        background-color: #212529;
        border: 1px solid #343a40;
        border-radius: 0.5rem;
        outline: 0px solid #3d7efd;
        padding-top: 0.2rem;
        padding-left: 0.4rem;
        padding-right: 0.2rem;

        width: 100%;
        // max-width: 32ch;
        word-break: break-word;
        min-height: 4rem;
        transition: outline 0.05s ease-out;


    }

    /* show light electric blue outline when note-editor is focused */
    .note-editor:focus {
        outline-width: 3px;
        border-color: transparent;
    }
}

.note-editor-container .note-editor-actions {
    display: flex;
    justify-content: end;
}

</style>
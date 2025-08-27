<script setup>

import { ref } from 'vue';
import Note from './Note.vue';

const notes = defineModel('notes');
</script>

<template>
    <div class="notes-list align-self-center mt-4">
        <ul v-if="notes.length > 0">
            <template v-for="note,index in notes" :key="index">
                <Note v-model:note="notes[index]" ></Note>
            </template>
        </ul>
    </div>
</template>

<style lang="scss" scoped>
.notes-list {
    width: 100%;
    ul {
        // border: 1px solid #343a40 !important
        border-radius: 0.5rem;
        // overflow-y: scroll;
        // overflow-x: hidden;
        margin: 0px;
        width: 100%;
        padding: 0px;
    }
}
</style>
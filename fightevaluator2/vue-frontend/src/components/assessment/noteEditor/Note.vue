<script setup>
import { watch,inject, ref, onMounted } from 'vue';

const note = defineModel('note');
// const active = ref(false);
const activeNote = inject('activeNote');
const active = ref(false);

const formatDateShort = inject('formatDateShort');

function onClickNote(){
    // console.log ('Clicked Note',note.value.data);
    if (activeNote.value == null){
        activeNote.value = note.value;
        // active.value = true;
    }else if (activeNote.value.id === note.value.id){
        //deactivate self
        // active.value = false;
        activeNote.value = null;
    }else {
        //activenote has a value that is different than mine
        activeNote.value = note.value;
        // active.value = true;
    }
}

watch (activeNote,(newNote,oldNote) => {
    // console.log ('watch!',oldNote,newNote)
    if (newNote == null || newNote.id != note.value.id){
        active.value = false;
    }
    else if (newNote.id == note.value.id){
        active.value = true;
    }
})



</script>

<template>
    <li class="note" :class="{'active':active}" :tabindex="100" @click="onClickNote" :data-timestamp="note.createdAt">
        <span class="timestamp">{{ formatDateShort(note.createdAt) }}</span>
        <p>{{ note.data }}</p>
    </li>
</template>

<style lang="scss" scoped>
.note {
    background-color: #212529;
    // border: 1px solid lavender;
    border-radius: 0.6rem;
    list-style: None;
    display: flex;
    flex-direction: column;
    padding: 1rem;
    padding-top: 0.6rem;
    margin: 1rem;

    p {
        word-break: break-word;
        text-wrap: wrap;
        min-width: 32ch;
        max-width: 100%;
        margin: 0px;
    }

    .timestamp{
        opacity: 0.7;
        font-size: 0.75rem;
        text-align: end;
        margin-bottom: 0.25rem;
    }
}

// .note:focus{
//   outline: 3px solid #3d7efd;
//   outline-offset: 2px;
// }

.note.active {
    outline: 3px solid #3d7efd;
    outline-offset: 2px;
}

.note:hover {
    cursor: pointer;
}
</style>
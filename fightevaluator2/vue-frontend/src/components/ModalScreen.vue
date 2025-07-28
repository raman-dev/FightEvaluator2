<script setup>
    
import { watch } from 'vue';

const show = defineModel('show',{default: false});
const emits = defineEmits(['screenClick'])

function onClickScreen(){
    show.value = !show.value;
    emits('screenClick');
}

</script>

<template>
    <div class="modal-screen" :class="{show : show}" @click="onClickScreen()">
    </div>
</template>

<style lang="scss">
    .modal-screen {
        position: absolute;
        display: flex;
        justify-content: center;
        width: 100%;
        height: 100%;
        left: 0px;
        top: 0px;
        background-color: rgba(0, 0, 0, 0);
        pointer-events: none;
        z-index: 1000;
        transition: background-color 0.2s ease-in-out;
    }

    .modal-screen.show{
        background-color: rgba(0, 0, 0, 0.5);
        pointer-events: initial;
    }
</style>
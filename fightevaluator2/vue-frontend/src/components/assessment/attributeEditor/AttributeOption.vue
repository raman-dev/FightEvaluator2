<script setup>
import { inject } from 'vue';

const attribInfoMap = inject('attribInfoMap');
const props = defineProps(['optionState','selected','state'])

</script>

<template>
    <div class="attrib-option" :data-option-state="props.optionState" :selected="props.selected">
        <h5 class="option">{{ props.state }}</h5>
        <p class="description"></p>
    </div>
</template>
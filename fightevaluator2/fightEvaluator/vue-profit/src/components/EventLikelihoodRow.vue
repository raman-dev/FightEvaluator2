<script setup>

import { onMounted, ref, useTemplateRef } from 'vue';
import EventLikelihood from './EventLikelihood.vue';

const props = defineProps(['matchup_id', 'events', 'title']);
const emits = defineEmits(['height-change']);
const expanded = ref(false);
const tr = useTemplateRef('matchup-tr');

function expandClick() {
    expanded.value = !expanded.value;
}

const maxUpdates = ref(0);
const updates = ref(0);
const heightChange = ref(0);
function resizeRow(height_delta){
    //take max delta
    if (height_delta < 0){
        updates.value -= 1;
        heightChange.value = Math.min(heightChange.value,height_delta);
    }else{
        updates.value += 1;
        heightChange.value = Math.max(heightChange.value,height_delta);
    }
    //if updates count == maxUpdates
    //transition the table with the change in height
    if (Math.abs(updates.value) == maxUpdates.value){
        emits('height-change',heightChange.value);
        updates.value = 0;
    }
}

onMounted(()=>{
    maxUpdates.value = tr.value.children.length;
});

</script>

<template>

    <tr ref="matchup-tr">
        <td>
            <div class="matchup-wrapper">
                <a href="/matchup/1091">
                    {{ props.title }}
                </a>
                <button class="expand-toggle btn btn-outline-info" @click="expandClick()">expand</button>
            </div>
        </td>

        <template v-for="(event, type) in props.events" :key="type">
            <td>
                <div class="d-flex justify-content-evenly align-items-start" v-if="type == 'win'">
                    <EventLikelihood v-bind="event[0]" :type="type" v-model="expanded" @height-change="resizeRow"/>
                    <EventLikelihood v-bind="event[1]" :type="type" v-model="expanded" @height-change="resizeRow"/>
                </div>
                <div v-else>
                    <EventLikelihood v-bind="event" v-model="expanded" @height-change="resizeRow"/>
                </div>
            </td>
        </template>
    </tr>

</template>

<style lang="scss" scoped>
.matchup-wrapper {
    display: flex;
    justify-content: space-between;
    align-items: center;

    a {
        color: white;
        text-decoration: none;
        white-space: nowrap;
    }

    a:hover {
        text-decoration: underline;
    }

    button{
        margin-left: 0.6rem;
    }
}
</style>
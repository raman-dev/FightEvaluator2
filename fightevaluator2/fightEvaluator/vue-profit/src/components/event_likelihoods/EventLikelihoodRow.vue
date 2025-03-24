<script setup>

import { onMounted, ref, useTemplateRef } from 'vue';
import EventLikelihood from './EventLikelihood.vue';
import { useSelectedEventsStore } from '@/stores/lines';

const props = defineProps(['matchupId', 'title']);
const emits = defineEmits(['height-change']);
const expanded = ref(false);

const events = defineModel('events');

const tr = useTemplateRef('matchup-tr');
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


function onClickEvent(event,type){
    //flip state of type,event
    // console.log(event,type);
    if (type == 'win'){
        const [fighterAObj,fighterBObj] = events.value[type];
        let clickedFighterEvent = fighterAObj;
        let other = fighterBObj;
        if (event.fighter != clickedFighterEvent.fighter){
            clickedFighterEvent = fighterBObj;
            other = fighterAObj;
        }
        if (clickedFighterEvent.selected == true){
            clickedFighterEvent.selected = false;
        }else{
            clickedFighterEvent.selected = true;
            other.selected = false;
        }
    }else{
        if (events.value[type].selected == true){
            events.value[type].selected = false;
        }else{
            events.value[type].selected = true;
        }
    }
}

</script>

<template>

    <tr ref="matchup-tr">
        <td>
            <div class="matchup-wrapper">
                <a href="/matchup/1091">
                    {{ props.title }}
                </a>
                <button class="expand-toggle btn btn-outline-info" @click="expanded = !expanded">expand</button>
            </div>
        </td>

        <template v-for="(event, type) in events" :key="type">
            <td>
                <div class="d-flex justify-content-evenly align-items-start" v-if="type == 'win'">
                    <EventLikelihood 
                        v-bind="event[0]" 
                        :type="type" 
                        v-model="expanded"
                        v-model:isSelected="event[0].selected"
                        @height-change="resizeRow"
                        @click="onClickEvent(event[0],type)"/> 
                    <EventLikelihood 
                        v-bind="event[1]" 
                        :type="type" 
                        v-model="expanded" 
                        v-model:isSelected="event[1].selected"
                        @height-change="resizeRow" 
                        @click="onClickEvent(event[1],type)"/>
                </div>
                <div v-else>
                    <EventLikelihood 
                        v-bind="event" 
                        :type="type" 
                        v-model="expanded" 
                        v-model:isSelected="events[type].selected"
                        @height-change="resizeRow" 
                        @click="onClickEvent(event,type)"/>
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
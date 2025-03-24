<script setup>

import { onMounted, ref, useTemplateRef } from 'vue';
import EventLikelihood from './EventLikelihood.vue';
import { useSelectedEventsStore } from '@/stores/lines';

const props = defineProps(['matchupId', 'events', 'title']);
const emits = defineEmits(['height-change']);
const expanded = ref(false);

const selectedEvents = ref({
    'win':{},
    'rounds_geq_one_half':false,
    'does_not_go_the_distance':false
});

const selectedEventsStore = useSelectedEventsStore();
const eventLikelihoodObject = {};

const currentWinner = ref();

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
    const eventsMap = props.events; //
    const winEventData = eventsMap['win'];
    
    for (const eventType in eventsMap){
        if (eventType == 'win'){
            const [fighter_a,fighter_b] = winEventData;
            selectedEvents.value['win'][fighter_a.fighter] = false;
            selectedEvents.value['win'][fighter_b.fighter] = false;
        }else{
            selectedEvents.value[eventType] = false;
        }
    }
    currentWinner.value = null;
});


function onClickEvent(event,type){
    //flip state of type,event
    if (type == 'win'){
        //selected same fighter -> deselec`t
        if (selectedEvents.value[type][event.fighter] == true){
            selectedEvents.value[type][event.fighter] = false;
            currentWinner.value = null;
            
            selectedEventsStore.removeEvent(props.matchupId,type);
        }else{
            //deselect previous
            if (currentWinner.value != null){
                selectedEvents.value[type][currentWinner.value] = false;
                selectedEventsStore.removeEvent(props.matchupId,type);
            }
            selectedEvents.value[type][event.fighter] = true; 
            selectedEventsStore.addEvent(props.matchupId,event,type,props.title);
            currentWinner.value = event.fighter;
        }
    }else{
        if (selectedEvents.value[type] == true){
            selectedEvents.value[type] = false;
            selectedEventsStore.removeEvent(props.matchupId,type);
        }else{
            selectedEvents.value[type] = true;
            selectedEventsStore.addEvent(props.matchupId,event,type,props.title);
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

        <template v-for="(event, type) in props.events" :key="type">
            <td>
                <div class="d-flex justify-content-evenly align-items-start" v-if="type == 'win'">
                    <EventLikelihood 
                        v-bind="event[0]" 
                        :type="type" 
                        v-model="expanded"
                        v-model:isSelected="selectedEvents[type][event[0].fighter]"
                        @height-change="resizeRow"
                        @click="onClickEvent(event[0],type)"/> 
                    <EventLikelihood 
                        v-bind="event[1]" 
                        :type="type" 
                        v-model="expanded" 
                        v-model:isSelected="selectedEvents[type][event[1].fighter]"
                        @height-change="resizeRow" 
                        @click="onClickEvent(event[1],type)"/>
                </div>
                <div v-else>
                    <EventLikelihood 
                        v-bind="event" 
                        :type="type" 
                        v-model="expanded" 
                        v-model:isSelected="selectedEvents[type]"
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
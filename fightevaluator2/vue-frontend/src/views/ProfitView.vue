<script setup>
import { useEventLikelihoodStore } from '@/stores/eventLikelihoodStore';
import { storeToRefs } from 'pinia';
import { onMounted } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

const eventLikelihoodStore = useEventLikelihoodStore()
const { fightEvent,eventLikelihoods,eventTypes } = storeToRefs(eventLikelihoodStore);
const { fetchEventLikelihoods } = eventLikelihoodStore;


onMounted(() => {
    //if no eventid we get empty string
    fetchEventLikelihoods(route.params.eventId);
})

</script>
<template>
    <div class="main-container container">
        <h1>Profit</h1>
        <table class="table table-bordered">
            <!--
                table of what?
            -->
            <thead>
                <tr>
                    <th v-for="data in eventTypes">
                        {{ data.label }}
                    </th>
                </tr>
            </thead>
            <tbody>
                <!--have what here-->
                <tr v-for="value in source"></tr>
            </tbody>
        </table>
    </div>
    
</template>
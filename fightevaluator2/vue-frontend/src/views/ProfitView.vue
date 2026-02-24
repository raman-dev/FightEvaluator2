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
        <table class="table table-bordered table-hover">
            <!--
                table of what?
            -->
            <thead>
                <tr>
                    <th>MatchUp</th>
                    <th v-for="data in eventTypes">
                        {{ data.label }}
                    </th>
                </tr>
            </thead>
            <tbody>
                <!--have what here-->
                <tr v-for="data in eventLikelihoods" :key="data.matchup">
                    <th>
                        {{ data.title }}
                    </th>
                    <!--
                        for every type in eventType
                        check data if type is in data
                         if it is then render td with value
                            else render td with 0
                    -->
                    <td v-for="eventType in eventTypes" :key="eventType.type">
                        <div v-if="eventType.type in data.likelihoods && eventType['type'] !== 'WIN'">
                            <div>{{ data.likelihoods[eventType.type].likelihood }}</div>
                            <div class="justification">
                                {{ data.likelihoods[eventType.type].justification }}
                            </div>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
    
</template>
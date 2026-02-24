<script setup>
import PredictionRow from '@/components/prediction-table/PredictionRow.vue';
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
    <div class="main-container container-fluid">
        <h1>Profit</h1>
        <table class="table table-bordered table-hover">
            <!--
                table of what?
            -->
            <thead>
                <tr>
                    <th>MatchUp</th>
                    <template v-for="data in eventTypes" >
                        <template v-if="data.type !== 'WIN'">
                            <th>{{ data.label }}</th>
                        </template>
                        <template v-else>
                            <th>Win A</th>
                            <th>Win B</th>
                        </template>
                    </template>
                </tr>
            </thead>
            <tbody>
                <!--have what here-->
                <template v-for="data in eventLikelihoods">
                    <PredictionRow :matchup-data="data"></PredictionRow>
                </template>
            </tbody>
        </table>
    </div>
    
</template>

<style lang="scss" scoped>
table {
    font-size: 14px;
}
table thead{
    th{
        max-width: 20ch;
        text-align: center;
    }
}

.main-container {
    margin: auto;
    max-width: 85%;
}

// @media (max-width: 1280px) {
//     .main-container {
//         max-width: 85%;
//     }
// }

@media (max-width: 1024px) {

    
    .main-container {
        max-width: 100%;
    }
}

@media (max-width: 768px) {

    
    .main-container {
        max-width: 100%;
    }
}
</style>
<script setup>
import PredictionRow from '@/components/prediction-table/PredictionRow.vue';
import SearchBox from '@/components/SearchBox.vue';
import { useEventLikelihoodStore } from '@/stores/eventLikelihoodStore';
import { storeToRefs } from 'pinia';
import { onMounted,ref,watch,inject } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();

const eventLikelihoodStore = useEventLikelihoodStore()
const { fightEvent,eventLikelihoods,eventTypes } = storeToRefs(eventLikelihoodStore);
const { fetchEventLikelihoods } = eventLikelihoodStore;

const searchBoxInput = ref('');
const searchResults = ref([]);
const server = inject('server');

onMounted(() => {
    //if no eventid we get empty string
    fetchEventLikelihoods(route.params.eventId);
})

function onReceiveFightEventSearchResults(results){
    // console.log(results);
    searchResults.value = results.result;
}

function onFightEventSelect(fightEvent) {
    // console.log(`selected => ${fightEventId}`);
    //update the page 
    fetchEventLikelihoods(fightEvent.id);
}

function onClickOutOfSearchBox() {
    console.log("onClickOutOfSearchBox");
    // searchBoxInput.value ="";
}

watch (searchBoxInput, (inputValue,_) => {
    const queryString = inputValue.trim().replaceAll(" ","-");
    if (queryString.length == 0){
        onReceiveFightEventSearchResults({result:[]});
        return;
    }
    // console.log(`searchBoxInput: ${queryString}`);
    server.search_events(onReceiveFightEventSearchResults,queryString)
});

</script>
<template>
    <div class="main-container container-fluid">
        <div class="title-container d-flex justify-content-between mb-2">
            <h5 class="my-0">{{fightEvent.title}} Prediction Table</h5>
            <SearchBox 
                v-model:result-list="searchResults" 
                v-model:search-box-input="searchBoxInput"
                placeholder="Find Event..."
                @select-result="onFightEventSelect"
                @input-box-defocus="onClickOutOfSearchBox"></SearchBox>
        </div>
        
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

.title-container{
    min-height: 42px;
    max-height: 42px;
}
table {
    font-size: 14px;
}

table thead{
    th{
        max-width: 20ch;
        text-align: center;
        padding: 0.3rem !important;
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
<script setup>
import PredictionRow from '@/components/prediction-table/PredictionRow.vue';

import SearchFilterBox from '@/components/SearchFilterBox.vue';
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
}

watch (searchBoxInput, (inputValue,_) => {
    const queryString = inputValue.trim().replaceAll(" ","-");
    if (queryString.length == 0){
        onReceiveFightEventSearchResults({result:[]});
        return;
    }
    // console.log(`searchBoxInput: ${queryString}`);
    server.search_events(onReceiveFightEventSearchResults,queryString);
});

watch (searchResults,(newValue,oldValue) => {
    console.log ('changed',newValue,oldValue);
});

</script>
<template>
    <div class="main-container container-fluid">
        <div class="title-container">
            <h5 class="my-0">{{fightEvent.title}} Prediction Table</h5>
            
            
            <SearchFilterBox v-model:search-results="searchResults"></SearchFilterBox>

            <!--
                render search results in a list 
                paginate
            -->
            <div class="border search-results-wrapper mb-2">
                <div class="event-container p-2">
                    <div class="fight-event-item p-2 rounded-2 m-1" v-for="result in searchResults">
                        <span class="title">{{ result.title }}</span>
                    </div>
                </div>
            </div>
            
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
.event-container {
    display: grid;
    grid-template-columns: repeat(4,1fr);

    .fight-event-item{
        max-width: 15rem;
        background-color: #12161a;
    }
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

@mixin width-lg {
    > *{
        margin: auto;
        width: 58%;
    }
}

@mixin width-md {
    > *{
        margin: auto;
        width: 85%;
    }
}

@mixin width-sm {
    > *{
        margin: auto;
        width: 100%;
    }
}

.main-container {
    // margin: auto;
    // max-width: 58%;
    @include width-lg;
}

// @media (max-width: 1280px) {
//     .main-container {
//         max-width: 85%;
//     }
// }

@media (max-width: 1024px) {

    .main-container {
        @include width-md;
    }
}

@media (max-width: 768px) {
    .main-container {
        @include width-sm;
    }
}
</style>
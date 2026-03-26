<script setup>
import SearchBox from '@/components/SearchBox.vue';
import { useEventLikelihoodStore } from '@/stores/eventLikelihoodStore';
import { storeToRefs } from 'pinia';
import { onMounted,ref,watch,inject } from 'vue';
import { useRoute } from 'vue-router';

const route = useRoute();
const eventLikelihoodStore = useEventLikelihoodStore()
const { fightEvent } = storeToRefs(eventLikelihoodStore);

const searchBoxInput = ref('');
const searchResults = defineModel('searchResults',{required: false,default:[]});

const server = inject('server');

const year = ref(null)
const month = ref(null);

// const sampleSearchResult = {"msg": "valid", "params": {"year": null, "month": null, "query": "hollow"}, "results": [{"title": "UFC 326: Holloway vs. Oliveira 2", "id": 156, "data": "2026-03-07"}, {"title": "UFC 318: Holloway vs. Poirier 3", "id": 117, "data": "2025-07-19"}, {"title": "UFC 308: Topuria vs. Holloway", "id": 65, "data": "2024-10-26"}]};
onMounted(() => {
    //if no eventid we get empty string
    eventLikelihoodStore.fetchEventLikelihoods(route.params.eventId);
})
function onReceiveFightEventSearchResults(data){
    // console.log('data=>',data);
    searchResults.value = data.results;
}

function onFightEventSelect(fightEvent) {
    // console.log(`selected => ${fightEventId}`);
    //update the page 
    eventLikelihoodStore.fetchEventLikelihoods(fightEvent.id);
}

function onClickOutOfSearchBox() {
    console.log("onClickOutOfSearchBox");
}


function onClickSearch() {
    //grab search 
    const query = searchBoxInput.value;
    // grab year val
    const yearIn = year.value;
    // grab month val
    const monthIn = month.value;

    // if (query.trim().length == 0 && yearIn === null && monthIn === null){
    //     return;//don't search nothing to search
    // }
    // server.search_events2(query,yearIn,monthIn,onReceiveFightEventSearchResults)
    
    onReceiveFightEventSearchResults(sampleSearchResult);

}

</script>
<template>
    <div class="border">
        <!--what does this have hear 
            year field select
            month field select 
            and search box for event name or fighter name
        -->
        <div class="d-flex flex-column">
            <SearchBox 
                v-model:search-box-input="searchBoxInput"
                @search-click="onClickSearch"
                placeholder="Find Event...">
            </SearchBox>

            <div class="filters d-flex gap-2">
                <!--year select box-->
                <select class="form-select form-select-sm" v-model="year" aria-label=".form-select-sm example">
                    <option selected :value="null">Year</option>
                    <option :value="2026">2026</option>
                    <option :value="2025">2025</option>
                    <option :value="2024">2024</option>
                    <option :value="2023">2023</option>
                </select>
                <!--month select box-->
                <select class="form-select form-select-sm" v-model="month" aria-label=".form-select-sm example">
                    <option selected :value="null">Month</option>
                    <option :value="1">January</option>
                    <option :value="2">February</option>
                    <option :value="3">March</option>
                    <option :value="4">April</option>
                    <option :value="5">May</option>
                    <option :value="6">June</option>
                    <option :value="7">July</option>
                    <option :value="8">August</option>
                    <option :value="9">September</option>
                    <option :value="10">October</option>
                    <option :value="11">November</option>
                    <option :value="12">December</option>
                </select>
            </div>
        </div>
            
    </div>
</template>
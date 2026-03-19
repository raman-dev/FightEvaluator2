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
const searchResults = ref([]);
const server = inject('server');

onMounted(() => {
    //if no eventid we get empty string
    eventLikelihoodStore.fetchEventLikelihoods(route.params.eventId);
})
function onReceiveFightEventSearchResults(results){
    // console.log(results);
    searchResults.value = results.result;
}
function onFightEventSelect(fightEvent) {
    // console.log(`selected => ${fightEventId}`);
    //update the page 
    eventLikelihoodStore.fetchEventLikelihoods(fightEvent.id);
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
    server.search_events(onReceiveFightEventSearchResults,queryString)
});
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
                v-model:result-list="searchResults" 
                :search-on-input="false"
                placeholder="Find Event...">
            </SearchBox>
            <div class="filters d-flex gap-2">
                <!--year select box-->
                <select class="form-select form-select-sm" aria-label=".form-select-sm example">
                    <option selected>Year</option>
                    <option value="1">2026</option>
                    <option value="2">2025</option>
                    <option value="3">2024</option>
                    <option value="4">2023</option>
                </select>
                <!--month select box-->
                <select class="form-select form-select-sm" aria-label=".form-select-sm example">
                    <option selected>Month</option>
                    <option value="1">January</option>
                    <option value="2">February</option>
                    <option value="3">March</option>
                    <option value="4">April</option>
                    <option value="5">May</option>
                    <option value="6">June</option>
                    <option value="7">July</option>
                    <option value="8">August</option>
                    <option value="9">September</option>
                    <option value="10">October</option>
                    <option value="11">November</option>
                    <option value="12">December</option>
                </select>
            </div>
        </div>
            
    </div>
</template>
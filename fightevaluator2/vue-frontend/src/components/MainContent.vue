<script setup>

import { onMounted, ref } from 'vue';
import Table from './Table.vue';

const sampleFetchResult = {
    "event": {"id": 118, "title": "UFC Fight Night: Whittaker vs. de Ridder", "date": "2025-07-26", "location": null, "link": "https://www.tapology.com/fightcenter/events/125931-ufc-fight-night", "hasResults": false}, 
    "mainCardMatchups": [
        {"id": 1302, "event": 118, "fighter_a": 3507, "fighter_b": 3854, "weight_class": "middleweight", "rounds": 5, "isprelim": false, "outcome": null, "inWatchList": true, "analysisComplete": false}, 
        {"id": 1303, "event": 118, "fighter_a": 3569, "fighter_b": 3639, "weight_class": "bantamweight", "rounds": 3, "isprelim": false, "outcome": null, "inWatchList": true, "analysisComplete": false}, 
        {"id": 1304, "event": 118, "fighter_a": 1922, "fighter_b": 236, "weight_class": "middleweight", "rounds": 3, "isprelim": false, "outcome": null, "inWatchList": true, "analysisComplete": false}, 
        {"id": 1305, "event": 118, "fighter_a": 3776, "fighter_b": 3797, "weight_class": "flyweight", "rounds": 3, "isprelim": false, "outcome": null, "inWatchList": true, "analysisComplete": false},
        {"id": 1306, "event": 118, "fighter_a": 1715, "fighter_b": 1270, "weight_class": "light_heavyweight", "rounds": 3, "isprelim": false, "outcome": null, "inWatchList": null, "analysisComplete": false}], 
    "prelimMatchups": [
        {"id": 1307, "event": 118, "fighter_a": 2148, "fighter_b": 3777, "weight_class": "bantamweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": true, "analysisComplete": false}, {"id": 1308, "event": 118, "fighter_a": 2846, "fighter_b": 3779, "weight_class": "welterweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": true, "analysisComplete": false}, {"id": 1309, "event": 118, "fighter_a": 320, "fighter_b": 1226, "weight_class": "bantamweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": true, "analysisComplete": false}, {"id": 1310, "event": 118, "fighter_a": 2699, "fighter_b": 2706, "weight_class": "strawweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": null, "analysisComplete": false}, {"id": 1311, "event": 118, "fighter_a": 179, "fighter_b": 3810, "weight_class": "light_heavyweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": null, "analysisComplete": false}, {"id": 1312, "event": 118, "fighter_a": 3558, "fighter_b": 2316, "weight_class": "featherweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": null, "analysisComplete": false}, {"id": 1313, "event": 118, "fighter_a": 434, "fighter_b": 3874, "weight_class": "heavyweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": null, "analysisComplete": false}]};

const standardColumns = ['matchup','weightclass','rounds'];
const watchListColumns = ['matchup','weightclass','rounds','analysis complete']
/*
    query api here
*/
const watchlist = ref([]);
const mainCard = ref(null);
const prelims = ref(null);

onMounted(() => {
    console.log("MainContent mounted");
    // fetch('/vue-next-event')
    //     .then(response => response.json())
    //     .then(data => {
    //         watchlist.value = data;
    //         console.log("Watchlist data fetched:", watchlist.value);
    //     })
    //     .catch(error => {
    //         console.error("Error fetching watchlist data:", error);
    // });
})

</script>
<template>
    <!--
        responsive container of content
    -->
    <div class="container-fluid">
        <!--
            contains 3 tables
            watchlist table
            maincard table
            prelims table
        -->
        <div class="title-container">
            <h3>
                {{ sampleFetchResult.event.title }}
            </h3>
        </div>
        
        <template v-if="watchlist.length != 0">
            <Table  table-name="WatchList" :columns=watchListColumns></Table>
        </template>
        <template v-else>
            <div class="empty-watchlist-notification border border-2 rounded-2 px-2 py-1">
                <h4>No matchups in watchlist.</h4>
            </div>
        </template>

        <Table class="mt-2" table-name="MainCard" :columns=standardColumns :matchups="sampleFetchResult.mainCardMatchups"></Table>
        <Table class="mt-2" table-name="Prelims" :columns=standardColumns :matchups="sampleFetchResult.prelimMatchups"></Table>
    </div>
</template>

<style scoped lang="scss">
    .empty-watchlist-notification{
        width: fit-content;
    }

</style>
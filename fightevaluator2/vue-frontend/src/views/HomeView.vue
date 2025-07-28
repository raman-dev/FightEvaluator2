<script setup>

import { onMounted, ref, Transition,inject } from 'vue';
import Table from '@/components/Table.vue';
import MatchUpEditor from '@/components/MatchUpEditor.vue';

const sampleFetchResult = {"event": {"id": 118, "title": "UFC Fight Night: Whittaker vs. de Ridder", "date": "2025-07-26", "location": null, "link": "https://www.tapology.com/fightcenter/events/125931-ufc-fight-night", "hasResults": false}, "mainCardMatchups": [{"id": 1302, "event": 118, "fighter_a": 3507, "fighter_b": 3854, "weight_class": "middleweight", "rounds": 5, "isprelim": false, "outcome": null, "inWatchList": true, "analysisComplete": false, "fighter_a_name": "Robert Whittaker", "fighter_b_name": "Reinier De ridder"}, {"id": 1303, "event": 118, "fighter_a": 3569, "fighter_b": 3639, "weight_class": "bantamweight", "rounds": 3, "isprelim": false, "outcome": null, "inWatchList": true, "analysisComplete": false, "fighter_a_name": "Petr Yan", "fighter_b_name": "Marcus Mcghee"}, {"id": 1304, "event": 118, "fighter_a": 1922, "fighter_b": 236, "weight_class": "middleweight", "rounds": 3, "isprelim": false, "outcome": null, "inWatchList": true, "analysisComplete": false, "fighter_a_name": "Shara Magomedov", "fighter_b_name": "Marc-andre Barriault"}, {"id": 1305, "event": 118, "fighter_a": 3776, "fighter_b": 3797, "weight_class": "flyweight", "rounds": 3, "isprelim": false, "outcome": null, "inWatchList": true, "analysisComplete": false, "fighter_a_name": "Asu Almabayev", "fighter_b_name": "Jose Ochoa"}, {"id": 1306, "event": 118, "fighter_a": 1715, "fighter_b": 1270, "weight_class": "light_heavyweight", "rounds": 3, "isprelim": false, "outcome": null, "inWatchList": null, "analysisComplete": false, "fighter_a_name": "Nikita Krylov", "fighter_b_name": "Bogdan Guskov"}], "prelimMatchups": [{"id": 1307, "event": 118, "fighter_a": 2148, "fighter_b": 3777, "weight_class": "bantamweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": true, "analysisComplete": false, "fighter_a_name": "Bryce Mitchell", "fighter_b_name": "Said Nurmagomedov"}, {"id": 1308, "event": 118, "fighter_a": 2846, "fighter_b": 3779, "weight_class": "welterweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": true, "analysisComplete": false, "fighter_a_name": "Muslim Salikhov", "fighter_b_name": "Carlos Leal"}, {"id": 1309, "event": 118, "fighter_a": 320, "fighter_b": 1226, "weight_class": "bantamweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": true, "analysisComplete": false, "fighter_a_name": "Da'mon Blackshear", "fighter_b_name": "Davey Grant"}, {"id": 1310, "event": 118, "fighter_a": 2699, "fighter_b": 2706, "weight_class": "strawweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": null, "analysisComplete": false, "fighter_a_name": "Amanda Ribas", "fighter_b_name": "Tabatha Ricci"}, {"id": 1311, "event": 118, "fighter_a": 179, "fighter_b": 3810, "weight_class": "light_heavyweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": null, "analysisComplete": false, "fighter_a_name": "Ibo Aslan", "fighter_b_name": "Billy Elekana"}, {"id": 1312, "event": 118, "fighter_a": 3558, "fighter_b": 2316, "weight_class": "featherweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": null, "analysisComplete": false, "fighter_a_name": "Mohammad Yahya", "fighter_b_name": "Steven Nguyen"}, {"id": 1313, "event": 118, "fighter_a": 434, "fighter_b": 3874, "weight_class": "heavyweight", "rounds": 3, "isprelim": true, "outcome": null, "inWatchList": null, "analysisComplete": false, "fighter_a_name": "Martin Buday", "fighter_b_name": "Marcus Buchecha"}]};
const fetchResult = ref(null);
const standardColumns = ['matchup','weightclass','rounds'];
const watchListColumns = ['matchup','weightclass','rounds','analysis complete']
/*
    query api here
*/
const watchlist = ref(null);
const mainCardMatchups = ref(null);
const prelimMatchups = ref(null);

const matchUpEditorOpen = ref(false);

// const pluginFunc = inject('pluginFunc');

onMounted(() => {
    // pluginFunc();
    console.log("MainContent mounted");
    fetch('/vue-next-event')
        .then(response => response.json())
        .then(data => {
            fetchResult.value = data;

            console.log("Matchups data fetched:", fetchResult.value.mainCardMatchups);
            mainCardMatchups.value = fetchResult.value.mainCardMatchups;
            prelimMatchups.value = fetchResult.value.prelimMatchups;
            watchlist.value = [];
            for (const m of mainCardMatchups.value){
                if (m.inWatchList){
                    watchlist.value.push(m);
                }
            }
            for (const m of prelimMatchups.value){
                if (m.inWatchList){
                    watchlist.value.push(m);
                }
            }
        })
        .catch(error => {
            console.error("Error fetching data:", error);
    });
    // mainCardMatchups.value = sampleFetchResult.mainCardMatchups;
    // prelimMatchups.value = sampleFetchResult.prelimMatchups;
    // watchlist.value = [];
    // for (const m of mainCardMatchups.value){
    //     if (m.inWatchList){
    //         watchlist.value.push(m);
    //     }
    // }
    // for (const m of prelimMatchups.value){
    //     if (m.inWatchList){
    //         watchlist.value.push(m);
    //     }
    // }
    // console.log("Watchlist:", watchlist.value);
})

function showMatchupEditor(emptyEditor){
    matchUpEditorOpen.value = true;
}

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
        
        <template v-if="watchlist != null">
            <Table  table-name="WatchList" :columns=watchListColumns :matchups="watchlist"></Table>
        </template>
        <template v-else>
            <div class="empty-watchlist-notification border border-2 rounded-2 px-2 py-1">
                <h4>No matchups in watchlist.</h4>
            </div>
        </template>

        <Table class="mt-2" table-name="MainCard" :columns=standardColumns :matchups="mainCardMatchups" @request-new-match-up="showMatchupEditor(true)"></Table>
        <Table class="mt-2" table-name="Prelims" :columns=standardColumns :matchups="prelimMatchups" @request-new-match-up="showMatchupEditor(true)"></Table>
        
        <MatchUpEditor v-model:open="matchUpEditorOpen"></MatchUpEditor>
        
        <!--

            accept components hold their own state
            entirely different paradigm to normal html and bootstrap

            transition wraps an element 
            and is triggered when element is rendered or not rendered

            transition will trigger named animations
                v-enter-from   -> before animation start
                    v-enter-active -> animating
                v-enter-to -> after animation
                      
                v-leave from -> before animation start
                    v-leave-active -> animatiing
                v-leave to -> after animating
            
            use name attribute for animations

            Transition name="animName"

            class -> 
                animName-enter-from
                animName-enter-active...
        -->

    </div>
</template>

<style scoped lang="scss">
    .empty-watchlist-notification{
        width: fit-content;
    }

</style>
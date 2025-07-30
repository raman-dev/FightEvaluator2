<script setup>

import { onMounted, ref } from 'vue';
import { useMatchupStore } from '@/stores/matchupStore.js';
import Table from '@/components/matchup-tables/Table.vue';
import MatchUpEditor from '@/components/matchup-tables/MatchUpEditor.vue';
import { storeToRefs } from 'pinia';

const standardColumns = ['matchup', 'weightclass', 'rounds'];
const watchListColumns = ['matchup', 'weightclass', 'rounds', 'analysis complete']
/*
    query api here
*/
const matchUpEditorOpen = ref(false);

const matchupStore = useMatchupStore();
const { event,mainCard,prelims,watchlist } = storeToRefs(matchupStore);

onMounted(() => {
    // console.log("MainContent mounted");
    matchupStore.fetchEvent();
})

function showMatchupEditor(emptyEditor) {
    matchUpEditorOpen.value = true;
}

</script>
<template>
    <div class="container-fluid">
        <div class="title-container">
            <h3>
                {{ event.title }}
            </h3>
        </div>

        <template v-if="watchlist">
            <Table table-name="WatchList" :columns=watchListColumns :matchups="watchlist"></Table>
        </template>
        <template v-else>
            <div class="empty-watchlist-notification border border-2 rounded-2 px-2 py-1">
                <h4>No matchups in watchlist.</h4>
            </div>
        </template>

        <Table class="mt-2" table-name="MainCard" :columns=standardColumns :matchups="mainCard"
            @request-new-match-up="showMatchupEditor(true)"></Table>
        <Table class="mt-2" table-name="Prelims" :columns=standardColumns :matchups="prelims"
            @request-new-match-up="showMatchupEditor(true)"></Table>

        <MatchUpEditor v-model:open="matchUpEditorOpen"></MatchUpEditor>

    </div>
</template>

<style scoped lang="scss">
.empty-watchlist-notification {
    width: fit-content;
}
</style>
<!--
**NOTE**
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
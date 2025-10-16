<script setup>

import { ref, watch } from 'vue';
import { useMatchupStore } from '@/stores/matchupStore.js';
import Table from '@/components/matchup-tables/Table.vue';
import MatchUpEditor from '@/components/matchup-tables/MatchUpEditor/MatchUpEditor.vue';
import MatchUpActionMenu from '@/components/matchup-tables/MatchUpActionMenu.vue';
import { storeToRefs } from 'pinia';
import { useMatchupActionMenuStore } from '@/stores/matchupActionMenuStore';
import { onBeforeRouteLeave, onBeforeRouteUpdate, useRoute  } from 'vue-router';
import TapologyButton from '@/components/TapologyButton.vue';
import { useMatchupDetailStore } from '@/stores/matchupDetailStore';


// const router = useRouter();
const route = useRoute();

const standardColumns = ['matchup', 'weightclass', 'rounds'];
const watchListColumns = ['matchup', 'weightclass', 'rounds', 'analysis complete']
/*
    query api here
*/
const matchUpEditorOpen = ref(false);
const inEditMode = ref(false);

const matchupStore = useMatchupStore();
const matchupActionMenuStore = useMatchupActionMenuStore();
const matchupDetailStore = useMatchupDetailStore();

const { event, mainCard, prelims, watchlist } = storeToRefs(matchupStore);
const { menuPosition,menuOpen } = storeToRefs(matchupActionMenuStore)


watch(route, (newData, oldData) => {
    // react to route changes...
    console.log(newData.params, oldData);
    if ('eventId' in newData.params) {
        //load id specific event data
        matchupStore.fetchEvent(newData.params.eventId);
    } else {
        matchupStore.fetchEvent();//normal next event
    }
}, { immediate: true });


onBeforeRouteLeave((to,from) => {
    console.log('HomeView.onBeforeRouteLeave',to.fullPath,from.fullPath);
    menuOpen.value = false;//close incase open
    
    console.log ('HomeView.onBeforeRouteLeave.to.params',to.params);
    console.log('HomeView.onBeforeRouteLeave.to',to);
    if (to.name === 'analyze'){
        console.log('analyze yo',to.params.matchupId);
        matchupDetailStore.fetchMatchupDetails(to.params.matchupId);
    }
});


function showMatchupEditor(emptyEditor) {
    matchUpEditorOpen.value = true;
}

function onClickEdit(){
    inEditMode.value = true;
    showMatchupEditor();
    menuOpen.value = false;
}

function closeEditor(){
    matchUpEditorOpen.value = false;
    inEditMode.value = false;
}

</script>
<template>

    <div class="container-fluid main-container" @mousemove="showGuides">
        <div class="title-container d-flex justify-content-between">
            <h3>
                {{ event.title }}
            </h3>
            
            <TapologyButton :link="event.link"></TapologyButton>
        </div>

        <div class="tables-wrapper">
            <template v-if="Object.keys(watchlist).length > 0">
                <Table table-name="WatchList" :columns=watchListColumns :matchups="watchlist"></Table>
            </template>
            <template v-else>
                <div class="d-flex empty-watchlist-notification border rounded-2 px-2 py-1 justify-content-start">
                    <h6>No matchups in watchlist.</h6>
                </div>
            </template>
            
            <div class="table-grid">
                <Table table-name="MainCard" :columns=standardColumns :matchups="mainCard"
                    @request-new-match-up="showMatchupEditor(true)"></Table>
                <Table table-name="Prelims" :columns=standardColumns :matchups="prelims"
                    @request-new-match-up="showMatchupEditor(true)"></Table>
            </div>
        </div>

        <MatchUpEditor v-model:open="matchUpEditorOpen" v-model:inEditMode="inEditMode" @editor-close="closeEditor"></MatchUpEditor>
        <MatchUpActionMenu v-model:menu-position="menuPosition" @edit-matchup="onClickEdit"></MatchUpActionMenu>
    </div>

</template>

<style scoped lang="scss">

.empty-watchlist-notification{
    border: 1px solid lavender !important;
    border-radius: 0.4rem;
    width: fit-content;
    padding: 0.4rem;

    margin-left: 0px;
    margin-right: auto;

    * {
        margin: 0px;
    }
}

.tables-wrapper, .title-container{
  margin: auto;
  max-width: 57%;  
}

.title-container{
  margin:auto;
  width: 100%;
//   margin-top: 1rem !important;
  margin-bottom: 1rem !important;
  padding: 0rem;
}

.tables-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;

    .table-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        width: 100%;

        table {
            width: 100%;
        }
    }
}

@media (max-width: 924px) {
  .table-grid{
        grid-template-columns: 1fr !important;
    } 
}

@media (max-width: 1280px) {
    .tables-wrapper, .title-container{
      max-width: 85%;
    }
}

@media (max-width: 1024px) {
  .tables-wrapper, .title-container{
    max-width: 100%;
  }
}

@media (max-width: 768px) {
  .tables-wrapper, .title-container{
      max-width: 100%;
   }
}

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
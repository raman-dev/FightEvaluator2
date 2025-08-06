<script setup>

import { onMounted, ref, useTemplateRef, watch } from 'vue';
import { useMatchupStore } from '@/stores/matchupStore.js';
import Table from '@/components/matchup-tables/Table.vue';
import MatchUpEditor from '@/components/matchup-tables/MatchUpEditor.vue';
import MatchUpActionMenu from '@/components/matchup-tables/MatchUpActionMenu.vue';
import { storeToRefs } from 'pinia';
import { useMatchupActionMenuStore } from '@/stores/matchupActionMenuStore';
import { useRouter,useRoute } from 'vue-router';


// const router = useRouter();
const route = useRoute();

const standardColumns = ['matchup', 'weightclass', 'rounds'];
const watchListColumns = ['matchup', 'weightclass', 'rounds', 'analysis complete']
/*
    query api here
*/
const matchUpEditorOpen = ref(false);

const matchupStore = useMatchupStore();
const matchupActionMenuStore = useMatchupActionMenuStore();

const { event,mainCard,prelims,watchlist } = storeToRefs(matchupStore);
const { menuPosition } = storeToRefs(matchupActionMenuStore)

const guideXRef = useTemplateRef('guideX');
const guideYRef = useTemplateRef('guideY');

const cursorX = ref(0);
const cursorY = ref(0);

const showingGuides = ref(false);

onMounted(() => {
    matchupStore.fetchEvent();
})

watch(route, (newId, oldId) => {
    // react to route changes...
    console.log (newId,oldId);
},{deep:true});

function showMatchupEditor(emptyEditor) {
    matchUpEditorOpen.value = true;
}

function showGuides(event){
    
    if (showingGuides.value === false){
        return;
    }
    event.stopPropagation();
    const guideX = guideXRef.value;
    const guideY = guideYRef.value;

    guideX.style.top = `${event.pageY}px`;
    guideY.style.left = `${event.pageX}px`;

    // console.log(event.pageX,event.pageY);
    /*
        viewport is the visible portion of the document to the user
    */
   cursorX.value = event.pageX;
   cursorY.value = event.pageY;
}

</script>
<template>
    <!-- <div class="mx-auto d-flex align-items-center">
        <input id="guideCheckbox" type="checkbox" @input="showingGuides=!showingGuides" name="guides"/>
        <label class="mx-1" for="guideCheckbox">Guides</label>
        <p class="p-0 m-0">{{ cursorX }}, {{ cursorY }}</p>
    </div> -->
    <div class="container-fluid main-container" @mousemove="showGuides">
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

        <Table table-name="MainCard" :columns=standardColumns :matchups="mainCard"
            @request-new-match-up="showMatchupEditor(true)"></Table>
        <Table table-name="Prelims" :columns=standardColumns :matchups="prelims"
            @request-new-match-up="showMatchupEditor(true)"></Table>

        <MatchUpEditor v-model:open="matchUpEditorOpen"></MatchUpEditor>
        <MatchUpActionMenu v-model:menu-position="menuPosition"></MatchUpActionMenu>
    </div>
    <!--horizontal line guide moves up and down-->
    <!-- <div class="guide-x" ref="guideX" v-if="showingGuides"></div> -->
    <!--vertical line guide moves left and right-->
    <!-- <div class="guide-y" ref="guideY" v-if="showingGuides"></div> -->
</template>

<style scoped lang="scss">

.guide-x{
    position: absolute;
    width: 100%;
    height: 1px;
    background-color: cyan;
}

.guide-y{
    position: absolute;
    height: 100%;
    width: 1px;
    background-color: red;
}


.main-container{
    // position: relative;
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
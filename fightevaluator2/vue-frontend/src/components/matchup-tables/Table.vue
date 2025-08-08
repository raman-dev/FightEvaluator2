<script setup>

import { useTemplateRef, watch } from 'vue';
import TableRow from './TableRow.vue';
import { useMatchupStore } from '@/stores/matchupStore';
import { storeToRefs } from 'pinia';
import { useMatchupActionMenuStore } from '@/stores/matchupActionMenuStore';


const props = defineProps(['tableName', 'columns', 'matchups']);
const tableContainerRef = useTemplateRef('tableContainer');

const emits = defineEmits(['requestNewMatchUp']);

function showMatchUpEditor() {
    emits('requestNewMatchUp');
}

const matchupStore = useMatchupStore();
const { toggleActiveMatchUp } = matchupStore;
const { activeMatchup } = storeToRefs(matchupStore);
const { menuOpen, menuPosition,menuLimitRect } = storeToRefs(useMatchupActionMenuStore());


watch(activeMatchup, (newVal, oldVal) => {
    //if oldVal is not null means the active matchup
    //that the action menu was open on is no longer active so the menu is
    //no longer valid to be shown
    if (oldVal != null) {
        console.log('close menu!');
        menuOpen.value = false;
    }
}, { deep: true });//deep is necessary if you don't a

function toggleActive(matchupId) {
    toggleActiveMatchUp(matchupId, props.tableName);
}

function onRightClickRow(event) {
    event.preventDefault();
    const currActive = activeMatchup.value.matchup;
    if (currActive == null) return;
    if (activeMatchup.value.table != props.tableName) return;
    //show right click 
    setMenuPosition(event);
}

function setMenuPosition(event) {
    const tableContainer = tableContainerRef.value;
    let rect = tableContainer.getBoundingClientRect(); // Get element's position and size

    let tablePageX = rect.left + window.scrollX;
    let tablePageY = rect.top + window.scrollY;

    let pageX = event.pageX;
    let pageY = event.pageY;

    let relX = pageX - tablePageX;
    let relY = pageY - tablePageY;

    let pctX = relX / rect.width;
    let pctY = relY / rect.height;

    let x = parseInt(pageX);
    let y = parseInt(pageY);

    menuOpen.value = true;
    //position the thing
    menuPosition.value.x = x;
    menuPosition.value.y = y;
    menuPosition.value.tablePctX = pctX;
    menuPosition.value.tablePctY = pctY;
    menuLimitRect.value = rect;
}

</script>
<template>
    <div class="table-container mt-2" ref="tableContainer" :class="{'w-100':props.tableName ==='WatchList'}">
        <table>
            <caption style="caption-side:top">
                <div class="d-flex justify-content-between">
                    <h4 style="text-transform: capitalize;">{{ props.tableName }}</h4>
                    <div class="action-wrapper">
                        <button type="button" class="btn btn-primary" v-if="props.tableName !== 'WatchList'"
                            @click="showMatchUpEditor()">
                            add
                        </button>
                    </div>
                </div>
            </caption>
            <thead>
                <tr>
                    <template v-for="col in columns">
                        <th>{{ col }}</th>
                    </template>
                </tr>
            </thead>
            <tbody>

                <template v-for="(matchup, matchupId) in props.matchups" :key="matchupId">
                    <TableRow v-model:matchup="props.matchups[matchupId]" :table-name="props.tableName"
                        @click="toggleActive(matchupId)" @contextmenu="onRightClickRow"></TableRow>
                </template>

            </tbody>
        </table>
    </div>

</template>

<style lang="scss">
.table-container {
    position: relative;
}

.table-container table {
    width: 100%;
    transition: all 0.3s ease-out;
    background-color: #111519 !important;

    thead {
        border: 1px solid lavender;
        text-transform: capitalize;
    }

    ;

    tbody {
        border: 1px solid lavender;
    }

    th, td {
        text-align: center;
        vertical-align: middle;
        padding: 0.4rem;
        padding-left: 0.8rem;
        padding-right: 0.8rem;
    }

    td {
        p {
            margin: 0px;
        }
    }
}
</style>
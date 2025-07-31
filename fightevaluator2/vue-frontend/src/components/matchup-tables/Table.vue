<script setup>

import TableRow from './TableRow.vue';
import MatchUpActionMenu from './MatchUpActionMenu.vue';
import { useMatchupStore } from '@/stores/matchupStore';


const props = defineProps(['tableName', 'columns', 'matchups']);
const emits = defineEmits(['requestNewMatchUp'])

function showMatchUpEditor() {
    emits('requestNewMatchUp');
}

const { toggleActiveMatchUp } = useMatchupStore();

function toggleActive(matchupId) {
    toggleActiveMatchUp(matchupId, props.tableName);
}

</script>
<template>
    <div class="table-container border">
        <table class>
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
                        @click="toggleActive(matchupId)"></TableRow>
                </template>

            </tbody>
        </table>
    </div>
    <!--
        on right click table row
            show a menu with options
             - watch/unwatch
             - analyze
             - edit
             - delete

            on click watch
                add to watchlist 
                    update matchup on server
            on click analyze 
                open analysis page
            on click edit
                open editor with matchup data instead of empty editor
            on click delete
                show confirmation dialog
    -->

    <!-- <MatchUpActionMenu v-model:open="actionMenuOpen"></MatchUpActionMenu> -->
</template>

<style lang="scss" >
    .table-container table{
        width: 100%;
        transition: all 0.3s ease-out;
        background-color: #111519 !important;
        thead{
            border: 1px solid lavender;
            text-transform: capitalize;
        };
        tbody{
            border: 1px solid lavender;
        }
        th, td{
            text-align: center;
            vertical-align: middle;
            padding: 0.4rem;
            padding-left: 0.8rem;
            padding-right: 0.8rem;
        } 
        td{
            p{
                margin: 0px;
            }
        }
    }
</style>
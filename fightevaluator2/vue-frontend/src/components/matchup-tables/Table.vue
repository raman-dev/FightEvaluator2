<script setup>
    
import TableRow from './TableRow.vue';
import MatchUpActionMenu from './MatchUpActionMenu.vue';

const props = defineProps(['tableName','columns','matchups']);
const emits = defineEmits(['requestNewMatchUp'])

function showMatchUpEditor(){
    emits('requestNewMatchUp');
}

</script>
<template>
    <div class="table-container border">
        <table class="table table-striped table-hover">
            <caption style="caption-side:top">
                <div class="d-flex justify-content-between">
                  <h4 style="text-transform: capitalize;">{{props.tableName}}</h4>
                  <div class="action-wrapper">
                    <button type="button" class="btn btn-primary" v-if="props.tableName !== 'WatchList'" @click="showMatchUpEditor()">
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

                <template v-for="(matchup,i) in props.matchups" :key="i">
                    <TableRow v-model:matchup="props.matchups[i]" :table-name="props.tableName" @click=""></TableRow>
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

<style lang="scss" scoped>
    tr {
        cursor: pointer;
    }
</style>
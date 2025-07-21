<script setup>

import { ref } from 'vue';
import Table from './Table.vue';


const standardColumns = ['matchup','weightclass','rounds'];
const watchListColumns = ['matchup','weightclass','rounds','analysis complete']
/*
    query api here
*/
const watchlist = ref([]);

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
        <template v-if="watchlist.length != 0">
            <Table  table-name="WatchList" :columns=watchListColumns></Table>
        </template>
        <template v-else>
            <div class="empty-watchlist-notification border border-2 rounded-2 px-2 py-1">
                <h4>No matchups in watchlist.</h4>
            </div>
        </template>

        <Table class="mt-2" table-name="MainCard" :columns=standardColumns></Table>
        <Table class="mt-2" table-name="Prelims" :columns=standardColumns></Table>
    </div>
</template>

<style scoped lang="scss">
    .empty-watchlist-notification{
        width: fit-content;
    }

</style>
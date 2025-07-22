<script setup>
    
const props = defineProps(['tableName','columns','matchups']);

</script>
<template>
    <div class="table-container border">
        <table class="table">
            <caption style="caption-side:top">
                <div class="d-flex justify-content-between">
                  <h4 style="text-transform: capitalize;">{{props.tableName}}</h4>
                  <div class="action-wrapper">
                    <button type="button" class="btn btn-primary">
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
                <tr v-for="matchup in props.matchups" :key="matchup.id">
                    <td>{{ matchup.fighter_a }} vs {{ matchup.fighter_b }}</td>
                    <td>{{ matchup.weight_class }}</td>
                    <td>{{ matchup.rounds }}</td>
                    <td v-if="props.tableName === 'WatchList'">{{ matchup.analysisComplete ? 'Yes' : 'No' }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>
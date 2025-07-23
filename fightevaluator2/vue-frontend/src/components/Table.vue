<script setup>
    
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
                <tr v-for="matchup in props.matchups" :key="matchup.id">
                    <td>{{ matchup.fighter_a_name }} vs {{ matchup.fighter_b_name }}</td>
                    <td>{{ matchup.weight_class }}</td>
                    <td>{{ matchup.rounds }}</td>
                    <td v-if="props.tableName === 'WatchList'">{{ matchup.analysisComplete ? 'Yes' : 'No' }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>
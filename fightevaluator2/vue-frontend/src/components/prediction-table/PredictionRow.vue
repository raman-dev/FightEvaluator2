<script setup>
import PredictionCell from './PredictionCell.vue';


const props = defineProps({ matchupData: { type: Object, default: {} } })
</script>
<template>
    <tr>
        <th>
            {{ matchupData.title }}
        </th>
        <!--
                        for every type in eventType
                        check data if type is in data
                         if it is then render td with value
                            else render td with 0
                    -->
        <!---
                        first render fighter win likelihoods
                        then render non win events 

                        data is a dict

                        matchup
                            title
                            likelihoods    
                                event_type
                                    likelihood
                                    justification
                                event_type.WIN
                                    [
                                        fighter_a 
                                            likelihood
                                            justifcation
                                        fighter_b
                                            likelihood
                                            justification
                                    ]
                    -->
        <template v-for="value, key in matchupData.likelihoods">
            <template v-if="key === 'WIN'">
                <PredictionCell :event-type="key" :fighter-name="value[0].fighter_a.name" :likelihood="value[0].likelihood" :justification="value[0].justification"></PredictionCell>
                <PredictionCell :event-type="key" :fighter-name="value[1].fighter_b.name"  :likelihood="value[1].likelihood" :justification="value[1].justification"></PredictionCell>
            </template>
            <template v-else>
                <PredictionCell :likelihood="value.likelihood" :justification="value.justification"></PredictionCell>
            </template>
        </template>
    </tr>
</template>

<style scoped lang="scss">
tr:hover{
    cursor: pointer;
}
</style>
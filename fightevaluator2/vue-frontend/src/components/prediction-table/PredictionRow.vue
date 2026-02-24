<script setup>
import PredictionCell from './PredictionCell.vue';
import { ref } from 'vue';

const props = defineProps({ matchupData: { type: Object, default: {} } })

const expandRow = ref(false);

const expandedOnClick = ref(false);
const expandTimer = ref (null);
const ON_HOVER_EXPAND_DELAY = 500; // Delay in milliseconds before expanding on hover

function toggleRow() {
    console.log("toggleRow: ",expandRow.value,!expandRow.value);
    if (expandedOnClick.value == false && expandRow.value == true) {
        // If the row is currently expanded due to hover and the user clicks, we want to keep it expanded but mark it as expanded due to click
        expandedOnClick.value = true;
        return; // Exit the function to prevent toggling the state again
        
    }
    expandedOnClick.value = !expandedOnClick.value;
    expandRow.value = !expandRow.value;
    
}

function mouseEnterRow() {
    console.log("mouseEnterRow: ",expandRow.value);
    if (!expandRow.value && !expandedOnClick.value) {
        expandTimer.value = setTimeout(() => {
            expandRow.value = true;
        }, ON_HOVER_EXPAND_DELAY); // Adjust the delay as needed
    }
}

function mouseLeaveRow() {
    console.log("mouseLeaveRow: ",expandRow.value);
    if (!expandedOnClick.value && (expandTimer.value !== null || expandTimer.value !== undefined)) {
        clearTimeout(expandTimer.value);
        expandTimer.value = null;
        
        expandRow.value = false; // Collapse the row immediately only if it was expanded due to hover
    }
}

</script>
<template>
    <tr @click="toggleRow" @mouseenter="mouseEnterRow" @mouseleave="mouseLeaveRow" :class="{'row-expanded-click':expandedOnClick}">
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
                <PredictionCell :show-justification="expandRow" :event-type="key" :fighter-name="value[0].fighter_a.name" :likelihood="value[0].likelihood" :justification="value[0].justification"></PredictionCell>
                <PredictionCell :show-justification="expandRow" :event-type="key" :fighter-name="value[1].fighter_b.name"  :likelihood="value[1].likelihood" :justification="value[1].justification"></PredictionCell>
            </template>
            <template v-else>
                <PredictionCell :show-justification="expandRow" :likelihood="value.likelihood" :justification="value.justification"></PredictionCell>
            </template>
        </template>
    </tr>
</template>

<style scoped lang="scss">
tr:hover{
    cursor: pointer;
}

tr.row-expanded-click{
    outline: 2px solid slateblue;
}
</style>
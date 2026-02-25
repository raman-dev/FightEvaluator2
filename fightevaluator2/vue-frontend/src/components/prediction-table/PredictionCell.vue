<script setup>
import { inject } from 'vue';
const props = defineProps({
    eventType: {default:"",type: String},
    fighterName: {default:"",type: String},
    likelihood: {default: 0,type: Number},
    justification: {default:"",type:String},
    showJustification: {default: false, type: Boolean}
});

function sliceIfNecessary(s) {
    if (s.charAt(0) === '-'){
        return s.slice(1);
    }
    return s;
}

const likelihoodLabelMap = inject('likelihoodLabelMap');
</script>
<template>
    <td>
        <div class="likelihood-wrapper mb-1">
            <div class="likelihood mx-auto" :class="{['likely-'.concat(likelihood)]:true,'likelihood-win':eventType==='WIN'}">{{ likelihoodLabelMap[likelihood] }}</div>
            <div class="fighter-name" v-if="eventType === 'WIN'">
                {{ fighterName }}
            </div>
        </div>
        
        <div class="justification" :class="{'d-none':showJustification == false}">{{ sliceIfNecessary(justification) }}</div>
    </td>
</template>
<style lang="scss" scoped>
td {
    max-width: 20ch;
    padding: 0.3rem !important;
}

$likelihoodBorderRadius: 0.2rem;
$likelihoodPadding: 0.2rem;

.likelihood-wrapper{
    max-width: 20ch;
    text-align: center;
    margin: auto;
}

.likelihood{
    color: black;
    border-radius: $likelihoodBorderRadius;
    padding: $likelihoodPadding;
    text-transform: capitalize;
    font-family: PoppinsSemiBold;

    max-width: 20ch;
}

.likelihood-win{
    border-bottom-right-radius: 0px;
    border-bottom-left-radius: 0px;
}

.fighter-name{
    text-align: center;
    background-color: black;
    padding-bottom: $likelihoodPadding;
    
    border-bottom-right-radius: $likelihoodBorderRadius;
    border-bottom-left-radius: $likelihoodBorderRadius;
    border-top: none;
}

.justification{
    text-transform: capitalize;
}
</style>
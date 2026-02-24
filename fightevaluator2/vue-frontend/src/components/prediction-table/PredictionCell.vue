<script setup>
import { inject } from 'vue';
const props = defineProps({
    eventType: {default:"",type: String},
    fighterName: {default:"",type: String},
    likelihood: {default: 0,type: Number},
    justification: {default:"",type:String},
    showJustification: {default: false, type: Boolean}
});

const likelihoodLabelMap = inject('likelihoodLabelMap');
</script>
<template>
    <td>
        
        <div class="likelihood mx-auto" :class="'likely-' + likelihood">{{ likelihoodLabelMap[likelihood] }}</div>
        <div class="fighter-name" v-if="eventType === 'WIN'">
            {{ fighterName }}
        </div>
        <div class="justification" :class="{'d-none':showJustification == false}">{{ justification.slice(1) }}</div>
    </td>
</template>
<style lang="scss" scoped>
td {
    max-width: 20ch;
}
.likelihood{
    color: black;
    border-radius: .3rem;
    padding: .2rem;
    text-align: center;
    text-transform: capitalize;
    font-family: PoppinsSemiBold;

    max-width: 20ch;
}
.fighter-name{
    text-align: center;
}

.justification{
    text-transform: capitalize;
}
</style>
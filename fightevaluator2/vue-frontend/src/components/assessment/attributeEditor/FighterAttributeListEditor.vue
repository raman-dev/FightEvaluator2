<script setup>
import { useAssessmentStore } from '@/stores/assessmentStore';
import { onMounted } from 'vue';
import { storeToRefs } from 'pinia';

import AttributeCard from './AttributeCard.vue';


const { assessment } = storeToRefs(useAssessmentStore());

onMounted(() => {
    console.log('FighterAttributeListEditor.onMounted -> ');
});
</script>

<template>
    <div class=".fighter-attrib-list">
        <template v-for="value, key in assessment">
            <AttributeCard v-if="key !== 'id' && key != 'fighter'" v-model:attributeValue="assessment[key]"
                :attrib_name="key">
            </AttributeCard>
        </template>
    </div>

</template>

<style>
.fighter-attrib-list {
    padding: 0.5rem;
}
</style>
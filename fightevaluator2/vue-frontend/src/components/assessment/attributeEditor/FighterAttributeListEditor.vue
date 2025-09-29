<script setup>
import { useAssessmentStore } from '@/stores/assessmentStore';
import { onMounted } from 'vue';
import { storeToRefs } from 'pinia';

import AttributeCard from './AttributeCard.vue';

const emit = defineEmits(["attributeChange"]);
const { assessment } = storeToRefs(useAssessmentStore());

</script>

<template>
    <div class="fighter-attrib-list">
        <template v-for="value, key in assessment">
            <AttributeCard v-if="key !== 'id' && key != 'fighter'" v-model:attributeValue="assessment[key]"
                :attrib_name="key"
                @attributeChange="$emit('attributeChange',$event)"
                >
            </AttributeCard>
        </template>
    </div>

</template>

<style scoped lang="scss">
.fighter-attrib-list {
    padding: 0.5rem;
    width: 100%;
}
</style>
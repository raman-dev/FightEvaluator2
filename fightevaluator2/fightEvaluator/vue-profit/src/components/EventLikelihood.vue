<script setup>
import { ref, useTemplateRef, watch } from 'vue';


const props = defineProps(['likelihood', 'likelihood_val', 'justification', 'fighter', 'type']);
const expanded = defineModel();

const container = useTemplateRef('container');

watch(expanded, async (newExpandedVal,oldExpandedVal) => {
    if (newExpandedVal == true){
        //expand the container the scrollHeight
        const scrollHeight = container.value.scrollHeight;
        container.value.style.height=`${scrollHeight}px`;
        // container.value.style.opacity=1;
    }else{
        container.value.style.height=`0px`;
        // container.value.style.opacity=0;
    }
});


</script>

<template>
    <div class="likelihood" :class="['likely-' + props.likelihood_val]">
        <span>{{ props.likelihood }}</span>
        <p class="bg-dark m-0 justification" ref="container">
            {{ props.justification }}
        </p>
    </div>
</template>

<style lang="scss" scoped>
:hover{
    cursor: pointer;
}
.justification {
    overflow: hidden;
    height: 0px;
    // opacity: 0;
    transition: height 0.3s, opacity 0.3s ease-out;
}

</style>
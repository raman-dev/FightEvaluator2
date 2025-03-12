<script setup>
import { ref, useTemplateRef, watch } from 'vue';


const props = defineProps(['likelihood', 'likelihood_val', 'justification', 'fighter', 'type']);
const expanded = defineModel();
const emits = defineEmits(['height-change']);

const container = useTemplateRef('container');


watch(expanded, async (newExpandedVal,oldExpandedVal) => {
    // console.log(marginY);
    const oldHeight = container.value.style.height;
    if (newExpandedVal == true){
        //expand the container the scrollHeight
        const newHeight = container.value.scrollHeight;
        container.value.style.height=`${newHeight}px`;
        // container.value.style.opacity=1;
        emits('height-change',newHeight);//the new height to add
    }else{
        const oldScrollHeight = container.value.scrollHeight;
        container.value.style.height=`${0}px`;
        // container.value.style.opacity=0;
        emits('height-change',-oldScrollHeight);
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
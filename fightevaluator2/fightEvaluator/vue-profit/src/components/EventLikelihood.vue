<script setup>

const props = defineProps(['likelihood', 'likelihood_val', 'justification', 'fighter','type']);

</script>

<template>
    <div class="border">
        <div :class="['likelihood','likely-' + props.likelihood_val]">
        <span>{{ props.likelihood }}</span>
        </div>
        <p class="justification bg-dark">
            {{ props.justification }}
        </p>
    </div>
    
</template>

<style lang="scss" scoped>
    .likelihood span{
        text-transform: capitalize;
    }
    .justification {
        overflow: hidden;
        height: 0px;
    }
    
</style>
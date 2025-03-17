<script setup>
import MatchUpEvents from './MatchUpEvents.vue';


const props  = defineProps(['line']);

</script>
<template>
    <div class="line border flex-wrap">
        <template v-for="(value,key) in props.line">
            <MatchUpEvents :matchup_id="key" :eventMap="value" :title="value.title"/>
        </template>
    </div>
</template>

<style scoped lang="scss">
    .line {
        height: fit-content;
        width: fit-content;
        
        display: flex;
        padding: 0.8rem !important;

        border-color: #151616 !important;
        border-width: 2px !important;
    }
</style>
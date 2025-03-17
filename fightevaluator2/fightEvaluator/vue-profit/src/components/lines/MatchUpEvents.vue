<script setup>
import EventNode from './EventNode.vue';

const props = defineProps(['matchup_id','eventMap','title']);

</script>

<template>
    <div class="matchup p-2">
        <h6 class="title m-0">{{ props.title }}</h6>
        <div class="event-wrapper d-flex">
            <!--contain event nodes -->
            <template v-for="(eventData,type) in props.eventMap">
                <EventNode v-bind="eventData" :type="type" v-if="type != 'count' && type != 'title'"/>
            </template>
        </div>
    </div>
    
</template>
<style scoped>
    .matchup {
        margin: 0.4rem;
        border-radius: 0.4rem !important;
        background-color: #151616;
    }
</style>
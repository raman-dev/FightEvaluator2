<script setup>

import { ref } from 'vue';
import EventLikelihood from './EventLikelihood.vue';

const props = defineProps(['matchup_id', 'events', 'title']);
const expanded = ref(false);

function expandClick() {
    expanded.value = !expanded.value;
}

</script>

<template>

    <tr>
        <td>
            <div class="matchup-wrapper">
                <a href="/matchup/1091">
                    {{ props.title }}
                </a>
                <button class="expand-toggle btn btn-outline-info" @click="expandClick()">expand</button>
            </div>
        </td>

        <template v-for="(event, type) in props.events" :key="type">
            <td>
                <div class="d-flex justify-content-evenly align-items-start" v-if="type == 'win'">
                    <EventLikelihood v-bind="event[0]" :type="type" v-model="expanded" />
                    <EventLikelihood v-bind="event[1]" :type="type" v-model="expanded" />
                </div>
                <div v-else>
                    <EventLikelihood v-bind="event" v-model="expanded" />
                </div>
            </td>
        </template>
    </tr>

</template>

<style lang="scss" scoped>
.matchup-wrapper {
    display: flex;
    justify-content: space-between;
    align-items: center;

    a {
        color: white;
        text-decoration: none;
        white-space: nowrap;
    }

    a:hover {
        text-decoration: underline;
    }

    button{
        margin-left: 0.6rem;
    }
}
</style>
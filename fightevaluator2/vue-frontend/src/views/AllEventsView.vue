<script setup>
import { useEventsStore } from '@/stores/eventsStore';
import { storeToRefs } from 'pinia';
import { onMounted } from 'vue';


const eventStore = useEventsStore();
const { fetchEvents } = eventStore
const { events } = storeToRefs(eventStore);

onMounted(() => {
    fetchEvents();
})

</script>
<template>
    <div class="main-container container-fluid">
        <div class="mx-auto content-container col-xxl-6 col-xl-9 col-lg-10 col-md-12 col-12">
            <h1>Events</h1>
            <template v-for="(monthDict, year) in events.events_yearMonth" :key="year">
                <h3>{{ year }}</h3>
                <div class="month-container m-2 my-4" v-for="(events, month) in monthDict">
                    <template v-if="events.length > 0">
                        <h4 class="date-title">{{ month }}</h4>
                        <div class="events-container p-2">
                            <div class="rounded-3 event-item" v-for="event in events">
                                <a href="/{{event.id}}">
                                    <h6 class="py-3 p-1 m-0 text-center">
                                        {{ event.title }}
                                    </h6>
                                </a>
                            </div>
                        </div>
                    </template>
                </div>
            </template>
        </div>
    </div>
</template>

<style scoped lang="scss">

$event-item-color: #111519;

.event-container{
    .date-title{
        margin: auto;
    }
}

ul.event-list{
    list-style-type: none;
    padding: 0.4rem;
    margin: 0;
    background-color: #111519 !important;

    li {
        padding: 0px;
        outline: 2px solid transparent;
        outline-offset: 2px;

        a{
            text-decoration: none;
            color: lavender;
        }
    }
    li:hover{
        outline-color: whitesmoke;
        a{
            text-decoration: underline;
        }
    }
}

.events-container{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.4rem;
    row-gap: 0.6rem;

    border: 2px solid #131b23;

    .event-item{
        background-color: $event-item-color;
        transition: background-color 0.1s ease; 
        a{
            text-decoration: none;
            color: whitesmoke;
        }
    }

    .event-item:hover{
        // background-color: hsl(175, 61.57%, 24.95%);
        background-color: hsl(200, 56%, 12%);
        cursor: pointer;
        outline-color: whitesmoke;
        a{
            text-decoration: underline;
        }
    }
}

</style>
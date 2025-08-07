<script setup>
import { useEventsStore } from '@/stores/eventsStore';
import { storeToRefs } from 'pinia';
import { onMounted } from 'vue';
import { RouterLink } from 'vue-router';


const eventStore = useEventsStore();
const { fetchEvents } = eventStore
const { eventsData } = storeToRefs(eventStore);

onMounted(() => {
    fetchEvents();
})

function monthNumberToString(monthInput) {
  const months = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];

  // Convert input to integer
  const monthNumber = parseInt(monthInput, 10);

  // Validate range
  if (isNaN(monthNumber) || monthNumber < 1 || monthNumber > 12) {
    return "Invalid month";
  }

  return months[monthNumber - 1];
}

</script>
<template>
    <div class="main-container container-fluid">
        <div class="mx-auto content-container col-xxl-6 col-xl-9 col-lg-10 col-md-12 col-12">
            <h1>Events</h1>
            <template v-for="(data,index) in eventsData.events" :key="index">
                <h3>{{ data.year }}</h3>
                <div class="month-container m-2 my-4" v-for="(monthEvents, monthIndex) in data.months" :key="monthIndex">
                    <template v-if="monthEvents.events.length > 0">
                        <h4 class="date-title">{{ monthNumberToString(monthEvents.month) }}</h4>
                        <div class="events-container p-2">
                            <div class="rounded-3 event-item" v-for="event in monthEvents.events" :key="event.id">
                                <RouterLink :to="{ name:'event-specific', params: {eventId:event.id }}">
                                    <h6 class="py-3 p-1 m-0 text-center">
                                        {{ event.title }}
                                    </h6>
                                </RouterLink>
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
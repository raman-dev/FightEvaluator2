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

function percentToColor(percentStr) {
  let value = parseFloat(percentStr.replace('%', ''));
  if (isNaN(value)) throw new Error("Invalid percentage string");

  // Clamp between 0 and 100
  value = Math.max(0, Math.min(100, value));

  // Color steps
  const steps = [
    "red",    // 0–50
    "orange", // 51–60
    "yellow", // 61–70
    "limegreen", // 71–80
    "lime",   // 81–90
    "green"   // 91–100
  ];

  if (value <= 50) return steps[0];

  // Divide 50–100 into 5 ranges
  let stepIndex = Math.min(
    steps.length - 1,
    Math.floor((value - 50) / 10) + 1
  );

  return steps[stepIndex];
}



</script>
<template>
    <div class="main-container container-fluid">
        <div class="mx-auto content-container col-xxl-6 col-xl-9 col-lg-10 col-md-12 col-12">
            <h1>Events</h1>
            <div class="nav nav-pills" id="yearTabs" role="tablist">
                <template v-for="(data, index) in eventsData.events" :key="index">
                    <button class="nav-link" 
                            :class="{'active':index == 0}" 
                            :id="'nav-'+data.year+'-tab'" 
                            data-bs-toggle="tab" 
                            :data-bs-target="'#'+data.year+'-tab-pane'" 
                            type="button" 
                            role="tab" 
                            :aria-controls="'nav-' +data.year" aria-selected="true">
                            <h5 class="m-0">{{ data.year }}</h5>
                            
                        </button>
                </template>
            </div>
            <div class="tab-content" id="myTabContent">
                
                <div class="tab-pane fade" 
                    :class="{active:index == 0, show:index == 0}"
                    :id="data.year+'-tab-pane'"
                    role="tabpanel"
                    :tabindex="index"

                    v-for="(data, index) in eventsData.events" :key="index">
                    <!-- <h3>{{ data.year }}</h3> -->
                    <div class="month-container m-2 my-4 p-1" v-for="(monthEvents, monthIndex) in data.months"
                        :key="monthIndex">
                        <template v-if="monthEvents.events.length > 0">
                            <div class="month-header d-flex align-items-center justify-content-between">
                                <h4 class="date-title">{{ monthNumberToString(monthEvents.month) }}</h4>
                                <div class="monthly-stats-container d-flex"
                                    v-if="Object.keys(monthEvents.monthlyStats).length > 0">
                                        <div class="stat" :style="{'color':'black','background-color':percentToColor(monthEvents.monthlyStats.accuracy)}" v-if="monthEvents.monthlyStats.events > 0">
                                            <strong>{{ monthEvents.monthlyStats.accuracy }} Accurracy</strong>
                                        </div>
                                        <div class="stat">
                                            {{ monthEvents.monthlyStats.correct }} Correct
                                        </div>
                                        <div class="stat">
                                            {{ monthEvents.monthlyStats.predictions }} Predictions
                                        </div>
                                    <div class="stat">
                                        {{ monthEvents.monthlyStats.events }} Events
                                    </div>
                                </div>
                            </div>
                            <div class="events-container p-2">
                                <div class="rounded-3 event-item" v-for="event in monthEvents.events" :key="event.id">
                                    <RouterLink :to="{ name: 'event-specific', params: { eventId: event.id } }">
                                        <h6 class="py-3 p-1 m-0 text-center">
                                            {{ event.title }}
                                        </h6>
                                    </RouterLink>
                                </div>
                            </div>
                        </template>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped lang="scss">
$event-item-color: #111519;

@mixin dark-border {
    border: 2px solid #131b23;
}

#yearTabs{
    button {
        text-decoration: none;
        color: whitesmoke;
    }
}
.event-container {
    .date-title {
        margin: auto;
    }
}

.month-container {
    @include dark-border();
    border-radius: 0.4rem;
    border-width: 3px;
}

.monthly-stats-container {
    .stat {
        background-color: $event-item-color;
        border-radius: 0.4rem;

        margin: 0.6rem;

        padding: 0.3rem;
        padding-left: 0.6rem;
        padding-right: 0.6rem;

        width: fit-content;
        text-transform: capitalize;
    }
}

ul.event-list {
    list-style-type: none;
    padding: 0.4rem;
    margin: 0;
    background-color: #111519 !important;

    li {
        padding: 0px;
        outline: 2px solid transparent;
        outline-offset: 2px;

        a {
            text-decoration: none;
            color: lavender;
        }
    }

    li:hover {
        outline-color: whitesmoke;

        a {
            text-decoration: underline;
        }
    }
}

.events-container {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.4rem;
    row-gap: 0.6rem;

    // @include dark-border();

    .event-item {
        background-color: $event-item-color;
        transition: background-color 0.1s ease;

        a {
            text-decoration: none;
            color: whitesmoke;
        }
    }

    .event-item:hover {
        // background-color: hsl(175, 61.57%, 24.95%);
        background-color: hsl(200, 56%, 12%);
        cursor: pointer;
        outline-color: whitesmoke;

        a {
            text-decoration: underline;
        }
    }
}

@media (max-width: 768px){

    .month-header{
        flex-direction: column;
    }

    .monthly-stats-container{
        display: grid !important;
        grid-template-columns: 1fr 1fr;
    }

    .events-container{
        grid-template-columns: 1fr;
    }
}
</style>
import { defineStore } from "pinia";
import { inject, ref } from "vue";

export const usePredictionsStore = defineStore('predictionsStore', () => {
    const server = inject('server');
    // const predictions = ref({});

    const eventPredictions = ref([]);
    const eventPredictionsByYearMonth = ref({});
    const stats = ref({});

    function onReceivePredictions(data) {
        console.log("Received predictions:", data.predictions);
        eventPredictionsByYearMonth.value = groupPredictionsByYearMonth(data);
        eventPredictions.value = data.predictions;
        console.log ("Grouped predictions by year/month:", eventPredictionsByYearMonth.value);
    }

    function onReceiveStats(data) {
        console.log("Received stats:", data);
        for (const [key, value] of Object.entries(data)) {
            stats.value[key] = value;
        }
    }

    async function getPredictions() {
        server.get_predictions(onReceivePredictions);
    }

    async function getStats() {
        server.get_stats(onReceiveStats);
    }

    function groupPredictionsByYearMonth(data) {
        const grouped = {};

        for (const entry of data.predictions) {
            const dateStr = entry.event.date; // "2025-10-18"
            const [year, month] = dateStr.split('-'); // ["2025", "10"]

            // Initialize year if missing
            if (!grouped[year]) grouped[year] = {};

            // Initialize month if missing
            if (!grouped[year][month]) grouped[year][month] = [];

            // Add entry
            grouped[year][month].push(entry);
        }

        return grouped;
    }

    return {
        // predictions,
        eventPredictions,
        eventPredictionsByYearMonth,
        stats,
        getStats,
        getPredictions
    }
});
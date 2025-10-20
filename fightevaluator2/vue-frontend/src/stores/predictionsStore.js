import { defineStore } from "pinia";
import { inject, ref } from "vue";

export const usePredictionsStore = defineStore('predictionsStore', () => {
    const server = inject('server');
    // const predictions = ref({});

    const eventPredictions = ref([]);
    const stats = ref({});

    function onReceivePredictions(data) {
        console.log ("Received predictions:", data.predictions);
        eventPredictions.value = data.predictions;
    }

    function onReceiveStats(data) {
        console.log ("Received stats:", data);
        for (const [key, value] of Object.entries(data)) {
            stats.value[key] = value; 
        }
    }

    async function getPredictions() {
        server.get_predictions(onReceivePredictions);
    }

    async function getStats(){
        server.get_stats(onReceiveStats);
    }

    return { 
        // predictions,
        eventPredictions,
        stats, 
        getStats,
        getPredictions 
    }
});
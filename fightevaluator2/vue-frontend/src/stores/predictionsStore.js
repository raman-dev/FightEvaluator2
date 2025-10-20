import { defineStore } from "pinia";
import { inject, ref } from "vue";

export const usePredictionsStore = defineStore('predictionsStore', () => {
    const server = inject('server');
    // const predictions = ref({});

    const eventPredictions = ref([]);
    const stats = ref({
        general: [
            { count: 10, total: 15, ratio_percent: "66%" }
        ],
        fight_outcome: [
            { label: "ko", count: 5, total: 8, ratio_percent: "62%" }
        ]
    });

    function onReceivePredictions(data) {
        console.log ("Received predictions:", data.predictions);
        eventPredictions.value = data.predictions;
    }

    function onReceiveStats(data) {
        console.log ("Received stats:", data.stats);
        for (const [key, value] of Object.entries(data.stats)) {
            stats.value[key] = value;
        }
    }

    function getPredictions() {
        server.get_predictions(onReceivePredictions);
    }

    function getStats(){
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
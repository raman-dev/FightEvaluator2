import { defineStore } from "pinia";
import { inject, ref } from "vue";

export const usePredictionStore = defineStore('predictionStore',() => {
    const server = inject('server');
    const predictions = ref({});

    function onReceivePredictions(data) {
        predictions.value = data.predictions;
    }

    function getPredictions() {
        server.get_predictions(onReceivePredictions);
    }
    
    return { predictions, getPredictions }
});
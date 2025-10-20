<script setup>
defineProps({
    eventPredictions: {
        type: Object,
        required: true
    }
});

const resultClass = (isCorrect) => {
    if (isCorrect === true) return "data-correct";
    if (isCorrect === false) return "data-incorrect";
    return "data-tbd";
};

const resultText = (isCorrect) => {
    if (isCorrect === null || isCorrect === undefined) return "tbd";
    return isCorrect ? "True" : "False";
};
</script>

<template>
    <div v-for="(predictions, eventIndex) in eventPredictions" :key="eventIndex" class="prediction-table row flex-column">
        <div
            class="mx-auto event-name col col-sm-12 col-md-10 col-lg-9 col-xl-7 col-xxl-6 d-flex justify-content-between">
            <p class="m-0">{{ predictions.event.date }}</p>
            <p class="m-0 text-end">{{ predictions.event.title }}</p>
        </div>

        <ul class="mx-auto my-0 px-2 col col-sm-12 col-md-10 col-lg-9 col-xl-7 col-xxl-6">
            <li>
                <div class="table-header row" data-key-count="0">
                    <div class="col col-4 column-label">
                        <p>MatchUp</p>
                    </div>
                    <div class="col col-4 column-label">
                        <p>Prediction</p>
                    </div>
                    <div class="col col-1 column-label">
                        <p>Result</p>
                    </div>
                    <div class="col col-3 column-label">
                        <p>Likelihood</p>
                    </div>
                </div>
            </li>

            <li v-for="(data, index) in predictions.items" :key="index" tabindex="index" class="data-row my-2"
                :data-prediction="data.prediction.predictionDisplay" :data-result="data.isCorrect"
                :data-likelihood="data.prediction.likelihood" :data-event="data.matchup.event.title">
                <div class="row">
                    <div class="col col-4 d-flex align-items-center">{{ data.matchup.title }}</div>
                    <div class="col col-4 d-flex align-items-center">{{ data.prediction.predictionDisplay }}</div>
                    <div class="col col-1 data-result d-flex align-items-center">
                        <p class="mx-auto" :class="resultClass(data.isCorrect)">
                            {{ resultText(data.isCorrect) }}
                        </p>
                    </div>
                    <div class="col col-3 d-flex align-items-center justify-content-end likelihood">
                        <p class="confidence" :class="'likely-' + data.prediction.likelihood">
                            very likely
                        </p>
                    </div>
                </div>
            </li>
        </ul>

        <div v-if="!predictions.event.hasResults"
            class="fetch-results-wrapper mx-auto d-flex align-items-center justify-content-end col col-sm-12 col-md-10 col-lg-9 col-xl-7 col-xxl-6">
            <p class="m-0">Results Available!</p>
            <button class="m-0 btn btn-primary">Fetch</button>
        </div>
    </div>
</template>

<style scoped lang="scss">
.likely-5 {
    background-color: #dc3545;
}

.likely-4 {
    background-color: #ed7b26;
}

.likely-3 {
    background-color: #ffc107;
}

.likely-2 {
    background-color: #80ff00;
}

.likely-1 {
    background-color: #00ff00;
}

.likely-0 {
    background-color: #52565A;
}

.prediction-table {
    ul {
        background-color: #12161A;
    }

    margin-bottom: 1rem;
}

.confidence {
    min-width: fit-content;
    border-radius: 0.2rem;
    padding: 0.3rem;
    text-align: center;
    text-transform: capitalize;
    font-family: PoppinsSemiBold;
    color: black;
    margin: 0px;
}

ul {
    padding: 0px;
    padding-bottom: 0.8rem;
    list-style: none;

    li {
        margin: 0.2rem;
        padding: 0.4rem
    }

    li.data-row {
        border: 1px solid lavender;
        border-radius: 0.4rem;

        .col {
            text-transform: capitalize;
        }
    }

    .data-result {
        p {
            font-family: PoppinsSemiBold;
            border-radius: 0.2rem;
            margin: 0px;

            width: 6ch;
            text-align: center;
            color: black;
        }

        p.data-correct {
            background-color: #00ff00;
        }

        p.data-incorrect {
            background-color: #dc3545;
        }

        p.data-tbd {
            background-color: slategrey;
        }
    }

    .column-label {
        padding: 0.2rem;
        display: flex;

        p {
            margin: 0px;
        }

        justify-content: center;
        align-items: center;

        .icon {
            color: #313539; //set fill="currentColor"
        }
    }


    .column-label:hover {
        cursor: pointer;
        background-color: #414549;
    }

    .column-label.sort-by {
        background-color: #111519;

        .icon {
            color: #818589; //set fill="currentColor"
        }
    }

    .column-label[data-sort="dec"] {

        //flip icon upside down
        .icon {
            transform: rotateZ(180deg);
        }
    }
}
</style>

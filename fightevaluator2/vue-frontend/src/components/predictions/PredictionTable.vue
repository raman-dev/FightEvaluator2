<script setup>

import { inject,onMounted,ref } from 'vue';
const props = defineProps({
    eventPredictions: {
        type: Object,
        required: true
    },

    eventPredictionsByYearMonth: {
        required: true,
        type: Object
    }
});

const minYear = ref(9999);
const maxYear = ref(-9999);

const abbreviatedDateFormat = inject('abbreviatedDateFormat');

const resultClass = (isCorrect) => {
    if (isCorrect === true) return "data-correct";
    if (isCorrect === false) return "data-incorrect";
    return "data-tbd";
};

const resultText = (isCorrect) => {
    if (isCorrect === null || isCorrect === undefined) return "tbd";
    return isCorrect ? "True" : "False";
};

const likelihoodLabelMap = inject('likelihoodLabelMap');

function toOrderedKeyList(object) {
    const result = [];
    for (const key of Object.keys(object)) {
        result.push(key)
    }
    result.sort((a,b) => {
        return b - a;
    })
    return result;
}


onMounted(()=>{
    
    for (const year in props.eventPredictionsByYearMonth) {
        // const element = props.eventPredictionsByYearMonth[year];
        minYear.value = Math.min(minYear.value,parseInt(year));
        maxYear.value = Math.max(maxYear.value,parseInt(year));
    }
    console.log(minYear.value,maxYear.value);
    
});
</script>

<template>
    <div class="wrapper">

        <div class="nav nav-pills border" id="yearTabs" role="tablist">
            <template v-for="(year, index) in toOrderedKeyList(eventPredictionsByYearMonth)" :key="index">
                <button class="nav-link" :class="{ 'active': index == 0 }" :id="'nav-' + year + '-tab'"
                    data-bs-toggle="tab" :data-bs-target="'#' + year + '-tab-pane'" type="button" role="tab"
                    :aria-controls="'nav-' + year" aria-selected="true">
                    <h5 class="m-0">{{ year }}</h5>
                </button>
            </template>
        </div>
        <div class="tab-content" id="myTabContent">
            <div class="tab-pane fade" 
                :class="{ active: index === 0, show: index === 0 }" 
                :id="year + '-tab-pane'" :tabindex="index" role="tabpanel" 
                v-for="(monthMap, year, index) in eventPredictionsByYearMonth" :key="index">
                <!--
                    year:
                        monthNum:
                            event_0
                            event_1
                    
                            need to order the data on your own
                -->
                <div class="border" v-for="(monthNum, mindex) in toOrderedKeyList(monthMap)" :key="mindex">
                    
                    <div v-for="(data, eventIndex) in monthMap[monthNum]" :key="monthNum"
                        class="prediction-table row flex-column">
                        <div
                            class="mx-auto event-name col col-sm-12 col-md-10 col-lg-9 col-xl-7 col-xxl-6 d-flex justify-content-between">
                            <p class="m-0">{{ abbreviatedDateFormat(data.event.date) }}</p>
                            <p class="m-0 text-end">{{ data.event.title }}</p>
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

                            <li v-for="(prediction, index) in data.predictions" :key="index" tabindex="index"
                                class="data-row my-2" :data-prediction="prediction.type"
                                :data-result="prediction.isCorrect" :data-likelihood="prediction.likelihood"
                                :data-event="prediction.matchup">
                                <div class="row">
                                    <div class="col col-4 d-flex align-items-center">{{ prediction.matchup }}</div>
                                    <div class="col col-4 d-flex align-items-center">{{ prediction.type_label }}</div>
                                    <div class="col col-1 data-result d-flex align-items-center">
                                        <p class="mx-auto" :class="resultClass(prediction.correct)">
                                            {{ resultText(prediction.correct) }}
                                        </p>
                                    </div>
                                    <div class="col col-3 d-flex align-items-center justify-content-end likelihood">
                                        <p class="confidence" :class="'likely-' + prediction.likelihood">
                                            {{ likelihoodLabelMap[prediction.likelihood] }}
                                        </p>
                                    </div>
                                </div>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>

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

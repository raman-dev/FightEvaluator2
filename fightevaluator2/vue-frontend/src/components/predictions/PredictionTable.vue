<script setup>

import { inject, onMounted, ref } from 'vue';
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

const abbreviatedDateFormat = inject('abbreviatedDateFormat');
const numToMonthName = inject('numToMonthName');
const isMobile = ref(false);

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
    result.sort((a, b) => {
        return b - a;
    })
    return result;
}

</script>

<template>
    <div class="wrapper d-flex flex-column mx-auto col col-md-12 col-lg-10 col-xl-8 col-xxl-6 align-items-center">
        <div class="d-flex w-100 nav nav-pills" id="yearTabs" role="tablist">
            <template v-for="(year, index) in toOrderedKeyList(eventPredictionsByYearMonth)" :key="index">
                <button class="nav-link" :class="{ 'active': index == 0 }" :id="'nav-' + year + '-tab'"
                    data-bs-toggle="tab" :data-bs-target="'#' + year + '-tab-pane'" type="button" role="tab"
                    :aria-controls="'nav-' + year" aria-selected="true">
                    <h5 class="m-0">{{ year }}</h5>
                </button>
            </template>
        </div>
        <div class="tab-content d-flex w-100 px-2" id="myTabContent">
            <div class="tab-pane fade w-100" :class="{ active: index === Object.keys(eventPredictionsByYearMonth).length - 1, show: index === Object.keys(eventPredictionsByYearMonth).length - 1 }"
                :id="year + '-tab-pane'" :tabindex="index" role="tabpanel"
                v-for="(monthMap, year, index) in eventPredictionsByYearMonth" :key="index">
                <!--
                    year:
                        monthNum:
                            event_0
                            event_1
                    
                            need to order the data on your own
                -->
                <div class="tables-container border mb-4" v-for="(monthNum, mindex) in toOrderedKeyList(monthMap)" :key="mindex">
                    <h3 class="">{{ numToMonthName(monthNum) }}</h3>
                    <div class="prediction-table row flex-column" v-for="(data, eventIndex) in monthMap[monthNum]" :key="monthNum" >
                        <table>
                            <thead>
                                <tr >
                                    <td><span>matchup</span></td>
                                    <td><span>prediction</span></td>
                                    <td><span>result</span></td>
                                    <td>
                                        <div class="d-flex justify-content-end">
                                            <span>likelihood</span>
                                        </div>
                                    </td>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(prediction, index) in data.predictions">
                                    <td><span>{{ prediction.matchup }}</span></td>
                                    <td><span>{{ prediction.type_label }}</span></td>
                                    <td><span class="data-result" :class="resultClass(prediction.correct)">{{resultText(prediction.correct) }}</span></td>
                                    <td>
                                        <div class="d-flex w-100 justify-content-end">
                                            <span class="likelihood" :class="'likely-' + prediction.likelihood">
                                                {{ likelihoodLabelMap[prediction.likelihood] }}
                                            </span>
                                        </div>
                                    </td>
                                </tr>
                            </tbody>
                            <caption>
                                <div class="d-flex w-100 justify-content-between px-1">
                                    <p class="m-0">{{ abbreviatedDateFormat(data.event.date) }}</p>
                                    <p class="m-0 text-end">{{ data.event.title }}</p>
                                </div>

                            </caption>
                        </table>
                    </div>
                </div>
            </div>

        </div>

    </div>
</template>

<style scoped lang="scss">
// $body-bg-dark: #00ff00;
.nav-link {
    color: white !important;
}
.prediction-table{
    background-color: #12161A !important;
    padding-bottom: 0.6rem;
    table {
        
        font-size: 0.95rem;
        text-transform: capitalize;
        border-collapse: separate;
        border-spacing: 0rem 0.4rem;
        td {
            padding:0.6rem;
        }

        caption {
            caption-side: top;
            color: lavender;
        }

        tbody {
            padding-bottom: 0.6rem;
            tr td:first-child{
                // border-top: 1px solid lavender;
                // border-left: 1px solid lavender;
                border: 1px solid lavender;
                border-top-left-radius: 0.5rem;
                border-bottom-left-radius: 0.5rem;
                border-right: none;
            }
            tr td:last-child{
                border: 1px solid lavender;
                border-top-right-radius: 0.5rem;
                border-bottom-right-radius: 0.5rem;
                border-left: none;
            }

            tr td{
                border-top: 1px solid lavender;
                border-bottom: 1px solid lavender;
            }
            .data-result,.likelihood {
                font-family: PoppinsSemiBold;
                border-radius: 0.2rem;

                text-align: center;
                color: black;
            }

            .likelihood{
                padding-left: 1ch;
                padding-right: 1ch;
            }

            .data-result{
                display: block;
                width: 6ch !important;
            }

            .data-correct {
                background-color: #00ff00;
            }

            .data-incorrect {
                background-color: #dc3545;
            }

            .data-tbd {
                background-color: slategrey;
            }
        }
    }
}

.prediction-content {
    display: flex;
    flex-direction: column;
}

@media (min-width: 576px) {}

// Medium devices (tablets, 768px and up)
@media (min-width: 768px) {
    .prediction-content {
        flex-direction: row !important;
    }
}

// Large devices (desktops, 992px and up)
@media (min-width: 992px) {}

// X-Large devices (large desktops, 1200px and up)
@media (min-width: 1200px) {}

// XX-Large devices (larger desktops, 1400px and up)
@media (min-width: 1400px) {}



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

    margin-top: 1.6rem;
    margin-bottom: 1.6rem;
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


</style>

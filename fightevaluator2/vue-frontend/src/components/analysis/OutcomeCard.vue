<script setup>
import { ref } from "vue";
import ConfidenceSelector from "./ConfidenceSelector.vue";
import { useMatchupDetailStore } from "@/stores/matchupDetailStore";

const props = defineProps({
    event: { type: String, required: true }, // { name, label }
    fighter: { type: Object, required: false },
    matchup: { type: Object, required: true },
    label : {type: String, required: false}
});

const emit = defineEmits(["update:likelihood", "update:justification"]);

const likelihood = ref(3);
const selectorLikelihood = ref(3);
const showConfidenceList = ref(false);

const justification = ref("Justification Statements and Conclusions");
const changed = ref(false);

const matchupDetailStore = useMatchupDetailStore();


function onChangeLikelihood(val) {
    // console.log('val,likelihood.val',val,likelihood.value);
    changed.value = likelihood.value !== val;
}

function updateJustification(e) {
    justification.value = e.target.innerText;
}

function updateOutcomePrediction() {
    if (changed.value === true){
        //send changes to server
        //grab data from child component how to do that
        const data = {
            event:props.event,
            likelihood:selectorLikelihood.value,
            justification: justification.value
        }
        if (data.event === 'WIN'){
            data.fighter = props.fighter.id;
        }
        matchupDetailStore.updateOutcomePrediction(data);
        changed.value = false;
        showConfidenceList.value = false;   
    }
}

</script>

<template>
    <div class="outcome-card event-card col-12 col-sm-6 col-md-5 col-lg-4 col-xl-3 col-xxl-2">
        <div class="outcome event" :data-event-type="event" data-id="0"
            :data-likelihood="likelihood">
            <div class="wrapper">
                <h6 v-if="event === 'WIN'">Win</h6>
                <h6 v-else>Yes</h6>
            </div>

            <button @click="updateOutcomePrediction" class="save-outcome-btn save-event-likelihood-btn btn btn-primary" :class="{disabled: changed === false}">
                save
            </button>

            <p>
                <template v-if="event === 'WIN'">
                    <span>
                        {{ fighter.last_name }} Wins
                    </span>
                </template>
                <template v-else>
                    {{ label }}
                </template>
            </p>

            <!-- Confidence Selector -->
            <ConfidenceSelector 
                v-model:server-likelihood="likelihood" 
                v-model:selector-likelihood="selectorLikelihood" 
                @update-likelihood="onChangeLikelihood" 
                v-model:show-confidence-list="showConfidenceList"
                />

            <!-- Justification -->
            <div class="justification">
                <div class="title-wrapper">
                    <h5>Justification</h5>
                    <button class="btn show-justification-btn w-0"></button>
                </div>
                <div class="justification-container">
                    <div class="editor-wrapper">
                        <div class="editor" contenteditable="plaintext-only" @input="updateJustification">
                            {{ justification }}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped lang="scss">
.outcome-card {
    background-color: #12161A;
    border-radius: 0.8rem;
    padding-bottom: 0.8rem;
    padding-top: 0.8rem;
    height: fit-content;

    .outcome {
        display: flex;
        flex-direction: column;

        padding: 0.2rem;
        position: relative;

        .save-outcome-btn {
            position: absolute;
            right: 0px;
        }

        .wrapper {
            margin: auto;
            width: 4rem;
            height: 4rem;

            display: flex;
            align-items: center;
            justify-content: center;

            border: 1px solid lavender;
            border-radius: 99rem;

            outline: 3px solid transparent;
            outline-offset: 1px;

            h6 {
                text-transform: capitalize;
                width: fit-content;
                text-align: center;
                margin: 0px;
            }

        }

        p {
            border-radius: 0.5rem;

            margin: 0px;
            margin-top: 1rem;

            text-align: center;
            text-transform: capitalize;
        }
    }

}


.justification {
    margin-top: 0.4rem;
    padding: 0.3rem;

    .title-wrapper {
        display: flex;
        align-items: center;
        justify-content: space-between;
    }

    .justification-container {
        margin-top: 0.4rem;

        .editor-wrapper {
            border: 1px solid lavender;
            border-radius: 0.4rem;
            // height: auto;
            overflow: hidden;
            transition: all 0.3s ease-in-out;

            .editor {
                margin: 0px;
                padding: 0.3rem;
                width: 100%;
                text-transform: capitalize;
                text-align: left;
                // max-width: 32ch;
                word-break: break-word;
                min-height: 4rem;
            }
        }
    }
}
</style>

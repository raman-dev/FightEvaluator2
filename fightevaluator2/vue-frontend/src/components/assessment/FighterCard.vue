<script setup>
import TapologyButton from "../TapologyButton.vue";
import { watch,inject } from "vue";

// fighter comes from v-model
const fighter = defineModel("fighter", { type: Object, required: true });
const nextMatchup = defineModel("nextMatchup", { type: Object, required: false });
//

const emit = defineEmits(['editClick']);
// nextMatchup is still a one-way prop
const props = defineProps({

    fullSize: {
        type: Boolean,
        default: true,
    },
    rtlImage: {
        type: Boolean,
        default: false
    }
});

// helpers
const removeScores = inject('replaceUnderscoreSpace');
const inchesToFeetStr = inject('inchesToFeetStr');

const formatHeight = (val) => {
    if (!val) return "N/A";
    return inchesToFeetStr(val);
};

const dobToAge = inject('dobToAge');

watch(nextMatchup, (newVal,oldVal) => {
    console.log("FighterCard.nextMatchup:", newVal);
});


</script>

<template>
    <div class="fighter-info-container">
        <div class="fighter-card" :class="{ rtlImage: props.rtlImage }">
            <div class="img-wrapper">
                <img class="fighter-image" :src="fighter.img_link ? fighter.img_link : '/static/fightEvaluator/media/sample_150.png'" alt="fighter image">
                <div class="next-matchup d-flex" v-if="props.fullSize">
                    <template v-if="nextMatchup">
                        <RouterLink class="text-center" :to="{ name: 'analyze', params: { matchupId: nextMatchup.id } }">
                            <p class="m-0">
                                {{ nextMatchup.title }}
                            </p>
                        </RouterLink>
                    </template>
                    <template v-else>
                        <a href="#">no upcoming matchup</a>
                    </template>
                </div>
            </div>

            <div class="content-wrapper">
                <div class="card-content">
                    <div class="card-header">
                        <h3 class="fighter-name">
                            <span id="first_name">{{ fighter.first_name }}</span>&nbsp;
                            <span id="last_name">{{ fighter.last_name }}</span>&nbsp;
                        </h3>
                        <div class="info-wrapper">
                            <p class="fighter-weight" id="weight_class">
                                {{ removeScores(fighter.weight_class) }}
                            </p>
                        </div>
                    </div>

                    <div class="card-body">
                        <div class="info-wrapper">
                            <h6>height:&nbsp;</h6>
                            <p class="fighter-height">{{ formatHeight(fighter.height) }}</p>
                        </div>

                        <div class="info-wrapper">
                            <h6>age:&nbsp;</h6>
                            <p class="fighter-age">{{ dobToAge(fighter.date_of_birth) }}</p>
                        </div>

                        <div class="info-wrapper">
                            <h6>record:&nbsp;</h6>
                            <p class="fighter-record">
                                <span>{{ fighter.wins }}-{{ fighter.losses }}-{{ fighter.draws }}</span>
                            </p>
                        </div>

                        <div class="info-wrapper">
                            <h6>reach:&nbsp;</h6>
                            <p class="fighter-reach" id="reach">{{ fighter.reach }}</p>
                        </div>

                        <div class="info-wrapper" v-if="props.fullSize">
                            <h6>stance:&nbsp;</h6>
                            <p class="fighter-stance" id="stance">{{ fighter.stance }}</p>
                        </div>

                        <div class="info-wrapper" v-if="props.fullSize">
                            <TapologyButton :link="fighter.data_api_link"></TapologyButton>
                        </div>
                    </div>
                </div>

                <div class="button-container" v-if="props.fullSize">
                    <button class="bio-edit-button btn btn-outline-light" @click="$emit('editClick')">
                        edit
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>



<style scoped lang="scss">
$backgroundColor: #212529;
// $cardColor: #242a34;
$cardBorderColor: #131b23;
$cardColor: #12161A;

$btnBorderColor: black;
$btnBorderRadius: 0.6rem;
$borderRadius: 0.5rem;

@mixin button-active {
    box-shadow: black 2px 2px 0 0;
    // background-color: $btnClickBackground;
}

.fighter-info-container {
    margin-bottom: 1rem;

    .img-link {
        margin-top: 0.5rem;
        margin-bottom: 0.5rem;
        opacity: 0;
    }
}

.fighter-card[data-edit-mode-enabled="true"] {
    .bio-edit-button {
        @include button-active;
    }
}

.rtlImage {
    flex-direction: row-reverse;
}

.fighter-card {
    display: flex;
    align-items: center;
    border-radius: $borderRadius;
    border: 2px solid $cardBorderColor;
    padding: 1rem;

    .img-wrapper {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        font-size: 0.85rem;

        margin-left: 0.6rem;
        margin-right: 0.6rem;
    }

    .img-wrapper .next-matchup {
        margin-top: 0.4rem;
        padding: 0.2rem;
        padding-left: 0.4rem;
        padding-right: 0.4rem;

        border-radius: 99rem;
        border: 2px solid lavender;

        a {
            margin: 0px;
            text-decoration: none;
            color: whitesmoke;
        }
    }

    .img-wrapper .fighter-image {
        clip-path: inset(0% 0% round 0.8rem);
        max-width: 10rem;
        max-height: 10rem;
    }

    .content-wrapper {
        display: flex;

        border-radius: $borderRadius;
        // border: 1px solid $cardBorderColor;
        background-color: $cardColor;

        // margin-left: 0.8rem;
        padding: 1.2rem;

        .button-container {
            display: flex;
            align-items: start;
        }
    }

    .card-content {
        margin-left: 0.8rem;

        .card-header {
            margin-bottom: 0.5rem;

            .fighter-name {
                margin: 0px;
            }

            .fighter-weight {
                text-transform: uppercase;
            }
        }

        .card-body {
            // border: 2px solid lavender;
            border-radius: $borderRadius;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 0.4rem;
            column-gap: 0.5rem;
            padding-top: 0.4rem;
        }
    }


    .info-wrapper {
        display: flex;
        align-items: center;
        justify-content: space-between;

        h6 {
            margin: 0px;
        }

        p {
            margin: 0px;
        }
    }

    .info-wrapper .fighter-stance {
        text-transform: capitalize;
    }
}

@media(max-width: 720px) {
    .fighter-card {
        width: 100%;
        margin: auto;
        row-gap: 1rem;

        .content-wrapper {
            justify-content: space-around;
            width: 100%;
        }
    }
}


@media(max-width: 576px) {
    .fighter-card {
        flex-direction: column;
    }
}
</style>

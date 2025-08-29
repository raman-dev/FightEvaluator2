<script setup>

const props = defineProps(['fighter'])

function inchesToFeetStr(inches) {
    return `${Math.floor(inches / 12)}'${inches % 12}`;
}
function dobToAge(dobString) {
    if (!dobString) return "N/A"; // handle empty input

    const today = new Date();
    const dob = new Date(dobString);

    let age = today.getFullYear() - dob.getFullYear();
    const monthDiff = today.getMonth() - dob.getMonth();
    const dayDiff = today.getDate() - dob.getDate();

    // if birthday hasn’t occurred yet this year, subtract 1
    if (monthDiff < 0 || (monthDiff === 0 && dayDiff < 0)) {
        age--;
    }

    return age;
}
</script>

<template>
    <div class="fighter-info m-1" >
        <div class="fighter-info-wrapper ">
            <div class="name">
                <h5>
                    <RouterLink to="/assessment/{{fighter.id}}">{{fighter.first_name }} {{ fighter.last_name }}</RouterLink>
                </h5>
            </div>
            <div class="d-flex">
                <img :src="fighter.img_link ? fighter.img_link : '/public/sample_150.png'" alt="">
                <div class="fighter-bio ">
                    <div class="age">
                        <h6 class="age-label">age:&nbsp;</h6>
                        <p class="age">{{ dobToAge(fighter.date_of_birth) }}</p>
                    </div>
                    <div class="record">
                        <h6 class="record-label">record:&nbsp;</h6>
                        <p class="record">{{ fighter.wins }}-{{ fighter.losses }}-{{ fighter.draws }}</p>
                    </div>
                    <div class="height">
                        <h6 class="height-label">height:&nbsp;</h6>
                        <p>{{ inchesToFeetStr(fighter.height) }}</p>
                    </div>
                    <div class="reach">
                        <h6 class="reach-label">reach:&nbsp;</h6>
                        <p>{{ fighter.reach }}</p>
                    </div>
                </div>
            </div>

        </div>
        <div class="fight-result-label d-none"></div><!--fight win method show-->
    </div>

</template>

<style lang="scss" scoped>
.fighter-info.win {
    outline-color: #00FF00;
}

.fighter-info.lose {
    outline-color: #FF0000;
}

.fighter-info {
    padding: 0.76rem;
    border-radius: 1rem;
    background-color: #12161A;
    outline: 3px solid transparent;
    outline-offset: 1px;

    h5 {
        margin: 0px;
    }

    .fight-result-label {
        color: #00FF00;
    }

    img {
        margin: auto;
        max-width: 10rem;
        border-radius: 1rem;
        transform: scale(0.8);
    }

    .fighter-bio>div {
        display: flex;
        align-items: center;
        justify-content: start;
        margin: 0.5rem;
    }

    .name {
        text-align: center;
        text-transform: capitalize;

        a {
            text-decoration: none;
            color: lavender;
        }
    }

    .fighter-bio {
        display: flex;
        flex-direction: column;
        justify-content: end;

        h6,
        p {
            margin: 0px;
        }
    }
}
</style>
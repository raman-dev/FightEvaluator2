<script setup>
import { ref } from 'vue';
import OddsTD from './OddsTD.vue';

const x = {
        fighter_a: 'Fighter A',
        fighter_b: 'Fighter B',
        odds: [{
            event:'win',
            odd:[1,2]
        },{
            event:'rounds_geq_one_half',
            odd: 3,
        },{
            event:'does_not_go_the_distance',
            odd: 4,
        }]
}

const matchupOddsList = [
    {
        fighter_a: 'Fighter A',
        fighter_b: 'Fighter B',
        odds: [
            { event: 'win', odd: [1, 2] },
            { event: 'rounds_geq_one_half', odd: 3 },
            { event: 'does_not_go_the_distance', odd: 4 }
        ]
    },
    {
        fighter_a: 'Fighter C',
        fighter_b: 'Fighter D',
        odds: [
            { event: 'win', odd: [2, 3] },
            { event: 'rounds_geq_one_half', odd: 2.5 },
            { event: 'does_not_go_the_distance', odd: 3.8 }
        ]
    },
    {
        fighter_a: 'Fighter E',
        fighter_b: 'Fighter F',
        odds: [
            { event: 'win', odd: [1.5, 2.5] },
            { event: 'rounds_geq_one_half', odd: 4.2 },
            { event: 'does_not_go_the_distance', odd: 3.1 }
        ]
    },
    {
        fighter_a: 'Fighter G',
        fighter_b: 'Fighter H',
        odds: [
            { event: 'win', odd: [2.1, 1.9] },
            { event: 'rounds_geq_one_half', odd: 3.3 },
            { event: 'does_not_go_the_distance', odd: 2.7 }
        ]
    },
    {
        fighter_a: 'Fighter I',
        fighter_b: 'Fighter J',
        odds: [
            { event: 'win', odd: [1.8, 2.2] },
            { event: 'rounds_geq_one_half', odd: 3.6 },
            { event: 'does_not_go_the_distance', odd: 2.9 }
        ]
    },
    {
        fighter_a: 'Fighter K',
        fighter_b: 'Fighter L',
        odds: [
            { event: 'win', odd: [1.7, 2.3] },
            { event: 'rounds_geq_one_half', odd: 2.8 },
            { event: 'does_not_go_the_distance', odd: 3.5 }
        ]
    },
    {
        fighter_a: 'Fighter M',
        fighter_b: 'Fighter N',
        odds: [
            { event: 'win', odd: [2.5, 1.5] },
            { event: 'rounds_geq_one_half', odd: 3.1 },
            { event: 'does_not_go_the_distance', odd: 2.6 }
        ]
    }
];


</script>

<template>
    <table class="table table-bordered">
        <thead>
            <th>Fighter A</th>
            <th>Fighter B</th>
            <th>Odds A</th>
            <th>Odds B</th>
            <th>Rounds >= 1.5</th>
            <th>Does Not Go The Distance</th>
        </thead>
        <tbody>
            <tr v-for="data in matchupOddsList">
                <td>{{ data.fighter_a }}</td>
                <td>{{ data.fighter_b }}</td>
                
                <template v-for="odd in data.odds">
                    <OddsTD v-bind="odd" />
                     <!-- <td v-if="eventName == 'win'" v-for="o in odd">
                        {{ o }}
                     </td>
                     <td v-else>
                        {{ odd }}
                     </td> -->
                </template>
            </tr>
        </tbody>
    </table>
</template>
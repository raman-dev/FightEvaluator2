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

/*
        matchup_id
            title
            events
                event_0
                    likelihood
                    likelihood_val
                    justification
                    fighter_x_name | None 
               
*/
const matchups = [
  {
    matchup_id: 1,
    title: "Fighter A vs Fighter B",
    events: {
      win: {
        likelihood: "very likely",
        likelihood_val: 1,
        justification: "Fighter A has a strong grappling advantage and recent win streak.",
        fighter: "Fighter A"
      },
      rounds_geq_one_half: {
        likelihood: "neutral",
        likelihood_val: 3,
        justification: "Both fighters tend to finish early, but may test each other in round 1.",
        fighter: null
      },
      does_not_go_the_distance: {
        likelihood: "very likely",
        likelihood_val: 1,
        justification: "Both fighters have high KO rates and rarely go to decision.",
        fighter: null
      }
    }
  },
  {
    matchup_id: 2,
    title: "Fighter C vs Fighter D",
    events: {
      win: {
        likelihood: "very unlikely",
        likelihood_val: 5,
        justification: "Fighter C is returning from injury and hasn't fought top competition.",
        fighter: "Fighter C"
      },
      rounds_geq_one_half: {
        likelihood: "somewhat likely",
        likelihood_val: 2,
        justification: "Both fighters have good cardio and tend to engage in technical fights.",
        fighter: null
      },
      does_not_go_the_distance: {
        likelihood: "neutral",
        likelihood_val: 3,
        justification: "Fighter D has some submission potential, but both are durable.",
        fighter: null
      }
    }
  },
  {
    matchup_id: 3,
    title: "Fighter E vs Fighter F",
    events: {
      win: {
        likelihood: "somewhat likely",
        likelihood_val: 2,
        justification: "Fighter F has powerful striking but Fighter E has better defense.",
        fighter: "Fighter F"
      },
      rounds_geq_one_half: {
        likelihood: "somewhat likely",
        likelihood_val: 2,
        justification: "Possible early exchanges, but both may respect each other's power.",
        fighter: null
      },
      does_not_go_the_distance: {
        likelihood: "somewhat unlikely",
        likelihood_val: 4,
        justification: "Both fighters have gone to decision in recent bouts.",
        fighter: null
      }
    }
  }
];

</script>

<template>
    <table class="table table-bordered">
        <thead>
            <th>Matchup</th>
            <th>
                <div class="d-flex justify-content-between">
                    <span>Win A</span>
                    <span>Win B</span>
                </div>
            </th>
            <th>Rounds >= 1.5</th>
            <th>Does Not Go The Distance</th>
        </thead>
        <tbody>
            <tr v-for="data in matchupOddsList">
                <td>
                    <span>{{ data.fighter_a }} vs {{ data.fighter_b }}</span>
                </td>
                <td>
                    <div class="d-flex justify-content-between">
                        <span>{{ data.fighter_a }}</span>
                        <span>{{ data.fighter_b }}</span>
                    </div>
                </td>
                
                <template v-for="odd in data.odds">
                    <OddsTD v-bind="odd" />
                    
                </template>
            </tr>
        </tbody>
    </table>
</template>
<script setup>

import { ref } from 'vue';
import EventLikelihoodRow from './EventLikelihoodRow.vue';

const matchupData = [
  {
    matchup_id: 1,
    title: "Fighter A vs Fighter B",
    events: {
      win: [
        {
          likelihood: "somewhat likely",
          likelihood_val: 2,
          justification: "Fighter A has a strong takedown defense and striking advantage.",
          fighter: "Fighter A"
        },
        {
          likelihood: "somewhat unlikely",
          likelihood_val: 4,
          justification: "Fighter B has shown weakness against similar opponents.",
          fighter: "Fighter B"
        }
      ],
      rounds_geq_one_half: {
        likelihood: "very likely",
        likelihood_val: 1,
        justification: "Both fighters are known for cautious first rounds."
      },
      does_not_go_the_distance: {
        likelihood: "somewhat likely",
        likelihood_val: 2,
        justification: "High knockout rates on both sides indicate early finish potential."
      }
    }
  },
  {
    matchup_id: 2,
    title: "Fighter C vs Fighter D",
    events: {
      win: [
        {
          likelihood: "neutral",
          likelihood_val: 3,
          justification: "Both fighters have similar skill levels and fight records.",
          fighter: "Fighter C"
        },
        {
          likelihood: "neutral",
          likelihood_val: 3,
          justification: "Both fighters have similar skill levels and fight records.",
          fighter: "Fighter D"
        }
      ],
      rounds_geq_one_half: {
        likelihood: "somewhat likely",
        likelihood_val: 2,
        justification: "Both tend to pace themselves in earlier rounds."
      },
      does_not_go_the_distance: {
        likelihood: "somewhat unlikely",
        likelihood_val: 4,
        justification: "Neither fighter has a high finish rate in recent fights."
      }
    }
  },
  {
    matchup_id: 3,
    title: "Fighter E vs Fighter F",
    events: {
      win: [
        {
          likelihood: "very likely",
          likelihood_val: 1,
          justification: "Fighter E's grappling dominance is expected to control the match.",
          fighter: "Fighter E"
        },
        {
          likelihood: "very unlikely",
          likelihood_val: 5,
          justification: "Fighter F lacks tools to counter Fighter E's ground game.",
          fighter: "Fighter F"
        }
      ],
      rounds_geq_one_half: {
        likelihood: "neutral",
        likelihood_val: 3,
        justification: "If Fighter E gets an early takedown, a quick finish is possible."
      },
      does_not_go_the_distance: {
        likelihood: "very likely",
        likelihood_val: 1,
        justification: "Fighter E typically finishes fights within the first round."
      }
    }
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
        
        
        
        matchup_id
        title
        events:
          win:[
              [likelihood,likelihood_val,justification,fighter_a],
              [likelihood,likelihood_val,justification,fighter_b]
            ]
          rounds_geq_one_half:
            likelihood,likelihood_val,justification 
          does_not_go_the_distance:
            likelihood,likelihood_val,justification 

               
*/




</script>

<template>
  <div class="table-container">
    <h2 class="event-title">event title</h2>
    <table class="prediction-table table table-bordered table-hover">
    <thead>
      <tr>
        <th>Matchup</th>
        <th>
          <div class="d-flex justify-content-between">
            <span>Win A</span>
            <span>Win B</span>
          </div>
        </th>
        <th>Rounds >= 1.5</th>
        <th>Does Not Go The Distance</th>
      </tr>

    </thead>
    <tbody>
      
      <template v-for="data in matchupData">
          <EventLikelihoodRow v-bind="data"/>
      </template>
    
    </tbody>
    </table>
  </div>
  
</template>

<style lang="scss" scoped>
.event-title{
  text-transform: capitalize;
}
.table-container{
    overflow-x: auto;
}

th {
  text-transform: capitalize;
}

tbody {
  span {
    text-align: center;
  }

  tr {
    transition: height 0.3s ease-out;
  }
}
</style>
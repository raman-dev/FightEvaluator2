<script setup>

import { onMounted, ref, useTemplateRef } from 'vue';
import EventLikelihoodRow from './EventLikelihoodRow.vue';
import TableActions from './TableActions.vue';

const tableExpanded = ref(true);
const tableContainer = useTemplateRef('table-container');

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

function hideTable() {
  //hide the table
  tableExpanded.value = !tableExpanded.value;
  const table = tableContainer.value.querySelector('table');
  const style = window.getComputedStyle(table);
  const tableHeight = table.offsetHeight;
  const tableMargin = parseFloat(style.marginTop) + parseFloat(style.marginBottom);

  if (tableExpanded.value == true) {
    //show table
    tableContainer.value.style.height = `${tableHeight + tableMargin+ 16}px`;
    // tableContainer.value.style.height ='auto';
  } else {
    // heightPreHide.value = tableContainer.value.offsetHeight;
    tableContainer.value.style.height = `0px`;
  }
}


function resizeTableHeight(heightChange) {
  //function executes before children change scroll height of container
  const table = tableContainer.value.querySelector("table");
  const style = window.getComputedStyle(table);
  const tableHeight = table.scrollHeight;
  const tableMargin = parseFloat(style.marginTop) + parseFloat(style.marginBottom);

  let newScrollHeight = tableHeight + heightChange + tableMargin;
  console.log(tableHeight,heightChange,tableMargin,newScrollHeight);

  tableContainer.value.style.height = `${newScrollHeight + 16}px`//16 for horizontal scrollbar
}

onMounted(() => {
  //set table height
  const scrollHeight = tableContainer.value.scrollHeight;
  tableContainer.value.style.height = `${scrollHeight}px`;
});

</script>

<template>
  <div class="d-flex justify-content-between my-3">
    <h1 class="event-title">Event Title</h1>
    <button class="btn btn-outline-secondary table-toggle-btn" @click="hideTable()">hide table</button>
  </div>

  <div class="table-container" ref="table-container">
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

        <template v-for="(data,index) in matchupData" :key="index">
          <EventLikelihoodRow v-bind="data" @height-change="resizeTableHeight" />
        </template>

      </tbody>
    </table>
  </div>
  <TableActions  />

</template>

<style lang="scss" scoped>
.event-title {
  text-transform: capitalize;
}

.table-container {
  transition: height 0.3s ease-out;
  overflow-x: auto;
  overflow-y: hidden;
}

// table {
//   margin: 0px;
// }

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
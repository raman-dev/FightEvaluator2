<script setup>
const matchup = defineModel ('matchup',{});
//     default : {
//         id: null,
//         fighter_a : -1,
//         fighter_b: -1,
//         fighter_a_name: '',
//         fighter_b_name: '',
//         weight_class: '',
//         rounds: 0,
//         analysisComplete: false,
//         inWatchList: false
//     }
// });
// <!--
//         on right click table row
//             show a menu with options
//              - watch/unwatch
//              - analyze
//              - edit
//              - delete

//             on click watch
//                 add to watchlist 
//                     update matchup on server
//             on click analyze 
//                 open analysis page
//             on click edit
//                 open editor with matchup data instead of empty editor
//             on click delete
//                 show confirmation dialog
//     -->


const props = defineProps(['tableName']); 
function removeUnderscores(str) {
  if (typeof str !== "string") {
    throw new TypeError("Expected a string");
  }
  return str.replace(/_/g, " ");
}
</script>
<template>
    <tr :class="{active:matchup.active,watching:matchup.inWatchList && props.tableName !== 'WatchList'}" class="matchup">
        <td>
            <div class="d-flex align-items-center justify-content-center p-1">
                <p>{{ matchup.fighter_a_name }} vs {{ matchup.fighter_b_name }}</p>
            </div>
        </td>
        <td class="weightclass">    
            <div class="d-flex align-items-center justify-content-center p-1">
                <p>{{removeUnderscores(matchup.weight_class)}}</p>
            </div>
        </td>
        <td>    
            <div class="d-flex align-items-center justify-content-center p-1">
                <p>{{matchup.rounds}}</p>
            </div>
        </td>
        <td v-if="props.tableName === 'WatchList'">
            <div class="d-flex align-items-center justify-content-center p-1">
                <p>
                    <svg v-if="matchup.analysisComplete" class="complete-icon" xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#75FB4C"><path d="M268-240 42-466l57-56 170 170 56 56-57 56Zm226 0L268-466l56-57 170 170 368-368 56 57-424 424Zm0-226-57-56 198-198 57 56-198 198Z"/></svg>
                    <svg v-else class="incomplete-icon" xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#EA3323"><path d="M680-80q-83 0-141.5-58.5T480-280q0-83 58.5-141.5T680-480q83 0 141.5 58.5T880-280q0 83-58.5 141.5T680-80Zm67-105 28-28-75-75v-112h-40v128l87 87Zm-547 65q-33 0-56.5-23.5T120-200v-560q0-33 23.5-56.5T200-840h167q11-35 43-57.5t70-22.5q40 0 71.5 22.5T594-840h166q33 0 56.5 23.5T840-760v250q-18-13-38-22t-42-16v-212h-80v120H280v-120h-80v560h212q7 22 16 42t22 38H200Zm280-640q17 0 28.5-11.5T520-800q0-17-11.5-28.5T480-840q-17 0-28.5 11.5T440-800q0 17 11.5 28.5T480-760Z"/></svg>                                              
                </p>
            </div>
        </td>
    </tr>
</template>

<style lang="scss" scoped>

    .matchup{
        user-select: none;
    }

    .watching{
        background-color: hsla(0, 0%, 12%, 0.5);
        pointer-events: none;
        color: darkslategray !important;
    }
    
    .matchup:hover{
        background-color: hsl(200, 56%, 12%);
        cursor: pointer;
    }
    //hover active order matters to not change active color when hover and active
    .matchup.active{
        background-color: hsl(175, 61.57%, 24.95%);
    }

    td.weightclass{
        text-transform: capitalize;
    }

</style>
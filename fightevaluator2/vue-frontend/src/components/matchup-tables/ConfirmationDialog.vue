<script setup>
import { useMatchupStore } from '@/stores/matchupStore';
import { storeToRefs } from 'pinia';
import { ref } from 'vue';

const open = defineModel('open', { type: Boolean, default: false });
const matchupStore = useMatchupStore();
const { activeMatchup } = storeToRefs(useMatchupStore());


function onClickCancelDelete(event) {
    open.value = false;
}

function deleteMatchup() {
    // Implement the deletion logic here, e.g., call an API or update the store
    console.log(`Deleting matchup with ID: ${activeMatchup.value.id}`);
    open.value = false;
    matchupStore.deleteMatchup(activeMatchup.value.matchup.id);
}

</script>

<template>
    <div class="confirmation-dialog" data-matchup-id="-1" v-if="open" @click="onClickCancelDelete">
        <div class="dialog-container bg-dark rounded-3">
            <div class="dialog-title">
                <h4>Delete following MatchUp.</h4>
            </div>
            <div class="dialog-body border p-1 my-3">
                <p class="m-0">{{ activeMatchup.matchup.fighter_a_name }} vs {{ activeMatchup.matchup.fighter_b_name }}</p>
            </div>
            <div class="dialog-actions">
                <button class="cancel btn btn-secondary" @click="onClickCancelDelete">cancel</button>
                <button class="confirm btn btn-primary" @click="deleteMatchup">confirm</button>
            </div>
        </div>
    </div>
</template>

<style lang="scss" scoped>
.confirmation-dialog{
  position: absolute;
  left: 0px;
  top: 0px;

  width: 100%;
  height: 100%;
  z-index: 20000;

  display: flex;
  justify-content: center;
  align-items: center;

  background-color: hsla(0, 0, 10%, 0.75);

  .dialog-container{
    border:2px solid #dc3545;
    padding: 1.4rem;
    width: fit-content;
    .dialog-title{
      margin-right: 1rem;
    } 
    .dialog-body{
      // border-width: 1px !important;
      border-color: #dc3545 !important;
      p{
        text-transform: capitalize;
        text-align: center;
      }
    }
    .dialog-actions{
      display: flex;
      justify-content: end;
      .cancel{
        margin-right: 0.8rem;
      }
    }
  }
}
</style>
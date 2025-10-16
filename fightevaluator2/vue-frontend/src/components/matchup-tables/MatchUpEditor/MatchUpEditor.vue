<script setup>

import { onMounted, ref, inject, watch } from 'vue';
import { Transition } from 'vue';
import SuggestionBox from './SuggestionBox.vue';
import WeightClassSelector from './WeightClassSelector.vue';
import RoundsSelector from './RoundsSelector.vue';
import PrelimSelector from './PrelimSelector.vue';
import { storeToRefs } from 'pinia';
import { useMatchupStore } from '@/stores/matchupStore';


const emits = defineEmits(['editorClosing']);
const open = defineModel('open', { default: false });
const inEditMode = defineModel('inEditMode', { default: false });

const selectedFighterA = ref(null);
const selectedFighterB = ref(null);

const queryFighterAEnabled = ref(true);
const suggestionsFighterA = ref([]);

const queryFighterBEnabled = ref(true);
const suggestionsFighterB = ref([]);

const fighterAText = ref('');
const fighterBText = ref('');
const rounds = ref("3");
const isPrelim = ref(false);
const weightClass = ref('');

const server = inject('server');
const matchupStore = useMatchupStore();
const { activeMatchup,event } = storeToRefs(useMatchupStore());

function commitChanges() {
  // console.log("Committing changes...");
  // console.log("Fighter A:", selectedFighterA.value);
  // console.log("Fighter B:", selectedFighterB.value);
  // console.log("Rounds:", rounds.value);
  // console.log("Is Prelim:", isPrelim.value);
  // console.log("Weight Class:", weightClass.value);
  if (inEditMode.value) {
    //update existing matchup
    console.log("Updating existing matchup...");
  } else {
    //create new matchup
    console.log("Creating new matchup...");
    const matchup = {
      event: event.value.id,
      fighter_a: selectedFighterA.value ? selectedFighterA.value.id : null,
      fighter_b: selectedFighterB.value ? selectedFighterB.value.id : null,
      rounds: rounds.value,
      isprelim: isPrelim.value,
      weight_class: weightClass.value
    }
    matchupStore.createMatchup(matchup);
  }
}

function onClickBackground(event) {
  if (event.target === event.currentTarget) {
    open.value = false;
    emits('editorClosing');
  }
}

function onFighterSearchResult(data) {
  let fighters = data['fighters'];
  //populate the suggestion box
  this.model.value = fighters;
}

function onSearchBoxValueChange(queryFlag, suggestions, searchText) {
  if (searchText.length > 0) {
    if (queryFlag.value == true) {
      server.search_fighters(onFighterSearchResult.bind({ model: suggestions }), searchText);
    }
  } else {
    suggestions.value = [];
  }
}

watch(fighterAText, (newSearchVal, _) => {
  onSearchBoxValueChange(queryFighterAEnabled, suggestionsFighterA, newSearchVal);
});

watch(fighterBText, (newSearchVal, _) => {
  onSearchBoxValueChange(queryFighterBEnabled, suggestionsFighterB, newSearchVal);
});

function onFighterSelect(queryFlag, fighterText, newFighter) {
  console.log('onFighterSelect called with: ', newFighter);
  if (newFighter != null) {
    queryFlag.value = false;
    if ('first_name' in newFighter) {
      fighterText.value = `${newFighter.first_name} ${newFighter.last_name}`;
    } else {
      fighterText.value = newFighter.name;
    }
  } else {
    queryFlag.value = true;
    fighterText.value = '';
  }
}

watch(selectedFighterA, (newFighter, _) => {
  // console.log("Fighter A selected:", newFighter);
  onFighterSelect(queryFighterAEnabled, fighterAText, newFighter);
});

watch(selectedFighterB, (newFighter, _) => {
  // console.log("Fighter B selected:", newFighter);
  onFighterSelect(queryFighterBEnabled, fighterBText, newFighter);
});

watch(open, (isOpen, _) => {
  if (isOpen === true) {
    if (inEditMode.value === true) {
      //check has activeMatchup
      //fill editor with activeMatchup data
      console.log('matchupEditor.open.inEditMode', activeMatchup);
      const matchup = activeMatchup.value.matchup;

      isPrelim.value = matchup.isprelim;
      rounds.value = matchup.rounds;
      weightClass.value = matchup.weight_class;
      selectedFighterA.value = { id: matchup.fighter_a, name: matchup.fighter_a_name };
      selectedFighterB.value = { id: matchup.fighter_b, name: matchup.fighter_b_name };
    }
  }else{
    console.log('matchup.Editor.closing');
    inEditMode.value = false;
    isPrelim.value = false;
    rounds.value = 3;
    weightClass.value = "";
    selectedFighterA.value = null;
    selectedFighterB.value = null;
  }
});


</script>

<template>
  <!-- <Transition> -->
  <div class="vmodal-container" @click="onClickBackground" v-if="open">
    <div class="vmodal-content">
      <div class="matchup-editor border rounded-2 bg-dark" data-event-id="118">
        <h1 class="modal-title title fs-4">Create MatchUp</h1>
        <form>
          <div class="search-box2">
            <div class="input-group">
              <label class="input-group-text" for="fighter-a-input">Fighter A</label>

              <div class="input-wrapper">
                <input class="form-control rounded-0" data-fighter-id="-1" type="text" name="fighter-a"
                  id="fighter-a-input" placeholder="Enter fighter name..." v-model="fighterAText"
                  :disabled="!queryFighterAEnabled">
                <!-- <ul class="suggestion-box list-group" id="fighter-a-suggestion-box"></ul>-->
                <SuggestionBox v-model:fighters="suggestionsFighterA" v-model:selectedFighter="selectedFighterA">
                </SuggestionBox>
              </div>

              <button class="btn btn-outline-danger clear-btn" type="button" id="button-addon2"
                @click="selectedFighterA = null">Clear</button>
            </div>

          </div>

          <div class="searchbox-seperator my-2">
            <p>versus</p>
          </div>

          <div class="search-box2">
            <div class="input-group">

              <label class="input-group-text" for="fighter-b-input">Fighter B</label>
              <div class="input-wrapper">
                <input class="form-control rounded-0" data-fighter-id="-1" type="text" v-model="fighterBText"
                  name="fighter-b" id="fighter-b-input" placeholder="Enter fighter name..."
                  :disabled="!queryFighterBEnabled">
                <SuggestionBox v-model:fighters="suggestionsFighterB" v-model:selectedFighter="selectedFighterB">
                </SuggestionBox>
              </div>

              <button class="btn btn-outline-danger clear-btn" type="button" id="button-addon2"
                @click="selectedFighterB = null">Clear</button>
            </div>
          </div>

          <WeightClassSelector v-model:weightClass="weightClass"></WeightClassSelector>

          <div class="rounds-isprelim-wrapper">
            <RoundsSelector v-model:rounds="rounds"></RoundsSelector>

            <PrelimSelector v-model:isPrelim="isPrelim"></PrelimSelector>
          </div>
        </form>
        <div class="editor-actions mt-3">
          <button type="button" class="btn btn-secondary mx-2 close-btn" @click="open = !open">Close</button>
          <button type="button" class="btn btn-primary create-btn current-action submit-btn"
            @click="commitChanges(true)">Create</button>
          <button type="button" class="btn btn-primary save-btn submit-btn" @click="commitChanges(false)">Save</button>
        </div>
      </div>

    </div>
  </div>
  <!-- </Transition> -->


</template>

<style lang="scss">
.matchup-editor {
  width: fit-content;
  padding: 0.6rem;

  .title {
    margin-bottom: 0.8rem;
  }

  form {
    padding-left: 0.6rem;
    padding-right: 0.6rem;

    select,
    option,
    button,
    input {
      cursor: pointer !important;
    }

  }

  .search-box2 {
    text-transform: capitalize;

    input,
    ul {
      width: 28ch;
      text-transform: capitalize;
    }

    ul {
      position: absolute;
      overflow: visible;
      z-index: 10000;

      li p {
        margin: 0px;
      }
    }
  }

  .searchbox-seperator {
    text-align: center;

    p {
      margin: 0px;
      text-transform: capitalize;
    }
  }



  .rounds-isprelim-wrapper {
    display: flex;
    justify-content: space-evenly;
  }

  .rounds-radio-group {
    width: fit-content;
    display: flex;

    .radio-group-title {
      margin: 0px;
    }
  }

  .isprelim-checkbox {
    label {
      text-transform: capitalize;
    }
  }

  .editor-actions {
    display: flex;
    justify-content: end;

    .submit-btn {
      display: none;
    }

    .current-action {
      display: block;
    }
  }
}

//full size width and height
.vmodal-container {
  position: fixed;
  width: 100%;
  height: 100%;

  top: 0px;
  left: 0px;
  z-index: 10000;

  display: flex;
  justify-content: center;

  background-color: rgba($color: #000000, $alpha: 0.5);


  .vmodal-content {
    margin: auto;
  }
}

// .r-modal {
//   position: absolute;

//   display: flex;
//   justify-content: center;
//   width: 100%;
//   height: 100%;
//   left: 0px;
//   top: 0px;

//   background-color: rgba($color: #000000, $alpha: 0);
//   // opacity: 0;
//   pointer-events: none;
//   z-index: 1000;


//   transition: background-color 0.2s ease-in-out;

//   .r-modal-content {
//     position: absolute;
//     // display: none;

//     background-color: #212529;
//     width: fit-content;

//     top: 0px;
//     border: 1px solid black;

//     // opacity: 0;
//     transition: all 0.2s ease-out !important;

//     pointer-events: none;
//     user-select: none;

//     * {
//       pointer-events: initial;
//       user-select: initial;
//     }
//   }

// }

// .r-modal.r-show {
//   background-color: rgba($color: #000000, $alpha: 0.5);
//   pointer-events: initial;

//   .r-modal-content {
//     opacity: 1 !important;
//     top: 15%;

//     pointer-events: initial;
//     user-select: initial;

//     * {
//       pointer-events: initial;
//       user-select: initial;
//     }
//   }
// }</style>

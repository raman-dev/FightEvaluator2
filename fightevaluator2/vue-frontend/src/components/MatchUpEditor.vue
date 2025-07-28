<script setup>

import { onMounted, ref, inject, watch } from 'vue';
import { Transition } from 'vue';


const emits = defineEmits(['editorClosing']);
const open = defineModel('open', { default: false });
const csrftoken = inject('csrftoken');


const fighterAText = ref('');
const fighterBText = ref('');
const rounds = ref("3");
const isPrelim = ref(false);
const weightClass = ref('');

function commitChanges() {

}

function onClickBackground(event) {
    if (event.target === event.currentTarget) {
        open.value = false;
        emits('editorClosing');
    }
}

watch(fighterAText,(newVal,oldVal) => {
  // console.log("Fighter A text: ",oldVal,newVal);
  //send get request to server to fetch top 5 suggestions
});

watch(fighterBText,(newVal,oldVal)=>{
  console.log("Fighter B text: ",oldVal,newVal);
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
                      id="fighter-a-input" placeholder="Enter fighter name..." v-model="fighterAText">
                    <ul class="suggestion-box list-group"></ul>
                  </div>

                  <button class="btn btn-outline-danger clear-btn" type="button" id="button-addon2">Clear</button>
                </div>

              </div>

              <div class="searchbox-seperator my-2">
                <p>versus</p>
              </div>

              <div class="search-box2">
                <div class="input-group">

                  <label class="input-group-text" for="fighter-b-input">Fighter B</label>
                  <div class="input-wrapper">
                    <input class="form-control rounded-0" data-fighter-id="-1" type="text" v-model="fighterBText" name="fighter-b"
                      id="fighter-b-input" placeholder="Enter fighter name...">
                    <ul class="suggestion-box list-group"></ul>
                  </div>

                  <button class="btn btn-outline-danger clear-btn" type="button" id="button-addon2">Clear</button>
                </div>
              </div>

              <!--weight class-->
              <div class="weightclass-selector my-4">
                <div class="weightclass input-group mb-3">
                  <label class="input-group-text" for="weight-class-select">Weightclass</label>
                  <select class="form-select" id="weight-class-select" name="weight_class" v-model="weightClass">
                    <option selected="" value="">Choose a weight class...</option>
                    <option value="strawweight">Strawweight</option>
                    <option value="flyweight">Flyweight</option>
                    <option value="bantamweight">Bantamweight</option>
                    <option value="featherweight">Featherweight</option>
                    <option value="lightweight">Lightweight</option>
                    <option value="welterweight">Welterweight</option>
                    <option value="middleweight">Middleweight</option>
                    <option value="light_heavyweight">Light Heavyweight</option>
                    <option value="heavyweight">Heavyweight</option>
                  </select>
                </div>
              </div>

              <div class="rounds-isprelim-wrapper">
                <!--rounds-->
                <div class="rounds-radio-group border rounded-2 p-1 px-3">
                  <p class="radio-group-title">Rounds</p>
                  <div class="form-check mx-3">
                    <input class="form-check-input" type="radio" name="rounds" value="3" id="rounds-radio-3" v-model="rounds">
                    <label class="form-check-label" for="rounds-radio-3">
                      3
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="radio" name="rounds" value="5" id="rounds-radio-5" v-model="rounds">
                    <label class="form-check-label" for="rounds-radio-5">
                      5
                    </label>
                  </div>
                </div>
                <!--prelim status-->
                <div class="isprelim-checkbox border rounded-2 p-1 px-3">
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" v-model="isPrelim" name="isprelim" id="isprelim-checkbox"
                      checked="">
                    <label class="form-check-label" for="isprelim-checkbox">
                      on prelims
                    </label>
                  </div>
                </div>
              </div>
            </form>
            <div class="editor-actions mt-3">
              <button type="button" class="btn btn-secondary mx-2 close-btn"
                @click="open=!open">Close</button>
              <button type="button" class="btn btn-primary create-btn current-action submit-btn"
                v-on:click="commitChanges(true)">Create</button>
              <button type="button" class="btn btn-primary save-btn submit-btn"
                v-on:click="commitChanges(false)">Save</button>
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
    button {
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

  .weightclass-selector {
    width: fit-content;
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
.vmodal-container{
  position: fixed;
  width: 100%;
  height: 100%;

  top: 0px;
  left: 0px;
  z-index: 10000;

  display: flex;
  justify-content: center;

  background-color: rgba($color: #000000, $alpha: 0.5);
  

  .vmodal-content{
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
// }
</style>

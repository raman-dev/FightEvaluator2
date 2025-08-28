<script setup>
import { reactive, ref } from "vue";

const visible = defineModel('visible');
const fighter = defineModel('fighter');

function saveFighter() {
  console.log("Saving fighter:", fighter);
  // TODO: send to backend
  closeModal();
}

function closeModal() {
  visible.value = false;
}

</script>
<template>
  <div class="xmodal" v-show="visible">
    <div class="xmodal-container bg-dark flex-column">
      <div class="fighter-creator">
        <h3 class="text-start mb-2">Edit Fighter</h3>
        <form class="border rounded p-2" @submit.prevent="saveFighter">
          <div class="row">
            <div class="col">
              <label for="first_name" class="form-label">First Name</label>
              <input
                type="text"
                class="form-control"
                id="first_name"
                v-model="fighter.first_name"
                placeholder="First Name"
              />
            </div>
            <div class="col">
              <label for="last_name" class="form-label">Last Name</label>
              <input
                type="text"
                class="form-control"
                id="last_name"
                v-model="fighter.last_name"
                placeholder="Last Name"
              />
            </div>
            <div class="col">
              <label for="date_of_birth" class="form-label">Date of Birth</label>
              <input
                type="date"
                class="form-control"
                id="date_of_birth"
                v-model="fighter.date_of_birth"
              />
            </div>
          </div>

          <div class="row">
            <div class="col">
              <label for="height" class="form-label">Height</label>
              <input
                type="number"
                class="form-control"
                id="height"
                v-model="fighter.height"
                max="99"
                placeholder="Height"
              />
            </div>
            <div class="col">
              <label for="reach" class="form-label">Reach</label>
              <input
                type="number"
                class="form-control"
                id="reach"
                v-model="fighter.reach"
                max="99"
                placeholder="Reach"
              />
            </div>
          </div>

          <div class="row record-edit justify-content-around">
            <div class="col col-3">
              <label for="wins" class="form-label">Wins</label>
              <input
                type="number"
                class="form-control"
                id="wins"
                v-model="fighter.wins"
                placeholder="Wins"
              />
            </div>
            <div class="col col-3">
              <label for="losses" class="form-label">Losses</label>
              <input
                type="number"
                class="form-control"
                id="losses"
                v-model="fighter.losses"
                placeholder="Losses"
              />
            </div>
            <div class="col col-3">
              <label for="draws" class="form-label">Draws</label>
              <input
                type="number"
                class="form-control"
                id="draws"
                v-model="fighter.draws"
                placeholder="Draws"
              />
            </div>
          </div>

          <div class="row">
            <div class="col">
              <label for="weight_class" class="form-label">Weight Class</label>
              <select
                class="form-select"
                id="weight_class"
                v-model="fighter.weight_class"
              >
                <option value="">Choose...</option>
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
            <div class="col">
              <label for="stance" class="form-label">Stance</label>
              <select
                class="form-select"
                id="stance"
                v-model="fighter.stance"
              >
                <option value="">Choose...</option>
                <option value="orthodox">Orthodox</option>
                <option value="southpaw">Southpaw</option>
                <option value="switch">Switch</option>
                <option value="open_stance">Open Stance</option>
              </select>
            </div>
          </div>

          <div class="row">
            <div class="col">
              <label for="img_link" class="form-label">Image Link</label>
              <input
                type="text"
                class="form-control img-link"
                id="img_link"
                v-model="fighter.img_link"
                placeholder="Image Link"
              />
            </div>
          </div>

          <div class="row">
            <div class="col">
              <label for="data_api_link" class="form-label">Data Api Link</label>
              <input
                type="text"
                class="form-control data-api-link"
                id="data_api_link"
                v-model="fighter.data_api_link"
                placeholder="Data Api Link"
              />
            </div>
          </div>

          <div class="row">
            <button
              class="btn btn-secondary my-2 w-auto"
              style="margin-left: auto; margin-right: 1rem"
              type="button"
              @click="closeModal"
            >
              Close
            </button>
            <button
              class="btn btn-primary my-2 w-auto"
              style="margin-right: 1rem"
              type="submit"
            >
              Save Changes
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>



<style scoped lang="scss">
.xmodal{
  position: absolute;
  z-index: 10000; 
  background-color: rgba($color: #000000, $alpha: 0);
  left: 0px;
  top: 0px;
  height: 100%;
  width: 100%;
  transition: all 0.2s ease-in-out;
  
  display: flex;
  align-items: center;
  justify-content: center;
  //rises up from bottom
  .xmodal-container{
    z-index: 10001;
    display: flex;
    width: fit-content;
    
    padding: 1.5rem; 
    border-radius: 0.5rem;
    
    // opacity: 0;
    transition: all 0.3s ease-in-out;
  }
}

.xmodal.show {
    pointer-events: all;
    background-color: rgba($color: #000000, $alpha: 0.5);
    .xmodal-container{
      opacity: 1;
      transform: translateY(0%);
    }
}

.xmodal.hide {
  background-color: rgba($color: #000000, $alpha: 0);
  pointer-events: none;
  .xmodal-container{
    opacity: 0;
    transform: translateY(100%);
  }
}

.fighter-creator form{
  display: flex;
  flex-direction: column;
  row-gap: 0.8rem;
  input#first_name, input#last_name{
    text-transform: capitalize;
  } 
} 
</style>

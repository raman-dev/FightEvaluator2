<script>
export const defaultFighterData = {
    'first_name':"",
    'last_name':"",
    'date_of_birth':"",
    'height':0,
    'reach':0,
    'wins':0,
    'draws':0,
    'losses':0,
    'weight_class':0,
    'img_link':"",
    'data_api_link':"",
};
</script>
<script setup>

import { ref,inject, watch } from 'vue';

const visible = defineModel('visible',{default:false}); 
const fighter = defineModel('fighter',{default : structuredClone(defaultFighterData)})

const server = inject('server');
const emit = defineEmits(['saveFighter']);

const createFighterError = ref(false);

function createFighter(){
  //grab details makesure something has changed though 
  //all required elements are present
  const fighterData = fighter.value;
  // console.log(`Fighter data: ${data}`);
  for (const key in fighterData) {
    console.log(`${key}: ${fighterData[key]}`);
  }
  
  //check if first name and last name and dob is not empty
  if (fighterData.first_name.length === 0 || 
      fighterData.last_name.length === 0 || 
      fighterData.date_of_birth.length === 0){
    return;
  }
  
  server.create_fighter(fighterData,onCreateFighterResult);
}

watch(visible,(newVal,oldVal) => {
  if (visible.value === true){
    //clear 
    fighter.value = structuredClone(defaultFighterData);
  }
});

function onCreateFighterResult(result){
  console.log(`create_fighter.result => \n${JSON.stringify(result)} `);
  //on success close dialog
  if ('success' in result){
    visible.value = false;
    return;
  }
  //on failure show error
  showErrorMessage();
}

function showErrorMessage(){
  createFighterError.value = true;
}


</script>
<template>
    <!--
        do what here?
        background + modal dialog?

        sit on top of entire page
    -->
    <Transition>
      <div class="modal-background" v-if="visible" @click.self="visible=!visible">
          <div class="fighter-creator p-3">
            <h3 class="text-start mb-2">Quick Add Fighter</h3>
            <form class="border rounded p-2" @submit.prevent="createFighter">
              <div class="row">
                <div class="col">
                  <label for="first_name" class="form-label">First Name</label>
                  <input type="text" class="form-control" id="first_name" v-model="fighter.first_name"
                    placeholder="First Name" />
                </div>
                <div class="col">
                  <label for="last_name" class="form-label">Last Name</label>
                  <input type="text" class="form-control" id="last_name" v-model="fighter.last_name"
                    placeholder="Last Name" />
                </div>
                
              </div>
              <div class="col">
                  <label for="date_of_birth" class="form-label">Date of Birth</label>
                  <input type="date" class="form-control" id="date_of_birth" v-model="fighter.date_of_birth" />
              </div>
              

              <div class="row">
                <div class="col">
                  <label for="weight_class" class="form-label">Weight Class</label>
                  <select class="form-select" id="weight_class" v-model="fighter.weight_class">
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
              </div>

              <div class="row">
                <div class="col">
                  <label for="data_api_link" class="form-label">Data Api Link</label>
                  <input type="text" class="form-control data-api-link" id="data_api_link"
                    v-model="fighter.data_api_link" placeholder="Data Api Link" />
                </div>
              </div>

              <div class="row">
                <button class="btn btn-secondary my-2 w-auto" style="margin-left: auto; margin-right: 1rem" type="button"
                  @click="visible = !visible">
                  Close
                </button>
                <button class="btn btn-primary my-2 w-auto" style="margin-right: 1rem" type="submit">
                  Save Changes
                </button>
              </div>
            </form>
            
            <div class="error-message px-1" v-if="createFighterError">
              <p>Fighter not created, check server logs.</p>
            </div>
          </div>
      </div>
    </Transition>
</template>

<style lang="scss">

.modal-background{
    position: absolute;

    left: 0px;
    top: 0px;
    width: 100vw;
    height: 100vh;    
    z-index: 99999;

    background: rgba(0, 0, 0, 0.7);

    display:flex;
    justify-content: center;
    align-items: center;

    .fighter-creator{
        // position: relative;
        z-index: 100000;
        background-color: rgb(33, 37, 41);
        form{    
            display: flex;
            flex-direction: column;
            row-gap: 0.4rem;
        }
    }
}

.v-enter-active,
.v-leave-active {

  transition: opacity 0.3s ease;
  
  .fighter-creator {
    transition: transform 0.2s ease;
    transform: translateY(0%);
  }

}

.v-enter-from,
.v-leave-to {
  opacity: 0;

  .fighter-creator{
    transform: translateY(-25%);
  }
}

.error-message{
  color: orangered;
}


</style>
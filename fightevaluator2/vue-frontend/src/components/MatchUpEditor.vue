<script setup>

function commitChanges(){

}

</script>
<template>
    <div class="matchup-editor border rounded-2" data-event-id="118">
          <h1 class="modal-title title fs-4">Create MatchUp</h1>
          <form>
              <div class="search-box2">
                <div class="input-group">  
                  <label class="input-group-text" for="fighter-a-input">Fighter A</label>
                  
                  <div class="input-wrapper">
                    <input class="form-control rounded-0" data-fighter-id="-1" type="text" value="" name="fighter-a" id="fighter-a-input" placeholder="Enter fighter name..."> 
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
                    <input class="form-control rounded-0" data-fighter-id="-1" type="text" value="" name="fighter-b" id="fighter-b-input" placeholder="Enter fighter name..."> 
                    <ul class="suggestion-box list-group"></ul>
                  </div>
                  
                  <button class="btn btn-outline-danger clear-btn" type="button" id="button-addon2">Clear</button>
                </div>
              </div>

              <!--weight class-->
              <div class="weightclass-selector my-4">
                <div class="weightclass input-group mb-3">
                  <label class="input-group-text" for="weight-class-select">Weightclass</label>
                  <select class="form-select" id="weight-class-select" name="weight_class">
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
                    <input class="form-check-input" type="radio" name="rounds" value="3" id="rounds-radio-3" checked="">
                    <label class="form-check-label" for="rounds-radio-3">
                      3
                    </label>
                  </div>
                  <div class="form-check">
                    <input class="form-check-input" type="radio" name="rounds" value="5" id="rounds-radio-5">
                    <label class="form-check-label" for="rounds-radio-5">
                      5
                    </label>
                  </div>
                </div>
                <!--prelim status-->
                <div class="isprelim-checkbox border rounded-2 p-1 px-3">
                  <div class="form-check">
                    <input class="form-check-input" type="checkbox" value="" name="isprelim" id="isprelim-checkbox" checked="">
                    <label class="form-check-label" for="isprelim-checkbox">
                      on prelims
                    </label>
                  </div>
                </div>
              </div>
          </form>
          <div class="editor-actions mt-3">
              <button type="button" class="btn btn-secondary mx-2 close-btn" v-on:click="hideMatchUpEditor()">Close</button>
              <button type="button" class="btn btn-primary create-btn current-action submit-btn" v-on:click="commitChanges(true)">Create</button>
              <button type="button" class="btn btn-primary save-btn submit-btn" v-on:click="commitChanges(false)">Save</button>
          </div>
    </div>
</template>

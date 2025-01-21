class MatchUpEditor{
      
    static EVENTS = {
      CREATE_MATCHUP : 'CREATE_MATCHUP',
      UPDATE_MATCHUP:'UPDATE_MATCHUP',
    }

    constructor(editor,server){
      this.editor = editor;//html element that contains all inputs
      this.eventId = this.editor.dataset.eventId;
      this.server = server;
      
      this.title = this.editor.querySelector(".title");
      const [searchBoxElem0,searchBoxElem1] = this.editor.querySelectorAll(".search-box2");
      
      //search box controllers
      this.searchBoxA = new FighterSearchBox(searchBoxElem0);
      this.searchBoxB = new FighterSearchBox(searchBoxElem1);
      this.weightClassSelector = this.editor.querySelector(".weightclass-selector select");
      this.createButton = this.editor.querySelector('.create-btn');
      this.saveButton = this.editor.querySelector('.save-btn');


      this.listeners = {}
      //list of elements listening for changes
      for (const eventName in MatchUpEditor.EVENTS){
        this.listeners[eventName] = [];
      }
      this.inEditMode = false;
    }

    loadMatchUp(matchup){
      this.inEditMode = true;
      //change editor title
      this.title.textContent = "Edit MatchUp";
      this.createButton.classList.remove('current-action');
      this.saveButton.classList.add('current-action');
      this.matchupId = matchup.id;
      //set input values
      this.searchBoxA.setSearchBoxValue({
        name:matchup.fighter_a_name,
        id:matchup.fighter_a,
      });
      this.searchBoxB.setSearchBoxValue({
        name:matchup.fighter_b_name,
        id:matchup.fighter_b,
      });
      //how to set rounds of radio group?
      this.editor.querySelectorAll('[name="rounds"]').forEach((element) => {
          element.checked=false;
      });
      this.editor.querySelector(`#rounds-radio-${matchup.rounds}`).checked = true;
      this.editor.querySelector('[name="isprelim"]').checked=matchup.isprelim;
      this.weightClassSelector.value= matchup.weight_class;
    }

    onMatchUpCreated(data){
      this.dispatchEventsOnListeners(MatchUpEditor.EVENTS.CREATE_MATCHUP,data);
    }

    dispatchEventsOnListeners(eventName,data){
      const event = new CustomEvent(eventName,{detail:{data : data}});
      for (const listener of this.listeners[eventName]){
        listener.dispatchEvent(event);
      }
    }

    async commitChanges(createNew){
      //grab changed input values
      let fighterA = this.searchBoxA.fighterId;
      let fighterB = this.searchBoxB.fighterId;
      
      // console.log(fighterA,fighterB);
      if (fighterA == -1 || fighterB == -1){
        alert('Please select 2 fighters');
        return;//nothing happens need to select 2 fighters
      }

      let formData = new FormData(this.editor.querySelector('form'));
      if (formData.get('weight_class') == ""){
        alert('Please select weight class.');
        return;//need weight_class
      }
      //no is prelim key means main card
      formData.set('isprelim',formData.has('isprelim'));
      formData.set('fighter_a_id',fighterA);
      formData.set('fighter_b_id',fighterB);
      // formData.set('event_id',this.eventId);
      const requestData = {};
      for (const key of formData.keys()){
        // console.log(key,formData.get(key));
        requestData[key] = formData.get(key);
      }
      //send to server 
      requestData['event_id']=this.eventId;
      //process result
      console.log(requestData);
      if (createNew){
        this.server.create_matchup(requestData,this.onMatchUpCreated.bind(this));
      }else{
        this.server.update_matchup(requestData,this.onMatchUpChangesSaved.bind(this),this.matchupId);
      }
    }

    onMatchUpChangesSaved(data){
      this.dispatchEventsOnListeners(MatchUpEditor.EVENTS.UPDATE_MATCHUP);
      console.log('server => ',data);
    }

    clearEditor(){
      //clear searchbox's
      this.searchBoxA.clearSearchBox();
      this.searchBoxB.clearSearchBox();
      //change weightclass to nothing
      this.weightClassSelector.value="";
      this.title.textContent= "Create MatchUp";//default title
      
      this.createButton.classList.add('current-action');
      this.saveButton.classList.remove('current-action');
    }

    registerListener(element,eventName,callback){
      if (eventName in MatchUpEditor.EVENTS){
        element.addEventListener(MatchUpEditor.EVENTS[eventName],callback);
        this.listeners[eventName].push(element);
      }
    }
    
  }
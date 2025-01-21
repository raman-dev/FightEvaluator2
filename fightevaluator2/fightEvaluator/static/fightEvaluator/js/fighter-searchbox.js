class FighterSearchBox{
      
    constructor(searchBox){
      this.searchBox = searchBox;
      this.input = searchBox.querySelector('input');//the input element of the searchbox
      this.suggestionList = searchBox.querySelector('ul');//the suggestion list
      this.searchBox.addEventListener("keyup", this.onKeyUp.bind(this));
      this.searchBox.querySelector('.clear-btn').addEventListener('click',this.clearSearchBox.bind(this));
    }

    async onKeyUp() {
      let input = this.searchBox.querySelector("input");
      let search = this.input.value;
      search = search.split(" ").join("+");
      //non-empty search string
      if (search.length > 0) {
        server.search_fighters(this.onFighterSearchResult.bind(this),search);
      } 
      else {
        this.suggestionList.innerHTML = "";//empty the list
      }
    }

    onFighterSearchResult(data){
      let fighters = data['fighters'];
      this.suggestionList.innerHTML = "";//list must always be emptied before populating with new values
      for (const fighter of fighters){
        let item = FighterSearchBox.createSuggestionListElement(fighter);
        item.addEventListener("click",this.onSuggestionListItemClick.bind(this,item));
        this.suggestionList.appendChild(item);
      }
    }

    onSuggestionListItemClick(suggestion,event){
      //populate input with this value
      this.input.dataset.fighterId = suggestion.dataset.fighterId;
      this.input.value = suggestion.dataset.fighterName;//fighter name string
      //list needs to be empty now
      this.suggestionList.innerHTML = "";
      this.input.toggleAttribute('disabled',true);//
    }

    clearSearchBox(){
      //clear suggestion
      this.input.dataset.fighterId =-1;
      this.input.value = "";
      this.input.toggleAttribute('disabled',false);
      //
      this.suggestionList.innerHTML="";
    }

    get fighterId(){
      return this.input.dataset.fighterId;
    }

    setSearchBoxValue(fighter){
      console.log('searchBoxValue.set=>',fighter);
      this.input.value = fighter.name;
      this.input.dataset.fighterId = fighter.id;
      this.input.setAttribute('disabled',true);
    }

    static createSuggestionListElement(fighter){
      return $(`
        <li class="list-group-item list-group-item-action" data-fighter-id="${fighter.id}" data-fighter-name="${fighter.first_name} ${fighter.last_name}">
          <div class="suggestion">
            <p class="name">${fighter.first_name} ${fighter.last_name}</p>
          </div>
        </li>`)[0];
    }
  }
 let xmodal = document.querySelector(".xmodal");
    // xmodal on click hide
    xmodal.addEventListener("click", (event) => {
      if (event.target == event.currentTarget){
        toggleXModal();
      }
    });
    function toggleXModal(){
      let xmodal = document.querySelector(".xmodal");
      let action = xmodal.classList.contains("hide") ? "show" : "hide";
      //these variables are defined only when showing the modal
      let matchupId = this.matchupId;//guaranteed to be there when showing
      let inWatchList = watchListItems.includes(matchupId);
      // console.log(matchup);
      if (action == "show"){
        //show the modal
        xmodal.classList.remove("hide");
        xmodal.classList.add("show");
        xmodal.dataset.matchupId = matchupId;
        //populate the modal with this matchup's data
        //extract matchup id from matchup
        //set the link href to /matchup/matchupId
        let watchButton = xmodal.querySelector("button.watch");
        xmodal.querySelector(".analyze").href = `/matchup/${matchupId}`;
        if (inWatchList){
          watchButton.textContent = "unwatch";
        }else{
          watchButton.textContent = "watch";
        }
      } else {
        //hide the modal
        xmodal.classList.remove("show");
        xmodal.classList.add("hide");
        xmodal.dataset.matchupId = "-1";
        //deactivate the matchup
        let activeMatchup = document.querySelector(".matchup.active");
        if (activeMatchup != null) activeMatchup.classList.remove("active");
      }
      
    }
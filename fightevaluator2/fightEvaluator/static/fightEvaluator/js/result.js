let resultBtn = document.querySelector('.reveal-result-btn');
/*


    result:{
       method : 'KO/TKO',
       final_round': 2,
       time : '3:32',
       winner_id : 3311
       total_rounds: 5
    }


    query which events are present 

    for every outcome card get the event type and fighterId if present event is fighterSpecific
    determine if the event occurred or not given the result object



*/

function checkEventOccurred(eventType, fighterId, resultData){
    if (fighterId != 0){
        //fighter specific event
        //right now only supporting win events 
        if (resultData.winner_id == fighterId){
            return true;
        }
        return false;
    }
    //non fighter specific event
    //form of rounds event -> ROUNDS_GEQ_NUMBER_AND_HALF 
    //check if eventType starts with ROUNDS_GEQ
    if (eventType == 'ROUNDS_GEQ_ONE_AND_HALF'){
        if (resultData.final_round > 2){
            return true;
        }
        let [minutes,seconds] = resultData.time.split(':');
        minutes = parseInt(minutes);
        seconds = parseInt(seconds);
        console.log(minutes,seconds);
        if (minutes > 2 || (minutes == 2 && seconds >= 30)){
            return true;
        }
        return false;
    }
    if (eventType == 'DOES_NOT_GO_THE_DISTANCE'){
        if (resultData.time != '15:00' && resultData.time != '25:00'){
            return true;
        }
        return false;
    }
}

resultBtn.addEventListener('click', (event) => {
    document.querySelectorAll('.outcome').forEach((outcome) => {
        let eventType = outcome.dataset.eventType;
        let fighterId = outcome.dataset.fighterId;
        
        let occurred = checkEventOccurred(eventType, fighterId,result);
        //check if has fighter-id attribute
        if (occurred){
            outcome.classList.add('occurred');
        }else{
            outcome.classList.add('not-occurred');
        }
    });
    
    if (result.winner_id != -1){
        document.querySelectorAll('.fighter-info').forEach((fighterInfo) => {
            if (fighterInfo.dataset.fighterId == result.winner_id){
                fighterInfo.classList.add('win');
                let fightResultLabel = fighterInfo.querySelector('.fight-result-label');
                fightResultLabel.classList.remove('d-none');
                fightResultLabel.innerHTML = `${result.method} at ${result.time} Round ${result.final_round} of ${result.total_rounds} `;
            }else{
                fighterInfo.classList.add('lose');  
            }
        });
    }
});
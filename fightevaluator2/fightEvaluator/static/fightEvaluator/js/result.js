let resultBtn = document.querySelector('.reveal-result-btn');
resultBtn.addEventListener('click', (event) => {
    let oneAndHalfCompleted = false;
    let winner_id = -1;
    let fightDidNotGoDistance = false;

    winner_id = result.winner_id;
    if (result.final_round > 2) {
        oneAndHalfCompleted = true;
    }
    if(result.final_round == 2){
        //check stop time of round 2 
        //extract minutes and seconds 
        let [minutes,seconds] = result.rounds[1].stop_time.split(':');
        minutes = parseInt(minutes);
        seconds = parseInt(seconds);
        if (minutes >= 2 && seconds >= 30){
            oneAndHalfCompleted = true;
        }
    }
    if (result.time != '15:00' && result.time != '25:00'){
        fightDidNotGoDistance = true;
    }
    if (oneAndHalfCompleted){
        console.log('one and half completed');
    }
    if (fightDidNotGoDistance){
        console.log('fight did not go distance');
    }

});
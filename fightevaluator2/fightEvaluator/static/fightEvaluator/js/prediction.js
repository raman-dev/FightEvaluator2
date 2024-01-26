let predictionSelector = document.querySelector('.prediction-selector');
let select = document.querySelector('.prediction-selector select');
let savePredictionBtn = document.querySelector('.save-prediction-btn');
let saveResultBtn = document.querySelector('.save-result-btn');
savePredictionBtn.addEventListener('click',onClickSavePredictionBtn);

const DEFAULT_OUTCOME_ID = 0;
const DEFAULT_LIKELIHOOD = 0;
const DEFAULT_LIKELIHOOD_LABEL = "Likelihood";

if (matchupOutcomePredictionId != 0){
    setLikelhoodDisplay(
        matchupOutcomePredictionId,
        outcomeMap[matchupOutcomePredictionId].likelihood,
        outcomeMap[matchupOutcomePredictionId].likelihood_display
    );

    select.value = matchupOutcomePredictionId;
}

function setLikelhoodDisplay(outcomeId,likelihoodValue, likelihoodLabel){
    let predictionLikelihoodWrapper = predictionSelector.querySelector('.current-likelihood');
    let predictionLikelihoodText = predictionSelector.querySelector('.prediction-likelihood-text');

    predictionLikelihoodText.classList.remove(`likely-${predictionLikelihoodWrapper.dataset.likelihood}`);
    
    predictionLikelihoodWrapper.dataset.likelihood = likelihoodValue;
    predictionLikelihoodText.textContent = likelihoodLabel;

    predictionLikelihoodText.classList.add(`likely-${likelihoodValue}`);
    predictionSelector.dataset.outcomePredictionId = outcomeId;
}

select.addEventListener('change',(event)=>{
    let outcomeId = parseInt(event.target.value);
    let valueChanged = matchupOutcomePredictionId != outcomeId;
    if (outcomeId == 0){
        setLikelhoodDisplay(DEFAULT_OUTCOME_ID,DEFAULT_LIKELIHOOD,DEFAULT_LIKELIHOOD_LABEL);
        if (valueChanged){
            savePredictionBtn.classList.remove('disabled');
        }else if (!savePredictionBtn.classList.contains('disabled')){
            savePredictionBtn.classList.add('disabled');
        }
        return;
    }

    let outcomeData = outcomeMap[outcomeId];
    setLikelhoodDisplay(outcomeId,outcomeData.likelihood, outcomeData.likelihood_display);
    if (valueChanged){
        savePredictionBtn.classList.remove('disabled');
    }else if (!savePredictionBtn.classList.contains('disabled')){
            savePredictionBtn.classList.add('disabled');
    }
});

async function onClickSavePredictionBtn(event) {
    let outcomePredictionId = predictionSelector.dataset.outcomePredictionId;
    let response = await fetch(`/matchup/update-prediction/${matchupId}/${outcomePredictionId}`, {
        method: "PATCH",
        headers: {
          accept: "application/json",
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        }
    });
    if (response.status == 200){
        let output =  await response.json();
        // console.log(output);
        for (let key in outcomeMap){
            outcomeMap[key].is_prediction = false;
        }
        if (output.outcomeId != 0){
            outcomeMap[output.outcomeId].is_prediction = true;
        }
    }
    savePredictionBtn.classList.add('disabled');
}
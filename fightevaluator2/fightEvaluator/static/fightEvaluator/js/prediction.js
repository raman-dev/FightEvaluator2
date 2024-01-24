let predictionSelector = document.querySelector('.prediction-selector');
let select = document.querySelector('.prediction-selector select');

function setLikelhoodDisplay(likelihoodValue, likelihoodLabel){
    let predictionLikelihoodWrapper = predictionSelector.querySelector('.current-likelihood');
    let predictionLikelihoodText = predictionSelector.querySelector('.prediction-likelihood-text');

    predictionLikelihoodText.classList.remove(`likely-${predictionLikelihoodWrapper.dataset.likelihood}`);
    
    predictionLikelihoodWrapper.dataset.likelihood = likelihoodValue;
    predictionLikelihoodText.textContent = likelihoodLabel;

    predictionLikelihoodText.classList.add(`likely-${likelihoodValue}`);
}

select.addEventListener('change',(event)=>{

    let outcomeId = event.target.value;
    if (outcomeId == "null"){
        setLikelhoodDisplay(0, "Likelihood");
        return;
    }

    // let outcomeObject = document.querySelector(`[data-id="${outcomeId}"]`);
    let outcomeData = outcomeMap[outcomeId];
    setLikelhoodDisplay(outcomeData.likelihood, outcomeData.likelihood_display);
    
});
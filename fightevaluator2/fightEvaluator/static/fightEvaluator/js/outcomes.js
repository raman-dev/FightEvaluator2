
async function updateEventLikelihood(){
    console.log(this.eventElement);
    let eventType = this.eventElement.dataset.eventType;
    let fighterId = this.eventElement.dataset.fighterId;
    let data = checkHasDataMappingElseCreate(eventType,fighterId);

    let newLikelihood = this.eventElement.querySelector('.current-confidence').dataset.likelihood;
    let saveOutcomeBtn = this.eventElement.querySelector('.save-outcome-btn');
    let newJustification = this.eventElement.querySelector('.justification .editor-wrapper .editor').textContent

    input_data = {
        "matchupId": matchupId, 
        "eventId": data.id,
        "eventType": eventType,
        "fighterId": parseInt(fighterId),
        "likelihood": newLikelihood,
        "justification": newJustification,
    };

    // console.log(input_data);
    let response = await fetch(`/matchup/update-event-likelihood/`, {
        method: "PUT",
        headers: {
          accept: "application/json",
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
        body: JSON.stringify(input_data),
    });
    if (response.status == 200){
        let output =  await response.json();
        // console.log(output);
        //update outcome likelihood
        data.id = output.id;
        data.likelihood = output.likelihood;
        data.justification = output.justification;
        data.likelihood_display = output.likelihood_display;
        //disable save button
        saveOutcomeBtn.classList.add('disabled');
        //collapse confidence list
        toggleConfidenceList(false,this.eventElement.querySelector('.confidence-list'));
    }
}


function toggleConfidenceList(expandList,confidenceList){
    if (expandList){
        //if confidenceList is collapsed, expand it
        confidenceList.classList.add('expanded');
        confidenceList.style.height = `${confidenceList.scrollHeight}px`;
    }else{
        //if confidenceList is expanded, collapse it
        confidenceList.classList.remove('expanded');
        confidenceList.style.height = '0px';
    }
}


function toggleJustification(expandJustification,justificationEditor){
    if (expandJustification){
        //if justificationEditor is collapsed, expand it
        justificationEditor.classList.add('expanded');
        justificationEditor.style.height = `${justificationEditor.scrollHeight}px`;
    }else{
        //if justificationEditor is expanded, collapse it
        justificationEditor.classList.remove('expanded');
        justificationEditor.style.height = '0px';
    }
}


//Write Fighter last names for standard event win
document.querySelectorAll('.event').forEach((eventElement) => {
    let eventType = eventElement.dataset.eventType;
    let fighterId = eventElement.dataset.fighterId;
    let data = checkHasDataMappingElseCreate(eventType,parseInt(fighterId));
    // console.log(data);
    let confidenceSelector= eventElement.querySelector('.confidence-selector');
    let showConfidenceListBtn = confidenceSelector.querySelector('.show-confidence-list-btn');
    // console.log(showConfidenceListBtn);

    let justifactionEditorWrapper = eventElement.querySelector( '.justification .editor-wrapper');
    let justifactionEditor = justifactionEditorWrapper.querySelector('.editor');

    let confidenceList = confidenceSelector.querySelector('.confidence-list');
    let currentConfidence = confidenceSelector.querySelector('.current-confidence');
    let confidenceTextElement = currentConfidence.querySelector('p');

    let saveOutcomeBtn = eventElement.querySelector('.save-outcome-btn');
    

    confidenceList.querySelectorAll('li').forEach(li => {
        li.addEventListener('click', (event) => {
            let listItem = event.currentTarget;
            let likelhoodTextElement = listItem.querySelector('.likelihood');
            let likelihood = listItem.dataset.likelihood;
            //clicked same confidence no change
            if (listItem.classList.contains('active')) {
                return;
            }
            //clicked different confidence
            let oldConfidence = confidenceList.querySelector('.active');
            let oldLikelihood = currentConfidence.dataset.likelihood;

            oldConfidence.classList.remove('active');
            listItem.classList.add('active');
            
            confidenceTextElement.textContent = likelhoodTextElement.textContent;
            confidenceTextElement.classList.remove(`likely-${oldLikelihood}`);
            confidenceTextElement.classList.add(`likely-${likelihood}`); 
            
            currentConfidence.dataset.likelihood = likelihood;
            //enable save button iff active confidence is different to outcome.dataset.likelihood
            if (currentConfidence.dataset.likelihood != data.likelihood){
                //enable save button
                saveOutcomeBtn.classList.remove('disabled');
            }else{
                //disable save button
                if (!saveOutcomeBtn.classList.contains('disabled')){
                    saveOutcomeBtn.classList.add('disabled');
                }
            }
        });
    });

    showConfidenceListBtn.addEventListener('click', () => {
        //check if confidenceList is expanded
        let isOpen = confidenceList.classList.contains('expanded');
        toggleConfidenceList(!isOpen,confidenceList);
    });

    justifactionEditor.addEventListener('input', (event) => {
        /*
            
            map {
                eventType :{
                    if fighter specific
                    fighterId0 : {
                    }
                    fighterId1 : {
                    }
                    ....
                }

                eventType:{
                    likelihood: 3,
                    likelihood_display: "Likely",
                    justification: "..."
                }
            }
        
        */
        //check if data mapping exists for eventType
        //check if data.justification is different to written data in html
        let justification = event.currentTarget.textContent.trim();
        if (data.justification != justification){
            //enable save button
            saveOutcomeBtn.classList.remove('disabled');
        }else{
            //disable save button
            if (!saveOutcomeBtn.classList.contains('disabled')){
                saveOutcomeBtn.classList.add('disabled');
            }
        }
    });
    //get data from event likelihood
    //populate the html with the data from eventLikelihood
    renderEventLikelihood(eventElement,data);
    saveOutcomeBtn.addEventListener('click',updateEventLikelihood.bind({eventElement:eventElement}));
});

function defaultLikelihood(){
    return {
        likelihood: 3,
        likelihood_display: "Neutral",
        justification: "Justification Statements and Conclusions",
        id : 0,//default id
    }
}

function checkHasDataMappingElseCreate(eventType,fighterId){
    //event doesn't exist in eventLikelihoodMap
    // console.log(eventType,fighterId,eventLikelihoodMap);
    if (eventType in eventLikelihoodMap == false){
        //fighter specific eventType
        // console.log(eventType,'not in eventLikelihoodMap');
        if (fighterId != 0){
            // console.log(fighterId,'not in eventLikelihoodMap');
            eventLikelihoodMap[eventType] = {};
            eventLikelihoodMap[eventType][fighterId] = defaultLikelihood();
            return eventLikelihoodMap[eventType][fighterId];
        }
        eventLikelihoodMap[eventType] = defaultLikelihood();
        return eventLikelihoodMap[eventType];
    }
    if (fighterId != 0){
        // console.log('fighterSpecific');
        if (fighterId in eventLikelihoodMap[eventType] == false){
            // console.log('making New!');
            eventLikelihoodMap[eventType][fighterId] = defaultLikelihood();
        }
        return eventLikelihoodMap[eventType][fighterId];
    }
    return eventLikelihoodMap[eventType];
}

function renderEventLikelihood(event,data){
    //check if eventType exists
    // console.log(event,data);
    //populate the html with the data from eventLikelihood
    event.querySelector(`.editor-wrapper .editor`).textContent = data.justification;
    event.dataset.likelihood = data.likelihood;

    let confidenceSelector= event.querySelector('.confidence-selector');
    let confidenceList = confidenceSelector.querySelector('.confidence-list');
    let confidenceTextContainer = confidenceSelector.querySelector('.current-confidence');
    let confidenceTextElement = confidenceTextContainer.querySelector('p.confidence');
    
    confidenceTextContainer.dataset.likelihood = data.likelihood;
    confidenceTextElement.textContent = data.likelihood_display;
    //remove default confidence class
    confidenceTextElement.classList.remove('likely-3');
    //add confidence class
    confidenceTextElement.classList.add(`likely-${data.likelihood}`);
    //remove default active list element
    confidenceList.querySelector('.active').classList.remove('active');
    //make active list element with correct likelihood
    confidenceList.querySelector(`[data-likelihood='${data.likelihood}']`).classList.add('active');
}



let predictionSelector = document.querySelector('.prediction-selector');
let select = document.querySelector('.prediction-selector select');
let savePredictionBtn = document.querySelector('.save-prediction-btn');
savePredictionBtn.addEventListener('click',onClickSavePredictionBtn);

const DEFAULT_OUTCOME_ID = 0;
const DEFAULT_LIKELIHOOD = 0;
const DEFAULT_LIKELIHOOD_LABEL = "Likelihood";
const DEFAULT_PREDICTION_TYPE = 'NA';
const DEFAULT_FIGHTER_ID = 0;
const DEFAULT_PREDICTION_DATA = {'likelihood': 0,'likelihood_display': 'Likelihood','id': 0};

if (prediction.eventType != 'NA'){
    console.log('prediction => ',prediction);
    let data = checkHasDataMappingElseCreate(prediction.eventType,parseInt(prediction.fighterId));
    console.log('showing prediction!',data);
    setLikelhoodDisplay2(data,prediction.eventType,prediction.fighterId);
    let selectOption = select.querySelector(`option[data-fighter-id="${prediction.fighterId}"][data-event-type="${prediction.eventType}"]`);
    // console.log(selectOption);
    let oldOption = select.querySelector('option[selected]');
    oldOption.selected = false;//old option
    oldOption.removeAttribute('selected');

    select.value = selectOption.value;
    selectOption.selected = true;
    selectOption.setAttribute('selected','');
}

function setLikelhoodDisplay2(data,eventType,fighterId){
    
    if (eventType == DEFAULT_PREDICTION_TYPE){
        data.likelihood = 0;
        data.likelihood_display = 'Likelihood';
    }
    // console.log(DEFAULT_PREDICTION_TYPE,eventType,fighterId);
    // console.log(data);
    let predictionLikelihoodWrapper = predictionSelector.querySelector('.current-likelihood');
    let predictionLikelihoodText = predictionSelector.querySelector('.prediction-likelihood-text');

    predictionLikelihoodText.classList.remove(`likely-${predictionLikelihoodWrapper.dataset.likelihood}`);
    
    predictionLikelihoodWrapper.dataset.likelihood = data.likelihood;
    predictionLikelihoodText.textContent = data.likelihood_display;

    predictionLikelihoodText.classList.add(`likely-${data.likelihood}`);
    predictionSelector.dataset.prediction = eventType;
    predictionSelector.dataset.fighterId = fighterId;   

}

select.addEventListener('change',(event)=>{
    // console.log(event.target,event);
    // console.log(event.target.options,event.target.selectedIndex);
    let oldOption = select.querySelector(`option[selected]`);
    // console.log(oldOption);
    oldOption.selected = false;
    oldOption.removeAttribute('selected');
    // console.log('select change event triggered');
    let option = event.target.options[event.target.selectedIndex];
    option.selected = true;
    option.setAttribute('selected','');
    let eventType = option.value;
    let fighterId = option.dataset.fighterId;
    
    let valueChanged = eventType != prediction.eventType;
    if (eventType == prediction.eventType && fighterId != prediction.fighterId){
        valueChanged = true;
    }
    console.log(eventType,fighterId,'valueChanged => '+ valueChanged);
    if (eventType == 'NA'){
        setLikelhoodDisplay2(DEFAULT_PREDICTION_DATA,DEFAULT_PREDICTION_TYPE,DEFAULT_FIGHTER_ID);
        if (valueChanged){
            savePredictionBtn.classList.remove('disabled');
        }else if (!savePredictionBtn.classList.contains('disabled')){
            savePredictionBtn.classList.add('disabled');
        }
        return;
    }

    // let outcomeData = outcomeMap[outcomeId];
    let data = checkHasDataMappingElseCreate(eventType,fighterId);
    console.log(data);
    setLikelhoodDisplay2(data,eventType,fighterId);
    if (valueChanged){
        savePredictionBtn.classList.remove('disabled');
    }else if (!savePredictionBtn.classList.contains('disabled')){
            savePredictionBtn.classList.add('disabled');
    }
});

async function onClickSavePredictionBtn(event) {

    let predictionEventType = predictionSelector.dataset.prediction;
    let predictionFighterId = predictionSelector.dataset.fighterId;

    let response = await fetch(`/matchup/update-event-prediction/`, {
        method: "PUT",
        headers: {
          accept: "application/json",
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
        body: JSON.stringify({
            "matchupId": matchupId, 
            "eventType": predictionEventType,
            "fighterId": parseInt(predictionFighterId),
        }),
    });
    
    let output =  await response.json();
    if (response.status == 200){

        prediction.eventType = output.eventType;
        prediction.fighterId = output.fighterId;
    }else{
        console.log('error',output);
    }
    savePredictionBtn.classList.add('disabled');
}
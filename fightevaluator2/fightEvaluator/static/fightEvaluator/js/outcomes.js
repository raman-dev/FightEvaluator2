//on click show confidence-list-btn expand confidence-list
//for every show-confidence-list-btn 
//add click event listener
async function updateLikelihood(){
    let outcome_id = this.outcome.dataset.id;
    let newLikelihood = this.outcome.querySelector('.current-confidence').dataset.likelihood;
    let saveOutcomeBtn = this.outcome.querySelector('.save-outcome-btn');
    let newJustification = this.outcome.querySelector('.justification .editor-wrapper .editor').textContent

    input_data = {
        "likelihood": newLikelihood,
        "justification": newJustification,
    };

    let response = await fetch(`/matchup/update-outcome/${outcome_id}`, {
        method: "PATCH",
        headers: {
          accept: "application/json",
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
        body: JSON.stringify(input_data),
    });
    if (response.status == 200){
        let output =  await response.json();
        console.log(output);
        //update outcome likelihood
        this.outcome.dataset.likelihood = output.likelhood;
        //disable save button
        this.outcome.querySelector('.justification .editor-wrapper .editor').textContent = output.justification;
        outcomeMap[outcome_id].justification = output.justification;
        outcomeMap[outcome_id].likelihood = output.likelihood;
        outcomeMap[outcome_id].likelihood_display = output.likelihood_display;
        console.log(outcomeMap);
        saveOutcomeBtn.classList.add('disabled');//disable save button
        toggleConfidenceList(false,this.outcome.querySelector('.confidence-list'));
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

//for every key value in a dictionary 
//add key value pair to FormData
for (const [key, data] of Object.entries(outcomeMap)) {
    document.querySelector(`[data-id='${key}'] .editor-wrapper .editor`).textContent = data.justification;
}

document.querySelectorAll('.outcome').forEach(outcome => {
    let confidenceSelector= outcome.querySelector('.confidence-selector');
    
    let showConfidenceListBtn = confidenceSelector.querySelector('.show-confidence-list-btn');
    let showJustifactionBtn = outcome.querySelector('.show-justification-btn');

    let justifactionEditorWrapper = outcome.querySelector('.justification .editor-wrapper');
    let justifactionEditor = justifactionEditorWrapper.querySelector('.editor');

    let confidenceList = confidenceSelector.querySelector('.confidence-list');
    let currentConfidence = confidenceSelector.querySelector('.current-confidence');
    let confidenceTextElement = currentConfidence.querySelector('p');

    let saveOutcomeBtn = outcome.querySelector('.save-outcome-btn');
    //add click event listener to list items of confidenceList
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
            if (currentConfidence.dataset.likelihood != outcome.dataset.likelihood){
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

    showConfidenceListBtn.addEventListener('click', (event) => {
        //check if confidenceList is expanded
        let isOpen = confidenceList.classList.contains('expanded');
        toggleJustification(!isOpen,confidenceList);
    });

    justifactionEditor.addEventListener('input', (event) => {
        let justification = event.currentTarget.textContent.trim();
        //enable save button iff justification is different to outcome.dataset.justification
        if (justification != outcome.dataset.justification){
            //enable save button
            saveOutcomeBtn.classList.remove('disabled');
        }else{
            //disable save button
            if (!saveOutcomeBtn.classList.contains('disabled')){
                saveOutcomeBtn.classList.add('disabled');
            }
        }
    });

    // showJustifactionBtn.addEventListener('click', (event) => {
    //     let isOpen = justifactionEditorWrapper.classList.contains('expanded');
    //     toggleJustification(!isOpen,justifactionEditorWrapper);
    // });

    saveOutcomeBtn.addEventListener('click',updateLikelihood.bind({outcome:outcome}));
});

//Write Fighter last names for standard event win
document.querySelectorAll('.event').forEach((eventElement) => {
    let eventType = eventElement.dataset.eventType;
    let confidenceSelector= eventElement.querySelector('.confidence-selector');
    
    let showConfidenceListBtn = confidenceSelector.querySelector('.show-confidence-list-btn');

    let justifactionEditorWrapper = eventElement.querySelector('.justification .editor-wrapper');
    let justifactionEditor = justifactionEditorWrapper.querySelector('.editor');

    let confidenceList = confidenceSelector.querySelector('.confidence-list');
    let currentConfidence = confidenceSelector.querySelector('.current-confidence');
    let confidenceTextElement = currentConfidence.querySelector('p');

    let saveOutcomeBtn = eventElement.querySelector('.save-outcome-btn');

    showConfidenceListBtn.addEventListener('click', () => {
        //check if confidenceList is expanded
        let isOpen = confidenceList.classList.contains('expanded');
        toggleJustification(!isOpen,confidenceList);
    });

    justifactionEditor.addEventListener('input', (event) => {
        let justification = event.currentTarget.textContent.trim();
        //enable save button iff justification is different to outcome.dataset.justification
        if (justification != outcome.dataset.justification){
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
    renderEventLikelihood(eventElement,eventType);
});

function renderEventLikelihood(event,eventType){
    //check if eventType exists
    if (!eventType in eventLikelihoodMap){
        return;
    }
    let data = eventLikelihoodMap[eventType];
    let fighterId = event.dataset.fighterId;
    //fighter specific event
    if (eventType == 'WIN'){
        data = data[fighterId];
    }
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

// async function getOutcomes(){
//     //fetch all outcomes from the api /matchup/get-outcomes-list
//     let response = await fetch('/matchup/get-outcomes-list',{
//         method: "GET",
//         headers: {
//         accept: "application/json",
//         "Content-Type": "application/json",
//         "X-CSRFToken": Cookies.get("csrftoken"),
//         },
//     });
//     if (response.status == 200){
//         let output =  await response.json();
//         // console.log(output);
//     }
// }

// getOutcomes();
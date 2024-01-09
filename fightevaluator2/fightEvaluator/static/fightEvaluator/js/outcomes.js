//on click show confidence-list-btn expand confidence-list
//for every show-confidence-list-btn 
//add click event listener
async function updateLikelihood(){
    let outcome_id = this.outcome.dataset.id;
    let newLikelihood = this.outcome.querySelector('.current-confidence').dataset.likelihood;
    let saveOutcomeBtn = this.outcome.querySelector('.save-outcome-btn');

    input_data = {
        "likelihood": newLikelihood,
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
        // console.log(output);
        //update outcome likelihood
        this.outcome.dataset.likelihood = output.likelhood;
        //disable save button
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

document.querySelectorAll('.outcome').forEach(outcome => {
    let confidenceSelector= outcome.querySelector('.confidence-selector');
    let showConfidenceListBtn = confidenceSelector.querySelector('.show-confidence-list-btn');
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
        if (isOpen) {
            toggleConfidenceList(false,confidenceList);
        } else {
            toggleConfidenceList(true,confidenceList);
        }
    });

    saveOutcomeBtn.addEventListener('click',updateLikelihood.bind({outcome:outcome}));
});
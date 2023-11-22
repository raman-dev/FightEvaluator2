//on click attrib-edit-button show card body
const attribCardSelector = '.attrib-card';
const attribEditButtonSelector = '.attrib-edit-button';
const attribCommitButtonSelector = '.attrib-commit-button';

function attribEditButtonClickListener(event){
    let attribCard = this.attribCard;
    let cardBody = attribCard.querySelector('.card-body');
    let scrollHeight = cardBody.scrollHeight;
    //toggle edit mode      gets previous edit mode then flips it
    let editModeEnabled = !(attribCard.getAttribute('data-edit-mode-enabled') == 'true');
    attribCard.setAttribute('data-edit-mode-enabled',editModeEnabled);
    if (editModeEnabled){
        //show card body
        cardBody.style.height = `${scrollHeight}px`;
        cardBody.style.opacity = '1';
    }else{
        //hide card body
        cardBody.style.height = '0px';
        cardBody.style.opacity = '0';
        let attribCardState = attribCard.getAttribute('data-attrib-state');
        //if we had selected anything deselect it if it is not the current state
        let selectedAttribOption = attribCard.querySelector('.attrib-option[selected]');
        //we selected something
        // console.log(selectedAttribOption);
        if (selectedAttribOption != null){        
            let selectedAttribOptionState = selectedAttribOption.getAttribute('data-option-state');
            let selectedAttribOptionDescription = attribCard.querySelector(`.attrib-option-description[data-option-state=${selectedAttribOptionState}]`);
            //is the option the same as data-attrib-state
            if (attribCardState != 'null' && attribCard != 'untested'){
                //check if the selected option is the same as the current state
                if (selectedAttribOptionState != attribCardState){
                    //we selected something that is not the current state
                    //deselect it
                    selectedAttribOption.removeAttribute('selected');
                    selectedAttribOptionDescription.removeAttribute('selected');
                    //select the corresponding option to the current state
                    let currentAttribOption = attribCard.querySelector(`.attrib-option[data-option-state=${attribCardState}]`);
                    let currentAttribOptionDescription = attribCard.querySelector(`.attrib-option-description[data-option-state=${attribCardState}]`);

                    currentAttribOption.setAttribute('selected','');
                    currentAttribOptionDescription.setAttribute('selected','');
                }
            }else{
                //we selected something that is not the current state and the current state is null
                //simply deselect it
                selectedAttribOption.removeAttribute('selected');
                selectedAttribOptionDescription.removeAttribute('selected');
            }
        }else{
            //reselect if the current state is not null
            if (attribCardState != 'null'){
                let currentAttribOption = attribCard.querySelector(`.attrib-option[data-option-state=${attribCardState}]`);
                let currentAttribOptionDescription = attribCard.querySelector(`.attrib-option-description[data-option-state=${attribCardState}]`);

                currentAttribOption.setAttribute('selected','');
                currentAttribOptionDescription.setAttribute('selected','');
            }
        }
    }
}

async function attribCommitButtonClickListener(event){
    //commit changes to the server and update the card
    let attribCard = this.attribCard
    //check if we are in editmode
    let editModeEnabled = attribCard.getAttribute('data-edit-mode-enabled') == 'true';
    if (!editModeEnabled){
        return;
    }
    let attribName = attribCard.getAttribute('data-attrib-name');
    let attribState = attribCard.getAttribute('data-attrib-state');
    /*
        TODO: check if the data has changed
    */
    let selectedAttribOption = attribCard.querySelector('.attrib-option[selected]');
    let selectedAttribOptionState = selectedAttribOption.getAttribute('data-option-state');
    // console.log(selectedAttribOption,selectedAttribOptionState);
    let dataStateChanged = selectedAttribOptionState != assessment_data[attribName];
    if (!dataStateChanged){
        return;
    }
    //dataStateChanged try and commit changes to server
    let data = structuredClone(assessment_data);
    data[attribName] = selectedAttribOptionState;
    let response = await fetch('/assessment/update',{
        method:'PATCH',
        headers:{
            'Content-Type':'application/json'
        },
        body:JSON.stringify(data)
    });
    let responseJson = await response.json();
    // console.log(responseJson);
    if (response.status == 200){
        //update the assessment object
        assessment_data[attribName] = responseJson[attribName];
        //reflect change in the card visually
        attribCard.querySelector('.card-state').textContent = attribInfoMap[attribName][assessment_data[attribName]].state;
        attribCard.setAttribute('data-attrib-state',assessment_data[attribName]);
    }else{
        console.log('error updating assessment',response);
    }
}

function attribOptionClickListener(event){
    let attribCard = this.attribCard;
    //toggle the attrib-option
    //if not selected select
    //if selected deselect
    let attribOption = event.currentTarget;
    let attribOptionState = attribOption.getAttribute('data-option-state');
    let attribOptionDescription = attribCard.querySelector(`.attrib-option-description[data-option-state=${attribOptionState}]`);
        
    let currentAttribOption = attribCard.querySelector('.attrib-option[selected]');
    //if they are different then change the state to attribOptionState
    let currentAttribOptionState = currentAttribOption.getAttribute('data-option-state');
    let currentAttribOptionDescription = attribCard.querySelector(`.attrib-option-description[data-option-state=${currentAttribOptionState}]`);
    if (currentAttribOptionState != attribOptionState){
        attribOption.setAttribute('selected','');
        attribOptionDescription.setAttribute('selected','');
    }else{
        //select untested attrib-option
        this.untestedOption.setAttribute('selected','');
        this.untestedOptionDescription.setAttribute('selected','');
    }
    currentAttribOption.removeAttribute('selected');
    currentAttribOptionDescription.removeAttribute('selected');

}

document.querySelectorAll(attribCardSelector).forEach((attribCard) => {
    //for the edit button of each card on click make the height 
    //of the card body auto
    attribCard.querySelector(attribEditButtonSelector).addEventListener('click',attribEditButtonClickListener.bind({attribCard:attribCard}));
    attribCard.querySelector(attribCommitButtonSelector).addEventListener('click',attribCommitButtonClickListener.bind({attribCard:attribCard}));
    let cardBody = attribCard.querySelector('.card-body');
    cardBody.querySelectorAll(".attrib-option").forEach((attribOption) => {
        attribOption.addEventListener('click',attribOptionClickListener.bind({
            attribCard:attribCard,
            untestedOption:attribCard.querySelector('.attrib-option[data-option-state="untested"]'),
            untestedOptionDescription:attribCard.querySelector('.attrib-option-description[data-option-state="untested"]')
        }));
    });
});
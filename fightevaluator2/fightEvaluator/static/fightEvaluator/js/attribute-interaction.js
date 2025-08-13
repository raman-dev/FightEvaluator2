//on click attrib-edit-button show card body

const attribCardSelector = '.attrib-card';
const attribEditButtonSelector = '.attrib-edit-button';
const attribCommitButtonSelector = '.attrib-commit-button';


function attribEditButtonClickListener(event){
    let attribCard = this.attribCard;
    let attribCardState = attribCard.getAttribute('data-attrib-state');
    let cardBody = attribCard.querySelector('.card-body');
    let scrollHeight = cardBody.scrollHeight;
    //toggle edit mode      gets previous edit mode then flips it
    let editModeEnabled = !(attribCard.getAttribute('data-edit-mode-enabled') == 'true');
    attribCard.setAttribute('data-edit-mode-enabled',editModeEnabled);
    //deselect all options
    attribCard.querySelectorAll('.attrib-option[selected]').forEach((attribOption) => {
        attribOption.removeAttribute('selected');
    });
    if (editModeEnabled){
        //show card body
        cardBody.style.height = `${scrollHeight}px`;
        cardBody.style.opacity = '1';
        // console.log(attribCardState);
        // if (attribCardState == 'null'){
        //     attribCardState = 'untested'; this never happens since django sets the state to untested if it is null
        // }
        //if we had selected anything deselect it if it is not the current state
        let selectedAttribOption = attribCard.querySelector(`.attrib-option[data-option-state="${attribCardState}"]`);
        selectedAttribOption.setAttribute('selected','');
        // we selected something
        //what am i doing here?
        //this is on click edit button responsibility is to show options
        //and show currently selected option if one exists
    }else{
        //hide card body
        cardBody.style.height = '0px';
        cardBody.style.opacity = '0';   
    }
}

function dataStateChanged(attribCard,attribName){
    attribCard.querySelector('.card-state').textContent = attribInfoMap[attribName][assessment_data[attribName]].state;
    attribCard.setAttribute('data-attrib-state',assessment_data[attribName]);
    let cardStateDescription = attribCard.querySelector('.card-state-description');
    cardStateDescription.setAttribute('data-option-state',assessment_data[attribName]);
    cardStateDescription.textContent = attribInfoMap[attribName][assessment_data[attribName]].description;
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

    let selectedAttribOption = attribCard.querySelector('.attrib-option[selected]');
    let selectedAttribOptionState = selectedAttribOption.getAttribute('data-option-state');
    // console.log(selectedAttribOption,selectedAttribOptionState);
    //value hasn't changed so return 
    if (selectedAttribOptionState == assessment_data[attribName] || selectedAttribOptionState == 'untested' && assessment_data[attribName] == null){
        return;
    }
    //dataStateChanged try and commit changes to server
    let data = {id: assessment_data['id']};
    // let data = structuredClone(assessment_data);
    data[attribName] = attribLabelValueMap[selectedAttribOptionState];
    // for (let key in data){   
    //     if (data[key] in attribLabelValueMap){
    //         data[key] = attribLabelValueMap[data[key]];
    //     }
    // }
    console.log(data);
    
    let response = await fetch('/assessment/update',{
        method:'PATCH',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':Cookies.get('csrftoken')
        },
        body:JSON.stringify(data)
    });
    let responseJson = await response.json();
    // console.log(responseJson);
    if (response.status == 200){
        // console.log(responseJson[attribName])
        //update the assessment object
        assessment_data[attribName] = attribValueLabelMap[responseJson[attribName]];
        //reflect change in the card visually
        dataStateChanged(attribCard,attribName);
        //toggle edit mode
        attribEditButtonClickListener.call({attribCard:attribCard});
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
        
    let currentAttribOption = attribCard.querySelector('.attrib-option[selected]');
    //if they are different then change the state to attribOptionState
    let currentAttribOptionState = currentAttribOption.getAttribute('data-option-state');
    if (currentAttribOptionState != attribOptionState){
        attribOption.setAttribute('selected','');
    }else{
        //select untested attrib-option
        this.untestedOption.setAttribute('selected','');
    }
    currentAttribOption.removeAttribute('selected');

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
            // untestedOptionDescription:attribCard.querySelector('.attrib-option-description[data-option-state="untested"]')
        }));
    });
});
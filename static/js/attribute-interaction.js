//on click attrib-edit-button show card body
const attribCardSelector = '.attrib-card';
const attribEditButtonSelector = '.attrib-edit-button';

function attribEditButtonClickListener(event){
    let attribCard = this.attribCard;
    let cardBody = attribCard.querySelector('.card-body');
    let scrollHeight = cardBody.scrollHeight;
    //toggle edit mode
    let editModeEnabled = attribCard.getAttribute('data-edit-mode-enabled') == 'true';
    if (editModeEnabled){
        //hide card body
        cardBody.style.height = '0px';
    }else{
        //show card body
        cardBody.style.height = `${scrollHeight}px`;

    }
    attribCard.setAttribute('data-edit-mode-enabled',!editModeEnabled);
}

function attribOptionClickListener(event){
    let attribCard = this.attribCard;
    //toggle the attrib-option
    //if not selected select
    //if selected deselect
    let attribOption = event.currentTarget;
    let attribOptionState = attribOption.getAttribute('data-state');
    let attribOptionDescription = attribCard.querySelector(`.attrib-option-description[data-state=${attribOptionState}]`);
    
    let newOptionState = null;
    
    let currentAttribOptionState = attribCard.getAttribute('data-attrib-state');
    //if they are different then change the state to attribOptionState
    if (currentAttribOptionState != attribOptionState){
        if (currentAttribOptionState != 'null'){
            //get the corresponding attrib-option and remove selected
            let currentAttribOption = attribCard.querySelector('.attrib-option[selected]');
            let currentAttribOptionDescription = attribCard.querySelector(`.attrib-option-description[selected]`);
            currentAttribOption.removeAttribute('selected');
            currentAttribOptionDescription.removeAttribute('selected');
        }
        attribCard.setAttribute('data-attrib-state',attribOptionState);
        attribOption.setAttribute('selected','');
        attribOptionDescription.setAttribute('selected','');
        newOptionState = attribOptionState;
    }else{
        attribCard.setAttribute('data-attrib-state','null');    
        attribOption.removeAttribute('selected');
        attribOptionDescription.removeAttribute('selected');
    }
    //reflect new state in attrib-card.state-container
    let attribStateElement = attribCard.querySelector('.state-container .card-state');
    if (newOptionState == null){
        attribStateElement.textContent = 'null';
        
    }else{
        attribStateElement.textContent = newOptionState;
    }
}

document.querySelectorAll(attribCardSelector).forEach((attribCard) => {
    //for the edit button of each card on click make the height 
    //of the card body auto
    attribCard.querySelector(attribEditButtonSelector).addEventListener('click',attribEditButtonClickListener.bind({attribCard:attribCard}));
    let cardBody = attribCard.querySelector('.card-body');
    cardBody.querySelectorAll(".attrib-option").forEach((attribOption) => {
        attribOption.addEventListener('click',attribOptionClickListener.bind({attribCard:attribCard}));
    });
});
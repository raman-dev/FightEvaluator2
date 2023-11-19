/*
    radio-group ----edit button
        content

    radio-group.click -> 
        if radio-group.isActive => 
            if edit-mode.isActive => do nothing
            else => deactivate
        else => activate
    edit-button.click ->
        if edit-mode.isActive => deactivate
            radio-group.deactivate
        else => 
            radio-group.activate
            edit-mode.activate
    
    ** NOTE **
    //target is the clicked element
    //currentTarget is the element listening for the event
*/
//on click list-group-item set it as active element of list
const attributeListItemSelector = '.mradio-group';
document.querySelectorAll(attributeListItemSelector).forEach((element) => {
    element.addEventListener('click',attributeItemClickListener);
});

//handle click on attribute item
function attributeItemClickListener(event){
    let attributeItem = event.currentTarget;//attribute list item
    let isActive = attributeItem.classList.contains('active');
    let editClicked = event.target.classList.contains('edit-button');
    // console.log('editModeActive: '+editModeActive);
    if (!isActive){
        //item is not active
        //activate
        attributeItem.classList.add('active');
        if (editClicked){
            attributeItem.setAttribute('data-edit-mode-enabled','true');
        }
    }else{
        //attribute item is active
        //edit button clicked        
        let editModeActive = attributeItem.getAttribute('data-edit-mode-enabled') == 'true';
        if (editClicked){
            //deactivate
            if (!editModeActive){
                //activate edit mode
                attributeItem.setAttribute('data-edit-mode-enabled','true');
            }else{
                //deactivate edit mode
                attributeItem.setAttribute('data-edit-mode-enabled','false');
                attributeItem.classList.remove('active');
            }
        }else{
            if (!editModeActive){
                attributeItem.classList.remove('active');
            }
        }
        
    }
}
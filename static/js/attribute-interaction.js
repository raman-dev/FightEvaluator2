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

function collapseListener(event){
    switch(event.type){
        case "show.bs.collapse":
          this.collapseState.isExpanding = true;
          this.collapseState.isCollapsing  = false;
          break;
        case "hide.bs.collapse":
          this.collapseState.isExpanding = false;
          this.collapseState.isCollapsing = true;
          break;
    }
}
//on click list-group-item set it as active element of list
const attributeListItemSelector = '.mradio-group';
document.querySelectorAll(attributeListItemSelector).forEach((element) => {
    let collapseState = {
        isCollapsing:false,
        isExpanding:false,
    }
    let collapseElement = element.querySelector('.collapse');//find collapse element
    collapseElement.addEventListener('show.bs.collapse',collapseListener.bind({collapseState:collapseState}));
    collapseElement.addEventListener('hide.bs.collapse',collapseListener.bind({collapseState:collapseState}));
    element.addEventListener('click',attributeItemClickListener.bind({collapseState:collapseState}));
    element.querySelector('.edit-button').addEventListener('click',editButtonClickListener.bind({
        collapseState:collapseState,
        radioGroup:element
    }));
});

//handle edit button click
function editButtonClickListener(event){
    // console.log('edit button clicked');
    let editModeActive = false;
    if (this.collapseState.isExpanding){
        //edit mode active
        editModeActive = true;
        console.log('edit mode active');
    }
    if (this.collapseState.isCollapsing){
        //edit mode inactive
        editModeActive = false;
        console.log('edit mode inactive');
    }
}

//handle click on attribute item
function attributeItemClickListener(event){
    // console.log('collapseState: '+this.collapseState.isExpanding);
    let attributeItem = event.currentTarget;//attribute list item
    let isActive = attributeItem.classList.contains('active');
    let editClicked = event.target.classList.contains('edit-button');
    let editModeActive = false;

    if (this.collapseState.isExpanding){
        //edit mode active
        attributeItem.setAttribute('data-edit-mode-enabled',true);
        editModeActive = true;
    }
    if (this.collapseState.isCollapsing){
        //edit mode inactive
        attributeItem.setAttribute('data-edit-mode-enabled',false);
        editModeActive = false;
    }
    
    if (editClicked){
        if (!isActive){
            //activate
            attributeItem.classList.add('active');
        }else{
            if (!editModeActive){
                attributeItem.classList.remove('active');
            }
        }
    }else{
        if (!editModeActive){
            if (isActive){
                //deactivate
                attributeItem.classList.remove('active');
            }else{
                //activate
                attributeItem.classList.add('active');
            }
        }
        // else{
            //do nothing
        // }
    }
}
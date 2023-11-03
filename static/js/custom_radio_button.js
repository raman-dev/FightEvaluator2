function setButtonStyles() {
  //for every element with data-polarity="positive"
  //add class btn-outline-primary
  document.querySelectorAll('[data-polarity="positive"]').forEach((element, idx) => {
    element.classList.add('btn-outline-primary');
  });
  //for every element with .neutral class
  //add class btn-outline-warning
  document.querySelectorAll('[data-polarity="neutral"]').forEach((element, idx) => {
    element.classList.add('btn-outline-warning');
  });
  //for every element with .negative class
  //add class btn-outline-danger
  document.querySelectorAll('[data-polarity="negative"]').forEach((element, idx) => {
    element.classList.add('btn-outline-danger');
  });
}

function getRadioType(radioType) {
  switch (radioType) {
    case "good":
      radioType = "primary";
      break;
    case "mediocre":
      radioType = "warning";
      break;
    case "bad":
      radioType = "danger";
      break;
  }
  return radioType;
}

/*
  custom radio button group structure

  mradio-group data-changed data-value="option-1"
    group-title
    group-options-container
      option-0
      option-1 attribute selected
      ...
      option-n
    
    
  when a an option is changed reflect it in the data-changed attribute
  when an option is clicked change the selected attribute to the clicked option
  change data-value to the option clicked
*/

function toggleRadioButtons(option,toggleOn) {
  if (toggleOn){
    option.setAttribute('data-mradio-selected','');
  }else{
    option.removeAttribute('data-mradio-selected');
  }
  let selectedClass = 'btn-warning';
  let unselectedClass = 'btn-outline-warning';
  
  let polarity = option.dataset.polarity.trim();
  if (polarity == "positive") {
    selectedClass = 'btn-primary';
    unselectedClass = 'btn-outline-primary';
  }
  else if (polarity == "negative"){
    selectedClass = 'btn-danger';
    unselectedClass = 'btn-outline-danger';
  }
  if (toggleOn){
    option.classList.add(selectedClass);
    option.classList.remove(unselectedClass);
  }else{
    option.classList.remove(selectedClass);
    option.classList.add(unselectedClass);
  }
  
}

function mRadioOptionChangeListener(optionElement,index) {
  //new value to reflect in page
  if(!editModeEnabled) {
    return;
  }
  let newOptionElement = optionElement;
  let newOptionValue = optionElement.dataset.polarity;
  let radioGroup = this.radioGroup;
  //check if data-value is null or empty
  let prevOptionElement = radioGroup.querySelector(`[data-mradio-selected]`);
  //check if values is null string
  //if it does not equal the current option change
  if (prevOptionElement != null) {
    toggleRadioButtons(prevOptionElement,false);
  }
  radioGroup.dataset.polarity = newOptionValue;
  //set the data-changed attribute to true
  radioGroup.dataset.changed = true;
  toggleRadioButtons(newOptionElement,true);
}

function initRadioButtionListeners() {
  //for every mradio-group 
  document.querySelectorAll('.mradio-group').forEach((element, idx) => {
    //each radio group needs its own event listener
    let mRadioGroup = element;
    //we need radioGroup to listen to the click 
    //but also the option itself to listen to the click
    //because the option needs to change the data-value attribute
    //and the radioGroup needs to change the data-changed attribute
    //for every mradio-option child of mradio-group add event listener
    mRadioGroup.querySelectorAll('.mradio-option').forEach((radioOptionElement, idx) => {
      radioOptionElement.addEventListener('click', mRadioOptionChangeListener.bind({ radioGroup: mRadioGroup }, radioOptionElement,idx));
    });
  });
}

function clearRadioButtons(){
  //any edit options selected need to be cleared
  //unset any options that are selected
  //now we need to map assessment_data to the radio buttons
  //for every mradio-group
  //compare value with assessment_data object
  //if different then return to original or unset if null
  document.querySelectorAll('[data-changed="true"]').forEach((element, idx) => {
    //
    let radioGroup = element;
    let attribute_name = radioGroup.getAttribute('data-attribute-name');
    //restore original value
    radioGroup.dataset.polarity = assessment_data[attribute_name];
    radioGroup.dataset.changed = false;
    // console.log(`assessment_data[${attribute_name}] => `,assessment_data[attribute_name]);
    //remove the selected attribute
    let candidate = radioGroup.querySelector(`[data-mradio-selected]`);
    toggleRadioButtons(candidate,false);
    //restore the original selected option
    if (assessment_data[attribute_name] != null){
      //set the selected attribute
      let original = radioGroup.querySelector(`[data-polarity="${assessment_data[attribute_name]}"]`);
      toggleRadioButtons(original,true);
    }
  });
}

function onAssessmentChanged(){
  //read the assessment_data object
  //for every key in assessment_data
  document.querySelectorAll('[data-changed="true"]').forEach((element, idx) => {
    element.setAttribute('data-changed','false');
  });
  for (let key in assessment_data){
    if (assessment_data[key] == null || key == 'id'){
      continue;
    }
    console.log(`key => ${key} value => ${assessment_data[key]}`);
    //get the radio group with data-attribute-name=key
    let radioGroup = document.querySelector(`[data-attribute-name="${key}"]`);
    radioGroup.dataset.polarity = assessment_data[key];
    let radioOption = radioGroup.querySelector(`[data-polarity="${assessment_data[key]}"]`);
    toggleRadioButtons(radioOption,true);
  }
}

setButtonStyles();
initRadioButtionListeners();


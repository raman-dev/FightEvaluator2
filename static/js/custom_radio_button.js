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

function reflectOptionChange(prevOption, newOption) {
  let selectedClass = 'btn-warning';
  let unselectedClass = 'btn-outline-warning';
  if (prevOption != null) {
    let prevPolarity = prevOption.dataset.polarity.trim();
    if (prevPolarity == "positive") {
      selectedClass = 'btn-primary';
      unselectedClass = 'btn-outline-primary';
    }
    else if (prevPolarity == "negative"){
      selectedClass = 'btn-danger';
      unselectedClass = 'btn-outline-danger';
    }
    prevOption.classList.remove(selectedClass);
    prevOption.classList.add(unselectedClass);
  }
  //set styling info based on option polarity
  // console.log('newOption => ', newOption);
  let polarity = newOption.dataset.polarity.trim();
  //reset selectedClass and unselectedClass
  selectedClass = 'btn-warning';
  unselectedClass = 'btn-outline-warning';
  if (polarity === "positive") {
    selectedClass = 'btn-primary';
    unselectedClass = 'btn-outline-primary';
  }
  else if (polarity === "negative"){
    selectedClass = 'btn-danger';
    unselectedClass = 'btn-outline-danger';
  }
  // console.log('selectedClass => ', selectedClass, ' unselectedClass => ', unselectedClass);
  newOption.classList.remove(unselectedClass);
  newOption.classList.add(selectedClass);
}

function mRadioOptionChangeListener(optionElement) {
  //new value to reflect in page
  let newOptionElement = optionElement;
  let newOptionValue = optionElement.textContent.trim();
  let radioGroup = this.radioGroup;
  //check if data-value is null or empty
  let prevOptionElement = radioGroup.querySelector(`[data-mradio-selected]`);
  // let prevOptionValue = radioGroup.dataset.value;
  //check if values is null string
  //if it does not equal the current option change
  if (prevOptionElement != null) {
    // console.log('option changed to => ',newOptionValue);
    prevOptionElement.removeAttribute('data-mradio-selected');
  }
  radioGroup.dataset.value = newOptionValue;
  //set the data-changed attribute to true
  radioGroup.dataset.changed = true;
  newOptionElement.setAttribute('data-mradio-selected', '');
  reflectOptionChange(prevOptionElement, newOptionElement);
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
      radioOptionElement.addEventListener('click', mRadioOptionChangeListener.bind({ radioGroup: mRadioGroup }, radioOptionElement));
    });
  });
}

setButtonStyles();
initRadioButtionListeners();


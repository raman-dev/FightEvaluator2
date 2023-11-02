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
  //for every mradio-group
  document.querySelectorAll(".mradio-group").forEach((element, idx) => {
    // console.log(element,idx);
    //for every radio button in element add event listener
    element.querySelectorAll(".btn").forEach((btn, idx) => {
      btn.addEventListener("click", (event) => {
        let selectedElement = element.querySelectorAll(".selected")[0];
        //add selected class to clicked button
        let currentClassList = event.target.classList;
        let currentRadioType = getRadioType(event.target.dataset.radiotype);

        let filledClass = "btn-" + currentRadioType;
        let outlineClass = "btn-outline-" + currentRadioType;
        if (!currentClassList.contains("selected")) {
          //add selected class to clicked button
          currentClassList.add("selected");
          currentClassList.add(filledClass);
          currentClassList.remove(outlineClass);
        }
        //remove selected class from previously selected button
        if (selectedElement != null) {
          let selectedClassList = selectedElement.classList;
          let selectedRadioType = getRadioType(
            selectedElement.dataset.radiotype
          );
          selectedClassList.remove("selected");
          selectedClassList.remove("btn-" + selectedRadioType);
          selectedClassList.add("btn-outline-" + selectedRadioType);
        }
      });
    });
  });
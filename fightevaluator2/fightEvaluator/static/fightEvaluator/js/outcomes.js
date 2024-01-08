//on click show confidence-list-btn expand confidence-list
//for every show-confidence-list-btn 
//add click event listener
document.querySelectorAll('.confidence-selector').forEach(item => {
    let showConfidenceListBtn = item.querySelector('.show-confidence-list-btn');
    let confidenceList = item.querySelector('.confidence-list');
    let confidence = item.querySelector('.current-confidence .confidence');
    //add click event listener to list items of confidenceList
    confidenceList.querySelectorAll('li').forEach(li => {
        li.addEventListener('click', (event) => {
            let listItem = event.currentTarget;
            if (listItem.classList.contains('active')) {
                //if clicked list item is active, remove active class
                return;
            }
            let currentConfidence = confidenceList.querySelector('.active');
            currentConfidence.classList.remove('active');
            listItem.classList.add('active');
            confidence.textContent = listItem.textContent;
            confidence.classList.remove(currentConfidence.classList[0]);
            confidence.classList.add(listItem.classList[0]);    
        });
    });
    showConfidenceListBtn.addEventListener('click', (event) => {
        //check if confidenceList is expanded
        let isOpen = confidenceList.classList.contains('expanded');
        if (isOpen) {
            //if confidenceList is expanded, collapse it
            confidenceList.classList.remove('expanded');
            //set height to 0
            confidenceList.style.height = '0px';
        } else {
            //if confidenceList is collapsed, expand it
            confidenceList.classList.add('expanded');
            confidenceList.style.height = `${confidenceList.scrollHeight}px`;
        }
    });
});
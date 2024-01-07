//on click show confidence-list-btn expand confidence-list
//for every show-confidence-list-btn 
//add click event listener
document.querySelectorAll('.confidence-selector').forEach(item => {
    let showConfidenceListBtn = item.querySelector('.show-confidence-list-btn');
    let confidenceList = item.querySelector('.confidence-list');
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
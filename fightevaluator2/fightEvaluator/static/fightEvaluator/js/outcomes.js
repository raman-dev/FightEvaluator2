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
            let likelihood = listItem.querySelector('.likelihood');
            if (listItem.classList.contains('active')) {
                //if clicked list item is active, remove active class
                return;
            }
            let currentConfidence = confidenceList.querySelector('.active');
            let oldLikelihoodElement = currentConfidence.querySelector('.likelihood');
            let oldLikelihood = oldLikelihoodElement.classList[oldLikelihoodElement.classList.length - 1];
            
            currentConfidence.classList.remove('active');
            listItem.classList.add('active');

            // console.log(likelihood,currentLikelihood);
            console.log(likelihood.classList[likelihood.classList.length - 1], oldLikelihood);

            confidence.textContent = likelihood.textContent;
            confidence.classList.remove(oldLikelihood);
            confidence.classList.add(likelihood.classList[likelihood.classList.length - 1]);    
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
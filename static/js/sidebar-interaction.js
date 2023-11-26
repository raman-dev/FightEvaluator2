function stripIdAndStore(stack,storeKey){
    let url_parts = url.split('/');
    let id = parseInt(url_parts[url_parts.length-1]);
    if (!id in stack){
        stack.push(id);
    }else{
        //remove the element from the stack and push it to the top
        //remove the element
        stack = stack.filter((item) => item !== id);
        stack.push(id);
    }
     //remove the last element of the stack if size is greater than 5
    if (stack.length > 5){
        stack.shift();
    }
    // Convert the array to a JSON string and store it in localStorage
    localStorage.setItem(storeKey, JSON.stringify(stack));
}

function addSideBarLinks(stack, linkContainer,path){
    // console.log(linkContainer);
    for (let i = stack.length - 1;i >= 0;i--){
        let id = stack[i];
        let link = document.createElement('a');
        link.href = `/${path}/${id}`;
        link.innerHTML = `<div class="link">${id}</div>`;
        linkContainer.appendChild(link);
        // console.log(link);
    }
}

//if current domain is /assessment then set cookie for assessment_id_0 -> assessment_id

// Retrieve the JSON string from localStorage
let assessmentStack = localStorage.getItem('assessments');
if (assessmentStack == null){
    assessmentStack = [];
}else{
    // Parse the JSON string back into an array
    assessmentStack = JSON.parse(assessmentStack);
}

let matchupStack = localStorage.getItem('matchups');
if (matchupStack == null){
    matchupStack = [];
}else{
    matchupStack = JSON.parse(matchupStack);
}

//get url of current page
let url = window.location.href;
//
if (url.includes('assessment')){
    stripIdAndStore(assessmentStack,'assessments');
    document.querySelector('.assessment-links').classList.add('active');
    
}else if (url.includes('matchup')){
    document.querySelector('.matchup-links').classList.add('active');
    stripIdAndStore(matchupStack,'matchups');
}

addSideBarLinks(assessmentStack, document.querySelector('.assessment-links .link-container'), 'assessment');
addSideBarLinks(matchupStack, document.querySelector('.matchup-links .link-container'), 'matchup');

//on click sidebar link wrapper expand to height of content
document.querySelectorAll('.sidebar-container .link-wrapper').forEach((linkWrapper) => {
    let lc = linkWrapper.querySelector('.link-container');
    if (linkWrapper.classList.contains('active')){
        lc.style.height = lc.scrollHeight+'px';
    }
    linkWrapper.addEventListener('click', (event) => {
        //check if linkWrapper is already expanded
        let linkContainer = linkWrapper.querySelector('.link-container');
        if (linkWrapper.classList.contains('active')) {
            //if it is expanded, collapse it
            linkWrapper.classList.remove('active');
            linkContainer.style.height = '0px';
            return;
        }
        linkWrapper.classList.add('active');
        //get the height of the link-container
        let linkContainerHeight = linkContainer.scrollHeight;
        linkContainer.style.height = linkContainerHeight + 'px';
    });
});

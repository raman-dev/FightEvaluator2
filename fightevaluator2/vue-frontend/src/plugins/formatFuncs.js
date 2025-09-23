function replaceUnderscoreSpace(value) {
  //replace underscores with spaces 
    return value.replace(/_/g,' ');
}

function dobToAge(dobString) {
    if (!dobString) return "N/A"; // handle empty input

    const today = new Date();
    const dob = new Date(dobString);

    let age = today.getFullYear() - dob.getFullYear();
    const monthDiff = today.getMonth() - dob.getMonth();
    const dayDiff = today.getDate() - dob.getDate();

    // if birthday hasn’t occurred yet this year, subtract 1
    if (monthDiff < 0 || (monthDiff === 0 && dayDiff < 0)) {
        age--;
    }

    return age;
}


function inchesToFeetStr(inches) {
    return `${Math.floor(inches / 12)}'${inches % 12}`;
}

export default {
  install: (app,options) => {
    
    app.provide('replaceUnderscoreSpace',replaceUnderscoreSpace);
    app.provide('dobToAge',dobToAge);
    app.provide('inchesToFeetStr',inchesToFeetStr);
  }
}
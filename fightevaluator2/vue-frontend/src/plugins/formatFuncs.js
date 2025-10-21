function replaceUnderscoreSpace(value) {
   if (value === undefined || value === null) return "";
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

/**
 * 
 * @param {*} dateString in the format "YYYY-MM-DD"
 * @returns Month name abbreviated Day, Year (e.g., "Jan. 5, 2020")
 */
function abbreviatedDateFormat(dateString) {
  // Parse the input string as a Date object
  const date = new Date(dateString);

  // Array of abbreviated month names
  const months = ["Jan.", "Feb.", "Mar.", "Apr.", "May.", "Jun.", 
                  "Jul.", "Aug.", "Sep.", "Oct.", "Nov.", "Dec."];

  // Extract parts
  const month = months[date.getMonth()];
  const day = date.getDate();
  const year = date.getFullYear();

  // Construct formatted string
  return `${month} ${day}, ${year}`;
}


function toPercent(value, decimals = 2){
    if (isNaN(value)) return "N/A";
    return (value * 100).toFixed(decimals) + "%";
}

function inchesToFeetStr(inches) {
    return `${Math.floor(inches / 12)}'${inches % 12}`;
}

export default {
  install: (app,options) => {
    
    app.provide('replaceUnderscoreSpace',replaceUnderscoreSpace);
    app.provide('dobToAge',dobToAge);
    app.provide('inchesToFeetStr',inchesToFeetStr);
    app.provide('toPercent',toPercent);
    app.provide('abbreviatedDateFormat',abbreviatedDateFormat);
  }
}
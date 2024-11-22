const pollingInterval = 3000;//500ms or 0.5s
// var pollingIntervalHandle = null;
const oddsResultLabel = document.querySelector('.odds-result-label');
function createOddsElement(odds){
    /*
        "fighter_a": fa,
        "fighter_b": fb,
        "mult_a": toMultiplier(oa),
        "mult_b": toMultiplier(ob),
        "odds_a": oa,
        "odds_b": ob,
    */
    return $(`
        <tr data-selected="">
            <td><p>${odds.fighter_a}</p></td>
            <td><p>${odds.fighter_b}</p></td>
            <td data-name="fighter-a-odds" onclick="onClickOdds(event)" class="odds"><p ><strong>${odds.mult_a} (${ odds.odds_a })</strong></p></td>
            <td data-name="fighter-b-odds" class="odds" onclick="onClickOdds(event)"><p ><strong>${odds.mult_b} (${ odds.odds_b })</strong></p></td>
            <!-- <td data-name="round-ge-one-half-odds" class="odds" onclick="onClickOdds(event)"><p ><strong>-200</strong></p></td> -->
        </tr>
        `)[0];
}

function pollEndpoint(){
    console.log(`${this.query}: Polling endpoint...`);
    
    fetch("/profit/get-odds", {
        method: "GET",
        headers: {
            accept: "application/json",
            "Content-Type": "application/json",
            "X-CSRFToken": Cookies.get("csrftoken"),
        },
      })
        .then((response) => response.json())
        .then((data) => {
          console.log('Received data...',data);
          //update matchup table
          //update on server
          //check if we have data or data not ready
          document.querySelector('table').classList.remove('transparent');//make visible
          if (data.available){
            clearInterval(pollingIntervalHandle);
            let tableBody = document.querySelector('.odds-table tbody');
            let oddsList = data.oddsList;
            for (const odd of oddsList){
                let row = createOddsElement(odd);
                tableBody.appendChild(row);
            }
            oddsResultLabel.textContent = 'Multiplier: 1';
          }else{
            //data is unavailble currently try again later
            //display the update message
            oddsResultLabel.textContent = 'Server is....' + data.message;
          } 
        });
    
    this.query = this.query + 1;

}

const pollingIntervalHandle = setInterval(pollEndpoint.bind({query:0}),pollingInterval);
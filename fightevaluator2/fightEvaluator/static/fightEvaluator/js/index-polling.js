
console.log('index poller included!');

const timeDelay = 3000;
const headers = {
    accept: "application/json",
    "Content-Type": "application/json",
    "X-CSRFToken": Cookies.get("csrftoken"),
}
const indexEndpoint = '/index-endpoint';

class Poller {
    static DEFAULT_POLLING_RATE = 3000;
    constructor(url, headers, resultFunction, pollingRate = Poller.DEFAULT_POLLING_RATE) {
        this.endpoint = url;
        this.headers = headers;
        this.resultFunction = resultFunction;
        this.timeDelay = pollingRate;
        this.functionHandle = null;
    }

    startPolling() {
        this.functionHandle = setInterval(this.poll.bind({ poller: this }), this.timeDelay);
    }

    async poll() {
        const response = await fetch(`${this.poller.endpoint}`, {
            method: 'GET',
            headers: this.poller.headers
        });
        const data = await response.json();
        if (data.available) {
            this.poller.stopPolling();
        }
        this.poller.resultFunction(data);
    }

    stopPolling() {
        clearInterval(this.functionHandle);
        this.functionHandle = null;
    }
}

function pollResult(data) {
    // console.log(data);
    if (!data.available) {
        console.log(`Server is.... ${data.message}`);
    } else {
        console.log('Received data...');//, data);
        //populate the tables with the data
        const eventData = data['event'];
        const mainCard = data['mainCard'];
        const prelims = data['prelims'];
        fightEventIdWrapper[0] = eventData.id;
        
        //set title
        document.querySelector('.event-title').textContent = eventData.title;
        //mainCardTable -> object
        for (const matchup of mainCard){
            matchupMap[matchup.id] = matchup;
            mainCardTable.addMatchup(matchup);
        }
        for (const matchup of prelims){
            matchupMap[matchup.id] = matchup;
            prelimTable.addMatchup(matchup);
        }
    }
    /*
        
    event_structure {
        "id": 77,
        "title": "UFC 310: Pantoja vs. Asakura",
        "date": "2024-12-07",
        "location": null,
        "link": "https://www.tapology.com/fightcenter/events/116766-ufc-310",
        "hasResults": false
    }
    
    matchup structure
    {
        "id": 780,
        "fighter_a": 2453,
        "fighter_b": 3799,
        "weight_class": "flyweight",
        "rounds": 5,
        "scheduled": "2024-12-07",
        "event": 77,
        "isprelim": false,
        "outcome": null,
        "inWatchList": null,
        "analysisComplete": false,
        "fighter_a_references": 0,
        "fighter_b_references": 0,
        "fighter_a_name": "alexandre pantoja",
        "fighter_b_name": "kai asakura"
    }
    */
}

const indexPoller = new Poller(indexEndpoint, headers, pollResult);
indexPoller.startPolling();


const timeDelay = 3000;//3s
const headers = {
    accept: "application/json",
    "Content-Type": "application/json",
    "X-CSRFToken": Cookies.get("csrftoken"),
}
const indexPoller = new Poller('/index-endpoint',headers,onReceiveIndexPollResult);

class Poller {
    static DEFAULT_POLLING_RATE = 3000;
    constructor(url, headers, resultFunction,pollingRate = DEFAULT_POLLING_RATE) {
        this.endpoint = url;
        this.headers = headers;
        this.functionHandle = null;
        this.timeDelay = pollingRate;
        this.resultFunction = resultFunction;
    }

    startPolling() {
        this.functionHandle = setInterval(poll, this.timeDelay);
    }

    poll() {
        fetch(`${this.endpoint}`, {
            method: 'GET',
            headers: this.headers
        })
        .then(response => response.json())
        .then((data) => {
            if (data.available){
                this.stopPolling();
            }
            this.resultFunction(data);
        });
    }

    stopPolling(){
        clearInterval(this.functionHandle);
        this.functionHandle = null;
    }
}

function onReceiveIndexPollResult(data) {
    console.log('Received data...', data);
    //update matchup table
    //update on server
    //check if we have data or data not ready
    // document.querySelector('table').classList.remove('transparent');//make visible
    if (data.available) {
        
    } else {
        //data is unavailble currently try again later
        //display the update message
        console.log(`'Server is....' + ${data.message}`);
    }
}

const pollingIntervalHandle = setInterval(indexPollingFunction, timeDelay);

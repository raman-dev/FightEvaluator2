
console.log('index poller included!');

const timeDelay = 3000;
const headers = {
    accept: "application/json",
    "Content-Type": "application/json",
    "X-CSRFToken": Cookies.get("csrftoken"),
}
const indexEndpoint = '/index-endpoint'
// const indexPoller = new Poller('/index-endpoint',headers,onReceiveIndexPollResult);

class Poller {
    static DEFAULT_POLLING_RATE = 3000;
    constructor(url, headers, resultFunction,pollingRate = Poller.DEFAULT_POLLING_RATE) {
        this.endpoint = url;
        this.headers = headers;
        this.resultFunction = resultFunction;
        this.timeDelay = pollingRate;
        this.functionHandle = null;
    }

    startPolling() {
        this.functionHandle = setInterval(this.poll.bind({poller:this}), this.timeDelay);
    }

    async poll() {
        const response = await fetch(`${this.poller.endpoint}`, {
            method: 'GET',
            headers: this.poller.headers
        });
        const data = await response.json();
        if (data.available){
            this.poller.stopPolling();
        }
        this.poller.resultFunction(data);
    }

    stopPolling(){
        clearInterval(this.functionHandle);
        this.functionHandle = null;
    }
}

function pollResult(data) {
    console.log(data);
    if (data.available) {
        console.log('Received data...', data);
    } else {
        console.log(`Server is.... ${data.message}`);
    }
}

const indexPoller = new Poller(indexEndpoint,headers,pollResult);
indexPoller.startPolling();

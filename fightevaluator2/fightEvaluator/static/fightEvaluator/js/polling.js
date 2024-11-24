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

// export default Poller;
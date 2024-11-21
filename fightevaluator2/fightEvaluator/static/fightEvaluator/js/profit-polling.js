const pollingInterval = 1500;//500ms or 0.5s
var pollingIntervalHandle = null;
function pollEndpoint(){
    console.log(`${this.query}: Polling endpoint...`);
    //clear interval here
    this.query = this.query + 1;
}

// pollingIntervalHandle = setInterval(pollEndpoint.bind({query:0}),pollingInterval);
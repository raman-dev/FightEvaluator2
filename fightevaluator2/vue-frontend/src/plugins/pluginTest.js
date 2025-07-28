export default {
    install: (app,options) => {
        //plugin code here
        app.provide('pluginFunc',()=>{
            console.log('Called plugin function');
        });
    }
}



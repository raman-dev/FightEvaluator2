class Server {
    static URLS = {
      CREATE_NOTE : '/notes/create-note',
      DELETE_NOTE : '/notes/delete-note/',
      
      UPDATE_FIGHTER :'/fighters/update-fighter2/',
      SEARCH_FIGHTERS : '/fighters/search/?search=',

      CREATE_MATCHUP : '/matchup/create-matchup',
      UPDATE_MATCHUP:'/matchup/update-matchup/',

      GET_NEXT_EVENT: 'vue/next-event',
      ALL_EVENTS: 'vue/events',
      GET_EVENT:'vue/events/'
    }

    //provide
    static headers = {

    }

    static async get_all_events(callback){
      fetch(Server.URLS.ALL_EVENTS)
      .then(response => response.json())
      .then((data) => {
        callback(data);
      });
    }

    //gets event data and matchups 
    static async get_next_event(callback){
      fetch(Server.URLS.GET_NEXT_EVENT)
        .then(response => response.json())
        .then((data) => {
          callback(data);
        });
    }

    static async update_fighter(requestData,callback,fighterId){
      fetch(Server.URLS.UPDATE_FIGHTER + `${fighterId}`,{
        method:"PATCH",
        headers:Server.headers,
        body: JSON.stringify(requestData)
      }).then(response => response.json())
      .then((data)=>{
        callback(data);//
      });
    }

    static async send_note(requestData,callback){
      fetch(Server.URLS.CREATE_NOTE,{
        method:"POST",
        headers:Server.headers,
        body: JSON.stringify(requestData)
      }).then(response => response.json())
      .then((data)=>{
        callback(data);//
      });
      // post(Server.URLS.CREATE_NOTE,requestData,callback);
    }

    static async remove_note(callback,noteId){
      //need error checking, parameter validation
      fetch(Server.URLS.DELETE_NOTE + `${noteId}`,{
        method:"DELETE",
        headers:Server.headers
      }).then(response => response.json())
      .then((data)=>{
        callback(data);//
      });
    }

    static async search_fighters(callback,query_string){
      fetch(Server.URLS.SEARCH_FIGHTERS + `${query_string}`)
      .then(response => response.json())
      .then((data) => {
        callback(data);
      });
    }

    static async create_matchup(requestData,callback){
      fetch(Server.URLS.CREATE_MATCHUP,{
        method:"POST",
        body: JSON.stringify(requestData),
        headers: Server.headers,
      })
      .then(response => response.json())
      .then((data) => {
        callback(data);
      });
    }

    static async update_matchup(requestData,callback,matchupId){
      fetch(Server.URLS.UPDATE_MATCHUP + `${matchupId}`,{
        method:"PATCH",
        body: JSON.stringify(requestData),
        headers: Server.headers,
      })
      .then(response => response.json())
      .then((data) => {
        callback(data);
      });
    }

    // post(url,requestData,callback){
    //   fetch(url,{
    //     method:"POST",
    //     body: JSON.stringify(requestData),
    //     headers:this.headers
    //   }).then(response => response.json())
    //   .then((data) => {
    //     callback(data);
    //   });
    // }

    // patch(url,requestData,callback){

    // }

    // get(url,requestData,callback){

    // }
}

export default {
  install: (app,options) => {
    Server.headers = options.headers;
    app.provide('server', Server);
  }
}
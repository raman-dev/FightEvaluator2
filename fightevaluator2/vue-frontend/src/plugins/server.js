class Server {
    static URLS = {
      CREATE_NOTE : '/notes/create-note',
      DELETE_NOTE : '/notes/delete-note/',
      
      UPDATE_FIGHTER :'/fighters/update-fighter2/',
      SEARCH_FIGHTERS : '/fighters/search/?search=',

      CREATE_MATCHUP : '/matchup/create-matchup',
      UPDATE_MATCHUP:'/matchup/update-matchup/',

      GET_NEXT_EVENT: '/vue/next-event',
      ALL_EVENTS: '/vue/events',

      GET_ASSESSMENT: '/vue/assessments'
    }

    //provide
    static headers = {

    }

    static async get_assessment(fighterId,callback){
      Server.get(Server.URLS.GET_ASSESSMENT + `/${fighterId}`,callback)
    }

    static async get_event(eventId,callback){
      Server.get(Server.URLS.ALL_EVENTS + `/${eventId}`,callback)
    }

    static async get_all_events(callback){
      Server.get(Server.URLS.ALL_EVENTS,callback);
    }

    //gets event data and matchups 
    static async get_next_event(callback){
      Server.get(Server.URLS.GET_NEXT_EVENT,callback);
    }

    static async update_fighter(requestData,fighterId,callback){
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

    static async delete_note(noteId,callback){
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

    static async get(url,callback){
      fetch(url)
        .then(response => response.json())
        .then((data) => {
          callback(data);
        });
    }
}

export default {
  install: (app,options) => {
    Server.headers = options.headers;
    app.provide('server', Server);
  }
}
class Server {

    static URLS = {
      CREATE_NOTE : '/notes/create-note',
      DELETE_NOTE : '/notes/delete-note/',
      UPDATE_FIGHTER :'/fighters/update-fighter2/',
      SEARCH_FIGHTERS : '/fighters/search/?search='
    }

    constructor(headers) {
        this.headers = headers
    }

    async update_fighter(requestData,callback,fighterId){
      fetch(Server.URLS.UPDATE_FIGHTER + `${fighterId}`,{
        method:"PATCH",
        headers:this.headers,
        body: JSON.stringify(requestData)
      }).then(response => response.json())
      .then((data)=>{
        callback(data);//
      });
    }

    async send_note(requestData,callback){
      fetch(Server.URLS.CREATE_NOTE,{
        method:"POST",
        headers:this.headers,
        body: JSON.stringify(requestData)
      }).then(response => response.json())
      .then((data)=>{
        callback(data);//
      });
    }

    async remove_note(callback,noteId){
      //need error checking, parameter validation
      fetch(Server.URLS.DELETE_NOTE + `${noteId}`,{
        method:"DELETE",
        headers:this.headers
      }).then(response => response.json())
      .then((data)=>{
        callback(data);//
      });
    }

    async search_fighters(callback,query_string){
      fetch(Server.URLS.SEARCH_FIGHTERS + `${query_string}`)
      .then(response => response.json())
      .then((data) => {
        callback(data);
      });
    }
}
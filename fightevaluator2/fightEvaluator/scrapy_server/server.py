
import zmq
import threading 
import json
import os
import copy

from queue import Queue
from rich import print as rprint
from enum import Enum
from fightEvaluator.scraper_funcs.commands import ServerCommands,ServerStates
from pathlib import Path
from datetime import datetime


from fightEvaluator.scraper_funcs import scrapy_worker
from . import scraper

DEFAULT_SERVER_TIMEOUT_S = 300# seconds

class ZmqRepServer:
    def __init__(self,serverPort: int,timeoutSeconds: int = DEFAULT_SERVER_TIMEOUT_S):
        self.port = serverPort
        self.timeout = timeoutSeconds

        # Create a command router
        self.command_handlers = {
            ServerCommands.SERVER_STATE: self.handle_server_state,
            ServerCommands.KILL_SERVER: self.handle_kill_server
        }

        self.state = ServerStates.IDLE
        self.running = False

        self.cache = {}
    def start(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.setsockopt(zmq.LINGER, 0)#don't block when trying to close
        self.socket.bind(f"tcp://*:{self.port}")
        
        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)

    def timeout_to_ms(self,seconds):
        return seconds * 1000

    def run(self):
        self.running = True
        rprint(f"[bold green]Server running on port {self.port}[/bold green]")
        #Keyboard interrupt doesn't work when poller.poll is called
        #if you want to use keyboard interrupts need to run server in background thread 
        #and allow user to stop from main thread
        while self.running:
            events = self.poller.poll(self.timeout_to_ms(DEFAULT_SERVER_TIMEOUT_S))
            
            if events == []:
                #no events
                rprint(f"[bold red]No requests within {DEFAULT_SERVER_TIMEOUT_S} seconds.[/bold red]")
                break

            message = self.socket.recv_pyobj()
            rprint(f"[bold yellow]Received message: {message}[/bold yellow]")
            validationResult = self.is_valid(message)
            if "error" not in validationResult:
                self.handle_message(message)
            else:
                self.send_response(validationResult)


        self.state = ServerStates.SHUTTING_DOWN

    def handle_message(self,message):
        rprint(f"[bold yellow]Received message: {message}[/bold yellow]")
        # response = self.process_message(message)
        self.send_response({"result":message['command'],"data":f"You sent {message}"})
    
    def send_response(self,message):
        self.socket.send_pyobj(message)

    def stop(self):
        self.poller.unregister(self.socket)
        self.socket.close()
        self.context.term()
        rprint(f"[bold red]Server stopped[/bold red]")
    

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def is_valid(self, message: dict):
        """Validate and route the command."""
        if not isinstance(message, dict) or "command" not in message:
            return {"error": "Invalid message format"}

        try:
            cmd = ServerCommands(message["command"])
        except ValueError:
            return {"error": f"Unknown command: {message['command']}"}

        return {"message":"valid"}

    def handle_server_state(self, msg) -> dict:
        return {
            "result": "SERVER_STATE",
            "state": self.state.value
        }

    def handle_kill_server(self, msg) -> dict:
        self.running = False
        return {"result": "KILL_SERVER", "status": "Server shutting down"}

    # ------------------------------------------------------------------

"""#need to break into more pieces
    message-processor
        worker
           states 
            working
            done
        append data to result_q
    message-processor.on_receive_request
        check result_q has data 
            if has return 
            else
                
"""
"""
    what do i need to do really?
    not much 
    just have a config file where parser and fetcher can be chosen

"""

class ScraperServer(ZmqRepServer):
    
    class ServerResponse:
        @staticmethod
        def build(command: ServerCommands,state: ServerStates,data: dict = None):
            response =  {
                "result":command.value,
                "state" : state.value,
            }
            if data != None:
                response['data'] = data
            
            return response

    def __init__(self, serverPort, timeoutSeconds = DEFAULT_SERVER_TIMEOUT_S):
        super().__init__(serverPort, timeoutSeconds)
        
        self.fightEventFileName = "fight-event-data.json"#use one file for event and matchups
        self.fighterDataFileName = "fighter-data.json"
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, f"{self.fightEventFileName}")
        
        self.fightEventFileNameAbs = file_path
        self.fighterDataFileNameAbs = os.path.join(script_dir,f"{self.fighterDataFileName}")
        self.data_q = Queue()#thread safe queue for data from worker to server
        self.workerThread = None
        

        self.fighter_data_cache = {}

        with open(self.fighterDataFileNameAbs,"r",encoding="utf-8") as f:
            self.fighter_data_cache = json.load(f)

    def handle_message(self, message):

        #process data in the q before moving forward
        """

            scrapy worker correctly returns data

            data is written to json file

            data is available on a thread 
            client queries for event
                if busy response busy
                if idle get event
                    if event-file dne or event-file.date is in the past:
                        fetch new event
                    else:
                        event is yet to come return file data
                

            server thread
            worker thread
               write data to file
               write state to queue
            on receive command
                read state from queue
                update server state 
                respond to client if worker complete and data available       

        """
        self.process_data_q()
        command = message['command']
        data = message['data']

        response = {}

        match ServerCommands[command]:
            case ServerCommands.SERVER_STATE:
                response = self.ServerResponse.build(ServerCommands.SERVER_STATE,self.state)
            case ServerCommands.FETCH_EVENT_LATEST:
                response = self.handle_fetch_event(data)
            case ServerCommands.FETCH_EVENT_RESULTS:
                response = self.handle_fetch_event_results(data)
            case ServerCommands.FETCH_FIGHTER: 
                response = self.handle_fetch_fighter(data)
            case ServerCommands.FETCH_FIGHTER_MULTI: 
                # response = self.handle_fetch_fighter_multi(data)
                #untested
                pass
            case ServerCommands.FETCH_EVENT_ANY:
                response = self.handle_fetch_event_any(data)
            case ServerCommands.KILL_SERVER:
                self.running = False
                response = self.ServerResponse.build(ServerCommands.KILL_SERVER,self.state, {"status": "Server shutting down"})
        super().send_response(response)

    def write_to_file(self,fname,data):
        with open(fname,"w",encoding="utf-8") as file:
            json.dump(data,file,indent=4,default=str)
        
    
    def update_fighter_data_file(self,data):
        with open(self.fighterDataFileNameAbs,"r+",encoding="utf-8") as fighter_data_file:
            fighter_data = json.load(fighter_data_file)
            #update fighter_data map 
            for k,v in data.items():
                fighter_data[k] = v 
                self.fighter_data_cache[k] = v

            fighter_data_file.seek(0)#move to start
            fighter_data_file.truncate(0)#0 bytes remain in the file after truncating


            json.dump(self.fighter_data_cache,fighter_data_file,default=str)

    def process_data_q(self):
        #process data in the q before processing new messages
        if not self.data_q.empty():
            print("data q non empty")
            data = self.data_q.get()
            #add to in memory cache
            rprint(f"Processing data from worker thread for [bold magenta]command: {self.working_on}[/bold magenta]")
            match self.working_on:
                case ServerCommands.FETCH_EVENT_RESULTS:
                    self.cache[ServerCommands.FETCH_EVENT_RESULTS] = data
                case ServerCommands.FETCH_EVENT_LATEST:

                    self.cache[ServerCommands.FETCH_EVENT_LATEST] = data
                    self.write_to_file(self.fightEventFileNameAbs,data)
                    #clear the fighter-data.json file 
                    self.write_to_file(self.fighterDataFileNameAbs,{})
                    self.fighter_data_cache = {}#clear fighter data cache
                    """
                     fight-event-data.json
                        title:
                        date:
                        link: 
                        matchups: [
                            {
                                fighter_a
                                fighter_b
                                fighter_a_link
                                fighter_b_link
                                weightclass
                                round
                                isprelim
                            }
                        ]

                    """
                case ServerCommands.FETCH_FIGHTER:
                    #update fighter-data file here 
                    # self.fighter_data_cache[]
                    self.update_fighter_data_file(data)
                    self.cache[ServerCommands.FETCH_FIGHTER] = data

                case ServerCommands.FETCH_FIGHTER_MULTI:
                    self.cache[ServerCommands.FETCH_FIGHTER_MULTI] = data
                case ServerCommands.FETCH_EVENT_ANY:
                    self.cache[ServerCommands.FETCH_EVENT_ANY] = data
            self.working_on = None
            if self.workerThread != None:
                self.workerThread.join()
                self.workerThread = None
            self.state = ServerStates.IDLE
    
    def handle_fetch_event_any(self,data: dict):
        if self.state == ServerStates.BUSY:
            #return its busy working
            return self.ServerResponse.build(ServerCommands.FETCH_EVENT_LATEST,self.state)
        
        if ServerCommands.FETCH_EVENT_ANY in self.cache:
            return self.ServerResponse.build(ServerCommands.FETCH_EVENT_ANY,self.state,
                self.cache.pop(ServerCommands.FETCH_EVENT_ANY))
        
        self.startWorker(
            ServerCommands.FETCH_EVENT_ANY,
            workerFunc=scraper.scrape_event,#scrapy_worker.runScrapyFetchEvent,
            workerArgs=[self.data_q,15,data['link'],data['date']])
        return self.ServerResponse.build(ServerCommands.FETCH_EVENT_LATEST,self.state,{"message":"Server starting scraper workers..."})
    

    def handle_fetch_event_results(self,data: dict) -> dict:
        if self.state == ServerStates.BUSY:
            return self.ServerResponse.build(ServerCommands.FETCH_EVENT_RESULTS,self.state)
        #not busy meaning we can perform the work
        #check if in cache
        
        if ServerCommands.FETCH_EVENT_RESULTS in self.cache:
            return self.ServerResponse.build(ServerCommands.FETCH_EVENT_RESULTS,self.state,self.cache.pop(ServerCommands.FETCH_EVENT_RESULTS))

        link = data['link']    
        #not in cache and server not busy
        self.startWorker(
                ServerCommands.FETCH_EVENT_RESULTS,
                workerFunc=scraper.scrape_fight_event_results,#scrapy_worker.runScrapyFetchResults,
                workerArgs=[self.data_q,link])
        
        return self.ServerResponse.build(ServerCommands.FETCH_EVENT_RESULTS,self.state,{"message":"Starting scrapy server"})

    def handle_fetch_fighter(self, data:dict) -> dict:
        if self.state == ServerStates.BUSY:
            return self.ServerResponse.build(ServerCommands.FETCH_FIGHTER,self.state)
        
        
        link = data["link"]
        #check cache for data
        if link in self.fighter_data_cache:
            return self.ServerResponse.build(ServerCommands.FETCH_FIGHTER,self.state,
                self.fighter_data_cache[link])
        #return last fighter fetch, could be wrong not my issue
        if ServerCommands.FETCH_FIGHTER in self.cache:
            return self.ServerResponse.build(ServerCommands.FETCH_FIGHTER,self.state,
                self.cache.pop(ServerCommands.FETCH_FIGHTER))
        

        # if self.workerThread == None or not self.workerThread.is_alive():
        #returns in format 
        """ 
            link:{
                k0:val_0
                k1:val_1
                ...
                kn:val_n
            }
                
        """
        self.startWorker(
            serverCommand=ServerCommands.FETCH_FIGHTER,
            workerFunc=scraper.scrape_fighter_data,#scrapy_worker.runScrapyFetchFighter,
            workerArgs=[self.data_q,link]
        )

        """
            how to make this be step based so same fighter is not fetched multiple times 

            event_fighter.json
            event 
                fighter_link 
                    data | None if some error 
                fighter_link 
                    data | None if some error
                
        """

        return self.ServerResponse.build(ServerCommands.FETCH_FIGHTER,self.state,{"message" : "Server starting scraper workers..."})

    def handle_fetch_event(self, data: dict = {}) -> dict: 
        if self.state == ServerStates.BUSY:
            #return its busy working
            return self.ServerResponse.build(ServerCommands.FETCH_EVENT_LATEST,self.state)
       
        #check file exists
        
        if not self.isFightEventDataAvailable(abs_filepath=self.fightEventFileNameAbs):
            rprint(f"Fight event [bold magenta]data not available or stale[/bold magenta], starting scraper worker thread...")
            #file does not exist start worker thread to fetch data
            # if self.workerThread == None or not self.workerThread.is_alive():
            self.startWorker(
                ServerCommands.FETCH_EVENT_LATEST,
                workerFunc=scraper.scrape_event,#scrapy_worker.runScrapyFetchEvent,
                workerArgs=[self.data_q])
            return self.ServerResponse.build(ServerCommands.FETCH_EVENT_LATEST,self.state,{"message":"Server starting scraper workers..."})
        
        return self.ServerResponse.build(ServerCommands.FETCH_EVENT_LATEST, self.state, self.getDataFromFile(abs_filepath=self.fightEventFileNameAbs))
        
    def handle_fetch_fighter_multi(self, data: dict={}) -> dict:
        if self.state == ServerStates.BUSY:
            return self.ServerResponse.build(ServerCommands.FETCH_FIGHTER_MULTI,self.state)

        #not busy idle check if in cache
        if ServerCommands.FETCH_FIGHTER_MULTI in self.cache:
            return self.cache.pop(ServerCommands.FETCH_FIGHTER_MULTI)

        links = data['links']
        # print(links)
        """
            contains a list in this form -> [
                matchup-index:int
                link:str

                matchup-index:int
                link:str
                ...
            ]
        """
        self.startWorker(
            serverCommand=ServerCommands.FETCH_FIGHTER_MULTI,
            workerFunc=scrapy_worker.runScrapyFetchFighterMulti,
            workerArgs=[self.data_q,links]
        )
        return self.ServerResponse.build(ServerCommands.FETCH_FIGHTER_MULTI,self.state,{"message":"Starting scrapy workers..."})


    def startWorker(self,serverCommand: ServerCommands, workerFunc, workerArgs: list):
        self.state = ServerStates.BUSY
        self.working_on = serverCommand
        self.workerThread = threading.Thread(
            target=workerFunc,
            args=workerArgs
            )
        self.workerThread.start()

    def isFightEventDataAvailable(self,abs_filepath: str):
        filePath = Path(abs_filepath)
        # rprint(f"Checking for fight event data file at [bold magenta]<{filePath}>[/bold magenta]\n{filename}")
        #check if file exists
        if filePath.is_file():
            #if exists check if is stale
            isStale = False
            with open(filePath,"r",encoding="utf-8") as file:
                data = json.load(file)
                eventDate = datetime.strptime(data['event']['date'],"%Y-%m-%d").date()
                today = datetime.today().date()
                # rprint('date diff => ',today,eventDate)
                #eventDate is in the past
                if eventDate < today:
                    isStale = True
            #if stale date not available if not stale date is available
            rprint(f"Fight event data file found. Data is: [bold magenta]{'Stale' if isStale else 'Valid'}[/bold magenta]")
            return not isStale 
        rprint(f"Fight event [bold magenta]data file not found.[/bold magenta]")
        return False

    def getDataFromFile(self,abs_filepath: str):
        data = {}
        try:
            with open(abs_filepath,"r",encoding="utf-8") as file:
                data = json.load(file)
        except OSError as e:
            print("Error opening fight event data file.",e)
        return data

def timeout(seconds=DEFAULT_SERVER_TIMEOUT_S):
    return seconds * 1000

def run_server():
    with ScraperServer(serverPort=42069) as server:
        server.run()

if __name__ == "__main__":
    run_server()
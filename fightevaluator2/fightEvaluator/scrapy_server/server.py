
import zmq
import threading 
import json
import os

from queue import Queue
from rich import print as rprint
from enum import Enum
from commands import ServerCommands,ServerStates
from pathlib import Path
from datetime import datetime


import scrapy_worker

DEFAULT_SERVER_TIMEOUT_S = 60# seconds

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

    def timeout(self,seconds):
        return seconds * 1000

    def run(self):
        self.running = True
        rprint(f"[bold green]Server running on port {self.port}[/bold green]")
        #Keyboard interrupt doesn't work when poller.poll is called
        #if you want to use keyboard interrupts need to run server in background thread 
        #and allow user to stop from main thread
        while self.running:
            events = self.poller.poll(timeout(DEFAULT_SERVER_TIMEOUT_S))
            
            if events == []:
                #no events
                rprint(f"[bold red]No requests within {DEFAULT_SERVER_TIMEOUT_S} seconds.[/bold red]")
                break

            message = self.socket.recv_pyobj()
            rprint(f"[bold yellow]Received message: {message}[/bold yellow]")
            self.handle_message(message)

        self.state = ServerStates.SHUTTING_DOWN

    def handle_message(self,message):
        rprint(f"[bold yellow]Received message: {message}[/bold yellow]")
        response = self.process_message(message)
        self.send_response(response)
    
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

    def process_message(self, message: dict):
        """Validate and route the command."""
        if not isinstance(message, dict) or "command" not in message:
            return {"error": "Invalid message format"}

        try:
            cmd = ServerCommands(message["command"])
        except ValueError:
            return {"error": f"Unknown command: {message['command']}"}

        handler = self.command_handlers.get(cmd)
        if handler is None:
            return {"error": f"Invalid command/Unsupported command {cmd.value}"}

        return handler(message)

    def handle_server_state(self, msg) -> dict:
        return {
            "result": "SERVER_STATE",
            "state": self.state.value
        }

    def handle_kill_server(self, msg) -> dict:
        self.running = False
        return {"result": "KILL_SERVER", "status": "Server shutting down"}

    # ------------------------------------------------------------------

class ScraperServer(ZmqRepServer):

    def __init__(self, serverPort, timeoutSeconds = DEFAULT_SERVER_TIMEOUT_S):
        super().__init__(serverPort, timeoutSeconds)
        
        self.fightEventFileName = "fight-event-data.json"#use one file for event and matchups
        
        script_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(script_dir, f"{self.fightEventFileName}")
        
        self.fightEventFileNameAbs = file_path
        self.data_q = Queue()#thread safe queue for data from worker to server
        self.workerThread = None

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

        response = {
            "result":ServerCommands.SERVER_STATE.value,
            "state":self.state.value
        }

        match ServerCommands[command]:
            case ServerCommands.SERVER_STATE:
                response = {
                    "result": ServerCommands.SERVER_STATE.value,
                    "state": self.state.value
                }
            case ServerCommands.FETCH_EVENT_LATEST:
                response = self.handle_fetch_event(data)
            case ServerCommands.FETCH_FIGHTER: 
                response = self.handle_fetch_fighter(data)
            case ServerCommands.FETCH_FIGHTER_MULTI: 
                # self.handle_fetch_fighter_multi
                pass
            case ServerCommands.KILL_SERVER:
                self.running = False
                response = {"result": "KILL_SERVER", "status": "Server shutting down"}
        super().send_response(response)

    def process_data_q(self):
        #process data in the q before processing new messages
        if not self.data_q.empty():
            print("data q non empty")
            data = self.data_q.get()
            #add to in memory cache
            rprint(f"Processing data from worker thread for [bold magenta]command: {self.working_on}[/bold magenta]")
            match self.working_on:
                case ServerCommands.FETCH_EVENT_LATEST:

                    self.cache[ServerCommands.FETCH_EVENT_LATEST] = data

                    with open(self.fightEventFileNameAbs,"w",encoding="utf-8") as file:
                        json.dump(data,file,indent=4,default=str)
                    
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
                    self.cache[ServerCommands.FETCH_FIGHTER] = data

                case ServerCommands.FETCH_FIGHTER_MULTI:
                    self.cache[ServerCommands.FETCH_FIGHTER_MULTI] = data
            self.working_on = None
            if self.workerThread != None:
                self.workerThread.join()
                self.workerThread = None
            self.state = ServerStates.IDLE
    
    def handle_fetch_fighter(self, data:dict) -> dict:
        if self.state == ServerStates.BUSY:
            return {
                "result": ServerCommands.FETCH_FIGHTER.value,
                "state": self.state.value
            }
        
        #check cache for data
        #return last fighter fetch, could be wrong not my issue
        if ServerCommands.FETCH_FIGHTER in self.cache:
            return {
                'result':ServerCommands.FETCH_FIGHTER.value,
                'state':self.state.value,
                'data':self.cache.pop(ServerCommands.FETCH_FIGHTER)
            }
        
        link = data["link"]

        # if self.workerThread == None or not self.workerThread.is_alive():
        self.startWorker(
            serverCommand=ServerCommands.FETCH_FIGHTER,
            workerFunc=scrapy_worker.runScrapyFetchFighter,
            workerArgs=[self.data_q,link]
        )

        return {
            "result": ServerCommands.FETCH_FIGHTER.value,
            "state":self.state.value,
            "data" : "Server starting scraper workers..."
        }

    def handle_fetch_event(self, data: dict = {}) -> dict: 
        if self.state == ServerStates.BUSY:
            #return its busy working
            return {
                "result": ServerCommands.FETCH_EVENT_LATEST.value,
                "state" : ServerStates.BUSY.value,
            }
       
        #check file exists
        response = {
            "result": ServerCommands.FETCH_EVENT_LATEST.value,
            "state": self.state.value,
            "data" : "Server starting scraper workers..."
        }
        if not self.isFightEventDataAvailable(abs_filepath=self.fightEventFileNameAbs):
            rprint(f"Fight event [bold magenta]data not available or stale[/bold magenta], starting scraper worker thread...")
            #file does not exist start worker thread to fetch data
            # if self.workerThread == None or not self.workerThread.is_alive():
            self.startWorker(
                ServerCommands.FETCH_EVENT_LATEST,
                workerFunc=scrapy_worker.runScrapyFetchEvent,
                workerArgs=[self.data_q])
        else:
            response['data'] = self.getDataFromFile(abs_filepath=self.fightEventFileNameAbs)
        return response
    
    def handle_fetch_fighter_multi(self, data: dict={}) -> dict:
        if self.state == ServerStates.BUSY:
            return {
                "result" : ServerCommands.FETCH_FIGHTER_MULTI.value,
                "state" : ServerStates.BUSY.value
            }

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
        return {
            "result": ServerCommands.FETCH_FIGHTER_MULTI.value,
            "data" : "Server starting scraper workers..."
        }


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

def server_test():
    with zmq.Context() as context:
        with context.socket(zmq.REP) as socket:
            
            socket.setsockopt(zmq.LINGER, 0)#don't block when trying to close
            socket.bind("tcp://*:42069")
            poller = zmq.Poller()
            poller.register(socket, zmq.POLLIN)

            while True:
                events = poller.poll(timeout(DEFAULT_SERVER_TIMEOUT_S))
                
                if events == []:
                    #no events
                    rprint(f"[bold red]No requests within {DEFAULT_SERVER_TIMEOUT_S} seconds.[/bold red]")
                    break
                else:
                    #message available 
                    message = socket.recv_pyobj()
                    rprint(f"Received message: {message}")

                    if message['action'] == 'kill':
                        #kill server 
                        socket.send_pyobj({
                            'server':'server closing...'
                        })
                        break
                    socket.send_pyobj({
                        'server':'hello from server! I got your message'
                    })
            poller.unregister(socket)

def run_server():
    with ScraperServer(serverPort=42069) as server:
        server.run()

if __name__ == "__main__":
    run_server()

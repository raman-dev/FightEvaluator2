
import zmq
import threading 
import json

from queue import Queue
from rich import print as rprint
from enum import Enum
from commands import ServerCommands
from pathlib import Path
from datetime import datetime


import scrapy_worker

DEFAULT_SERVER_TIMEOUT_S = 60# seconds
    
class ServerStates(Enum):
    IDLE = "IDLE"
    BUSY = "BUSY"
    SHUTTING_DOWN = "SHUTTING_DOWN"
    """
    
        what does the server do?
        - listen for commands from clients
        - respond to commands
        - do work in the background 
        - maintain state
    """

#do the work of scraping and parsing

class Server:
    def __init__(self,serverPort: int,timeoutSeconds: int = DEFAULT_SERVER_TIMEOUT_S):
        self.port = serverPort
        self.timeout = timeoutSeconds

        # Create a command router
        self.command_handlers = {
            ServerCommands.SERVER_STATE: self.handle_server_state,
            ServerCommands.FETCH_EVENT_LATEST: self.handle_fetch_event,
            ServerCommands.FETCH_FIGHTER: self.handle_fetch_fighter,
            ServerCommands.FETCH_FIGHTER_MULTI: self.handle_fetch_fighter_multi,
            ServerCommands.KILL_SERVER: self.handle_kill_server,
        }

        self.state = ServerStates.IDLE
        self.running = False
        
        self.fightEventFileName = "fight-event-data.json"#use one file for event and matchups
        self.data_q = Queue()#thread safe queue for data from worker to server
        self.workerThread = None
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
        #if you want to use keyboard interrupts
        #need to run server in background thread 
        #and allow user to stop from main thread
        while self.running:
            events = self.poller.poll(timeout(DEFAULT_SERVER_TIMEOUT_S))
            
            if events == []:
                #no events
                rprint(f"[bold red]No requests within {DEFAULT_SERVER_TIMEOUT_S} seconds.[/bold red]")
                break

            message = self.socket.recv_pyobj()
            rprint(f"[bold yellow]Received message: {message}[/bold yellow]")

            response = self.process_message(message)
            self.socket.send_pyobj(response)

        self.state = ServerStates.SHUTTING_DOWN

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

    # ------------------------------------------------------------------
    # HANDLERS
    # ------------------------------------------------------------------


    def checkDataIsAvailable(self,filename: str):
        filePath = Path(filename)
        #check if file exists
        if filePath.is_file():
            #if exists check if is stale
            isStale = False
            with open(filePath,"r",encoding="utf-8") as file:
                data = json.load(file)
                date_str = data['event']['date']
                eventDate = datetime.strptime(data['event']['date'],"%Y-%m-%d")
                today = datetime.today()
                #eventDate is in the past
                if eventDate < today:
                    isStale = True
            #if stale date not available if not stale date is available
            return not isStale 
        return False

    def getDataFromFile(self,filename: str):
        data = {}
        try:
            with open(filename,"r",encoding="utf-8") as file:
                data = json.load(file)
        except OSError as e:
            print("Error opening fight event data file.",e)
        return data 
       
    def handle_server_state(self, msg) -> dict:
        return {
            "result": "SERVER_STATE",
            "state": self.state.value
        }

    def handle_fetch_event(self, msg) -> dict: 
        if self.state == ServerStates.BUSY:
            #check q for data 
            if self.data_q.empty():
                #return its busy working
                return {
                    "result":ServerCommands.FETCH_EVENT_LATEST.value,
                    "state" : ServerStates.BUSY.value,
                }
            #non empty queue 
            #grab data and write to file 
            data = self.data_q.get()

            with open(self.fightEventFileName,"w",encoding="utf-8") as file:
                json.dump(data,file,indent=4,default=str)
            
            self.state = ServerStates.IDLE
            self.workerThread.join()
            self.workerThread = None
            return {
                "result":ServerCommands.FETCH_EVENT_LATEST.value,
                "data" : data
            }
        #do the work in a background thread
        """

            scrapy worker correctly returns data

            data is written to json file

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
        #check file exists
        if self.checkDataIsAvailable(self.fightEventFileName):
            return self.getDataFromFile(self.fightEventFileName)
        else:
            #file does not exist start worker thread to fetch data
            if self.workerThread == None or not self.workerThread.is_alive():
                self.state = ServerStates.BUSY
                self.workerThread = threading.Thread(
                    target=scrapy_worker.runScrapyFetchEvent,
                    args=[self.data_q]
                    )
                self.workerThread.start()
                return {
                    "result": ServerCommands.FETCH_EVENT_LATEST.value,
                    "data" : "Server starting scraper workers..."
                }
        return {
            "result": ServerCommands.FETCH_EVENT_LATEST.value,
            "data": f"Should not reach here check if server is operating correctly"
        }

    def handle_fetch_fighter(self, msg) -> dict:
        # link = msg.get("fighter_link")
        return {
            "result": "FETCH_FIGHTER",
            # "fighter_link": link,
            "data": f"Mock fighter data for fighter_link"
        }

    def handle_fetch_fighter_multi(self, msg) -> dict:
        # links = msg.get("fighter_links", [])
        return {
            "result": "FETCH_FIGHTER_MULTI",
            # "requested": links,
            "data": "Fetching data for multiple fighters"
        }

    def handle_kill_server(self, msg) -> dict:
        self.running = False
        return {"result": "KILL_SERVER", "status": "Server shutting down"}

    # ------------------------------------------------------------------



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
    with Server(serverPort=42069) as server:
        server.run()

if __name__ == "__main__":
    run_server()

import zmq
from rich import print as rprint
from enum import Enum
from commands import ServerCommands


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
class Server:
    def __init__(self,serverPort: int,timeoutSeconds: int = DEFAULT_SERVER_TIMEOUT_S):
        self.port = serverPort
        self.timeout = timeoutSeconds
        self.state = ServerStates.IDLE

        # Create a command router
        self.command_handlers = {
            ServerCommands.SERVER_STATE: self.handle_server_state,
            ServerCommands.FETCH_EVENT: self.handle_fetch_event,
            ServerCommands.FETCH_FIGHTER: self.handle_fetch_fighter,
            ServerCommands.FETCH_FIGHTER_MULTI: self.handle_fetch_fighter_multi,
            ServerCommands.KILL_SERVER: self.handle_kill_server,
        }

        self.running = False

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
        while True:
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

    def handle_server_state(self, msg):
        return {
            "result": "SERVER_STATE",
            "state": self.state.value
        }

    def handle_fetch_event(self, msg):
        event_id = msg.get("event_id")
        # TODO: fetch event data here
        return {
            "result": "FETCH_EVENT",
            "event_id": event_id,
            "data": f"Mock event data for {event_id}"
        }

    def handle_fetch_fighter(self, msg):
        link = msg.get("fighter_link")
        return {
            "result": "FETCH_FIGHTER",
            "fighter_link": link,
            "data": f"Mock fighter data for {link}"
        }

    def handle_fetch_fighter_multi(self, msg):
        links = msg.get("fighter_links", [])
        return {
            "result": "FETCH_FIGHTER_MULTI",
            "requested": links,
            "data": [f"Mock fighter data for {l}" for l in links]
        }

    def handle_kill_server(self, msg):
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

import zmq
from rich import print as rprint
from enum import Enum

    
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
    def __init__(self,serverPort: int,timeoutSeconds: int):
        self.port = serverPort
        self.timeout = timeoutSeconds
        self.state = ServerStates.IDLE

    def start(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.setsockopt(zmq.LINGER, 0)#don't block when trying to close
        self.socket.bind(f"tcp://*:{self.port}")
        
        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)

        rprint(f"[bold green]Server started on port {self.port}[/bold green]")

    def timeout(self,seconds):
        return seconds * 1000

    def run(self):
        while True:
            events = poller.poll(timeout(DEFAULT_SERVER_TIMEOUT))
            
            if events == []:
                #no events
                rprint(f"[bold red]No requests within {DEFAULT_SERVER_TIMEOUT} seconds.[/bold red]")
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

    def stop(self):
        self.poller.unregister(self.socket)
        self.socket.close()
        self.context.term()
        rprint(f"[bold red]Server stopped[/bold red]")

DEFAULT_SERVER_TIMEOUT = 5 * 60#5 MINIUTES

def timeout(seconds=DEFAULT_SERVER_TIMEOUT):
    return seconds * 1000
with zmq.Context() as context:
    with context.socket(zmq.REP) as socket:
        
        socket.setsockopt(zmq.LINGER, 0)#don't block when trying to close
        socket.bind("tcp://*:42069")
        poller = zmq.Poller()
        poller.register(socket, zmq.POLLIN)

        while True:
            events = poller.poll(timeout(DEFAULT_SERVER_TIMEOUT))
            
            if events == []:
                #no events
                rprint(f"[bold red]No requests within {DEFAULT_SERVER_TIMEOUT} seconds.[/bold red]")
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

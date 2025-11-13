import zmq
from rich import print as rprint
from enum import Enum

class ServerCommands(Enum):
    """
        what are commands
        command message
        action: state

        action: fetch
        type : event

        action: fetch
        type: fighter
        link: fighter_link expect
    """
    SERVER_STATE = "SERVER_STATE"
    FETCH_EVENT = "FETCH_EVENT"
    FETCH_FIGHTER = "FETCH_FIGHTER"
    FETCH_FIGHTER_MULTI = "FETCH_FIGHTER_MULTI"
    KILL_SERVER = "KILL_SERVER"

#NOTE ZMQ request socket wrapper
class Client:
    """
        what does the client do? 
         - send commands to server
         - receive responses from server
    """
    def __init__(self,serverPort: int,serverAddress: str = "localhost",clientTimeoutSeconds: int = 5):
        self.port = serverPort
        self.address = serverAddress
        self.context = None
        self.clientTimeoutSeconds = clientTimeoutSeconds

    def connect(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.setsockopt(zmq.LINGER,0)#must be set so pending messages are
        self.socket.setsockopt(zmq.SNDTIMEO, self.clientTimeoutSeconds * 1000)#send timeout
        self.socket.setsockopt(zmq.RCVTIMEO, self.clientTimeoutSeconds * 1000)#receive timeout

        self.socket.connect(f"tcp://{self.address}:{self.port}")
    
    def disconnect(self):
        self.socket.close()
        self.context.term()
    
    def send_command(self,command: ServerCommands):
        self.socket.send_pyobj(command)
        response = self.socket.recv_pyobj()
        return response

    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()

    
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

from .commands import ServerCommands,ServerStates
#uncomment when useing testClient
# from commands import ServerCommands,ServerStates 
import zmq
from rich import print as rprint
import time

from django.db import models
# from ..models import  WeightClass,Assessment
# from ..forms import FighterForm

DEFAULT_CLIENT_TIMEOUT_SECONDS = 15
#NOTE ZMQ request socket wrapper
class ZmqReqClient:
    """
        what does the client do? 
         - send commands to server
         - receive responses from server
    """
    def __init__(self,serverPort: int,
                 serverAddress: str = "localhost",
                 clientTimeoutSeconds: int =DEFAULT_CLIENT_TIMEOUT_SECONDS,maxRetries: int=15,retryDelaySeconds: int=3):
        self.port = serverPort
        self.address = serverAddress
        self.context = None
        self.clientTimeoutSeconds = clientTimeoutSeconds
        self.MAX_RETRIES = maxRetries
        self.RETRY_DELAY_S = retryDelaySeconds

    def connect(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        
        self.socket.setsockopt(zmq.LINGER,0)#must be set so pending messages are cleared from buffer
        self.socket.setsockopt(zmq.SNDTIMEO, self.clientTimeoutSeconds * 1000)#send timeout
        self.socket.setsockopt(zmq.RCVTIMEO, self.clientTimeoutSeconds * 1000)#receive timeout
        
        self.poller = zmq.Poller()
        self.poller.register(self.socket,zmq.POLLIN)

        self.socket.connect(f"tcp://{self.address}:{self.port}")
    
    def disconnect(self):
        self.poller.unregister(self.socket)
        self.socket.close()
        self.context.term()

        self.poller = None
        self.socket = None  
        self.context = None

    
    def send_command(self,command: ServerCommands,data: dict = {}):
        if type(command) != ServerCommands:
            raise ValueError("Command arg is not of type ServerCommand")
        
        self.socket.send_pyobj({
            'command': command.value,
            'data':data
        })
        
        event_mask = self.socket.poll(self.timeout(self.clientTimeoutSeconds))

        if (event_mask & zmq.POLLIN) != 0:
            #we have an object to receive
            response = self.socket.recv_pyobj()
            return response
        
        raise TimeoutError("Client socket timed out, server did not send timely response")
    
    def sendCommandRetryLoop(self,command: ServerCommands,data: dict = {}):
        attempts = 0
        while attempts < self.MAX_RETRIES:
            try: 
                response = self.send_command(command,data)
                if response['state'] != ServerStates.BUSY.value:
                    return response
                attempts += 1
                time.sleep(self.RETRY_DELAY_S)
            except TimeoutError as te:
                rprint("[bold red]Client timed out.[/bold red] Check server")
                break
        rprint("[bold cyan] Client MAX_RETRIES reached![/bold cyan]")
        return None

    def timeout(self,seconds):
        return seconds * 1000

    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()


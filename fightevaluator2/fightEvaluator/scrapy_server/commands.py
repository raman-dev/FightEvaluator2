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
    FETCH_EVENT_LATEST = "FETCH_EVENT_LATEST"
    FETCH_FIGHTER = "FETCH_FIGHTER"
    FETCH_FIGHTER_MULTI = "FETCH_FIGHTER_MULTI"
    FETCH_EVENT_RESULTS = "FETCH_EVENT_RESULTS"
    KILL_SERVER = "KILL_SERVER"


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
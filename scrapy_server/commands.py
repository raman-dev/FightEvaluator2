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
import zmq
from enum import Enum
# import json
#read config file for port number
PORT = 42069

from rich import print as rprint

class Commands(Enum):
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

    SERVER_STATE = {
        "action":"state"
    }

    FETCH_EVENT = {
        "action":"fetch",
        "type":"event"
    }

    FETCH_FIGHTER = {
        "action":"fetch",
        "type":"single-fighter",
        "link":"fighter-link"
    }

    FETCH_FIGHTER_MULTI = {
        "action":"fetch",
        "type":"many-fighter",
        "links":[
            {"name":"fighter-a","link":"fighter-a-link"},
            {"name":"fighter-b","link":"fighter-b-link"},
        ]
    }

    KILL_SERVER = {
        "action":"kill"
    }

# for command in Commands:
#     rprint(command,command.value)

def print_menu():
    print("\n=== Scrapy Server Test Client ===")
    for i,command in enumerate(Commands):
        print(f"{i + 1}. {command.name}")
    
    print("m. Print menu")
    print("q. Quit client")
    print("===============================")



DEFAULT_TIMEOUT = 5#seconds
def timeout(seconds=DEFAULT_TIMEOUT):
    return seconds * 1000

def runTestClient():
    with zmq.Context() as context:
        with context.socket(zmq.REQ) as socket:
            socket.connect(f"tcp://localhost:{PORT}")
            poller = zmq.Poller()
            poller.register(socket, zmq.POLLIN)

            commandMap = {}
            for i,cmd in enumerate(Commands):
                commandMap[i + 1] = cmd.name
            print_menu()

            while True:
                userin = input("Select an option: ").strip()
                if userin != "q" and userin != "m" and not userin.isnumeric():
                    print("invalid input")
                    continue
                if userin == "q":
                    break
                if userin == "m":
                    print_menu()
                    continue
                key = int(userin)
                if key not in commandMap:
                    print("invalid command")
                    continue

                choice = commandMap[int(userin)]
                print(Commands[choice])
                socket.send_pyobj(Commands[choice].value)
                socketEvents = poller.poll(timeout(seconds=5))
                socket,event_mask = socketEvents[0]

                if (event_mask & zmq.POLLIN) != 0:
                    message = socket.recv_pyobj()
                    rprint(f"[bold green]Received reply:[/bold green] {message}")
                else:
                    rprint(f"[bold red]No response from server within {DEFAULT_TIMEOUT} seconds.[/bold red]")
                    socket.close()
                    break

            poller.unregister(socket)


if __name__ =="__main__":
    runTestClient()
"""
    testClient for scrapy server
    do what test all commands and states
    of the server

    command 1
        scrape event
    command 2
        scrape fighter 
        info
    
    server states
        idle
        working
    
    incoming message format?

        
    
    outgoing message format
        message:data
        action:fetch
        type: event
        data: some_data

        message:state 
        data: server_data              
"""

import zmq
from enum import Enum
from scraper_client import ZmqReqClient,DEFAULT_CLIENT_TIMEOUT_SECONDS
from commands import ServerCommands,ServerStates
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
    for i,command in enumerate(ServerCommands):
        print(f"{i + 1}. {command.name}")
    
    print("m. Print menu")
    print("q. Quit client")
    print("===============================")


DEFAULT_TIMEOUT = 5#seconds
def timeout(seconds=DEFAULT_TIMEOUT):
    return seconds * 1000


commandMap = {}
for i,cmd in enumerate(ServerCommands):
    commandMap[i + 1] = cmd.name

def inputLoop(socket):
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
        event_mask = socket.poll(timeout(seconds=5))

        # if socketEvents == []:
        #     rprint(f"[bold red]No response from server within {DEFAULT_TIMEOUT} seconds.[/bold red]")
        #     socket.close()
        #     break

        
        # socket,event_mask = socketEvents[0]
        if (event_mask & zmq.POLLIN) != 0:
            message = socket.recv_pyobj()
            rprint(f"[bold green]Received reply:[/bold green] {message}")
            if Commands[choice] == Commands.KILL_SERVER:
                rprint("Client will now close.")
                break
        else:
            rprint(f"[bold red]No response from server within {DEFAULT_TIMEOUT} seconds.[/bold red]")
            socket.close()
            break

def runTestClient():
    with ZmqReqClient(serverPort=PORT) as client:
        # breakLoop = False
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

            print(ServerCommands[choice])
            data = {}
            match ServerCommands[choice]:
                case ServerCommands.SERVER_STATE:
                    data = {}
                case ServerCommands.FETCH_EVENT_LATEST:
                    data = {}
                case ServerCommands.FETCH_EVENT_RESULTS:
                    data = {
                        # 'link':"https://www.tapology.com/fightcenter/events/130635-ufc-fight-night" 2025 link
                        'link':"https://www.tapology.com/fightcenter/events/136549-ufc-325-volkanovski-vs-lopes-2"#2026 link
                    }
                case ServerCommands.FETCH_FIGHTER:
                    data = {
                        'link':'https://www.tapology.com/fightcenter/fighters/32797-belal-muhammad'
                    }
                case ServerCommands.FETCH_FIGHTER_MULTI:
                    data = {
                        'links':[
                            {'matchup-index':0,'link':'https://www.tapology.com/fightcenter/fighters/115752-arman-tsarukyan'},
                            {'matchup-index':1,'link':'https://www.tapology.com/fightcenter/fighters/171377-ian-garry'}
                        ]
                    }
                case ServerCommands.KILL_SERVER:
                    data = {}
            
            try:
                response = client.send_command(ServerCommands[choice],data=data)
                rprint(f"[bold green]Server response: [/bold green]\n [cyan]{response}")
            except TimeoutError as te:
                rprint(f"[bold red]Client Timed Out. No response from server within {DEFAULT_CLIENT_TIMEOUT_SECONDS} seconds.[/bold red]")
                break

        
    # with zmq.Context() as context:
    #     with context.socket(zmq.REQ) as socket:
            
    #         socket.setsockopt(zmq.LINGER,0)#must be set so pending messages are 
    #         #discarded and when term and disconnect are called
    #         socket.setsockopt(zmq.SNDTIMEO,timeout(seconds=5))#send timeout
    #         socket.setsockopt(zmq.RCVTIMEO,timeout(seconds=5))#receive timeout

    #         socket.connect(f"tcp://localhost:{PORT}")
    #         poller = zmq.Poller()
    #         poller.register(socket, zmq.POLLIN)

            
    #         print_menu()

    #         try:
    #             inputLoop(socket)
    #         except KeyboardInterrupt:
    #             print("Ending client..")
           
    #         poller.unregister(socket)


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

from datetime import datetime
import time

from .. import scraper
from ..forms import MatchUpFormMF, FightEventForm, FighterForm
from ..models import Fighter, Assessment, FightEventDataState, WeightClass

from ..scrapy_server.commands import ServerCommands
from ..scrapy_server import scraper_client

from rich import print as rprint
from django.db.models import Q
from django.db import transaction

PORT = 42069

def ScrapyFightEventControlFunction():
    #this function is launched when the newest event has not been fetched or created
    """
        do what here
        launch a scrapy process with a pool
            scrapy process
                query fight event for page source
                break into matchups with fighter links and names
                return to thread
            if all fighters of matchups in db
                save all matchups with corresponding fighter objects
            else:
                queue list of unknown fighters
                launch scrapy process to fetch fighter data
                    return fighter info to thread
                create fighter objects
                save all matchups with corresponding fighter objects  

            complete
        **NOTE**
        CANNOT USE ProcessPoolExecutor since it may reuse an existing 
        process in the pool and scrapy does not allow the underlying
        twisted.reactor to be restarted once completed in the same process

        MUST CREATE A NEW PROCESS FOR EACH TIME I WANT TO USE SCRAPY
    """
    # attempts = 0
    with transaction.atomic():
        fightEventDataState = FightEventDataState.objects.select_for_update().first()
        with scraper_client.ZmqReqClient(serverPort=PORT) as client:
            #response = fetcher.nextEvent()
            response = client.sendCommandRetryLoop(command=ServerCommands.FETCH_EVENT_LATEST)
            fighterData = response['data']
            
            fightEventData = fighterData['event']
            matchupsRaw = fighterData['matchups']
            matchups = []
            rprint(matchupsRaw)
            
            fightEventForm = FightEventForm(fightEventData)
            fightEvent = None
            if fightEventForm.is_valid():
                # fightEvent = fightEventForm.save()
                rprint("[bold cyan]Event Valid[/bold cyan]")
                
            for matchupData in matchupsRaw:
                rprint("")
                matchup = {
                    'weight_class':scraper.poundsToWeightClass(matchupData['weight_class']),
                    'rounds':matchupData['rounds'],
                    'isprelim':matchupData['isprelim']
                }
                for i,fighter in enumerate(matchupData['fighters_raw']):
                    #check if fighter is in database
                    name = fighter['name']
                    names = list(map(lambda x: x.lower(), name.split(' ')))
                    name_index = "-".join(names)#search using this
                    first_name = names[0]#try only first name
                    last_name = names[-1]#last name may include middle name
                    if len(name) > 1:
                        last_name = " ".join(names[1:])

                    rprint("\t",first_name,last_name,name_index)

                    first_name_and_last_name_contains=Q(first_name=first_name) & Q(last_name__contains=last_name)
                    query_a = first_name_and_last_name_contains
                    fighterObj = Fighter.objects.filter(name_index=name_index).first()
                    if not fighterObj:            
                        fighterObj = Fighter.objects.filter(query_a).first()
                        if fighterObj == None:
                            rprint("No fighter object found")
                            # response = fetcher.fetchFighter(link=fighter['link'])
                            response = client.sendCommandRetryLoop(ServerCommands.FETCH_FIGHTER,data={'link':fighter['link']})
                            if response:
                                fighterData = response['data']
                                rprint(fighterData)
                                
                                fighterData['data_api_link'] = fighter['link']
                                
                                if fighterData['date_of_birth'] == 'N/A':
                                    fighterData['date_of_birth'] = None#datetime.strptime("2001-01-01","%Y-%m-%d").date()
                                
                                weight_class = WeightClass[fighterData['weight_class']]
                                fighterData['weight_class'] = weight_class
                                fighterForm = FighterForm(fighterData)#validate fighter data
                                
                                if fighterForm.is_valid():
                                    fighterObj = fighterForm.save()

                                    rprint('Valid fighter',fighterObj)
                                    assessment = Assessment(fighter=fighterObj)
                                    assessment.save()
                                    
                                    fighterObj.assessment = assessment
                                    # fighterObj.save()
                                else:
                                    rprint(fighterForm.errors)
                                    break
                            else:
                                rprint(f"[bold red]No response for fighter:{first_name} {last_name} fetch[/bold red]")
                                time.sleep(10)
                                continue #ignore this matchup
                            time.sleep(10)#need to sleep before fetching again if we have to
                    
                    if i == 0:
                        matchup['fighter_a'] = fighterObj
                    else:
                        matchup['fighter_b'] = fighterObj
                matchups.append(matchup) 
                rprint(matchup)
            
            fightEvent = fightEventForm.save()
            for m in matchups:
                m['event'] = fightEvent
                m['scheduled'] = fightEvent.date
                mf = MatchUpFormMF(m)
                if mf.is_valid():
                    mf.save()
            """     
                    event:
                    link 
                    date
                    title
                matchups: 
                    0
                        fighters_raw
                            0: name 
                                link
                            1: name
                                link
                        weight_class
                        rounds
                        isprelim

                    1   fighters_raw
                            0: name
                                link
                            1: name
                                link
                        weight_class
                        rounds
                        isprelim
                    {
            """ 
        fightEventDataState.staleOrEmpty = False
        fightEventDataState.updating = False
        # fightEventDataState.date = datetime.today().date()
        fightEventDataState.save()

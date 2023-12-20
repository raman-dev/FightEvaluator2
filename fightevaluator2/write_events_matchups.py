from fightEvaluator.models import Fighter,MatchUp,FightEvent,WeightClass
import re
from datetime import datetime
import unicodedata

def normalizeString(string):
    return unicodedata.normalize('NFD',string).encode('ascii', 'ignore').decode("ascii").lower()
#read in old_data.db file
import sqlite3
conn = sqlite3.connect("old_data.db")
c = conn.cursor()

missing_matchups = []
 
def write():
    c.execute("SELECT * FROM fightevent")
    for row in c.fetchall():
        print(row)
        event_id = row[0]
        title = row[1]
        date = row[2]
        location = row[3]

        fightEvent = FightEvent()
        fightEvent.title = title
        fightEvent.date = datetime.strptime(date,"%Y-%m-%d")
        fightEvent.location = location
        print(fightEvent)
        fightEvent.save()
        #grab matchups for this event
        for matchupRow in c.execute("SELECT * FROM matchup WHERE event_id="+str(event_id)).fetchall():
            matchup = MatchUp()
            matchup.weight_class = WeightClass[matchupRow[1]]
            fighter_a_fullName = matchupRow[2]
            split = fighter_a_fullName.split(' ')
            fighter_a_firstName = normalizeString(split[0].lower())
            fighter_a_lastName = normalizeString(" ".join(split[1:]).lower())
            fighter_a = Fighter.objects.filter(first_name=fighter_a_firstName,last_name=fighter_a_lastName).first()
            # print('    ',fighter)
            
            fighter_b_fullName = matchupRow[5]
            split = fighter_b_fullName.split(' ')
            fighter_b_firstName = normalizeString(split[0].lower())
            fighter_b_lastName = normalizeString(" ".join(split[1:]).lower())
            fighter_b = Fighter.objects.filter(first_name=fighter_b_firstName,last_name=fighter_b_lastName).first()
            # # rounds = matchupRow[5]
            matchup.fighter_a = fighter_a
            matchup.fighter_b = fighter_b
            
            if not fighter_a or not fighter_b:
                if not fighter_a:
                    print('MISSING!',fighter_a_firstName,fighter_a_lastName)
            
                if not fighter_b:
                    print('MISSING!',fighter_b_firstName,fighter_b_lastName)
                missing_matchups.append([row,matchupRow])
                continue

            print(matchupRow[-4])
            if matchupRow[-4]:
                matchup.rounds = int(matchupRow[-4].split(' ')[0])
            matchup.event = fightEvent
            print(fighter_a,'\n',fighter_b)
            print('    ',matchupRow)
            matchup.save()

write()

#write missing matchups to missing_matchups.txt
with open("missing_matchups.txt","w") as f:
    for matchup in missing_matchups:
        f.write(str(matchup)+'\n')

c.close()
conn.close()

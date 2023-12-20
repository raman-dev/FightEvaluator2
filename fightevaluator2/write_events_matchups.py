from fightEvaluator.models import Fighter,MatchUp,FightEvent,WeightClass
import re
from datetime import datetime
#read in old_data.db file
import sqlite3
conn = sqlite3.connect("old_data.db")
c = conn.cursor()

c.execute("SELECT * FROM fightevent")
counter = 0
for row in c.fetchall():
    print(row)
    event_id = row[0]
    title = row[1]
    date = row[2]
    location = row[3]
    
    #grab matchups for this event
    for matchupRow in c.execute("SELECT * FROM matchup WHERE event_id="+str(event_id)).fetchall():
        # matchup = MatchUp()
        # matchup.weight_class = WeightClass[matchupRow[1]]
        # # fighter_a = matchupRow[2]
        # # fighter_b = matchupRow[4]
        # # rounds = matchupRow[5]
        print('    ',matchupRow)

c.close()
conn.close()

from fightEvaluator.models import Fighter,WeightClass,Stance
import re
from datetime import date,datetime
#read in old_data.db file
import sqlite3
conn = sqlite3.connect("old_data.db")
c = conn.cursor()

c.execute("SELECT * FROM assessment")
counter = 0
for row in c.fetchall():
    assessment_id = row[0]
    if assessment_id > 10:
        break
    noteRow = c.execute("SELECT * FROM note WHERE assessment_id=" + str(assessment_id)).fetchone()
    print(row)

c.close()
conn.close()

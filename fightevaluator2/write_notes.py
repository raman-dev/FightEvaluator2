from fightEvaluator.models import Fighter,Assessment,Note
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
    # if assessment_id > 10:
        # break
    #need fighter object with corresponding assessment_id
    # fighterRow = c.execute("SELECT * FROM fighter WHERE assessment_id=" + str(assessment_id)).fetchone()
    #get assessment object
    # first_name = fighterRow[1]
    # last_name = fighterRow[2]
    for noteRow in  c.execute("SELECT * FROM note WHERE assessment_id=" + str(assessment_id)).fetchall():
        fighter = Fighter.objects.filter(assessment_id=assessment_id).first()
        if not fighter:
            continue
        
        assessment = Assessment.objects.filter(fighter=fighter).first()
        if not assessment:
            continue
        # print(noteRow)
        #create note objects for each noterow
        data = noteRow[2]#string data
        createdAt = noteRow[3]#string date convert to date object
        note = Note(assessment=assessment,data=data,createdAt=createdAt)
        print(fighter.first_name +" "+fighter.last_name,note)
        note.save()
        # print(note)
    # print(row)

c.close()
conn.close()

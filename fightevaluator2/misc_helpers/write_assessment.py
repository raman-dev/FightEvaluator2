from fightEvaluator.models import Fighter,Assessment
import re
from datetime import date,datetime
#read in old_data.db file
import sqlite3
conn = sqlite3.connect("old_data.db")
c = conn.cursor()

c.execute("SELECT * FROM fighter")
for row in c.fetchall():
    id = row[0]
    # if id > 100:
        # break
    assessment_id = row[10]
    if id == 0:
        continue
    print(row[0],row[1],row[2])
    if not row[10]:
        #create an assessment
        continue
    assessment_row = c.execute("SELECT * FROM assessment WHERE id="+str(row[10])).fetchone()
    if assessment_row == None:
        fighter = Fighter.objects.filter(first_name=row[1],last_name=row[2]).first()
        assessment = Assessment(fighter=fighter)
        assessment.save()
        continue
    print(assessment_row)
    fighter = Fighter.objects.filter(first_name=row[1],last_name=row[2],assessment_id=assessment_id).first()
    print(fighter.id,fighter.first_name,fighter.last_name,fighter.assessment_id)
    #create an assessment object
    assessment = Assessment(
        fighter=fighter,
        head_movement= Assessment.AttributeQualifier.UNTESTED if not assessment_row[1] else Assessment.AttributeQualifier[assessment_row[1].upper()],
        gas_tank=Assessment.AttributeQualifier.UNTESTED if not assessment_row[2] else Assessment.AttributeQualifier[assessment_row[2].upper()],
        aggression=Assessment.AttributeQualifier.UNTESTED if not assessment_row[3] else Assessment.AttributeQualifier[assessment_row[3].upper()],
        desire_to_win=Assessment.AttributeQualifier.UNTESTED if not assessment_row[4] else Assessment.AttributeQualifier[assessment_row[4].upper()],
        striking=Assessment.AttributeQualifier.UNTESTED if not assessment_row[5] else Assessment.AttributeQualifier[assessment_row[5].upper()],
        chinny=Assessment.AttributeQualifier.UNTESTED if not assessment_row[6] else Assessment.AttributeQualifier[assessment_row[6].upper()],
        grappling_offense=Assessment.AttributeQualifier.UNTESTED if not assessment_row[7] else Assessment.AttributeQualifier[assessment_row[7].upper()],
        grappling_defense=Assessment.AttributeQualifier.UNTESTED if not assessment_row[8] else Assessment.AttributeQualifier[assessment_row[8].upper()]
    )
    # print(assessment)
    assessment.save()    

c.close()
conn.close()

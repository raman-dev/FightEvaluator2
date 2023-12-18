from fightEvaluator.models import Fighter,WeightClass,Stance
import re
from datetime import date,datetime
#read in old_data.db file
import sqlite3
conn = sqlite3.connect("old_data.db")
c = conn.cursor()

#read in fighter data from old_data
#write to Fighter object 
#save Fighter object
#repeat for all 
def heightToInches(str):
    if not re.match(r"\d{2}\"",str):
        return 0
    return int(str.split("\"")[0])
def reachToInches(str):
    if not re.match(r"\d{2}\.\d{1,2}\"",str):
        return 0
    return int(str.split(".")[0])
c.execute("SELECT * FROM fighter")
counter = 0
for row in c.fetchall():
    if row[0] < 3630:
        continue
    """
        old data format:
        id: int = Field(primary_key=True)
        first_name: str
        last_name: str
        nick_name: str
        weight_class: str
        height: str
        date_of_birth: date -> format: "YYYY-MM-DD"
        reach: str
        stance: str
        record: str -> format: "W-L-D"
        assessment_id: int
        img_link: str
        
    """
    print(row)
    first_name = row[1]
    last_name = row[2]
    nick_name = row[3]
    if not nick_name:
        nick_name = "N/A"
    weight_class = WeightClass.LIGHTWEIGHT
    if row[4] and row[4].upper() in WeightClass.__members__:
        weight_class = WeightClass[row[4]]
    height = heightToInches(row[5])
    date_of_birth = None
    if row[6] and re.match(r"\d{4}-\d{2}-\d{2}",row[6]):
        split = row[6].split("-")
        date_of_birth = date(int(split[0]),int(split[1]),int(split[2]))
    reach = reachToInches(row[7])
    stance = None
    if row[8] and row[8].upper() in Stance.__members__:
        stance = Stance[row[8].upper()]
    wld = row[9]
    wins,losses,draws = 0,0,0
    if wld and re.match(r"\d+-\d+-\d+",wld):
        split = re.match(r"\d+-\d+-\d+",wld).group(0).split("-")
        wins = int(split[0])
        losses = int(split[1])
        draws = int(split[2])
    assessment_id = row[10]
    img_link = row[11]
    fighter = Fighter(
        first_name=first_name,
        last_name=last_name,
        nick_name=nick_name,
        weight_class=weight_class,
        height=height,
        date_of_birth=date_of_birth,
        reach=reach,
        stance=stance,
        wins=wins,
        losses=losses,
        draws=draws,
        assessment_id=assessment_id,
        img_link=img_link
    )
    print(fighter)
    fighter.save()
    # print(f)
    # print(f.id)
    # print("")

c.close()
conn.close()

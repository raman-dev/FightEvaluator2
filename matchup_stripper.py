import re
import beautifulsoup4
#strip matchups from the text file

def strip_matchups():
    with open('matchups.txt', 'r') as f:
        lines = f.readlines()
        """

        matchup structure
           ul.fightCard <---first result of selector query
            li.fightCard 
        
        """


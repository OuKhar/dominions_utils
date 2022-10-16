from bs4 import BeautifulSoup
import requests
import pandas as pd
import json
# also needed:
#pip install html5lib

# read config
with open('dominions_config.json', 'r') as config:
    config_data = json.load(config)

def turn_reminder(dom_website):
    # parse html page for reading the table
    dom_page = requests.get(dom_website)
    soup = BeautifulSoup(dom_page.content, "html.parser")
    turn_tbl = soup.find("table")
    dom_data = pd.read_html(str(turn_tbl))[0]

    # count players and how many have played their turn
    count_players = dom_data[0].count()
    count_turn_played = dom_data[dom_data[1] == 'Turn played'][0].count()

    # form and process string for nations not plaed their turn
    not_played = dom_data.loc[dom_data[1] != 'Turn played', [0]]
    not_played_string_original = not_played.to_string(index=False,header=False)
    not_played_string = not_played_string_original.split("\n",1)[1]
    
    # check whether there is only one player not played its turn and print relevant information 
    if count_players - count_turn_played == 1:
        print("Sunrise depending on:", not_played_string.strip())
    else:
        print("More than one nation still unplayed")
if __name__ == "__main__":
    turn_reminder(config_data["website"])
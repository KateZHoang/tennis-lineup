import os
import json 
import gspread
import time
import MatchLineupsCreation
import GetPlayerList
from google.oauth2.service_account import Credentials

# Load service account key from environment variable
secret_key = os.getenv("SERVICE_ACCOUNT_KEY")

if not secret_key:
     raise ValueError("SERVICE_ACCOUNT_KEY environment variable is not set.")

# Parse the JSON string
parsed_json = json.loads(secret_key)

# Authenticate with Google API using the JSON secret
scope = ["https://spreadsheets.google.com/feeds", 
         "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", 
         "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_info(parsed_json, scopes=scope)
client = gspread.authorize(creds)

# Access the Google Sheet tabs
round_robin_sheet = client.open_by_key("1Z3jSqZv4cikdgrajeFmP5Dd1O9NOt_f1WWFkUCCkMOo").worksheet("Copy of RR")  
player_sheet = client.open_by_key("1Z3jSqZv4cikdgrajeFmP5Dd1O9NOt_f1WWFkUCCkMOo").worksheet("Test")  


# Re-format lineup data
def reformat_lineup(lineups):
    data_to_write = {}
    for set_num, lineup_set in enumerate(lineups):
        for match_num, (team1, team2) in enumerate(lineup_set[0]):
            cell_num = 6
            cell_num += match_num + (set_num * 6)
            data_to_write["C" + str(cell_num)] = f"{team1[0].name} & {team1[1].name}"
            data_to_write["D" + str(cell_num)] = f"{team2[0].name} & {team2[1].name}"
    return data_to_write

# Fill in players to Google Sheet
def write_to_gsheet(data):
    for cell, value in data.items():
        round_robin_sheet.update(values = [[value]], range_name = cell)
        time.sleep(1) 

# Get player data
players = GetPlayerList.get_players(player_sheet)
print("The length of players are: {}".format(len(player)))

# Get lineup
lineups = MatchLineupsCreation.generate_lineups(players, sets = 3)

# Write the data to Gsheet
data = reformat_lineup(lineups)
print(data)
write_to_gsheet(data)


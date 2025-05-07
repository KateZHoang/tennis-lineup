import os
import json 
import gspread
import time
import AuthenticateGoogle
import MatchLineupsCreation
import GetPlayerList
from google.oauth2.service_account import Credentials

# Authenticate google 
creds, client = AuthenticateGoogle.authenticate_google()

# Access the Google Sheet tabs
round_robin_sheet = client.open_by_key("1pG6MNE5WRD9IikzX66HsNfme1DRZsMDVY0FUPnSnFtY").worksheet("Lineup")  
player_sheet = client.open_by_key("1pG6MNE5WRD9IikzX66HsNfme1DRZsMDVY0FUPnSnFtY").worksheet("Player_Info")  

# Get player data
players = GetPlayerList.get_players(player_sheet)

# Re-format lineup data
def reformat_lineup(lineups):
    data_to_write = {}
    for set_num, lineup_set in enumerate(lineups):
        for match_num, (team1, team2) in enumerate(lineup_set[0]):
            cell_num = 3
            cell_num += match_num + (set_num * 6)
            data_to_write["B" + str(cell_num)] = f"{team1[0].name} & {team1[1].name}"
            data_to_write["C" + str(cell_num)] = f"{team2[0].name} & {team2[1].name}"
    return data_to_write

# Fill in players to Google Sheet
def write_to_gsheet(data):
    for cell, value in data.items():
        round_robin_sheet.update(values = [[value]], range_name = cell)
        time.sleep(1) 

# Get player data
players = GetPlayerList.get_players(player_sheet)

# Get lineup
lineups = MatchLineupsCreation.generate_lineups(players, sets = 3)

# Write the data to Gsheet
data = reformat_lineup(lineups)
print(f"Player data are: {data}")
write_to_gsheet(data)


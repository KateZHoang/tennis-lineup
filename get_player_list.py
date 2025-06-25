import gspread
from google.oauth2.service_account import Credentials
import authenticate_google

# Define player class
class Player:
    def __init__(self, name, gender, level):
        self.name = name
        self.gender = gender
        self.level = level
    
    def __repr__(self):
        return f"Player({self.name}, {self.gender}, {self.level})" 

    def __lt__(self, other):
        # Compare players primarily by name, alphabetically
        return self.name < other.name

# Create player list from Google Sheet
def get_players(sheet):

    # Get player info as a list or dictionaries
    data = sheet.get_all_records()  # list of dictionaries
    rows_as_lists = [list(row.values()) for row in data]  # convert each row to list if needed

    player_list = []
    for i in rows_as_lists:
        if i[3] == 'Yes':
            player = Player(i[0], i[1], i[2])
            player_list.append(player)

    return player_list

if __name__ == "__main__":

    creds, client = authenticate_google.authenticate_google()
    player_sheet = client.open_by_key("1pG6MNE5WRD9IikzX66HsNfme1DRZsMDVY0FUPnSnFtY").worksheet("Player_Info")  

    # Get and print the player data
    players = get_players(player_sheet)
    print(f"There are {len(players)} players. The players are: {[player.name for player in players]}")
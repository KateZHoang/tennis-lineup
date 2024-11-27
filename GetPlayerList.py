import gspread
from google.oauth2.service_account import Credentials

# Define player class
class Player:
    def __init__(self, name, gender, level):
        self.name = name
        self.gender = gender
        self.level = level
    
    def __repr__(self):
        return f"Player({self.name}, {self.gender}, {self.level})"
'''
# Set up the scope and authenticate
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = Credentials.from_service_account_file("/Users/ItsKate/Downloads/googlesheetapi.json", scopes=scope)
client = gspread.authorize(creds)

# Access your Google Sheet
sheet = client.open_by_key("1Z3jSqZv4cikdgrajeFmP5Dd1O9NOt_f1WWFkUCCkMOo").worksheet("Test")  # or specify the sheet by name
'''

# Create player list from Google Sheet
def get_players(sheet):
    # Get data as a list of lists or dictionaries
    data = sheet.get_all_records()  # list of dictionaries
    rows_as_lists = [list(row.values()) for row in data]  # convert each row to list if needed

    player_list = []
    for i in rows_as_lists:
        if i[3] == 'Yes':
            player = Player(i[0], i[1], i[2])
            player_list.append(player)

    return player_list

'''
OLD CODE

# Get data as a list of lists or dictionaries
data = sheet.get_all_records()  # list of dictionaries
rows_as_lists = [list(row.values()) for row in data]  # convert each row to list if needed

player_list = []
for i in rows_as_lists:
    if i[3] == 'Yes':
        player = Player(i[0], i[1], i[2])
        player_list.append(player)

'''
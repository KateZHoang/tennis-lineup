import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from GetPlayerList import get_players
import AuthenticateGoogle

# Test GetPlayerList.py. Ensure the number of generated players in the lineup is a multiple of 4.
def test_get_player_list():

    # Authenticate google 
    creds, client = AuthenticateGoogle.authenticate_google()

    # Access the Google Sheet tabs
    player_sheet = client.open_by_key("1pG6MNE5WRD9IikzX66HsNfme1DRZsMDVY0FUPnSnFtY").worksheet("Player_Info")

    players = get_players(player_sheet)
    assert len(players) % 4 == 0
import os
import time
import random
from itertools import combinations
from authenticate_google import authenticate_google
from google.oauth2.service_account import Credentials
import gspread
from get_player_list import get_players

# -- Utility Functions --

# Sort pairs by gender and their combined levels
def sorting_key(pair):
    # Rank the pair based on gender
    genders = tuple([pair[0].gender, pair[1].gender])
    if "female" in genders and "male" in genders:
        priority = 2 # Assign a high xxx.
    else:
        priority = 1
    
    # Rank the pair based on combined level
    combined_level = pair[0].level + pair[1].level

    #Attempt to return 1 value for the function instead of 2.
    #return (priority * combined_level)

    
    return (priority, combined_level)
    

# -- Core Pairing Logic --

# Generate pairs avoiding repeats. Shuffle and pair each female with a male, and pair up the rest

#Track previous pairings to avoid repeats
previous_pairings = set()

# Generate pairs for mix.
def pair_up_mix(short_list, long_list):

    # Make a copy of short and long list
    copy_short = short_list[:]
    copy_long = long_list[:]

    # Generate pairs starting with the short list
    pairs = []

    while copy_short and copy_long:
        selected_player_from_short = random.choice(copy_short)
        selected_player_from_long = random.choice(copy_long)
        
        # Create the pair as a sorted tuple
        temp_pair = tuple(sorted((selected_player_from_short, selected_player_from_long)))

        # Only add the pairs if not already exist
        if temp_pair in previous_pairings:
            continue

        pairs.append(temp_pair)
        previous_pairings.add(temp_pair)
        
        # Remove the players from their respective lists
        copy_short.remove(selected_player_from_short)
        copy_long.remove(selected_player_from_long)

    # Generate pairs with the remaining from the long list
    if len(copy_long) > 1:
        mid = len(copy_long) // 2
        pairs += pair_up_mix(copy_long[:mid],copy_long[mid:])

    # Ensure teams have close USTA levels by pairing highest level pairs against each other
    pairs.sort(key=sorting_key, reverse=True)

    return pairs

# Generate pairs for one gender.
def pair_up_single_gender(players):

    # Make a copy of the player list
    copy_players = players[:]

    # Generate pairs starting with the short list
    pairs = []

    while copy_players:
        selected_player1 = random.choice(copy_players)
        selected_player2 = random.choice(copy_players)

        while selected_player2 == selected_player1:
            selected_player2 = random.choice(copy_players)
 
        # Create the pair as a sorted tuple
        temp_pair = tuple(sorted((selected_player1, selected_player2)))

        # Only add the pairs if not already exist
        if temp_pair in previous_pairings:
            continue

        pairs.append(temp_pair)
        previous_pairings.add(temp_pair)
        
        # Remove the players from their respective lists
        copy_players.remove(selected_player1)
        copy_players.remove(selected_player2)

    # Ensure teams have close USTA levels by pairing highest level pairs against each other
    pairs.sort(key=sorting_key, reverse=True)

    return pairs

# Generate matches with varied partners and opponents
def generate_lineups(players, sets=3):
    
    # Split males and females from player list
    males = [p for p in players if p.gender == 'Male']
    females = [p for p in players if p.gender == 'Female']

    # Split players by gender if there is more than one gender
    if males and females:
        # Decide on the short and the long list
        if len(males) != len(females):
            short = min(males, females, key=len)
            long = max(males, females, key=len)
        else:
            short = females
            long = males

    # Ensure each player has different partners in each set and balanced match levels
    lineups = []
    for s in range(sets):
        lineup_set = []

        # Pair up the players
        if "short" in locals() and short and "long" in locals() and long:
            pairs = pair_up_mix(short, long)
        else:
            pairs = pair_up_single_gender(players)

        matches = []
        for i in range(0, len(pairs), 2):
            a_match = tuple(sorted([pairs[i], pairs[i + 1]]))
            matches.append(a_match)

        # Add matches to the set
        lineup_set.append(matches)
        lineups.append(lineup_set)
    
    return lineups

# -- Debug and Validation Functions --

# Flatten the nested structure for the lineup
def iterative_flatten(nested):
    while isinstance(nested, list) and len(nested) == 1:
        nested = nested[0]  # Unpack single-element lists
    return nested

# Validate sorting_key function with flattened lineup
def validate_sorting_key(lineup):
    for i in lineup:
        print("The set is".format(i))
        
        flattened = interative_flatten(i)
        print(flattened)

# Print the generated lineup (with names, gender, and level)
def print_lineups(lineups):
    for set_num, lineup_set in enumerate(lineups, 1):
        print(f"\nSet {set_num}:")
        for match_num, (team1, team2) in enumerate(lineup_set[0], 1):
            team1_names = f"{team1[0].name} ({team1[0].gender}, {team1[0].level}) & {team1[1].name} ({team1[1].gender}, {team1[1].level})"
            team2_names = f"{team2[0].name} ({team2[0].gender}, {team2[0].level}) & {team2[1].name} ({team2[1].gender}, {team2[1].level})"
            print(f"Match {match_num}: {team1_names} vs {team2_names}")

# Print the generated lineup sets (with names only)
def print_lineups_namesonly(lineups):
    for set_num, lineup_set in enumerate(lineups, 1):
        print(f"\nSet {set_num}:")
        for match_num, (team1, team2) in enumerate(lineup_set[0], 1):
            team1_names = f"{team1[0].name} & {team1[1].name}"
            team2_names = f"{team2[0].name} & {team2[1].name}"
            print(f"Match {match_num}: {team1_names} vs {team2_names}")

# -- Entry Point --
if __name__ == "__main__":

    # Authenticate google 
    creds, client = authenticate_google()

    # Access the Google Sheet tabs
    player_sheet = client.open_by_key("1pG6MNE5WRD9IikzX66HsNfme1DRZsMDVY0FUPnSnFtY").worksheet("Player_Info")  

    # Get player data
    players = get_players(player_sheet)
    print(f"There are {len(players)} players. The players are: {[player.name for player in players]}")

    # Generate lineup and print them out formatted
    results = generate_lineups(players, sets = 3)
    results_formatted = print_lineups_namesonly(results)
    print(results_formatted)
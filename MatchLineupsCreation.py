import random
import GetPlayerList
from itertools import combinations

#Track previous pairings to avoid repeats
previous_pairings = set()

# Generate pairs avoiding repeats. Shuffle and pair each female with a male, and pair up the rest
def pair_up(short_list, long_list):
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
        pairs += pair_up(copy_long[:mid],copy_long[mid:])

    # Ensure teams have close USTA levels by pairing highest level pairs against each other
    pairs.sort(key=sorting_key, reverse=True)

    return pairs

# Define sorting function
def sorting_key(pair):
    # Rank the pair based on gender
    genders = tuple([pair[0].gender, pair[1].gender])
    if "female" in genders and "male" in genders:
        priority = 1 # Assign higher priorty as 1 to keep it consistent with the levels. The higher number is higher priority
    else:
        priority = 0
    
    # Rank the pair based on combined level
    combined_level = pair[0].level + pair[1].level

    return (priority, combined_level)

# Generate matches with varied partners and opponents
def generate_lineups(players, sets=3):
    # Split players by gender
    males = [p for p in players if p.gender == 'Male']
    females = [p for p in players if p.gender == 'Female']

    # Decide on the short and the long list
    short = min(males, females, key=len)
    long = max(males, females, key=len)

    # Ensure each player has different partners in each set and balanced match levels
    lineups = []
    for s in range(sets):
        lineup_set = []

        # Pair up the players
        pairs = pair_up(short, long)
        print("Pairs are sorting are: {}".format())
        
        matches = []
        for i in range(0, len(pairs), 2):
            a_match = tuple(sorted([pairs[i], pairs[i + 1]]))
            matches.append(a_match)

        # Add matches to the set
        lineup_set.append(matches)
        lineups.append(lineup_set)
    
    return lineups

# Print the generated lineup sets (with names, gender, and level)
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
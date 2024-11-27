import random
import GetPlayerList
from itertools import combinations

# Create a function to generate pairs with varied partners and balanced matchups
def generate_lineups(players, sets=3):
    # Split players by gender
    males = [p for p in players if p.gender == 'Male']
    females = [p for p in players if p.gender == 'Female']

    # Ensure each player has a new partner in each set and balanced match levels
    lineups = []
    for s in range(sets):
        lineup_set = []
        
        # Shuffle players to vary pairings each set
        random.shuffle(males)
        random.shuffle(females)
        
        # Pair each female with a male, and balance remaining pairs
        pairs = []
        if len(females) <= len(males):
            pairs += [(females[i], males[i]) for i in range(len(females))]
            remaining_males = males[len(females):]
            pairs += [(remaining_males[i], remaining_males[i+1]) for i in range(0, len(remaining_males), 2)]
        else:
            pairs += [(males[i], females[i]) for i in range(len(males))]
            remaining_females = females[len(males):]
            pairs += [(remaining_females[i], remaining_females[i+1]) for i in range(0, len(remaining_females), 2)]

        # Ensure teams have close USTA levels by pairing highest level pairs against each other
        pairs.sort(key=lambda pair: pair[0].level + pair[1].level, reverse=True)
        matches = []
        for i in range(0, len(pairs), 2):
            team1, team2 = pairs[i], pairs[i + 1]
            matches.append((team1, team2))

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

'''
# Get player data
players = GetPlayerList.player_list

# Generate lineups
lineups = generate_lineups(players, sets=3)


# Print lineups
print_lineups_namesonly(lineups)
print_lineups(lineups)
'''

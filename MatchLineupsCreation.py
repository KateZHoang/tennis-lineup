import random
import GetPlayerList
from itertools import combinations

# Generate pairs. Pair each female with a male, and pair up the rest
def pair_up(short_list, long_list):
    pairs = []
    pairs += [(short_list[i], long_list[i]) for i in range(0, len(short_list), 2)]
        
    remaining = long_list[len(short_list):]
    pairs += [(long_list[i], long_list[i+1]) for i in range(0, len(remaining), 2)]

    # Ensure teams have close USTA levels by pairing highest level pairs against each other
    pairs.sort(key=lambda pair: pair[0].level + pair[1].level, reverse=True)

    return pairs

# Create a function to generate pairs with varied partners and balanced matchups
def generate_lineups(players, sets=3):
    # Split players by gender
    males = [p for p in players if p.gender == 'Male']
    females = [p for p in players if p.gender == 'Female']

    # Track previous pairings and matchups to avoid repeats
    previous_pairings = set()
    previous_matchups = set()

    # Ensure each player has a new partner in each set and balanced match levels
    lineups = []
    for s in range(sets):
        lineup_set = []

        # Decide on the short and the long list
        short = min(males, females, key=len)
        long = max(males, females, key=len)

        # Shuffle players to vary pairings each matchup
        random.shuffle(short)
        random.shuffle(long)

        # Pair up the players
        pairs = pair_up(short, long)
        
        matches = []

        for i in range(0, len(pairs), 2):
            team1, team2 = pairs[i], pairs[i + 1]

            # Check if this pairing or matchup has already occurred
            while (
                tuple(sorted([team1[0], team1[1]])) in previous_pairings 
                or tuple(sorted([team2[0], team2[1]])) in previous_pairings 
                or (tuple(sorted([team1, team2]))) in previous_matchups
            ):
                
                # If repeat, reshuffle players and create new pairings
                random.shuffle(short)
                random.shuffle(long)

                # Recreate the pairs
                pairs = pair_up(short, long)
                team1, team2 = pairs[i], pairs[i + 1]
            
            # Add valid pairings and matchups to track
            previous_pairings.add(tuple(sorted([team1[0], team1[1]])))
            previous_pairings.add(tuple(sorted([team2[0], team2[1]])))
            previous_matchups.add(tuple(sorted([team1, team2])))

            matches.append((team1, team2))

        # Add matches to the set
        lineup_set.append(matches)
        lineups.append(lineup_set)
    
    return lineups

# Print the generated lineup sets (with names, gender, and level)
# def print_lineups(lineups):
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

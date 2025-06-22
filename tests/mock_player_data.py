from GetPlayerList import Player

# Create a set of mock player data to test against test scripts
def mock_valid_players():
    return [
        Player("Alice", "Female", "3.0"),
        Player("Betty", "Female", "3.5"),
        Player("Cathy", "Female", "3.5"),
        Player("Dan", "Male", "3.0"),
        Player("Ethan", "Male", "3.5"),
        Player("Frank", "Male", "4.0"),
        Player("Grace", "Female", "3.0"),
        Player("Henry", "Male", "3.0"),
    ]

def mock_missing_gender():
    return [
        Player("Alice", "Female", "3.0"),
        Player("Ethan", "", "3.0"),  # Missing gender
        Player("Frank", "Male", "3.5"),
        Player("Grace", "Female", "3.0"),
    ]

def mock_invalid_level():
    return [
        Player("Alice", "Female", ""),     # Empty level
        Player("Betty", "Female", "N/A"),  # Non-numeric
        Player("Dan", "Male", "3.0"),
        Player("Ethan", "Male", "3.5"),
    ]

def mock_duplicate_names():
    return [
        Player("Alice", "Female", "3.0"),
        Player("Alice", "Female", "3.5"),  # Duplicate
        Player("Dan", "Male", "3.0"),
        Player("Ethan", "Male", "3.5"),
    ]

def get_mock_players(scenario):
    scenarios = {
        "valid": mock_valid_players,
        "missing_gender": mock_missing_gender,
        "invalid_level": mock_invalid_level,
        "duplicate_names": mock_duplicate_names,
    }
    if scenario not in scenarios:
        raise ValueError(f"Unknown mock scenario: {scenario}")
    return scenarios[scenario]()

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from get_player_list import get_players
from authenticate_google import authenticate_google
from mock_player_data import get_mock_players

@pytest.fixture
def scenario(request):
    return request.config.getoption("--mock-scenario")

# Test 1: Ensure the number of generated players in the lineup is a multiple of 4.
def test_player_number_is_accurate(player_data):
    assert len(player_data) % 4 == 0

# Test 2: Ensure each player has a "gender"
def test_players_have_gender(player_data, scenario):
    if scenario == "missing_gender":
        pytest.xfail("Expected failure for missing gender case")

    for player in player_data:
        assert hasattr(player, 'gender'), f"Missing gender attribute on {player}"
        assert player.gender is not None and player.gender != '', f"Empty gender for player: {player.name}"
        assert player.gender in ['Female', 'Male','female', 'male'], f"Invalid gender value for player {player.name}: {player.gender}"

# Test 3: Every player has a non-empty 'level'
def test_players_have_level(player_data, scenario):
    if scenario == "invalid_level":
        pytest.xfail("Expected failure for invalid_level case")

    for player in player_data:
        assert hasattr(player, 'level'), f"Missing level attribute on {player}"
        assert player.level is not None and player.level != '', f"Empty level for player: {player.name}"
        try:
            float(player.level)
        except ValueError:
            assert False, f"Non-numeric level value for player: {player.name} ({player.level})"

# Test 4: Ensure every player's name is unique
def test_players_not_duplicate(player_data, scenario):
    if scenario == "duplicate_names":
        pytest.xfail("Expected failure for duplicate names case")

    seen = set()
    for player in player_data:
        assert player.name not in seen, f"Duplicate name: {player.name}"
        seen.add(player.name)
    
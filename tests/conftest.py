import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from mock_player_data import get_mock_players
from get_player_list import get_players
from authenticate_google import authenticate_google

def pytest_addoption(parser):
    parser.addoption("--data-source", action="store", default="mock", help="mock or real")
    parser.addoption("--mock-scenario", action="store", default="valid", help="choose mock scenario")

# Scenarios known to be invalid
xfail_cases = {"missing_gender", "invalid_level", "duplicate_names"}

@pytest.fixture
def player_data(request):
    source = request.config.getoption("--data-source")
    scenario = request.config.getoption("--mock-scenario")

    if source == "real":
        creds, client = authenticate_google()
        sheet = client.open_by_key("1pG6MNE5WRD9IikzX66HsNfme1DRZsMDVY0FUPnSnFtY").worksheet("Player_Info")
        return get_players(sheet)
    else:
#        if scenario in xfail_cases:
#            pytest.xfail(f"Expected failure for mock case: {scenario}")  
        return get_mock_players(scenario)

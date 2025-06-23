import os
import pytest
import gspread
from authenticate_google import authenticate_google
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

def test_authenticate_google_success():

    load_dotenv()  # Load environment variables from .env file

    # Ensure the env var is set before testing
    assert "SERVICE_ACCOUNT_KEY" in os.environ, "Missing SERVICE_ACCOUNT_KEY in environment variables"
    
    creds, client = authenticate_google()
    
    # Check credentials type
    assert creds is not None
    assert client is not None
    assert isinstance(client, gspread.client.Client)
    
    # Try accessing the google sheet
    test_sheet_key = "1RLVxG0qlzww2K9d_s1ZK1MZ2I8uTu9Rrt59EAcCTqYM"
    try:
        sheet = client.open_by_key(test_sheet_key)
        worksheet = sheet.get_worksheet(0)
        assert worksheet is not None
    except Exception as e:
        pytest.fail(f"Failed to open or access test sheet: {e}")

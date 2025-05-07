import os
import json
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

def authenticate_google():
    load_dotenv()  # Load environment variables from .env file

    # Load service account key from environment variable
    secret_key = os.getenv("SERVICE_ACCOUNT_KEY")

    if not secret_key:
        raise ValueError("SERVICE_ACCOUNT_KEY environment variable is not set.")

    # Parse the JSON string
    parsed_json = json.loads(secret_key)

    # Authenticate with Google API using the JSON secret
    scope = ["https://spreadsheets.google.com/feeds", 
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file", 
            "https://www.googleapis.com/auth/drive"
    ]

    creds = Credentials.from_service_account_info(parsed_json, scopes=scope)
    client = gspread.authorize(creds)

    # return the creds and client to be used if needed
    return creds, client
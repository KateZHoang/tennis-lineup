# 🎾 Tennis Lineup Automation

This project automates weekly tennis practice lineups for mix doubles practices. It replaces manual coordination with Python scripts that verify player data, generate balanced matchups, and push the final lineup directly to a Google Sheet.

## 🚀 Features

- **Lineup Generator**: Creates fair and randomized doubles matches.
- **Player Validation**: Ensures players are grouped in multiples of four.
- **Google Sheets Integration**: Automatically updates lineups to a designated sheet.
- **Test Coverage**: Includes unit tests using `pytest` and mock data to validate logic and Google API connectivity.

## 🧪 Tech Stack

- **Python 3.12**
- `pytest` – for backend logic tests  
- `gspread` – for Google Sheets interaction  
- `dotenv` – for handling environment variables  
- Google Service Account – for API authentication

## 🧩 Scripts Overview

- `get_player_list.py`: Loads and validates players.
- `match_lineup_creation.py`: Creates the match lineup.
- `update_google_sheet.py`: Pushes lineup to a Google Sheet.
- `authenticate_google.py`: Handles Google API auth.
- `tests/`: Contains mock data and unit tests for all components.

## 🛠 Setup

1. Set up a Google Service Account and store its credentials as an environment variable `SERVICE_ACCOUNT_KEY`.
2. Install dependencies:  
   ```bash
   pip install -r requirements.txt

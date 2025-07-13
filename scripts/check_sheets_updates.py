#!/usr/bin/env python3
"""
Google Sheets Update Monitor for Public Sheets

This script checks for updates in a publicly shared Google Sheet and creates GitHub issues
when new records are detected. Uses CSV export instead of Google Sheets API.
"""

import os
import json
import hashlib
import requests
import pandas as pd
from datetime import datetime
from io import StringIO

def get_sheet_data(spreadsheet_id, sheet_name):
    """Fetch data from publicly shared Google Sheet via CSV export."""
    try:
        # Google Sheets CSV export URL format
        csv_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        
        print(f"Fetching data from: {csv_url}")
        response = requests.get(csv_url, timeout=30)
        response.raise_for_status()
        
        # Parse CSV data
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data)
        
        # Convert DataFrame to list of lists for consistency
        data = [df.columns.tolist()] + df.values.tolist()
        
        print(f"Successfully fetched {len(data)} rows from sheet")
        return data
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching sheet data: {e}")
        return []
    except Exception as e:
        print(f"Error parsing CSV data: {e}")
        return []

def calculate_data_hash(data):
    """Calculate hash of sheet data to detect changes."""
    data_str = json.dumps(data, sort_keys=True)
    return hashlib.md5(data_str.encode()).hexdigest()

def load_previous_state():
    """Load previous state from file."""
    state_file = 'sheets_state.json'
    if os.path.exists(state_file):
        try:
            with open(state_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading state file: {e}")
    return {'last_hash': None, 'last_check': None}

def save_state(data_hash):
    """Save current state to file."""
    state_file = 'sheets_state.json'
    state = {
        'last_hash': data_hash,
        'last_check': datetime.now().isoformat()
    }
    try:
        with open(state_file, 'w') as f:
            json.dump(state, f)
    except Exception as e:
        print(f"Error saving state file: {e}")

def count_new_records(old_data, new_data):
    """Count new records by comparing data."""
    if not old_data:
        return len(new_data) if new_data else 0
    
    # Simple comparison - count rows that weren't in the old data
    old_rows = set(tuple(row) for row in old_data if row)
    new_rows = set(tuple(row) for row in new_data if row)
    
    return len(new_rows - old_rows)

def main():
    """Main function to check for sheet updates."""
    # Get environment variables
    spreadsheet_id = os.environ.get('GOOGLE_SHEETS_ID')
    sheet_name = os.environ.get('SHEET_NAME', 'Sheet1')
    
    if not spreadsheet_id:
        print("Error: GOOGLE_SHEETS_ID environment variable not set")
        exit(1)
    
    # Get current sheet data
    current_data = get_sheet_data(spreadsheet_id, sheet_name)
    if not current_data:
        print("No data found in sheet")
        exit(0)
    
    # Calculate current data hash
    current_hash = calculate_data_hash(current_data)
    
    # Load previous state
    previous_state = load_previous_state()
    
    # Check for updates
    has_updates = False
    new_records_count = 0
    
    if previous_state['last_hash'] != current_hash:
        has_updates = True
        print(f"Changes detected in Google Sheet!")
        print(f"Previous hash: {previous_state['last_hash']}")
        print(f"Current hash: {current_hash}")
        
        # Calculate new records count
        if previous_state['last_hash']:
            new_records_count = len(current_data) - 1  # Subtract header row
        else:
            new_records_count = len(current_data) - 1  # First run, count all data rows
    
    # Save current state
    save_state(current_hash)
    
    # Set output for GitHub Actions using environment files
    github_output = os.environ.get('GITHUB_OUTPUT')
    if github_output:
        with open(github_output, 'a') as f:
            if has_updates:
                f.write(f"has_updates=true\n")
                f.write(f"new_records_count={new_records_count}\n")
                f.write(f"last_check={datetime.now().isoformat()}\n")
            else:
                f.write(f"has_updates=false\n")
    
    # Also print for backward compatibility
    if has_updates:
        print(f"has_updates=true")
        print(f"new_records_count={new_records_count}")
        print(f"last_check={datetime.now().isoformat()}")
    else:
        print(f"has_updates=false")
        print("No updates detected")
    
    print(f"Sheet: {sheet_name}")
    print(f"Total rows: {len(current_data)}")
    print(f"Last check: {datetime.now().isoformat()}")

if __name__ == "__main__":
    main() 

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
        return data, df
        
    except requests.exceptions.RequestException as e:
        print(f"Error fetching sheet data: {e}")
        return [], None
    except Exception as e:
        print(f"Error parsing CSV data: {e}")
        return [], None

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
    return {'last_hash': None, 'last_check': None, 'last_row_count': 0}

def save_state(data_hash, row_count):
    """Save current state to file."""
    state_file = 'sheets_state.json'
    state = {
        'last_hash': data_hash,
        'last_check': datetime.now().isoformat(),
        'last_row_count': row_count
    }
    try:
        with open(state_file, 'w') as f:
            json.dump(state, f)
    except Exception as e:
        print(f"Error saving state file: {e}")

def get_latest_instance_id(df, previous_row_count):
    """Get the instanceID from the latest added row."""
    if df is None or df.empty:
        return None
    
    # Check if instanceID column exists
    if 'instanceID' not in df.columns:
        print("Warning: 'instanceID' column not found in sheet")
        return None
    
    # Get the latest row (assuming new rows are added at the bottom)
    current_row_count = len(df)
    
    if current_row_count > previous_row_count:
        # Get the latest row
        latest_row = df.iloc[-1]
        instance_id = latest_row['instanceID']
        print(f"Latest instanceID: {instance_id}")
        return str(instance_id)
    
    return None

def main():
    """Main function to check for sheet updates."""
    # Get environment variables
    spreadsheet_id = os.environ.get('GOOGLE_SHEETS_ID')
    sheet_name = os.environ.get('SHEET_NAME', 'Sheet1')
    
    if not spreadsheet_id:
        print("Error: GOOGLE_SHEETS_ID environment variable not set")
        exit(1)
    
    # Get current sheet data
    current_data, df = get_sheet_data(spreadsheet_id, sheet_name)
    if not current_data:
        print("No data found in sheet")
        exit(0)
    
    # Calculate current data hash
    current_hash = calculate_data_hash(current_data)
    current_row_count = len(current_data) - 1  # Subtract header row
    
    # Load previous state
    previous_state = load_previous_state()
    previous_row_count = previous_state.get('last_row_count', 0)
    
    # Check for updates
    has_updates = False
    new_records_count = 0
    latest_instance_id = None
    
    if previous_state['last_hash'] != current_hash:
        has_updates = True
        print(f"Changes detected in Google Sheet!")
        print(f"Previous hash: {previous_state['last_hash']}")
        print(f"Current hash: {current_hash}")
        print(f"Previous row count: {previous_row_count}")
        print(f"Current row count: {current_row_count}")
        
        # Calculate new records count
        if previous_state['last_hash']:
            new_records_count = current_row_count - previous_row_count
        else:
            new_records_count = current_row_count  # First run, count all data rows
        
        # Get the latest instanceID
        latest_instance_id = get_latest_instance_id(df, previous_row_count)
    
    # Save current state
    save_state(current_hash, current_row_count)
    
    # Set output for GitHub Actions using environment files
    github_output = os.environ.get('GITHUB_OUTPUT')
    if github_output:
        with open(github_output, 'a') as f:
            if has_updates:
                f.write(f"has_updates=true\n")
                f.write(f"new_records_count={new_records_count}\n")
                f.write(f"last_check={datetime.now().isoformat()}\n")
                if latest_instance_id:
                    f.write(f"latest_instance_id={latest_instance_id}\n")
            else:
                f.write(f"has_updates=false\n")
    
    # Also print for backward compatibility
    if has_updates:
        print(f"has_updates=true")
        print(f"new_records_count={new_records_count}")
        print(f"last_check={datetime.now().isoformat()}")
        if latest_instance_id:
            print(f"latest_instance_id={latest_instance_id}")
    else:
        print(f"has_updates=false")
        print("No updates detected")
    
    print(f"Sheet: {sheet_name}")
    print(f"Total rows: {len(current_data)}")
    print(f"Last check: {datetime.now().isoformat()}")

if __name__ == "__main__":
    main() 

#!/usr/bin/env python3
"""
Test Google Sheets Connection for Public Sheets

This script tests the connection to a publicly shared Google Sheet
and verifies that the sheet is accessible.
"""

import os
import requests
import pandas as pd
from io import StringIO

def test_connection():
    """Test the Google Sheets connection."""
    print("🔍 Testing Google Sheets Connection...")
    
    # Check environment variables
    spreadsheet_id = os.environ.get('GOOGLE_SHEETS_ID')
    sheet_name = os.environ.get('SHEET_NAME', 'Sheet1')
    
    if not spreadsheet_id:
        print("❌ Error: GOOGLE_SHEETS_ID environment variable not set")
        return False
    
    try:
        # Test sheet access
        print(f"📊 Testing access to sheet: {sheet_name}")
        csv_url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
        
        print(f"📡 Fetching data from: {csv_url}")
        response = requests.get(csv_url, timeout=30)
        response.raise_for_status()
        
        # Parse CSV data
        csv_data = StringIO(response.text)
        df = pd.read_csv(csv_data)
        
        print(f"✅ Successfully accessed sheet!")
        print(f"📈 Found {len(df)} rows of data")
        print(f"📋 Found {len(df.columns)} columns")
        
        if not df.empty:
            print("📋 Sample data (first row):")
            print(f"   {df.iloc[0].tolist()}")
            
            print("📋 Column names:")
            for i, col in enumerate(df.columns):
                print(f"   {i+1}. {col}")
        
        return True
        
    except requests.exceptions.HTTPError as error:
        print(f"❌ HTTP Error: {error}")
        if error.response.status_code == 403:
            print("💡 This might be a permissions issue. Make sure:")
            print("   1. The Google Sheet is shared publicly (Anyone with the link can view)")
            print("   2. The sheet is not restricted to specific users")
        elif error.response.status_code == 404:
            print("💡 Sheet not found. Check:")
            print("   1. The GOOGLE_SHEETS_ID is correct")
            print("   2. The SHEET_NAME is correct")
            print("   3. The sheet exists and is accessible")
        return False
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Request Error: {e}")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main function."""
    print("🚀 Google Sheets Connection Test (Public Sheets)")
    print("=" * 50)
    
    success = test_connection()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! Your setup is ready.")
        print("💡 You can now run the main monitoring script.")
    else:
        print("❌ Tests failed. Please check the setup instructions.")
        print("📖 Refer to the README.md for troubleshooting steps.")

if __name__ == "__main__":
    main() 
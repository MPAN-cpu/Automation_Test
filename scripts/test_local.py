#!/usr/bin/env python3
"""
Local Testing Script for Google Sheets Integration

This script can be run locally to test the Google Sheets integration
before setting up the GitHub Actions workflow.
"""

import os
import sys
from pathlib import Path

# Add the parent directory to the path so we can import our modules
sys.path.append(str(Path(__file__).parent.parent))

def load_env_file():
    """Load environment variables from .env file if it exists."""
    env_file = Path(__file__).parent.parent / '.env'
    if env_file.exists():
        print("📁 Loading environment variables from .env file...")
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value
        print("✅ Environment variables loaded")
    else:
        print("⚠️  No .env file found. Make sure environment variables are set manually.")

def main():
    """Main function for local testing."""
    print("🧪 Local Testing for Google Sheets Integration")
    print("=" * 50)
    
    # Load environment variables
    load_env_file()
    
    # Import and run the test connection script
    try:
        from test_connection import test_connection
        
        success = test_connection()
        
        if success:
            print("\n🎉 Local test successful!")
            print("💡 Your setup is ready for GitHub Actions.")
        else:
            print("\n❌ Local test failed.")
            print("🔧 Please fix the issues before setting up GitHub Actions.")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure you have installed the required dependencies:")
        print("   pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main() 
#!/usr/bin/env python3
"""
Setup script for Google Sheets GitHub Actions Monitor

This script helps set up the project for local testing and development.
"""

import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"   Error: {e.stderr}")
        return False

def main():
    """Main setup function."""
    print("🚀 Setting up Google Sheets GitHub Actions Monitor")
    print("=" * 50)
    
    # Check if Python is available
    if not run_command("python --version", "Checking Python installation"):
        print("❌ Python is not available. Please install Python 3.8+ and try again.")
        return False
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        print("❌ Failed to install dependencies. Please check your pip installation.")
        return False
    
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if not env_file.exists() and env_example.exists():
        print("📝 Creating .env file from template...")
        try:
            with open(env_example, 'r') as src, open(env_file, 'w') as dst:
                dst.write(src.read())
            print("✅ .env file created. Please edit it with your configuration.")
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
    
    # Make scripts executable
    scripts_dir = Path("scripts")
    if scripts_dir.exists():
        for script in scripts_dir.glob("*.py"):
            try:
                script.chmod(0o755)
                print(f"✅ Made {script} executable")
            except Exception as e:
                print(f"⚠️  Could not make {script} executable: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("1. Edit the .env file with your Google Sheets configuration")
    print("2. Run: python scripts/test_local.py")
    print("3. Set up GitHub repository secrets")
    print("4. Push to GitHub to enable the workflow")
    print("\n📖 For detailed instructions, see README.md")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
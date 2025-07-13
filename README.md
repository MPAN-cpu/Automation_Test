# Google Sheets GitHub Actions Monitor (Public Sheets)

This repository contains a GitHub Actions workflow that monitors publicly shared Google Sheets for updates and automatically creates GitHub issues when new records are detected.

## Features

- 🔄 **Scheduled Monitoring**: Checks Google Sheets every 5 minutes
- 📊 **Change Detection**: Uses hash-based comparison to detect updates
- 🎫 **Automatic Issue Creation**: Creates GitHub issues when updates are detected
- 🔧 **Manual Triggering**: Can be triggered manually via GitHub Actions
- 📝 **State Tracking**: Maintains state between runs to avoid duplicate issues
- 🌐 **Public Sheet Support**: Works with publicly shared Google Sheets (no authentication required)

## Setup Instructions

### 1. Google Sheet Setup

#### Step 1: Make Your Sheet Public
1. Open your Google Sheet
2. Click "Share" in the top right
3. Click "Change to anyone with the link"
4. Set permissions to "Viewer"
5. Click "Done"

#### Step 2: Get Sheet Information
1. Copy the Sheet ID from the URL:
   - URL format: `https://docs.google.com/spreadsheets/d/YOUR_SHEET_ID/edit`
   - Copy the long string between `/d/` and `/edit`
2. Note the sheet tab name (default is "Sheet1")

### 2. GitHub Repository Setup

#### Step 1: Add Repository Secrets
Go to your GitHub repository > Settings > Secrets and variables > Actions, and add the following secrets:

- `GOOGLE_SHEETS_ID`: Your Google Sheet ID (from the URL)
- `SHEET_NAME`: The name of the sheet tab to monitor (default: "Sheet1")

#### Step 2: Configure Workflow (Optional)
You can customize the workflow by editing `.github/workflows/google-sheets-monitor.yml`:

- **Schedule**: Change the cron expression to adjust frequency
- **Issue Labels**: Add or modify labels in the workflow

### 3. Testing the Setup

1. **Manual Trigger**: Go to Actions tab and manually trigger the workflow
2. **Add Test Data**: Add a new row to your Google Sheet
3. **Check Results**: The workflow should create a GitHub issue within 5 minutes

## File Structure

```
├── .github/
│   └── workflows/
│       └── google-sheets-monitor.yml    # GitHub Actions workflow
├── scripts/
│   ├── check_sheets_updates.py          # Python script for monitoring
│   ├── test_connection.py               # Connection test script
│   └── test_local.py                    # Local testing script
├── requirements.txt                     # Python dependencies
├── env.example                          # Environment template
├── setup.py                             # Setup script
└── README.md                            # This file
```

## How It Works

1. **Scheduled Execution**: The workflow runs every 5 minutes via cron
2. **Data Fetching**: Uses Google Sheets CSV export to fetch current data
3. **Change Detection**: Compares current data hash with previous state
4. **Issue Creation**: Creates GitHub issues when changes are detected
5. **State Management**: Saves current state to avoid duplicate issues

## Customization Options

### Change Monitoring Frequency
Edit the cron expression in `.github/workflows/google-sheets-monitor.yml`:
```yaml
schedule:
  - cron: '*/5 * * * *'  # Every 5 minutes
  # Other options:
  # '0 */6 * * *'        # Every 6 hours
  # '0 9 * * *'          # Daily at 9 AM
```

### Custom Issue Content
Modify the issue creation step in the workflow to include custom content, links, or formatting.

## Local Testing

### Quick Setup
```bash
python setup.py                    # Install dependencies
python scripts/test_local.py       # Test the connection
```

### Manual Testing
1. Copy `env.example` to `.env`
2. Edit `.env` with your sheet details:
   ```bash
   GOOGLE_SHEETS_ID=your_actual_sheet_id_here
   SHEET_NAME=YourSheetTabName
   ```
3. Run the test script

## Troubleshooting

### Common Issues

1. **403 Forbidden Error**: Make sure your Google Sheet is shared publicly
2. **404 Not Found**: Verify the Sheet ID and Sheet Name are correct
3. **No Data Found**: Check if the sheet has data and the tab name is correct
4. **CSV Parsing Error**: Ensure your sheet has proper column headers

### Debug Steps

1. Check the Actions tab for workflow logs
2. Verify all secrets are set correctly
3. Test the sheet access manually by visiting the CSV export URL
4. Ensure the sheet is publicly accessible

## Security Considerations

- Only works with publicly shared Google Sheets
- No authentication required (simpler setup)
- Consider the privacy implications of making your sheet public
- The sheet data is only read, never modified

## Advantages of Public Sheet Approach

- ✅ **No Google Cloud setup required**
- ✅ **No service account management**
- ✅ **No API quotas or limits**
- ✅ **Simpler configuration**
- ✅ **Faster execution**

## Limitations

- ❌ **Sheet must be publicly accessible**
- ❌ **No access to private sheets**
- ❌ **Limited to CSV export format**

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the [MIT License](LICENSE). 

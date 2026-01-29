# Stock Performance Tracker

Ahoy, matey! This be a Python program to track and analyze stock performance.

## Features

- Input any stock ticker symbol
- Fetch current stock price and historical data
- Analyze performance using multiple indicators:
  - 50-day and 200-day moving averages
  - Weekly, monthly, and yearly price trends
  - 52-week high/low positioning
- Clear verdict: "DOING GOOD", "DOING BAD", or "MIXED"
- Proper error handling for invalid tickers and API failures

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python stock_tracker.py
```

Then enter a stock ticker symbol when prompted (e.g., AAPL, GOOGL, MSFT).

## How It Works

The tracker analyzes stocks based on:
1. **Moving Averages**: Compares current price to 50-day and 200-day averages
2. **Price Trends**: Calculates weekly, monthly, and yearly percentage changes
3. **52-Week Range**: Determines where the price sits in its yearly range

A stock is considered "DOING GOOD" when more positive signals outweigh negative ones, and "DOING BAD" when the reverse is true.

## Example Output

```
============================================================
  STOCK PERFORMANCE REPORT FOR: AAPL
============================================================

  Current Price: $175.50
------------------------------------------------------------

  PRICE AVERAGES:
    50-Day Average:  $172.30
    200-Day Average: $168.45
    Overall Average: $165.20

  52-WEEK RANGE:
    High: $199.62
    Low:  $143.90

  PERFORMANCE TRENDS:
    Weekly Change:  +2.35%
    Monthly Change: +5.12%
    Yearly Change:  +15.67%

------------------------------------------------------------

  OVERALL VERDICT: *** DOING GOOD ***

  ANALYSIS:
    1. Price be above the 50-day average (bullish signal)
    2. Price be above the 200-day average (long-term bullish)
    3. Weekly trend be positive (+2.35%)
    4. Monthly trend be positive (+5.12%)
    5. Yearly performance be positive (+15.67%)

============================================================
  Data based on 252 trading days
============================================================
```

---

## Test Script: list_tmp_dirs.sh

This repository also includes a test script (`list_tmp_dirs.sh`) that lists all directories in `/tmp/` and displays the number of files present in each directory.

### Test Script Features

- Lists all directories in `/tmp/` (excluding `/tmp/` itself)
- Counts files in each directory (non-recursive)
- Displays results in a formatted table
- Handles edge cases (empty `/tmp/`, missing `/tmp/`)
- Executable shell script with proper error handling

### Running the Test Script

```bash
chmod +x list_tmp_dirs.sh
./list_tmp_dirs.sh
```

### Test Script Verification Results

The test script was executed and verified in a sandbox environment with the following results:

**Test Scenario 1: Empty /tmp/ directory**
```
==========================================
  Listing directories in /tmp/
==========================================

No directories found in /tmp/
```
- **Result**: ✅ PASSED - Script handles empty directories gracefully

**Test Scenario 2: /tmp/ with multiple directories containing files**
```
==========================================
  Listing directories in /tmp/
==========================================

Directory Name                          | Files Present
------------------------------------------+--------------
test_dir3                                | 0
test_dir1                                | 2
test_dir2                                | 3
------------------------------------------+--------------

Total directories found: 3
==========================================
```
- **Result**: ✅ PASSED - Script correctly lists directories and counts files

### Issues Found and Fixes Applied

**No issues were found during sandbox verification.** The test script executed successfully without any errors or modifications needed. The script properly:

1. Checks for `/tmp/` directory existence
2. Uses `find` command with appropriate depth limits
3. Counts only files (not subdirectories) in each directory
4. Formats output in a readable table format
5. Handles empty directory scenarios gracefully

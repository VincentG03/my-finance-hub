# Modular Design Documentation

## Overview
The Finance Hub application is designed to be **fully modular** and can handle multiple Excel files using the same template structure but with different data (different people, varying numbers of assets/liabilities/jobs, different names for items).

## Quick Start: Switching Between Files

### Step 1: Change the Excel File
Open `dash_app.py` and modify line 9:

```python
EXCEL_FILE = 'data/your_file_name.xlsx'  # Change this to your file
```

For example:
```python
EXCEL_FILE = 'data/john_financial_data.xlsx'
```

That's it! The entire dashboard will now load data from the new file.

## Modular Features

### 1. Dynamic Section Detection
The code **automatically finds** the "Assets" and "Liabilities" sections in your Excel file:
- **No hardcoded row numbers** for section headers
- Searches the first column for cells containing "Assets" and "Liabilities"
- Works regardless of where these sections appear in the sheet

**Code Location**: `data_loader.py` → `_find_section_headers()` method

### 2. Variable Number of Liabilities
- **No hardcoded limit** on the number of liability items
- The code reads all rows between "Liabilities" header and "Assets" header
- Each liability (HELP, Car Loan, etc.) is dynamically parsed
- Constraint: Assets header is typically on row 16, so liabilities naturally end at row 15

**Code Location**: `data_loader.py` → `_parse_section()` method

### 3. Variable Number of Assets
- **No hardcoded limit** on the number of asset items  
- The code reads all rows from "Assets" header until the end of data
- Each asset type (Cash, Super, Shares, etc.) is dynamically detected
- Automatically skips empty rows

**Code Location**: `data_loader.py` → `_parse_section()` method

### 4. Variable Asset/Liability Names
- **No hardcoded names** for specific assets or liabilities
- The first column value becomes the "Type" name
- Example transformations applied for cleaner display:
  - "Cash - Commbank & ING" → "Cash"
  - "Super - Aussuper" → "Super"

**Code Location**: `data_loader.py` → `load_assets_liabilities()` method (line 95-97)

### 5. Smart Date Detection ("Cash Stop" Logic)
- **Automatically determines** how many date columns contain valid data
- Uses the Cash row to detect where valid data ends
- Stops reading at the first blank cell in the Cash row
- Handles varying numbers of date columns per person

**Code Location**: `data_loader.py` → `_count_valid_dates()` method

### 6. Variable Number of Jobs
- **No hardcoded assumptions** about employment history
- Reads entire Employment sheet dynamically
- Handles any number of job entries
- Automatically calculates duration for each job

**Code Location**: `data_loader.py` → `load_employment()` method

### 7. Variable Number of Investments
- **No hardcoded assumptions** about investment transactions
- Reads entire Investments sheet dynamically
- Handles any number of trades/symbols

**Code Location**: `data_loader.py` → `load_investments()` method

## Template Requirements

Your Excel file must follow this template structure:

### Info Sheet
```
Full Name    | [Name]
DOB          | [Date]
Currency     | [Currency Code]
```

### Assets & Liabilities Sheet
```
[Row 0]       | Date1 | Date2 | Date3 | ...
Liabilities   |       |       |       |
[Liability 1] | val   | val   | val   | ...
[Liability 2] | val   | val   | val   | ...
...           | ...   | ...   | ...   |
Assets        |       |       |       |     <- Typically Row 16
[Asset 1]     | val   | val   | val   | ... <- Cash row used for date detection
[Asset 2]     | val   | val   | val   | ...
...           | ...   | ...   | ...   |
```

**Key Points**:
- Row 0: Contains dates (starting column 1)
- First column: Contains section headers and item names
- "Cash" row is critical - must exist to determine valid date range
- "Assets" header typically on row 16 (but dynamically detected)
- "Liabilities" section ends where "Assets" begins

### Employment Sheet
```
[Any columns you want - common ones:]
Date Started | Date Ended | Company | Role | Salary | ...
```

### Investments - Cost Basis Sheet
```
[Any columns - common ones:]
Trade Date | Symbol | Side | Units | Avg. Price | Value | Fees | ...
```

## Example: Adding a New Person's File

1. **Create Excel file**: `data/sarah_financial_data.xlsx`
   - Use the same template structure
   - Sarah can have:
     - Different number of liabilities (3 instead of 5)
     - Different number of assets (7 instead of 4)
     - Different asset names ("HISA - Westpac" instead of "Cash - Commbank")
     - Different number of jobs (2 instead of 4)

2. **Update dash_app.py**:
   ```python
   EXCEL_FILE = 'data/sarah_financial_data.xlsx'
   ```

3. **Run the app** - Everything works automatically!

## Testing Modularity

To verify the code handles your new file:

1. Check the terminal for any errors when loading
2. Verify all sections appear in the dashboard:
   - User name displays correctly
   - Net worth chart shows all dates
   - Assets pie chart shows all asset types
   - Liabilities section shows all liability items
   - Employment history shows all jobs

## Common Issues & Solutions

### Issue: "Could not find 'Cash' row"
**Solution**: Ensure you have an asset item that starts with "Cash" (e.g., "Cash", "Cash - Bank Name")

### Issue: "Could not find 'Assets' or 'Liabilities' section headers"
**Solution**: Ensure row headers in column 0 contain exactly "Assets" and "Liabilities" (case-insensitive)

### Issue: Missing dates/columns
**Solution**: The Cash row determines valid dates. Ensure Cash row has values in all date columns you want to include.

### Issue: Zero values showing up
**Solution**: The code filters out zero values automatically. If you see zeros, check the data parsing logic.

## Architecture Summary

```
dash_app.py
├── EXCEL_FILE (configuration variable - change this!)
├── data_loader = load_data(EXCEL_FILE)
└── [All dashboard logic uses data_loader methods]

data_loader.py (FinanceDataLoader class)
├── __init__(excel_path) - Takes file path as parameter
├── Dynamic section detection (no hardcoded rows)
├── Dynamic item parsing (no hardcoded item names)
├── Dynamic date range detection (Cash stop logic)
└── Returns normalized DataFrames for any template-compliant file
```

## Conclusion

The entire system is **template-driven** and **fully modular**. Simply change the `EXCEL_FILE` variable at the top of `dash_app.py` to switch between different people's files, and the code will automatically adapt to:
- Different numbers of assets, liabilities, and jobs
- Different names for assets and liabilities  
- Different date ranges
- Different personal information

No code changes required beyond updating the `EXCEL_FILE` variable!

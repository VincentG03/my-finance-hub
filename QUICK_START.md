# Quick Reference: Switching Between Excel Files

## How to Change the Data Source

Open [dash_app.py](dash_app.py) and change **line 9**:

```python
EXCEL_FILE = 'data/your_filename.xlsx'
```

## Examples

### Using Vincent's data (default):
```python
EXCEL_FILE = 'data/vincent_financial_data.xlsx'
```

### Using a different person's data:
```python
EXCEL_FILE = 'data/john_financial_data.xlsx'
```

### Using the copy file:
```python
EXCEL_FILE = 'data/vincent_financial_data copy.xlsx'
```

## What the Code Handles Automatically

✅ Different numbers of liabilities (1 to 15+ items)  
✅ Different numbers of assets (any number)  
✅ Different asset/liability names  
✅ Different number of jobs in employment history  
✅ Different number of investment transactions  
✅ Different date ranges  
✅ Different personal info (name, DOB, currency)

## File Requirements

Your Excel file **must** have these sheets:
1. **Info** - Contains Full Name, DOB, Currency
2. **Assets & Liabilities** - Contains date-based financial data
3. **Employment** - Contains job history
4. **Investments - Cost Basis** - Contains investment transactions

See [MODULAR_DESIGN.md](MODULAR_DESIGN.md) for detailed template structure.

## Testing Your New File

1. Update `EXCEL_FILE` variable
2. Run: `python dash_app.py`
3. Open browser to the local URL
4. Verify all sections load correctly

## Troubleshooting

If you encounter errors, check:
- [ ] File path is correct (relative to project root)
- [ ] File has all required sheets
- [ ] "Assets" and "Liabilities" headers exist in column 0
- [ ] At least one asset starts with "Cash"
- [ ] Dates are in row 0 (starting column 1)

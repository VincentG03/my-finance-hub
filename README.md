# My Finance Hub

Personal finance dashboard built with Plotly Dash.

## Quick Start

### Installation

Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the App

Start the dashboard:
```bash
python dash_app.py
```

Then open your browser to: **http://localhost:8050**

### Stopping the App

Press `Ctrl+C` in the terminal where it's running.

Or kill the process:
```bash
pkill -f "python.*dash_app.py"
```

## Data File

The app loads an Excel workbook from the `user_data/` folder. By default the project is configured to load the test file `user_data/test_financial_data.xlsx`.

Required sheets (do NOT rename these):
- Assets & Liabilities
- Employment
- Investments - Cost Basis

Using your own Excel file (very simple):

1. Make a copy of the sample file and rename it. For example:

```bash
cp user_data/test_financial_data.xlsx user_data/my_financial_data.xlsx
```

2. Open the copy (`user_data/my_financial_data.xlsx`) and fill it with your personal data. IMPORTANT: do not rename the required sheets or change obvious title/header rows (for example the quarter dates row, or the sheet names `Assets & Liabilities`, `Employment`, and `Investments - Cost Basis`).

3. Point the app to your new file by editing one of these two lines in the code (pick one):

- Open `dash_app.py` and change the `EXCEL_FILE` value on line 9 to your filename, for example:

    ```python
    EXCEL_FILE = 'user_data/my_financial_data.xlsx'  # [dash_app.py](dash_app.py#L9)
    ```

That's it — save the file and restart the app.

Notes:
- The repository is configured to only commit the test file (`user_data/test_financial_data.xlsx`). Other Excel files in `user_data/` are ignored by `.gitignore` so you can keep your personal files private.
- If you are unsure, prefer duplicating and renaming the test file rather than editing the test file directly.

Installation and run (quick):

```bash
pip install -r requirements.txt
python dash_app.py
```

Then open your browser to: **http://localhost:8050**

Important: for projects pushed to GitHub only the test file should be committed. The repository's `.gitignore` is configured to ignore other Excel files in `user_data/` while allowing `user_data/test_financial_data.xlsx`.

## Project Structure

```
my-finance-hub/
├── dash_app.py         # Main Dash application
├── data_loader.py      # Excel data parser
├── requirements.txt    # Python dependencies
├── data/               # Reference data (benchmarks, tax tables)
└── user_data/          # User financial data
    └── test_financial_data.xlsx  # The sample/test file you should copy or edit with your own data
```

## Requirements

- Python 3.8+
- See `requirements.txt` for package dependencies

---

*Personal project - functionality subject to change*

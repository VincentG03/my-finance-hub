# My Finance Hub

I built My Finance Hub to solve a problem I faced after tracking my finances manually in Excel for three years: spreadsheets are great for storage, but terrible for insight. I needed a robust, scalable platform that could evolve with my financial journey over the next decades.

This dashboard serves as my "one-stop shop" for financial health, turning static rows of data into interactive visualizations that track net worth, liabilities, income streams, and investment performance over time.

**Note:** The included demo data is dummy data for demonstration purposes. Replace it with your own financial data to get started.


<img width="1797" height="938" alt="image" src="https://github.com/user-attachments/assets/51b0af8b-4faf-4ce8-8f24-b7e06216b5a4" />


## What's Inside

**Assets & Liabilities**  
Track your complete financial picture across multiple accounts and asset classes. Visualize net worth trends over time, monitor debt paydown progress, and see your portfolio allocation at a glance.

**Investment Performance**  
Compare your portfolio returns against major market benchmarks (S&P 500, All Ords). Track cost basis, realized gains, and see how your investment strategy is performing in real-time.

**Income & Employment**  
Monitor income streams, tax obligations, and superannuation contributions. Forecast retirement savings and understand your take-home pay across different scenarios.

**Financial Calculators**  
A suite of predictive tools to model different financial scenarios, including a FIRE Calculator to plan your path to financial independence with detailed year-by-year projections showing both nominal and inflation-adjusted values.


## Demo

https://github.com/user-attachments/assets/372040cb-50fd-4a7a-abda-004eca7689c9



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

Using your own Excel file:

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

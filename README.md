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

The app reads from: `user_data/vincent_financial_data.xlsx`

Make sure this file exists with the required sheets:
- Assets & Liabilities
- Employment
- Investments - Cost Basis

## Project Structure

```
my-finance-hub/
├── dash_app.py         # Main Dash application
├── data_loader.py      # Excel data parser
├── requirements.txt    # Python dependencies
├── data/               # Reference data (benchmarks, tax tables)
└── user_data/          # User financial data
    └── vincent_financial_data.xlsx
```

## Requirements

- Python 3.8+
- See `requirements.txt` for package dependencies

---

*Personal project - functionality subject to change*

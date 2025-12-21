# My Finance Hub 💰

A premium personal finance dashboard built with Streamlit, designed for sophisticated financial tracking and analysis.

## Features

- **User Management**: Secure user selection with session persistence for Vincent, Amy, and Test users
- **Summary Overview**: Comprehensive financial snapshot with net worth tracking and asset allocation
- **Investment Tracker**: Monitor portfolio performance across multiple asset types with interactive charts
- **Mortgage Debt Tracker**: Track mortgage balance, payments, and interest over time
- **Assets & Liabilities**: Complete balance sheet view with detailed breakdowns
- **Salary Tracker**: Income analysis with tax breakdown and YTD summaries
- **Retirement Calculator**: Interactive retirement planning with goal-based projections

## Design Philosophy

### Visual Identity
- **Color Palette**: Black (#000000) and Light Blue (#4A9EFF) on pure white background
- **Typography**: Inter font family for a modern, professional look
- **Components**: Premium containers with subtle shadows and light grey borders (#E5E5E5)
- **Charts**: Interactive Plotly visualizations matching the color scheme

### User Experience
- Minimalist landing page with clean user selection
- Sidebar navigation for seamless page transitions
- Session state management to maintain user context
- Responsive layout optimized for desktop viewing

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone or navigate to the repository**
   ```bash
   cd my-finance-hub
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate  # On Windows
   ```

3. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Generate dummy data files**
   ```bash
   python setup_data.py
   ```
   
   This creates the following Excel files in the `data/` directory:
   - `Salary_Tracker.xlsx`
   - `Investment_Tracker.xlsx`
   - `Mortgage_Tracker.xlsx`
   - `Assets_Liabilities.xlsx`
   
   Each file contains three sheets (Vincent, Amy, Test) with 3 years of realistic financial data.

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Access the dashboard**
   - The app will automatically open in your default browser
   - If not, navigate to `http://localhost:8501`

## Project Structure

```
my-finance-hub/
├── app.py                      # Main Streamlit application
├── setup_data.py              # Data generation script
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── data/                      # Generated Excel files (created by setup_data.py)
    ├── Salary_Tracker.xlsx
    ├── Investment_Tracker.xlsx
    ├── Mortgage_Tracker.xlsx
    └── Assets_Liabilities.xlsx
```

## Usage Guide

### Landing Page
1. Select a user from the dropdown (Vincent, Amy, or Test)
2. Click "Continue to Dashboard" to proceed

### Dashboard Navigation
- Use the sidebar on the left to switch between different trackers
- Click "Change User" at the bottom of the sidebar to switch users

### Data Structure

Each Excel workbook contains three sheets (one per user) with the following columns:

**Salary_Tracker.xlsx**
- Date, Gross Income, Tax, Superannuation, Net Income, Bonus, Overtime

**Investment_Tracker.xlsx**
- Date, Asset Type, Value, Monthly Contribution, Growth Rate

**Mortgage_Tracker.xlsx**
- Date, Remaining Balance, Monthly Payment, Principal Payment, Interest Payment, Interest Rate

**Assets_Liabilities.xlsx**
- Date, Category, Type, Name, Value

### Customization

#### Adding Your Own Data
Replace the generated Excel files in the `data/` directory with your own data, ensuring:
- Sheet names match user names (Vincent, Amy, Test)
- Column names match the expected structure
- Dates are in a recognizable format

#### Modifying Users
Edit the `users` dictionary in `setup_data.py` to add/remove users or adjust financial parameters.

#### Styling
Custom CSS is defined in the `load_custom_css()` function in `app.py`. Modify the hex codes and styles to match your preferences.

## Technical Stack

- **Framework**: Streamlit 1.28+
- **Data Processing**: Pandas 2.0+
- **Visualizations**: Plotly 5.17+
- **Excel Handling**: Openpyxl 3.1+
- **Numerical Computing**: NumPy 1.24+

## Features Breakdown

### Summary Overview
- Net worth tracking with month-over-month comparison
- Total assets and investment portfolio values
- Average monthly income calculation
- Net worth trend line chart
- Asset allocation pie chart
- Monthly income vs expenses bar chart

### Investment Tracker
- Total portfolio value with return percentage
- Portfolio value timeline
- Current asset allocation pie chart
- Individual asset performance comparison
- Monthly contribution tracking

### Mortgage Debt Tracker
- Remaining balance tracking
- Principal vs interest breakdown
- Monthly payment details
- Cumulative interest paid analysis
- Balance reduction timeline

### Assets & Liabilities
- Complete balance sheet view
- Net worth calculation and trend
- Asset and liability pie charts
- Detailed itemized tables
- Category-based breakdowns

### Salary Tracker
- YTD gross and net income
- Tax paid analysis
- Average monthly net income
- Income timeline charts
- Monthly breakdown with tax and super
- Effective tax rate analysis

### Retirement Calculator
- Interactive retirement planning tool
- Customizable inputs (age, contributions, returns)
- Projection calculations with compound interest
- Visual growth timeline
- Gap analysis (surplus/shortfall)
- Personalized recommendations

## Future Enhancements

Potential features for future development:
- **Comparison Mode**: Overlay data from multiple users (Vincent vs Amy)
- **Export Functionality**: Generate PDF reports
- **Budget Tracker**: Monthly budget planning and tracking
- **Goal Setting**: Set and track financial goals
- **Expense Categorization**: Detailed expense tracking
- **Mobile Responsive**: Optimize for mobile devices
- **Data Import**: Upload your own Excel files via UI
- **Authentication**: Secure login system

## Troubleshooting

### Common Issues

**"No module named 'streamlit'"**
- Ensure you've installed requirements: `pip install -r requirements.txt`

**"FileNotFoundError: data/Salary_Tracker.xlsx"**
- Run the data generation script: `python setup_data.py`

**Charts not displaying properly**
- Clear browser cache and refresh the page
- Try a different browser (Chrome/Firefox recommended)

**Session state issues**
- Click "Change User" in the sidebar to reset
- Refresh the browser page

## Contributing

This is a personal finance dashboard. Feel free to fork and customize for your own use.

## License

This project is provided as-is for personal use.

## Author

Built with ❤️ using Streamlit

---

**Note**: All data generated by `setup_data.py` is fictional and for demonstration purposes only.
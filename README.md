# My Finance Hub 💰

A professional personal finance dashboard built with Streamlit, powered by real financial data from Excel spreadsheets.

## 🎯 Overview

My Finance Hub is a comprehensive financial tracking application that ingests real financial data and provides powerful visualizations and insights. This is NOT a simulation - it uses actual transaction data, employment history, and asset/liability records.

## ✨ Features

### 📊 Dashboard
- Real-time net worth calculation and tracking
- Asset vs liability comparison
- Month-over-month growth analysis
- Interactive trend visualizations

### 💰 Net Worth Analysis
- Comprehensive net worth progression tracking
- Compound Annual Growth Rate (CAGR) calculation
- Month-over-month change analysis
- Linear trend analysis with predictive modeling
- Detailed asset and liability breakdown tables

### 💼 Investment Portfolio
- Transaction-level investment tracking
- Portfolio allocation visualization
- Cumulative investment analysis
- Investment activity trends by month
- Detailed transaction history

### 👔 Employment History
- Complete employment timeline
- Compensation analysis by company and role type
- Duration tracking for each position
- Total compensation calculations

### 📈 Growth Analysis
- Year-over-year net worth growth
- Asset category growth breakdown
- CAGR calculation
- Total invested vs total earned comparison

## 🗂️ Data Structure

The application reads from a single Excel file (`vincent_financial_data.xlsx`) with three standardized sheets:

### 1. Assets & Liabilities (Wide Format)
- **Structure**: Dates as columns, categories as rows
- **Smart Date Filtering**: Automatically stops at the first empty "Cash" cell (future dates ignored)
- **Dynamic Section Detection**: Finds "Assets" and "Liabilities" sections dynamically (robust to empty rows)
- **Template-Reusable**: Designed to work with any file following this schema

### 2. Employment (Long Format)
- Standard database format with dates as rows
- Columns: Date Started, Date Ended, Company, Position, Type, Base Salary, Super, Bonus, Stock, Total Compensation, Comments
- Automatic duration calculation

### 3. Investments - Cost Basis (Long Format)
- Transaction log format
- Columns: Trade Date, Settlement Date, Symbol, Side, Trade Identifier, Units, Avg. Price, Value, Fees, GST, Total Value, Currency, AUD/USD rate
- Buy/sell tracking with portfolio summary

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Navigate to the repository**
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

4. **Ensure your data file exists**
   - Place your Excel file at: `data/vincent_financial_data.xlsx`
   - The file must contain the three required sheets with proper formatting
   - Future users can have their own files (e.g., `data/partner_financial_data.xlsx`)

5. **Test the data parser**
   ```bash
   python test_parser.py
   ```

6. **Run the application**
   ```bash
   streamlit run app.py
   ```

7. **Access the dashboard**
   - The app will automatically open in your default browser
   - If not, navigate to `http://localhost:8501`

## 📁 Project Structure

```
my-finance-hub/
├── app.py                          # Main Streamlit application
├── data_parser.py                  # Excel data parser module
├── test_parser.py                  # Parser validation script
├── requirements.txt                # Python dependencies
├── README.md                       # This file
└── data/                           # Real financial data
    └── vincent_financial_data.xlsx # Main data file
```

## 🎨 Design Philosophy

### Visual Identity
- **Color Palette**: Professional blue (#4A9EFF) accents with clean black text on white background
- **Typography**: Inter font family for modern readability
- **Charts**: Interactive Plotly visualizations with consistent styling
- **Layout**: Responsive, wide-format dashboard optimized for data analysis

### Code Architecture
- **Reusable Parser**: The `FinanceDataParser` class can handle any Excel file following the template
- **Single User Focus**: Currently optimized for one user, easily extensible to multiple users
- **Cached Data Loading**: Streamlit caching for optimal performance
- **Separation of Concerns**: Data parsing separate from visualization logic

## 💡 Usage Tips

### Navigation
- Use the sidebar to switch between different views
- Each page provides different insights into your financial data
- All charts are interactive - hover for details, click legends to filter

### Data Updates
- Simply update your Excel file with new data
- Restart the Streamlit app to see the latest information
- The parser automatically handles new dates and categories

### Future Multi-User Support
To add another user (e.g., a partner):
1. Create a new Excel file following the same template structure
2. Modify the `load_data()` function to accept a user parameter
3. Add user selection logic to the sidebar

## 📊 Visualizations Included

1. **Net Worth Trend** - Line chart with area fill showing progression over time
2. **Asset Breakdown** - Donut chart showing current asset allocation
3. **Assets vs Liabilities** - Grouped bar chart for period comparison
4. **Net Worth Progression with Trend Line** - Linear regression trend analysis
5. **Month-over-Month Changes** - Bar chart with percentage labels
6. **Investment Activity** - Monthly investment visualization
7. **Portfolio Allocation** - Pie chart of investment holdings
8. **Employment Timeline** - Gantt-style timeline of positions
9. **Year-over-Year Growth** - Dual-axis chart with growth rate overlay
10. **Asset Category Growth** - Growth breakdown by asset type

## 🔧 Technical Details

### Dependencies
- `streamlit` - Web application framework
- `pandas` - Data manipulation and analysis
- `plotly` - Interactive visualizations
- `openpyxl` - Excel file reading
- `numpy` - Numerical computing
- `scikit-learn` - Trend line modeling

### Key Features
- **Smart Date Detection**: Uses "Cash" row to determine valid date columns
- **Dynamic Section Parsing**: Finds asset/liability sections by keyword search
- **Robust Error Handling**: Validates file structure and required sheets
- **Type Conversion**: Automatic handling of dates, numbers, and text
- **Summary Functions**: Pre-built methods for common financial calculations

## 🎓 Learning from This Project

This project demonstrates:
- Real-world data ingestion from Excel
- Financial data modeling and analysis
- Interactive dashboard development with Streamlit
- Separation of data parsing from presentation logic
- Reusable template-based data structures
- Professional data visualization techniques

## 📝 Notes

- **No Synthetic Data**: All dummy data generators have been removed
- **Single Source of Truth**: The Excel file is the only data source
- **Template-Based**: The parser is designed to work with the specific Excel schema
- **Production Ready**: This is a real application using actual financial data

## 🚦 Next Steps

To extend this application:
1. Add data export functionality
2. Implement data validation and error reporting
3. Create data entry forms for updating the Excel file
4. Add goal tracking and forecasting
5. Implement multi-user support with separate data files
6. Add authentication and security features
7. Create automated backup and versioning

---

**Built with real data. Designed for real insights.**

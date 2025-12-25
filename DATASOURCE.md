# Data Source Documentation

This document details exactly where each visualization and data table in the My Finance Hub dashboard pulls its data from.

**Excel File**: `data/vincent_financial_data.xlsx`

---

## 📊 Dashboard Page

### Dashboard - User Information (Bottom Left Sidebar)
- **Data Source**: Sheet `Info`
- **Fields Used**:
  - Row 0: Full Name (Column 0: "Full Name", Column 1: User's full name)
  - Row 1: DOB (Column 0: "DOB", Column 1: Date of birth)
  - Row 2: Currency (Column 0: "Currency", Column 1: Currency code e.g., AUD)

### Dashboard - Net Worth Metric Card
- **Data Source**: Sheet `Assets & Liabilities`
- **Calculation**: 
  - Latest date's Total Assets - Latest date's Total Liabilities
  - Uses `get_latest_metrics()` method
  - Parses all asset and liability rows from columns 1 onwards (dates in row 0)
  - Stops parsing at first NaN in "Cash - Commbank & ING" row

### Dashboard - Total Assets Metric Card
- **Data Source**: Sheet `Assets & Liabilities`
- **Calculation**: 
  - Sum of all Asset category items for latest date
  - Uses `get_latest_metrics()` method

### Dashboard - Total Liabilities Metric Card
- **Data Source**: Sheet `Assets & Liabilities`
- **Calculation**: 
  - Sum of all Liability category items for latest date
  - Uses `get_latest_metrics()` method

### Dashboard - Net Worth Trend (Line Chart)
- **Data Source**: Sheet `Assets & Liabilities`
- **Calculation**:
  - Uses `get_net_worth_timeseries()` method
  - For each date column: Assets - Liabilities
  - X-axis: Dates from row 0 (starting column 1)
  - Y-axis: Calculated Net Worth for each date

### Dashboard - Asset Breakdown (Pie Chart)
- **Data Source**: Sheet `Assets & Liabilities`
- **Calculation**:
  - Uses `get_asset_breakdown()` method
  - Groups all Asset category items by Type
  - Shows latest date only
  - Data structure: Each row in "Assets" section has Type name in column 0, values in date columns

### Dashboard - Assets vs Liabilities Over Time (Bar Chart)
- **Data Source**: Sheet `Assets & Liabilities`
- **Calculation**:
  - Uses `get_net_worth_timeseries()` method
  - For each date: Sum of Assets and Sum of Liabilities
  - Grouped bar chart showing both categories over time

---

## 💰 Net Worth Page

### Net Worth - Current Net Worth Metric Card
- **Data Source**: Sheet `Assets & Liabilities`
- **Calculation**: 
  - Most recent date's Assets - Liabilities
  - Uses `get_net_worth_timeseries()` method, takes last row

### Net Worth - Total Growth Metric Card
- **Data Source**: Sheet `Assets & Liabilities`
- **Calculation**: 
  - Latest Net Worth - First Net Worth
  - Uses `get_net_worth_timeseries()` method

### Net Worth - Growth Rate Metric Card
- **Data Source**: Sheet `Assets & Liabilities`
- **Calculation**: 
  - ((Current NW - Initial NW) / Initial NW) * 100
  - Uses `get_net_worth_timeseries()` method

### Net Worth - Average Monthly Growth Metric Card
- **Data Source**: Sheet `Assets & Liabilities`
- **Calculation**: 
  - Total Growth / Number of months elapsed
  - Uses `get_net_worth_timeseries()` method

### Net Worth - Net Worth Progression (Line Chart with Trend)
- **Data Source**: Sheet `Assets & Liabilities`
- **Calculation**:
  - Blue line: Net Worth over time from `get_net_worth_timeseries()`
  - Red dashed line: Linear regression trend line
  - X-axis: Dates, Y-axis: Net Worth values

### Net Worth - Month-over-Month Changes (Bar Chart)
- **Data Source**: Sheet `Assets & Liabilities`
- **Calculation**:
  - Uses `get_net_worth_timeseries()` method
  - Calculates difference between consecutive dates
  - Green bars: positive change, Red bars: negative change
  - Percentage shown as text on bars

---

## 💼 Investments Page

### Investments - Total Invested Metric Card
- **Data Source**: Sheet `Investments - Cost Basis`
- **Calculation**: 
  - Sum of all "Total Value" column (Column E)
  - Uses `get_investment_summary()` method

### Investments - Active Holdings Metric Card
- **Data Source**: Sheet `Investments - Cost Basis`
- **Calculation**: 
  - Count of unique symbols with net positive units (Buys - Sells > 0)
  - Uses `get_investment_summary()` method

### Investments - Total Transactions Metric Card
- **Data Source**: Sheet `Investments - Cost Basis`
- **Calculation**: 
  - Count of all rows in sheet
  - Uses `load_investments()` method
  - Columns: Trade Date (A), Symbol (B), Side (C), Units (D), Total Value (E)

### Investments - Cumulative Investment (Line Chart)
- **Data Source**: Sheet `Investments - Cost Basis`
- **Calculation**: 
  - Running sum of "Total Value" column over time
  - Sorted by "Trade Date" column
  - X-axis: Trade Date, Y-axis: Cumulative investment

### Investments - Investment by Symbol (Bar Chart)
- **Data Source**: Sheet `Investments - Cost Basis`
- **Calculation**: 
  - Groups by "Symbol" column
  - Sums "Total Value" for each symbol
  - Only shows symbols with positive net units

### Investments - Buy vs Sell Activity (Pie Chart)
- **Data Source**: Sheet `Investments - Cost Basis`
- **Calculation**: 
  - Groups by "Side" column (Buy/Sell)
  - Sums "Total Value" for each side

---

## 👔 Employment Page

### Employment - Total Compensation Metric Card
- **Data Source**: Sheet `Employment`
- **Calculation**: 
  - Sum of "Total Compensation" column (Column E)
  - Uses `load_employment()` method

### Employment - Total Positions Metric Card
- **Data Source**: Sheet `Employment`
- **Calculation**: 
  - Count of rows
  - Uses `load_employment()` method
  - Columns: Company (B), Role (C), Type (D), Total Compensation (E), Start Date (F), End Date (G)

### Employment - Average Compensation Metric Card
- **Data Source**: Sheet `Employment`
- **Calculation**: 
  - Mean of "Total Compensation" column
  - Uses `load_employment()` method

### Employment - Compensation by Company (Bar Chart)
- **Data Source**: Sheet `Employment`
- **Calculation**: 
  - X-axis: "Company" column
  - Y-axis: "Total Compensation" column
  - Direct mapping, no aggregation

### Employment - Employment Type Distribution (Pie Chart)
- **Data Source**: Sheet `Employment`
- **Calculation**: 
  - Groups by "Type" column
  - Sums "Total Compensation" for each type

---

## 📈 Growth Analysis Page

### Growth - CAGR (Compound Annual Growth Rate) Metric Card
- **Data Source**: Sheet `Assets & Liabilities`
- **Calculation**: 
  - Uses `calculate_cagr()` method
  - Formula: ((Ending NW / Beginning NW)^(1/years) - 1) * 100
  - Uses `get_net_worth_timeseries()` for start and end values

### Growth - Total Invested Metric Card
- **Data Source**: Sheet `Investments - Cost Basis`
- **Calculation**: 
  - Sum of "Total Value" column
  - Uses `load_investments()` method

### Growth - Total Earned Metric Card
- **Data Source**: Sheet `Employment`
- **Calculation**: 
  - Sum of "Total Compensation" column
  - Uses `load_employment()` method

### Growth - Year-over-Year Net Worth Growth (Bar Chart)
- **Data Source**: Sheet `Assets & Liabilities`
- **Calculation**: 
  - Uses `get_net_worth_timeseries()` method
  - Groups by year (from date column)
  - Takes last net worth value for each year
  - Calculates year-over-year percentage change

### Growth - Asset Category Growth (Bar Chart)
- **Data Source**: Sheet `Assets & Liabilities`
- **Calculation**: 
  - Uses `load_assets_liabilities()` method
  - For each asset type: Final value - Initial value
  - Growth % calculated as: ((Final - Initial) / Initial) * 100
  - Green bars for positive growth, red for negative

---

## 📋 Excel Sheet Structures

### Sheet: `Info`
- **Structure**: 3 rows × 2 columns (no headers)
  - Row 0: Full Name | [User's Name]
  - Row 1: DOB | [Date of Birth]
  - Row 2: Currency | [Currency Code]

### Sheet: `Assets & Liabilities`
- **Structure**: Wide format with dates as columns
  - Row 0: [blank] | Date 1 | Date 2 | Date 3 | ...
  - Row 1+: Contains "Liabilities" section header
  - Following rows: Liability Type | Value 1 | Value 2 | ...
  - Later rows: Contains "Assets" section header
  - Following rows: Asset Type | Value 1 | Value 2 | ...
  - **Special Row**: "Cash - Commbank & ING" - used for "Cash stop" logic (first NaN determines last valid date)

### Sheet: `Employment`
- **Structure**: Table with headers
  - Column A: (Row number/index)
  - Column B: Company
  - Column C: Role
  - Column D: Type (e.g., Full-time, Part-time, Contract)
  - Column E: Total Compensation
  - Column F: Start Date
  - Column G: End Date

### Sheet: `Investments - Cost Basis`
- **Structure**: Table with headers
  - Column A: Trade Date
  - Column B: Symbol (ticker/stock code)
  - Column C: Side (Buy/Sell)
  - Column D: Units (quantity)
  - Column E: Total Value (cost/proceeds)

---

## 🔧 Data Loading Methods

All data loading is handled by `data_loader.py` class methods:

- `get_user_info()` → Info sheet
- `load_assets_liabilities()` → Assets & Liabilities sheet with Cash stop logic
- `get_net_worth_timeseries()` → Calculates from Assets & Liabilities
- `get_latest_metrics()` → Latest date from Assets & Liabilities
- `get_asset_breakdown()` → Groups Assets by Type for latest/specified date
- `get_liability_breakdown()` → Groups Liabilities by Type for latest/specified date
- `load_investments()` → Investments - Cost Basis sheet
- `get_investment_summary()` → Aggregates Investments by Symbol
- `load_employment()` → Employment sheet
- `calculate_cagr()` → Calculates from net worth timeseries

---

**Note**: All monetary values are stored as numbers in Excel. The dashboard applies currency formatting (`$` symbol, thousands separators) during display only.

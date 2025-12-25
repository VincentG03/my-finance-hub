# Dash Migration Guide

## Running the Dash Application

Your Streamlit dashboard has been migrated to a professional Plotly Dash application using Dash Mantine Components (DMC).

### Installation

1. **Install Dash dependencies:**
   ```bash
   pip install dash>=2.14.0 dash-mantine-components>=0.12.0
   ```

   Or install all requirements:
   ```bash
   pip install -r requirements.txt
   ```

### Running the App

**Start the Dash Application:**
```bash
python dash_app.py
```

Then open your browser to: **http://localhost:8050**

**Stop the Dash Application:**

Press `Ctrl+C` in the terminal where the app is running, or:
```bash
# Find and kill the process
pkill -f "python.*dash_app.py"

# Or find the process ID and kill it
ps aux | grep "dash_app.py" | grep -v grep | awk '{print $2}' | xargs kill
```

**Original Streamlit App (still available):**
```bash
streamlit run app.py
```

## Architecture

### `data_loader.py`
Robust data loading module with:
- **Cash Stop Logic**: Automatically stops parsing Assets & Liabilities sheet when "Cash - Commbank & ING" row has an empty cell
- **Dynamic Section Detection**: Finds "Assets" and "Liabilities" headers dynamically (handles spacer rows)
- **Caching**: Parsed data is cached until `reload_all()` is called
- **Type Safety**: Proper date and numeric conversions

### `dash_app.py`
Professional FinTech UI using:
- **Dash Mantine Components**: Modern, professional component library
- **AppShell Layout**: Persistent sidebar navigation with main content area
- **Metric Cards**: Clean `dmc.Paper` components replacing HTML metric cards
- **Plotly Charts**: All charts use `template='plotly_white'` for consistency
- **Navigation Callbacks**: Dynamic page switching without page reloads

## Key Features Implemented

### 📊 Dashboard Page
- Net worth, assets, and liabilities metrics with change indicators
- Net worth trend line chart
- Asset breakdown donut chart
- Assets vs Liabilities grouped bar chart

### 💰 Net Worth Page
- Current net worth, total growth, growth rate, and average monthly growth
- Net worth progression with linear regression trend line
- Month-over-month change analysis with color-coded bars

### 💼 Investments Page
- Total invested, unique holdings, and transaction count
- Cumulative investment value over time
- Portfolio allocation pie chart
- Monthly investment activity bar chart

### 👔 Employment Page
- Total compensation, positions count, and average compensation
- Compensation by company bar chart
- Employment type distribution pie chart

### 📈 Growth Analysis Page
- CAGR (Compound Annual Growth Rate) calculation
- Year-over-year net worth growth with dual-axis chart
- Asset category growth breakdown

## Design Philosophy

### Professional FinTech Aesthetic
- **Clean Layout**: AppShell with persistent sidebar navigation
- **Consistent Typography**: Inter font family throughout
- **Metric Cards**: Mantine Paper components with subtle shadows and borders
- **Chart Styling**: All Plotly charts use `plotly_white` template
- **Color Scheme**: Blue primary (#4A9EFF), green for positive (#10B981), red for negative (#EF4444)

### No CSS Hacks
- Pure Dash Mantine Components
- Theme configuration via `MantineProvider`
- Component-based styling using DMC props (`p`, `radius`, `withBorder`, `shadow`)

## Data Structure Handling

The data loader correctly handles your Excel structure:

### Assets & Liabilities Sheet
- **Wide Format**: Dates as columns, categories as rows
- **Cash Stop Logic**: Iterates through date columns until "Cash - Commbank & ING" row is empty
- **Dynamic Sections**: Searches for "Assets" and "Liabilities" keywords in column A
- **Spacer Rows**: Automatically skips empty rows between sections

### Employment & Investments Sheets
- Standard tabular format (dates as rows)
- Automatic date parsing and duration calculation
- Numeric type conversion for all financial columns

## Customization

### Changing Colors
Edit the theme in `dash_app.py`:
```python
theme={
    "primaryColor": "blue",  # Change to: "indigo", "violet", "teal", etc.
    "fontFamily": "Inter, system-ui, sans-serif",
}
```

### Adding New Pages
1. Create a new layout function (e.g., `def my_page_layout()`)
2. Add navigation item to `create_navbar()`
3. Update the `update_page()` callback to handle the new page

### Modifying Charts
All charts use Plotly Graph Objects. Customize by editing the `fig.update_layout()` calls:
```python
fig.update_layout(
    template='plotly_white',  # Or 'plotly_dark', 'seaborn', etc.
    font=dict(family='Inter, sans-serif', size=12),
    # Add more customizations...
)
```

## Performance Notes

- **Data Caching**: `FinanceDataLoader` caches parsed data
- **Lazy Loading**: Data is only parsed when first accessed
- **Force Reload**: Call `data_loader.reload_all()` to refresh from Excel

## Migration Benefits

✅ **Professional UI**: Modern FinTech aesthetic without CSS hacks  
✅ **Component-Based**: Reusable Mantine components  
✅ **Type Safety**: Better type hints in data loader  
✅ **Maintainable**: Cleaner separation of data and presentation  
✅ **Scalable**: Easy to add new pages and features  
✅ **Robust Parsing**: Handles Excel edge cases properly  

## Comparison: Streamlit vs Dash

| Feature | Streamlit | Dash |
|---------|-----------|------|
| UI Framework | Custom HTML/CSS | Dash Mantine Components |
| Navigation | Page reloads | Callback-based (no reload) |
| Data Loading | `@st.cache_data` | Class-based caching |
| Styling | CSS in markdown | Component props + theme |
| State Management | Session state | Callback context |
| Performance | Good for prototypes | Better for production |

Both apps are fully functional and can coexist in the same project!

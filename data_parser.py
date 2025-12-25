"""
Real Data Parser for My Finance Hub
Parses the vincent_financial_data.xlsx file with proper handling of the specific structure
"""

import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path


class FinanceDataParser:
    """Parser for the standardized financial data Excel template"""
    
    def __init__(self, excel_path):
        """
        Initialize parser with path to Excel file
        
        Args:
            excel_path: Path to the Excel file (e.g., 'data/vincent_financial_data.xlsx')
        """
        self.excel_path = excel_path
        self._validate_file()
    
    def _validate_file(self):
        """Validate that the Excel file exists and has required sheets"""
        if not Path(self.excel_path).exists():
            raise FileNotFoundError(f"Excel file not found: {self.excel_path}")
        
        # Check required sheets exist
        xl = pd.ExcelFile(self.excel_path)
        required_sheets = ['Assets & Liabilities', 'Employment', 'Investments - Cost Basis']
        missing_sheets = [s for s in required_sheets if s not in xl.sheet_names]
        
        if missing_sheets:
            raise ValueError(f"Missing required sheets: {missing_sheets}")
    
    def parse_assets_liabilities(self):
        """
        Parse the Assets & Liabilities sheet (wide format)
        
        Returns:
            DataFrame in long format with columns: Date, Category, Type, Value
        """
        # Read the entire sheet without header
        df_raw = pd.read_excel(self.excel_path, sheet_name='Assets & Liabilities', header=None)
        
        # First row contains dates (starting from column 1)
        date_row = df_raw.iloc[0, 1:].values
        dates = pd.to_datetime(date_row, errors='coerce')
        
        # Find the "Cash - Commbank & ING" row to determine valid date columns
        cash_row_idx = None
        for i, val in enumerate(df_raw.iloc[:, 0]):
            if pd.notna(val) and 'Cash' in str(val) and 'Commbank' in str(val):
                cash_row_idx = i
                break
        
        if cash_row_idx is None:
            raise ValueError("Could not find 'Cash - Commbank & ING' row for date filtering")
        
        # Get cash row values and find where data ends (first NaN)
        cash_values = df_raw.iloc[cash_row_idx, 1:].values
        valid_date_count = 0
        for val in cash_values:
            if pd.isna(val):
                break
            valid_date_count += 1
        
        # Filter to only valid dates
        valid_dates = dates[:valid_date_count]
        
        # Find Assets and Liabilities section start rows
        assets_row = None
        liabilities_row = None
        
        for i, val in enumerate(df_raw.iloc[:, 0]):
            if pd.notna(val):
                if str(val).strip().lower() == 'assets':
                    assets_row = i
                elif str(val).strip().lower() == 'liabilities':
                    liabilities_row = i
        
        if assets_row is None or liabilities_row is None:
            raise ValueError("Could not find 'Assets' or 'Liabilities' section headers")
        
        # Parse both sections
        result_data = []
        
        # Parse Liabilities (comes first in the file)
        for row_idx in range(liabilities_row + 1, assets_row):
            category_name = df_raw.iloc[row_idx, 0]
            
            # Skip empty rows
            if pd.isna(category_name):
                continue
            
            # Get values for this category
            values = df_raw.iloc[row_idx, 1:valid_date_count + 1].values
            
            for date, value in zip(valid_dates, values):
                if pd.notna(value) and value != 0:
                    result_data.append({
                        'Date': date,
                        'Category': 'Liability',
                        'Type': str(category_name).strip(),
                        'Value': float(value)
                    })
        
        # Parse Assets (after assets_row until end of data)
        for row_idx in range(assets_row + 1, len(df_raw)):
            category_name = df_raw.iloc[row_idx, 0]
            
            # Skip empty rows
            if pd.isna(category_name):
                continue
            
            # Get values for this category
            values = df_raw.iloc[row_idx, 1:valid_date_count + 1].values
            
            for date, value in zip(valid_dates, values):
                if pd.notna(value) and value != 0:
                    result_data.append({
                        'Date': date,
                        'Category': 'Asset',
                        'Type': str(category_name).strip(),
                        'Value': float(value)
                    })
        
        # Convert to DataFrame and sort
        df_result = pd.DataFrame(result_data)
        if not df_result.empty:
            df_result = df_result.sort_values(['Date', 'Category', 'Type']).reset_index(drop=True)
        
        return df_result
    
    def parse_employment(self):
        """
        Parse the Employment sheet (long format)
        
        Returns:
            DataFrame with employment history
        """
        df = pd.read_excel(self.excel_path, sheet_name='Employment')
        
        # Convert date columns to datetime
        if 'Date Started' in df.columns:
            df['Date Started'] = pd.to_datetime(df['Date Started'], errors='coerce')
        if 'Date Ended' in df.columns:
            df['Date Ended'] = pd.to_datetime(df['Date Ended'], errors='coerce')
        
        # Calculate duration for each job
        if 'Date Started' in df.columns and 'Date Ended' in df.columns:
            df['Duration (days)'] = (df['Date Ended'] - df['Date Started']).dt.days
            df['Duration (months)'] = df['Duration (days)'] / 30.44  # Average month length
        
        return df
    
    def parse_investments(self):
        """
        Parse the Investments - Cost Basis sheet (transaction log)
        
        Returns:
            DataFrame with investment transactions
        """
        df = pd.read_excel(self.excel_path, sheet_name='Investments - Cost Basis')
        
        # Convert date columns to datetime
        if 'Trade Date' in df.columns:
            df['Trade Date'] = pd.to_datetime(df['Trade Date'], errors='coerce')
        if 'Settlement Date' in df.columns:
            df['Settlement Date'] = pd.to_datetime(df['Settlement Date'], errors='coerce')
        
        # Ensure numeric columns are properly typed
        numeric_cols = ['Units', 'Avg. Price', 'Value', 'Fees', 'GST', 'Total Value']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        return df
    
    def get_all_data(self):
        """
        Parse all sheets and return as a dictionary
        
        Returns:
            dict with keys: 'assets_liabilities', 'employment', 'investments'
        """
        return {
            'assets_liabilities': self.parse_assets_liabilities(),
            'employment': self.parse_employment(),
            'investments': self.parse_investments()
        }
    
    def get_latest_net_worth(self):
        """
        Calculate the most recent net worth
        
        Returns:
            tuple: (date, net_worth, total_assets, total_liabilities)
        """
        df = self.parse_assets_liabilities()
        
        if df.empty:
            return None, 0, 0, 0
        
        latest_date = df['Date'].max()
        latest_data = df[df['Date'] == latest_date]
        
        total_assets = latest_data[latest_data['Category'] == 'Asset']['Value'].sum()
        total_liabilities = latest_data[latest_data['Category'] == 'Liability']['Value'].sum()
        net_worth = total_assets - total_liabilities
        
        return latest_date, net_worth, total_assets, total_liabilities
    
    def get_investment_summary(self):
        """
        Calculate investment summary statistics
        
        Returns:
            DataFrame with summary by symbol
        """
        df = self.parse_investments()
        
        if df.empty:
            return pd.DataFrame()
        
        # Group by symbol and calculate metrics
        summary = df.groupby('Symbol').agg({
            'Units': lambda x: (df[df['Symbol'] == x.name]['Units'] * 
                               df[df['Symbol'] == x.name]['Side'].map({'Buy': 1, 'Sell': -1})).sum(),
            'Total Value': 'sum',
            'Trade Date': ['min', 'max']
        }).reset_index()
        
        summary.columns = ['Symbol', 'Total Units', 'Total Invested', 'First Trade', 'Last Trade']
        
        # Filter out holdings with zero units (fully sold)
        summary = summary[summary['Total Units'] > 0]
        
        return summary
    
    def get_employment_summary(self):
        """
        Get employment summary with total compensation by company
        
        Returns:
            DataFrame with employment summary
        """
        df = self.parse_employment()
        
        if df.empty:
            return pd.DataFrame()
        
        # Add calculated fields
        summary = df.copy()
        
        # Sort by date started (most recent first)
        summary = summary.sort_values('Date Started', ascending=False)
        
        return summary


# Convenience function for quick data loading
def load_financial_data(excel_path='data/vincent_financial_data.xlsx'):
    """
    Quick loader function
    
    Args:
        excel_path: Path to the Excel file
    
    Returns:
        FinanceDataParser instance
    """
    return FinanceDataParser(excel_path)


if __name__ == "__main__":
    # Test the parser
    parser = load_financial_data()
    
    print("=== Testing Data Parser ===\n")
    
    # Test Assets & Liabilities
    print("Assets & Liabilities:")
    al_df = parser.parse_assets_liabilities()
    print(f"  Total records: {len(al_df)}")
    print(f"  Date range: {al_df['Date'].min()} to {al_df['Date'].max()}")
    print(f"  Categories: {al_df['Category'].unique()}")
    print(f"  Sample:\n{al_df.head(10)}\n")
    
    # Test Employment
    print("Employment:")
    emp_df = parser.parse_employment()
    print(f"  Total jobs: {len(emp_df)}")
    print(f"  Sample:\n{emp_df.head()}\n")
    
    # Test Investments
    print("Investments:")
    inv_df = parser.parse_investments()
    print(f"  Total transactions: {len(inv_df)}")
    print(f"  Unique symbols: {inv_df['Symbol'].nunique()}")
    print(f"  Sample:\n{inv_df.head()}\n")
    
    # Test summary functions
    print("Latest Net Worth:")
    date, nw, assets, liabs = parser.get_latest_net_worth()
    print(f"  Date: {date}")
    print(f"  Net Worth: ${nw:,.2f}")
    print(f"  Assets: ${assets:,.2f}")
    print(f"  Liabilities: ${liabs:,.2f}")

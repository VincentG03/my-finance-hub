"""
Data Loader for Finance Dashboard
Robust Excel parser with "Cash stop" logic for Assets & Liabilities sheet
"""

import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
from typing import Tuple, Dict, Optional


class FinanceDataLoader:
    """
    Load and parse financial data from Excel file
    Implements special parsing logic for wide-format Assets & Liabilities sheet
    """
    
    def __init__(self, excel_path: str = 'data/vincent_financial_data.xlsx'):
        """
        Initialize data loader
        
        Args:
            excel_path: Path to the Excel file
        """
        self.excel_path = excel_path
        self._validate_file()
        
        # Cache parsed data
        self._assets_liabilities_df = None
        self._employment_df = None
        self._investments_df = None
    
    def _validate_file(self):
        """Validate Excel file exists and has required sheets"""
        if not Path(self.excel_path).exists():
            raise FileNotFoundError(f"Excel file not found: {self.excel_path}")
        
        xl = pd.ExcelFile(self.excel_path)
        required_sheets = ['Assets & Liabilities', 'Employment', 'Investments - Cost Basis']
        missing = [s for s in required_sheets if s not in xl.sheet_names]
        
        if missing:
            raise ValueError(f"Missing required sheets: {missing}")
    
    def load_assets_liabilities(self, force_reload: bool = False) -> pd.DataFrame:
        """
        Load Assets & Liabilities sheet with Cash stop logic
        
        Returns:
            DataFrame with columns: Date, Category, Type, Value
        """
        if self._assets_liabilities_df is not None and not force_reload:
            return self._assets_liabilities_df
        
        # Read raw sheet without header
        df_raw = pd.read_excel(self.excel_path, sheet_name='Assets & Liabilities', header=None)
        
        # Row 0 contains dates (starting from column 1)
        date_row = df_raw.iloc[0, 1:].values
        dates = pd.to_datetime(date_row, errors='coerce')
        
        # Find "Cash - Commbank & ING" row for stop logic
        cash_row_idx = self._find_cash_row(df_raw)
        
        # Implement "Cash stop" logic - count valid dates until first NaN in Cash row
        valid_date_count = self._count_valid_dates(df_raw, cash_row_idx)
        valid_dates = dates[:valid_date_count]
        
        # Find Assets and Liabilities section headers dynamically
        assets_row, liabilities_row = self._find_section_headers(df_raw)
        
        # Parse both sections
        result_data = []
        
        # Parse Liabilities (comes before Assets in file)
        result_data.extend(
            self._parse_section(df_raw, liabilities_row + 1, assets_row, 
                               valid_dates, valid_date_count, 'Liability')
        )
        
        # Parse Assets (after Assets header until end)
        result_data.extend(
            self._parse_section(df_raw, assets_row + 1, len(df_raw), 
                               valid_dates, valid_date_count, 'Asset')
        )
        
        # Convert to DataFrame
        self._assets_liabilities_df = pd.DataFrame(result_data)
        if not self._assets_liabilities_df.empty:
            self._assets_liabilities_df = self._assets_liabilities_df.sort_values(
                ['Date', 'Category', 'Type']
            ).reset_index(drop=True)
        
        return self._assets_liabilities_df
    
    def _find_cash_row(self, df_raw: pd.DataFrame) -> int:
        """Find the Cash row index for stop logic"""
        for i, val in enumerate(df_raw.iloc[:, 0]):
            if pd.notna(val) and 'Cash' in str(val) and 'Commbank' in str(val):
                return i
        raise ValueError("Could not find 'Cash - Commbank & ING' row")
    
    def _count_valid_dates(self, df_raw: pd.DataFrame, cash_row_idx: int) -> int:
        """Count valid dates until first NaN in Cash row"""
        cash_values = df_raw.iloc[cash_row_idx, 1:].values
        count = 0
        for val in cash_values:
            if pd.isna(val):
                break
            count += 1
        return count
    
    def _find_section_headers(self, df_raw: pd.DataFrame) -> Tuple[int, int]:
        """Find Assets and Liabilities section header rows"""
        assets_row = None
        liabilities_row = None
        
        for i, val in enumerate(df_raw.iloc[:, 0]):
            if pd.notna(val):
                val_lower = str(val).strip().lower()
                if val_lower == 'assets':
                    assets_row = i
                elif val_lower == 'liabilities':
                    liabilities_row = i
        
        if assets_row is None or liabilities_row is None:
            raise ValueError("Could not find 'Assets' or 'Liabilities' section headers")
        
        return assets_row, liabilities_row
    
    def _parse_section(self, df_raw: pd.DataFrame, start_row: int, end_row: int,
                       valid_dates: np.ndarray, valid_date_count: int, 
                       category: str) -> list:
        """Parse a section (Assets or Liabilities) from the sheet"""
        data = []
        
        for row_idx in range(start_row, end_row):
            category_name = df_raw.iloc[row_idx, 0]
            
            # Skip empty rows
            if pd.isna(category_name):
                continue
            
            # Get values for this category
            values = df_raw.iloc[row_idx, 1:valid_date_count + 1].values
            
            # Add non-zero, non-NaN values
            for date, value in zip(valid_dates, values):
                if pd.notna(value) and value != 0:
                    data.append({
                        'Date': date,
                        'Category': category,
                        'Type': str(category_name).strip(),
                        'Value': float(value)
                    })
        
        return data
    
    def load_employment(self, force_reload: bool = False) -> pd.DataFrame:
        """
        Load Employment sheet
        
        Returns:
            DataFrame with employment history
        """
        if self._employment_df is not None and not force_reload:
            return self._employment_df
        
        df = pd.read_excel(self.excel_path, sheet_name='Employment')
        
        # Convert date columns
        if 'Date Started' in df.columns:
            df['Date Started'] = pd.to_datetime(df['Date Started'], errors='coerce')
        if 'Date Ended' in df.columns:
            df['Date Ended'] = pd.to_datetime(df['Date Ended'], errors='coerce')
        
        # Calculate duration
        if 'Date Started' in df.columns and 'Date Ended' in df.columns:
            df['Duration (days)'] = (df['Date Ended'] - df['Date Started']).dt.days
            df['Duration (months)'] = df['Duration (days)'] / 30.44
        
        self._employment_df = df
        return self._employment_df
    
    def load_investments(self, force_reload: bool = False) -> pd.DataFrame:
        """
        Load Investments - Cost Basis sheet
        
        Returns:
            DataFrame with investment transactions
        """
        if self._investments_df is not None and not force_reload:
            return self._investments_df
        
        df = pd.read_excel(self.excel_path, sheet_name='Investments - Cost Basis')
        
        # Convert date columns
        if 'Trade Date' in df.columns:
            df['Trade Date'] = pd.to_datetime(df['Trade Date'], errors='coerce')
        if 'Settlement Date' in df.columns:
            df['Settlement Date'] = pd.to_datetime(df['Settlement Date'], errors='coerce')
        
        # Ensure numeric columns
        numeric_cols = ['Units', 'Avg. Price', 'Value', 'Fees', 'GST', 'Total Value']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        self._investments_df = df
        return self._investments_df
    
    def get_net_worth_timeseries(self) -> pd.DataFrame:
        """
        Calculate net worth over time
        
        Returns:
            DataFrame with columns: Date, Assets, Liabilities, Net Worth
        """
        al_df = self.load_assets_liabilities()
        
        net_worth_data = []
        for date in sorted(al_df['Date'].unique()):
            date_data = al_df[al_df['Date'] == date]
            assets = date_data[date_data['Category'] == 'Asset']['Value'].sum()
            liabilities = date_data[date_data['Category'] == 'Liability']['Value'].sum()
            net_worth_data.append({
                'Date': date,
                'Assets': assets,
                'Liabilities': liabilities,
                'Net Worth': assets - liabilities
            })
        
        return pd.DataFrame(net_worth_data)
    
    def get_latest_metrics(self) -> Dict[str, float]:
        """
        Get latest financial metrics
        
        Returns:
            Dict with keys: date, net_worth, total_assets, total_liabilities
        """
        al_df = self.load_assets_liabilities()
        
        if al_df.empty:
            return {
                'date': None,
                'net_worth': 0,
                'total_assets': 0,
                'total_liabilities': 0
            }
        
        latest_date = al_df['Date'].max()
        latest_data = al_df[al_df['Date'] == latest_date]
        
        total_assets = latest_data[latest_data['Category'] == 'Asset']['Value'].sum()
        total_liabilities = latest_data[latest_data['Category'] == 'Liability']['Value'].sum()
        
        return {
            'date': latest_date,
            'net_worth': total_assets - total_liabilities,
            'total_assets': total_assets,
            'total_liabilities': total_liabilities
        }
    
    def get_investment_summary(self) -> pd.DataFrame:
        """
        Calculate investment summary by symbol
        
        Returns:
            DataFrame with holdings summary
        """
        inv_df = self.load_investments()
        
        if inv_df.empty:
            return pd.DataFrame()
        
        # Group by symbol
        summary_data = []
        for symbol in inv_df['Symbol'].unique():
            symbol_data = inv_df[inv_df['Symbol'] == symbol]
            
            # Calculate net units (Buy - Sell)
            total_units = 0
            for _, row in symbol_data.iterrows():
                if row['Side'] == 'Buy':
                    total_units += row['Units']
                elif row['Side'] == 'Sell':
                    total_units -= row['Units']
            
            # Only include if we still hold units
            if total_units > 0:
                summary_data.append({
                    'Symbol': symbol,
                    'Total Units': total_units,
                    'Total Invested': symbol_data['Total Value'].sum(),
                    'First Trade': symbol_data['Trade Date'].min(),
                    'Last Trade': symbol_data['Trade Date'].max()
                })
        
        return pd.DataFrame(summary_data)
    
    def get_asset_breakdown(self, date: Optional[pd.Timestamp] = None) -> pd.DataFrame:
        """
        Get asset breakdown for a specific date (or latest)
        
        Returns:
            DataFrame with Type and Value columns
        """
        al_df = self.load_assets_liabilities()
        
        if date is None:
            date = al_df['Date'].max()
        
        date_data = al_df[al_df['Date'] == date]
        assets = date_data[date_data['Category'] == 'Asset']
        
        return assets.groupby('Type')['Value'].sum().reset_index().sort_values('Value', ascending=False)
    
    def get_liability_breakdown(self, date: Optional[pd.Timestamp] = None) -> pd.DataFrame:
        """
        Get liability breakdown for a specific date (or latest)
        
        Returns:
            DataFrame with Type and Value columns
        """
        al_df = self.load_assets_liabilities()
        
        if date is None:
            date = al_df['Date'].max()
        
        date_data = al_df[al_df['Date'] == date]
        liabilities = date_data[date_data['Category'] == 'Liability']
        
        return liabilities.groupby('Type')['Value'].sum().reset_index().sort_values('Value', ascending=False)
    
    def calculate_cagr(self) -> float:
        """
        Calculate Compound Annual Growth Rate of net worth
        
        Returns:
            CAGR as percentage
        """
        nw_df = self.get_net_worth_timeseries()
        
        if len(nw_df) < 2:
            return 0.0
        
        initial_nw = nw_df.iloc[0]['Net Worth']
        current_nw = nw_df.iloc[-1]['Net Worth']
        
        years = (nw_df.iloc[-1]['Date'] - nw_df.iloc[0]['Date']).days / 365.25
        
        if years > 0 and initial_nw > 0:
            cagr = (((current_nw / initial_nw) ** (1 / years)) - 1) * 100
            return cagr
        
        return 0.0
    
    def reload_all(self):
        """Force reload all data from Excel"""
        self._assets_liabilities_df = None
        self._employment_df = None
        self._investments_df = None
        
        self.load_assets_liabilities(force_reload=True)
        self.load_employment(force_reload=True)
        self.load_investments(force_reload=True)
    
    def get_user_info(self) -> Dict[str, any]:
        """
        Load user information from Info sheet
        
        Returns:
            Dictionary with keys: full_name, dob, currency
        """
        df_info = pd.read_excel(self.excel_path, sheet_name='Info', header=None)
        
        # Extract values from the structure
        info = {}
        for idx, row in df_info.iterrows():
            key = str(row[0]).strip()
            value = row[1]
            
            if key == 'Full Name':
                info['full_name'] = str(value).strip()
            elif key == 'DOB':
                # Convert to datetime if it's not already
                if isinstance(value, str):
                    info['dob'] = pd.to_datetime(value)
                else:
                    info['dob'] = value
            elif key == 'Currency':
                info['currency'] = str(value).strip()
        
        return info


# Convenience function
def load_data(excel_path: str = 'data/vincent_financial_data.xlsx') -> FinanceDataLoader:
    """
    Convenience function to create data loader
    
    Args:
        excel_path: Path to Excel file
    
    Returns:
        FinanceDataLoader instance
    """
    return FinanceDataLoader(excel_path)

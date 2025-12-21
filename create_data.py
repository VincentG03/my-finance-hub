"""
Create Excel files with financial data for My Finance Hub
"""

import pandas as pd
import openpyxl
from openpyxl import Workbook
from datetime import datetime, timedelta
import random
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_dates(start_date, num_months):
    """Generate a list of dates spanning num_months from start_date (first day of each month)"""
    dates = []
    current = start_date.replace(day=1)  # Always start on the 1st of the month
    for _ in range(num_months):
        dates.append(current)
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1, day=1)
        else:
            current = current.replace(month=current.month + 1, day=1)
    return dates

# ==================== ASSETS & LIABILITIES ====================
def create_assets_liabilities_sheet(user_name, user_config):
    """Create assets and liabilities data for a user"""
    start_date = datetime(2022, 1, 1)
    num_months = 36
    dates = generate_dates(start_date, num_months)
    
    data = []
    
    # Starting values
    property_value = user_config['property_value']
    savings = user_config['savings']
    investments = user_config['investments']
    super_balance = user_config['super']
    vehicle = user_config['vehicle']
    
    mortgage = user_config['mortgage']
    car_loan = user_config['car_loan']
    credit_card = user_config['credit_card_base']
    
    for i, date in enumerate(dates):
        # Simulate growth/depreciation
        property_value *= 1.004  # ~5% annual
        savings += random.uniform(500, 2000)
        investments *= random.uniform(0.995, 1.015)
        super_balance *= 1.006  # ~7% annual
        vehicle *= 0.997  # Depreciation
        
        # Pay down debts
        mortgage -= random.uniform(1500, 2500)
        car_loan = max(0, car_loan - 400)
        credit_card = random.uniform(user_config['credit_card_base'] * 0.4, user_config['credit_card_base'] * 1.6)
        
        # Assets
        data.append({
            'Date': date,
            'Category': 'Asset',
            'Type': 'Property',
            'Name': 'Primary Residence',
            'Value': round(property_value, 2)
        })
        data.append({
            'Date': date,
            'Category': 'Asset',
            'Type': 'Cash',
            'Name': 'Savings Account',
            'Value': round(savings, 2)
        })
        data.append({
            'Date': date,
            'Category': 'Asset',
            'Type': 'Investment',
            'Name': 'Investment Portfolio',
            'Value': round(investments, 2)
        })
        data.append({
            'Date': date,
            'Category': 'Asset',
            'Type': 'Retirement',
            'Name': 'Superannuation',
            'Value': round(super_balance, 2)
        })
        data.append({
            'Date': date,
            'Category': 'Asset',
            'Type': 'Vehicle',
            'Name': 'Car',
            'Value': round(vehicle, 2)
        })
        
        # Liabilities
        data.append({
            'Date': date,
            'Category': 'Liability',
            'Type': 'Mortgage',
            'Name': 'Home Loan',
            'Value': round(mortgage, 2)
        })
        if car_loan > 0:
            data.append({
                'Date': date,
                'Category': 'Liability',
                'Type': 'Loan',
                'Name': 'Car Loan',
                'Value': round(car_loan, 2)
            })
        data.append({
            'Date': date,
            'Category': 'Liability',
            'Type': 'Credit Card',
            'Name': 'Credit Card Debt',
            'Value': round(credit_card, 2)
        })
    
    return pd.DataFrame(data)

# ==================== EMPLOYMENT ====================
def create_employment_sheet(user_name, user_config):
    """Create employment/salary data for a user"""
    start_date = datetime(2022, 1, 1)
    num_months = 36
    dates = generate_dates(start_date, num_months)
    
    data = []
    base_salary = user_config['base_salary']
    bonus_range = user_config['bonus_range']
    
    for date in dates:
        monthly_salary = base_salary / 12
        # Annual bonus in December
        bonus = random.uniform(bonus_range[0], bonus_range[1]) if date.month == 12 else 0
        
        # Some monthly variations
        overtime = random.uniform(0, 1000) if random.random() > 0.7 else 0
        
        gross_income = monthly_salary + bonus + overtime
        tax = gross_income * 0.25  # Simplified tax
        superannuation = gross_income * 0.11  # Australian super
        net_income = gross_income - tax
        
        data.append({
            'Date': date,
            'Gross Income': round(gross_income, 2),
            'Tax': round(tax, 2),
            'Superannuation': round(superannuation, 2),
            'Net Income': round(net_income, 2),
            'Bonus': round(bonus, 2),
            'Overtime': round(overtime, 2)
        })
    
    return pd.DataFrame(data)

# ==================== INVESTMENTS ====================
def create_investments_sheet(user_name, user_config):
    """Create investment tracker data for a user"""
    start_date = datetime(2022, 1, 1)
    num_months = 36
    dates = generate_dates(start_date, num_months)
    
    # Different asset types
    assets = ['Australian Shares', 'International Shares', 'Property Fund', 'Bonds', 'Cash']
    
    data = []
    initial_investment = user_config['initial_investment']
    monthly_contribution = user_config['monthly_contribution']
    
    current_values = {asset: initial_investment / len(assets) for asset in assets}
    
    for i, date in enumerate(dates):
        for asset in assets:
            # Simulate market growth with volatility
            if asset == 'Australian Shares':
                growth_rate = random.uniform(-0.03, 0.05)
            elif asset == 'International Shares':
                growth_rate = random.uniform(-0.04, 0.06)
            elif asset == 'Property Fund':
                growth_rate = random.uniform(-0.01, 0.03)
            elif asset == 'Bonds':
                growth_rate = random.uniform(-0.005, 0.015)
            else:  # Cash
                growth_rate = 0.002
            
            # Add monthly contribution
            contribution = monthly_contribution / len(assets)
            current_values[asset] = current_values[asset] * (1 + growth_rate) + contribution
            
            data.append({
                'Date': date,
                'Asset Type': asset,
                'Value': round(current_values[asset], 2),
                'Monthly Contribution': round(contribution, 2),
                'Growth Rate': round(growth_rate * 100, 2)
            })
    
    return pd.DataFrame(data)

# ==================== MAIN ====================
def main():
    """Create all Excel files"""
    
    print("Creating Excel files for My Finance Hub...")
    print("=" * 60)
    
    # User configurations
    users_config = {
        'Vincent': {
            'base_salary': 120000,
            'bonus_range': (10000, 20000),
            'initial_investment': 50000,
            'monthly_contribution': 2000,
            'property_value': 800000,
            'savings': 50000,
            'investments': 100000,
            'super': 150000,
            'vehicle': 30000,
            'mortgage': 600000,
            'car_loan': 25000,
            'credit_card_base': 5000
        },
        'Amy': {
            'base_salary': 95000,
            'bonus_range': (5000, 12000),
            'initial_investment': 35000,
            'monthly_contribution': 1500,
            'property_value': 800000,  # Joint property
            'savings': 35000,
            'investments': 70000,
            'super': 120000,
            'vehicle': 25000,
            'mortgage': 600000,  # Joint mortgage
            'car_loan': 20000,
            'credit_card_base': 4000
        },
        'Test': {
            'base_salary': 75000,
            'bonus_range': (3000, 8000),
            'initial_investment': 20000,
            'monthly_contribution': 1000,
            'property_value': 550000,
            'savings': 20000,
            'investments': 45000,
            'super': 80000,
            'vehicle': 18000,
            'mortgage': 400000,
            'car_loan': 15000,
            'credit_card_base': 3000
        }
    }
    
    # Create assets_liabilities.xlsx
    print("\n1. Creating assets_liabilities.xlsx...")
    with pd.ExcelWriter('data/assets_liabilities.xlsx', engine='openpyxl') as writer:
        for user_name, config in users_config.items():
            df = create_assets_liabilities_sheet(user_name, config)
            df.to_excel(writer, sheet_name=user_name, index=False)
    print("   ✓ Created with sheets: Vincent, Amy, Test")
    
    # Create employment.xlsx
    print("\n2. Creating employment.xlsx...")
    with pd.ExcelWriter('data/employment.xlsx', engine='openpyxl') as writer:
        for user_name, config in users_config.items():
            df = create_employment_sheet(user_name, config)
            df.to_excel(writer, sheet_name=user_name, index=False)
    print("   ✓ Created with sheets: Vincent, Amy, Test")
    
    # Create investments.xlsx
    print("\n3. Creating investments.xlsx...")
    with pd.ExcelWriter('data/investments.xlsx', engine='openpyxl') as writer:
        for user_name, config in users_config.items():
            df = create_investments_sheet(user_name, config)
            df.to_excel(writer, sheet_name=user_name, index=False)
    print("   ✓ Created with sheets: Vincent, Amy, Test")
    
    print("\n" + "=" * 60)
    print("✓ All Excel files created successfully!")
    print("\nFiles created in data/ directory:")
    print("  - assets_liabilities.xlsx (Date, Category, Type, Name, Value)")
    print("  - employment.xlsx (Date, Gross Income, Tax, Superannuation, Net Income, Bonus, Overtime)")
    print("  - investments.xlsx (Date, Asset Type, Value, Monthly Contribution, Growth Rate)")
    print("\nYou can now run: streamlit run app.py")

if __name__ == "__main__":
    main()

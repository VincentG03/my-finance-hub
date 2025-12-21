"""
Data Generation Script for My Finance Hub
This script creates dummy Excel files with realistic financial data for three users: Vincent, Amy, and Test.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_dates(start_date, num_months):
    """Generate a list of dates spanning num_months from start_date"""
    dates = []
    current = start_date
    for _ in range(num_months):
        dates.append(current)
        # Move to next month
        if current.month == 12:
            current = current.replace(year=current.year + 1, month=1)
        else:
            current = current.replace(month=current.month + 1)
    return dates

def create_salary_data(user_name, base_salary, bonus_range):
    """Generate salary tracker data"""
    start_date = datetime(2022, 1, 1)
    num_months = 36  # 3 years of data
    
    dates = generate_dates(start_date, num_months)
    
    data = []
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

def create_investment_data(user_name, initial_investment, monthly_contribution):
    """Generate investment tracker data"""
    start_date = datetime(2022, 1, 1)
    num_months = 36
    
    dates = generate_dates(start_date, num_months)
    
    # Different asset types
    assets = ['Australian Shares', 'International Shares', 'Property Fund', 'Bonds', 'Cash']
    
    data = []
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

def create_mortgage_data(user_name, loan_amount, interest_rate):
    """Generate mortgage debt tracker data"""
    start_date = datetime(2022, 1, 1)
    num_months = 36
    
    dates = generate_dates(start_date, num_months)
    
    # Calculate monthly payment (30-year loan)
    monthly_rate = interest_rate / 12
    num_payments = 30 * 12
    monthly_payment = loan_amount * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
    
    data = []
    remaining_balance = loan_amount
    
    for date in dates:
        interest_payment = remaining_balance * monthly_rate
        principal_payment = monthly_payment - interest_payment
        remaining_balance -= principal_payment
        
        data.append({
            'Date': date,
            'Remaining Balance': round(remaining_balance, 2),
            'Monthly Payment': round(monthly_payment, 2),
            'Principal Payment': round(principal_payment, 2),
            'Interest Payment': round(interest_payment, 2),
            'Interest Rate': round(interest_rate * 100, 2)
        })
    
    return pd.DataFrame(data)

def create_assets_liabilities_data(user_name):
    """Generate assets and liabilities tracker data"""
    start_date = datetime(2022, 1, 1)
    num_months = 36
    
    dates = generate_dates(start_date, num_months)
    
    data = []
    
    # Assets that grow over time
    property_value = 800000
    savings_account = 50000
    investment_portfolio = 100000
    superannuation = 150000
    vehicle_value = 30000
    
    # Liabilities
    mortgage = 600000
    car_loan = 25000
    credit_card = 5000
    
    for i, date in enumerate(dates):
        # Simulate growth/depreciation
        property_value *= 1.004  # ~5% annual growth
        savings_account += random.uniform(500, 2000)
        investment_portfolio *= random.uniform(0.995, 1.015)
        superannuation *= 1.006  # ~7% annual growth
        vehicle_value *= 0.997  # Depreciation
        
        # Pay down debts
        mortgage -= random.uniform(1500, 2500)
        car_loan = max(0, car_loan - 400)
        credit_card = random.uniform(2000, 8000)
        
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
            'Value': round(savings_account, 2)
        })
        data.append({
            'Date': date,
            'Category': 'Asset',
            'Type': 'Investment',
            'Name': 'Portfolio',
            'Value': round(investment_portfolio, 2)
        })
        data.append({
            'Date': date,
            'Category': 'Asset',
            'Type': 'Retirement',
            'Name': 'Superannuation',
            'Value': round(superannuation, 2)
        })
        data.append({
            'Date': date,
            'Category': 'Asset',
            'Type': 'Vehicle',
            'Name': 'Car',
            'Value': round(vehicle_value, 2)
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

def create_excel_file(filename, users_data):
    """Create an Excel file with multiple sheets (one per user)"""
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        for user_name, df in users_data.items():
            df.to_excel(writer, sheet_name=user_name, index=False)
    
    print(f"Created {filename}")

def main():
    """Generate all Excel files with dummy data"""
    
    print("Generating dummy data for My Finance Hub...")
    print("=" * 60)
    
    # User configurations
    users = {
        'Vincent': {
            'base_salary': 120000,
            'bonus_range': (10000, 20000),
            'initial_investment': 50000,
            'monthly_contribution': 2000,
            'loan_amount': 600000,
            'interest_rate': 0.045
        },
        'Amy': {
            'base_salary': 95000,
            'bonus_range': (5000, 12000),
            'initial_investment': 35000,
            'monthly_contribution': 1500,
            'loan_amount': 600000,  # Joint mortgage
            'interest_rate': 0.045
        },
        'Test': {
            'base_salary': 75000,
            'bonus_range': (3000, 8000),
            'initial_investment': 20000,
            'monthly_contribution': 1000,
            'loan_amount': 400000,
            'interest_rate': 0.050
        }
    }
    
    # Generate Salary Tracker
    print("\n1. Generating Salary_Tracker.xlsx...")
    salary_data = {}
    for user_name, config in users.items():
        salary_data[user_name] = create_salary_data(
            user_name, 
            config['base_salary'], 
            config['bonus_range']
        )
    create_excel_file('data/Salary_Tracker.xlsx', salary_data)
    
    # Generate Investment Tracker
    print("2. Generating Investment_Tracker.xlsx...")
    investment_data = {}
    for user_name, config in users.items():
        investment_data[user_name] = create_investment_data(
            user_name,
            config['initial_investment'],
            config['monthly_contribution']
        )
    create_excel_file('data/Investment_Tracker.xlsx', investment_data)
    
    # Generate Mortgage Tracker
    print("3. Generating Mortgage_Tracker.xlsx...")
    mortgage_data = {}
    for user_name, config in users.items():
        mortgage_data[user_name] = create_mortgage_data(
            user_name,
            config['loan_amount'],
            config['interest_rate']
        )
    create_excel_file('data/Mortgage_Tracker.xlsx', mortgage_data)
    
    # Generate Assets and Liabilities Tracker
    print("4. Generating Assets_Liabilities.xlsx...")
    assets_liabilities_data = {}
    for user_name in users.keys():
        assets_liabilities_data[user_name] = create_assets_liabilities_data(user_name)
    create_excel_file('data/Assets_Liabilities.xlsx', assets_liabilities_data)
    
    print("\n" + "=" * 60)
    print("✓ All dummy data files generated successfully!")
    print("\nFiles created:")
    print("  - data/Salary_Tracker.xlsx")
    print("  - data/Investment_Tracker.xlsx")
    print("  - data/Mortgage_Tracker.xlsx")
    print("  - data/Assets_Liabilities.xlsx")
    print("\nYou can now run the Streamlit app with: streamlit run app.py")

if __name__ == "__main__":
    import os
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    main()

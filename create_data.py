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

# ==================== MORTGAGE ====================
def create_mortgage_sheet(user_name, user_config):
    """Create mortgage tracking data for a user"""
    start_date = datetime(2022, 1, 1)
    num_months = 36
    dates = generate_dates(start_date, num_months)
    
    data = []
    
    # Mortgage details
    initial_balance = user_config['mortgage']
    interest_rate = user_config.get('mortgage_rate', 0.045)  # 4.5% annual
    monthly_rate = interest_rate / 12
    
    current_balance = initial_balance
    
    for date in dates:
        # Calculate interest for the month
        interest_payment = current_balance * monthly_rate
        
        # Fixed monthly payment (approximate using standard formula)
        monthly_payment = user_config.get('monthly_payment', 3000)
        principal_payment = monthly_payment - interest_payment
        
        # Update balance
        current_balance -= principal_payment
        current_balance = max(0, current_balance)  # Don't go negative
        
        data.append({
            'Date': date,
            'Balance': round(current_balance, 2),
            'Principal Payment': round(principal_payment, 2),
            'Interest Payment': round(interest_payment, 2),
            'Total Payment': round(monthly_payment, 2)
        })
    
    return pd.DataFrame(data)

# ==================== EMPLOYMENT ====================
def create_employment_sheet(user_name, user_config):
    """Create employment history data for a user (job history, not monthly salary)"""
    
    data = []
    
    # Sample job history for each user
    if user_name == 'Vincent':
        data = [
            {
                'Date Started': '2020-03-01',
                'Date Ended': '2022-12-31',
                'Company': 'Tech Corp Australia',
                'Job Position': 'Senior Software Engineer',
                'Job Type': 'Full-Time',
                'Wage (inc Super)': 110000,
                'Equivalent Salary': 110000,
                'Bonus': 15000,
                'Stock': 5000,
                'Other Remuneration': 2000,
                'Comments': 'Great company culture'
            },
            {
                'Date Started': '2023-01-15',
                'Date Ended': '',
                'Company': 'Innovation Labs',
                'Job Position': 'Lead Developer',
                'Job Type': 'Full-Time',
                'Wage (inc Super)': 133200,
                'Equivalent Salary': 120000,
                'Bonus': 20000,
                'Stock': 10000,
                'Other Remuneration': 3000,
                'Comments': 'Current role - excellent benefits'
            }
        ]
    elif user_name == 'Amy':
        data = [
            {
                'Date Started': '2019-07-01',
                'Date Ended': '2023-06-30',
                'Company': 'Marketing Solutions Pty Ltd',
                'Job Position': 'Marketing Manager',
                'Job Type': 'Full-Time',
                'Wage (inc Super)': 88800,
                'Equivalent Salary': 80000,
                'Bonus': 8000,
                'Stock': 0,
                'Other Remuneration': 1500,
                'Comments': 'Good work-life balance'
            },
            {
                'Date Started': '2023-07-01',
                'Date Ended': '',
                'Company': 'Digital Growth Agency',
                'Job Position': 'Senior Marketing Manager',
                'Job Type': 'Full-Time',
                'Wage (inc Super)': 105450,
                'Equivalent Salary': 95000,
                'Bonus': 12000,
                'Stock': 5000,
                'Other Remuneration': 2000,
                'Comments': 'Current role - great team'
            }
        ]
    else:  # Test
        data = [
            {
                'Date Started': '2021-02-01',
                'Date Ended': '',
                'Company': 'Service Industries Ltd',
                'Job Position': 'Account Manager',
                'Job Type': 'Full-Time',
                'Wage (inc Super)': 83250,
                'Equivalent Salary': 75000,
                'Bonus': 5000,
                'Stock': 0,
                'Other Remuneration': 1000,
                'Comments': 'Current role - stable income'
            }
        ]
    
    return pd.DataFrame(data)

# ==================== INVESTMENTS ====================
def create_investments_sheet(user_name, user_config):
    """Create simple investment holdings list for a user"""
    
    data = []
    
    # Sample investment holdings for each user
    if user_name == 'Vincent':
        data = [
            {'Asset Type': 'Australian Shares', 'Ticker': 'VAS', 'Value': 45000},
            {'Asset Type': 'International Shares', 'Ticker': 'VGS', 'Value': 38000},
            {'Asset Type': 'Property Fund', 'Ticker': 'VAP', 'Value': 25000},
            {'Asset Type': 'Bonds', 'Ticker': 'VGB', 'Value': 20000},
            {'Asset Type': 'Cash', 'Ticker': 'N/A', 'Value': 15000},
        ]
    elif user_name == 'Amy':
        data = [
            {'Asset Type': 'Australian Shares', 'Ticker': 'VAS', 'Value': 32000},
            {'Asset Type': 'International Shares', 'Ticker': 'VGS', 'Value': 28000},
            {'Asset Type': 'Property Fund', 'Ticker': 'VAP', 'Value': 18000},
            {'Asset Type': 'Bonds', 'Ticker': 'VGB', 'Value': 15000},
            {'Asset Type': 'Cash', 'Ticker': 'N/A', 'Value': 10000},
        ]
    else:  # Test
        data = [
            {'Asset Type': 'Australian Shares', 'Ticker': 'VAS', 'Value': 22000},
            {'Asset Type': 'International Shares', 'Ticker': 'VGS', 'Value': 18000},
            {'Asset Type': 'Property Fund', 'Ticker': 'VAP', 'Value': 12000},
            {'Asset Type': 'Bonds', 'Ticker': 'VGB', 'Value': 8000},
            {'Asset Type': 'Cash', 'Ticker': 'N/A', 'Value': 5000},
        ]
    
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
            'mortgage_rate': 0.045,
            'monthly_payment': 3500,
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
            'mortgage_rate': 0.045,
            'monthly_payment': 3500,
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
            'mortgage_rate': 0.050,
            'monthly_payment': 2500,
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
    
    # Create mortgage.xlsx
    print("\n4. Creating mortgage.xlsx...")
    with pd.ExcelWriter('data/mortgage.xlsx', engine='openpyxl') as writer:
        for user_name, config in users_config.items():
            df = create_mortgage_sheet(user_name, config)
            df.to_excel(writer, sheet_name=user_name, index=False)
    print("   ✓ Created with sheets: Vincent, Amy, Test")
    
    print("\n" + "=" * 60)
    print("✓ All Excel files created successfully!")
    print("\nFiles created in data/ directory:")
    print("  - assets_liabilities.xlsx (Date, Category, Type, Name, Value)")
    print("  - employment.xlsx (Date Started, Date Ended, Company, Job Position, etc.)")
    print("  - investments.xlsx (Asset Type, Ticker, Value)")
    print("  - mortgage.xlsx (Date, Balance, Principal Payment, Interest Payment, Total Payment)")
    print("\nYou can now run: streamlit run app.py")

if __name__ == "__main__":
    main()

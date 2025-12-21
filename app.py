"""
My Finance Hub - Premium Personal Finance Dashboard
A sophisticated financial tracking application built with Streamlit
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Page configuration
st.set_page_config(
    page_title="My Finance Hub",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': None
    }
)

# Custom CSS for premium styling
def load_custom_css():
    st.markdown("""
        <style>
        /* Import professional font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Global styles */
        * {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        /* Force black text on all streamlit elements */
        .stMarkdown, .stText, p, span, div, label, h1, h2, h3, h4, h5, h6 {
            color: #000000 !important;
        }
        
        /* Streamlit specific text elements */
        [data-testid="stMarkdownContainer"] p {
            color: #000000 !important;
        }
        
        /* Main background */
        .stApp {
            background-color: #FFFFFF;
        }
        
        /* Hide default Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* Premium container styling - invisible, just for spacing */
        .premium-container {
            background-color: transparent;
            border: none;
            border-radius: 0;
            padding: 0;
            margin: 8px 0;
            box-shadow: none;
        }
        
        /* Hide empty streamlit containers */
        .element-container:empty {
            display: none;
        }
        
        [data-testid="stVerticalBlock"] > div:empty {
            display: none;
        }
        
        /* Title styling */
        .main-title {
            font-size: 48px;
            font-weight: 700;
            color: #000000;
            text-align: center;
            margin-top: 100px;
            margin-bottom: 40px;
            letter-spacing: -0.5px;
        }
        
        .section-title {
            font-size: 24px;
            font-weight: 600;
            color: #000000;
            margin-bottom: 16px;
            border-bottom: 2px solid #4A9EFF;
            padding-bottom: 8px;
        }
        
        /* Metric card styling */
        .metric-card {
            background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFB 100%);
            border: 1px solid #E5E5E5;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
            transition: transform 0.2s;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        }
        
        .metric-value {
            font-size: 32px;
            font-weight: 700;
            color: #000000;
            margin: 8px 0;
        }
        
        .metric-label {
            font-size: 14px;
            font-weight: 500;
            color: #666666;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        
        .metric-change {
            font-size: 14px;
            font-weight: 500;
            margin-top: 4px;
        }
        
        .positive {
            color: #4A9EFF;
        }
        
        .negative {
            color: #FF6B6B;
        }
        
        /* Button styling */
        .stButton > button {
            background-color: #4A9EFF;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 32px;
            font-weight: 600;
            font-size: 16px;
            transition: all 0.3s;
        }
        
        .stButton > button:hover {
            background-color: #3A8EEF;
            box-shadow: 0 4px 12px rgba(74, 158, 255, 0.3);
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #F8FAFB;
            border-right: 1px solid #E5E5E5;
        }
        
        [data-testid="stSidebar"] .css-1d391kg {
            padding-top: 2rem;
        }
        
        /* TARGET THE EXACT COLLAPSE BUTTON - Force it to be always visible and BLACK */
        [data-testid="stSidebarCollapseButton"],
        [data-testid="stSidebarCollapseButton"] button,
        [data-testid="stSidebarCollapseButton"] span,
        [data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"] {
            display: inline-flex !important;
            opacity: 1 !important;
            visibility: visible !important;
            color: #000000 !important;
        }
        
        /* Force the button itself to be always visible */
        button[kind="headerNoPadding"][data-testid="stBaseButton-headerNoPadding"],
        button[kind="headerNoPadding"] {
            opacity: 1 !important;
            visibility: visible !important;
        }
        
        /* Override the light gray color on the icon spans */
        [data-testid="stSidebarCollapseButton"] span[color],
        [data-testid="stIconMaterial"] {
            color: rgb(0, 0, 0) !important;
            opacity: 1 !important;
        }
        
        /* Header background - keep it dark/black */
        [data-testid="stHeader"] {
            background-color: rgba(14, 17, 23, 1);
        }
        
        /* When sidebar is CLOSED - chevron should be WHITE (on black header) */
        [data-testid="collapsedControl"],
        [data-testid="collapsedControl"] *,
        [data-testid="collapsedControl"] svg,
        [data-testid="collapsedControl"] svg * {
            color: #FFFFFF !important;
            fill: #FFFFFF !important;
            stroke: #FFFFFF !important;
        }
        
        /* When sidebar is OPEN - chevron should be BLACK (on light sidebar) */
        [data-testid="stSidebar"] button[kind="header"],
        [data-testid="stSidebar"] button[kind="header"] *,
        [data-testid="stSidebar"] button[kind="header"] svg,
        [data-testid="stSidebar"] button[kind="header"] svg *,
        [data-testid="stSidebar"] [data-testid="baseButton-header"],
        [data-testid="stSidebar"] [data-testid="baseButton-header"] *,
        [data-testid="stSidebar"] [data-testid="baseButton-header"] svg,
        [data-testid="stSidebar"] [data-testid="baseButton-header"] svg * {
            color: #000000 !important;
            fill: #000000 !important;
            stroke: #000000 !important;
            opacity: 1 !important;
            visibility: visible !important;
        }
        
        /* Force chevron button in sidebar to always be visible */
        [data-testid="stSidebar"] button[kind="header"],
        [data-testid="stSidebar"] [data-testid="baseButton-header"] {
            display: block !important;
            opacity: 1 !important;
            visibility: visible !important;
        }
        
        /* Other header buttons should be white */
        [data-testid="stHeader"] button,
        [data-testid="stHeader"] button *,
        header button,
        header button * {
            color: #FFFFFF !important;
            fill: #FFFFFF !important;
            stroke: #FFFFFF !important;
            background-color: transparent !important;
        }
        
        /* Select box styling */
        .stSelectbox > div > div {
            background-color: #FFFFFF;
            border: 2px solid #E5E5E5;
            border-radius: 8px;
        }
        
        /* Dropdown menu styling */
        [data-baseweb="popover"] {
            background-color: #FFFFFF !important;
        }
        
        [data-baseweb="menu"] {
            background-color: #FFFFFF !important;
        }
        
        [role="option"] {
            background-color: #FFFFFF !important;
            color: #000000 !important;
        }
        
        [role="option"]:hover {
            background-color: #F0F0F0 !important;
            color: #000000 !important;
        }
        
        /* Select box text */
        .stSelectbox [data-baseweb="select"] > div {
            color: #000000 !important;
        }
        
        /* Tab styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        
        .stTabs [data-baseweb="tab"] {
            background-color: #F8FAFB;
            border-radius: 8px 8px 0 0;
            padding: 12px 24px;
            font-weight: 500;
            color: #666666;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: #FFFFFF;
            color: #000000;
            border-bottom: 2px solid #4A9EFF;
        }
        
        /* Chart container */
        .chart-container {
            background-color: #FFFFFF;
            border-radius: 12px;
            padding: 16px;
            margin: 16px 0;
        }
        
        </style>
    """, unsafe_allow_html=True)

# Data loading functions
@st.cache_data
def load_salary_data(user):
    """Load employment data for selected user"""
    try:
        df = pd.read_excel('data/employment.xlsx', sheet_name=user)
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except Exception as e:
        st.error(f"Error loading employment data: {e}")
        return pd.DataFrame()

@st.cache_data
def load_investment_data(user):
    """Load investment tracker data for selected user"""
    try:
        df = pd.read_excel('data/investments.xlsx', sheet_name=user)
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except Exception as e:
        st.error(f"Error loading investment data: {e}")
        return pd.DataFrame()

@st.cache_data
def load_mortgage_data(user):
    """Load mortgage tracker data for selected user (calculated from assets/liabilities)"""
    try:
        df = load_assets_liabilities_data(user)
        if df.empty:
            return pd.DataFrame()
        
        # Filter for mortgage liability
        mortgage_df = df[(df['Category'] == 'Liability') & (df['Type'] == 'Mortgage')].copy()
        
        if mortgage_df.empty:
            return pd.DataFrame()
        
        # Calculate mortgage metrics
        mortgage_df = mortgage_df.rename(columns={'Value': 'Remaining Balance'})
        mortgage_df['Monthly Payment'] = 3200.00  # Approximate monthly payment
        mortgage_df['Interest Rate'] = 4.5  # Approximate interest rate
        
        # Calculate principal and interest portions
        mortgage_df['Interest Payment'] = (mortgage_df['Remaining Balance'] * (mortgage_df['Interest Rate'] / 100)) / 12
        mortgage_df['Principal Payment'] = mortgage_df['Monthly Payment'] - mortgage_df['Interest Payment']
        
        # Select relevant columns
        mortgage_df = mortgage_df[['Date', 'Remaining Balance', 'Monthly Payment', 'Principal Payment', 'Interest Payment', 'Interest Rate']]
        
        return mortgage_df.sort_values('Date')
    except Exception as e:
        st.error(f"Error loading mortgage data: {e}")
        return pd.DataFrame()

@st.cache_data
def load_assets_liabilities_data(user):
    """Load assets and liabilities data for selected user"""
    try:
        df = pd.read_excel('data/assets_liabilities.xlsx', sheet_name=user)
        df['Date'] = pd.to_datetime(df['Date'])
        return df
    except Exception as e:
        st.error(f"Error loading assets/liabilities data: {e}")
        return pd.DataFrame()

# Utility functions
def format_currency(value):
    """Format number as currency"""
    return f"${value:,.2f}"

def calculate_percentage_change(current, previous):
    """Calculate percentage change"""
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100

# Initialize session state
if 'user_selected' not in st.session_state:
    st.session_state.user_selected = False
if 'current_user' not in st.session_state:
    st.session_state.current_user = None

def main():
    """Main application logic"""
    load_custom_css()
    
    # Landing page - User selection
    if not st.session_state.user_selected:
        show_landing_page()
    else:
        # Main dashboard
        show_dashboard()

def show_landing_page():
    """Display the landing page with user selection"""
    st.markdown('<h1 class="main-title">My Finance Hub</h1>', unsafe_allow_html=True)
    
    # Center the dropdown
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        user = st.selectbox(
            "Select User",
            options=["Vincent", "Amy", "Test"],
            key="user_selector"
        )
        
        if user:
            if st.button("Continue to Dashboard", use_container_width=True):
                st.session_state.current_user = user
                st.session_state.user_selected = True
                st.rerun()

def show_dashboard():
    """Display the main dashboard with all trackers"""
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown(f"### Welcome, {st.session_state.current_user}!")
        st.markdown("---")
        
        page = st.radio(
            "Navigation",
            ["Summary Overview", 
             "Investment Tracker", 
             "Mortgage Debt Tracker", 
             "Assets & Liabilities", 
             "Salary Tracker",
             "Retirement Calculator"],
            key="navigation"
        )
        
        st.markdown("---")
        
        if st.button("Change User", use_container_width=True):
            st.session_state.user_selected = False
            st.session_state.current_user = None
            st.rerun()
    
    # Display selected page
    if page == "Summary Overview":
        show_summary_overview()
    elif page == "Investment Tracker":
        show_investment_tracker()
    elif page == "Mortgage Debt Tracker":
        show_mortgage_tracker()
    elif page == "Assets & Liabilities":
        show_assets_liabilities()
    elif page == "Salary Tracker":
        show_salary_tracker()
    elif page == "Retirement Calculator":
        show_retirement_calculator()

def show_summary_overview():
    """Display summary overview page"""
    st.markdown('<h2 class="section-title">Summary Overview</h2>', unsafe_allow_html=True)
    
    user = st.session_state.current_user
    
    # Load all data
    salary_df = load_salary_data(user)
    investment_df = load_investment_data(user)
    mortgage_df = load_mortgage_data(user)
    assets_liabilities_df = load_assets_liabilities_data(user)
    
    # Calculate key metrics
    if not salary_df.empty:
        latest_salary = salary_df.iloc[-1]
        prev_salary = salary_df.iloc[-2] if len(salary_df) > 1 else latest_salary
        
        total_income_ytd = salary_df[salary_df['Date'].dt.year == datetime.now().year]['Net Income'].sum()
        avg_monthly_income = salary_df['Net Income'].tail(12).mean()
    
    if not investment_df.empty:
        latest_investments = investment_df[investment_df['Date'] == investment_df['Date'].max()]
        total_investment_value = latest_investments['Value'].sum()
        
        prev_month_investments = investment_df[investment_df['Date'] == investment_df['Date'].unique()[-2]]
        prev_investment_value = prev_month_investments['Value'].sum()
        investment_change = calculate_percentage_change(total_investment_value, prev_investment_value)
    
    if not mortgage_df.empty:
        current_mortgage = mortgage_df.iloc[-1]['Remaining Balance']
        initial_mortgage = mortgage_df.iloc[0]['Remaining Balance']
    
    if not assets_liabilities_df.empty:
        latest_date = assets_liabilities_df['Date'].max()
        latest_data = assets_liabilities_df[assets_liabilities_df['Date'] == latest_date]
        
        total_assets = latest_data[latest_data['Category'] == 'Asset']['Value'].sum()
        total_liabilities = latest_data[latest_data['Category'] == 'Liability']['Value'].sum()
        net_worth = total_assets - total_liabilities
        
        # Previous month for comparison
        prev_date = assets_liabilities_df['Date'].unique()[-2]
        prev_data = assets_liabilities_df[assets_liabilities_df['Date'] == prev_date]
        prev_net_worth = prev_data[prev_data['Category'] == 'Asset']['Value'].sum() - prev_data[prev_data['Category'] == 'Liability']['Value'].sum()
        net_worth_change = calculate_percentage_change(net_worth, prev_net_worth)
    
    # Display key metrics in cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Net Worth</div>
                <div class="metric-value">{format_currency(net_worth)}</div>
                <div class="metric-change {'positive' if net_worth_change > 0 else 'negative'}">
                    {'↑' if net_worth_change > 0 else '↓'} {abs(net_worth_change):.2f}% vs last month
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Assets</div>
                <div class="metric-value">{format_currency(total_assets)}</div>
                <div class="metric-change metric-label">Current Value</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Investment Portfolio</div>
                <div class="metric-value">{format_currency(total_investment_value)}</div>
                <div class="metric-change {'positive' if investment_change > 0 else 'negative'}">
                    {'↑' if investment_change > 0 else '↓'} {abs(investment_change):.2f}% vs last month
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Avg Monthly Income</div>
                <div class="metric-value">{format_currency(avg_monthly_income)}</div>
                <div class="metric-change metric-label">Last 12 months</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Net Worth Trend Chart
    st.markdown("### Net Worth Trend")
    
    # Calculate net worth over time
    net_worth_data = []
    for date in assets_liabilities_df['Date'].unique():
        date_data = assets_liabilities_df[assets_liabilities_df['Date'] == date]
        assets = date_data[date_data['Category'] == 'Asset']['Value'].sum()
        liabilities = date_data[date_data['Category'] == 'Liability']['Value'].sum()
        net_worth_data.append({
            'Date': date,
            'Assets': assets,
            'Liabilities': liabilities,
            'Net Worth': assets - liabilities
        })
    
    net_worth_df = pd.DataFrame(net_worth_data)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=net_worth_df['Date'],
        y=net_worth_df['Net Worth'],
        mode='lines',
        name='Net Worth',
        line=dict(color='#4A9EFF', width=3),
        fill='tozeroy',
        fillcolor='rgba(74, 158, 255, 0.1)',
        textfont=dict(color='#000000')
    ))
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Inter', color='#000000', size=12),
        xaxis=dict(
            showgrid=True,
            gridcolor='#F0F0F0',
            title=dict(text='Date', font=dict(color='#000000', size=14)),
            tickfont=dict(color='#000000', size=12),
            color='#000000'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#F0F0F0',
            title=dict(text='Net Worth ($)', font=dict(color='#000000', size=14)),
            tickfont=dict(color='#000000', size=12),
            color='#000000'
        ),
        hovermode='x unified',
        height=400,
        hoverlabel=dict(font=dict(color='#FFFFFF', size=12))
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Asset Allocation
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Asset Allocation")
        
        asset_breakdown = latest_data[latest_data['Category'] == 'Asset'].groupby('Type')['Value'].sum().reset_index()
        
        fig = go.Figure(data=[go.Pie(
            labels=asset_breakdown['Type'],
            values=asset_breakdown['Value'],
            hole=0.4,
            marker=dict(colors=['#4A9EFF', '#3A8EEF', '#2A7EDF', '#1A6ECF', '#0A5EBF']),
            textfont=dict(color='#000000', size=14),
            textposition='inside'
        )])
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter', color='#000000'),
            showlegend=True,
            legend=dict(
                font=dict(color='#000000', size=12),
                bgcolor='white'
            ),
            height=350
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Monthly Income vs Expenses")
        
        # Get recent months
        recent_salary = salary_df.tail(6)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=recent_salary['Date'],
            y=recent_salary['Net Income'],
            name='Net Income',
            marker_color='#4A9EFF',
            textfont=dict(color='#000000')
        ))
        
        fig.add_trace(go.Bar(
            x=recent_salary['Date'],
            y=recent_salary['Tax'],
            name='Tax',
            marker_color='#000000',
            textfont=dict(color='#FFFFFF')
        ))
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter', color='#000000', size=12),
            xaxis=dict(
                showgrid=False,
                tickfont=dict(color='#000000', size=12),
                color='#000000'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#F0F0F0',
                title=dict(text='Amount ($)', font=dict(color='#000000', size=14)),
                tickfont=dict(color='#000000', size=12),
                color='#000000'
            ),
            barmode='group',
            height=350,
            legend=dict(font=dict(color='#000000', size=12)),
            hoverlabel=dict(font=dict(color='#FFFFFF', size=12))
        )
        
        st.plotly_chart(fig, use_container_width=True)

def show_investment_tracker():
    """Display investment tracker page"""
    st.markdown('<h2 class="section-title">Investment Tracker</h2>', unsafe_allow_html=True)
    
    user = st.session_state.current_user
    investment_df = load_investment_data(user)
    
    if investment_df.empty:
        st.warning("No investment data available.")
        return
    
    # Latest values
    latest_date = investment_df['Date'].max()
    latest_investments = investment_df[investment_df['Date'] == latest_date]
    total_value = latest_investments['Value'].sum()
    
    # Calculate returns
    first_date = investment_df['Date'].min()
    initial_investments = investment_df[investment_df['Date'] == first_date]
    initial_value = initial_investments['Value'].sum()
    total_return = ((total_value - initial_value) / initial_value) * 100
    
    # Display summary metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Portfolio Value</div>
                <div class="metric-value">{format_currency(total_value)}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Return</div>
                <div class="metric-value {'positive' if total_return > 0 else 'negative'}">
                    {total_return:.2f}%
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        monthly_contribution = latest_investments['Monthly Contribution'].sum()
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Monthly Contribution</div>
                <div class="metric-value">{format_currency(monthly_contribution)}</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Portfolio value over time
    st.markdown("### Portfolio Value Over Time")
    
    portfolio_timeline = investment_df.groupby('Date')['Value'].sum().reset_index()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=portfolio_timeline['Date'],
        y=portfolio_timeline['Value'],
        mode='lines',
        name='Total Value',
        line=dict(color='#4A9EFF', width=3),
        fill='tozeroy',
        fillcolor='rgba(74, 158, 255, 0.1)',
        textfont=dict(color='#000000')
    ))
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Inter', color='#000000', size=12),
        xaxis=dict(
            showgrid=True,
            gridcolor='#F0F0F0',
            title=dict(text='Date', font=dict(color='#000000', size=14)),
            tickfont=dict(color='#000000', size=12),
            color='#000000'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#F0F0F0',
            title=dict(text='Value ($)', font=dict(color='#000000', size=14)),
            tickfont=dict(color='#000000', size=12),
            color='#000000'
        ),
        hovermode='x unified',
        height=400,
        hoverlabel=dict(font=dict(color='#FFFFFF', size=12))
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Asset breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Current Asset Allocation")
        
        fig = go.Figure(data=[go.Pie(
            labels=latest_investments['Asset Type'],
            values=latest_investments['Value'],
            hole=0.4,
            marker=dict(colors=['#4A9EFF', '#3A8EEF', '#2A7EDF', '#1A6ECF', '#0A5EBF']),
            textfont=dict(color='#000000', size=14),
            textposition='inside'
        )])
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter', color='#000000'),
            legend=dict(
                font=dict(color='#000000', size=12),
                bgcolor='white'
            ),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Asset Performance")
        
        # Get latest value for each asset type
        asset_performance = []
        for asset_type in investment_df['Asset Type'].unique():
            asset_data = investment_df[investment_df['Asset Type'] == asset_type]
            initial = asset_data.iloc[0]['Value']
            current = asset_data.iloc[-1]['Value']
            performance = ((current - initial) / initial) * 100
            asset_performance.append({
                'Asset': asset_type,
                'Performance': performance
            })
        
        perf_df = pd.DataFrame(asset_performance)
        
        fig = go.Figure(go.Bar(
            x=perf_df['Asset'],
            y=perf_df['Performance'],
            marker_color=['#4A9EFF' if x > 0 else '#000000' for x in perf_df['Performance']],
            textfont=dict(color='#000000')
        ))
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter', color='#000000', size=12),
            xaxis=dict(
                showgrid=False,
                title=dict(text='Asset Type', font=dict(color='#000000', size=14)),
                tickfont=dict(color='#000000', size=12),
                color='#000000'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#F0F0F0',
                title=dict(text='Return (%)', font=dict(color='#000000', size=14)),
                tickfont=dict(color='#000000', size=12),
                color='#000000'
            ),
            height=400,
            hoverlabel=dict(font=dict(color='#FFFFFF', size=12))
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def show_mortgage_tracker():
    """Display mortgage debt tracker page"""
    st.markdown('<h2 class="section-title">Mortgage Debt Tracker</h2>', unsafe_allow_html=True)
    
    user = st.session_state.current_user
    mortgage_df = load_mortgage_data(user)
    
    if mortgage_df.empty:
        st.warning("No mortgage data available.")
        return
    
    # Current mortgage details
    current = mortgage_df.iloc[-1]
    initial = mortgage_df.iloc[0]
    
    total_paid = initial['Remaining Balance'] - current['Remaining Balance']
    total_interest_paid = mortgage_df['Interest Payment'].sum()
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Remaining Balance</div>
                <div class="metric-value">{format_currency(current['Remaining Balance'])}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Monthly Payment</div>
                <div class="metric-value">{format_currency(current['Monthly Payment'])}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Principal Paid</div>
                <div class="metric-value">{format_currency(total_paid)}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Interest Paid</div>
                <div class="metric-value">{format_currency(total_interest_paid)}</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Remaining balance over time
    st.markdown('<div class="premium-container">', unsafe_allow_html=True)
    st.markdown("### Remaining Balance Over Time")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=mortgage_df['Date'],
        y=mortgage_df['Remaining Balance'],
        mode='lines',
        name='Remaining Balance',
        line=dict(color='#4A9EFF', width=3),
        fill='tozeroy',
        fillcolor='rgba(74, 158, 255, 0.1)',
        textfont=dict(color='#000000')
    ))
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Inter', color='#000000', size=12),
        xaxis=dict(
            showgrid=True,
            gridcolor='#F0F0F0',
            title=dict(text='Date', font=dict(color='#000000', size=14)),
            tickfont=dict(color='#000000', size=12),
            color='#000000'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#F0F0F0',
            title=dict(text='Balance ($)', font=dict(color='#000000', size=14)),
            tickfont=dict(color='#000000', size=12),
            color='#000000'
        ),
        hovermode='x unified',
        height=400,
        hoverlabel=dict(font=dict(color='#FFFFFF', size=12))
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Principal vs Interest
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="premium-container">', unsafe_allow_html=True)
        st.markdown("### Monthly Payment Breakdown")
        
        recent_payments = mortgage_df.tail(12)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=recent_payments['Date'],
            y=recent_payments['Principal Payment'],
            name='Principal',
            marker_color='#4A9EFF',
            textfont=dict(color='#000000')
        ))
        
        fig.add_trace(go.Bar(
            x=recent_payments['Date'],
            y=recent_payments['Interest Payment'],
            name='Interest',
            marker_color='#000000',
            textfont=dict(color='#FFFFFF')
        ))
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter', color='#000000', size=12),
            xaxis=dict(
                showgrid=False,
                title=dict(text='Date', font=dict(color='#000000', size=14)),
                tickfont=dict(color='#000000', size=12),
                color='#000000'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#F0F0F0',
                title=dict(text='Payment ($)', font=dict(color='#000000', size=14)),
                tickfont=dict(color='#000000', size=12),
                color='#000000'
            ),
            barmode='stack',
            height=400,
            legend=dict(font=dict(color='#000000', size=12)),
            hoverlabel=dict(font=dict(color='#FFFFFF', size=12))
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="premium-container">', unsafe_allow_html=True)
        st.markdown("### Cumulative Interest Paid")
        
        mortgage_df['Cumulative Interest'] = mortgage_df['Interest Payment'].cumsum()
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=mortgage_df['Date'],
            y=mortgage_df['Cumulative Interest'],
            mode='lines',
            name='Cumulative Interest',
            line=dict(color='#000000', width=3),
            fill='tozeroy',
            fillcolor='rgba(0, 0, 0, 0.1)',
            textfont=dict(color='#000000')
        ))
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter', color='#000000', size=12),
            xaxis=dict(
                showgrid=True,
                gridcolor='#F0F0F0',
                title=dict(text='Date', font=dict(color='#000000', size=14)),
                tickfont=dict(color='#000000', size=12),
                color='#000000'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#F0F0F0',
                title=dict(text='Cumulative Interest ($)', font=dict(color='#000000', size=14)),
                tickfont=dict(color='#000000', size=12),
                color='#000000'
            ),
            hovermode='x unified',
            height=400,
            hoverlabel=dict(font=dict(color='#FFFFFF', size=12))
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def show_assets_liabilities():
    """Display assets and liabilities tracker page"""
    st.markdown('<h2 class="section-title">Assets & Liabilities Tracker</h2>', unsafe_allow_html=True)
    
    user = st.session_state.current_user
    df = load_assets_liabilities_data(user)
    
    if df.empty:
        st.warning("No assets/liabilities data available.")
        return
    
    # Calculate current totals
    latest_date = df['Date'].max()
    latest_data = df[df['Date'] == latest_date]
    
    total_assets = latest_data[latest_data['Category'] == 'Asset']['Value'].sum()
    total_liabilities = latest_data[latest_data['Category'] == 'Liability']['Value'].sum()
    net_worth = total_assets - total_liabilities
    
    # Display key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Assets</div>
                <div class="metric-value positive">{format_currency(total_assets)}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Liabilities</div>
                <div class="metric-value negative">{format_currency(total_liabilities)}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Net Worth</div>
                <div class="metric-value">{format_currency(net_worth)}</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Net worth trend
    st.markdown('<div class="premium-container">', unsafe_allow_html=True)
    st.markdown("### Net Worth Trend")
    
    # Calculate net worth for each date
    net_worth_data = []
    for date in df['Date'].unique():
        date_data = df[df['Date'] == date]
        assets = date_data[date_data['Category'] == 'Asset']['Value'].sum()
        liabilities = date_data[date_data['Category'] == 'Liability']['Value'].sum()
        net_worth_data.append({
            'Date': date,
            'Assets': assets,
            'Liabilities': liabilities,
            'Net Worth': assets - liabilities
        })
    
    net_worth_df = pd.DataFrame(net_worth_data)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=net_worth_df['Date'],
        y=net_worth_df['Assets'],
        mode='lines',
        name='Assets',
        line=dict(color='#4A9EFF', width=2),
        stackgroup='one',
        textfont=dict(color='#000000')
    ))
    
    fig.add_trace(go.Scatter(
        x=net_worth_df['Date'],
        y=net_worth_df['Liabilities'],
        mode='lines',
        name='Liabilities',
        line=dict(color='#000000', width=2),
        stackgroup='two',
        textfont=dict(color='#000000')
    ))
    
    fig.add_trace(go.Scatter(
        x=net_worth_df['Date'],
        y=net_worth_df['Net Worth'],
        mode='lines',
        name='Net Worth',
        line=dict(color='#2A7EDF', width=3, dash='dash'),
        textfont=dict(color='#000000')
    ))
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Inter', color='#000000', size=12),
        xaxis=dict(
            showgrid=True,
            gridcolor='#F0F0F0',
            title=dict(text='Date', font=dict(color='#000000', size=14)),
            tickfont=dict(color='#000000', size=12),
            color='#000000'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#F0F0F0',
            title=dict(text='Value ($)', font=dict(color='#000000', size=14)),
            tickfont=dict(color='#000000', size=12),
            color='#000000'
        ),
        hovermode='x unified',
        height=400,
        legend=dict(font=dict(color='#000000', size=12)),
        hoverlabel=dict(font=dict(color='#FFFFFF', size=12))
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Asset and liability breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="premium-container">', unsafe_allow_html=True)
        st.markdown("### Asset Breakdown")
        
        assets_breakdown = latest_data[latest_data['Category'] == 'Asset'].groupby('Type')['Value'].sum().reset_index()
        
        fig = go.Figure(data=[go.Pie(
            labels=assets_breakdown['Type'],
            values=assets_breakdown['Value'],
            hole=0.4,
            marker=dict(colors=['#4A9EFF', '#3A8EEF', '#2A7EDF', '#1A6ECF', '#0A5EBF']),
            textfont=dict(color='#000000', size=14),
            textposition='inside'
        )])
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter', color='#000000'),
            legend=dict(
                font=dict(color='#000000', size=12),
                bgcolor='white'
            ),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="premium-container">', unsafe_allow_html=True)
        st.markdown("### Liability Breakdown")
        
        liabilities_breakdown = latest_data[latest_data['Category'] == 'Liability'].groupby('Type')['Value'].sum().reset_index()
        
        fig = go.Figure(data=[go.Pie(
            labels=liabilities_breakdown['Type'],
            values=liabilities_breakdown['Value'],
            hole=0.4,
            marker=dict(colors=['#000000', '#333333', '#666666', '#999999']),
            textfont=dict(color='#FFFFFF', size=14),
            textposition='inside'
        )])
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter', color='#000000'),
            legend=dict(
                font=dict(color='#000000', size=12),
                bgcolor='white'
            ),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Detailed tables
    st.markdown('<div class="premium-container">', unsafe_allow_html=True)
    st.markdown("### Detailed Breakdown")
    
    tab1, tab2 = st.tabs(["Assets", "Liabilities"])
    
    with tab1:
        assets_table = latest_data[latest_data['Category'] == 'Asset'][['Type', 'Name', 'Value']].sort_values('Value', ascending=False)
        st.dataframe(assets_table, use_container_width=True, hide_index=True)
    
    with tab2:
        liabilities_table = latest_data[latest_data['Category'] == 'Liability'][['Type', 'Name', 'Value']].sort_values('Value', ascending=False)
        st.dataframe(liabilities_table, use_container_width=True, hide_index=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def show_salary_tracker():
    """Display salary tracker page"""
    st.markdown('<h2 class="section-title">Salary Tracker</h2>', unsafe_allow_html=True)
    
    user = st.session_state.current_user
    salary_df = load_salary_data(user)
    
    if salary_df.empty:
        st.warning("No salary data available.")
        return
    
    # Calculate metrics
    ytd_data = salary_df[salary_df['Date'].dt.year == datetime.now().year]
    ytd_gross = ytd_data['Gross Income'].sum()
    ytd_net = ytd_data['Net Income'].sum()
    ytd_tax = ytd_data['Tax'].sum()
    avg_monthly = salary_df['Net Income'].tail(12).mean()
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">YTD Gross Income</div>
                <div class="metric-value">{format_currency(ytd_gross)}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">YTD Net Income</div>
                <div class="metric-value">{format_currency(ytd_net)}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">YTD Tax Paid</div>
                <div class="metric-value">{format_currency(ytd_tax)}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Avg Monthly Net</div>
                <div class="metric-value">{format_currency(avg_monthly)}</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Income over time
    st.markdown('<div class="premium-container">', unsafe_allow_html=True)
    st.markdown("### Income Over Time")
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=salary_df['Date'],
        y=salary_df['Gross Income'],
        mode='lines',
        name='Gross Income',
        line=dict(color='#4A9EFF', width=2),
        textfont=dict(color='#000000')
    ))
    
    fig.add_trace(go.Scatter(
        x=salary_df['Date'],
        y=salary_df['Net Income'],
        mode='lines',
        name='Net Income',
        line=dict(color='#2A7EDF', width=2),
        textfont=dict(color='#000000')
    ))
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Inter', color='#000000', size=12),
        xaxis=dict(
            showgrid=True,
            gridcolor='#F0F0F0',
            title=dict(text='Date', font=dict(color='#000000', size=14)),
            tickfont=dict(color='#000000', size=12),
            color='#000000'
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#F0F0F0',
            title=dict(text='Income ($)', font=dict(color='#000000', size=14)),
            tickfont=dict(color='#000000', size=12),
            color='#000000'
        ),
        hovermode='x unified',
        height=400,
        legend=dict(font=dict(color='#000000', size=12)),
        hoverlabel=dict(font=dict(color='#FFFFFF', size=12))
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Income breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="premium-container">', unsafe_allow_html=True)
        st.markdown("### Monthly Income Breakdown (Last 12 Months)")
        
        recent_data = salary_df.tail(12)
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=recent_data['Date'],
            y=recent_data['Net Income'],
            name='Net Income',
            marker_color='#4A9EFF',
            textfont=dict(color='#000000')
        ))
        
        fig.add_trace(go.Bar(
            x=recent_data['Date'],
            y=recent_data['Tax'],
            name='Tax',
            marker_color='#000000',
            textfont=dict(color='#FFFFFF')
        ))
        
        fig.add_trace(go.Bar(
            x=recent_data['Date'],
            y=recent_data['Superannuation'],
            name='Super',
            marker_color='#2A7EDF',
            textfont=dict(color='#000000')
        ))
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter', color='#000000', size=12),
            xaxis=dict(
                showgrid=False,
                title=dict(text='Date', font=dict(color='#000000', size=14)),
                tickfont=dict(color='#000000', size=12),
                color='#000000'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#F0F0F0',
                title=dict(text='Amount ($)', font=dict(color='#000000', size=14)),
                tickfont=dict(color='#000000', size=12),
                color='#000000'
            ),
            barmode='stack',
            height=400,
            legend=dict(font=dict(color='#000000', size=12)),
            hoverlabel=dict(font=dict(color='#FFFFFF', size=12))
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="premium-container">', unsafe_allow_html=True)
        st.markdown("### Tax Rate Analysis")
        
        salary_df['Effective Tax Rate'] = (salary_df['Tax'] / salary_df['Gross Income']) * 100
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=salary_df['Date'],
            y=salary_df['Effective Tax Rate'],
            mode='lines+markers',
            name='Effective Tax Rate',
            line=dict(color='#000000', width=2),
            marker=dict(size=6, color='#000000'),
            textfont=dict(color='#000000')
        ))
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter', color='#000000', size=12),
            xaxis=dict(
                showgrid=True,
                gridcolor='#F0F0F0',
                title=dict(text='Date', font=dict(color='#000000', size=14)),
                tickfont=dict(color='#000000', size=12),
                color='#000000'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#F0F0F0',
                title=dict(text='Tax Rate (%)', font=dict(color='#000000', size=14)),
                tickfont=dict(color='#000000', size=12),
                color='#000000',
                range=[0, 50]
            ),
            hovermode='x unified',
            height=400,
            hoverlabel=dict(font=dict(color='#FFFFFF', size=12))
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

def show_retirement_calculator():
    """Display retirement calculator page"""
    st.markdown('<h2 class="section-title">Retirement Calculator</h2>', unsafe_allow_html=True)
    
    user = st.session_state.current_user
    
    # Load current financial data
    salary_df = load_salary_data(user)
    investment_df = load_investment_data(user)
    
    st.markdown('<div class="premium-container">', unsafe_allow_html=True)
    st.markdown("### Retirement Planning Inputs")
    
    col1, col2 = st.columns(2)
    
    with col1:
        current_age = st.number_input("Current Age", min_value=18, max_value=100, value=35)
        retirement_age = st.number_input("Retirement Age", min_value=current_age, max_value=100, value=65)
        current_savings = st.number_input("Current Retirement Savings ($)", min_value=0, value=150000, step=10000)
        monthly_contribution = st.number_input("Monthly Contribution ($)", min_value=0, value=2000, step=100)
    
    with col2:
        expected_return = st.slider("Expected Annual Return (%)", min_value=0.0, max_value=15.0, value=7.0, step=0.5)
        inflation_rate = st.slider("Expected Inflation Rate (%)", min_value=0.0, max_value=10.0, value=2.5, step=0.5)
        retirement_income = st.number_input("Desired Annual Retirement Income ($)", min_value=0, value=60000, step=5000)
        life_expectancy = st.number_input("Life Expectancy", min_value=retirement_age, max_value=120, value=90)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Calculate retirement projections
    if st.button("Calculate Retirement Plan", use_container_width=True):
        years_to_retirement = retirement_age - current_age
        years_in_retirement = life_expectancy - retirement_age
        
        # Project retirement savings
        monthly_return = (expected_return / 100) / 12
        months_to_retirement = years_to_retirement * 12
        
        # Future value of current savings
        fv_current = current_savings * ((1 + monthly_return) ** months_to_retirement)
        
        # Future value of monthly contributions
        if monthly_return > 0:
            fv_contributions = monthly_contribution * (((1 + monthly_return) ** months_to_retirement - 1) / monthly_return)
        else:
            fv_contributions = monthly_contribution * months_to_retirement
        
        total_at_retirement = fv_current + fv_contributions
        
        # Calculate required savings for retirement
        real_return = ((1 + expected_return/100) / (1 + inflation_rate/100)) - 1
        if real_return > 0:
            required_savings = retirement_income * ((1 - (1 + real_return) ** -years_in_retirement) / real_return)
        else:
            required_savings = retirement_income * years_in_retirement
        
        # Display results
        st.markdown('<div class="premium-container">', unsafe_allow_html=True)
        st.markdown("### Retirement Projection Results")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Projected at Retirement</div>
                    <div class="metric-value">{format_currency(total_at_retirement)}</div>
                    <div class="metric-change metric-label">Age {retirement_age}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Required for Goal</div>
                    <div class="metric-value">{format_currency(required_savings)}</div>
                    <div class="metric-change metric-label">{format_currency(retirement_income)}/year</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            surplus_deficit = total_at_retirement - required_savings
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">{'Surplus' if surplus_deficit > 0 else 'Shortfall'}</div>
                    <div class="metric-value {'positive' if surplus_deficit > 0 else 'negative'}">
                        {format_currency(abs(surplus_deficit))}
                    </div>
                    <div class="metric-change metric-label">
                        {'On track!' if surplus_deficit > 0 else 'Need to save more'}
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Projection chart
        st.markdown('<div class="premium-container">', unsafe_allow_html=True)
        st.markdown("### Savings Growth Projection")
        
        # Create projection data
        projection_data = []
        balance = current_savings
        
        for year in range(years_to_retirement + 1):
            age = current_age + year
            projection_data.append({
                'Age': age,
                'Year': year,
                'Balance': balance
            })
            
            # Add monthly contributions and growth for next year
            if year < years_to_retirement:
                for _ in range(12):
                    balance = balance * (1 + monthly_return) + monthly_contribution
        
        projection_df = pd.DataFrame(projection_data)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=projection_df['Age'],
            y=projection_df['Balance'],
            mode='lines',
            name='Projected Savings',
            line=dict(color='#4A9EFF', width=3),
            fill='tozeroy',
            fillcolor='rgba(74, 158, 255, 0.1)',
            textfont=dict(color='#000000')
        ))
        
        # Add target line
        fig.add_hline(
            y=required_savings,
            line_dash="dash",
            line_color="#000000",
            annotation_text="Required Amount",
            annotation_position="right",
            annotation_font=dict(color='#000000', size=12)
        )
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter', color='#000000', size=12),
            xaxis=dict(
                showgrid=True,
                gridcolor='#F0F0F0',
                title=dict(text='Age', font=dict(color='#000000', size=14)),
                tickfont=dict(color='#000000', size=12),
                color='#000000'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#F0F0F0',
                title=dict(text='Savings ($)', font=dict(color='#000000', size=14)),
                tickfont=dict(color='#000000', size=12),
                color='#000000'
            ),
            hovermode='x unified',
            height=400,
            hoverlabel=dict(font=dict(color='#FFFFFF', size=12))
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Recommendations
        if surplus_deficit < 0:
            st.markdown('<div class="premium-container">', unsafe_allow_html=True)
            st.markdown("### 💡 Recommendations")
            
            # Calculate required monthly contribution
            if monthly_return > 0:
                required_monthly = (required_savings - fv_current) * (monthly_return / ((1 + monthly_return) ** months_to_retirement - 1))
            else:
                required_monthly = (required_savings - fv_current) / months_to_retirement
            
            additional_needed = required_monthly - monthly_contribution
            
            st.markdown(f"""
            - **Increase monthly contribution** to {format_currency(required_monthly)} (additional {format_currency(additional_needed)}/month)
            - **Delay retirement** by {int(abs(surplus_deficit) / (monthly_contribution * 12))} years
            - **Reduce retirement income goal** to {format_currency(retirement_income * (total_at_retirement / required_savings))}/year
            - **Seek higher returns** (even 1% more can make a significant difference)
            """)
            
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

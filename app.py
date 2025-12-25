"""
My Finance Hub - Personal Finance Dashboard
Real data-driven financial tracking application built with Streamlit
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
from data_parser import load_financial_data

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
        
        /* Premium container styling */
        .premium-container {
            background-color: transparent;
            border: none;
            padding: 0;
            margin: 8px 0;
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
            color: #10B981;
        }
        
        .negative {
            color: #EF4444;
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
        
        /* Header customization */
        [data-testid="stHeader"] {
            background-color: rgba(14, 17, 23, 1);
        }
        
        /* When sidebar is CLOSED - chevron should be WHITE */
        [data-testid="collapsedControl"],
        [data-testid="collapsedControl"] * {
            color: #FFFFFF !important;
            fill: #FFFFFF !important;
        }
        
        /* When sidebar is OPEN - chevron should be BLACK */
        [data-testid="stSidebar"] button[kind="header"] *,
        [data-testid="stSidebar"] [data-testid="baseButton-header"] * {
            color: #000000 !important;
            fill: #000000 !important;
        }
        
        </style>
    """, unsafe_allow_html=True)

# Data loading functions
@st.cache_data
def load_data():
    """Load all financial data using the parser"""
    parser = load_financial_data('data/vincent_financial_data.xlsx')
    return parser

# Utility functions
def format_currency(value):
    """Format number as currency"""
    return f"${value:,.2f}"

def calculate_percentage_change(current, previous):
    """Calculate percentage change"""
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100

def main():
    """Main application logic"""
    load_custom_css()
    
    # Initialize data parser
    try:
        parser = load_data()
    except Exception as e:
        st.error(f"Error loading financial data: {e}")
        return
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("### My Finance Hub")
        st.markdown("---")
        
        page = st.radio(
            "Navigation",
            ["📊 Dashboard", 
             "💰 Net Worth",
             "💼 Investments",
             "👔 Employment History",
             "📈 Growth Analysis"],
            key="navigation"
        )
        
        st.markdown("---")
        st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d')}*")
    
    # Display selected page
    if page == "📊 Dashboard":
        show_dashboard(parser)
    elif page == "💰 Net Worth":
        show_net_worth(parser)
    elif page == "💼 Investments":
        show_investments(parser)
    elif page == "👔 Employment History":
        show_employment(parser)
    elif page == "📈 Growth Analysis":
        show_growth_analysis(parser)

def show_dashboard(parser):
    """Display main dashboard"""
    st.markdown('<h2 class="section-title">Financial Dashboard</h2>', unsafe_allow_html=True)
    
    # Get latest metrics
    latest_date, net_worth, total_assets, total_liabilities = parser.get_latest_net_worth()
    
    # Get assets & liabilities data for trend
    al_df = parser.parse_assets_liabilities()
    
    # Calculate previous month for comparison
    dates = sorted(al_df['Date'].unique())
    if len(dates) >= 2:
        prev_date = dates[-2]
        prev_data = al_df[al_df['Date'] == prev_date]
        prev_assets = prev_data[prev_data['Category'] == 'Asset']['Value'].sum()
        prev_liabilities = prev_data[prev_data['Category'] == 'Liability']['Value'].sum()
        prev_net_worth = prev_assets - prev_liabilities
        
        nw_change = calculate_percentage_change(net_worth, prev_net_worth)
        assets_change = calculate_percentage_change(total_assets, prev_assets)
    else:
        nw_change = 0
        assets_change = 0
    
    # Key metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Net Worth</div>
                <div class="metric-value">{format_currency(net_worth)}</div>
                <div class="metric-change {'positive' if nw_change > 0 else 'negative'}">
                    {'↑' if nw_change > 0 else '↓'} {abs(nw_change):.1f}% vs last period
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Assets</div>
                <div class="metric-value positive">{format_currency(total_assets)}</div>
                <div class="metric-change {'positive' if assets_change > 0 else 'negative'}">
                    {'↑' if assets_change > 0 else '↓'} {abs(assets_change):.1f}% vs last period
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Liabilities</div>
                <div class="metric-value negative">{format_currency(total_liabilities)}</div>
                <div class="metric-change metric-label">As of {latest_date.strftime('%Y-%m-%d')}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Net Worth Trend
    st.markdown("### Net Worth Trend")
    
    # Calculate net worth over time
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
    
    nw_df = pd.DataFrame(net_worth_data)
    
    fig = go.Figure()
    
    # Net worth line
    fig.add_trace(go.Scatter(
        x=nw_df['Date'],
        y=nw_df['Net Worth'],
        mode='lines+markers',
        name='Net Worth',
        line=dict(color='#4A9EFF', width=3),
        marker=dict(size=8, color='#4A9EFF'),
        fill='tozeroy',
        fillcolor='rgba(74, 158, 255, 0.1)'
    ))
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Inter', color='#000000'),
        xaxis=dict(
            showgrid=True,
            gridcolor='#E5E5E5',
            title='Date',
            title_font=dict(size=14, color='#000000')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#E5E5E5',
            title='Net Worth ($)',
            title_font=dict(size=14, color='#000000')
        ),
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Asset breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Asset Breakdown")
        latest_data = al_df[al_df['Date'] == latest_date]
        asset_breakdown = latest_data[latest_data['Category'] == 'Asset'].groupby('Type')['Value'].sum().reset_index()
        asset_breakdown = asset_breakdown.sort_values('Value', ascending=False)
        
        fig = go.Figure(data=[go.Pie(
            labels=asset_breakdown['Type'],
            values=asset_breakdown['Value'],
            hole=0.5,
            marker=dict(colors=px.colors.sequential.Blues_r),
            textposition='auto',
            textfont=dict(size=13, color='#000000')
        )])
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter', color='#000000'),
            showlegend=True,
            height=400,
            legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.05)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Assets vs Liabilities Over Time")
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=nw_df['Date'],
            y=nw_df['Assets'],
            name='Assets',
            marker_color='#10B981'
        ))
        
        fig.add_trace(go.Bar(
            x=nw_df['Date'],
            y=nw_df['Liabilities'],
            name='Liabilities',
            marker_color='#EF4444'
        ))
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter', color='#000000'),
            xaxis=dict(
                showgrid=False,
                title='Date',
                title_font=dict(size=14, color='#000000')
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#E5E5E5',
                title='Amount ($)',
                title_font=dict(size=14, color='#000000')
            ),
            barmode='group',
            height=400,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)

def show_net_worth(parser):
    """Display detailed net worth page"""
    st.markdown('<h2 class="section-title">Net Worth Analysis</h2>', unsafe_allow_html=True)
    
    al_df = parser.parse_assets_liabilities()
    
    # Calculate net worth over time
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
    
    nw_df = pd.DataFrame(net_worth_data)
    
    # Calculate growth metrics
    initial_nw = nw_df.iloc[0]['Net Worth']
    current_nw = nw_df.iloc[-1]['Net Worth']
    total_growth = current_nw - initial_nw
    total_growth_pct = ((current_nw - initial_nw) / abs(initial_nw)) * 100 if initial_nw != 0 else 0
    
    # Time period
    time_period_days = (nw_df.iloc[-1]['Date'] - nw_df.iloc[0]['Date']).days
    time_period_months = time_period_days / 30.44
    
    # Monthly average growth
    avg_monthly_growth = total_growth / time_period_months if time_period_months > 0 else 0
    
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Current Net Worth</div>
                <div class="metric-value">{format_currency(current_nw)}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Growth</div>
                <div class="metric-value {'positive' if total_growth > 0 else 'negative'}">
                    {format_currency(total_growth)}
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Growth Rate</div>
                <div class="metric-value {'positive' if total_growth_pct > 0 else 'negative'}">
                    {total_growth_pct:.1f}%
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Avg Monthly Growth</div>
                <div class="metric-value {'positive' if avg_monthly_growth > 0 else 'negative'}">
                    {format_currency(avg_monthly_growth)}
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Detailed net worth chart with trend line
    st.markdown("### Net Worth Progression")
    
    fig = go.Figure()
    
    # Actual net worth
    fig.add_trace(go.Scatter(
        x=nw_df['Date'],
        y=nw_df['Net Worth'],
        mode='lines+markers',
        name='Net Worth',
        line=dict(color='#4A9EFF', width=3),
        marker=dict(size=10, color='#4A9EFF'),
        fill='tozeroy',
        fillcolor='rgba(74, 158, 255, 0.15)'
    ))
    
    # Add trend line
    from sklearn.linear_model import LinearRegression
    X = np.array(range(len(nw_df))).reshape(-1, 1)
    y = nw_df['Net Worth'].values
    model = LinearRegression()
    model.fit(X, y)
    trend = model.predict(X)
    
    fig.add_trace(go.Scatter(
        x=nw_df['Date'],
        y=trend,
        mode='lines',
        name='Trend',
        line=dict(color='#EF4444', width=2, dash='dash')
    ))
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Inter', color='#000000'),
        xaxis=dict(
            showgrid=True,
            gridcolor='#E5E5E5',
            title='Date',
            title_font=dict(size=14, color='#000000')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#E5E5E5',
            title='Net Worth ($)',
            title_font=dict(size=14, color='#000000')
        ),
        hovermode='x unified',
        height=500,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Monthly change analysis
    st.markdown("### Month-over-Month Changes")
    
    nw_df['Month-over-Month Change'] = nw_df['Net Worth'].diff()
    nw_df['MoM Change %'] = nw_df['Net Worth'].pct_change() * 100
    
    fig = go.Figure()
    
    colors = ['#10B981' if x > 0 else '#EF4444' for x in nw_df['Month-over-Month Change'].fillna(0)]
    
    fig.add_trace(go.Bar(
        x=nw_df['Date'],
        y=nw_df['Month-over-Month Change'],
        marker_color=colors,
        name='MoM Change',
        text=nw_df['MoM Change %'].fillna(0).round(1).astype(str) + '%',
        textposition='outside'
    ))
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Inter', color='#000000'),
        xaxis=dict(
            showgrid=False,
            title='Date',
            title_font=dict(size=14, color='#000000')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#E5E5E5',
            title='Change ($)',
            title_font=dict(size=14, color='#000000')
        ),
        height=400,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed table
    st.markdown("### Detailed Breakdown by Period")
    
    latest_date = al_df['Date'].max()
    latest_data = al_df[al_df['Date'] == latest_date]
    
    tab1, tab2 = st.tabs(["Assets", "Liabilities"])
    
    with tab1:
        assets = latest_data[latest_data['Category'] == 'Asset'][['Type', 'Value']].sort_values('Value', ascending=False)
        assets['% of Total'] = (assets['Value'] / assets['Value'].sum() * 100).round(2)
        assets['Value'] = assets['Value'].apply(format_currency)
        st.dataframe(assets, use_container_width=True, hide_index=True)
    
    with tab2:
        liabilities = latest_data[latest_data['Category'] == 'Liability'][['Type', 'Value']].sort_values('Value', ascending=False)
        if not liabilities.empty:
            liabilities['% of Total'] = (liabilities['Value'] / liabilities['Value'].sum() * 100).round(2)
            liabilities['Value'] = liabilities['Value'].apply(format_currency)
            st.dataframe(liabilities, use_container_width=True, hide_index=True)
        else:
            st.info("No liabilities recorded")

def show_investments(parser):
    """Display investment tracker page"""
    st.markdown('<h2 class="section-title">Investment Portfolio</h2>', unsafe_allow_html=True)
    
    inv_df = parser.parse_investments()
    
    if inv_df.empty:
        st.warning("No investment data available.")
        return
    
    # Calculate current holdings
    inv_summary = parser.get_investment_summary()
    
    if not inv_summary.empty:
        total_invested = inv_summary['Total Invested'].sum()
        total_units = inv_summary['Total Units'].sum()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Total Invested</div>
                    <div class="metric-value">{format_currency(total_invested)}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Unique Holdings</div>
                    <div class="metric-value">{len(inv_summary)}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-label">Total Transactions</div>
                    <div class="metric-value">{len(inv_df)}</div>
                </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Investment over time
    st.markdown("### Cumulative Investment Value")
    
    inv_df_sorted = inv_df.sort_values('Trade Date')
    inv_df_sorted['Cumulative Invested'] = inv_df_sorted['Total Value'].cumsum()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=inv_df_sorted['Trade Date'],
        y=inv_df_sorted['Cumulative Invested'],
        mode='lines+markers',
        name='Cumulative Invested',
        line=dict(color='#10B981', width=3),
        marker=dict(size=6),
        fill='tozeroy',
        fillcolor='rgba(16, 185, 129, 0.1)'
    ))
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Inter', color='#000000'),
        xaxis=dict(
            showgrid=True,
            gridcolor='#E5E5E5',
            title='Trade Date',
            title_font=dict(size=14, color='#000000')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#E5E5E5',
            title='Cumulative Amount ($)',
            title_font=dict(size=14, color='#000000')
        ),
        hovermode='x unified',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Holdings breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Portfolio Allocation by Investment")
        
        fig = go.Figure(data=[go.Pie(
            labels=inv_summary['Symbol'],
            values=inv_summary['Total Invested'],
            hole=0.5,
            marker=dict(colors=px.colors.sequential.Greens_r),
            textposition='auto',
            textfont=dict(size=13, color='#000000')
        )])
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter', color='#000000'),
            showlegend=True,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Investment Activity by Month")
        
        inv_df['Month'] = inv_df['Trade Date'].dt.to_period('M').dt.to_timestamp()
        monthly_inv = inv_df.groupby('Month')['Total Value'].sum().reset_index()
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=monthly_inv['Month'],
            y=monthly_inv['Total Value'],
            marker_color='#4A9EFF',
            name='Monthly Investment'
        ))
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter', color='#000000'),
            xaxis=dict(
                showgrid=False,
                title='Month',
                title_font=dict(size=14, color='#000000')
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#E5E5E5',
                title='Amount Invested ($)',
                title_font=dict(size=14, color='#000000')
            ),
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Transaction history
    st.markdown("### Recent Transactions")
    
    recent_inv = inv_df.sort_values('Trade Date', ascending=False).head(20)
    display_cols = ['Trade Date', 'Symbol', 'Side', 'Units', 'Avg. Price', 'Total Value']
    recent_inv_display = recent_inv[display_cols].copy()
    recent_inv_display['Trade Date'] = recent_inv_display['Trade Date'].dt.strftime('%Y-%m-%d')
    recent_inv_display['Total Value'] = recent_inv_display['Total Value'].apply(format_currency)
    recent_inv_display['Avg. Price'] = recent_inv_display['Avg. Price'].apply(lambda x: f"${x:.2f}")
    
    st.dataframe(recent_inv_display, use_container_width=True, hide_index=True)

def show_employment(parser):
    """Display employment history page"""
    st.markdown('<h2 class="section-title">Employment History</h2>', unsafe_allow_html=True)
    
    emp_df = parser.parse_employment()
    
    if emp_df.empty:
        st.warning("No employment data available.")
        return
    
    # Calculate total compensation
    total_comp = emp_df['Total Compensation'].sum()
    avg_comp = emp_df['Total Compensation'].mean()
    total_jobs = len(emp_df)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Compensation</div>
                <div class="metric-value">{format_currency(total_comp)}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Positions</div>
                <div class="metric-value">{total_jobs}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Average Compensation</div>
                <div class="metric-value">{format_currency(avg_comp)}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Timeline visualization
    st.markdown("### Employment Timeline")
    
    fig = go.Figure()
    
    for idx, row in emp_df.iterrows():
        fig.add_trace(go.Scatter(
            x=[row['Date Started'], row['Date Ended']],
            y=[idx, idx],
            mode='lines+markers',
            line=dict(color='#4A9EFF', width=20),
            marker=dict(size=12, color='#4A9EFF'),
            name=row['Company'],
            hovertemplate=f"<b>{row['Company']}</b><br>" +
                         f"Position: {row['Position']}<br>" +
                         f"Type: {row['Type']}<br>" +
                         f"Duration: {row['Duration (months)']:.1f} months<br>" +
                         f"Compensation: {format_currency(row['Total Compensation'])}<extra></extra>"
        ))
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Inter', color='#000000'),
        xaxis=dict(
            showgrid=True,
            gridcolor='#E5E5E5',
            title='Date',
            title_font=dict(size=14, color='#000000')
        ),
        yaxis=dict(
            showgrid=False,
            showticklabels=False,
            title=''
        ),
        height=max(400, len(emp_df) * 80),
        showlegend=True,
        legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.05)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Compensation breakdown
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Compensation by Company")
        
        fig = go.Figure(data=[go.Bar(
            x=emp_df['Company'],
            y=emp_df['Total Compensation'],
            marker_color='#10B981',
            text=emp_df['Total Compensation'].apply(format_currency),
            textposition='outside'
        )])
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter', color='#000000'),
            xaxis=dict(
                showgrid=False,
                title='Company',
                title_font=dict(size=14, color='#000000')
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#E5E5E5',
                title='Total Compensation ($)',
                title_font=dict(size=14, color='#000000')
            ),
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### Employment Type Distribution")
        
        type_dist = emp_df.groupby('Type')['Total Compensation'].sum().reset_index()
        
        fig = go.Figure(data=[go.Pie(
            labels=type_dist['Type'],
            values=type_dist['Total Compensation'],
            hole=0.5,
            marker=dict(colors=px.colors.sequential.Blues_r),
            textposition='auto',
            textfont=dict(size=13, color='#000000')
        )])
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter', color='#000000'),
            showlegend=True,
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed table
    st.markdown("### Employment Details")
    
    emp_display = emp_df.copy()
    emp_display['Date Started'] = emp_display['Date Started'].dt.strftime('%Y-%m-%d')
    emp_display['Date Ended'] = emp_display['Date Ended'].dt.strftime('%Y-%m-%d')
    emp_display['Duration (months)'] = emp_display['Duration (months)'].round(1)
    emp_display['Total Compensation'] = emp_display['Total Compensation'].apply(format_currency)
    
    display_cols = ['Date Started', 'Date Ended', 'Company', 'Position', 'Type', 'Duration (months)', 'Total Compensation']
    st.dataframe(emp_display[display_cols], use_container_width=True, hide_index=True)

def show_growth_analysis(parser):
    """Display growth analysis page"""
    st.markdown('<h2 class="section-title">Financial Growth Analysis</h2>', unsafe_allow_html=True)
    
    # Get all data
    al_df = parser.parse_assets_liabilities()
    inv_df = parser.parse_investments()
    emp_df = parser.parse_employment()
    
    # Calculate net worth progression
    net_worth_data = []
    for date in sorted(al_df['Date'].unique()):
        date_data = al_df[al_df['Date'] == date]
        assets = date_data[date_data['Category'] == 'Asset']['Value'].sum()
        liabilities = date_data[date_data['Category'] == 'Liability']['Value'].sum()
        net_worth_data.append({
            'Date': date,
            'Net Worth': assets - liabilities
        })
    
    nw_df = pd.DataFrame(net_worth_data)
    
    # Calculate annualized growth rate
    if len(nw_df) > 1:
        years = (nw_df.iloc[-1]['Date'] - nw_df.iloc[0]['Date']).days / 365.25
        cagr = (((nw_df.iloc[-1]['Net Worth'] / nw_df.iloc[0]['Net Worth']) ** (1 / years)) - 1) * 100 if years > 0 and nw_df.iloc[0]['Net Worth'] > 0 else 0
    else:
        cagr = 0
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">CAGR (Net Worth)</div>
                <div class="metric-value {'positive' if cagr > 0 else 'negative'}">
                    {cagr:.1f}%
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        total_invested = inv_df['Total Value'].sum()
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Invested</div>
                <div class="metric-value">{format_currency(total_invested)}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        total_earned = emp_df['Total Compensation'].sum()
        st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Total Earned</div>
                <div class="metric-value">{format_currency(total_earned)}</div>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Year-over-year comparison
    st.markdown("### Year-over-Year Net Worth Growth")
    
    nw_df['Year'] = nw_df['Date'].dt.year
    yearly_nw = nw_df.groupby('Year')['Net Worth'].last().reset_index()
    yearly_nw['YoY Growth'] = yearly_nw['Net Worth'].pct_change() * 100
    yearly_nw['YoY Change ($)'] = yearly_nw['Net Worth'].diff()
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=yearly_nw['Year'],
        y=yearly_nw['Net Worth'],
        name='Net Worth',
        marker_color='#4A9EFF',
        yaxis='y',
        text=yearly_nw['Net Worth'].apply(format_currency),
        textposition='outside'
    ))
    
    fig.add_trace(go.Scatter(
        x=yearly_nw['Year'],
        y=yearly_nw['YoY Growth'].fillna(0),
        name='YoY Growth %',
        line=dict(color='#10B981', width=3),
        marker=dict(size=10),
        yaxis='y2'
    ))
    
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font=dict(family='Inter', color='#000000'),
        xaxis=dict(
            showgrid=False,
            title='Year',
            title_font=dict(size=14, color='#000000')
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='#E5E5E5',
            title='Net Worth ($)',
            title_font=dict(size=14, color='#000000')
        ),
        yaxis2=dict(
            title='YoY Growth (%)',
            title_font=dict(size=14, color='#10B981'),
            overlaying='y',
            side='right',
            showgrid=False
        ),
        height=450,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Asset growth breakdown
    st.markdown("### Asset Category Growth")
    
    # Get unique asset types
    asset_types = al_df[al_df['Category'] == 'Asset']['Type'].unique()
    
    # Calculate growth for each asset type
    asset_growth = []
    for asset_type in asset_types:
        asset_data = al_df[(al_df['Category'] == 'Asset') & (al_df['Type'] == asset_type)]
        if not asset_data.empty:
            dates = sorted(asset_data['Date'].unique())
            if len(dates) >= 2:
                initial_val = asset_data[asset_data['Date'] == dates[0]]['Value'].sum()
                final_val = asset_data[asset_data['Date'] == dates[-1]]['Value'].sum()
                growth = final_val - initial_val
                growth_pct = ((final_val - initial_val) / initial_val * 100) if initial_val > 0 else 0
                
                asset_growth.append({
                    'Asset Type': asset_type,
                    'Initial Value': initial_val,
                    'Current Value': final_val,
                    'Growth ($)': growth,
                    'Growth (%)': growth_pct
                })
    
    if asset_growth:
        growth_df = pd.DataFrame(asset_growth).sort_values('Growth ($)', ascending=False)
        
        fig = go.Figure()
        
        colors = ['#10B981' if x > 0 else '#EF4444' for x in growth_df['Growth ($)']]
        
        fig.add_trace(go.Bar(
            x=growth_df['Asset Type'],
            y=growth_df['Growth ($)'],
            marker_color=colors,
            text=growth_df['Growth (%)'].round(1).astype(str) + '%',
            textposition='outside'
        ))
        
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font=dict(family='Inter', color='#000000'),
            xaxis=dict(
                showgrid=False,
                title='Asset Type',
                title_font=dict(size=14, color='#000000')
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#E5E5E5',
                title='Growth ($)',
                title_font=dict(size=14, color='#000000')
            ),
            height=400,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()

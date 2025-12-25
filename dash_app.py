"""
My Finance Hub - Dash Application
Professional FinTech dashboard using Plotly Dash and Dash Mantine Components
"""

import dash
from dash import dcc, html, Input, Output, callback, ALL
import dash_mantine_components as dmc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.linear_model import LinearRegression
import random

from data_loader import load_data

# Initialize data loader
data_loader = load_data()

# Load user info
user_info = data_loader.get_user_info()

# Rotating greeting messages (second part only)
ROTATING_MESSAGES = [
    "let's see how you're tracking. 🧐",
    "time for a wealth check? 💸",
    "let's look at the gains. 📈",
    "here is your latest snapshot. 📸",
    "ready to review the portfolio? 💼",
    "let's crunch the numbers. 🔢",
    "ready to see where you stand? 📍",
    "let's see if the line went up. 🚀",
    "time for a financial health check. 🩺",
    "let's take a look at the books. 📚"
]

# Initialize Dash app
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ]
)

app.title = "My Finance Hub"

# Add custom CSS for animations
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            @keyframes messagecycle {
                0% {
                    opacity: 0;
                    transform: translateY(-10px);
                }
                13% {
                    opacity: 1;
                    transform: translateY(0);
                }
                87% {
                    opacity: 1;
                    transform: translateY(0);
                }
                100% {
                    opacity: 0;
                    transform: translateY(10px);
                }
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Theme configuration
THEME = {
    'primaryColor': '#4A9EFF',
    'fontFamily': 'Inter, system-ui, -apple-system, sans-serif',
}

# Utility functions
def calculate_age_detailed(dob):
    """Calculate age in years, months, and days from date of birth"""
    today = datetime.now()
    
    # Calculate years
    years = today.year - dob.year
    
    # Calculate months
    months = today.month - dob.month
    if months < 0:
        years -= 1
        months += 12
    
    # Calculate days
    days = today.day - dob.day
    if days < 0:
        months -= 1
        if months < 0:
            years -= 1
            months += 12
        # Get days in previous month
        if today.month == 1:
            prev_month = 12
            prev_year = today.year - 1
        else:
            prev_month = today.month - 1
            prev_year = today.year
        
        from calendar import monthrange
        days_in_prev_month = monthrange(prev_year, prev_month)[1]
        days += days_in_prev_month
    
    return f"{years} years, {months} months, {days} days"

def format_currency(value):
    """Format number as currency"""
    return f"${value:,.2f}"

def calculate_percentage_change(current, previous):
    """Calculate percentage change"""
    if previous == 0:
        return 0
    return ((current - previous) / previous) * 100

def create_metric_card(label, value, change=None, color='blue'):
    """Create a metric card using DMC components"""
    return dmc.Paper(
        children=[
            dmc.Stack(
                children=[
                    dmc.Text(label, size="sm", fw=500, c="dimmed", tt="uppercase"),
                    dmc.Text(value, size="xl", fw=700, style={"fontSize": "32px"}),
                    dmc.Text(
                        change if change else "",
                        size="sm",
                        fw=500,
                        c="green" if change and '↑' in change else "red" if change and '↓' in change else "dimmed"
                    ) if change else html.Div()
                ],
                gap="xs"
            )
        ],
        p="lg",
        radius="md",
        withBorder=True,
        shadow="sm",
        style={"height": "100%"}
    )

def create_animated_greeting():
    """Create animated greeting component with rotating messages"""
    first_name = user_info['full_name'].split()[0]
    
    return html.Div([
        # Interval component to trigger message rotation every 3 seconds
        dcc.Interval(
            id='greeting-interval',
            interval=5400,  # 5.4 seconds total (0.7s fade in + 4s visible + 0.7s fade out)
            n_intervals=0
        ),
        # Greeting container
        html.Div([
            # First line: "Hey Vincent," (static)
            html.Div(
                f"Hey {first_name},",
                style={
                    "fontSize": "24px",
                    "fontWeight": "700",
                    "color": "#000000",  # Black
                    "marginBottom": "2px",
                    "lineHeight": "1.2"
                }
            ),
            # Second line: rotating message container with wrapper for animation
            html.Div(
                id="rotating-message-container",
                style={"minHeight": "40px", "overflow": "visible"}
            )
        ], style={"marginBottom": "10px"})
    ])

# Layout components
def create_navbar():
    """Create navigation sidebar"""
    nav_items = [
        {"icon": "📊", "label": "Dashboard", "value": "dashboard"},
        {"icon": "💰", "label": "Net Worth", "value": "net-worth"},
        {"icon": "💼", "label": "Investments", "value": "investments"},
        {"icon": "👔", "label": "Employment", "value": "employment"},
        {"icon": "📈", "label": "Growth Analysis", "value": "growth"},
    ]
    
    # Calculate user age
    age_text = calculate_age_detailed(user_info['dob'])
    
    nav_links = [
        create_animated_greeting(),
        dmc.Divider(),
    ] + [
        dmc.NavLink(
            label=html.Span(item["label"], style={"position": "relative", "top": "-3px"}),
            leftSection=item["icon"],
            id={"type": "nav-link", "index": item["value"]},
            active=False,
            variant="filled",
            style={
                "marginBottom": "5px", 
                "fontSize": "26px", 
                "paddingTop": "16px", 
                "paddingBottom": "16px",
                "display": "flex",
                "alignItems": "center"
            }
        ) for item in nav_items
    ] + [
        dmc.Divider(style={"marginTop": "auto"}),
        dmc.Stack([
            # User information
            dmc.Text(
                f"👤 {user_info['full_name']}",
                size="xs",
                fw=500,
                c="dimmed"
            ),
            dmc.Text(
                f"🎂 Age: {age_text}",
                size="xs",
                c="dimmed"
            ),
            dmc.Text(
                f"💱 Currency: {user_info['currency']}",
                size="xs",
                c="dimmed"
            ),
            dmc.Text(
                f"📅 Last updated: {datetime.now().strftime('%Y-%m-%d')}",
                size="xs",
                c="dimmed"
            ),
            dmc.Divider(my="xs"),
            # Disclaimer
            dmc.Group([
                dmc.Text("✓", c="green", size="sm", fw=700),
                dmc.Stack([
                    dmc.Text(
                        "Running locally",
                        size="xs",
                        fw=500,
                        c="dimmed"
                    ),
                    dmc.Text(
                        f"Data: {data_loader.excel_path.split('/')[-1]}",
                        size="xs",
                        c="dimmed",
                        style={"lineHeight": "1.2"}
                    ),
                ], gap=2)
            ], gap="xs", align="flex-start")
        ], gap="xs")
    ]
    
    return dmc.Stack(
        children=nav_links,
        gap="sm",
        style={"height": "100%"}
    )

# Page layouts
def dashboard_layout():
    """Dashboard page layout"""
    # Get data
    metrics = data_loader.get_latest_metrics()
    al_df = data_loader.load_assets_liabilities()
    
    # Calculate changes
    dates = sorted(al_df['Date'].unique())
    nw_change = 0
    assets_change = 0
    
    if len(dates) >= 2:
        prev_date = dates[-2]
        prev_data = al_df[al_df['Date'] == prev_date]
        prev_assets = prev_data[prev_data['Category'] == 'Asset']['Value'].sum()
        prev_liabilities = prev_data[prev_data['Category'] == 'Liability']['Value'].sum()
        prev_net_worth = prev_assets - prev_liabilities
        
        nw_change = calculate_percentage_change(metrics['net_worth'], prev_net_worth)
        assets_change = calculate_percentage_change(metrics['total_assets'], prev_assets)
    
    # Net worth timeseries
    nw_df = data_loader.get_net_worth_timeseries()
    
    fig_networth = go.Figure()
    fig_networth.add_trace(go.Scatter(
        x=nw_df['Date'],
        y=nw_df['Net Worth'],
        mode='lines+markers',
        name='Net Worth',
        line=dict(color='#4A9EFF', width=3),
        marker=dict(size=8),
        fill='tozeroy',
        fillcolor='rgba(74, 158, 255, 0.1)'
    ))
    
    fig_networth.update_layout(
        template='plotly_white',
        font=dict(family='Inter, sans-serif'),
        xaxis_title='Date',
        yaxis_title='Net Worth ($)',
        hovermode='x unified',
        height=400,
        margin=dict(l=0, r=0, t=20, b=0)
    )
    
    # Asset breakdown
    asset_breakdown = data_loader.get_asset_breakdown()
    
    fig_assets = go.Figure(data=[go.Pie(
        labels=asset_breakdown['Type'],
        values=asset_breakdown['Value'],
        hole=0.5,
        marker=dict(colors=px.colors.sequential.Blues_r),
        textposition='auto'
    )])
    
    fig_assets.update_layout(
        template='plotly_white',
        font=dict(family='Inter, sans-serif'),
        height=400,
        margin=dict(l=0, r=0, t=20, b=0),
        showlegend=True
    )
    
    # Assets vs Liabilities bar chart
    fig_comparison = go.Figure()
    fig_comparison.add_trace(go.Bar(
        x=nw_df['Date'],
        y=nw_df['Assets'],
        name='Assets',
        marker_color='#10B981'
    ))
    fig_comparison.add_trace(go.Bar(
        x=nw_df['Date'],
        y=nw_df['Liabilities'],
        name='Liabilities',
        marker_color='#EF4444'
    ))
    
    fig_comparison.update_layout(
        template='plotly_white',
        font=dict(family='Inter, sans-serif'),
        xaxis_title='Date',
        yaxis_title='Amount ($)',
        barmode='group',
        height=400,
        margin=dict(l=0, r=0, t=20, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    return dmc.Stack([
        dmc.Title("Financial Dashboard", order=2, mb="lg"),
        
        # Metrics row
        dmc.Grid([
            dmc.GridCol(create_metric_card(
                "Net Worth",
                format_currency(metrics['net_worth']),
                f"{'↑' if nw_change > 0 else '↓'} {abs(nw_change):.1f}% vs last period"
            ), span=4),
            dmc.GridCol(create_metric_card(
                "Total Assets",
                format_currency(metrics['total_assets']),
                f"{'↑' if assets_change > 0 else '↓'} {abs(assets_change):.1f}% vs last period"
            ), span=4),
            dmc.GridCol(create_metric_card(
                "Total Liabilities",
                format_currency(metrics['total_liabilities']),
                f"As of {metrics['date'].strftime('%Y-%m-%d')}" if metrics['date'] else ""
            ), span=4),
        ], gutter="lg"),
        
        dmc.Divider(my="xl"),
        
        # Net worth trend
        dmc.Title("Net Worth Trend", order=3, mb="md"),
        dmc.Paper(
            dcc.Graph(figure=fig_networth, config={'displayModeBar': False}),
            p="md",
            radius="md",
            withBorder=True
        ),
        
        # Charts row
        dmc.Grid([
            dmc.GridCol([
                dmc.Title("Asset Breakdown", order=3, mb="md"),
                dmc.Paper(
                    dcc.Graph(figure=fig_assets, config={'displayModeBar': False}),
                    p="md",
                    radius="md",
                    withBorder=True
                )
            ], span=6),
            dmc.GridCol([
                dmc.Title("Assets vs Liabilities Over Time", order=3, mb="md"),
                dmc.Paper(
                    dcc.Graph(figure=fig_comparison, config={'displayModeBar': False}),
                    p="md",
                    radius="md",
                    withBorder=True
                )
            ], span=6),
        ], gutter="lg", mt="xl"),
    ], gap="lg")

def networth_layout():
    """Net Worth analysis page"""
    nw_df = data_loader.get_net_worth_timeseries()
    
    # Calculate metrics
    initial_nw = nw_df.iloc[0]['Net Worth']
    current_nw = nw_df.iloc[-1]['Net Worth']
    total_growth = current_nw - initial_nw
    total_growth_pct = ((current_nw - initial_nw) / abs(initial_nw)) * 100 if initial_nw != 0 else 0
    
    time_period_days = (nw_df.iloc[-1]['Date'] - nw_df.iloc[0]['Date']).days
    time_period_months = time_period_days / 30.44
    avg_monthly_growth = total_growth / time_period_months if time_period_months > 0 else 0
    
    # Net worth with trend line
    fig_trend = go.Figure()
    
    fig_trend.add_trace(go.Scatter(
        x=nw_df['Date'],
        y=nw_df['Net Worth'],
        mode='lines+markers',
        name='Net Worth',
        line=dict(color='#4A9EFF', width=3),
        marker=dict(size=10),
        fill='tozeroy',
        fillcolor='rgba(74, 158, 255, 0.15)'
    ))
    
    # Add trend line
    X = np.array(range(len(nw_df))).reshape(-1, 1)
    y = nw_df['Net Worth'].values
    model = LinearRegression()
    model.fit(X, y)
    trend = model.predict(X)
    
    fig_trend.add_trace(go.Scatter(
        x=nw_df['Date'],
        y=trend,
        mode='lines',
        name='Trend',
        line=dict(color='#EF4444', width=2, dash='dash')
    ))
    
    fig_trend.update_layout(
        template='plotly_white',
        font=dict(family='Inter, sans-serif'),
        xaxis_title='Date',
        yaxis_title='Net Worth ($)',
        hovermode='x unified',
        height=500,
        margin=dict(l=0, r=0, t=20, b=0)
    )
    
    # Month-over-month changes
    nw_df['MoM Change'] = nw_df['Net Worth'].diff()
    nw_df['MoM Change %'] = nw_df['Net Worth'].pct_change() * 100
    
    colors = ['#10B981' if x > 0 else '#EF4444' for x in nw_df['MoM Change'].fillna(0)]
    
    fig_mom = go.Figure()
    fig_mom.add_trace(go.Bar(
        x=nw_df['Date'],
        y=nw_df['MoM Change'],
        marker_color=colors,
        text=nw_df['MoM Change %'].fillna(0).round(1).astype(str) + '%',
        textposition='outside'
    ))
    
    fig_mom.update_layout(
        template='plotly_white',
        font=dict(family='Inter, sans-serif'),
        xaxis_title='Date',
        yaxis_title='Change ($)',
        height=400,
        margin=dict(l=0, r=0, t=20, b=0),
        showlegend=False
    )
    
    return dmc.Stack([
        dmc.Title("Net Worth Analysis", order=2, mb="lg"),
        
        # Metrics
        dmc.Grid([
            dmc.GridCol(create_metric_card("Current Net Worth", format_currency(current_nw)), span=3),
            dmc.GridCol(create_metric_card("Total Growth", format_currency(total_growth)), span=3),
            dmc.GridCol(create_metric_card("Growth Rate", f"{total_growth_pct:.1f}%"), span=3),
            dmc.GridCol(create_metric_card("Avg Monthly Growth", format_currency(avg_monthly_growth)), span=3),
        ], gutter="lg"),
        
        dmc.Divider(my="xl"),
        
        # Net worth progression
        dmc.Title("Net Worth Progression", order=3, mb="md"),
        dmc.Paper(
            dcc.Graph(figure=fig_trend, config={'displayModeBar': False}),
            p="md",
            radius="md",
            withBorder=True
        ),
        
        # Month-over-month
        dmc.Title("Month-over-Month Changes", order=3, mb="md", mt="xl"),
        dmc.Paper(
            dcc.Graph(figure=fig_mom, config={'displayModeBar': False}),
            p="md",
            radius="md",
            withBorder=True
        ),
    ], gap="lg")

def investments_layout():
    """Investments page"""
    inv_df = data_loader.load_investments()
    inv_summary = data_loader.get_investment_summary()
    
    if inv_df.empty:
        return dmc.Alert("No investment data available", color="yellow")
    
    total_invested = inv_summary['Total Invested'].sum() if not inv_summary.empty else 0
    
    # Cumulative investment
    inv_df_sorted = inv_df.sort_values('Trade Date')
    inv_df_sorted['Cumulative'] = inv_df_sorted['Total Value'].cumsum()
    
    fig_cumulative = go.Figure()
    fig_cumulative.add_trace(go.Scatter(
        x=inv_df_sorted['Trade Date'],
        y=inv_df_sorted['Cumulative'],
        mode='lines+markers',
        line=dict(color='#10B981', width=3),
        marker=dict(size=6),
        fill='tozeroy',
        fillcolor='rgba(16, 185, 129, 0.1)'
    ))
    
    fig_cumulative.update_layout(
        template='plotly_white',
        font=dict(family='Inter, sans-serif'),
        xaxis_title='Trade Date',
        yaxis_title='Cumulative Amount ($)',
        hovermode='x unified',
        height=400,
        margin=dict(l=0, r=0, t=20, b=0)
    )
    
    # Portfolio allocation
    fig_allocation = go.Figure(data=[go.Pie(
        labels=inv_summary['Symbol'],
        values=inv_summary['Total Invested'],
        hole=0.5,
        marker=dict(colors=px.colors.sequential.Greens_r)
    )])
    
    fig_allocation.update_layout(
        template='plotly_white',
        font=dict(family='Inter, sans-serif'),
        height=400,
        margin=dict(l=0, r=0, t=20, b=0)
    )
    
    # Monthly activity
    inv_df['Month'] = inv_df['Trade Date'].dt.to_period('M').dt.to_timestamp()
    monthly_inv = inv_df.groupby('Month')['Total Value'].sum().reset_index()
    
    fig_monthly = go.Figure()
    fig_monthly.add_trace(go.Bar(
        x=monthly_inv['Month'],
        y=monthly_inv['Total Value'],
        marker_color='#4A9EFF'
    ))
    
    fig_monthly.update_layout(
        template='plotly_white',
        font=dict(family='Inter, sans-serif'),
        xaxis_title='Month',
        yaxis_title='Amount Invested ($)',
        height=400,
        margin=dict(l=0, r=0, t=20, b=0)
    )
    
    return dmc.Stack([
        dmc.Title("Investment Portfolio", order=2, mb="lg"),
        
        # Metrics
        dmc.Grid([
            dmc.GridCol(create_metric_card("Total Invested", format_currency(total_invested)), span=4),
            dmc.GridCol(create_metric_card("Unique Holdings", str(len(inv_summary))), span=4),
            dmc.GridCol(create_metric_card("Total Transactions", str(len(inv_df))), span=4),
        ], gutter="lg"),
        
        dmc.Divider(my="xl"),
        
        # Cumulative
        dmc.Title("Cumulative Investment Value", order=3, mb="md"),
        dmc.Paper(
            dcc.Graph(figure=fig_cumulative, config={'displayModeBar': False}),
            p="md",
            radius="md",
            withBorder=True
        ),
        
        # Charts row
        dmc.Grid([
            dmc.GridCol([
                dmc.Title("Portfolio Allocation", order=3, mb="md"),
                dmc.Paper(
                    dcc.Graph(figure=fig_allocation, config={'displayModeBar': False}),
                    p="md",
                    radius="md",
                    withBorder=True
                )
            ], span=6),
            dmc.GridCol([
                dmc.Title("Investment Activity by Month", order=3, mb="md"),
                dmc.Paper(
                    dcc.Graph(figure=fig_monthly, config={'displayModeBar': False}),
                    p="md",
                    radius="md",
                    withBorder=True
                )
            ], span=6),
        ], gutter="lg", mt="xl"),
    ], gap="lg")

def employment_layout():
    """Employment history page"""
    emp_df = data_loader.load_employment()
    
    if emp_df.empty:
        return dmc.Alert("No employment data available", color="yellow")
    
    total_comp = emp_df['Total Compensation'].sum()
    avg_comp = emp_df['Total Compensation'].mean()
    
    # Compensation by company
    fig_comp = go.Figure(data=[go.Bar(
        x=emp_df['Company'],
        y=emp_df['Total Compensation'],
        marker_color='#10B981',
        text=emp_df['Total Compensation'].apply(format_currency),
        textposition='outside'
    )])
    
    fig_comp.update_layout(
        template='plotly_white',
        font=dict(family='Inter, sans-serif'),
        xaxis_title='Company',
        yaxis_title='Total Compensation ($)',
        height=400,
        margin=dict(l=0, r=0, t=20, b=0)
    )
    
    # Type distribution
    type_dist = emp_df.groupby('Type')['Total Compensation'].sum().reset_index()
    
    fig_type = go.Figure(data=[go.Pie(
        labels=type_dist['Type'],
        values=type_dist['Total Compensation'],
        hole=0.5,
        marker=dict(colors=px.colors.sequential.Blues_r)
    )])
    
    fig_type.update_layout(
        template='plotly_white',
        font=dict(family='Inter, sans-serif'),
        height=400,
        margin=dict(l=0, r=0, t=20, b=0)
    )
    
    return dmc.Stack([
        dmc.Title("Employment History", order=2, mb="lg"),
        
        # Metrics
        dmc.Grid([
            dmc.GridCol(create_metric_card("Total Compensation", format_currency(total_comp)), span=4),
            dmc.GridCol(create_metric_card("Total Positions", str(len(emp_df))), span=4),
            dmc.GridCol(create_metric_card("Average Compensation", format_currency(avg_comp)), span=4),
        ], gutter="lg"),
        
        dmc.Divider(my="xl"),
        
        # Charts
        dmc.Grid([
            dmc.GridCol([
                dmc.Title("Compensation by Company", order=3, mb="md"),
                dmc.Paper(
                    dcc.Graph(figure=fig_comp, config={'displayModeBar': False}),
                    p="md",
                    radius="md",
                    withBorder=True
                )
            ], span=6),
            dmc.GridCol([
                dmc.Title("Employment Type Distribution", order=3, mb="md"),
                dmc.Paper(
                    dcc.Graph(figure=fig_type, config={'displayModeBar': False}),
                    p="md",
                    radius="md",
                    withBorder=True
                )
            ], span=6),
        ], gutter="lg"),
    ], gap="lg")

def growth_layout():
    """Growth analysis page"""
    nw_df = data_loader.get_net_worth_timeseries()
    inv_df = data_loader.load_investments()
    emp_df = data_loader.load_employment()
    al_df = data_loader.load_assets_liabilities()
    
    cagr = data_loader.calculate_cagr()
    total_invested = inv_df['Total Value'].sum()
    total_earned = emp_df['Total Compensation'].sum()
    
    # Year-over-year
    nw_df['Year'] = nw_df['Date'].dt.year
    yearly_nw = nw_df.groupby('Year')['Net Worth'].last().reset_index()
    yearly_nw['YoY Growth'] = yearly_nw['Net Worth'].pct_change() * 100
    
    fig_yoy = go.Figure()
    fig_yoy.add_trace(go.Bar(
        x=yearly_nw['Year'],
        y=yearly_nw['Net Worth'],
        name='Net Worth',
        marker_color='#4A9EFF',
        yaxis='y',
        text=yearly_nw['Net Worth'].apply(format_currency),
        textposition='outside'
    ))
    
    fig_yoy.add_trace(go.Scatter(
        x=yearly_nw['Year'],
        y=yearly_nw['YoY Growth'].fillna(0),
        name='YoY Growth %',
        line=dict(color='#10B981', width=3),
        marker=dict(size=10),
        yaxis='y2'
    ))
    
    fig_yoy.update_layout(
        template='plotly_white',
        font=dict(family='Inter, sans-serif'),
        xaxis_title='Year',
        yaxis=dict(title='Net Worth ($)'),
        yaxis2=dict(title='YoY Growth (%)', overlaying='y', side='right'),
        height=450,
        margin=dict(l=0, r=0, t=20, b=0)
    )
    
    # Asset category growth
    asset_types = al_df[al_df['Category'] == 'Asset']['Type'].unique()
    asset_growth = []
    
    for asset_type in asset_types:
        asset_data = al_df[(al_df['Category'] == 'Asset') & (al_df['Type'] == asset_type)]
        if not asset_data.empty:
            dates = sorted(asset_data['Date'].unique())
            if len(dates) >= 2:
                initial = asset_data[asset_data['Date'] == dates[0]]['Value'].sum()
                final = asset_data[asset_data['Date'] == dates[-1]]['Value'].sum()
                growth = final - initial
                growth_pct = ((final - initial) / initial * 100) if initial > 0 else 0
                
                asset_growth.append({
                    'Type': asset_type,
                    'Growth': growth,
                    'Growth %': growth_pct
                })
    
    if asset_growth:
        growth_df = pd.DataFrame(asset_growth).sort_values('Growth', ascending=False)
        colors = ['#10B981' if x > 0 else '#EF4444' for x in growth_df['Growth']]
        
        fig_assets = go.Figure()
        fig_assets.add_trace(go.Bar(
            x=growth_df['Type'],
            y=growth_df['Growth'],
            marker_color=colors,
            text=growth_df['Growth %'].round(1).astype(str) + '%',
            textposition='outside'
        ))
        
        fig_assets.update_layout(
            template='plotly_white',
            font=dict(family='Inter, sans-serif'),
            xaxis_title='Asset Type',
            yaxis_title='Growth ($)',
            height=400,
            margin=dict(l=0, r=0, t=20, b=0)
        )
    else:
        fig_assets = go.Figure()
    
    return dmc.Stack([
        dmc.Title("Financial Growth Analysis", order=2, mb="lg"),
        
        # Metrics
        dmc.Grid([
            dmc.GridCol(create_metric_card("CAGR (Net Worth)", f"{cagr:.1f}%"), span=4),
            dmc.GridCol(create_metric_card("Total Invested", format_currency(total_invested)), span=4),
            dmc.GridCol(create_metric_card("Total Earned", format_currency(total_earned)), span=4),
        ], gutter="lg"),
        
        dmc.Divider(my="xl"),
        
        # YoY growth
        dmc.Title("Year-over-Year Net Worth Growth", order=3, mb="md"),
        dmc.Paper(
            dcc.Graph(figure=fig_yoy, config={'displayModeBar': False}),
            p="md",
            radius="md",
            withBorder=True
        ),
        
        # Asset growth
        dmc.Title("Asset Category Growth", order=3, mb="md", mt="xl"),
        dmc.Paper(
            dcc.Graph(figure=fig_assets, config={'displayModeBar': False}),
            p="md",
            radius="md",
            withBorder=True
        ),
    ], gap="lg")

# Main app layout
app.layout = dmc.MantineProvider(
    children=dmc.AppShell(
        children=[
            dmc.AppShellNavbar(
                children=create_navbar(),
                p="md",
            ),
            dmc.AppShellMain(
                children=html.Div(id="page-content", style={"padding": "20px"})
            ),
        ],
        navbar={"width": 250, "breakpoint": "sm"},
        padding="md",
    )
)

# Callback for navigation
@callback(
    [Output("page-content", "children"),
     Output({"type": "nav-link", "index": ALL}, "active")],
    [Input({"type": "nav-link", "index": ALL}, "n_clicks")]
)
def update_page(n_clicks):
    """Update page content and navigation highlighting based on navigation clicks"""
    ctx = dash.callback_context
    
    # Determine which page to show
    current_page = "dashboard"
    
    if ctx.triggered:
        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
        
        if triggered_id and triggered_id != "":
            import json
            nav_data = json.loads(triggered_id)
            current_page = nav_data.get("index", "dashboard")
    
    # Update active states for all nav links
    nav_items = ["dashboard", "net-worth", "investments", "employment", "growth"]
    active_states = [page == current_page for page in nav_items]
    
    # Get page content
    page_content = dashboard_layout()
    if current_page == "net-worth":
        page_content = networth_layout()
    elif current_page == "investments":
        page_content = investments_layout()
    elif current_page == "employment":
        page_content = employment_layout()
    elif current_page == "growth":
        page_content = growth_layout()
    
    return page_content, active_states

# Callback for rotating greeting message
@callback(
    Output("rotating-message-container", "children"),
    Input("greeting-interval", "n_intervals")
)
def update_greeting_message(n_intervals):
    """Update the rotating greeting message with fade animation"""
    # Get current message index
    message_index = n_intervals % len(ROTATING_MESSAGES)
    current_message = ROTATING_MESSAGES[message_index]
    
    # Return a new div with unique key to force re-render and animation
    return html.Div(
        current_message,
        key=f"message-{n_intervals}",  # Unique key forces React to re-render
        style={
            "fontSize": "24px",
            "fontWeight": "700",
            "color": "#4A9EFF",  # Blue
            "lineHeight": "1.2",
            "animation": "messagecycle 5.4s ease-in-out"
        }
    )

# Run server
if __name__ == "__main__":
    app.run(debug=True, port=8050)

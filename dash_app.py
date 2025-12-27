"""
My Finance Hub - Dash Application
Professional FinTech dashboard using Plotly Dash and Dash Mantine Components
"""

# ============================================================================
# CONFIGURATION: Set the Excel file to load
# ============================================================================
EXCEL_FILE = 'user_data/test_financial_data.xlsx'  # Change this to load a different file
# ============================================================================

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
data_loader = load_data(EXCEL_FILE)

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

def create_metric_card(label, value, change=None, color='blue', is_liability=False, change_color_override=None):
    """Create a metric card using DMC components
    
    Args:
        label: Card label
        value: Main value to display
        change: Change text (e.g., '↑ 5.2% vs last period')
        color: Card color theme
        is_liability: If True, inverts color logic (up=red, down=green)
        change_color_override: Force a specific color for change text (e.g., 'blue')
    """
    # Determine color based on direction and metric type
    if change_color_override:
        change_color = change_color_override
    elif change:
        if is_liability:
            # For liabilities: increase is bad (red), decrease is good (green)
            change_color = "red" if '↑' in change else "green" if '↓' in change else "dimmed"
        else:
            # For assets/net worth: increase is good (green), decrease is bad (red)
            change_color = "green" if '↑' in change else "red" if '↓' in change else "dimmed"
    
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
                        c=change_color
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
        # Interval component to trigger message rotation
        dcc.Interval(
            id='greeting-interval',
            interval=3900,  # 3.9 seconds total (0.7s fade in + 2.5s visible + 0.7s fade out)
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
        {"icon": "💰", "label": "Net Worth", "value": "dashboard"},
        {"icon": "📈", "label": "Investments", "value": "investments"},
        {"icon": "👔", "label": "Employment", "value": "employment"},
        {"icon": "📊", "label": "Benchmarking", "value": "benchmarking"},
        {"icon": "🧮", "label": "Calculators", "value": "calculators"},
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
    """Net Worth page layout (merged with old Net Worth analysis)"""
    # Get data
    metrics = data_loader.get_latest_metrics()
    al_df = data_loader.load_assets_liabilities()
    
    # Calculate changes
    dates = sorted(al_df['Date'].unique())
    nw_change = 0
    assets_change = 0
    liabilities_change = 0
    
    if len(dates) >= 2:
        prev_date = dates[-2]
        prev_data = al_df[al_df['Date'] == prev_date]
        prev_assets = prev_data[prev_data['Category'] == 'Asset']['Value'].sum()
        prev_liabilities = prev_data[prev_data['Category'] == 'Liability']['Value'].sum()
        prev_net_worth = prev_assets - prev_liabilities
        
        nw_change = calculate_percentage_change(metrics['net_worth'], prev_net_worth)
        assets_change = calculate_percentage_change(metrics['total_assets'], prev_assets)
        liabilities_change = calculate_percentage_change(metrics['total_liabilities'], prev_liabilities)
    
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
        margin=dict(l=0, r=0, t=20, b=0),
        hoverlabel=dict(
            bgcolor='white',
            font_size=13,
            font_family='Inter, sans-serif',
            font_color='black',
            bordercolor='black',
            namelength=0
        )
    )
    
    # Asset breakdown
    asset_breakdown = data_loader.get_asset_breakdown()
    
    fig_assets = go.Figure(data=[go.Pie(
        labels=asset_breakdown['Type'],
        values=asset_breakdown['Value'],
        hole=0.5,
        marker=dict(colors=px.colors.sequential.Blues_r),
        textposition='auto',
        hovertemplate='<b>%{label}</b><br>$%{value:,.2f}<br>%{percent}<extra></extra>'
    )])
    
    fig_assets.update_layout(
        template='plotly_white',
        font=dict(family='Inter, sans-serif'),
        height=400,
        margin=dict(l=0, r=0, t=20, b=0),
        showlegend=True,
        hoverlabel=dict(
            bgcolor='white',
            font_size=13,
            font_family='Inter, sans-serif',
            font_color='black',
            bordercolor='black',
            namelength=0
        )
    )
    
    # Liabilities breakdown
    liability_breakdown = data_loader.get_liability_breakdown()
    
    fig_liabilities = go.Figure(data=[go.Pie(
        labels=liability_breakdown['Type'],
        values=liability_breakdown['Value'],
        hole=0.5,
        marker=dict(colors=px.colors.sequential.Reds_r),
        textposition='auto',
        hovertemplate='<b>%{label}</b><br>$%{value:,.2f}<br>%{percent}<extra></extra>'
    )])
    
    fig_liabilities.update_layout(
        template='plotly_white',
        font=dict(family='Inter, sans-serif'),
        height=400,
        margin=dict(l=0, r=0, t=20, b=0),
        showlegend=True,
        hoverlabel=dict(
            bgcolor='white',
            font_size=13,
            font_family='Inter, sans-serif',
            font_color='black',
            bordercolor='black',
            namelength=0
        )
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
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hoverlabel=dict(
            bgcolor='white',
            font_size=13,
            font_family='Inter, sans-serif',
            font_color='black',
            bordercolor='black',
            namelength=0
        )
    )
    
    # Month-over-month changes
    nw_df = data_loader.get_net_worth_timeseries()
    nw_df['MoM Change'] = nw_df['Net Worth'].diff()
    nw_df['MoM Change %'] = nw_df['Net Worth'].pct_change() * 100
    
    colors = ['#10B981' if x > 0 else '#EF4444' for x in nw_df['MoM Change'].fillna(0)]
    
    fig_mom = go.Figure()
    fig_mom.add_trace(go.Bar(
        x=nw_df['Date'],
        y=nw_df['MoM Change'],
        marker_color=colors,
        text=nw_df['MoM Change %'].fillna(0).round(1).astype(str) + '%',
        textposition='outside',
        textfont=dict(size=12, color='#1f2937'),
        hovertemplate='<b>%{x}</b><br>Net Worth Change: $%{y:,.2f}<extra></extra>'
    ))
    
    fig_mom.update_layout(
        template='plotly_white',
        font=dict(family='Inter, sans-serif'),
        xaxis_title='Date',
        yaxis_title='Net Worth Change ($)',
        height=400,
        margin=dict(l=0, r=0, t=20, b=0),
        showlegend=False,
        hoverlabel=dict(
            bgcolor='white',
            font_size=13,
            font_family='Inter, sans-serif',
            font_color='black',
            bordercolor='black',
            namelength=0
        )
    )
    
    # Create Net Worth card with glow effect
    net_worth_card = dmc.Paper(
        children=[
            dmc.Stack(
                children=[
                    dmc.Text("Net Worth", size="sm", fw=500, c="dimmed", tt="uppercase"),
                    dmc.Text(format_currency(metrics['net_worth']), size="xl", fw=700, style={"fontSize": "32px"}),
                    dmc.Text(
                        f"{'↑' if nw_change > 0 else '↓'} {abs(nw_change):.1f}% vs last period",
                        size="sm",
                        fw=500,
                        c="green" if nw_change > 0 else "red"
                    )
                ],
                gap="xs"
            )
        ],
        p="lg",
        radius="md",
        withBorder=True,
        shadow="xl",
        style={
            "height": "100%",
            "boxShadow": "0 0 20px rgba(74, 158, 255, 0.3)",
            "border": "2px solid #4A9EFF"
        }
    )
    
    return dmc.Stack([
        dmc.Title("Net Worth", order=2, mb="lg"),
        
        # Metrics row
        dmc.Grid([
            dmc.GridCol(create_metric_card(
                "Total Assets",
                format_currency(metrics['total_assets']),
                f"{'↑' if assets_change > 0 else '↓'} {abs(assets_change):.1f}% vs last period"
            ), span=4),
            dmc.GridCol(net_worth_card, span=4),
            dmc.GridCol(create_metric_card(
                "Total Liabilities",
                format_currency(metrics['total_liabilities']),
                f"{'↑' if liabilities_change > 0 else '↓'} {abs(liabilities_change):.1f}% vs last period",
                is_liability=True
            ), span=4),
        ], gutter="lg"),
        
        dmc.Divider(my="xl"),
        
        # Net worth trend
        dmc.Title("Overall Trend", order=3, mb="md"),
        dmc.Paper(
            dcc.Graph(figure=fig_networth, config={'displayModeBar': False}),
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
        
        # Assets vs Liabilities Over Time - full width
        dmc.Title("Assets vs Liabilities Over Time", order=3, mb="md", mt="xl"),
        dmc.Paper(
            dcc.Graph(figure=fig_comparison, config={'displayModeBar': False}),
            p="md",
            radius="md",
            withBorder=True
        ),
        
        # Breakdown charts row
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
                dmc.Title("Liabilities Breakdown", order=3, mb="md"),
                dmc.Paper(
                    dcc.Graph(figure=fig_liabilities, config={'displayModeBar': False}),
                    p="md",
                    radius="md",
                    withBorder=True
                )
            ], span=6),
        ], gutter="lg", mt="xl"),
    ], gap="lg")



def investments_layout():
    """Investments page"""
    inv_df = data_loader.load_investments()
    inv_summary = data_loader.get_investment_summary()
    al_df = data_loader.load_assets_liabilities()
    
    if inv_df.empty:
        return dmc.Alert("No investment data available", color="yellow")
    
    # Calculate cost basis (sum of buy transactions)
    cost_basis = inv_df[inv_df['Side'] == 'Buy']['Total Value'].sum()
    
    # Get total stock value from Assets & Liabilities (Stocks - Stake AUS - IVV)
    latest_date = al_df['Date'].max()
    stock_data = al_df[(al_df['Date'] == latest_date) & 
                       (al_df['Category'] == 'Asset') & 
                       (al_df['Type'].str.contains('Stocks', na=False))]
    total_value = stock_data['Value'].sum()
    
    # Calculate % increase
    pct_increase = ((total_value / cost_basis) - 1) * 100 if cost_basis > 0 else 0
    
    # Cumulative investment (cost basis over time)
    inv_df_sorted = inv_df[inv_df['Side'] == 'Buy'].sort_values('Trade Date').copy()
    
    # Check if we have buy transactions
    if inv_df_sorted.empty:
        return dmc.Alert("No buy transactions found in investment data", color="yellow")
    
    inv_df_sorted['Cumulative Cost Basis'] = inv_df_sorted['Total Value'].cumsum()
    
    # Get stock values over time for overlay
    stock_values_over_time = al_df[(al_df['Category'] == 'Asset') & 
                                    (al_df['Type'].str.contains('Stocks', na=False))]
    stock_timeseries = stock_values_over_time.groupby('Date')['Value'].sum().reset_index()
    stock_timeseries.columns = ['Date', 'Stock Value']
    
    # Ensure Date column is datetime
    stock_timeseries['Date'] = pd.to_datetime(stock_timeseries['Date'])
    inv_df_sorted['Trade Date'] = pd.to_datetime(inv_df_sorted['Trade Date'])
    
    # Helper function for linear interpolation
    def linear_interpolate(x, x1, y1, x2, y2):
        """Linear interpolation: find y at x given two points (x1,y1) and (x2,y2)"""
        if x2 == x1:
            return y1
        return y1 + (y2 - y1) * (x - x1) / (x2 - x1)
    
    # Create dense timeline for interpolation
    all_dates = sorted(set(list(inv_df_sorted['Trade Date']) + list(stock_timeseries['Date'])))
    
    # Interpolate cost basis and market value for all dates
    cost_basis_interpolated = []
    market_value_interpolated = []
    
    for date in all_dates:
        # Interpolate cost basis
        cb_dates = list(inv_df_sorted['Trade Date'])
        cb_values = list(inv_df_sorted['Cumulative Cost Basis'])
        
        if date in cb_dates:
            cb_val = inv_df_sorted[inv_df_sorted['Trade Date'] == date]['Cumulative Cost Basis'].iloc[0]
        elif date < cb_dates[0]:
            cb_val = 0
        elif date > cb_dates[-1]:
            cb_val = cb_values[-1]  # Hold last value
        else:
            # Find surrounding points
            cb_val = cb_values[-1]  # Default to last value
            for i in range(len(cb_dates) - 1):
                if cb_dates[i] <= date <= cb_dates[i+1]:
                    cb_val = linear_interpolate(
                        date.timestamp(), 
                        cb_dates[i].timestamp(), cb_values[i],
                        cb_dates[i+1].timestamp(), cb_values[i+1]
                    )
                    break
        
        # Interpolate market value
        mv_dates = list(stock_timeseries['Date'])
        mv_values = list(stock_timeseries['Stock Value'])
        
        if date in mv_dates:
            mv_val = stock_timeseries[stock_timeseries['Date'] == date]['Stock Value'].iloc[0]
        elif date < mv_dates[0]:
            mv_val = None
        elif date > mv_dates[-1]:
            mv_val = mv_values[-1]  # Hold last value
        else:
            # Find surrounding points
            mv_val = mv_values[-1]  # Default to last value
            for i in range(len(mv_dates) - 1):
                if mv_dates[i] <= date <= mv_dates[i+1]:
                    mv_val = linear_interpolate(
                        date.timestamp(),
                        mv_dates[i].timestamp(), mv_values[i],
                        mv_dates[i+1].timestamp(), mv_values[i+1]
                    )
                    break
        
        cost_basis_interpolated.append(cb_val)
        market_value_interpolated.append(mv_val)
    
    # Determine if we need extensions
    cb_last_date = inv_df_sorted['Trade Date'].max()
    mv_last_date = stock_timeseries['Date'].max()
    
    fig_cumulative = go.Figure()
    
    # Market value - solid line (light blue with shading) - ADD FIRST so it's underneath
    mv_actual_dates = list(stock_timeseries['Date'])
    mv_actual_values = list(stock_timeseries['Stock Value'])
    
    fig_cumulative.add_trace(go.Scatter(
        x=mv_actual_dates,
        y=mv_actual_values,
        mode='lines+markers',
        name='Market Value',
        line=dict(color='#60a5fa', width=3),
        marker=dict(size=8, color='#60a5fa'),
        fill='tozeroy',
        fillcolor='rgba(96, 165, 250, 0.3)',
        hoverinfo='skip'
    ))
    
    # If cost basis is more recent, extend market value with dotted line AND shading
    if cb_last_date > mv_last_date:
        fig_cumulative.add_trace(go.Scatter(
            x=[mv_last_date, cb_last_date],
            y=[mv_actual_values[-1], mv_actual_values[-1]],
            mode='lines',
            name='Market Value (estimated)',
            line=dict(color='#60a5fa', width=2, dash='dot'),
            fill='tozeroy',
            fillcolor='rgba(96, 165, 250, 0.3)',
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Cost basis - solid line (dark blue with shading) - ADD SECOND so it overlaps on top
    cb_actual_dates = list(inv_df_sorted['Trade Date'])
    cb_actual_values = list(inv_df_sorted['Cumulative Cost Basis'])
    
    fig_cumulative.add_trace(go.Scatter(
        x=cb_actual_dates,
        y=cb_actual_values,
        mode='lines+markers',
        name='Cost Basis',
        line=dict(color='#1e40af', width=3),
        marker=dict(size=7, color='#1e40af'),
        fill='tozeroy',
        fillcolor='rgba(30, 64, 175, 0.2)',
        hoverinfo='skip'
    ))
    
    # If market value is more recent, extend cost basis with dotted line AND shading
    if mv_last_date > cb_last_date:
        fig_cumulative.add_trace(go.Scatter(
            x=[cb_last_date, mv_last_date],
            y=[cb_actual_values[-1], cb_actual_values[-1]],
            mode='lines',
            name='Cost Basis (estimated)',
            line=dict(color='#1e40af', width=2, dash='dot'),
            fill='tozeroy',
            fillcolor='rgba(30, 64, 175, 0.2)',
            showlegend=False,
            hoverinfo='skip'
        ))
    
    # Add invisible trace with interpolated values for hover
    interpolated_df = pd.DataFrame({
        'Date': all_dates,
        'Cost Basis': cost_basis_interpolated,
        'Market Value': market_value_interpolated
    })
    
    # Create custom hover text
    hover_texts = []
    for idx, row in interpolated_df.iterrows():
        text = ""
        if pd.notna(row['Market Value']):
            text += f"<span style='color:#60a5fa;'>⬤</span>Market Value: ${row['Market Value']:,.2f}<br>"
        else:
            text += "<span style='color:#60a5fa;'>⬤</span>Market Value: N/A<br>"
        text += f"<span style='color:#1e40af;'>⬤</span>Cost Basis: ${row['Cost Basis']:,.2f}"
        hover_texts.append(text)
    
    fig_cumulative.add_trace(go.Scatter(
        x=interpolated_df['Date'],
        y=interpolated_df['Cost Basis'],
        mode='markers',
        marker=dict(size=0.1, opacity=0),
        showlegend=False,
        hovertemplate='%{text}<extra></extra>',
        text=hover_texts
    ))
    
    fig_cumulative.update_layout(
        template='plotly_white',
        font=dict(family='Inter, sans-serif'),
        xaxis_title='Date',
        xaxis=dict(
            type='date'
            # Range is automatically determined from data
        ),
        yaxis_title='Amount ($)',
        hovermode='x unified',
        height=400,
        margin=dict(l=0, r=0, t=20, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hoverlabel=dict(
            bgcolor='white',
            font_size=13,
            font_family='Inter, sans-serif',
            font_color='black',
            bordercolor='black',
            namelength=0
        )
    )
    
    # Portfolio allocation with blue gradient
    blue_gradient = ['#1e3a8a', '#2563eb', '#3b82f6', '#60a5fa', '#93c5fd', '#bfdbfe', '#dbeafe']
    
    fig_allocation = go.Figure(data=[go.Pie(
        labels=inv_summary['Symbol'],
        values=inv_summary['Total Invested'],
        hole=0.5,
        marker=dict(colors=blue_gradient[:len(inv_summary)]),
        hovertemplate='<b>%{label}</b><br>$%{value:,.2f}<br>%{percent}<extra></extra>'
    )])
    
    fig_allocation.update_layout(
        template='plotly_white',
        font=dict(family='Inter, sans-serif'),
        height=400,
        margin=dict(l=0, r=0, t=20, b=0),
        hoverlabel=dict(
            bgcolor='white',
            font_size=13,
            font_family='Inter, sans-serif',
            font_color='black',
            bordercolor='black',
            namelength=0
        )
    )
    
    # Monthly activity
    inv_df['Month'] = inv_df['Trade Date'].dt.to_period('M').dt.to_timestamp()
    monthly_inv = inv_df.groupby('Month')['Total Value'].sum().reset_index()
    
    fig_monthly = go.Figure()
    fig_monthly.add_trace(go.Bar(
        x=monthly_inv['Month'],
        y=monthly_inv['Total Value'],
        marker_color='#4A9EFF',
        hovertemplate='<b>%{x}</b><br>Amount: $%{y:,.2f}<extra></extra>'
    ))
    
    fig_monthly.update_layout(
        template='plotly_white',
        font=dict(family='Inter, sans-serif'),
        xaxis_title='Month',
        yaxis_title='Amount Invested ($)',
        height=400,
        margin=dict(l=0, r=0, t=20, b=0),
        hoverlabel=dict(
            bgcolor='white',
            font_size=13,
            font_family='Inter, sans-serif',
            font_color='black',
            bordercolor='black',
            namelength=0
        )
    )
    
    # Performance by ticker (% gain/loss)
    ticker_performance = []
    for ticker in inv_summary['Symbol']:
        ticker_cost = inv_summary[inv_summary['Symbol'] == ticker]['Total Invested'].iloc[0]
        # Get current value from latest stock data
        ticker_current = stock_data[stock_data['Type'].str.contains(ticker, na=False)]['Value'].sum()
        if ticker_cost > 0:
            pct_change = ((ticker_current / ticker_cost) - 1) * 100
        else:
            pct_change = 0
        ticker_performance.append({'Symbol': ticker, 'Performance': pct_change, 'Current Value': ticker_current})
    
    perf_df = pd.DataFrame(ticker_performance).sort_values('Performance', ascending=True)
    
    # Color code: green for positive, red for negative
    bar_colors = ['#10B981' if x >= 0 else '#EF4444' for x in perf_df['Performance']]
    
    fig_performance = go.Figure(data=[go.Bar(
        x=perf_df['Performance'],
        y=perf_df['Symbol'],
        orientation='h',
        marker_color=bar_colors,
        text=[f"{x:+.1f}%" for x in perf_df['Performance']],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Performance: %{x:.2f}%<extra></extra>'
    )])
    
    fig_performance.update_layout(
        template='plotly_white',
        font=dict(family='Inter, sans-serif'),
        xaxis_title='Performance (%)',
        yaxis_title='',
        height=400,
        margin=dict(l=0, r=0, t=20, b=0),
        hoverlabel=dict(
            bgcolor='white',
            font_size=13,
            font_family='Inter, sans-serif',
            font_color='black',
            bordercolor='black',
            namelength=0
        )
    )
    
    fig_allocation.update_layout(
        template='plotly_white',
        font=dict(family='Inter, sans-serif'),
        height=400,
        margin=dict(l=0, r=0, t=20, b=0),
        hoverlabel=dict(
            bgcolor='white',
            font_size=13,
            font_family='Inter, sans-serif',
            font_color='black',
            bordercolor='black',
            namelength=0
        )
    )
    
    # Monthly activity
    inv_df['Month'] = inv_df['Trade Date'].dt.to_period('M').dt.to_timestamp()
    monthly_inv = inv_df.groupby('Month')['Total Value'].sum().reset_index()
    
    fig_monthly = go.Figure()
    fig_monthly.add_trace(go.Bar(
        x=monthly_inv['Month'],
        y=monthly_inv['Total Value'],
        marker_color='#4A9EFF',
        hovertemplate='<b>%{x}</b><br>Amount: $%{y:,.2f}<extra></extra>'
    ))
    
    fig_monthly.update_layout(
        template='plotly_white',
        font=dict(family='Inter, sans-serif'),
        xaxis_title='Month',
        yaxis_title='Amount Invested ($)',
        height=400,
        margin=dict(l=0, r=0, t=20, b=0),
        hoverlabel=dict(
            bgcolor='white',
            font_size=13,
            font_family='Inter, sans-serif',
            font_color='black',
            bordercolor='black',
            namelength=0
        )
    )
    
    # Investment frequency (number of purchase transactions per ticker)
    transaction_counts = inv_df[inv_df['Side'] == 'Buy'].groupby('Symbol').size().reset_index(name='Transactions')
    transaction_counts = transaction_counts.sort_values('Transactions', ascending=True)
    
    # Create a blue gradient for the bars
    ticker_colors = ['#1e3a8a', '#2563eb', '#3b82f6', '#60a5fa', '#93c5fd']
    bar_colors_ticker = [ticker_colors[i % len(ticker_colors)] for i in range(len(transaction_counts))]
    
    fig_performance = go.Figure(data=[go.Bar(
        x=transaction_counts['Transactions'],
        y=transaction_counts['Symbol'],
        orientation='h',
        marker_color=bar_colors_ticker,
        text=transaction_counts['Transactions'],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Transactions: %{x}<extra></extra>'
    )])
    
    fig_performance.update_layout(
        template='plotly_white',
        font=dict(family='Inter, sans-serif'),
        xaxis_title='Number of Transactions',
        yaxis_title='',
        height=400,
        margin=dict(l=0, r=0, t=20, b=0),
        hoverlabel=dict(
            bgcolor='white',
            font_size=13,
            font_family='Inter, sans-serif',
            font_color='black',
            bordercolor='black',
            namelength=0
        )
    )
    
    # Calculate previous quarter values for comparison
    # Get second-to-last date from stock_timeseries (represents previous quarter)
    if len(stock_timeseries) >= 2:
        prev_quarter_date = stock_timeseries.iloc[-2]['Date']
        
        # Get market value at previous quarter
        prev_quarter_mv = stock_timeseries.iloc[-2]['Stock Value']
        
        # Get cost basis at previous quarter using interpolation
        cb_dates = list(inv_df_sorted['Trade Date'])
        cb_values = list(inv_df_sorted['Cumulative Cost Basis'])
        
        if prev_quarter_date in cb_dates:
            prev_quarter_cb = inv_df_sorted[inv_df_sorted['Trade Date'] == prev_quarter_date]['Cumulative Cost Basis'].iloc[0]
        elif prev_quarter_date < cb_dates[0]:
            prev_quarter_cb = 0
        elif prev_quarter_date > cb_dates[-1]:
            prev_quarter_cb = cb_values[-1]
        else:
            # Linear interpolation
            prev_quarter_cb = cb_values[-1]
            for i in range(len(cb_dates) - 1):
                if cb_dates[i] <= prev_quarter_date <= cb_dates[i+1]:
                    prev_quarter_cb = linear_interpolate(
                        prev_quarter_date.timestamp(),
                        cb_dates[i].timestamp(), cb_values[i],
                        cb_dates[i+1].timestamp(), cb_values[i+1]
                    )
                    break
        
        # Format previous quarter name as month abbreviation
        prev_quarter_name = prev_quarter_date.strftime("%b %Y")
        
        # Calculate changes
        mv_change = total_value - prev_quarter_mv
        cb_change = cost_basis - prev_quarter_cb
        
        # Format change text
        mv_change_text = f"{'↑' if mv_change >= 0 else '↓'} {format_currency(abs(mv_change))} vs {prev_quarter_name}"
        cb_change_text = f"{'↑' if cb_change >= 0 else '↓'} {format_currency(abs(cb_change))} vs {prev_quarter_name}"
    else:
        mv_change_text = None
        cb_change_text = None
    
    # Calculate dollar increase and percentage
    dollar_increase = total_value - cost_basis
    pct_increase_text = f"{'↑' if pct_increase >= 0 else '↓'} {abs(pct_increase):.1f}% vs inception"
    
    # Create Total Value card with glow effect and change text
    total_value_children = [
        dmc.Text("Total Value", size="sm", fw=500, c="dimmed", tt="uppercase"),
        dmc.Text(format_currency(total_value), size="xl", fw=700, style={"fontSize": "32px"}),
    ]
    
    # Add change text if available
    if mv_change_text:
        change_color = "green" if mv_change >= 0 else "red"
        total_value_children.append(
            dmc.Text(mv_change_text, size="sm", fw=500, c=change_color)
        )
    
    total_value_card = dmc.Paper(
        children=[
            dmc.Stack(
                children=total_value_children,
                gap="xs"
            )
        ],
        p="lg",
        radius="md",
        withBorder=True,
        shadow="xl",
        style={
            "height": "100%",
            "boxShadow": "0 0 20px rgba(74, 158, 255, 0.3)",
            "border": "2px solid #4A9EFF"
        }
    )
    
    return dmc.Stack([
        dmc.Title("Investment Portfolio", order=2, mb="lg"),
        
        # Metrics
        dmc.Grid([
            dmc.GridCol(create_metric_card("Cost Basis", format_currency(cost_basis), change=cb_change_text), span=4),
            dmc.GridCol(total_value_card, span=4),
            dmc.GridCol(create_metric_card("Total Increase", format_currency(dollar_increase), change=pct_increase_text), span=4),
        ], gutter="lg"),
        
        dmc.Divider(my="xl"),
        
        # Stock Market Investments - Full Width
        dmc.Title("Stock Market Investments", order=3, mb="md"),
        dmc.Paper(
            dcc.Graph(figure=fig_cumulative, config={'displayModeBar': False}),
            p="md",
            radius="md",
            withBorder=True
        ),
        
        # Investment Activity by Month - Full Width
        dmc.Title("Investment Activity by Month", order=3, mb="md", mt="xl"),
        dmc.Paper(
            dcc.Graph(figure=fig_monthly, config={'displayModeBar': False}),
            p="md",
            radius="md",
            withBorder=True
        ),
        
        # Charts row - Portfolio Allocation and Performance
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
                dmc.Title("Investment Frequency", order=3, mb="md"),
                dmc.Paper(
                    dcc.Graph(figure=fig_performance, config={'displayModeBar': False}),
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
    
    # Salary progression timeline
    emp_df_sorted = emp_df.sort_values('Date Started').copy()
    
    # Dynamic color palette that fits the app's color scheme
    # Primary color: #4A9EFF (blue)
    color_palette = [
        '#4A9EFF',  # primary blue
        '#8b5cf6',  # purple
        '#10b981',  # green
        '#f59e0b',  # amber
        '#ef4444',  # red
        '#ec4899',  # pink
        '#06b6d4',  # cyan
        '#8b5a3c',  # brown
        '#6366f1',  # indigo
        '#14b8a6',  # teal
    ]
    
    # Assign colors dynamically to companies in order of appearance
    unique_companies = emp_df_sorted['Company'].unique()
    company_colors = {company: color_palette[i % len(color_palette)] 
                     for i, company in enumerate(unique_companies)}
    
    # Calculate business days worked and handle ongoing positions
    # Special case: Artin Education only worked weekends (Sat + Sun)
    from datetime import datetime, timedelta
    import numpy as np
    
    def count_working_days(row):
        """Count working days - weekends only for Artin Education, business days for others"""
        if pd.isna(row['Date Started']):
            return 0
        
        end_date = row['Date Ended'] if pd.notna(row['Date Ended']) else pd.Timestamp.now()
        start = row['Date Started'].date()
        end = end_date.date()
        
        # For Artin Education, count only Saturdays and Sundays
        if 'Artin' in str(row['Company']):
            total_days = 0
            current = start
            while current <= end:
                # 5 = Saturday, 6 = Sunday
                if current.weekday() in [5, 6]:
                    total_days += 1
                current += timedelta(days=1)
            return total_days
        else:
            # For all other companies, count business days (Mon-Fri)
            return np.busday_count(start, end)
    
    emp_df_sorted['End Date Calculated'] = emp_df_sorted['Date Ended'].fillna(pd.Timestamp.now())
    emp_df_sorted['Business Days'] = emp_df_sorted.apply(count_working_days, axis=1)
    
    # Calculate metrics
    total_business_days = emp_df_sorted['Business Days'].sum()
    current_salary = emp_df_sorted.iloc[-1]['Total Compensation'] if not emp_df_sorted.empty else 0
    current_base = emp_df_sorted.iloc[-1]['Base Salary'] if 'Base Salary' in emp_df_sorted.columns else 0
    max_salary = emp_df_sorted['Total Compensation'].max()
    
    fig_timeline = go.Figure()
    
    # Create timeline with segments for each job
    for idx, row in emp_df_sorted.iterrows():
        # Get color for this company
        company_name = row['Company']
        color = company_colors.get(company_name, '#6b7280')  # default grey if not found
        
        # Build hover template with base + super breakdown
        base_salary = row.get('Base Salary', 0)
        super_amount = row.get('Super', 0)
        
        hover_text = f"<b>{row['Company']}</b><br>"
        hover_text += f"Type: {row['Type']}<br>"
        if base_salary > 0:
            hover_text += f"Base Salary: ${base_salary:,.2f}<br>"
        if super_amount > 0:
            hover_text += f"Super: ${super_amount:,.2f}<br>"
        hover_text += f"Total: ${row['Total Compensation']:,.2f}/year<br>"
        hover_text += f"Duration: {row['Duration (months)']:.1f} months"
        
        fig_timeline.add_trace(go.Scatter(
            x=[row['Date Started'], row['Date Ended'] if pd.notna(row['Date Ended']) else pd.Timestamp.now()],
            y=[row['Total Compensation'], row['Total Compensation']],
            mode='lines+markers',
            name=row['Company'],
            line=dict(color=color, width=4),
            marker=dict(size=10),
            hovertemplate=hover_text
        ))
    
    fig_timeline.update_layout(
        template='plotly_white',
        font=dict(family='Inter, sans-serif'),
        xaxis_title='Date',
        yaxis_title='Annualized Salary ($)',
        hovermode='closest',
        height=400,
        margin=dict(l=0, r=0, t=20, b=0),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hoverlabel=dict(
            bgcolor='white',
            font_size=13,
            font_family='Inter, sans-serif',
            font_color='black',
            bordercolor='black',
            namelength=0
        )
    )
    
    # Career Progression Bar Chart
    # Shows salary for each job with company name and role
    progression_companies = []
    progression_salaries = []
    progression_colors_list = []
    
    for idx, row in emp_df_sorted.iterrows():
        # X-axis label: Company name and role
        label = f"{row['Company']}<br>{row.get('Position', 'N/A')}"
        progression_companies.append(label)
        progression_salaries.append(row['Total Compensation'])
        progression_colors_list.append(company_colors.get(row['Company'], '#6b7280'))
    
    fig_progression = go.Figure(data=[
        go.Bar(
            x=progression_companies,
            y=progression_salaries,
            marker_color=progression_colors_list,
            text=[f"${sal:,.0f}" for sal in progression_salaries],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br>Salary: %{text}<extra></extra>'
        )
    ])
    
    fig_progression.update_layout(
        template='plotly_white',
        font=dict(family='Inter, sans-serif'),
        xaxis_title='Company & Role',
        yaxis_title='Salary ($)',
        height=450,
        margin=dict(l=0, r=0, t=20, b=0),
        hoverlabel=dict(
            bgcolor='white',
            font_size=13,
            font_family='Inter, sans-serif',
            font_color='black',
            bordercolor='black',
            namelength=0
        ),
        yaxis=dict(
            tickformat='$,.0f'
        )
    )
    
    # Business days worked by company
    company_days = emp_df_sorted.groupby('Company')['Business Days'].sum().sort_values(ascending=False).reset_index()
    
    # Use dynamically assigned company colors
    bar_colors = [company_colors.get(company, '#6b7280') for company in company_days['Company']]
    
    fig_days = go.Figure(data=[go.Bar(
        x=company_days['Company'],
        y=company_days['Business Days'],
        marker_color=bar_colors,
        text=company_days['Business Days'],
        textposition='outside',
        hovertemplate='<b>%{x}</b><br>Business Days: %{y:,.0f}<extra></extra>'
    )])
    
    fig_days.update_layout(
        template='plotly_white',
        font=dict(family='Inter, sans-serif'),
        xaxis_title='Company',
        yaxis_title='Business Days Worked',
        height=400,
        margin=dict(l=0, r=0, t=20, b=0),
        hoverlabel=dict(
            bgcolor='white',
            font_size=13,
            font_family='Inter, sans-serif',
            font_color='black',
            bordercolor='black',
            namelength=0
        )
    )
    
    # Create Current Annualized Salary card with glow effect
    current_salary_card = dmc.Paper(
        children=[
            dmc.Stack(
                children=[
                    dmc.Text("Current Annualized Salary", size="sm", fw=500, c="dimmed", tt="uppercase"),
                    dmc.Text(format_currency(current_salary), size="xl", fw=700, style={"fontSize": "32px"}),
                ],
                gap="xs"
            )
        ],
        p="lg",
        radius="md",
        withBorder=True,
        shadow="xl",
        style={
            "height": "100%",
            "boxShadow": "0 0 20px rgba(74, 158, 255, 0.3)",
            "border": "2px solid #4A9EFF"
        }
    )
    
    return dmc.Stack([
        dmc.Title("Employment History", order=2, mb="lg"),
        
        # Metrics
        dmc.Grid([
            dmc.GridCol(create_metric_card("Total Business Days Worked", f"{total_business_days:,}"), span=4),
            dmc.GridCol(current_salary_card, span=4),
            dmc.GridCol(create_metric_card("Highest Salary", format_currency(max_salary)), span=4),
        ], gutter="lg"),
        
        dmc.Divider(my="xl"),
        
        # Salary timeline
        dmc.Title("Annualized Salary Timeline", order=3, mb="md"),
        dmc.Paper(
            dcc.Graph(figure=fig_timeline, config={'displayModeBar': False}),
            p="md",
            radius="md",
            withBorder=True
        ),
        
        # Career Progression Waterfall
        dmc.Title("Career Progression", order=3, mb="md", mt="xl"),
        dmc.Text("See how your salary has changed with each job transition", c="dimmed", size="sm", mb="md"),
        dmc.Paper(
            dcc.Graph(figure=fig_progression, config={'displayModeBar': False}),
            p="md",
            radius="md",
            withBorder=True
        ),
        
        # Business days worked
        dmc.Title("Business Days Worked by Company", order=3, mb="md", mt="xl"),
        dmc.Paper(
            dcc.Graph(figure=fig_days, config={'displayModeBar': False}),
            p="md",
            radius="md",
            withBorder=True
        ),
    ], gap="lg")


def benchmarking_layout():
    """Benchmarking page comparing user's metrics to population"""
    # Get latest metrics
    latest_metrics = data_loader.get_latest_metrics()
    emp_df = data_loader.load_employment()
    
    # Get most recent job
    if not emp_df.empty:
        emp_df_sorted = emp_df.sort_values('Date Started', ascending=False)
        latest_job = emp_df_sorted.iloc[0]
        job_title = latest_job.get('Position', 'N/A')
        company = latest_job.get('Company', 'N/A')
        salary = latest_job.get('Total Compensation', 0)
    else:
        job_title = 'N/A'
        company = 'N/A'
        salary = 0
    
    net_worth = latest_metrics['net_worth']
    
    # Get superannuation value from Assets & Liabilities
    al_df = data_loader.load_assets_liabilities()
    latest_date = al_df['Date'].max()
    super_data = al_df[(al_df['Date'] == latest_date) & 
                       (al_df['Category'] == 'Asset') & 
                       (al_df['Type'].str.contains('Super', na=False))]
    super_value = super_data['Value'].sum() if not super_data.empty else 0
    
    # Calculate user age
    from datetime import datetime
    age = (datetime.now() - user_info['dob']).days // 365
    
    # Load benchmark data from Excel
    benchmark_path = 'data/benchmark.xlsx'
    super_bench = pd.read_excel(benchmark_path, sheet_name='Superannuation')
    networth_bench = pd.read_excel(benchmark_path, sheet_name='Net Worth')
    salary_bench = pd.read_excel(benchmark_path, sheet_name='Salary')
    
    # Helper function to find appropriate benchmark for age
    def get_super_benchmark(age):
        # Map age to age group
        if 18 <= age <= 24:
            row = super_bench[super_bench['Age Group'] == '18-24']
            age_group = '18-24'
        elif 25 <= age <= 29:
            row = super_bench[super_bench['Age Group'] == '25-29']
            age_group = '25-29'
        elif 30 <= age <= 34:
            row = super_bench[super_bench['Age Group'] == '30-34']
            age_group = '30-34'
        elif 35 <= age <= 39:
            row = super_bench[super_bench['Age Group'] == '35-39']
            age_group = '35-39'
        elif 40 <= age <= 44:
            row = super_bench[super_bench['Age Group'] == '40-44']
            age_group = '40-44'
        elif 45 <= age <= 49:
            row = super_bench[super_bench['Age Group'] == '45-49']
            age_group = '45-49'
        elif 50 <= age <= 54:
            row = super_bench[super_bench['Age Group'] == '50-54']
            age_group = '50-54'
        elif 55 <= age <= 59:
            row = super_bench[super_bench['Age Group'] == '55-59']
            age_group = '55-59'
        elif 60 <= age <= 64:
            row = super_bench[super_bench['Age Group'] == '60-64']
            age_group = '60-64'
        else:
            row = super_bench[super_bench['Age Group'] == '65-69']
            age_group = '65-69'
        return row['Median Balance ($)'].values[0] if not row.empty else 0, age_group
    
    def get_networth_benchmark(age):
        if age <= 40:
            row = networth_bench[networth_bench['Age of Household Reference Person'] == '25-40']
            age_group = '25-40'
        elif age <= 64:
            row = networth_bench[networth_bench['Age of Household Reference Person'] == '41-64']
            age_group = '41-64'
        else:
            row = networth_bench[networth_bench['Age of Household Reference Person'] == '65+']
            age_group = '65+'
        return (row['Median Net Worth ($)'].values[0] if not row.empty else 0,
                row['Top 25% Net Worth ($)'].values[0] if not row.empty else 0,
                row['Top 1% Net Worth ($)'].values[0] if not row.empty else 0,
                age_group)
    
    def get_salary_benchmark(age):
        if 15 <= age <= 24:
            row = salary_bench[salary_bench['Age Group'] == '15-24']
            age_group = '15-24'
        elif 25 <= age <= 34:
            row = salary_bench[salary_bench['Age Group'] == '25-34']
            age_group = '25-34'
        elif 35 <= age <= 44:
            row = salary_bench[salary_bench['Age Group'] == '35-44']
            age_group = '35-44'
        elif 45 <= age <= 54:
            row = salary_bench[salary_bench['Age Group'] == '45-54']
            age_group = '45-54'
        else:
            row = salary_bench[salary_bench['Age Group'] == '55-64']
            age_group = '55-64'
        return row['Median Annual Income ($)'].values[0] if not row.empty else 0, age_group
    
    # Get benchmarks
    super_median, super_age_group = get_super_benchmark(age)
    nw_median, nw_top25, nw_top1, nw_age_group = get_networth_benchmark(age)
    salary_median, salary_age_group = get_salary_benchmark(age)
    
    # Calculate % above/below median
    super_pct = ((super_value - super_median) / super_median * 100) if super_median > 0 else 0
    nw_pct = ((net_worth - nw_median) / nw_median * 100) if nw_median > 0 else 0
    salary_pct = ((salary - salary_median) / salary_median * 100) if salary_median > 0 else 0
    
    # Approximate percentile for net worth based on available data
    def approximate_percentile(value, median, top25, top1):
        if value >= top1:
            return "Top 1% (Approx.)"
        elif value >= top25:
            # Linear interpolation between top 25% and top 1%
            pct = 25 - ((value - top25) / (top1 - top25) * 24)
            return f"Top {max(1, int(pct))}% (Approx.)"
        elif value >= median:
            # Between median (50th) and top 25%
            pct = 50 - ((value - median) / (top25 - median) * 25)
            return f"Top {max(25, int(pct))}% (Approx.)"
        else:
            # Below median
            pct = 50 + ((median - value) / median * 50)
            return f"Bottom {min(99, int(pct))}% (Approx.)"
    
    nw_percentile = approximate_percentile(net_worth, nw_median, nw_top25, nw_top1)
    
    # Simple percentile estimate for super and salary (no top % data available)
    def simple_percentile(value, median):
        if value >= median:
            return "Above Median"
        else:
            return "Below Median"
    
    super_percentile = simple_percentile(super_value, super_median)
    salary_percentile = simple_percentile(salary, salary_median)
    
    # Format subtext for cards
    super_subtext = f"{'+' if super_pct >= 0 else ''}{super_pct:.1f}% vs median"
    nw_subtext = f"{'+' if nw_pct >= 0 else ''}{nw_pct:.1f}% vs median"
    salary_subtext = f"{job_title} at {company}"
    
    # Determine color for Net Worth and Super based on performance
    nw_change_color = "green" if nw_pct >= 0 else "red"
    super_change_color = "green" if super_pct >= 0 else "red"
    
    return dmc.Stack([
        dmc.Title("Benchmarking", order=2, mb="lg"),
        
        # Top Summary Cards - Net Worth/Super show green/red, Salary shows blue
        dmc.Grid([
            dmc.GridCol(
                create_metric_card(
                    "Net Worth",
                    format_currency(net_worth),
                    nw_subtext,
                    change_color_override=nw_change_color
                ),
                span=4
            ),
            dmc.GridCol(
                create_metric_card(
                    "Superannuation",
                    format_currency(super_value),
                    super_subtext,
                    change_color_override=super_change_color
                ),
                span=4
            ),
            dmc.GridCol(
                create_metric_card(
                    "Salary",
                    format_currency(salary),
                    salary_subtext,
                    change_color_override="blue"
                ),
                span=4
            ),
        ], gutter="lg"),
        
        dmc.Divider(my="xl"),
        
        # Comparison Table
        dmc.Title("How You Compare", order=3, mb="md"),
        dmc.Paper([
            dmc.Table([
                dmc.TableThead([
                    dmc.TableTr([
                        dmc.TableTh("Metric"),
                        dmc.TableTh("Your Value"),
                        dmc.TableTh("Age Group"),
                        dmc.TableTh("Median"),
                        dmc.TableTh("% Above/Below"),
                        dmc.TableTh("Estimated Position"),
                    ])
                ]),
                dmc.TableTbody([
                    dmc.TableTr([
                        dmc.TableTd("Net Worth"),
                        dmc.TableTd(format_currency(net_worth), style={"fontWeight": "600"}),
                        dmc.TableTd(nw_age_group, style={"color": "dimmed"}),
                        dmc.TableTd(format_currency(nw_median)),
                        dmc.TableTd(
                            f"{'+' if nw_pct >= 0 else ''}{nw_pct:.1f}%",
                            style={"color": "#10B981" if nw_pct >= 0 else "#EF4444", "fontWeight": "600"}
                        ),
                        dmc.TableTd(nw_percentile, style={"color": "#10B981" if nw_pct >= 0 else "#EF4444", "fontWeight": "600"}),
                    ]),
                    dmc.TableTr([
                        dmc.TableTd("Salary"),
                        dmc.TableTd(format_currency(salary), style={"fontWeight": "600"}),
                        dmc.TableTd(salary_age_group, style={"color": "dimmed"}),
                        dmc.TableTd(format_currency(salary_median)),
                        dmc.TableTd(
                            f"{'+' if salary_pct >= 0 else ''}{salary_pct:.1f}%",
                            style={"color": "#10B981" if salary_pct >= 0 else "#EF4444", "fontWeight": "600"}
                        ),
                        dmc.TableTd(salary_percentile, style={"color": "#10B981" if salary_pct >= 0 else "#EF4444", "fontWeight": "600"}),
                    ]),
                    dmc.TableTr([
                        dmc.TableTd("Superannuation"),
                        dmc.TableTd(format_currency(super_value), style={"fontWeight": "600"}),
                        dmc.TableTd(super_age_group, style={"color": "dimmed"}),
                        dmc.TableTd(format_currency(super_median)),
                        dmc.TableTd(
                            f"{'+' if super_pct >= 0 else ''}{super_pct:.1f}%",
                            style={"color": "#10B981" if super_pct >= 0 else "#EF4444", "fontWeight": "600"}
                        ),
                        dmc.TableTd(super_percentile, style={"color": "#10B981" if super_pct >= 0 else "#EF4444", "fontWeight": "600"}),
                    ]),
                ])
            ], striped=True, highlightOnHover=True)
        ], p="md", radius="md", withBorder=True),
        
        # Benchmark Data Accordion
        dmc.Accordion(
            children=[
                dmc.AccordionItem(
                    children=[
                        dmc.AccordionControl("View Benchmark Data"),
                        dmc.AccordionPanel([
                            # Net Worth Benchmark Table (Full Width)
                            dmc.Title("Net Worth Benchmark (Grattan Institute / ABS, 2024)", order=4, size="md", mb="sm", mt="sm"),
                            dmc.Table([
                                dmc.TableThead([
                                    dmc.TableTr([
                                        dmc.TableTh("Age Group"),
                                        dmc.TableTh("Median Net Worth"),
                                        dmc.TableTh("Top 25%"),
                                        dmc.TableTh("Top 1%"),
                                    ])
                                ]),
                                dmc.TableTbody([
                                    dmc.TableTr([
                                        dmc.TableTd(row['Age of Household Reference Person']),
                                        dmc.TableTd(format_currency(row['Median Net Worth ($)'])),
                                        dmc.TableTd(format_currency(row['Top 25% Net Worth ($)'])),
                                        dmc.TableTd(format_currency(row['Top 1% Net Worth ($)'])),
                                    ]) for _, row in networth_bench.iterrows()
                                ])
                            ], striped=True),
                            
                            # Grid with Salary and Superannuation side by side
                            dmc.Grid([
                                # Salary Benchmark Table
                                dmc.GridCol([
                                    dmc.Title("Salary Benchmark (ABS, 2023)", order=4, size="md", mb="sm", mt="lg"),
                                    dmc.Table([
                                        dmc.TableThead([
                                            dmc.TableTr([
                                                dmc.TableTh("Age Group"),
                                                dmc.TableTh("Median Income"),
                                            ])
                                        ]),
                                        dmc.TableTbody([
                                            dmc.TableTr([
                                                dmc.TableTd(row['Age Group']),
                                                dmc.TableTd(format_currency(row['Median Annual Income ($)'])),
                                            ]) for _, row in salary_bench.iterrows()
                                        ])
                                    ], striped=True),
                                ], span=6),
                                
                                # Superannuation Benchmark Table
                                dmc.GridCol([
                                    dmc.Title("Superannuation Benchmark (ASFA, 2024)", order=4, size="md", mb="sm", mt="lg"),
                                    dmc.Table([
                                        dmc.TableThead([
                                            dmc.TableTr([
                                                dmc.TableTh("Age Group"),
                                                dmc.TableTh("Median Balance"),
                                            ])
                                        ]),
                                        dmc.TableTbody([
                                            dmc.TableTr([
                                                dmc.TableTd(row['Age Group']),
                                                dmc.TableTd(format_currency(row['Median Balance ($)'])),
                                            ]) for _, row in super_bench.iterrows()
                                        ])
                                    ], striped=True),
                                ], span=6),
                            ], gutter="lg"),
                        ])
                    ],
                    value="benchmark-data"
                )
            ],
            mt="lg"
        ),
    ], gap="lg")


def calculators_layout():
    """Financial calculators page"""
    # Get most recent job for salary
    emp_df = data_loader.load_employment()
    default_salary = 75000  # fallback
    
    if not emp_df.empty:
        emp_df_sorted = emp_df.sort_values('Date Started', ascending=False)
        latest_job = emp_df_sorted.iloc[0]
        default_salary = latest_job.get('Total Compensation', 75000)
    
    # Get current portfolio value
    latest_metrics = data_loader.get_latest_metrics()
    current_portfolio = latest_metrics.get('total_assets', 0)
    
    # Calculate user age
    from datetime import datetime
    current_age = (datetime.now() - user_info['dob']).days // 365
    
    return dmc.Stack([
        dmc.Title("Financial Calculators", order=2, mb="lg"),
        
        # Tax Calculator Section
        dmc.Title("Tax & Superannuation Calculator (2025-26)", order=3, mb="md"),
        dmc.Paper([
            dmc.Stack([
                dmc.Text("Calculate your estimated income tax and superannuation based on Australian tax rates.", c="dimmed", size="sm"),
                
                dmc.Grid([
                    dmc.GridCol([
                        dmc.NumberInput(
                            id="tax-base-salary-input",
                            label="Annual Base Salary ($)",
                            value=default_salary,
                            min=0,
                            step=1000,
                            style={"width": "100%"}
                        ),
                    ], span=4),
                    dmc.GridCol([
                        dmc.NumberInput(
                            id="tax-bonus-input",
                            label="Bonus ($)",
                            value=0,
                            min=0,
                            step=1000,
                            style={"width": "100%"}
                        ),
                    ], span=4),
                    dmc.GridCol([
                        html.Div([
                            dmc.Checkbox(
                                id="medicare-levy-checkbox",
                                label="Include Medicare Levy (2%)",
                                checked=True
                            )
                        ], style={"display": "flex", "alignItems": "center", "height": "100%", "paddingTop": "28px"})
                    ], span=4),
                ]),
                
                dmc.Button("Calculate Tax", id="calculate-tax", mt="md"),
                
                html.Div(id="tax-results", children=[
                    dmc.Stack([
                        dmc.Alert(
                            "Enter your base salary and click Calculate to see your tax and super breakdown",
                            color="blue",
                            title="Ready to calculate"
                        ),
                        dmc.Text(
                            "Last updated 27 Dec 2025 (2025-26 Tax Tables, 12% Super Guarantee)",
                            c="dimmed",
                            size="xs",
                            ta="center",
                            mt="xs"
                        )
                    ], gap="xs")
                ], style={"marginTop": "20px"})
            ], gap="md")
        ], p="lg", radius="md", withBorder=True, shadow="sm"),
        
        dmc.Divider(my="xl"),
        
        # True Cost Calculator Section
        dmc.Title("True Cost Calculator", order=3, mb="md"),
        dmc.Paper([
            dmc.Stack([
                dmc.Text("Understand the real cost of your purchases (calculations based on pre-tax income)", c="dimmed", size="sm"),
                
                dmc.Grid([
                    dmc.GridCol([
                        dmc.NumberInput(
                            id="purchase-price-input",
                            label="Purchase Price ($)",
                            placeholder="Enter amount",
                            value=0,
                            min=0,
                            step=1,
                            style={"width": "100%"}
                        ),
                    ], span=6),
                    dmc.GridCol([
                        dmc.NumberInput(
                            id="salary-input",
                            label="Annual Base Salary ($)",
                            value=default_salary,
                            min=0,
                            step=1000,
                            style={"width": "100%"}
                        ),
                    ], span=6),
                ]),
                
                dmc.Button("Calculate", id="calculate-true-cost", mt="md"),
                
                html.Div(id="true-cost-results", children=[
                    dmc.Alert(
                        "Enter a purchase price and click Calculate to see the true cost analysis",
                        color="blue",
                        title="Ready to analyze"
                    )
                ], style={"marginTop": "20px"})
            ], gap="md")
        ], p="lg", radius="md", withBorder=True, shadow="sm"),
        
        dmc.Divider(my="xl"),
        
        # FIRE Calculator Section  
        dmc.Title("FIRE Calculator", order=3, mb="md"),
        dmc.Paper([
            dmc.Stack([
                dmc.Text("Calculate when you can achieve Financial Independence and Retire Early", c="dimmed", size="sm"),
                
                dmc.Grid([
                    dmc.GridCol([
                        dmc.NumberInput(
                            id="current-age-input",
                            label="Current Age",
                            value=current_age,
                            min=18,
                            max=100,
                        ),
                    ], span=4),
                    dmc.GridCol([
                        dmc.NumberInput(
                            id="retirement-age-input",
                            label="Target Retirement Age",
                            value=65,
                            min=18,
                            max=100,
                        ),
                    ], span=4),
                    dmc.GridCol([
                        dmc.NumberInput(
                            id="portfolio-value-input",
                            label="Current Portfolio ($)",
                            value=current_portfolio,
                            min=0,
                            step=1000,
                        ),
                    ], span=4),
                ]),
                
                dmc.Grid([
                    dmc.GridCol([
                        dmc.NumberInput(
                            id="annual-contribution-input",
                            label="Annual Contribution ($)",
                            value=20000,
                            min=0,
                            step=1000,
                        ),
                    ], span=4),
                    dmc.GridCol([
                        dmc.NumberInput(
                            id="target-spend-input",
                            label="Target Annual Spend ($)",
                            value=60000,
                            min=0,
                            step=1000,
                        ),
                    ], span=4),
                    dmc.GridCol([
                        dmc.Select(
                            id="fire-mode-select",
                            label="FIRE Mode",
                            data=[
                                {"value": "custom", "label": "Custom"},
                                {"value": "lean", "label": "Lean FIRE ($40k/yr)"},
                                {"value": "fat", "label": "Fat FIRE ($100k/yr)"},
                                {"value": "coast", "label": "Coast FIRE"},
                            ],
                            value="custom",
                        ),
                    ], span=4),
                ]),
                
                dmc.Grid([
                    dmc.GridCol([
                        dmc.NumberInput(
                            id="inflation-rate-input",
                            label="Inflation Rate (%)",
                            value=3,
                            min=0,
                            max=20,
                            step=0.1,
                        ),
                    ], span=6),
                    dmc.GridCol([
                        dmc.NumberInput(
                            id="investment-return-input",
                            label="Investment Return (%)",
                            value=7,
                            min=0,
                            max=20,
                            step=0.1,
                        ),
                    ], span=6),
                ]),
                
                dmc.Button("Calculate FIRE", id="calculate-fire", mt="md"),
                
                html.Div(id="fire-mode-explanation", style={"marginTop": "15px", "marginBottom": "15px"}),
                
                html.Div(id="fire-results", children=[
                    dmc.Alert(
                        "Configure your inputs and click Calculate to see when you can achieve FIRE",
                        color="blue",
                        title="Ready to plan"
                    )
                ], style={"marginTop": "20px"})
            ], gap="md")
        ], p="lg", radius="md", withBorder=True, shadow="sm"),
        
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
    nav_items = ["dashboard", "investments", "employment", "benchmarking", "calculators"]
    active_states = [page == current_page for page in nav_items]
    
    # Get page content
    page_content = dashboard_layout()
    if current_page == "investments":
        page_content = investments_layout()
    elif current_page == "employment":
        page_content = employment_layout()
    elif current_page == "benchmarking":
        page_content = benchmarking_layout()
    elif current_page == "calculators":
        page_content = calculators_layout()
    
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

# Callback for Tax Calculator
@callback(
    Output("tax-results", "children"),
    [Input("calculate-tax", "n_clicks")],
    [Input("tax-base-salary-input", "value"),
     Input("tax-bonus-input", "value"),
     Input("medicare-levy-checkbox", "checked")]
)
def calculate_tax(n_clicks, base_salary, bonus, include_medicare):
    """Calculate Australian income tax and superannuation for 2025-26"""
    # Combine base salary and bonus
    total_salary = (base_salary or 0) + (bonus or 0)
    
    if not n_clicks or total_salary == 0:
        return dmc.Stack([
            dmc.Alert(
                "Enter your base salary and click Calculate to see your tax and super breakdown",
                color="blue",
                title="Ready to calculate"
            ),
            dmc.Text(
                "Last updated 27 Dec 2025 (2025-26 Tax Tables, 12% Super Guarantee)",
                c="dimmed",
                size="xs",
                ta="center",
                mt="xs"
            )
        ], gap="xs")
    
    # Load tax brackets from Excel (dynamically every time)
    tax_table_df = pd.read_excel('data/25_26_tax.xlsx', sheet_name='Sheet1')
    
    # Load Medicare Levy Surcharge thresholds from Excel (dynamically every time)
    mls_df = pd.read_excel('data/medicare_levy.xlsx', sheet_name='Sheet1', header=1)
    
    # Superannuation calculation (12% super guarantee)
    super_rate = 0.12
    employer_super = total_salary * super_rate
    
    # Super contributions tax (15%)
    super_tax = employer_super * 0.15
    after_tax_super = employer_super - super_tax
    
    # Australian tax brackets for 2025-26 (on salary only, not super)
    income = total_salary
    tax = 0
    
    if income <= 18200:
        tax = 0
    elif income <= 45000:
        tax = (income - 18200) * 0.16
    elif income <= 135000:
        tax = 4288 + (income - 45000) * 0.30
    elif income <= 190000:
        tax = 31288 + (income - 135000) * 0.37
    else:
        tax = 51638 + (income - 190000) * 0.45
    
    # Standard Medicare levy (2% of taxable income for everyone)
    medicare_levy = income * 0.02 if include_medicare else 0
    
    # Medicare Levy Surcharge (MLS) - additional charge based on income thresholds
    # Only applies if income is above the base tier
    mls_rate = 0
    mls_tier = "Base tier (No surcharge)"
    if income > 158000:
        mls_rate = 0.015
        mls_tier = "Tier 3"
    elif income > 118000:
        mls_rate = 0.0125
        mls_tier = "Tier 2"
    elif income > 101000:
        mls_rate = 0.01
        mls_tier = "Tier 1"
    
    medicare_levy_surcharge = income * mls_rate if include_medicare else 0
    
    # Total Medicare costs
    total_medicare = medicare_levy + medicare_levy_surcharge
    
    # Total tax on salary
    total_salary_tax = tax + total_medicare
    
    # After-tax income
    after_tax_income = income - total_salary_tax
    
    # Effective tax rate
    effective_rate = (total_salary_tax / income * 100) if income > 0 else 0
    
    # Marginal tax rate
    if income <= 18200:
        marginal_rate = 0
    elif income <= 45000:
        marginal_rate = 16
    elif income <= 135000:
        marginal_rate = 30
    elif income <= 190000:
        marginal_rate = 37
    else:
        marginal_rate = 45
    
    # Add Medicare levy to marginal rate if included
    if include_medicare:
        marginal_rate += 2
        if mls_rate > 0:
            marginal_rate += (mls_rate * 100)
    
    return dmc.Stack([
        # Salary Row
        dmc.Title("Salary Breakdown", order=4, size="sm", mb="sm"),
        dmc.Grid([
            dmc.GridCol(
                create_metric_card(
                    "Gross Salary",
                    format_currency(income),
                    "Base + bonuses",
                    change_color_override="blue"
                ),
                span=3
            ),
            dmc.GridCol(
                create_metric_card(
                    "Income Tax",
                    format_currency(tax),
                    f"Marginal rate: {marginal_rate - (2 if include_medicare else 0) - (mls_rate * 100 if include_medicare else 0):.0f}%",
                    change_color_override="blue"
                ),
                span=2
            ),
            dmc.GridCol(
                create_metric_card(
                    "Medicare Levy",
                    format_currency(total_medicare),
                    f"2% + {mls_rate*100:.2f}% surcharge" if include_medicare and mls_rate > 0 else ("2%" if include_medicare else "Not included"),
                    change_color_override="blue"
                ),
                span=2
            ),
            dmc.GridCol(
                create_metric_card(
                    "Total Tax",
                    format_currency(total_salary_tax),
                    f"Effective: {effective_rate:.1f}%",
                    change_color_override="blue"
                ),
                span=2
            ),
            dmc.GridCol(
                dmc.Paper(
                    children=[
                        dmc.Stack(
                            children=[
                                dmc.Text("After-Tax Income", size="sm", fw=500, c="dimmed", tt="uppercase"),
                                dmc.Text(format_currency(after_tax_income), size="xl", fw=700, style={"fontSize": "32px"}),
                                dmc.Text(
                                    f"Take home: {(after_tax_income/income*100):.1f}%",
                                    size="sm",
                                    fw=500,
                                    c="blue"
                                )
                            ],
                            gap="xs"
                        )
                    ],
                    p="lg",
                    radius="md",
                    withBorder=True,
                    shadow="xl",
                    style={
                        "height": "100%",
                        "boxShadow": "0 0 20px rgba(74, 158, 255, 0.3)",
                        "border": "2px solid #4A9EFF"
                    }
                ),
                span=3
            ),
        ], gutter="md"),
        
        # Superannuation Row
        dmc.Title("Superannuation Breakdown", order=4, size="sm", mb="sm", mt="lg"),
        dmc.Grid([
            dmc.GridCol(
                create_metric_card(
                    "Employer Contribution",
                    format_currency(employer_super),
                    f"12% of {format_currency(income)}",
                    change_color_override="blue"
                ),
                span=3
            ),
            dmc.GridCol(
                create_metric_card(
                    "Super Contributions Tax",
                    format_currency(super_tax),
                    "15% of contribution",
                    change_color_override="blue"
                ),
                span=3
            ),
            dmc.GridCol(
                dmc.Paper(
                    children=[
                        dmc.Stack(
                            children=[
                                dmc.Text("After-Tax Super", size="sm", fw=500, c="dimmed", tt="uppercase"),
                                dmc.Text(format_currency(after_tax_super), size="xl", fw=700, style={"fontSize": "32px"}),
                                dmc.Text(
                                    f"Net: {(after_tax_super/employer_super*100):.1f}%",
                                    size="sm",
                                    fw=500,
                                    c="blue"
                                )
                            ],
                            gap="xs"
                        )
                    ],
                    p="lg",
                    radius="md",
                    withBorder=True,
                    shadow="xl",
                    style={
                        "height": "100%",
                        "boxShadow": "0 0 20px rgba(74, 158, 255, 0.3)",
                        "border": "2px solid #4A9EFF"
                    }
                ),
                span=3
            ),
        ], gutter="md"),
        
        # Tax Tables Accordion
        dmc.Accordion(
            children=[
                dmc.AccordionItem(
                    children=[
                        dmc.AccordionControl("View Tax Tables"),
                        dmc.AccordionPanel([
                            dmc.Title("2025-26 Resident Tax Rates", order=4, size="md", mb="sm", mt="sm"),
                            dmc.Table([
                                dmc.TableThead([
                                    dmc.TableTr([
                                        dmc.TableTh("Taxable Income"),
                                        dmc.TableTh("Tax on This Income"),
                                    ])
                                ]),
                                dmc.TableTbody([
                                    dmc.TableTr([
                                        dmc.TableTd("$0 – $18,200"),
                                        dmc.TableTd("Nil"),
                                    ]),
                                    dmc.TableTr([
                                        dmc.TableTd("$18,201 – $45,000"),
                                        dmc.TableTd("16c for each $1 over $18,200"),
                                    ]),
                                    dmc.TableTr([
                                        dmc.TableTd("$45,001 – $135,000"),
                                        dmc.TableTd("$4,288 plus 30c for each $1 over $45,000"),
                                    ]),
                                    dmc.TableTr([
                                        dmc.TableTd("$135,001 – $190,000"),
                                        dmc.TableTd("$31,288 plus 37c for each $1 over $135,000"),
                                    ]),
                                    dmc.TableTr([
                                        dmc.TableTd("$190,001 and over"),
                                        dmc.TableTd("$51,638 plus 45c for each $1 over $190,000"),
                                    ]),
                                ])
                            ], striped=True),
                            
                            dmc.Title("Medicare Levy & Surcharge", order=4, size="md", mb="sm", mt="lg"),
                            dmc.Table([
                                dmc.TableThead([
                                    dmc.TableTr([
                                        dmc.TableTh("Income Threshold"),
                                        dmc.TableTh("Medicare Levy"),
                                        dmc.TableTh("Surcharge Rate"),
                                    ])
                                ]),
                                dmc.TableTbody([
                                    dmc.TableTr([
                                        dmc.TableTd("All incomes"),
                                        dmc.TableTd("2%"),
                                        dmc.TableTd("-"),
                                    ]),
                                    dmc.TableTr([
                                        dmc.TableTd("$101,000 or less"),
                                        dmc.TableTd("-"),
                                        dmc.TableTd("0% (No surcharge)"),
                                    ]),
                                    dmc.TableTr([
                                        dmc.TableTd("$101,001 – $118,000"),
                                        dmc.TableTd("-"),
                                        dmc.TableTd("1.0%"),
                                    ]),
                                    dmc.TableTr([
                                        dmc.TableTd("$118,001 – $158,000"),
                                        dmc.TableTd("-"),
                                        dmc.TableTd("1.25%"),
                                    ]),
                                    dmc.TableTr([
                                        dmc.TableTd("$158,001 or more"),
                                        dmc.TableTd("-"),
                                        dmc.TableTd("1.5%"),
                                    ]),
                                ])
                            ], striped=True),
                            
                            dmc.Title("Superannuation", order=4, size="md", mb="sm", mt="lg"),
                            dmc.Table([
                                dmc.TableThead([
                                    dmc.TableTr([
                                        dmc.TableTh("Item"),
                                        dmc.TableTh("Rate"),
                                    ])
                                ]),
                                dmc.TableTbody([
                                    dmc.TableTr([
                                        dmc.TableTd("Superannuation Guarantee"),
                                        dmc.TableTd("12% of ordinary time earnings"),
                                    ]),
                                    dmc.TableTr([
                                        dmc.TableTd("Super Contributions Tax"),
                                        dmc.TableTd("15% of concessional contributions"),
                                    ]),
                                ])
                            ], striped=True),
                        ])
                    ],
                    value="tax-tables"
                )
            ],
            mt="lg"
        ),
    ], gap="md")
    
    # Superannuation calculation (12% super guarantee)
    super_rate = 0.12
    employer_super = base_salary * super_rate
    
    # Super contributions tax (15%)
    super_tax = employer_super * 0.15
    after_tax_super = employer_super - super_tax
    
    # Australian tax brackets for 2025-26 (on salary only, not super)
    income = base_salary
    tax = 0
    
    if income <= 18200:
        tax = 0
    elif income <= 45000:
        tax = (income - 18200) * 0.16
    elif income <= 135000:
        tax = 4288 + (income - 45000) * 0.30
    elif income <= 190000:
        tax = 31288 + (income - 135000) * 0.37
    else:
        tax = 51638 + (income - 190000) * 0.45
    
    # Standard Medicare levy (2% of taxable income for everyone above threshold)
    # The standard Medicare levy is 2% for most people
    medicare_levy = income * 0.02 if include_medicare else 0
    
    # Medicare Levy Surcharge (MLS) - additional charge based on income thresholds
    # Only applies if income is above the base tier
    mls_rate = 0
    mls_tier = "Base tier (No surcharge)"
    if income > 158000:
        mls_rate = 0.015
        mls_tier = "Tier 3"
    elif income > 118000:
        mls_rate = 0.0125
        mls_tier = "Tier 2"
    elif income > 101000:
        mls_rate = 0.01
        mls_tier = "Tier 1"
    
    medicare_levy_surcharge = income * mls_rate if include_medicare else 0
    
    # Total Medicare costs
    total_medicare = medicare_levy + medicare_levy_surcharge
    
    # Total tax on salary
    total_salary_tax = tax + total_medicare
    
    # After-tax income
    after_tax_income = income - total_salary_tax
    
    # Effective tax rate
    effective_rate = (total_salary_tax / income * 100) if income > 0 else 0
    
    # Marginal tax rate
    if income <= 18200:
        marginal_rate = 0
    elif income <= 45000:
        marginal_rate = 16
    elif income <= 135000:
        marginal_rate = 30
    elif income <= 190000:
        marginal_rate = 37
    else:
        marginal_rate = 45
    
    # Add Medicare levy to marginal rate if included
    if include_medicare:
        marginal_rate += 2
        if mls_rate > 0:
            marginal_rate += (mls_rate * 100)
    
    return dmc.Stack([
        # Salary Row
        dmc.Title("Salary Breakdown", order=4, size="sm", mb="sm"),
        dmc.Grid([
            dmc.GridCol(
                create_metric_card(
                    "Gross Salary",
                    format_currency(income),
                    "Base + bonuses",
                    change_color_override="blue"
                ),
                span=3
            ),
            dmc.GridCol(
                create_metric_card(
                    "Income Tax",
                    format_currency(tax),
                    f"Marginal rate: {marginal_rate - (2 if include_medicare else 0) - (mls_rate * 100 if include_medicare else 0):.0f}%",
                    change_color_override="blue"
                ),
                span=2
            ),
            dmc.GridCol(
                create_metric_card(
                    "Medicare Levy",
                    format_currency(total_medicare),
                    f"2% + {mls_rate*100:.2f}% surcharge" if include_medicare and mls_rate > 0 else ("2%" if include_medicare else "Not included"),
                    change_color_override="blue"
                ),
                span=2
            ),
            dmc.GridCol(
                create_metric_card(
                    "Total Tax",
                    format_currency(total_salary_tax),
                    f"Effective: {effective_rate:.1f}%",
                    change_color_override="blue"
                ),
                span=2
            ),
            dmc.GridCol(
                dmc.Paper(
                    children=[
                        dmc.Stack(
                            children=[
                                dmc.Text("After-Tax Income", size="sm", fw=500, c="dimmed", tt="uppercase"),
                                dmc.Text(format_currency(after_tax_income), size="xl", fw=700, style={"fontSize": "32px"}),
                                dmc.Text(
                                    f"Take home: {(after_tax_income/income*100):.1f}%",
                                    size="sm",
                                    fw=500,
                                    c="blue"
                                )
                            ],
                            gap="xs"
                        )
                    ],
                    p="lg",
                    radius="md",
                    withBorder=True,
                    shadow="xl",
                    style={
                        "height": "100%",
                        "boxShadow": "0 0 20px rgba(74, 158, 255, 0.3)",
                        "border": "2px solid #4A9EFF"
                    }
                ),
                span=3
            ),
        ], gutter="md"),
        
        # Superannuation Row
        dmc.Title("Superannuation Breakdown", order=4, size="sm", mb="sm", mt="lg"),
        dmc.Grid([
            dmc.GridCol(
                create_metric_card(
                    "Employer Contribution",
                    format_currency(employer_super),
                    f"12% of {format_currency(income)}",
                    change_color_override="blue"
                ),
                span=3
            ),
            dmc.GridCol(
                create_metric_card(
                    "Super Contributions Tax",
                    format_currency(super_tax),
                    "15% of contribution",
                    change_color_override="blue"
                ),
                span=3
            ),
            dmc.GridCol(
                dmc.Paper(
                    children=[
                        dmc.Stack(
                            children=[
                                dmc.Text("After-Tax Super", size="sm", fw=500, c="dimmed", tt="uppercase"),
                                dmc.Text(format_currency(after_tax_super), size="xl", fw=700, style={"fontSize": "32px"}),
                                dmc.Text(
                                    f"Net: {(after_tax_super/employer_super*100):.1f}%",
                                    size="sm",
                                    fw=500,
                                    c="blue"
                                )
                            ],
                            gap="xs"
                        )
                    ],
                    p="lg",
                    radius="md",
                    withBorder=True,
                    shadow="xl",
                    style={
                        "height": "100%",
                        "boxShadow": "0 0 20px rgba(74, 158, 255, 0.3)",
                        "border": "2px solid #4A9EFF"
                    }
                ),
                span=3
            ),
        ], gutter="md"),
        
        # Tax Tables Accordion
        dmc.Accordion(
            children=[
                dmc.AccordionItem(
                    children=[
                        dmc.AccordionControl("View Tax Tables"),
                        dmc.AccordionPanel([
                            dmc.Title("2025-26 Resident Tax Rates", order=4, size="md", mb="sm", mt="sm"),
                            dmc.Table([
                                dmc.TableThead([
                                    dmc.TableTr([
                                        dmc.TableTh("Taxable Income"),
                                        dmc.TableTh("Tax on This Income"),
                                    ])
                                ]),
                                dmc.TableTbody([
                                    dmc.TableTr([
                                        dmc.TableTd("$0 – $18,200"),
                                        dmc.TableTd("Nil"),
                                    ]),
                                    dmc.TableTr([
                                        dmc.TableTd("$18,201 – $45,000"),
                                        dmc.TableTd("16c for each $1 over $18,200"),
                                    ]),
                                    dmc.TableTr([
                                        dmc.TableTd("$45,001 – $135,000"),
                                        dmc.TableTd("$4,288 plus 30c for each $1 over $45,000"),
                                    ]),
                                    dmc.TableTr([
                                        dmc.TableTd("$135,001 – $190,000"),
                                        dmc.TableTd("$31,288 plus 37c for each $1 over $135,000"),
                                    ]),
                                    dmc.TableTr([
                                        dmc.TableTd("$190,001 and over"),
                                        dmc.TableTd("$51,638 plus 45c for each $1 over $190,000"),
                                    ]),
                                ])
                            ], striped=True),
                            
                            dmc.Title("Medicare Levy & Surcharge", order=4, size="md", mb="sm", mt="lg"),
                            dmc.Table([
                                dmc.TableThead([
                                    dmc.TableTr([
                                        dmc.TableTh("Income Threshold"),
                                        dmc.TableTh("Medicare Levy"),
                                        dmc.TableTh("Surcharge Rate"),
                                    ])
                                ]),
                                dmc.TableTbody([
                                    dmc.TableTr([
                                        dmc.TableTd("All incomes"),
                                        dmc.TableTd("2%"),
                                        dmc.TableTd("-"),
                                    ]),
                                    dmc.TableTr([
                                        dmc.TableTd("$101,000 or less"),
                                        dmc.TableTd("-"),
                                        dmc.TableTd("0% (No surcharge)"),
                                    ]),
                                    dmc.TableTr([
                                        dmc.TableTd("$101,001 – $118,000"),
                                        dmc.TableTd("-"),
                                        dmc.TableTd("1.0%"),
                                    ]),
                                    dmc.TableTr([
                                        dmc.TableTd("$118,001 – $158,000"),
                                        dmc.TableTd("-"),
                                        dmc.TableTd("1.25%"),
                                    ]),
                                    dmc.TableTr([
                                        dmc.TableTd("$158,001 or more"),
                                        dmc.TableTd("-"),
                                        dmc.TableTd("1.5%"),
                                    ]),
                                ])
                            ], striped=True),
                            
                            dmc.Title("Superannuation", order=4, size="md", mb="sm", mt="lg"),
                            dmc.Table([
                                dmc.TableThead([
                                    dmc.TableTr([
                                        dmc.TableTh("Item"),
                                        dmc.TableTh("Rate"),
                                    ])
                                ]),
                                dmc.TableTbody([
                                    dmc.TableTr([
                                        dmc.TableTd("Superannuation Guarantee"),
                                        dmc.TableTd("12% of ordinary time earnings"),
                                    ]),
                                    dmc.TableTr([
                                        dmc.TableTd("Super Contributions Tax"),
                                        dmc.TableTd("15% of concessional contributions"),
                                    ]),
                                ])
                            ], striped=True),
                        ])
                    ],
                    value="tax-tables"
                )
            ],
            mt="lg"
        ),
    ], gap="md")

# Callback for True Cost Calculator
@callback(
    Output("true-cost-results", "children"),
    [Input("calculate-true-cost", "n_clicks")],
    [Input("purchase-price-input", "value"),
     Input("salary-input", "value")]
)
def calculate_true_cost(n_clicks, purchase_price, salary):
    """Calculate and display true cost metrics"""
    if not n_clicks or purchase_price is None or purchase_price == 0 or salary is None or salary == 0:
        return dmc.Alert(
            "Enter a purchase price and click Calculate to see the true cost analysis",
            color="blue",
            title="Ready to analyze"
        )
    
    # Convert to float if needed
    purchase_price = float(purchase_price)
    salary = float(salary)
    
    # Calculate metrics
    hourly_rate = salary / 2080  # 40 hours/week * 52 weeks
    hours_of_work = purchase_price / hourly_rate
    days_of_work = int(hours_of_work / 8 * 10) / 10  # 8 hours per day, round down to 1 decimal
    
    # Opportunity cost (7% annual return over 30 years)
    years = 30
    return_rate = 0.07
    future_value = purchase_price * ((1 + return_rate) ** years)
    opportunity_cost = future_value - purchase_price
    
    return dmc.Stack([
        dmc.Alert(
            f"To afford this {format_currency(purchase_price)} purchase, you'll need to work {hours_of_work:.1f} hours or {days_of_work:.1f} days",
            title="Labour Required",
            color="blue"
        ),
        dmc.Alert(
            f"If invested instead, this money would grow to {format_currency(future_value)} in {years} years (at 7% return). That's {format_currency(opportunity_cost)} in missed growth!",
            title="Opportunity Cost",
            color="yellow"
        ),
        dmc.Grid([
            dmc.GridCol(
                create_metric_card(
                    "Break-even Hours",
                    f"{hours_of_work:.1f} hrs",
                    f"At {format_currency(hourly_rate)}/hr"
                ),
                span=6
            ),
            dmc.GridCol(
                create_metric_card(
                    "30-Year Opportunity Cost",
                    format_currency(opportunity_cost),
                    "Missed investment growth"
                ),
                span=6
            ),
        ], gutter="md")
    ], gap="md")


# Callback for FIRE Calculator
@callback(
    [Output("fire-results", "children"),
     Output("target-spend-input", "value"),
     Output("fire-mode-explanation", "children")],
    [Input("calculate-fire", "n_clicks"),
     Input("fire-mode-select", "value")],
    [dash.dependencies.State("current-age-input", "value"),
     dash.dependencies.State("retirement-age-input", "value"),
     dash.dependencies.State("portfolio-value-input", "value"),
     dash.dependencies.State("annual-contribution-input", "value"),
     dash.dependencies.State("target-spend-input", "value"),
     dash.dependencies.State("inflation-rate-input", "value"),
     dash.dependencies.State("investment-return-input", "value")]
)
def calculate_fire(n_clicks, fire_mode, current_age, retirement_age, portfolio_value, 
                  annual_contribution, target_spend, inflation_rate, investment_return):
    """Calculate FIRE metrics"""
    # Create mode explanation
    fire_explanations = {
        "custom": "Set your own target annual spending in retirement. All values are in current day purchasing power with inflation calculated in.",
        "lean": "Lean FIRE: Achieve financial independence with a modest lifestyle ($40k/year). Minimalist approach focused on essential expenses. All values are in current day purchasing power with inflation calculated in.",
        "fat": "Fat FIRE: Achieve financial independence with a comfortable lifestyle ($100k/year). Maintains a higher standard of living in retirement. All values are in current day purchasing power with inflation calculated in.",
        "coast": "Coast FIRE: Your portfolio is large enough that you can stop contributing and it will grow to your FIRE number by retirement age. You still work, but don't need to save for retirement. Note: This calculation does NOT include annual contributions. All values are in current day purchasing power with inflation calculated in."
    }
    
    explanation = dmc.Alert(
        fire_explanations.get(fire_mode, ""),
        color="gray",
        icon=True,
        style={"textAlign": "center"}
    )
    
    # Adjust target spend based on mode
    if fire_mode == "lean":
        target_spend = 40000
    elif fire_mode == "fat":
        target_spend = 100000
    
    if not n_clicks:
        return dmc.Alert(
            "Configure your inputs and click Calculate to see when you can achieve FIRE",
            color="blue",
            title="Ready to plan"
        ), target_spend, explanation
    
    # Convert percentages to decimals
    inflation = inflation_rate / 100
    returns = investment_return / 100
    
    # Calculate real return (adjusted for inflation)
    real_return = (1 + returns) / (1 + inflation) - 1
    
    # Calculate FIRE number (using 4% rule - 25x annual expenses)
    withdrawal_rate = 0.04
    fire_number = target_spend / withdrawal_rate
    
    # For Coast FIRE, check if current portfolio will grow to FIRE number by retirement
    if fire_mode == "coast":
        years_to_retirement = retirement_age - current_age
        future_portfolio = portfolio_value * ((1 + real_return) ** years_to_retirement)
        
        results = dmc.Stack([
            dmc.Alert(
                f"Your FIRE Number: {format_currency(fire_number)} (25x your annual spend of {format_currency(target_spend)})",
                title="Target",
                color="blue"
            ),
            dmc.Alert(
                f"With NO additional contributions, your current portfolio of {format_currency(portfolio_value)} will grow to {format_currency(future_portfolio)} by age {retirement_age}",
                title="Coast FIRE Projection (Annual Contribution Ignored)",
                color="green" if future_portfolio >= fire_number else "red"
            ),
            dmc.Alert(
                "✅ You can Coast FIRE! Stop contributing now and still retire on time." if future_portfolio >= fire_number else "❌ You cannot Coast FIRE yet. Keep contributing to reach your goal.",
                color="green" if future_portfolio >= fire_number else "red"
            )
        ], gap="md")
        
        return results, target_spend, explanation
    
    # Calculate years to FIRE - track both nominal and real values
    nominal_portfolio = portfolio_value
    years_to_fire = 0
    max_years = 200  # Allow calculations up to 200 years if needed
    
    # Calculate until real (inflation-adjusted) portfolio reaches FIRE number
    while years_to_fire < max_years:
        # Calculate present value (inflation-adjusted)
        inflation_factor = (1 + inflation) ** years_to_fire if years_to_fire >= 0 else 1
        present_value = nominal_portfolio / inflation_factor if inflation_factor != 0 else nominal_portfolio
        
        if present_value >= fire_number:
            break
            
        # Grow portfolio nominally for next year with inflation-adjusted contribution
        inflation_adjusted_contribution = annual_contribution * ((1 + inflation) ** years_to_fire)
        nominal_portfolio = nominal_portfolio * (1 + returns) + inflation_adjusted_contribution
        years_to_fire += 1
    
    fire_age = current_age + years_to_fire
    # Build per-year calculation rows for the accordion table
    calc_rows = []
    nominal = portfolio_value
    prev_nominal = None
    fire_achieved_highlighted = False
    # iterate from current age to calculated FIRE age inclusive
    for year_offset, age in enumerate(range(current_age, fire_age + 1)):
        years_from_now = year_offset
        if year_offset == 0:
            nominal = portfolio_value
            investment_gain = 0.0
            investment_gain_real = 0.0
            contribution_nominal = 0.0
            contribution_real = 0.0
        else:
            prev_nominal = nominal
            # Annual contribution increases with inflation
            contribution_nominal = (annual_contribution if annual_contribution else 0) * ((1 + inflation) ** (years_from_now - 1))
            nominal = prev_nominal * (1 + returns) + contribution_nominal
            investment_gain = nominal - prev_nominal - contribution_nominal

        inflation_factor = (1 + inflation) ** years_from_now if years_from_now >= 0 else 1
        present_value = nominal / inflation_factor if inflation_factor != 0 else nominal
        investment_gain_real = investment_gain / inflation_factor if inflation_factor != 0 and year_offset > 0 else 0.0
        contribution_real = contribution_nominal / inflation_factor if inflation_factor != 0 and year_offset > 0 else 0.0
        cumulative_return_pct = ((nominal / portfolio_value) - 1) * 100 if portfolio_value and portfolio_value != 0 else 0

        # Check if this is the first time we exceed FIRE number
        is_fire_row = not fire_achieved_highlighted and present_value >= fire_number
        if is_fire_row:
            fire_achieved_highlighted = True
        
        # Style for the last value cell - green if FIRE achieved, blue otherwise
        value_style = {"backgroundColor": "#C8E6C9", "color": "#2E7D32", "fontWeight": "bold"} if is_fire_row else {"backgroundColor": "#E3F2FD"}

        calc_rows.append(
            dmc.TableTr([
                dmc.TableTd(str(age)),
                dmc.TableTd(str(datetime.now().year + years_from_now)),
                dmc.TableTd(f"x{inflation_factor:.2f}"),
                dmc.TableTd(format_currency(contribution_nominal), style={"borderLeft": "2px solid #ddd"}),
                dmc.TableTd(format_currency(investment_gain)),
                dmc.TableTd(format_currency(nominal)),
                dmc.TableTd(format_currency(contribution_real), style={"backgroundColor": "#E3F2FD", "borderLeft": "2px solid #1976D2"}),
                dmc.TableTd(format_currency(investment_gain_real), style={"backgroundColor": "#E3F2FD"}),
                dmc.TableTd(format_currency(present_value), style=value_style),
            ])
        )

    fire_calc_table = dmc.Table([
        dmc.TableThead([
            dmc.TableTr([
                dmc.TableTh("Age"),
                dmc.TableTh("Year"),
                dmc.TableTh("Inflation Factor"),
                dmc.TableTh("Annual Contributions", style={"borderLeft": "2px solid #ddd"}),
                dmc.TableTh("Investment Gain"),
                dmc.TableTh("Value"),
                dmc.TableTh("Annual Contributions", style={"backgroundColor": "#E3F2FD", "color": "#1976D2", "borderLeft": "2px solid #1976D2"}),
                dmc.TableTh("Investment Gain", style={"backgroundColor": "#E3F2FD", "color": "#1976D2"}),
                dmc.TableTh("Value", style={"backgroundColor": "#E3F2FD", "color": "#1976D2"}),
            ])
        ]),
        dmc.TableTbody(calc_rows)
    ], striped=True, highlightOnHover=True)
    
    # Add section labels above table
    fire_calc_section = dmc.Stack([
        html.Div([
            dmc.Badge("Nominal $", size="lg", variant="outline", color="gray", 
                     style={"position": "absolute", "left": "42%", "transform": "translateX(-50%)"}),
            dmc.Badge("Real $ (Inflation Adjusted)", size="lg", variant="filled", color="blue",
                     style={"position": "absolute", "left": "78%", "transform": "translateX(-50%)"}),
        ], style={"position": "relative", "marginBottom": "10px", "height": "30px"}),
        fire_calc_table
    ], gap="xs")
    
    # Create results
    results = dmc.Stack([
        dmc.Alert(
            f"Your FIRE Number: {format_currency(fire_number)} (25x your annual spend of {format_currency(target_spend)})",
            title="Target",
            color="blue"
        ),
        dmc.Alert(
            f"You can achieve FIRE in {years_to_fire} years at age {fire_age}!" if years_to_fire < max_years else "FIRE may not be achievable with current parameters",
            title="FIRE Timeline",
            color="green" if years_to_fire < max_years else "red"
        ),
        dmc.Grid([
            dmc.GridCol(
                create_metric_card(
                    "Years to FIRE",
                    f"{years_to_fire}",
                    f"Age {fire_age}"
                ),
                span=4
            ),
            dmc.GridCol(
                create_metric_card(
                    "FIRE Number",
                    format_currency(fire_number),
                    f"Based on {format_currency(target_spend)}/yr"
                ),
                span=4
            ),
            dmc.GridCol(
                create_metric_card(
                    "Monthly Target",
                    format_currency(target_spend / 12),
                    "In retirement"
                ),
                span=4
            ),
        ], gutter="md")
        # Detailed per-year calculations (collapsed by default)
        ,
        dmc.Accordion(
            children=[
                dmc.AccordionItem(
                    value="fire-calculations",
                    children=[
                        dmc.AccordionControl("View calculations"),
                        dmc.AccordionPanel([
                            dmc.Text("Per-year FIRE projection (rows: current age → FIRE age)", size="sm", c="dimmed", mb="xs"),
                            dmc.List(
                                [
                                    dmc.ListItem("Annual contributions automatically increase with inflation each year (maintaining purchasing power)"),
                                    dmc.ListItem("Nominal $ = future dollar amounts without inflation adjustment"),
                                    dmc.ListItem("Real $ = inflation-adjusted values in today's purchasing power"),
                                    dmc.ListItem("FIRE is achieved when 'Value (Real $)' reaches your FIRE number"),
                                    dmc.ListItem("Investment gain = portfolio growth from returns only (excluding your contributions)"),
                                ],
                                size="sm",
                                c="dimmed",
                                mb="md"
                            ),
                            fire_calc_section
                        ]),
                    ]
                )
            ],
            variant="separated",
            radius="md",
            multiple=False
        )
    ], gap="md")
    
    return results, target_spend, explanation

# Run server
if __name__ == "__main__":
    app.run(debug=True, port=8050)

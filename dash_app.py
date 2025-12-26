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

def create_metric_card(label, value, change=None, color='blue', is_liability=False):
    """Create a metric card using DMC components
    
    Args:
        label: Card label
        value: Main value to display
        change: Change text (e.g., '↑ 5.2% vs last period')
        color: Card color theme
        is_liability: If True, inverts color logic (up=red, down=green)
    """
    # Determine color based on direction and metric type
    change_color = "dimmed"
    if change:
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
        {"icon": "💰", "label": "Net Worth", "value": "dashboard"},
        {"icon": "📈", "label": "Investments", "value": "investments"},
        {"icon": "👔", "label": "Employment", "value": "employment"},
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
    
    # Add hardcoded market value data points
    hardcoded_market_values = pd.DataFrame([
        {'Date': pd.Timestamp('2022-10-28'), 'Stock Value': 5400},
        {'Date': pd.Timestamp('2022-11-03'), 'Stock Value': 12500},
        {'Date': pd.Timestamp('2023-02-22'), 'Stock Value': 18000},
        {'Date': pd.Timestamp('2023-06-27'), 'Stock Value': 21000},
    ])
    
    # Combine hardcoded and actual market values, remove duplicates
    stock_timeseries = pd.concat([stock_timeseries, hardcoded_market_values]).drop_duplicates(subset=['Date']).sort_values('Date').reset_index(drop=True)
    
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
            type='date',
            range=['2022-10-27', pd.Timestamp.now().strftime('%Y-%m-%d')]
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
    
    # Create Total Value card with glow effect
    total_value_card = dmc.Paper(
        children=[
            dmc.Stack(
                children=[
                    dmc.Text("Total Value", size="sm", fw=500, c="dimmed", tt="uppercase"),
                    dmc.Text(format_currency(total_value), size="xl", fw=700, style={"fontSize": "32px"}),
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
        dmc.Title("Investment Portfolio", order=2, mb="lg"),
        
        # Metrics
        dmc.Grid([
            dmc.GridCol(create_metric_card("Cost Basis", format_currency(cost_basis)), span=4),
            dmc.GridCol(total_value_card, span=4),
            dmc.GridCol(create_metric_card("Total % Increase", f"{pct_increase:.1f}%"), span=4),
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
    
    # Define specific colors for each company (use lowercase for matching)
    company_colors = {
        'artin': '#8b5cf6',  # purple
        'commbank': '#eab308',  # yellow
        'commonwealth': '#eab308',  # yellow (alternate)
        'jetstar': '#f97316',  # orange
        'deloitte': '#6b7280',  # grey
        'aurecon': '#10b981',  # green
    }
    
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
        # Match company name case-insensitively
        company_name = str(row['Company'])
        color = '#6b7280'  # default grey
        for company_key, company_color in company_colors.items():
            if company_key in company_name.lower():
                color = company_color
                break
        
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
    
    # Business days worked by company
    company_days = emp_df_sorted.groupby('Company')['Business Days'].sum().sort_values(ascending=False).reset_index()
    
    # Use company colors with case-insensitive matching
    bar_colors = []
    for company in company_days['Company']:
        color = '#6b7280'  # default grey
        for company_key, company_color in company_colors.items():
            if company_key in str(company).lower():
                color = company_color
                break
        bar_colors.append(color)
    
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
        
        # Business days worked
        dmc.Title("Business Days Worked by Company", order=3, mb="md", mt="xl"),
        dmc.Paper(
            dcc.Graph(figure=fig_days, config={'displayModeBar': False}),
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
    nav_items = ["dashboard", "investments", "employment"]
    active_states = [page == current_page for page in nav_items]
    
    # Get page content
    page_content = dashboard_layout()
    if current_page == "investments":
        page_content = investments_layout()
    elif current_page == "employment":
        page_content = employment_layout()
    
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

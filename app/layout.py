from dash import dcc, html

# Define layout
layout = html.Div([
    html.H1("Global Internet Usage Dashboard", style={'textAlign': 'center'}),

    # Dropdown to select single year or two years for comparison
    html.Div([
        dcc.RadioItems(
            id="map_mode",
            options=[
                {'label': 'Single Year', 'value': 'single'},
                {'label': 'Compare Two Years', 'value': 'compare'}
            ],
            value='single',
            inline=True
        ),
        dcc.Dropdown(
            id="year_selector",
            options=[{'label': str(year), 'value': str(year)} for year in range(2000, 2023)],
            value="2022",
            clearable=False
        ),
        dcc.Dropdown(
            id="compare_year_selector",
            options=[{'label': str(year), 'value': str(year)} for year in range(2000, 2023)],
            value="2000",
            clearable=False,
            style={'display': 'none'}  # Initially hidden
        )
    ], style={'width': '50%', 'margin': 'auto'}),

    # World map visualization
    dcc.Graph(id="world_map"),

])

from dash import dcc, html

grouping_columns = ['INCOME_GRP', 'CONTINENT']

# Define layout
layout = html.Div([
    html.H1("Global Internet Usage Dashboard", style={'textAlign': 'center'}),

    # Dropdown to select single year or two years for comparison
    html.Div([
        dcc.RadioItems(
            id="map_mode",
            options=[
                {'label': 'Show Single Year', 'value': 'single'},
                {'label': 'Compare Two Years', 'value': 'compare'}
            ],
            value='single',
            inline=True
        ),
        dcc.Dropdown(
            id="year_selector",
            options=[{'label': str(year), 'value': str(year)} for year in range(2000, 2023)],
            value="2000",
            clearable=False
        ),
        dcc.Dropdown(
            id="compare_year_selector",
            options=[{'label': str(year), 'value': str(year)} for year in range(2000, 2023)],
            value="2022",
            clearable=False,
            style={'display': 'none'}  # Initially hidden
        )
    ], style={'width': '20%', 'margin': 'auto'}),

    # World map visualization
    dcc.Loading(id="loading-plot", children=[dcc.Graph(id="world_map")]),

    html.Hr(),
    html.H3("Box Plots By Continent or Income Group"),
     # Grouping Variable Dropdown
    html.Div([
        html.Div([
            html.Label("Select how to group the countries:", style={'margin-right': '10px', 'fontWeight': 'bold'}),
        ], style={'display': 'inline-block', 'width': '50%', 'textAlign': 'center'}),

        dcc.Dropdown(
            id='grouping-variable',
            options=[{'label': col, 'value': col} for col in grouping_columns],
            value='INCOME_GRP',  # Default value
            style={'width': '50%', 'margin': 'auto','textAlign': 'left'}
        ),
    ], style={'width': '100%', 'display': 'block', 'padding': '10px', 'textAlign': 'center'}),

    # Box Plots Section
    html.Div([
        # Box Plot 1
        html.Div([
            # Dropdown for selecting the first year for box plot
            dcc.Dropdown(
                id='year-selector-1',
                options=[{'label': str(year), 'value': str(year)} for year in range(2000, 2023)],
                value='2000',  # Default value
                style={'width': '100%'}
            ),
            dcc.Graph(id='box-plot-1')
        ], style={'padding': '20px', 'width': '45%', 'display': 'inline-block', 'vertical-align': 'top', 'textAlign': 'center'}),

        # Box Plot 2
        html.Div([
            # Dropdown for selecting the second year for box plot
            dcc.Dropdown(
                id='year-selector-2',
                options=[{'label': str(year), 'value': str(year)} for year in range(2000, 2023)],
                value='2022',  # Default value
                style={'width': '100%'}
            ),
            dcc.Graph(id='box-plot-2')
        ], style={'padding': '20px', 'width': '45%', 'display': 'inline-block', 'vertical-align': 'top', 'textAlign': 'center'})
    ], style={'padding': '10px', 'display': 'flex', 'justify-content': 'center', 'gap': '20px', 'textAlign': 'center'})
])

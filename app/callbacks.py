from dash import Input, Output
import plotly.express as px
from app.data_loader import merged
from app.app import app  # Import the Dash app

# Callback to show/hide the second year dropdown
@app.callback(
    Output("compare_year_selector", "style"),
    Input("map_mode", "value")
)
def toggle_year_dropdown(mode):
    return {'display': 'block'} if mode == 'compare' else {'display': 'none'}

# Callback to update the map
@app.callback(
    Output("world_map", "figure"),
    [Input("map_mode", "value"),
     Input("year_selector", "value"),
     Input("compare_year_selector", "value")]
)
def update_map(mode, year, compare_year):
    if mode == "single":
        color_data = merged[year]
        title = f"Internet Usage in {year}"
    else:
        color_data = merged[year] - merged[compare_year]
        title = f"Change in Internet Usage ({year} - {compare_year})"

    fig = px.choropleth(
        merged,
        geojson=merged.geometry,
        locations=merged.index,
        color=color_data,
        hover_name=merged["Country Name"],
        color_continuous_scale="YlGnBu",
        labels={'color': 'Internet Usage (%)'},
    )

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(title=title, title_x=0.5, coloraxis_colorbar={'title': '%'})

    return fig

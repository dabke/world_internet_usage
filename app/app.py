from dash import Dash
import dash_bootstrap_components as dbc
from dash import Input, Output
from dash import html
from app.layout import layout
from app.data_loader import load_and_prepare_data
import plotly.express as px

# Load data when the app starts
merged, geojson = load_and_prepare_data()

# Initialize Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Internet Usage Dashboard"
app.layout = layout

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
        color_data = abs(merged[year] - merged[compare_year])
        if (merged[year].mean() - merged[compare_year].mean())<0:
            variation = "Increase"
        else:
            variation="Decrease"
            
        title = f"Value of {variation} in Internet Usage ({year} - {compare_year})"

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
    fig.update_layout(title=title, title_x=0.5, coloraxis_colorbar=dict(
        tickvals=[10, 20, 30, 40, 50, 60, 70, 80, 90], 
        ticktext=["0-10", "10-20", "20-30", "30-40", "40-50", "50-60", "60-70", "70-80", "80-90"],
        tickmode='array',
        ticks="",  
        title="%"
    ),coloraxis=dict(
        cmin=0,  
        cmax=100  
    ))

    return fig

# @app.callback(
#     [Output("top-5-countries", "children"),
#      Output("bottom-5-countries", "children"),
#      Output("median-usage", "children")],
#     [Input("year_selector", "value")]
# )
# def update_statistics(year):
#     year = str(year)  # Ensure it's an integer
#     data_year = merged[['Country Name', year]].dropna().sort_values(by=year,ascending=False)
    
#     # Top 5 and Bottom 5 countries
#     top_5 = data_year.head(5)
#     bottom_5 = data_year.tail(5)

#     # Compute median
#     median_usage = data_year[year].median()

#     # Convert to list items for display
#     top_5_list = [html.Li(f"{row['Country Name']}: {row[year]:.2f}%") for _, row in top_5.iterrows()]
#     bottom_5_list = [html.Li(f"{row['Country Name']}: {row[year]:.2f}%") for _, row in bottom_5.iterrows()]

#     return top_5_list, bottom_5_list, f"{median_usage:.2f}%"

@app.callback(
    [Output("top-5-countries", "children"),
     Output("bottom-5-countries", "children"),
     Output("median-usage", "children")],
    [Input("map_mode", "value"),
     Input("year_selector", "value"),
     Input("compare_year_selector", "value")]
)
def update_statistics(mode, year, compare_year):
    if mode == "single":
        data = merged[[year]].dropna()
        data_sorted = data.sort_values(by=year, ascending=False)
        top5 = data_sorted.head(5)
        bottom5 = data_sorted.tail(5)
        median = data[year].median()

        top5_list = [html.Li(f"{country}: {value:.2f}%") for country, value in zip(top5.index, top5[year])]
        bottom5_list = [html.Li(f"{country}: {value:.2f}%") for country, value in zip(bottom5.index, bottom5[year])]
        median_text = f"Median Internet Usage in {year}: {median:.2f}%"
    
    else:  # Compare mode
        data = merged[[year, compare_year]].dropna()
        data["Difference"] = data[compare_year] - data[year]
        data_sorted = data.sort_values(by="Difference", ascending=False)
        top5 = data_sorted.head(5)
        bottom5 = data_sorted.tail(5)
        median = data["Difference"].median()

        top5_list = [html.Li(f"{country}: {value:.2f}%") for country, value in zip(top5.index, top5["Difference"])]
        bottom5_list = [html.Li(f"{country}: {value:.2f}%") for country, value in zip(bottom5.index, bottom5["Difference"])]
        median_text = f"Median Change ({year} - {compare_year}): {median:.2f}%"

    return html.Ul(top5_list), html.Ul(bottom5_list), html.P(median_text)

@app.callback(
    Output('box-plot-1', 'figure'),
    [Input('year-selector-1', 'value'),
     Input('grouping-variable', 'value')]
)
def update_box_plot_1(year, grouping_variable):
    # Group the data by the selected variable and plot a box plot for the selected year
    fig = px.box(
        merged, 
        x=grouping_variable, 
        y=year,
        points="all",  # Display all data points
        title=f"Internet Usage Box Plots by {grouping_variable} in {year}",
        hover_data="Country Name"
    )
    fig.update_layout(
        yaxis=dict(range=[-5, 105]),
        xaxis_title='',
        yaxis_title='% internet usage'
    )
    return fig

# Callback to update the second box plot
@app.callback(
    Output('box-plot-2', 'figure'),
    [Input('year-selector-2', 'value'),
     Input('grouping-variable', 'value')]
)
def update_box_plot_2(year, grouping_variable):
    # Group the data by the selected variable and plot a box plot for the selected year
    fig = px.box(
        merged, 
        x=grouping_variable, 
        y=year,
        points="all",  # Display all data points
        title=f"Internet Usage Box Plots by {grouping_variable} in {year}",
        hover_data="Country Name"
    )
    fig.update_layout(
        yaxis=dict(range=[-5, 105]),
        xaxis_title='',
        yaxis_title='% internet usage'
    )
    return fig


server = app.server

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)

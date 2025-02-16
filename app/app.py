from dash import Dash
import dash_bootstrap_components as dbc
from app.layout import layout
from app.data_loader import load_and_prepare_data

# Load data when the app starts
merged, geojson = load_and_prepare_data()

# Initialize Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Internet Usage Dashboard"
app.layout = layout

# Import callbacks
import app.callbacks

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)

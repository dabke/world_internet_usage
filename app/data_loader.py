import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import shape

def load_and_prepare_data():
    """
    Load, clean, and merge internet usage data with geospatial world data.
    Returns:
        merged (GeoDataFrame): The processed dataset.
        geojson (str): GeoJSON representation for plotting.
    """
    # Load internet usage data
    data = pd.read_csv("data/internet_usage.csv")

    # Replace unknown values with NaN and drop the mostly null 2023 column
    data.replace(r"^\.+$", np.nan, regex=True, inplace=True)
    data.drop("2023", axis=1, inplace=True)

    # Convert year columns to float
    nonnum_cols = ["Country Name", "Country Code"]
    years_col = [col for col in data.columns if col not in nonnum_cols]
    data[years_col] = data[years_col].astype(float)

    # Load world map shapefile
    world = gpd.read_file("data/ne_10m_admin_0_countries.shp")

    # Select relevant columns
    world = world[[
        "SOVEREIGNT", "ADMIN", "NAME", "CONTINENT", "SU_A3", "ISO_A3", 
        "ADM0_A3", "POP_EST", "POP_RANK", "POP_YEAR", "GDP_MD", "GDP_YEAR", 
        "geometry", "ECONOMY", "INCOME_GRP"
    ]]

    # Correct country codes for merging
    replacements = {
        "France": "FRA", "Norway": "NOR", "Kosovo": "XKX", "Palestine": "PSE", 
        "South Sudan": "SSD", "Jersey": "CHI"
    }
    for country, code in replacements.items():
        world.loc[world["ADMIN"] == country, "ADM0_A3"] = code

    # Assign continents to missing entries
    continent_fixes = {"MDV": "Asia", "MUS": "Africa", "SYC": "Africa"}
    for code, continent in continent_fixes.items():
        world.loc[world["ADM0_A3"] == code, "CONTINENT"] = continent

    # Merge datasets on country code
    merged = data.set_index('Country Code').join(world.set_index('ADM0_A3'), how="left")

    # Ensure geometries are in the correct format
    merged["geometry"] = merged["geometry"].apply(lambda x: shape(x) if isinstance(x, dict) else x)

    # Convert to GeoDataFrame if not already
    if not isinstance(merged, gpd.GeoDataFrame):
        merged = gpd.GeoDataFrame(merged, geometry="geometry")

    # Simplify geometries for lighter computation
    merged["geometry"] = merged["geometry"].simplify(0.05)

    # Convert to GeoJSON for plotting
    geojson = merged.to_json()

    return merged, geojson
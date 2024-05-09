import streamlit as st
import geopandas as gpd
import plotly.express as px
import json
from geopy.distance import geodesic

fp = 'NUTS3_Jan_2018_UGCB_in_the_UK.shp'

# Load the UK geospatial data from a shapefile
gdf = gpd.read_file(fp)
gdf = gdf.to_crs(epsg=4326)

# Dropdown for selecting the first location
selected_location1 = st.sidebar.selectbox("Select First Location", gdf['nuts318nm'].unique())

# Dropdown for selecting the second location
selected_location2 = st.sidebar.selectbox("Select Second Location", gdf['nuts318nm'].unique())

# Highlight the selected locations
gdf['highlight'] = gdf['nuts318nm'].apply(lambda x: 1 if x == selected_location1 or x == selected_location2 else 0)

# Find the centroids of the selected locations
centroid1 = gdf[gdf['nuts318nm'] == selected_location1].geometry.unary_union.centroid
centroid2 = gdf[gdf['nuts318nm'] == selected_location2].geometry.unary_union.centroid

# Calculate the distance between the centroids
distance = geodesic((centroid1.y, centroid1.x), (centroid2.y, centroid2.x)).miles

# Display the distance in the Streamlit app
st.write(f"The distance between {selected_location1} and {selected_location2} is {distance} miles.")

# Convert the entire GeoDataFrame with 'to_json' and load as JSON
json_data = json.loads(gdf.to_json())

# Create a Plotly Mapbox figure
fig = px.choropleth_mapbox(gdf,
                           geojson=json_data,
                           locations=gdf.index,
                           color='highlight',  # Use the 'highlight' column for the color
                           color_continuous_scale="Viridis",  # Use a color scale that clearly distinguishes between 0 and 1
                           mapbox_style="open-street-map",
                           zoom=5,
                           center={"lat": 54.7, "lon": -3.5},
                           opacity=0.5)

# Update the layout for a cleaner look
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

# Streamlit app title
st.title('Interactive UK Map')

# Render the plotly figure in Streamlit
st.plotly_chart(fig)
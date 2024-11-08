import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster, HeatMap
from streamlit_folium import st_folium
import io

st.set_page_config(layout="wide")
# Load the data
data = pd.read_csv('training_ready_data.csv')

# Sidebar filter for selecting state
st.sidebar.title("Filter Options")
states = ["All States"] + sorted(data['StateName'].unique())
selected_state = st.sidebar.selectbox("Select a State", options=states)

# Filter data based on state selection
if selected_state != "All States":
    filtered_data = data[data['StateName'] == selected_state]
else:
    filtered_data = data  # Show all data if "All States" is selected

# Calculate the combined score using the Normalized Difference Index
filtered_data['combined_score'] = (
    (filtered_data['DENSITY_DOM'] - filtered_data['DENSITY_GROUPQ']) /
    (filtered_data['DENSITY_DOM'] + filtered_data['DENSITY_GROUPQ']).replace(0, 1)  # Avoid divide by zero
)

# Initialize a Folium map centered over the US
m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)

# Add combined heatmap for the Normalized Difference Index
heatmap_data = filtered_data[['Latitude_zillow', 'Longitude_zillow', 'combined_score']].dropna()
heatmap = HeatMap(data=heatmap_data.values.tolist(), radius=15, max_zoom=12)
heatmap_layer = folium.FeatureGroup(name='Heatmap Layer')
heatmap_layer.add_child(heatmap)
m.add_child(heatmap_layer)

# Create a separate feature group for markers to make it toggleable
marker_layer = folium.FeatureGroup(name='Marker Layer')

# Configure MarkerCluster with options to handle overlapping markers
marker_cluster = MarkerCluster(
    disableClusteringAtZoom=10  # Disable clustering at closer zoom levels for easier interaction
).add_to(marker_layer)

# Columns for detailed information in the tooltip
columns = [
    "E_POV150", "E_UNEMP", "E_NOHSDP", "E_UNINSUR", "E_AGE65",
    "E_AGE17", "E_DISABL", "E_SNGPNT", "E_LIMENG", "E_MINRTY",
    "E_MUNIT", "E_MOBILE", "E_CROWD", "E_NOVEH", "E_GROUPQ",
]

# Add markers for each row in the filtered data with a tooltip only
for _, row in filtered_data.iterrows():
    lat = row['Latitude_zillow']
    lon = row['Longitude_zillow']
    
    # Generate the tooltip text with summary details
    tooltip_text = f"""
    Location: {row['LOCATION']}<br>
    State: {row['StateName']}<br>
    DOM: {row['DOM']}<br>
    {"<br>".join([f"{col}: {row[col]}" for col in columns])}
    DENSITY_GROUPQ: {row['DENSITY_GROUPQ']}<br>
    """
    
    # Add marker with tooltip (hover effect) only, no popup to avoid panning
    folium.Marker(
        location=[lat, lon],
        tooltip=tooltip_text  # Show data on hover without clicking
    ).add_to(marker_cluster)

# Add the marker layer to the map
m.add_child(marker_layer)

# Add LayerControl to toggle the heatmap and marker layers on and off
folium.LayerControl().add_to(m)

# Move data grid and download option to sidebar
st.sidebar.subheader("Raw Data")
st.sidebar.dataframe(filtered_data)

# Download filtered data as CSV
csv = filtered_data.to_csv(index=False).encode('utf-8')
st.sidebar.download_button(
    label="Download filtered data as CSV",
    data=csv,
    file_name='filtered_data.csv',
    mime='text/csv',
)

# Display the map in Streamlit with `use_container_width` set to maximize width
st.header("Zillow DOM with Social Vulnerability Indices", anchor="map")
st_folium(m, use_container_width=True)

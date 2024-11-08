# Zillow DOM and Social Vulnerability Index Visualization

This Streamlit app visualizes Zillow DOM (Days on Market) data alongside the CDC's Social Vulnerability Index (SVI) indicators, specifically focusing on `E_GROUPQ`, which represents population groups living in group quarters. The app includes interactive maps with heatmaps and tooltips to explore the relationship between `DENSITY_DOM` (Days on Market density) and `DENSITY_GROUPQ` (group quarters density), as well as other SVI factors. Although the data shows little to no correlation, this visualization provides insights into regional patterns and facilitates exploration by state.

## Features

- **State-Based Filtering**: Select any U.S. state to filter data and view results for specific regions.
- **Interactive Map with Heatmap**: The map includes a heatmap layer to visualize combined `DENSITY_DOM` and `DENSITY_GROUPQ` scores.
- **Clustered Markers with Tooltips**: Markers display detailed information for each location, including Zillow DOM and various SVI attributes.
- **Downloadable Data**: Download the filtered dataset directly from the sidebar.

## Technical Overview

- **Combined Score Calculation**: 
  - A normalized difference score (`combined_score`) is computed to highlight the interaction between `DENSITY_DOM` and `DENSITY_GROUPQ`:
    \[
    \text{combined_score} = \frac{\text{DENSITY_DOM} - \text{DENSITY_GROUPQ}}{\text{DENSITY_DOM} + \text{DENSITY_GROUPQ}}
    \]
  - This score is used to create a heatmap layer, providing a visual interpretation of DOM and group quarters density across the U.S.
- **Interactive Map Using Folium**:
  - A Folium map is initialized, with MarkerClusters for interactive exploration.
  - `MarkerCluster` allows viewing of closely placed data points without excessive overlap and supports spiderfied (spread out) views at closer zoom levels.
- **Tooltips for Detailed Data**:
  - Each marker displays additional SVI information for each location, making it easy to assess different vulnerability indices.

## Data Sources

1. **Zillow DOM Data** (`zillow_dom.csv`): Contains real estate data, particularly Days on Market (DOM).
2. **CDC Social Vulnerability Index (SVI)** (`vulnerability_index.csv`): Provides information on social vulnerability, including attributes like `E_GROUPQ` for individuals in group quarters.

## Installation

To set up and run this Streamlit app locally:

1. Clone this repository and navigate to the directory.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run heatmap.py
   ```

## File Structure

- **heatmap.py**: Main application code (the code you provided), handling data loading, map visualization, and user interface.
- **data/**: Folder containing the input CSV files (`zillow_dom.csv` and `vulnerability_index.csv`).
- **README.md**: This file, providing documentation.
- **requirements.txt**: Contains the necessary Python libraries.

## Usage

1. **Select a State**: Use the sidebar dropdown to filter the data by a specific U.S. state, or select "All States" to view national data.
2. **Explore the Map**:
   - Toggle the heatmap and marker layers on and off using the `LayerControl` in the top right corner of the map.
   - Hover over markers to view tooltip information for each location.
3. **Download Filtered Data**:
   - View the filtered data in the sidebar and download it as a CSV file for further analysis.

## Key Components in `heatmap.py`

### Import Libraries and Configuration

```python
import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster, HeatMap
from streamlit_folium import st_folium
import io
```

- Imports required libraries for interactive visualization (`folium` and `streamlit_folium`) and data manipulation (`pandas`).
- Configures the Streamlit app to display in wide mode.

### Data Loading and Filtering

```python
data = pd.read_csv('data/training_ready_data.csv')
```

- Loads data from the `training_ready_data.csv` file. This file should be prepared beforehand and saved in the `data` folder.

### User Interface with Streamlit Sidebar

```python
st.sidebar.title("Filter Options")
selected_state = st.sidebar.selectbox("Select a State", options=states)
```

- Adds filtering options in the sidebar for users to select specific states.

### Calculating the Combined Score

```python
filtered_data['combined_score'] = (
    (filtered_data['DENSITY_DOM'] - filtered_data['DENSITY_GROUPQ']) /
    (filtered_data['DENSITY_DOM'] + filtered_data['DENSITY_GROUPQ']).replace(0, 1)
)
```

- Calculates a normalized difference score (`combined_score`) for `DENSITY_DOM` and `DENSITY_GROUPQ`, enabling visualization of their combined effect across regions.

### Map Initialization and Layer Addition

```python
m = folium.Map(location=[37.0902, -95.7129], zoom_start=4)
heatmap_layer = folium.FeatureGroup(name='Heatmap Layer')
marker_layer = folium.FeatureGroup(name='Marker Layer')
```

- Initializes the Folium map, centered on the U.S.
- Adds a heatmap and marker layer to visualize `combined_score` and individual data points.

### Tooltips and Clustered Markers

```python
for _, row in filtered_data.iterrows():
    folium.Marker(
        location=[lat, lon],
        tooltip=tooltip_text  # Show data on hover without clicking
    ).add_to(marker_cluster)
```

- Loops through filtered data and adds each location to the map with a tooltip showing various SVI and DOM details.

### Displaying the Map and Data Download Option

```python
st_folium(m, use_container_width=True)
st.sidebar.dataframe(filtered_data)
st.sidebar.download_button(...)
```

- Displays the map with `st_folium`.
- Adds a data table and download button to the sidebar, allowing users to view and download the filtered data.

## Known Limitations

- **Performance**: The app does not optimize for performance and may run slowly with large datasets.
- **Correlation Analysis**: Initial results suggest weak or no correlation between `DENSITY_DOM` and `DENSITY_GROUPQ`, though the map allows further visual inspection.
  
## Future Enhancements

- **Performance Optimization**: Improve loading and filtering performance for large datasets, potentially using Spark.
- **Additional SVI Indices**: Expand to analyze other SVI indices beyond `E_GROUPQ`.

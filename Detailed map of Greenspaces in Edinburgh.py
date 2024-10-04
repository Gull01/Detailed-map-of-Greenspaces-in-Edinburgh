import folium
import geopandas as gpd

# shapefiles
greenspaces_path = r'E:\Edenburg\Greenspaces.shp'
target_path = r'E:\Project\Target.shp'
target_roads_path = r'E:\Edenburg\Related_Roads.shp'
access_points_path = r'E:\Edenburg\Access_points.shp'

# Read the shapefiles using geopandas
gdf_greenspaces = gpd.read_file(greenspaces_path)
gdf_target = gpd.read_file(target_path)
gdf_target_roads = gpd.read_file(target_roads_path)
gdf_access_points = gpd.read_file(access_points_path)

# map centered on Edinburgh, Scotland
map_edinburgh = folium.Map(location=[55.9533, -3.1883], zoom_start=12)

# Basemap
folium.TileLayer('openstreetmap', name='OpenStreetMap').add_to(map_edinburgh)
folium.TileLayer('stamenterrain', name='Terrain').add_to(map_edinburgh)
folium.TileLayer('stamentoner', name='Toner').add_to(map_edinburgh)
folium.TileLayer('cartodbpositron', name='Positron').add_to(map_edinburgh)
folium.TileLayer('cartodbdark_matter', name='Dark Matter').add_to(map_edinburgh)
folium.TileLayer(
    tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', 
    attr='Google', 
    name='Google Satellite'
).add_to(map_edinburgh)

# Pop ups
def popup_greenspaces(row):
    function = row.get('function', 'N/A')
    area_sqm = row.get('Area_SQM', 'N/A')
    html = f"""
    <b>Function:</b> {function}<br>
    <b>Area (sqm):</b> {area_sqm}
    """
    return html


def popup_target(row):
    name = row.get('Name', 'N/A')
    html = f"<b>Name:</b> {name}"
    return html


def popup_target_roads(row):
    road_type = row.get('type', 'N/A')
    html = f"<b>Type:</b> {road_type}"
    return html


def popup_access_points(row):
    access_type = row.get('accessType', 'N/A')
    html = f"<b>Access Type:</b> {access_type}"
    return html

# greenspaces as a separate layer
greenspaces_layer = folium.FeatureGroup(name='Greenspaces')
for idx, row in gdf_greenspaces.iterrows():
    folium.GeoJson(
        row['geometry'],
        popup=folium.Popup(popup_greenspaces(row), max_width=300)
    ).add_to(greenspaces_layer)
greenspaces_layer.add_to(map_edinburgh)

# target layer boundary
target_layer = folium.FeatureGroup(name='Target')
for idx, row in gdf_target.iterrows():
    folium.GeoJson(
        row['geometry'],
        popup=folium.Popup(popup_target(row), max_width=300)
    ).add_to(target_layer)
target_layer.add_to(map_edinburgh)

# target roads layer
target_roads_layer = folium.FeatureGroup(name='Target Roads')
for idx, row in gdf_target_roads.iterrows():
    folium.GeoJson(
        row['geometry'],
        popup=folium.Popup(popup_target_roads(row), max_width=300)
    ).add_to(target_roads_layer)
target_roads_layer.add_to(map_edinburgh)

# access points layer
access_points_layer = folium.FeatureGroup(name='Access Points')
for idx, row in gdf_access_points.iterrows():
    folium.GeoJson(
        row['geometry'],
        popup=folium.Popup(popup_access_points(row), max_width=300)
    ).add_to(access_points_layer)
access_points_layer.add_to(map_edinburgh)

# control panel to switch between the layers
folium.LayerControl().add_to(map_edinburgh)

# Save the map to an HTML file
map_edinburgh.save('map_edinburgh_all_layers.html')

# Display the map
map_edinburgh
]
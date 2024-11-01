import sys
import os
import requests
import time
import plotly.express as px

# Agregar la carpeta 'reference_tables' al sistema de rutas
sys.path.append(os.path.join(os.path.dirname(__file__), '../reference_tables'))

# Importar los DataFrames
from tabla_mun_equipo_pob_asist import func_mun_equipo_pob_asist

df_mun_x_team = func_mun_equipo_pob_asist()

# Obtener Latitud y Longitud (A VECES NO FUNCIONA)
def obtener_coordenadas(municipio):
    for attempt in range(3):  # Try up to 3 times
        try:
            print(f"Fetching coordinates for {municipio} (Attempt {attempt+1})")
            url = f"https://nominatim.openstreetmap.org/search?q={municipio},+spain&format=json"
            response = requests.get(url)
            time.sleep(2)  # Recommended delay to respect rate limits
            if response.status_code == 200 and response.json():
                result = response.json()[0]
                return float(result['lat']), float(result['lon'])
        except Exception as e:
            print(f"Error fetching coordinates for {municipio} on attempt {attempt+1}: {e}")
    return None, None  # Return None if all attempts fail

# Normalize 'Municipio' column to lower case and strip any whitespace
df_mun_x_team['Municipio'] = df_mun_x_team['Municipio'].str.lower().str.strip()

# Apply the function and fetch coordinates
df_mun_x_team['Latitude'], df_mun_x_team['Longitude'] = zip(*df_mun_x_team['Municipio'].apply(obtener_coordenadas))

# Check for missing coordinates
missing_coords = df_mun_x_team[df_mun_x_team['Latitude'].isna()]
if not missing_coords.empty:
    print("Municipios sin coordenadas:")
    print(missing_coords[['Municipio', 'Equipo']])

# Create geoJSON for mapping with Plotly
my_geojson = []
for _, row in df_mun_x_team.dropna(subset=['Latitude', 'Longitude']).iterrows():
    feature = {
        "type": "Feature",
        "properties": {
            "Municipio": row['Municipio'],
            "attendance_pct": (row['Asistencia_media_estadio'] / row['Poblacion']) * 100
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": [row['Longitude'], row['Latitude']]
        },
        "id": row['Municipio']        
    }
    my_geojson.append(feature)
# NECESITA MAS INFORMACION PARA FORMAR EL POLYGON
# https://api-features.ign.es/collections/administrativeboundary/items?limit=1000 
# Calculate attendance percentage
df_mun_x_team['attendance_pct'] = (df_mun_x_team['Asistencia_media_estadio'] / df_mun_x_team['Poblacion']) * 100

# NUEVO MAPA
# https://plotly.com/python/tile-county-choropleth/
fig = px.choropleth_map(
    df_mun_x_team,
    geojson=my_geojson,
    locations='Municipio',
    color='attendance_pct',
    color_continuous_scale="Viridis",
    range_color=(0, 6),
    map_style="carto-positron",
    zoom=6,
    center = {"lat": 39.326069, "lon":  -4.837979},
    opacity=0.5,
    labels={'attendance_pct':'Attendance rate'})

fig.update_layout(
    margin={"r":0,"t":0,"l":0,"b":0},
    title_text="Municipal Attendance Rates in Spain")

fig.show()
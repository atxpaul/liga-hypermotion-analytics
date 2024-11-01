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

def obtener_coordenadas(municipio):
    for attempt in range(3):  # Try up to 3 times
        try:
            print(f"Fetching coordinates for {municipio} (Attempt {attempt+1})")
            url = f"https://nominatim.openstreetmap.org/search?q={municipio},+spain&format=json"
            response = requests.get(url)
            time.sleep(1.5)  # Slightly longer delay to respect rate limits
            if response.status_code == 200 and response.json():
                result = response.json()[0]
                return float(result['lat']), float(result['lon'])
        except Exception as e:
            print(f"Error fetching coordinates for {municipio} on attempt {attempt+1}: {e}")
    return None, None  # Return None if all attempts fail

df_mun_x_team['Municipio'] = df_mun_x_team['Municipio'].str.lower().str.strip()

# Apply the function and fetch coordinates
df_mun_x_team['lat'], df_mun_x_team['lon'] = zip(*df_mun_x_team['Municipio'].apply(obtener_coordenadas))

# Check for missing coordinates
missing_coords = df_mun_x_team[df_mun_x_team['lat'].isna()]
if not missing_coords.empty:
    print("Municipios sin coordenadas:")
    print(missing_coords[['Municipio', 'Equipo']])

# Remove rows with missing coordinates to avoid issues
df_mun_x_team = df_mun_x_team.dropna(subset=['lat', 'lon'])

df_mun_x_team['attendance_pct'] = (df_mun_x_team['Asistencia_media_estadio'] / df_mun_x_team['Poblacion']) * 100

# NUEVO MAPA
fig = px.choropleth_map(
    df_mun_x_team,
    geojson=df_mun_x_team['lat'],df_mun_x_team['lon']
                        )
# https://plotly.com/python/tile-county-choropleth/

# MAPA ORIGINAL
# Custom red color scale for attendance percentage
custom_red_scale = [
    [0, "#DF1B3F"],  # Darker red
    [1, "#FF9999"]   # Lighter red
]

fig = px.scatter_mapbox(
    df_mun_x_team,
    lat='lat',
    lon='lon',
    size='Asistencia_media_estadio',  
    color='attendance_pct',  
    color_continuous_scale=custom_red_scale,
    size_max=15,  # Reduce maximum size of circles
    hover_name='Equipo',
    hover_data={
        'Poblacion': True, 
        'Asistencia_media_estadio': True, 
        'attendance_pct': ':.2f',
        'lat': False,  
        'lon': False
    },
    text='Municipio', 
    zoom=5,
    center=dict(lat=40.0, lon=-3.7),
    title="Asistencia Media y % de la Población en Municipios de Equipos",
    mapbox_style="carto-positron"
)

fig.update_traces(textposition="top right")

fig.show()
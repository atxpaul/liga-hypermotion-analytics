import pandas as pd
import requests
import time
import plotly.express as px
from table_popxmunixequipo import df_mun_x_team

df_mun_x_team.rename(columns={'Población\r\n(1 de enero de 2023)': 'Poblacion'}, inplace=True)

df_mun_x_team['Poblacion'] = df_mun_x_team['Poblacion'].str.replace(' ', '').astype(int)

def obtener_coordenadas(municipio):
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={municipio},+spain&format=json"
        response = requests.get(url)
        time.sleep(1) 
        if response.status_code == 200 and response.json():
            result = response.json()[0]
            return float(result['lat']), float(result['lon'])
    except Exception as e:
        print(f"Error obteniendo coordenadas para {municipio}: {e}")
    return None, None

df_mun_x_team['lat'], df_mun_x_team['lon'] = zip(*df_mun_x_team['municipio'].apply(obtener_coordenadas))

missing_coords = df_mun_x_team[df_mun_x_team['lat'].isna()]
if not missing_coords.empty:
    print("Municipios sin coordenadas:")
    print(missing_coords[['municipio', 'CLUB']])

df_mun_x_team = df_mun_x_team.dropna(subset=['lat', 'lon'])

df_mun_x_team['attendance_pct'] = (df_mun_x_team['Average'] / df_mun_x_team['Poblacion']) * 100

fig = px.scatter_mapbox(
    df_mun_x_team,
    lat='lat',
    lon='lon',
    size='Average',  
    color='attendance_pct',  
    color_continuous_scale=px.colors.sequential.YlOrBr, 
    size_max=50, 
    hover_name='CLUB',
    hover_data={'Poblacion': True, 'Average': True, 'attendance_pct': ':.2f'},
    text='municipio', 
    zoom=5,
    center=dict(lat=40.0, lon=-3.7),
    title="Asistencia Media y % de la Población en Municipios de Equipos",
    mapbox_style="carto-positron"
)

fig.update_traces(textposition="top right")

fig.show()

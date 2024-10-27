import sys
import os
import requests
import time
import plotly.express as px

# Agregar la carpeta 'reference_tables' al sistema de rutas
sys.path.append(os.path.join(os.path.dirname(__file__), '../reference_tables'))

# Importar los DataFrames
from tabla_ppto_jugadores import func_ppto_jugadores
from tabla_mun_equipo_pob_asist import func_mun_equipo_pob_asist

df_ppto_jugadores = func_ppto_jugadores()
df_mun_x_team = func_mun_equipo_pob_asist()

# Dasboard 1
# Calcular el valor por gol
df_ppto_jugadores['Valor_por_gol'] = df_ppto_jugadores['Valor_de_mercado_total'] / df_ppto_jugadores['N_goles']

# Ordenar el DataFrame por 'Valor_por_gol' de mayor a menor
df_ppto_jugadores = df_ppto_jugadores.sort_values(by='Valor_por_gol', ascending=False)

# Crear gráfico de barras
fig1 = px.bar(df_ppto_jugadores, x='Equipo', y='Valor_por_gol', 
             title="Valor por Gol de Cada Equipo",
             labels={'Equipo': 'Equipo', 'Valor_por_gol': 'Valor por Gol (€)'},
             color_discrete_sequence=["#19204E"])

# Personalizar el título
fig1.update_layout(title='<b>Valor por Gol de Cada Equipo<b>',
    title_font=dict(family='Arial Black', size=30))


# Dashboard 2
# Def obtener coordenadas(a veces no funciona)
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

df_mun_x_team['Municipio'] = df_mun_x_team['Municipio'].str.lower().str.strip()

df_mun_x_team['lat'], df_mun_x_team['lon'] = zip(*df_mun_x_team['Municipio'].apply(obtener_coordenadas))

missing_coords = df_mun_x_team[df_mun_x_team['lat'].isna()]
if not missing_coords.empty:
    print("Municipios sin coordenadas:")
    print(missing_coords[['Municipio', 'Equipo']])

df_mun_x_team = df_mun_x_team.dropna(subset=['lat', 'lon'])

df_mun_x_team['attendance_pct'] = (df_mun_x_team['Asistencia_media_estadio'] / df_mun_x_team['Poblacion']) * 100

custom_red_scale = [
    [0, "#DF1B3F"],
    [1, "#FF9999"]
]

fig2 = px.scatter_mapbox(
    df_mun_x_team,
    lat='lat',
    lon='lon',
    size='Asistencia_media_estadio',  
    color='attendance_pct',
    color_continuous_scale=custom_red_scale,
    size_max=15,   
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

fig2.update_traces(textposition="top right")

fig1.show()
fig2.show()

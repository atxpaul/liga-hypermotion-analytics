import sys
import os
import plotly.express as px
import json
import pandas as pd
import geopandas as gpd

# Agregar la carpeta 'reference_tables' al sistema de rutas
sys.path.append(os.path.join(os.path.dirname(__file__), '../reference_tables'))

# Importar el df con todas las columnas
from tabla_mun_equipo_pob_asist import func_mun_equipo_pob_asist
df_para_mapa = func_mun_equipo_pob_asist()

# Calcular el porcentaje de asistencia y añadir columna al df
df_para_mapa['asist_pct'] = (df_para_mapa['Asistencia_media_estadio'] / df_para_mapa['Poblacion']) * 100

# Leer archivo JSON y asignarlo a una variable
with open('../scrap_results/geojson_data.json', 'r', encoding='utf=8') as file:
   geojson_data = json.load(file)
# Crear nueva estructura con "feature" alrededor de cada municipio
new_gejson_data = {key: {"features": value} for key, value in geojson_data.items()}
# Guardar el nuevo archivo JSON
with open('geojson_data_updated.json', 'w', encoding='utf-8') as file:
    json.dump(new_gejson_data, file, ensure_ascii=False, indent=4)
# Leer nuevo archivo JSON y asignarlo a variable
with open('../dashboard/geojson_data_updated.json', 'r', encoding='utf=8') as file:
    geojson_data_updated = json.load(file)

# Extraer propiedades y geometría para crear DataFrame
data = []
geojson_coord = []

# Desempaquetar cada feature dentro de geojson_data_updated
for key, municipality_data in geojson_data_updated.items():
    # Acceder a 'features' de cada municipio
    feature = municipality_data["features"]
    # Añadir el "id" como el nombre del municipio
    feature["id"] = feature["properties"]["nameunit"]

# Agregar properties a la lista de datos y geometry a las coordenadas
    data.append(feature["properties"])
    geojson_coord.append(feature["geometry"])

# Desempaquetar las características y añadirlas a una lista
features = []
for key, municipality_data in geojson_data_updated.items():
    feature = municipality_data["features"]
    # Agregar cada característica a la lista
    features.append(feature)

# Crear un GeoDataFrame a partir de las características extraídas
geo_df = gpd.GeoDataFrame.from_features(features).set_index("nameunit")
geo_df.index = geo_df.index.str.lower()
print(geo_df)

# Unir `geo_df` con `df_para_mapa` para incluir la columna `asist_pct`
geo_df = geo_df.join(df_para_mapa.set_index("Municipio")[["asist_pct"]])

# Configurar el gráfico del mapa
map_fig = px.choropleth_mapbox(
    geo_df,
    geojson=geo_df.geometry,
    locations=geo_df.index,
    color="asist_pct",
    center={"lat": 39.326069, "lon":  -4.837979},
    color_continuous_scale="Viridis",
    mapbox_style='carto-positron',
    zoom=5.5
)
map_fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

# Mostrar el mapa
map_fig.show()

import pandas as pd

df_1 = pd.read_json("players_data.json")

df_2 = df_1[['NOMBRE', 'EQUIPO', 'G']]  # Selecciona solo las columnas 'columna1' y 'columna3'.
df_2['EQUIPO'] = df_2['EQUIPO'].str.lower()

df_2 = pd.DataFrame(df_2)

# Contar valores únicos en la columna 'nombre'
count_distinct_nombres = df_2['EQUIPO'].nunique()

# Obtener una lista con los valores únicos en la columna 'nombre'
lista_valores_unicos = df_2['EQUIPO'].unique().tolist()

df_3 = df_2.groupby('EQUIPO')['G'].sum().reset_index()

df_3.loc[[1, 14, 15], 'EQUIPO'] = list(map(lambda x: x.lower(),["Albacete Balompié", "Real Racing Club", "Racing Ferrol"]))

df_players = df_3

print(df_3)


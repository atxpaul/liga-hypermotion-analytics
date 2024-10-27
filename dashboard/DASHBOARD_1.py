import sys
import os
import plotly.express as px

# Agregar la carpeta 'reference_tables' al sistema de rutas
sys.path.append(os.path.join(os.path.dirname(__file__), '../reference_tables'))

# Importar los DataFrames
from tabla_ppto_jugadores import func_ppto_jugadores

df_ppto_jugadores = func_ppto_jugadores()

# Calcular el valor por gol
df_ppto_jugadores['Valor_por_gol'] = df_ppto_jugadores['Valor_de_mercado_total'] / df_ppto_jugadores['N_goles']

# Ordenar el DataFrame por 'Valor_por_gol' de mayor a menor
df_ppto_jugadores = df_ppto_jugadores.sort_values(by='Valor_por_gol', ascending=False)

# Crear gráfico de barras
fig = px.bar(df_ppto_jugadores, x='Equipo', y='Valor_por_gol', 
             title="Valor por Gol de Cada Equipo",
             labels={'Equipo': 'Equipo', 'Valor_por_gol': 'Valor por Gol (€)'},
             color_discrete_sequence=["#19204E"])

# Personalizar el título
fig.update_layout(title='<b>Valor por Gol de Cada Equipo<b>',
    title_font=dict(family='Arial Black', size=30))

# Mostrar gráfico
fig.show()


import pandas as pd
import numpy as np
import plotly.express as px

from table_budgetxplayers import df_budget_per_team
from table_popxmunixequipo import df_mun_x_team

df_budget_per_team['valor_por_gol'] = df_budget_per_team['valor_total_entero'] / df_budget_per_team['G']


fig = px.bar(df_budget_per_team, x='EQUIPO', y='valor_por_gol', title="Valor por Gol de Cada Equipo",
             labels={'EQUIPO': 'Equipo', 'valor_por_gol': 'Valor por Gol (€)'})

fig.show()

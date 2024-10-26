import pandas as pd

from table_budget import df_budget
from table_players_data import df_players

df_budget_per_team = pd.merge(df_budget, df_players, on="EQUIPO", how="inner")

print(df_budget_per_team)
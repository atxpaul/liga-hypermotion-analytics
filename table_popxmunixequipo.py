import pandas as pd 

from table_popxmuni import df_popxmuni
from table_munxestadio import df_munxestadio
from table_es_attendance import df_attendance

# pd.set_option('display.max_columns', None);

df_junto = pd.merge(df_popxmuni, df_munxestadio, on="municipio", how="inner")

df_mun_x_team = pd.merge(df_junto, df_attendance, on="CLUB", how="inner")

print (df_junto)
#print (df_mun_x_team)


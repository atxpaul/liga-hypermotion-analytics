import pandas as pd

df_1 = pd.read_csv("la_liga_2_teams.csv")

df_1 = pd.DataFrame(df_1)

columns_del = ['MANAGER', 'LIGA', 'ESTADIO', 'FUNDACIÓN']

for col in df_1.select_dtypes(include='object').columns:
    df_1[col] = df_1[col].str.lower()
df_2 = df_1.drop(columns=columns_del)

df_2 = df_2.rename(columns={'UBICACIÓN': 'municipio'}) 

df_munxestadio = df_2

print(df_munxestadio)
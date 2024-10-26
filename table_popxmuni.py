import pandas as pd

df_1 = pd.read_csv("poblacionxmunicipioesp.csv")
df_1 = pd.DataFrame(df_1)

for col in df_1.select_dtypes(include='object').columns:
    df_1[col] = df_1[col].str.lower()

df_1 = df_1.rename(columns={'Nombre': 'municipio'}) 

df_popxmuni = df_1
print(df_popxmuni)

import pandas as pd

# Cargar el DataFrame
df_1 = pd.read_csv("spanish_football_attendance.csv")

# Crear una copia del DataFrame sin las columnas especificadas
columns_del = ['Stadium', 'Spectators', 'Rank']
df_2 = df_1.drop(columns=columns_del)

# Convertir todos los valores de texto en el DataFrame a minúsculas
for col in df_2.select_dtypes(include='object').columns:
    df_2[col] = df_2[col].str.lower()

# Actualizar un subconjunto de celdas con valores específicos
df_2.loc[[1, 2, 3, 16], 'Team'] = ["real sporting", "rc deportivo", "real racing club", "racing ferrol"]

df_2 = df_2.rename(columns={'Team': 'CLUB'}) 

df_attendance = df_2
print(df_attendance)

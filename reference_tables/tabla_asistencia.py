import pandas as pd

def func_asistencia():
    # Leer el archivo CSV
    df_1 = pd.read_csv("../scrap_results/spanish_football_attendance.csv")

    # Definir columnas a eliminar
    columns_del = ['Stadium', 'Spectators', 'Rank']
    
    # Eliminar columnas no deseadas
    df_2 = df_1.drop(columns=columns_del)

    # Limpiar columnas de tipo objeto
    for col in df_2.select_dtypes(include='object').columns:
        df_2[col] = df_2[col].str.lower().str.strip()

    # Corregir nombres de equipos
    df_2.loc[[1, 2, 3, 16], 'Team'] = ["real sporting", "rc deportivo", "real racing club", "racing ferrol"]

    # Renombrar columnas
    df_2 = df_2.rename(columns={
        'Team': 'Equipo',
        'Capacity': 'Capacidad_estadio',
        'Average': 'Asistencia_media_estadio'
    })

    return df_2

if __name__ == "__main__":
    df_asistencia = func_asistencia()
    print(df_asistencia)

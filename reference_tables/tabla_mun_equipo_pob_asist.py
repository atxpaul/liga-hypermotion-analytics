import pandas as pd 

from tabla_pob_mun import func_pob_mun
from tabla_mun_equipo import func_mun_equipo
from tabla_asistencia import func_asistencia

def func_mun_equipo_pob_asist():
    # Obtener los DataFrames
    df_pob_mun = func_pob_mun()
    df_mun_equipo = func_mun_equipo()
    df_asistencia = func_asistencia()

    # Configurar pandas para mostrar todas las columnas y filas
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)

    # Fusionar DataFrames
    df_1 = pd.merge(df_pob_mun, df_mun_equipo, on="Municipio", how="inner")
    df_2 = pd.merge(df_1, df_asistencia, on="Equipo", how="inner")

    # Reemplazar NaN en "Comunidad autónoma" con los valores de "Provincia"
    df_2['Comunidad autónoma'] = df_2['Comunidad autónoma'].fillna(df_2['Provincia'])

    return df_2

if __name__ == "__main__":
    df_mun_equipo_pob_asist = func_mun_equipo_pob_asist()
    print(df_mun_equipo_pob_asist)
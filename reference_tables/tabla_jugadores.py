import pandas as pd

def func_df_jugadores():
    # Leer el archivo JSON
    df_1 = pd.read_json("../scrap_results/players_data.json")

    # Seleccionar columnas relevantes
    df_2 = df_1[['NOMBRE', 'EQUIPO', 'G']]
    
    # Limpiar y normalizar el nombre del equipo
    df_2.loc[:, 'EQUIPO'] = df_2['EQUIPO'].str.lower().str.strip()

    # Contar nombres únicos
    count_distinct_nombres = df_2['EQUIPO'].nunique()
    lista_valores_unicos = df_2['EQUIPO'].unique().tolist()

    # Agrupar por equipo y sumar goles
    df_3 = df_2.groupby('EQUIPO')['G'].sum().reset_index()

    # Reemplazar nombres específicos
    df_3.loc[[1, 14, 15], 'EQUIPO'] = ["albacete balompié", "real racing club", "racing ferrol"]

    # Renombrar columnas
    df_3 = df_3.rename(columns={
        'EQUIPO': 'Equipo',
        'G': 'N_goles'
    })

    return df_3

if __name__ == "__main__":
    df_jugadores = func_df_jugadores()
    print(df_jugadores)



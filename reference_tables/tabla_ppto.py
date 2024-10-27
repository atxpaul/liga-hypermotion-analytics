import pandas as pd

def convertir_a_entero(valor):
    valor = valor.replace('mill. €', '').replace('mil €', '').replace(',', '.').strip()
    return int(float(valor) * 1_000_000)

def func_df_ppto():
    # Leer el archivo CSV
    df_budget_1 = pd.read_csv("../scrap_results/team_budget.csv")

    # Realizar la copia de las primeras 22 filas
    df_sin_filas = df_budget_1.iloc[:22].copy()

    # Aplicar la conversión de valores a entero
    for col in ['valor_total', 'valor_promedio']:
        df_sin_filas[f'{col}_entero'] = df_sin_filas[col].apply(convertir_a_entero)

    # Eliminar columnas innecesarias
    df_sin_filas = df_sin_filas.drop(['valor_total', 'valor_promedio', 'extranjeros'], axis=1)

    # Limpiar y normalizar nombres
    df_sin_filas['nombre'] = df_sin_filas['nombre'].str.lower().str.strip()
    df_sin_filas.loc[[7, 11, 17], 'nombre'] = ["real sporting", "rc deportivo", "racing ferrol"]

    # Renombrar columnas
    df_sin_filas = df_sin_filas.rename(columns={
        'nombre': 'Equipo',
        'jugadores': 'Jugadores',
        'edad': 'Jugador_edad_media',
        'valor_promedio_entero': 'Valor_de_mercado_promedio',
        'valor_total_entero': 'Valor_de_mercado_total'
    })
    
    # Definir el orden de las columnas
    columnas_ordenadas = ['Equipo', 'Jugadores', 'Jugador_edad_media', 'Valor_de_mercado_promedio', 'Valor_de_mercado_total']
    df_ppto = df_sin_filas[columnas_ordenadas]
    
    return df_ppto

if __name__ == "__main__":
    df_ppto_final = func_df_ppto()
    print(df_ppto_final)

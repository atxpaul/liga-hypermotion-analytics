import pandas as pd

def func_pob_mun():
    # Leer el archivo CSV
    df_1 = pd.read_csv("../scrap_results/poblacionxmunicipioesp.csv")

    # Realizar la conversión a DataFrame (opcional, ya que read_csv ya devuelve un DataFrame)
    df_1 = pd.DataFrame(df_1)

    # Limpiar columnas de tipo objeto
    for col in df_1.select_dtypes(include='object').columns:
        df_1[col] = df_1[col].str.lower().str.strip()

    # Renombrar columnas
    df_1 = df_1.rename(columns={'Nombre': 'Municipio', 'Población\r\n(1 de enero de 2023)': 'Poblacion'})
    
    # Eliminar la columna no deseada
    df_1 = df_1.drop(['N.º'], axis=1)

    # Limpiar y convertir la población a entero
    df_1['Poblacion'] = df_1['Poblacion'].str.replace(' ', '').astype(int)

    return df_1

if __name__ == "__main__":
    df_pob_mun = func_pob_mun()
    print(df_pob_mun)

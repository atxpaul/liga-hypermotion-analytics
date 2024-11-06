import pandas as pd

def func_mun_equipo():
    # Leer el archivo CSV
    df_1 = pd.read_csv("../scrap_results/la_liga_2_teams.csv")

    # Realizar la conversión a DataFrame (opcional, ya que read_csv ya devuelve un DataFrame)
    df_1 = pd.DataFrame(df_1)

    # Definir columnas a eliminar
    columns_del = ['MANAGER', 'LIGA', 'ESTADIO', 'FUNDACIÓN']
    
    # Eliminar columnas no deseadas
    df_2 = df_1.drop(columns=columns_del)

    # Limpiar columnas de tipo objeto
    for col in df_2.select_dtypes(include='object').columns:
        df_2[col] = df_2[col].str.lower().str.strip()    
    
    # Renombrar columnas
    df_2 = df_2.rename(columns={'UBICACIÓN': 'Municipio', 'CLUB': 'Equipo'}) 
    
    # Renombrar municipios que no están correctamente nombrados
    # Agregar según sea necesario
    renombrar_municipios = {
        'tenerife': 'santa cruz de tenerife',
        'castellon': 'castelló de la plana',
        'valencia': 'valència',
        'elche': 'elx/elche'}
    
    df_2['Municipio'] = df_2['Municipio'].replace(renombrar_municipios)

    return df_2

if __name__ == "__main__":
    df_mun_equipo = func_mun_equipo()
    print(df_mun_equipo)

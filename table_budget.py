import pandas as pd

# Cargar el DataFrame
df_test = pd.read_csv("./team_budget.csv")

# Seleccionar las primeras 22 filas y convertir todos los valores de texto a minúsculas
df_sin_filas = df_test.iloc[:22].applymap(lambda x: x.lower() if isinstance(x, str) else x)

# Crear un nuevo DataFrame
df_2 = pd.DataFrame(df_sin_filas)

# Función para convertir el string al valor entero
def convertir_a_entero(valor):
    # Eliminar los caracteres innecesarios
    valor = valor.replace('mill. €', '').replace('mil €', '').replace(',', '.').strip()
    # Convertir a float y multiplicar por 1 millón
    valor_numerico = float(valor) * 1_000_000
    # Convertir a entero
    return int(valor_numerico)

# Aplicar la función a las columnas numéricas
df_2['valor_total_entero'] = df_2['valor_total'].apply(convertir_a_entero)
df_2['valor_promedio_entero'] = df_2['valor_promedio'].apply(convertir_a_entero)

# Eliminar las columnas originales
df_2 = df_2.drop(['valor_total', 'valor_promedio'], axis=1)

# Cambiar el valor específico en minúsculas para la fila 17
df_2.loc[17, 'nombre'] = "racing ferrol"

# Renombrar la columna para que coincida con el formato esperado en el mapeo
df_2 = df_2.rename(columns={'nombre': 'EQUIPO'})

# Copiar df_2 a df_budget, preservando todo el código original
df_budget = df_2.copy()

# Asegurar que todos los nombres en 'EQUIPO' estén en minúsculas y quitar espacios antes del mapeo
df_budget["EQUIPO"] = df_budget["EQUIPO"].str.lower().str.strip()

# Diccionario de mapeo para los nombres de equipos
nombre_equipos = {
    "ud almería": "ud almería",
    "granada cf": "granada cf",
    "real zaragoza": "real zaragoza",
    "real oviedo": "real oviedo",
    "elche cf": "elche cf",
    "cádiz cf": "cádiz cf",
    "real racing club": "real racing club",
    "real sporting de gijón": "real sporting",  # Confirmar si se debe cambiar
    "levante ud": "levante ud",
    "burgos cf": "burgos cf",
    "sd eibar": "sd eibar",
    "rc deportivo de la coruña": "rc deportivo",  # Confirmar si se debe cambiar
    "cd tenerife": "cd tenerife",
    "sd huesca": "sd huesca",
    "albacete balompié": "albacete balompié",
    "málaga cf": "málaga cf",
    "cd castellón": "cd castellón",
    "racing ferrol": "racing ferrol",
    "cd eldense": "cd eldense",
    "fc cartagena": "fc cartagena",
    "cd mirandés": "cd mirandés",
    "córdoba cf": "córdoba cf"
}

# Aplicar el mapeo al DataFrame
df_budget["EQUIPO"] = df_budget["EQUIPO"].replace(nombre_equipos)

# Verificar el resultado
print(df_budget)

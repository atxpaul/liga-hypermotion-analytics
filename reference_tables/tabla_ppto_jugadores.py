import pandas as pd

from tabla_ppto import func_df_ppto
from tabla_jugadores import func_df_jugadores

def func_ppto_jugadores():
    df_ppto = func_df_ppto()
    df_jugadores = func_df_jugadores()

    df_conjunto_ppto_jugadores = pd.merge(df_ppto, df_jugadores, on="Equipo", how="inner")

    return df_conjunto_ppto_jugadores

if __name__ == "__main__":
    df_ppto_jugadores = func_ppto_jugadores()
    print(df_ppto_jugadores)

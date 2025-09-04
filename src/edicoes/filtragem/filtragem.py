from pathlib import Path
from typing import Union, cast
import dask.dataframe as dd
from leituras.ler_arquivos import ler_arquivo

def filtra_estacao(dataframe_diretorio_relativo: Union[str, Path], estacoes: Union[str, list]) -> dd.DataFrame:
    """Filtra um dataframe por uma estação ou lista de estações.
    
    Args:
        dataframe_diretorio_relativo (str | Path): Diretório relativo onde está o dataframe. É relativo à "data/dataframes".

        estacoes (str | list): Estação ou lista de estações pelas quais se deseja filtrar.
    """

    #dataframe_diretorio_relativo = 
    df = ler_arquivo("parquet", dataframe_diretorio_relativo)
    df = cast(dd.DataFrame, df)  # Garantir que o dataframe é do tipo Dask DataFrame

    df_filtrado = df[df["estacao"].isin(estacoes) if isinstance(estacoes, list) else df["estacao"] == estacoes]
    #df_filtrado = df_filtrado.persist()  # Persistir o dataframe filtrado para otimizar o desempenho
    return df_filtrado


if __name__ == "__main__":

    import pandas as pd
    pd.set_option('display.max_columns', None)

    df_filtrado = filtra_estacao("coordenadas_especificas/plataformas/p1-NAMORADO_2_(PNA-2)", "Inverno")
    #print(df_filtrado.head())
    #print(df_filtrado.tail())
    print(df_filtrado.compute())
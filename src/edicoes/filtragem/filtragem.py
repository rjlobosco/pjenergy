from typing import Union
import dask.dataframe as dd

from leituras.ler_arquivos_pastas_especificas import ler_dataframes_pontuais_plataformas_geral


def filtra_estacao(plataforma_representacao: str, estacoes: Union[str, list]) -> dd.DataFrame:
    """Filtra um dataframe por uma estação ou lista de estações.
    
    Args:
        dataframe_diretorio_relativo (str | Path): Diretório relativo onde está o dataframe. É relativo à "data/dataframes".

        estacoes (str | list): Estação ou lista de estações pelas quais se deseja filtrar.
    """

    df = ler_dataframes_pontuais_plataformas_geral(plataforma_representacao)

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
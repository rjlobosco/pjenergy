from pathlib import Path
import xarray as xr
from typing import Literal
import dask.dataframe as dd

from utils.existencia_path import verifica_erro_nao_existe_path
from leituras.ler_datasets import ler_dataset_nc
from leituras.ler_dataframes import ler_dataframe_parquet
from config.constants import FormatosDados as fa
from utils.monta_path_absoluto import monta_path_absoluto
from utils.str_para_path import str_para_path



# FUNÇÃO PRINCIPAL -------------------------------------------------------------------------------


def ler_arquivo(path: Path | str, formato_arquivo: Literal["netcdf", "parquet"], path_absoluto_bool: bool = False) -> xr.Dataset | dd.DataFrame:
    """Lê arquivos de dados.
    Args:
        path (Path | str): Path do arquivo a ser lido. Pode ser um Path ou uma string. Por padrão
            é um caminho relativo ao caminho do projeto. Pode ser escolhido um caminho absoluto, mudando path_absoluto_bool para False.
        formato_arquivo: Formato do arquivo a ser lido.
            Examples: "netcdf", "parquet".
        path_absoluto_bool (bool): Define se o caminho é absoluto (True) ou relativo ao projeto (False - padrão)

    Returns:
        xr.Dataset: Dataset lido.
        dd.DataFrame: Dataframe lido.
    """

    # Para manter em um formato padrão (path) para os seguintes processos
    path = str_para_path(path)

    path_absoluto = monta_path_absoluto(path, path_absoluto_bool)

    # Verifica a existência do caminho
    verifica_erro_nao_existe_path(path)

    if formato_arquivo == fa.NETCDF:
        d = ler_dataset_nc(path_absoluto)
    elif formato_arquivo == fa.PARQUET:
        d = ler_dataframe_parquet(path_absoluto)

    return d

if __name__ == "__main__":

    # EXEMPLOS:

    # Configura o pandas para mostrar todas as colunas
    import pandas as pd
    pd.set_option('display.max_columns', None)
    

    d1 = ler_arquivo("data/datasets/unido/dataset_unido.nc", "netcdf")
    print(d1)
    d2 = ler_arquivo("data/dataframes/pontuais/plataformas/geral/p3-PETROBRAS_32_(P-32)", "parquet")
    print(d2.compute())
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



# FUNÇÃO AUXILIAR -------------------------------------------------------------------------------


# def identifica_caminho_base_padrao(formato_dados: str) -> Path:
#     """Identifica o caminho base da pasta de dados de acordo com o formato dos dados desejado
    
#     Args:
#         formato_dados (str): Formato dos dados desejado.

#     Returns:
#         Path: Caminho base da pasta de dados.

#     Raises:
#         ValueError: Erro quando o formato usado não é aceito.
    
#     """

#     if formato_dados not in fa.FORMATOS_ACEITOS:
#         raise ValueError(f"Formato... \n-> {formato_dados} \n...não aceito.")
#     elif formato_dados == fa.ARQUIVO:
#         caminho_base_padrao = PathsDados.Datasets.BASE
#     elif formato_dados == fa.PARQUET:
#         caminho_base_padrao = PathsDados.Dataframes.BASE

#     return caminho_base_padrao



# FUNÇÃO PRINCIPAL -------------------------------------------------------------------------------


# def ler_arquivo(formato_arquivo: Literal["netcdf", "parquet"],
#                 path: Path | str, 
#                 eh_caminho_relativo: bool = True, 
#                 caminho_base: Path | Literal["padrao"] = "padrao") -> xr.Dataset | dd.DataFrame:
#     """Lê um arquivo de acordo com o tipo de arquivo e o path fornecido.

#     Args:
#         formato_arquivo: Formato do arquivo a ser lido.
#             Examples: "netcdf", "parquet".
#         path: Caminho do arquivo a ser lido. Pode ser um Path ou uma string. 
#             No caso de dask dataframes, o caminho deve ser de uma pasta onde os arquivos estão armazenados. 
#             Mas também pode ser passado o caminho de um arquivo parquet específico, que será lido como um dask dataframe.
#         eh_caminho_relativo: Se o caminho é relativo ao caminho base. Se for True, o caminho será concatenado com o caminho base.
#         caminho_base: Caminho base a ser usado caso o caminho seja relativo. 
#             Se for "padrao", o caminho base será identificado de acordo com o formato do arquivo. 
#             Se for passado um caminho, ele será usado como caminho base.
    
#     Returns:
#         xr.Dataset: Dataset lido se o formato de arquivo passado for "netcdf".
        
#         dd.DataFrame: Dataframe lido se o formato de arquivo passado for "parquet".
#     """

#     # Para manter em um formato padrão (path) para os seguintes processos
#     if isinstance(path, str):
#         path = Path(path)

#     # Caso o caminho seja relativo e exige o caminho base padrão, que varia de acordo com o tipo de arquivo
#     if eh_caminho_relativo and caminho_base == "padrao":
#         caminho_base = identifica_caminho_base_padrao(formato_arquivo)

#     # Se o caminho passado é relativo, monta o caminho absoluto
#     if eh_caminho_relativo:
#         path = caminho_base / path

#     # Verifica a existência do caminho
#     verifica_erro_nao_existe_path(path)


#     if formato_arquivo == fa.NETCDF:
#         d = ler_dataset_nc(path)
#     elif formato_arquivo == fa.PARQUET:
#         d = ler_dataframe_parquet(path)

#     return d

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
    
    # #d = ler_arquivo("netcdf", "unido/dataset_unido.nc")
    # d = ler_arquivo("parquet", "coordenadas_especificas/plataformas/p1-NAMORADO_2_(PNA-2)")
    # print(d.compute())
    # print(d.columns)
    # d = ler_arquivo("parquet", "coordenadas_especificas/plataformas/p1-NAMORADO_2_(PNA-2)/part.0.parquet")
    # print(d.compute())

    d1 = ler_arquivo("data/datasets/unido/dataset_unido.nc", "netcdf")
    print(d1)
    d2 = ler_arquivo("data/dataframes/coordenadas_especificas/plataformas/p3-PETROBRAS_32_(P-32)", "parquet")
    print(d2.compute())
from pathlib import Path
import xarray as xr
from typing import Literal
import dask.dataframe as dd

from utils.existencia_path import verifica_erro_nao_existe_path
from config.paths import PathsDados
from leituras.ler_datasets import ler_dataset_nc
from leituras.ler_dataframes import ler_dataframe_parquet
from config.constants import FormatosArquivo as fa


# FUNÇÃO AUXILIAR -------------------------------------------------------------------------------


def identifica_caminho_base_padrao(formato_arquivo: str) -> Path:
    """Identifica o caminho base da pasta de dados de acordo com o tipo de arquivo desejado
    
    Args:
        formato_arquivo (str): Formato do arquivo que se quer identificar o caminho.

    Returns:
        Path: Caminho base da pasta de dados.

    Raises:
        ValueError: Erro quando o formato usado não é aceito.
    
    """

    if formato_arquivo not in fa.FORMATOS_ACEITOS:
        raise ValueError(f"Formato... \n-> {formato_arquivo} \n...não aceito.")
    elif formato_arquivo == fa.NETCDF:
        caminho_base_padrao = PathsDados.Datasets.BASE
    elif formato_arquivo == fa.PARQUET:
        caminho_base_padrao = PathsDados.Dataframes.BASE

    return caminho_base_padrao



# FUNÇÃO PRINCIPAL -------------------------------------------------------------------------------


def ler_arquivo(formato_arquivo: Literal["netcdf", "parquet"],
                path: Path | str, 
                eh_caminho_relativo: bool = True, 
                caminho_base: Path | Literal["padrao"] = "padrao") -> xr.Dataset | dd.DataFrame:
    """Lê um arquivo de acordo com o tipo de arquivo e o path fornecido.

    Args:
        formato_arquivo: Formato do arquivo a ser lido.
            Examples: "netcdf", "parquet".
        path: Caminho do arquivo a ser lido. Pode ser um Path ou uma string. 
            No caso de dask dataframes, o caminho deve ser de uma pasta onde os arquivos estão armazenados. 
            Mas também pode ser passado o caminho de um arquivo parquet específico, que será lido como um dask dataframe.
        eh_caminho_relativo: Se o caminho é relativo ao caminho base. Se for True, o caminho será concatenado com o caminho base.
        caminho_base: Caminho base a ser usado caso o caminho seja relativo. 
            Se for "padrao", o caminho base será identificado de acordo com o formato do arquivo. 
            Se for passado um caminho, ele será usado como caminho base.
    
    Returns:
        xr.Dataset: Dataset lido se o formato de arquivo passado for "netcdf".
        
        dd.DataFrame: Dataframe lido se o formato de arquivo passado for "parquet".
    """

    # Para manter em um formato padrão (path) para os seguintes processos
    if isinstance(path, str):
        path = Path(path)

    # Caso o caminho seja relativo e exige o caminho base padrão, que varia de acordo com o tipo de arquivo
    if eh_caminho_relativo and caminho_base == "padrao":
        caminho_base = identifica_caminho_base_padrao(formato_arquivo)

    # Se o caminho passado é relativo, monta o caminho absoluto
    if eh_caminho_relativo:
        path = caminho_base / path

    # Verifica a existência do caminho
    verifica_erro_nao_existe_path(path)


    if formato_arquivo == fa.NETCDF:
        d = ler_dataset_nc(path)
    elif formato_arquivo == fa.PARQUET:
        d = ler_dataframe_parquet(path)

    return d



if __name__ == "__main__":

    # EXEMPLOS:

    # Configura o pandas para mostrar todas as colunas
    import pandas as pd
    pd.set_option('display.max_columns', None)
    
    #d = ler_arquivo("netcdf", "unido/dataset_unido.nc")
    d = ler_arquivo("parquet", "coordenadas_especificas/plataformas/p1-NAMORADO_2_(PNA-2)")
    print(d.compute())
    print(d.columns)
    d = ler_arquivo("parquet", "coordenadas_especificas/plataformas/p1-NAMORADO_2_(PNA-2)/part.0.parquet")
    print(d.compute())


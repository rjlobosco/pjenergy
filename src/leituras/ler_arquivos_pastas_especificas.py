
import xarray as xr
import dask.dataframe as dd
from typing import Literal, cast

from leituras.ler_arquivos import ler_arquivo
from config.paths import Datasets, Dataframes
from utils.gerencia_plataformas_representacoes import gerencia_plataforma_representacoes
from utils.obtem_dados_plataformas import plataforma_para_arquivo_nome, plataforma_para_pasta_nome
from config.constants import Plataformas
from config.constants import Correspondencias as cr


# Datasets

def ler_datasets_original(arquivo_nome: str, formato_arquivo: Literal["netcdf"] = "netcdf") -> xr.Dataset:
    caminho = Datasets.DIRETORIO_ORIGINAIS / arquivo_nome
    dataset = ler_arquivo(caminho, formato_arquivo, True)
    dataset = cast(xr.Dataset, dataset)
    return dataset

def ler_dataset_unido(formato_arquivo: Literal["netcdf"] = "netcdf")-> xr.Dataset:
    dataset = ler_arquivo(Datasets.CAMINHO_UNIDO, formato_arquivo, True)
    dataset = cast(xr.Dataset, dataset)
    return dataset

def ler_datasets_pontuais_plataformas_geral(plataforma_representacao: str, formato_arquivo: Literal["netcdf"] = "netcdf")-> xr.Dataset:
    plataforma = gerencia_plataforma_representacoes(plataforma_representacao)
    arquivo_nome = plataforma_para_arquivo_nome(plataforma)
    caminho = Datasets.DIRETORIO_PLATAFORMAS_GERAL / arquivo_nome
    dataset = ler_arquivo(caminho, formato_arquivo, True)
    dataset = cast(xr.Dataset, dataset)
    return dataset





# Dataframes

def ler_dataframes_pontuais_plataformas_geral(plataforma_representacao, formato_arquivo: Literal["parquet"] = "parquet") -> dd.DataFrame:
    plataforma = gerencia_plataforma_representacoes(plataforma_representacao)
    pasta_nome = plataforma_para_pasta_nome(plataforma)
    caminho = Dataframes.DIRETORIO_PLATAFORMAS_GERAL / pasta_nome
    dataframe = ler_arquivo(caminho, formato_arquivo, True)
    dataframe = cast(dd.DataFrame, dataframe)
    return dataframe




if __name__ == "__main__":


    dataset = ler_datasets_original("(var-geopotential)_(ano-2017)_(pressao-950).nc")
    print(f"1){dataset}\n")
    dataset = ler_dataset_unido()
    print(f"2){dataset}\n")
    dataset = ler_datasets_pontuais_plataformas_geral("p5")
    print(f"3){dataset}\n")


    # Configura o pandas para mostrar todas as colunas
    import pandas as pd
    pd.set_option('display.max_columns', None)

    dataframe = ler_dataframes_pontuais_plataformas_geral("p4")
    print(f"4){dataframe.compute()}\n")
from typing import Optional
from geracoes.gera_datasets_editados import gera_datasets_editados_pontuais
from geracoes.gera_dataframes import nc_para_dask_dataframe_plataformas
from edicoes.unioes.une_nc import unifica_datasets

def montagem_dados() -> None:
    """
    Unifica os datasets obtidos pela API do CDS, monta datasets editados para localizações específicas e 
    depois cria dataframes a partir destes datasets editados
    """

    unifica_datasets()

    gera_datasets_editados_pontuais()

    nc_para_dask_dataframe_plataformas()


if __name__ == "__main__":
    montagem_dados()
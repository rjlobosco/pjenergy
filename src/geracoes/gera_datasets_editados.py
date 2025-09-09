from typing import cast
import xarray as xr

from config.constants import Plataformas
from leituras.ler_arquivos_pastas_especificas import ler_dataset_unido
from salvamentos.salva_datasets import salva_dataset_nc
from config.paths import Datasets
from edicoes.limpezas.remove_de_datasets import remove_variaveis_indesejadas
from edicoes.interpolacoes.interpola_em_datasets import dataset_interpola_lat_lon, interpola_varias_variaveis_em_altura
from edicoes.adicoes.adiciona_a_datasets import adiciona_variaveis
from edicoes.renomeacoes.renomeia_em_datasets import dataset_renomeacoes
from utils.representa_progresso import representa_progresso
from utils.obtem_dados_plataformas import plataforma_para_arquivo_nome


# FUNÇÃO AUXILIARR ----------------------------------------

def processa_edicoes(plataforma: str, latitude_longitude_alvo: tuple[float, float]) -> xr.Dataset:
    """Chama as várias funções que realizam edições sequenciais no dataset único para criar um dataset para uma coordenada específica.
    
    Args: 
        plataforma (str): Nome da plataforma cujo dados se deseja obter.
        latitude_longitude_alvo (tuple[float, float]): Coordenadas caso não seja escolhida uma plataforma.
    Returns: 
        xr.Dataset: Dataset após o processamento de todas as edições.
    """

    print("Editando...\n")
    
    # Lê dataset (verificando se o dataset existe)
    ds = ler_dataset_unido()
   
    # Lista de processo a ser aplicado
    processos = [remove_variaveis_indesejadas, 
                 dataset_interpola_lat_lon,  
                 interpola_varias_variaveis_em_altura,
                 adiciona_variaveis,
                 dataset_renomeacoes]

    # Aplicações sequnecial de cada processo
    for funcao in processos:
        if funcao == dataset_interpola_lat_lon:
            ds = funcao(ds, latitude_longitude_alvo)
        else:
            ds = funcao(ds)
        #print(f"Função: {funcao} \n{ds}")

    print("Editado.\n")

    arquivo_nome = plataforma_para_arquivo_nome(plataforma)
    salva_dataset_nc(ds, Datasets.DIRETORIO_PLATAFORMAS_GERAL / arquivo_nome)

    ds = cast(xr.Dataset, ds)
    return ds


# FUNÇÃO PRINCIPAL ----------------------------------------


def gera_datasets_editados_pontuais() -> None :
    """Gera um ou vários datasets editados de ponto geográficos específicos, a partir do dataset unido. 

    Returns: 
        xr.Dataset: Dataset após o processamento de todas as edições. 

    Raises:
        ValueError: Erro quando `usa_plataformas` é False, mas não são passadas coordenas específicas.
    """

    print("--- EDIÇÃO DE DATASET(S) ---\n\n")

    
    plataformas_dados = Plataformas.DADOS
    i = 1

    for plat in Plataformas.PLATAFORMAS:
        print(f" -> -> -> Plataforma: {plat} ({representa_progresso(i, Plataformas.PLATAFORMAS)})\n")
        latitude_longitude_alvo = plataformas_dados[plat]["coords"]
        processa_edicoes(plat, latitude_longitude_alvo)  
        i += 1

    # return ds    # Retorna o dataset da última plataforma


if __name__ == "__main__":

    ds = gera_datasets_editados_pontuais()


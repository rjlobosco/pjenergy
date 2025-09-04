import re
import xarray as xr
from typing import Optional
from config.paths import Datasets
from config.constants import ArquivosNomes as an
from salvamentos.salva_datasets import salva_dataset_nc
from utils.pega_arquivos import pega_arquivos

# FUNÇÕES AUXILIARES

def variaveis_match(arquivo: str) -> tuple[Optional[str], Optional[str], Optional[str]]: 
    """Captura informações de variável, ano e nível de pressão a partir do nome do arquivo através de expressão regular.
    
    Args:
        arquivo (str): Nome do arquivo.

    Returns:
        tuple: Tupla com a variável, ano e pressão, respectivamente.
        Caso, o nome do arquivo não dê match com a expressão regular, a tupla retorna (None, None, None).
    """

    # Utiliza expressão regular para capturar os grupos de interesse do nome dos arquivos que seguem o padrão
    match = re.search(an.PADRAO_ARQUIVOS_NC_ORIGINAIS_REGEX, arquivo) 

    if match:
        variavel, ano, nivel_pressao = match.groups()
        return variavel, ano, nivel_pressao
    else:
        return None, None, None


def constroi_parametros_dicio() -> dict:
    """Dado o diretório, obtém datasets para os conjuntos dos parâmetros utilizados de variáveis, anos e níveis de pressão.

    Returns:
        dict: Retorna um dicionário aninhado, no formato {variavel: {nivel_pressao: {ano: dataset}}}.
    """

    # Obtém os arquivos do diretório que seguem o padrão de nome esperado
    arquivos = pega_arquivos(Datasets.DIRETORIO_ORIGINAIS)   

    # Cria um dicionário aninhado para armazenar os datasets das combinações de variáveis, anos e níveis de pressão
    print(" -> -> -> Etapa (2/5)\n")
    print("Organizando datasets em dicionários aninhados...\n")
    parametros_dicio = {}
    for arquivo in arquivos:
        variavel, ano, nivel_pressao = variaveis_match(arquivo) # Captura os parâmetros a partir do nome do arquivo
        if not variavel or not ano or not nivel_pressao:
            print(f"Arquivo que não segue o padrão de nome desconsiderado: {arquivo}")
        elif variavel and ano and nivel_pressao:
            # Para armazenar o ano e o nível de pressão como inteiros
            ano = int(ano) 
            nivel_pressao = int(nivel_pressao) 
            # Verifica se a variável, nível de pressão e ano já existem no dicionário
            # Se não existirem, cria as chaves e adiciona o dataset
            if variavel not in parametros_dicio:
                parametros_dicio[variavel] = {}
            if nivel_pressao not in parametros_dicio[variavel]:
                parametros_dicio[variavel][nivel_pressao] = {}
            if ano not in parametros_dicio[variavel][nivel_pressao]:
                parametros_dicio[variavel][nivel_pressao][ano] = xr.open_dataset(arquivo)

    print("Organização dos datasets em dicionários finalizada.\n\n")
    return parametros_dicio


# ---------------------------------------------
# FUNÇÕES INTERMEDIÁRIAS (pré-processamento e estruturação de dados)


def concatena_datasets() -> dict:
    """Concatena os datasets de níveis de pressão e anos diferentes.
    
    Returns:
        dict: Dicionário com um dataset para cada variável, no formato {variavel: dataset, ...} .
    """

    # Obtém os dicionários de parâmetros, com os datasets das combinações de variáveis, anos e níveis de pressão
    parametros_dicio = constroi_parametros_dicio() # {variavel: {nivel_pressao: {ano: dataset, ...}, ...}, ...}
    
    # Concatena os datasets de anos para cada nível de pressão, e depois concatena os níveis de pressão para cada variável
    print(" -> -> -> Etapa (3/5)\n")
    print("Concatenando datasets de diversos níveis de pressão e anos...\n")
    for variavel_chave in parametros_dicio.keys():

        dataset_pressoes_lista = [] # Lista para armazenar datasets de todas as pressões, para determinada variável
        pressoes_dict = parametros_dicio[variavel_chave] # Dicionário de todas pressões para determinada variável  -> {nivel_pressao: {ano: dataset, ...}, ...}

        for pressao_chave in sorted(pressoes_dict.keys()): # Ordena os níveis de pressão em ordem crescente

            dataset_anos_lista = [] # Lista para armazenar datasets de todos os anos, para determinada combinação de variável e pressão
            anos_dict = pressoes_dict[pressao_chave] # Dicionário de todos os anos para determinada combinação variável e nível de pressão -> {ano: dataset, ...}

            for ano_chave in anos_dict.keys():

                dataset_anos = anos_dict[ano_chave]  # Dataset que representa uma combinação específica de variável, pressão e ano.
                dataset_anos_lista.append(dataset_anos) 

            # Concatena os datasets de anos ao longo da dimensão "valid_time", para cada combinação de variável e pressão
            dataset_pressoes = xr.concat(
                dataset_anos_lista, 
                dim = "valid_time")
            dataset_pressoes_lista.append(dataset_pressoes)

        # Concatena os datasets de diferentes níveis de pressão ao longo da dimensão "pressure_level", para cada variável
        parametros_dicio[variavel_chave] = xr.concat(
            dataset_pressoes_lista,
            dim="pressure_level")

    print("Concatenação finalizada.\n\n")
    return parametros_dicio  # {variavel: dataset, ...}


def merge_datasets(variaveis_dicio: dict) -> xr.Dataset:
    """Mescla os datasets das diversas variáveis.
    
    Args:
        variaveis_dicio (dict): Dicinário com um dataset para cada variável, no formato {variavel: dataset, ...}.

    Returns:
        xr.Dataset: Dataset composto pela mesclagem dos datasets de cada variável.
    """

    # Faz uma lista dos datasets de variáveis
    variaveis_datasets = list(variaveis_dicio.values())

    # Mescla os datasets de variáveis em um único dataset
    print("Unindo datasets de todas as variáveis...\n")
    dataset_unico = xr.merge(variaveis_datasets)
    print(f"Dataset único gerado, com {len(dataset_unico.data_vars)} variáveis em {len(dataset_unico.pressure_level)} alturas.\n\n")
    
    return dataset_unico  


# ---------------------------------------------
# FUNÇÃO PRINCIPAL

def unifica_datasets() -> xr.Dataset:
    """Gera um dataset único a partir da combinação dos vários datasets originais.
    Caso o dataset já exista, ele será substituído.
    
    Returns:
        xr.Dataset: Dataset unificado.
    """

    print("\n--- UNIFICAÇÃO DE DATASETS ---\n\n")

    # Concatena os datasets de diferentes níveis de pressão e anos
    print(" -> -> -> Etapa (1/5)\n")
    variaveis_dicio = concatena_datasets()

    # Mescla os datasets de todas variáveis
    print(" -> -> -> Etapa (4/5)\n")
    dataset_unido = merge_datasets(variaveis_dicio)

    # Salva o dataset em um arquivo NetCDF único
    print(" -> -> -> Etapa (5/5)\n")
    salva_dataset_nc(dataset_unido, Datasets.CAMINHO_UNIDO)

    print("Datasets unificados com sucesso!\n\n")

    return dataset_unido


if __name__ == "__main__":
    dataset_unido = unifica_datasets()
    print(dataset_unido)
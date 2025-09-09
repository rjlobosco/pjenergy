
"""Para obtenção de dados de um dataset do Climate Data Store"""

from typing import Literal, cast
import cdsapi
from pathlib import Path
from config.paths import Datasets
from config.constants import ParametrosObtencaoDados as pod
from utils.existencia_path import garante_path_pai_existencia, verifica_erro_ja_existe_arquivo, existe_path_e_exibe_mensagem
from utils.verifica_argumentos_padrao import erro_algum_parametro_diferente_do_padrao, erro_algum_parametro_igual_ao_padrao



# FUNÇÕES AUXILIARES ----------------------------------------

def gera_porcentagem_progresso(n_total: int, n_atual: int) -> float:
    """Calcula a porcentagem de progresso de um processo.

    Args:
        n_total: Número total de processos.
        n_atual: Número atual de processos concluídos.
    
    Returns: 
        float: Porcentagem cumprida (%)
    """

    porcentagem_cumprida = round(100 * n_atual/n_total, 2)
    return porcentagem_cumprida



def exibe_progresso(n_atual: int, n_total: int) -> None:
    """Printa o progresso de um processo.
    
    Args:
        n_atual (int): Etapa atual.
        n_total (int): Número total de etapas.
    """
    porcentagem = gera_porcentagem_progresso(n_total, n_atual)
    print(f" -> -> -> Progresso atual: {n_atual}/{n_total} ({porcentagem}%)\n\n {'-'*100} \n")




def gera_nome_arquivo_nc_padrao(variavel: str, ano: int, pressao_nivel: int) -> str:
    """Gera o nome do arquivo .nc baseado na variável, ano e nível de pressão.
    
    Args:
        variavel (str): Variável considerada.
        ano (int): Ano considerado.
        pressao_nivel (int): Nível de pressão considerado.

    Returns:
        str: Nome do arquivo
    """

    return f"(var-{variavel})_(ano-{ano})_(pressao-{pressao_nivel}).nc" 
# ATENÇÃO!!
# Essa formatação do nome do arquivo é muito importante para manter a consistência 
# e facilitar a identificação dos arquivos baixados.
# Não é recomendado, mas tenha certeza do que está fazendo se for alterar.



def calcula_combinacoes(variaveis: tuple, anos: tuple, pressao_niveis: tuple) -> int:
    """Calcula o número total de requisições contando o número de combinações de variáveis, anos e níveis de pressão.
    
    Args:
        variaveis (tuple): Tupla de variáveis.
        anos (tuple): Tupla de anos.
        pressao_niveis (tuple): Tupla de níveis de pressão.

    Returns:
        int: Número total de requisições 
    """
    n_requisicoes = len(variaveis) * len(anos) * len(pressao_niveis)
    print(f"\n -> -> -> Número total de requisições: {n_requisicoes}\n")
    return n_requisicoes


def prepara_arquivo_para_download(caminho: Path, substituir: bool = False) -> str:
    """Prepara o diretório, verifica se o arquivo já existe e retorna o nome do arquivo.

    Args: 
        caminho (Path): Caminho do arquivo.
        substituir (bool): True para permitir a substituição do arquivo caso já exista.
            False levanta um erro caso o arquivo já exista.
    
    Returns:
        str: Nome do arquivo extraído do caminho dele.
    """
    garante_path_pai_existencia(caminho)

    nome = caminho.name
    print(f"\n -> -> -> Nome do arquivo atual: {nome}\n")

    if not substituir:
        verifica_erro_ja_existe_arquivo(caminho, f"\n -> -> -> Erro: O arquivo {nome} já existe. \
                                        Para substituí-lo, mude o parâmetro 'substituir' para True.")

    return nome




# FUNÇÕES INTERMEDIÁRIAS ----------------------------------------

def requisita_unica_combinacao(
                    dataset_salvamento_caminho: Path,
                    variavel: str, 
                    ano: int, 
                    pressao_nivel: int,  
                    substituir: bool = False) -> None: 
    """Requisita dados do Climate Data Store (CDS) e salva em um arquivo NetCDF.

    Args:
        dataset_salvamento_caminho (Path): Caminho onde será salvo o dataset. É um caminho padrão 
            quando `usa_multiplas_combinacoes` é True.
        variavel (str): Variável a ser obtida.
        ano (int): Ano a ser obtido.
        pressao_nivel (int): Nível de pressão a ser obtido.
        substituir (bool): True para permitir a substituição do arquivo caso já exista.
    """

    arquivo_nome = prepara_arquivo_para_download(dataset_salvamento_caminho, substituir)

    # Inicializar API do CDS
    c = cdsapi.Client() # Exige que o url e a key já estejam configurados em um arquivo .cdsapirc externo.
    
    # Requisição dos dados
    dataset = 'reanalysis-era5-pressure-levels'
    request = {
    'product_type': ['reanalysis'],
    'variable': variavel,
    'year': ano,
    'month': pod.MESES,
    'day': pod.DIAS,
    'time': pod.HORAS,
    'area': pod.AREA,  
    'pressure_level': pressao_nivel,  # Em hPa
    'data_format': pod.DATA_FORMAT,
    'download_format': pod.DOWNLOAD_FORMAT
    }

    c.retrieve(dataset, request, dataset_salvamento_caminho)

    print(f"Requisição de {arquivo_nome} concluída com sucesso!")



def requisita_multiplas_combinacoes() -> None:
    """Faz loops de várias requesições do Climate Data Store (CDS) para obter vários arquivos NetCDF 
    de acordo com os valores padrões passados como parâmetros. 
    O caminho onde os datasets são salvos também é padronizado."""

    n_requisicoes = calcula_combinacoes(pod.VARIAVEIS, pod.ANOS, pod.PRESSAO_NIVEIS)
    
    requisicao_atual = 0

    for variavel in pod.VARIAVEIS:
        for ano in pod.ANOS:
            for pressao_nivel in pod.PRESSAO_NIVEIS:

                # Monta o caminho do arquivo
                arquivo_nome = gera_nome_arquivo_nc_padrao(variavel, ano, pressao_nivel)
                dataset_salvamento_caminho = Datasets.DIRETORIO_ORIGINAIS / arquivo_nome

                # Verifica se o arquivo já existe
                # Se existir, pula o download
                if existe_path_e_exibe_mensagem(dataset_salvamento_caminho, 
                                                f" -> -> -> Arquivo {dataset_salvamento_caminho} já existe. Pulando download.\n"):
                    requisicao_atual += 1
                    exibe_progresso(requisicao_atual, n_requisicoes)
                    continue

                # O arquivo não existindo, faz a requisição
                requisita_unica_combinacao(dataset_salvamento_caminho, variavel, ano, pressao_nivel) 

                requisicao_atual += 1
                exibe_progresso(requisicao_atual, n_requisicoes)

    print(f"\n -> -> -> Todos os arquivos .nc foram baixados com sucesso.\n")


# FUNÇÃO PRINCIPAL ----------------------------------------

def requisita_dados_api(
                    usa_multiplas_combinacoes: bool = True,
                    dataset_salvamento_caminho: Path | Literal["padrao"] = "padrao",
                    variavel: str = "padrao", 
                    ano: int | Literal["padrao"] = "padrao", 
                    pressao_nivel: int | Literal["padrao"] = "padrao", 
                    substituir: bool = False) -> None: 
    """Requisita dados da API do Climate Data Store, podendo ser vários arquivos NetCDF ou apenas um.
    
    Args:
        usa_multiplas_combinacoes (bool): `True` para requisitar múltiplos arquivos NetCDF, seguindo argumentos `padrao`. 
            Caso não sejam escolhidos os argumentos padrões, será levantado um ValueError. 
            Caso False, apenas um arquivo NetCDF será requisitado. Nesse caso, os argumentos devem ser definidos, pois,
            se mantidos como `padrao`, também será levantado um ValueError.
        dataset_salvamento_caminho (Path | Literal["padrao"]): Caminho onde será salvo o dataset. É um caminho padrão 
            quando `usa_multiplas_combinacoes` é True.
        variavel (str): Variável a ser obtida. É padronizado quando `usa_multiplas_combinacoes` é True.
            Examples: "u_component_of_wind", "v_component_of_wind", "relative_humidity", "temperature", "geopotential".
        ano (int | Literal["padrao"]): Ano a ser obtido. É padronizado quando `usa_multiplas_combinacoes` é True.
            Examples: 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024.
        pressao_nivel (int | Literal["padrao"]): Nível de pressão a ser obtido. É padronizado quando `usa_multiplas_combinacoes` é True.
            Examples: 900, 925, 950, 975, 1000.
        substituir (bool): True para permitir a substituição do arquivo caso já exista.
    """
    
    # Monta lista com parametros que tem a possibilidade de receber o valor 'padrao'
    parametros_possivel_padrao = [dataset_salvamento_caminho, variavel, ano, pressao_nivel]

    if usa_multiplas_combinacoes:
        erro_algum_parametro_diferente_do_padrao(parametros_possivel_padrao, 
                                                 "Quando 'usa_multiplas_combinacoes' é True, se pode usar apenas o valor 'padrao' para os parâmetros.")
        requisita_multiplas_combinacoes()

    elif not usa_multiplas_combinacoes:
        erro_algum_parametro_igual_ao_padrao(parametros_possivel_padrao,
                                             "Quando 'usa_multiplas_combinacoes' é False, não se pode usar o valor 'padrao' para nenhum parâmetro.")
            
        requisita_unica_combinacao(cast(Path, dataset_salvamento_caminho), variavel, cast(int, ano), cast(int, pressao_nivel), substituir) 
        # O cast() serve apenas para ajudar o verificador de tipo estático, para os casos em que ele não reconhece o tipo preciso.
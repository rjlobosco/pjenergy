from typing import Literal
from pathlib import Path
from geracoes.requisicao_dados_nc import requisita_dados_api

def obtem_datasets_originais(
                    usa_multiplas_combinacoes: bool = True,
                    dataset_salvamento_caminho: Path | Literal["padrao"] = "padrao",
                    variavel: str = "padrao", 
                    ano: int | Literal["padrao"] = "padrao", 
                    pressao_nivel: int | Literal["padrao"] = "padrao", 
                    substituir: bool = False) -> None: 
    """Função para baixar os arquivos NetCDF do Climate Data Store (CDS). 
    
    Requisita dados da API do Climate Data Store, podendo ser vários arquivos NetCDF ou apenas um.

    Args:
        usa_multiplas_combinacoes (bool): `True` para requisitar múltiplos arquivos NetCDF, seguindo argumentos `padrao`. 
            Caso não sejam escolhidos os argumentos padrões, será levantado um erro. 
            Caso `False`, apenas um arquivo NetCDF será requisitado. Nesse caso, os argumentos devem ser definidos, pois,
            se mantidos como `padrao`, também será levantado um erro.
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

    requisita_dados_api(usa_multiplas_combinacoes, dataset_salvamento_caminho, variavel, ano, pressao_nivel, substituir)


if __name__ == "__main__":
    obtem_datasets_originais() # Obtenção de todos os arquivos NetCDF de cada combinação de variável, ano e nível de pressão.
    
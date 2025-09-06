from pathlib import Path

class DiretoriosBasicos:
    """Agrupa diretorios básicos do projeto
    
    Attributes:
        DIRETORIO_BASE_GERAL (Path): Diretório base do projeto.
        DIRETORIO_DADOS (Path): Diretório onde se localizam os dados.
        DIRETORIO_TESTES (Path): Diretório onde se localizam os testes.
        """

    # Diretório do projeto
    DIRETORIO_BASE_GERAL = Path(__file__).parent.parent.parent 

    # Diretório da pasta de dados
    DIRETORIO_DADOS = DIRETORIO_BASE_GERAL / "data" # .../data

    # Diretório da pasta de testes
    DIRETORIO_TESTES = DIRETORIO_BASE_GERAL / "tests" # .../data/tests




# class PathsDados:
#     """Agrupa diretórios de armazenamento de dados e fornece funções para construir caminhos para diferentes tipos de dados."""
    
#     # Funções Auxiliares

#     @staticmethod
#     def diretorio_estrutura(formato_arquivo: Literal["netcdf", "parquet"]) -> Path: 
#         """Obtém o diretório onde fica a estrutura de dados específica (dataframe ou dataset), que depende do formato do arquivo.
        
#         Args:
#             formato_arquivo (Literal["netcdf", "parquet"]): Formato com o qual se deseja trabalhar. 

#         Returns: 
#             Path: Diretório onde fica a estrutura de dados específica.
#                 Examples: ".../data/datasets", ".../data/dataframes"
#         """ 

#         nome_pasta_arquivos_estrutura = obtem_nome_pasta_dados(formato_arquivo)
#         diretorio_arquivos_estrutura = DiretoriosBasicos.DIRETORIO_DADOS / nome_pasta_arquivos_estrutura 

#         return diretorio_arquivos_estrutura
    

#     @staticmethod
#     def diretorio_coordenadas(formato_arquivo: Literal["netcdf", "parquet"]) -> Path:  
#         """Obtém o diretório onde ficam dados para coordenadas específicas, que depende do formato do arquivo.
        
#         Args:
#             formato_arquivo (Literal["netcdf", "parquet"]): Formato de arquivo com o qual se deseja trabalhar. 
#                 Se `formato_arquivo` for "netcdf", o caminho retornado é de um **arquivo único**. 
#                 Se for "parquet", o caminho retornado é de uma **pasta** com múltiplos arquivos .parquet.

#         Returns: 
#             Path: Diretório onde ficam dados para coordenadas específicas.
#                 Examples: ".../data/datasets/coordenadas_especificas", ".../data/dataframes/coordenadas_especificas"
#         """

#         diretorio_arquivos_estrutura = PathsDados.diretorio_estrutura(formato_arquivo)
#         diretorio_coordenadas_especificas = diretorio_arquivos_estrutura / pn.COORDENADAS_ESPECIFICAS

#         return diretorio_coordenadas_especificas


#     @staticmethod
#     def caminho_relativo(formato_arquivo: Literal["netcdf", "parquet"], 
#                         plataforma_representacao: Optional[str]) -> Path:   
#         """Obtém o caminho relativo do arquivo/pasta.
            
#         Args:
#             formato_arquivo (Literal["netcdf", "parquet"]): Formato de arquivo com o qual se deseja trabalhar.
#             plataforma_representacao (Optional[str]): Nome (ou símbolo) da plataforma cujo caminho dos dados se deseja obter.
#                 É None no caso de uma coordenada que não define uma plataforma.
        
#         Returns:
#             Path: Caminho relativo do arquivo/pasta
#                 Examples: plataformas/NAMORADO_2_(PNA-2), 
#                 plataformas/NAMORADO_2_(PNA-2).nc, 
#                 ponto_nao_plataforma/ponto_nao_plataforma, 
#                 ponto_nao_plataforma/ponto_nao_plataforma.nc
#         """

#         caminho_relativo = obtem_caminho_relativo(formato_arquivo, plataforma_representacao)
        
#         return caminho_relativo
    

#     # Funções Principais

#     @staticmethod
#     def caminho_absoluto_coordenadas(formato_arquivo: Literal["netcdf", "parquet"], 
#                                      plataforma_representacao: Optional[str]) -> Path:   
#         """Decide o caminho ou diretório absoluto do arquivo ou pasta que contém dados 
#         para coordenadas específicas para uma plataforma, dado o formato de arquivo com o qual 
#         se deseja trabalhar.
        
#         Args:
#             formato_arquivo (Literal["netcdf", "parquet"]): Formato de arquivo com o qual se deseja trabalhar. 
#                 Se `formato_arquivo` for "netcdf", o caminho retornado é de um **arquivo único**. 
#                 Se for "parquet", o caminho retornado é de uma **pasta** com múltiplos arquivos .parquet.
                
#             plataforma (Optional[str]): Nome (ou símbolo) da plataforma cujo caminho dos dados se deseja obter.
#                 É None no caso de uma coordenada que não define uma plataforma.

#         Returns: 
#             Path: Caminho ou diretório absoluto do arquivo ou pasta.
#                 Examples: ".../data/datasets/coordenadas_especificas/plataformas/NAMORADO_2_(PNA-2).nc", 
#                 ".../data/dataframes/coordenadas_especificasplataformas/NAMORADO_2_(PNA-2)"
#         """

#         caminho_relativo = PathsDados.caminho_relativo(formato_arquivo, plataforma_representacao)
#         diretorio_coordenadas_especificas = PathsDados.diretorio_coordenadas(formato_arquivo)
        
#         path = diretorio_coordenadas_especificas / caminho_relativo

#         return path
    

def diretorios_genericos(base: Path) -> tuple[Path, Path, Path, Path, Path]:

    DIRETORIO_LOCALIZACOES_PONTUAIS = base / "pontuais" 

    DIRETORIO_PLATAFORMAS = DIRETORIO_LOCALIZACOES_PONTUAIS / "plataformas" 
    DIRETORIO_PLATAFORMAS_GERAL = DIRETORIO_PLATAFORMAS / "geral" 

    DIRETORIO_OUTROS_PONTOS = DIRETORIO_LOCALIZACOES_PONTUAIS / "outros_pontos" 
    DIRETORIO_OUTROS_PONTOS_GERAL = DIRETORIO_OUTROS_PONTOS / "geral" 

    return (DIRETORIO_LOCALIZACOES_PONTUAIS,
            DIRETORIO_PLATAFORMAS,
            DIRETORIO_PLATAFORMAS_GERAL,
            DIRETORIO_OUTROS_PONTOS,
            DIRETORIO_OUTROS_PONTOS_GERAL)


class Datasets:
    """Agrupa diretórios onde se localizam datasets.
    
    Attributes:
        BASE (Path): Diretório base onde se encontram todos os datasets.
        DIRETORIO_ORIGINAIS (Path): Diretório dos arquivos originais obtidos do Climate Data Store.
        DIRETORIO_UNIDO (Path): Diretório da pasta onde fica o arquivo feito da união dos arquivos originais obtidos.
        CAMINHO_UNIDO (Path): Caminho absoluto do arquivo feito da união dos arquivos originais obtidos.
        DIRETORIO_LOCALIZACOES_PONTUAIS (Path): Diretório de datasets modificados para representar coordenadas específicas.
        DIRETORIO_PLATAFORMAS (Path): Diretório de datasets modificados para representar pontos de plataformas específicas.
        DIRETORIO_PLATAFORMAS_GERAL (Path): A versão mais abrangente dos dados das plataformas.
        DIRETORIO_OUTROS_PONTOS (Path): Diretório de datasets modificados para representar pontos que não são de plataformas.
        DIRETORIO_OUTROS_PONTOS_GERAL (Path): A versão mais abrangente dos dados fora dos pontos das plataformas.
    """

    BASE = DiretoriosBasicos.DIRETORIO_DADOS / "datasets"  # .../data/datasets

    DIRETORIO_ORIGINAIS = BASE / "originais" # .../data/datasets/originais

    CAMINHO_UNIDO = BASE / "unido" / "dataset_unido.nc"  # Caminho do arquivo: .../data/datasets/unido/dataset_unido.nc

    (DIRETORIO_LOCALIZACOES_PONTUAIS, # .../data/datasets/pontuais
    DIRETORIO_PLATAFORMAS,            # .../data/datasets/pontuais/plataformas
    DIRETORIO_PLATAFORMAS_GERAL,      # .../data/datasets/pontuais/plataformas/geral
    DIRETORIO_OUTROS_PONTOS,          # .../data/datasets/pontuais/outros_pontos
    DIRETORIO_OUTROS_PONTOS_GERAL     # .../data/datasets/pontuais/outros_pontos/geral
    ) = diretorios_genericos(BASE)


class Dataframes:
    """Agrupa diretórios onde se localizam dataframes.
    
    Attributes:
        BASE (Path): Diretório base onde se encontram todos os dataframes.
        DIRETORIO_LOCALIZACOES_PONTUAIS (Path): Diretório de datasets modificados para representar coordenadas específicas.
        DIRETORIO_PLATAFORMAS (Path): Diretório de datasets modificados para representar pontos de plataformas específicas.
        DIRETORIO_PLATAFORMAS_GERAL (Path): A versão mais abrangente dos dados das plataformas.
        DIRETORIO_OUTROS_PONTOS (Path): Diretório de datasets modificados para representar pontos que não são de plataformas.
        DIRETORIO_OUTROS_PONTOS_GERAL (Path): A versão mais abrangente dos dados fora dos pontos das plataformas. 
    """

    BASE = DiretoriosBasicos.DIRETORIO_DADOS /  "dataframes" # .../data/dataframes

    (DIRETORIO_LOCALIZACOES_PONTUAIS, # .../data/dataframes/pontuais
    DIRETORIO_PLATAFORMAS,            # .../data/dataframes/pontuais/plataformas
    DIRETORIO_PLATAFORMAS_GERAL,      # .../data/dataframes/pontuais/plataformas/geral
    DIRETORIO_OUTROS_PONTOS,          # .../data/dataframes/pontuais/outros_pontos
    DIRETORIO_OUTROS_PONTOS_GERAL     # .../data/dataframes/pontuais/outros_pontos/geral
    ) = diretorios_genericos(BASE)



class DadosTestes:
    """Agrupa diretórios onde se localizam dados de teste.
    
    Attributes:
        DIRETORIO_DADOS_GERADOS_TESTES (Path): Diretório de dados gerados em testes.  
    """

    DIRETORIO_DADOS_GERADOS_TESTES = DiretoriosBasicos.DIRETORIO_TESTES / "dados_gerados_testes"  # .../data/tests/dados_gerados_testes


if "__main__" == __name__:
    # print(f'Função diretorio_estrutura:\n{PathsDados.diretorio_estrutura("netcdf")}\n')
    # print(f'Função diretorio_coordenadas:\n{PathsDados.diretorio_coordenadas("netcdf")}\n')
    # print(f'Função caminho_relativo:\n{PathsDados.caminho_relativo("parquet", "p5")}\n')
    # print(f'Função caminho_absoluto_coordenadas:\n{PathsDados.caminho_absoluto_coordenadas("parquet", "p2")}\n')

    print("-------------------------\n")

    print(Dataframes.DIRETORIO_PLATAFORMAS_GERAL)

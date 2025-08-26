from pathlib import Path
from typing import Optional, Literal, cast
from config.constants import ArquivosNomes as an, PastasNomes as pn, Plataformas, Correspondencias as cr, FormatosArquivo as fa
from utils.gerencia_plataformas_representacoes import gerencia_plataforma_representacoes
from utils.obtem_dados_plataformas import obtem_dados_pasta_nome, obtem_nome_pasta_ou_arquivo_chave, obtem_pasta_local_nome_especifico



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
    DIRETORIO_DADOS = DIRETORIO_BASE_GERAL / pn.DADOS

    # Diretório da pasta de testes
    DIRETORIO_TESTES = DIRETORIO_BASE_GERAL / pn.TESTES  




class PathsDados:
    """Agrupa diretórios de armazenamento de dados e fornece funções para construir caminhos para diferentes tipos de dados."""
    
    @staticmethod
    def obtem_pasta_arquivos_estrutura(formato_arquivo: Literal["netcdf", "parquet"]) -> Path: 
        """Obtém o diretório onde fica a estrutura de dados específica (dataframe ou dataset), que depende do formato do arquivo.
        
        Args:
            formato_arquivo (Literal["netcdf", "parquet"]): Formato com o qual se deseja trabalhar. 

        Returns: 
            Path: Diretório onde fica a estrutura de dados específica.
        """ 

        nome_pasta_arquivos_estrutura = obtem_dados_pasta_nome(formato_arquivo)
        diretorio_arquivos_estrutura = DiretoriosBasicos.DIRETORIO_DADOS / nome_pasta_arquivos_estrutura 

        return diretorio_arquivos_estrutura
    

    @staticmethod
    def obtem_diretorio_coordenadas_especificas(formato_arquivo: Literal["netcdf", "parquet"]) -> Path:  
        """Obtém o diretório onde ficam dados para coordenadas específicas, que depende do formato do arquivo.
        
        Args:
            formato_arquivo (Literal["netcdf", "parquet"]): Formato de arquivo com o qual se deseja trabalhar. 
                Se `formato_arquivo` for "netcdf", o caminho retornado é de um **arquivo único**. 
                Se for "parquet", o caminho retornado é de uma **pasta** com múltiplos arquivos .parquet.

        Returns: 
            Path: Diretório onde ficam dados para coordenadas específicas.
        """
        diretorio_arquivos_estrutura = PathsDados.obtem_pasta_arquivos_estrutura(formato_arquivo)
        diretorio_coordenadas_especificas = diretorio_arquivos_estrutura / pn.COORDENADAS_ESPECIFICAS

        return diretorio_coordenadas_especificas

    @staticmethod
    def obtem_caminho_relativo(formato_arquivo: Literal["netcdf", "parquet"], plataforma_representacao: Optional[str]) -> Path:
        """Obtém o caminho relativo do arquivo/pasta.
            
        Args:
            formato_arquivo (Literal["netcdf", "parquet"]): Formato de arquivo com o qual se deseja trabalhar.
            plataforma_representacao (Optional[str]): Nome (ou símbolo) da plataforma cujo caminho dos dados se deseja obter.
                É None no caso de uma coordenada que não define uma plataforma.
        
        Returns:
            Path: Caminho relativo do arquivo/pasta
                Exemples: plataformas/NAMORADO_2_(PNA-2), 
                plataformas/NAMORADO_2_(PNA-2).nc, 
                ponto_nao_plataforma/ponto_nao_plataforma, 
                ponto_nao_plataforma/ponto_nao_plataforma.nc
        """

        pasta_local, nome = obtem_pasta_local_nome_especifico(formato_arquivo, plataforma_representacao)
        
        # Caminho relativo em relação
        caminho_relativo = pasta_local / nome

        return caminho_relativo
    

    @staticmethod
    def obtem_path_coord_especifica(formato_arquivo: Literal["netcdf", "parquet"], plataforma: Optional[str]) -> Path:   
        """Decide o path (caminho ou diretório) absoluto do arquivo ou pasta que contém dados 
        para coordenadas específicas para uma plataforma, dado o formato de arquivo com o qual 
        se deseja trabalhar.
        
        Args:
            formato_arquivo (Literal["netcdf", "parquet"]): Formato de arquivo com o qual se deseja trabalhar. 
                Se `formato_arquivo` for "netcdf", o caminho retornado é de um **arquivo único**. 
                Se for "parquet", o caminho retornado é de uma **pasta** com múltiplos arquivos .parquet.
                
            plataforma (Optional[str]): Nome (ou símbolo) da plataforma cujo caminho dos dados se deseja obter.
                É None no caso de uma coordenada que não define uma plataforma.

        Returns: 
            Path: Caminho ou diretório absoluto do arquivo ou pasta.
        """

        caminho_relativo = PathsDados.obtem_caminho_relativo(formato_arquivo, plataforma)
        diretorio_coordenadas_especificas = PathsDados.obtem_diretorio_coordenadas_especificas(formato_arquivo)
        
        path = diretorio_coordenadas_especificas / caminho_relativo

        return path
    

    class Datasets:
        """Agrupa diretórios onde se localizam datasets.
        
        Attributes:
            BASE (Path): Diretório base onde se encontram todos os datasets.
            DIRETORIO_ORIGINAIS (Path): Diretório dos arquivos originais obtidos do Climate Data Store.
            DIRETORIO_UNIDO (Path): Diretório da pasta onde fica o arquivo feito da união dos arquivos originais obtidos.
            CAMINHO_UNIDO (Path): Caminho absoluto do arquivo feito da união dos arquivos originais obtidos.
            DIRETORIO_COORDENADAS_ESPECIFICAS (Path): Diretório de datasets modificados para representar coordenadas específicas.
            DIRETORIO_PLATAFORMAS (Path): Diretório de datasets modificados para representar pontos de plataformas específicas.
            DIRETORIO_NAO_PLATAFORMAS (Path): Diretório de datasets modificados para representar pontos que não são plataformas.
        """

        BASE = DiretoriosBasicos.DIRETORIO_DADOS / pn.DATASETS 

        DIRETORIO_ORIGINAIS = BASE / pn.ORIGINAIS

        DIRETORIO_UNIDO = BASE / pn.UNIDO
        CAMINHO_UNIDO = DIRETORIO_UNIDO / an.ARQUIVO_NC_UNIDO

        DIRETORIO_COORDENADAS_ESPECIFICAS = BASE / pn.COORDENADAS_ESPECIFICAS
        DIRETORIO_PLATAFORMAS = DIRETORIO_COORDENADAS_ESPECIFICAS / pn.PLATAFORMAS
        DIRETORIO_NAO_PLATAFORMAS = DIRETORIO_COORDENADAS_ESPECIFICAS / pn.PONTOS_NAO_PLATAFORMA

    
    class Dataframes:
        """Agrupa diretórios onde se localizam dataframes.
        
        Attributes:
            BASE (Path): Diretório base onde se encontram todos os dataframes.
            DIRETORIO_COORDENADAS_ESPECIFICAS (Path): Diretório de dataframes que representam coordenadas específicas.
            DIRETORIO_PLATAFORMAS (Path): Diretório de dataframes que representam pontos de plataformas específicas.
            DIRETORIO_NAO_PLATAFORMAS (Path): Diretório de dataframes que representam pontos que não são plataformas.  
        """

        BASE = DiretoriosBasicos.DIRETORIO_DADOS /  pn.DATAFRAMES

        DIRETORIO_COORDENADAS_ESPECIFICAS = BASE / pn.COORDENADAS_ESPECIFICAS
        DIRETORIO_PLATAFORMAS = DIRETORIO_COORDENADAS_ESPECIFICAS / pn.PLATAFORMAS
        DIRETORIO_NAO_PLATAFORMAS = DIRETORIO_COORDENADAS_ESPECIFICAS / pn.PONTOS_NAO_PLATAFORMA



    class Testes:
        """Agrupa diretórios onde se localizam dados de teste.
        
        Attributes:
            DIRETORIO_DADOS_GERADOS_TESTES (Path): Diretório de dados gerados em testes.  
        """

        DIRETORIO_DADOS_GERADOS_TESTES = DiretoriosBasicos.DIRETORIO_TESTES / pn.DADOS_GERADOS_TESTES


if "__main__" == __name__:
    print(PathsDados.obtem_pasta_arquivos_estrutura("netcdf"))
    print(PathsDados.obtem_diretorio_coordenadas_especificas("netcdf"))  
    print(PathsDados.obtem_caminho_relativo("parquet", "p5"))
      
    
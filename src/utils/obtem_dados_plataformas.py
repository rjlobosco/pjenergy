from typing import Literal, cast, Optional
from pathlib import Path
from config.constants import PastasNomes as pn, Correspondencias as cr, FormatosArquivo as fa, Plataformas, ArquivosNomes as an
from utils.gerencia_plataformas_representacoes import gerencia_plataforma_representacoes

def obtem_nome_pasta_ou_arquivo_chave(formato_arquivo: Literal["netcdf", "parquet"]) -> str:
        """Pega a chave para o nome do arquivo ou pasta, a partir do formato do arquivo.
            
        Args:
            formato_arquivo (Literal["netcdf", "parquet"]): Formato de arquivo com o qual se deseja trabalhar.
        
        Returns:
            str: Nome da chave para o nome do arquivo ou pasta.
                Exemples: "arquivo_nc_nome", "pasta_dask_nome"
        """

        if formato_arquivo == fa.NETCDF:
            chave_arquivo_nome = cr.Chaves.ARQUIVO_NC_CHAVE
        elif formato_arquivo == fa.PARQUET:
            chave_arquivo_nome = cr.Chaves.PASTA_DASK_DATAFRAME_CHAVE

        return chave_arquivo_nome
    

def obtem_dados_pasta_nome(formato_arquivo: Literal["netcdf", "parquet"]) -> str:
    """Decide o nome da pasta onde se localizam os arquivos do formato especificado.
        
    Args:
        formato_arquivo (Literal["netcdf", "parquet"]): Formato de arquivo com o qual se deseja trabalhar.
    
    Returns:
        str: Nome da pasta de dados
            Exemples: "datasets", "dataframes"
    """

    if formato_arquivo == fa.NETCDF:
        dado_pasta_nome = pn.DATASETS
    elif formato_arquivo == fa.PARQUET:
        dado_pasta_nome = pn.DATAFRAMES

    return dado_pasta_nome


def obtem_pasta_local_nome_especifico(formato_arquivo: Literal["netcdf", "parquet"], 
                                      plataforma_representacao: Optional[str]) -> tuple[Path, str]:
    """Obtem o nome da pasta que indica o tipo de local dos dados e o nome específico do dataset/dataframe.

    Args:
            formato_arquivo (Literal["netcdf", "parquet"]): Formato de arquivo com o qual se deseja trabalhar.
            plataforma_representacao (Optional[str]): Nome (ou símbolo) da plataforma cujo caminho dos dados se deseja obter.
                É None no caso de uma coordenada que não define uma plataforma.
        
    """

    if isinstance(plataforma_representacao, str): # Condição para descartar os casos em que não é passado nenhuma plataforma em específico (None)
        # Garante a possibilidade de receber tanto o nome completo da plataforma quanto seu símbolo
        plataforma_representacao = gerencia_plataforma_representacoes(plataforma_representacao)
        
    chave_arquivo_nome = obtem_nome_pasta_ou_arquivo_chave(formato_arquivo)

    # Caso seja escolhida uma plataforma específica
    if plataforma_representacao in Plataformas.PLATAFORMAS:
        pasta_local = Path(pn.PLATAFORMAS) # Pasta que indica o tipo de local dos dados (no caso, em plataforma)
        nome = Plataformas.DADOS[plataforma_representacao][chave_arquivo_nome] # Pode ser um arquivo ou pasta
        nome = cast(str, nome) # isso é só para o linters, não muda o valor em tempo de execução           
    # Caso seja escolhido um outro ponto qualquer coberto pelos dados
    elif plataforma_representacao is None:
        pasta_local = Path(pn.PONTOS_NAO_PLATAFORMA)
        if formato_arquivo == fa.NETCDF:
            nome = an.ARQUIVO_NC_PONTO_NAO_PLATAFORMA # É um arquivo
        elif formato_arquivo == fa.PARQUET:
            nome = pn.PONTOS_NAO_PLATAFORMA # É uma pasta
    else:
        raise ValueError(f" {plataforma_representacao} é um valor não válido para plataforma. \n\
                            Valores válidos: \n{Plataformas.PLATAFORMAS} \n\
                            Ou seus simbolos correspondentes: \n{Plataformas.SIMBOLOS}")
    
    return pasta_local, nome


if "__main__" == __name__:
    # Exemplo de uso das funções
    print(obtem_nome_pasta_ou_arquivo_chave("netcdf"))
    print(obtem_dados_pasta_nome("parquet"))
    obtem_pasta_local_nome_especifico("netcdf","p2")
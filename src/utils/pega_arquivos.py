import glob
from pathlib import Path
from config.paths import Datasets
from config.constants import ArquivosNomes as an


def pega_arquivos(diretorio: Path =Datasets.DIRETORIO_ORIGINAIS, nome_padrao: str = an.PADRAO_ARQUIVOS_NC_ORIGINAIS) -> list[str]:
    """Pega todos os arquivos de um determinado diretório com o nome em um determinado padrão
    
    Args:
        diretorio (Path): Diretório onde os arquivos serão procurados.
        nome_padrao (str): Nome padrão de arquivo a ser procurado.

    Returns: 
        list[str]: Lista dos nomes dos arquivos que seguem ao padrão de nome.
    """

    caminho_padrao = diretorio / nome_padrao 
    caminho_padrao = str(caminho_padrao)

    # Lista todos os arquivos que correspondem ao padrão
    print(f"Procurando arquivos com nome no padrão: {nome_padrao} ...\n")
    arquivos = glob.glob(caminho_padrao) 
    print("Arquivos encontrados.\n\n")

    return arquivos


if __name__ == "__main__":
    arquivos = pega_arquivos()
    print(arquivos)
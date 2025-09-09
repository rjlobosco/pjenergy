from pathlib import Path

def verifica_erro_nao_existe_path(path: Path) -> None:
    """Verifica a existência de um arquivo ou diretório e levanta erro caso não exista.
    
    Args
        path (Path): Path a ser verificado.

    Raises:
        FileNotFoundError: Erro levantado quando o path não existe.
    """

    if not path.exists():
        raise FileNotFoundError(f"\nO arquivo... \n -> {path} \n...não existe.\n")


def verifica_erro_ja_existe_arquivo(caminho: Path, mensagem_erro: str) -> None:
    """Levanta um erro caso o arquivo já exista.
    
    Args: 
        caminho (Path): Caminho a ser verificado
        mensagem_erro: Mensagem a ser exibida em caso de erro

    Raises:
        FileExistsError: Erro de existência do arquivo
    """

    if caminho.exists():
        raise FileExistsError(mensagem_erro)


def cria_path_se_nao_existe(path: Path) -> None:
    """Cria um path caso não exista.
    
    Args:
        path (Path): Path cuja existência se deseja garantir.
    """

    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        print(f"Diretório '{path}' criado com sucesso.\n")


def existe_path_e_exibe_mensagem(path: Path, mensagem: str) -> bool:
    """Retorna a existência de um path e printa uma mensagem caso exista.
    
    Args: 
        path (Path): Path a ser verificado.
        mensagem (str): Mensagem a ser printada caso `path` exista.

    Returns: 
        bool: Se o path existe ou não.
    """

    existe = path.exists()
    if existe:
        print(mensagem)
    return existe


def garante_path_pai_existencia(path: Path) -> None:
    """Cria pastas parentais para um path caso não exista.
    
    Args:
        path (Path): Path cujas pastas parentais se busca garantir
    """

    cria_path_se_nao_existe(path.parent)



if __name__ == "__main__":
    
    # EXEMPLOS
    
    verifica_erro_nao_existe_path(Path("a/b/c/d/e/f")) # Exemplo de levantamento de erro
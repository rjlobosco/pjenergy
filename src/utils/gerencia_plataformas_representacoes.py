from config.constants import Plataformas
from utils.obtem_dados_plataformas import simbolo_para_plataforma

def gerencia_plataforma_representacoes(plataforma_representacao: str ) -> str:
    """Gerencia a representação de plataformas, convertendo símbolos em nomes de plataformas específicos e 
    levantando erros para nomes errados.

    Args:
        representacao (str): Pode ser um nome padronizado de plataforma, um símbolo associado ou outra string qualquer. 
            Nesse último caso, é levantado um erro. 

    Returns:
        str: Nome da plataforma, no caso de `representação` ser o símbolo associado à plataforma ou já ser o próprio nome
        da plataforma.

    Raises:
        ValueError: Se a representação não for válida como nome de plataforma
        ValueError: Se a representação for um símbolo que não está associado a nenhuma plataforma conhecida.
    """


    if plataforma_representacao not in Plataformas.SIMBOLOS and plataforma_representacao not in Plataformas.PLATAFORMAS:
        raise ValueError("Nome inválido para plataforma. " \
        f"Nomes validos: {Plataformas.PLATAFORMAS} ou " \
        f"Seus símbolos: {Plataformas.SIMBOLOS}")

    elif plataforma_representacao in Plataformas.PLATAFORMAS:
        return plataforma_representacao
    
    else: # representacao in Plataformas.SIMBOLOS:
        # Busca o nome da plataforma associada ao símbolo
        plataforma = simbolo_para_plataforma(plataforma_representacao)
        return plataforma
    


if __name__ == "__main__":

    # EXEMPLOS
    plataforma = gerencia_plataforma_representacoes("p3")   
    plataforma = gerencia_plataforma_representacoes("PETROBRAS 26 (P-26)")
from config.constants import Plataformas, Correspondencias as cr

def gerencia_plataforma_representacoes(representacao: str ) -> str:
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


    if representacao not in Plataformas.SIMBOLOS and representacao not in Plataformas.PLATAFORMAS:
        raise ValueError("Nome inválido para plataforma. " \
        f"Nomes validos: {Plataformas.PLATAFORMAS} ou " \
        f"Seus símbolos: {Plataformas.SIMBOLOS}")

    elif representacao in Plataformas.PLATAFORMAS:
        return representacao
    
    else: # representacao in Plataformas.SIMBOLOS:
        # Busca o nome da plataforma associada ao símbolo
        for plataforma in Plataformas.PLATAFORMAS:
            if Plataformas.DADOS[plataforma][cr.Chaves.SIMBOLO_CHAVE] == representacao:
                print(f"Correspondência: {representacao} -> {plataforma}")
                return plataforma
        # Se não encontrar, lança erro
        raise ValueError("Símbolo não associado a nenhuma plataforma conhecida.")

        
 

if __name__ == "__main__":

    # EXEMPLOS
    plataforma = gerencia_plataforma_representacoes("p3")   
    plataforma = gerencia_plataforma_representacoes("PETROBRAS 26 (P-26)")
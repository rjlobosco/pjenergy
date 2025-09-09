from config.constants import Plataformas, Correspondencias as cr

def simbolo_para_plataforma(simbolo: str) -> str:
    """Obtém o nome da plataforma a partir do símbolo desta."""

    for plat in Plataformas.PLATAFORMAS:
        if Plataformas.DADOS[plat][cr.Chaves.SIMBOLO_CHAVE] == simbolo:
            print(f"Correspondência: {simbolo} -> {plat}")
            return plat
    
    raise TypeError("Essa função deve retornar o nome de uma plataforma (str)")



def plataforma_para_arquivo_nome(plataforma: str) -> str:
    """Obtém o nome do arquivo a partir da plataforma correspondente."""

    for plat in Plataformas.DADOS:
        if plat == plataforma:
            arquivo_nome = Plataformas.DADOS[plat][cr.Chaves.ARQUIVO_CHAVE]
            return arquivo_nome

    raise TypeError("Essa função deve retornar o nome de um arquivo (str)")



def plataforma_para_pasta_nome(plataforma: str) -> str:
    """Obtém o nome da pasta a partir da plataforma correspondente."""

    for plat in Plataformas.DADOS:
        if plat == plataforma:
            pasta_nome = Plataformas.DADOS[plat][cr.Chaves.PASTA_CHAVE]
            return pasta_nome

    raise TypeError("Essa função deve retornar o nome de uma pasta (str)")




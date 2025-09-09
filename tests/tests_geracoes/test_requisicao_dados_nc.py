# Módulos internos do projeto
from config.paths import DadosTestes
from geracoes.requisicao_dados_nc import requisita_dados_api
from config.constants import ParametrosObtencaoDados as pod

def test_requisicao_dados(requisitar = True, variavel: str = pod.VARIAVEIS[0], ano: int = pod.ANOS[0], pressao_nivel: int = pod.PRESSAO_NIVEIS[0]):
    """Teste para verificar a requisição de dados do Climate Data Store (CDS)"""

    print(f"\n -> -> -> Variável escolhida: {variavel}")
    print(f" -> -> -> Ano escolhido: {ano}")
    print(f" -> -> -> Nível de pressão escolhido: {pressao_nivel}")

    # Localização do arquivo de saída
    dataset_salvamento_caminho = DadosTestes.DIRETORIO_DADOS_GERADOS_TESTES / f"teste-(var-{variavel})_(ano-{ano})_(pressao-{pressao_nivel}).nc"
   
    if not requisitar:
        print("\n -> -> -> ATENÇÃO: Na verdade, a requisição de dados não foi realizada e nada será salvo. Este é apenas um teste. Mude o parâmetro 'requisitar' para True para realizar a requisição.")
    else:
        requisita_dados_api(False, dataset_salvamento_caminho, variavel, ano, pressao_nivel, substituir = True)
        
    print(f"Dataset salvo em {dataset_salvamento_caminho} .")


if __name__ == "__main__":
    test_requisicao_dados(True, pressao_nivel = 1000)

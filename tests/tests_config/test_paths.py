import pytest
from config.paths import PathsDados, DiretoriosBasicos
from config.constants import FormatosDados as fa

@pytest.mark.parametrize(
    "formato_arquivo, plataforma, esperado_path",
    [
        (fa.NETCDF, "NAMORADO 2 (PNA-2)", DiretoriosBasicos.DIRETORIO_DADOS / "datasets/coordenadas_especificas/plataformas/p1-NAMORADO_2_(PNA-2).nc"),
        (fa.PARQUET, "p2", DiretoriosBasicos.DIRETORIO_DADOS /"dataframes/coordenadas_especificas/plataformas/p2-PETROBRAS_26_(P-26)"),
        (fa.NETCDF, None, DiretoriosBasicos.DIRETORIO_DADOS / "datasets/coordenadas_especificas/ponto_nao_plataforma/ponto_nao_plataforma.nc"),
        (fa.PARQUET, None, DiretoriosBasicos.DIRETORIO_DADOS / "dataframes/coordenadas_especificas/ponto_nao_plataforma/ponto_nao_plataforma"),
    ]
)
def test_obtem_path_coord_especifica(formato_arquivo, plataforma, esperado_path):
    path = PathsDados.caminho_absoluto_coordenadas(formato_arquivo, plataforma)
    assert esperado_path == path

def test_obtem_path_coord_especifica_plataforma_invalida():
    with pytest.raises(ValueError):
        PathsDados.caminho_absoluto_coordenadas(fa.NETCDF, "PLATAFORMA_INVALIDA")
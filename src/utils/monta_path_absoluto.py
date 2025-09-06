from pathlib import Path
from config.paths import DiretoriosBasicos

def monta_path_absoluto(path: Path, path_absoluto_bool = False) -> Path:

    if path_absoluto_bool == False:
        path_absoluto = DiretoriosBasicos.DIRETORIO_BASE_GERAL / path
    else:
        path_absoluto = path

    return path_absoluto
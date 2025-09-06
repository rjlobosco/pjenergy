from pathlib import Path


def str_para_path(path: Path | str) -> Path:

    if isinstance(path, str):
        path = Path(path)

    return path
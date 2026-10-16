from pathlib import Path

import pandas as pd

from extract import URL_CADOP, extract
from load import load_data
from transform import transform_data


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
DB_PATH = PROJECT_ROOT / "data" / "operadoras.db"


def main() -> None:
    """Executa o pipeline completo: extração, transformação e carga."""

    print("=== Pipeline ANS: operadoras ativas ===")

    raw_path = extract(URL_CADOP, RAW_DIR)

    rows_read = len(pd.read_csv(raw_path, sep=";", dtype=str, encoding="utf-8-sig"))

    df = transform_data(raw_path)
    load_data(df, DB_PATH)

    rows_loaded = len(df)
    rows_discarded = rows_read - rows_loaded

    print("=== Resumo da execução ===")
    print(f"Linhas lidas: {rows_read}")
    print(f"Linhas descartadas: {rows_discarded}")
    print(f"Linhas carregadas: {rows_loaded}")


if __name__ == "__main__":
    main()
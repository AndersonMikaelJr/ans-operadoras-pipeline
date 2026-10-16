import sqlite3
from contextlib import closing
from pathlib import Path

import pandas as pd


def load_data(df: pd.DataFrame, db_path: Path) -> None:
    """Grava a tabela tratada no SQLite, substituindo a carga anterior."""

    print("Iniciando carga no SQLite...")

    db_path.parent.mkdir(parents=True, exist_ok=True)

    with closing(sqlite3.connect(db_path)) as connection:
        df.to_sql("operadoras", connection, if_exists="replace", index=False)

    print(f"Linhas carregadas: {len(df)}")
    print(f"Banco salvo em: {db_path}")
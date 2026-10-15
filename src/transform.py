from pathlib import Path

import numpy as np
import pandas as pd


def clean_text_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Remove espaços extras e converte textos vazios em nulos."""

    print("Limpando textos...")

    df = df.copy()

    for column in df.columns:
        df[column] = df[column].str.strip()

    df = df.replace("", np.nan)

    return df



EXPECTED_COLUMNS = [
    "REGISTRO_OPERADORA",
    "CNPJ",
    "RAZAO_SOCIAL",
    "NOME_FANTASIA",
    "MODALIDADE",
    "LOGRADOURO",
    "NUMERO",
    "COMPLEMENTO",
    "BAIRRO",
    "CIDADE",
    "UF",
    "CEP",
    "DDD",
    "TELEFONE",
    "FAX",
    "ENDERECO_ELETRONICO",
    "REPRESENTANTE",
    "CARGO_REPRESENTANTE",
    "REGIAO_DE_COMERCIALIZACAO",
    "DATA_REGISTRO_ANS",
]

PLACEHOLDERS = {
    "NOME_FANTASIA": "******",
    "ENDERECO_ELETRONICO": "XX@XX.XX",
}

def validate_data(file_path: Path) -> pd.DataFrame:
    """Lê o CSV bruto e confere se a estrutura esperada está presente."""

    print("Iniciando validação dos dados...")

    df = pd.read_csv(
        file_path,
        sep=";",
        dtype=str,
        encoding="utf-8-sig",
    )

    missing_columns = [
        column for column in EXPECTED_COLUMNS if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(f"Colunas obrigatórias ausentes: {missing_columns}")

    print(f"Colunas encontradas: {len(df.columns)}")
    print(f"Linhas recebidas: {len(df)}")
    print("Validação estrutural concluída.")

    return df

def replace_placeholders(df: pd.DataFrame) -> pd.DataFrame:
    """Converte valores de preenchimento falso em nulos."""

    print("Substituindo valores de preenchimento falso...")

    df = df.copy()

    for column, placeholder in PLACEHOLDERS.items():
        df[column] = df[column].replace(placeholder, np.nan)

    return df
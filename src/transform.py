from pathlib import Path

import pandas as pd


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
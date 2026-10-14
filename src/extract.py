from datetime import date
from pathlib import Path

import requests


URL_CADOP = (
    "https://dadosabertos.ans.gov.br/FTP/PDA/"
    "operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv"
)


def extract(url: str, destination_dir: Path) -> Path:
    """Baixa o CSV da ANS e salva uma cópia bruta com a data no nome."""

    print("Iniciando extração...")

    destination_dir.mkdir(parents=True, exist_ok=True)

    file_name = f"Relatorio_cadop_{date.today().isoformat()}.csv"
    file_path = destination_dir / file_name

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
    except requests.RequestException as error:
        raise RuntimeError(f"Falha ao baixar o arquivo: {error}") from error

    file_path.write_bytes(response.content)

    print(f"Arquivo salvo em: {file_path}")
    return file_path
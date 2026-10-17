# ANS: pipeline de operadoras de planos de saúde

## Objetivo

Pipeline ETL em Python que baixa o cadastro de operadoras ativas da ANS, limpa os dados, grava em SQLite e responde perguntas de negócio com SQL. É o primeiro projeto do meu portfólio de engenharia de dados.

## Arquitetura

```mermaid
flowchart LR
    A[Portal ANS<br/>Relatorio_cadop.csv] --> B[extract.py<br/>baixa o CSV]
    B --> C[transform.py<br/>valida e limpa]
    C --> D[load.py<br/>grava no SQLite]
    D --> E[(operadoras.db)]
    E --> F[sql/consultas.sql]
```

## Como executar

1. Clonar o repositório e entrar na pasta:

```
   git clone https://github.com/AndersonMikaelJr/ans-operadoras-pipeline.git
   cd ans-operadoras-pipeline
```

2. Criar e ativar o ambiente virtual:

```
   python -m venv .venv
   .venv\Scripts\activate
```

3. Instalar as dependências:

```
   pip install -r requirements.txt
```

4. Rodar o pipeline:

```
   python src/main.py
```

5. Consultar o banco no DBeaver: `data/operadoras.db`, com as consultas em `sql/consultas.sql`.

> No Windows, se o PowerShell bloquear a ativação do ambiente virtual, rode uma vez: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

## Decisões de limpeza

| Problema | Exemplo no arquivo | Tratamento | Função |
|---|---|---|---|
| Zeros à esquerda | `000515`, CNPJ `00360305000104` | Ler tudo como texto | `validate_data` |
| Número com `.0` | `1001.0` | Remover o sufixo | `fix_number_decimals` |
| Espaços sobrando | `"ALICE "` | Remover nas colunas de texto | `clean_text_columns` |
| Campos vazios | `""` | Converter para nulo | `clean_text_columns` |
| Caixa inconsistente | `BAIRRO` e `LOGRADOURO` com trechos em minúsculas | Padronizar em maiúsculas | `standardize_case` |
| Valores de preenchimento | `******`, `XX@XX.XX` | Converter para nulo | `replace_placeholders` |
| Datas em texto | `2015-05-19` | Converter para data; inválidas viram nulo | `convert_dates` |
| Dados pessoais (LGPD) | `REPRESENTANTE`, `CARGO_REPRESENTANTE` | Remover as colunas | `remove_personal_data` |
| Telefones inválidos | DDD `01`, telefone com 16 dígitos | Marcar em `TELEFONE_SUSPEITO`, sem corrigir | `flag_suspicious_phones` |
| Região em branco | `REGIAO_DE_COMERCIALIZACAO` vazia | Manter como nulo e contar | `count_missing_region` |

Nenhuma linha é descartada: as regras tratam valores e removem colunas, mas não removem registros. Por isso o resumo da execução mostra 0 linhas descartadas.

## Principais resultados

- **Operadoras por modalidade:** Cooperativa Médica lidera com 262, seguida por Medicina de Grupo (252) e Administradora de Benefícios (182).
- **Top 5 UFs:** SP (375), RJ (134), MG (130), PR (64) e RS (56).
- **Espírito Santo:** 34 operadoras, em 6 modalidades.
- **Sem região de comercialização:** 4,3% das operadoras (48 de 1.105).
- **Concentração em 1998:** 495 operadoras, 44,8% do total. Vale confirmar no dicionário de dados o que essa data representa.
- **Operadora mais antiga por modalidade:** a Q6 traz uma por modalidade. Seis delas foram registradas em 16/12/1998, e o desempate usa o `REGISTRO_OPERADORA`.
- **Acumulado até 2026:** 1.105 registros (Q7).

## Consultas

As consultas estão em `sql/consultas.sql`, com um comentário por pergunta.
-- Pergunta 1: operadoras ativas por modalidade
SELECT MODALIDADE,
       COUNT(*) AS qtd_operadoras
FROM operadoras
GROUP BY MODALIDADE
ORDER BY qtd_operadoras DESC;

-- Pergunta 2: os 5 estados com mais operadoras
SELECT UF,
       COUNT(*) AS qtd_operadoras
FROM operadoras
GROUP BY UF
ORDER BY qtd_operadoras DESC
LIMIT 5;

-- Pergunta 3: operadoras sediadas no Espírito Santo, por modalidade
SELECT MODALIDADE,
       COUNT(*) AS qtd_operadoras
FROM operadoras
WHERE UF = 'ES'
GROUP BY MODALIDADE
ORDER BY qtd_operadoras DESC;

-- Pergunta 4: operadoras registradas por ano
SELECT strftime('%Y', DATA_REGISTRO_ANS) AS ano,
       COUNT(*) AS qtd_operadoras
FROM operadoras
GROUP BY ano
ORDER BY ano;

-- Pergunta 5: percentual de operadoras sem região de comercialização
SELECT ROUND(100.0 * SUM(REGIAO_DE_COMERCIALIZACAO IS NULL) / COUNT(*), 1) AS pct_sem_regiao
FROM operadoras;

-- Pergunta 6: operadora mais antiga de cada modalidade
WITH ranking AS (
    SELECT MODALIDADE,
           RAZAO_SOCIAL,
           DATA_REGISTRO_ANS,
           ROW_NUMBER() OVER (
               PARTITION BY MODALIDADE
               ORDER BY DATA_REGISTRO_ANS
           ) AS posicao
    FROM operadoras
)
SELECT MODALIDADE, RAZAO_SOCIAL, DATA_REGISTRO_ANS
FROM ranking
WHERE posicao = 1;

-- Pergunta 7: acumulado de registros ano a ano
WITH por_ano AS (
    SELECT strftime('%Y', DATA_REGISTRO_ANS) AS ano,
           COUNT(*) AS qtd_operadoras
    FROM operadoras
    GROUP BY ano
)
SELECT ano,
       qtd_operadoras,
       SUM(qtd_operadoras) OVER (ORDER BY ano) AS acumulado
FROM por_ano;
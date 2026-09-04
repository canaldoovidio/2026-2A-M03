# ADR-003: Regressão tabular com defasagens, em base trimestral, no lugar de séries temporais

**Data:** 03/08/2026
**Status:** Aceita, parcialmente revista pela ADR-010
**Decisores:** Prof. Ovidio Lopes da Cruz Netto

> **Nota de revisão (04/09/2026):** a `ADR-010` revoga a afirmação, no Contexto abaixo, de que "não
> existe versão mensal aberta dessas séries". A decisão principal deste ADR continua de pé:
> regressão tabular com defasagens no lugar de séries temporais, validada por corte temporal de
> data.

## Contexto

O TAPI da Louis Dreyfus Company pede previsão de produção de proteína animal com **horizonte de
24 meses** e, no mesmo documento, **proíbe explicitamente o uso de modelos de séries temporais**.

Há ainda um segundo descompasso, descoberto ao consultar a API do SIDRA durante a construção do
acervo: o TAPI fala em "abate mensal" e pede "projeções mensais", mas as cinco tabelas do IBGE que
sustentam o case (1092, 1093, 1094, 7524 e 1086) pertencem à **Pesquisa Trimestral**. Não existe
versão mensal aberta dessas séries. O período devolvido pela API vem como `AAAATT`, então
`202504` é o quarto trimestre de 2025, e não abril de 2025, confusão que, se passasse, produziria
um modelo treinado sobre um eixo de tempo inexistente.

Ou seja: o pedido do parceiro é de previsão de horizonte longo, com a família de modelos mais
óbvia vetada e numa granularidade que a fonte aberta não tem.

## Decisão

O módulo ensina **previsão de horizonte longo por regressão tabular**, com features de defasagem,
janelas móveis e codificação de sazonalidade, validada por **corte temporal de data** em vez de
embaralhamento aleatório. E trabalha em **base trimestral, com horizonte de 8 trimestres**, que
cobre exatamente os mesmos 24 meses que o parceiro pediu.

## Motivações

- **Respeita a restrição do parceiro** sem abandonar o problema: defasagem, janela móvel e
  sazonalidade codificada dão ao modelo tabular a memória temporal que ele precisa, sem que ele
  seja um modelo de série temporal.
- **Não inventa observação.** Interpolar trimestre em mês criaria dois terços de observações que
  ninguém mediu e contaminaria qualquer métrica de erro, o que seria um péssimo exemplo justamente
  num módulo sobre métricas de erro.
- **A restrição vira conteúdo.** O descompasso entre o que o parceiro pediu e o que a fonte
  permite medir é o assunto da Aula 02 (CRISP-DM) e da ART.1: negociar granularidade com quem pede
  o modelo é trabalho real de projeto, não desculpa técnica. A Aula 01 já provoca o reparo, ao
  fazer a turma descobrir na mão que a coluna `periodo` traz `2025-T4`.
- **Alinha com o resto da ementa.** Regressão tabular é o que as aulas 05 a 11 ensinam mesmo
  (supervisionado, ensembles, hiperparâmetros, explicabilidade, AutoML). Uma família paralela de
  modelos de série temporal exigiria uma trilha inteira que não cabe em 14 encontros.

## Riscos conhecidos

| Risco | Mitigação |
|---|---|
| Aluno aplicar `train_test_split` aleatório e vazar o futuro no treino | A Aula 09 trata vazamento temporal explicitamente, e o notebook da Aula 05 já usa corte por data desde a primeira vez que separa treino e teste. |
| A turma achar que "trimestral" foi preguiça nossa, não limitação da fonte | O motivo está escrito em `dados/README.md` e é discutido em sala na Aula 01 e na Aula 02, com a turma abrindo a interface do IBGE. |
| O parceiro receber a entrega em trimestres esperando meses | A contraproposta (8 trimestres cobrindo os 24 meses) é parte do escopo da ART.1, ou seja, é comunicada, não presumida. |
| Defasagem com base trimestral reduz muito o número de observações úteis | 117 observações por série, e a defasagem consome as primeiras. A Aula 04 dimensiona isso explicitamente ao construir as features. |

## Consequências

**Positivas.** O módulo inteiro ganha uma espinha dorsal coerente: o problema de previsão é
resolvido com as ferramentas que a ementa ensina, e a limitação de dado real virou objetivo de
aprendizagem em vez de nota de rodapé. As métricas (RMSE e MAPE) medem previsão sobre observações
que existem.

**Negativas.** O aluno sai do módulo sem ter visto ARIMA, Prophet ou família equivalente, o que é
uma lacuna real de repertório. A Aula 14 (Revisão e Futuro) é o lugar de nomear essa lacuna, para
o aluno saber que ela existe e por que foi deixada de fora aqui.

## ADRs relacionadas

- [ADR-004](ADR-004-case-ancorado-em-fontes-abertas.md): a granularidade trimestral é consequência
  direta de usar só fonte aberta.

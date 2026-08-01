# Dados do case (Louis Dreyfus Company)

Este diretório versiona as cinco séries do IBGE/SIDRA que sustentam o case da Louis Dreyfus
Company usado em todo o Módulo 03 IN. **Todos os notebooks das 14 aulas leem destes CSVs, nunca
da rede**: a aula não pode depender de o SIDRA estar no ar no dia da apresentação.

Os arquivos foram gerados por `tools/baixar_dados.py` e podem ser regenerados a qualquer momento
rodando `python3 tools/baixar_dados.py` (requer acesso à internet). A regeneração não é necessária
para as aulas: os CSVs aqui presentes já são a fonte de verdade do acervo.

## Contrato de colunas

Cada CSV tem exatamente três colunas:

- `periodo`: texto no formato `AAAA-TN` (por exemplo `2025-T4` para o quarto trimestre de 2025);
- `valor`: número (float) da série, ou vazio quando o IBGE marcou o dado como ausente/suprimido;
- `unidade`: texto com a unidade de medida do IBGE, igual em todas as linhas do arquivo.

## As séries são trimestrais, não mensais

As cinco tabelas pertencem à Pesquisa Trimestral do IBGE (abate de animais e produção de ovos e
leite). O período devolvido pela API vem como `AAAATT` (por exemplo `202504` é o **quarto
trimestre** de 2025, não o mês de abril). O acervo converte isso para o contrato `AAAA-TN`, então
`202504` vira `2025-T4`.

Não existe versão mensal aberta dessas séries. O IBGE publica avanço trimestral apenas; não há
interpolação de trimestre em mês porque inventar uma observação que não foi medida contaminaria
qualquer métrica de erro do modelo preditivo, o que seria um péssimo exemplo justamente num módulo
sobre isso.

## TAPI pede mensal, o dado aberto é trimestral

O TAPI da Louis Dreyfus Company fala em "abate mensal" e pede "projeções mensais". As fontes
abertas do IBGE que sustentam essas séries, porém, só existem em base **trimestral**. Esse
descompasso não foi escondido nem contornado por interpolação: virou conteúdo de aula.

Decisão do professor, tomada com esse fato confirmado na API: **o acervo trabalha em base
trimestral, com horizonte de previsão de 8 trimestres**, o que cobre os mesmos 24 meses que o
parceiro pediu, só que na granularidade que o dado realmente permite medir. A Aula 02 (CRISP-DM) e
a ART.1 (Entendimento do negócio) discutem essa diferença explicitamente: negociar granularidade
com quem encomenda o modelo é trabalho real de projeto de dados, não um detalhe técnico a esconder.

## As tabelas SIDRA têm dimensões extras

Além do período, as tabelas trazem dimensões como tipo de rebanho bovino, tipo de inspeção
(federal/estadual/municipal) e referência temporal (mês dentro do trimestre). O script pede a
variável específica de cada série (nunca `v/all`, que traria peso, número de informantes e
percentuais misturados no mesmo arquivo) e filtra apenas as linhas em que essas dimensões extras
vêm marcadas como "Total", que é o agregado do trimestre inteiro. Sem esse filtro, o mesmo
trimestre apareceria repetido várias vezes com recortes diferentes (por tipo de rebanho, por tipo
de inspeção etc.), e a série ficaria silenciosamente errada.

## As cinco séries

### `abate_bovinos.csv`

- Tabela SIDRA: 1092 (Trimestre de referência, com abate de bovinos)
- Variável: 285, "Peso total das carcaças" (escolhida porque é a série física do abate; a mesma
  tabela também devolve "Número de informantes" e percentuais, que não são a série de interesse)
- URL: `https://apisidra.ibge.gov.br/values/t/1092/n1/all/v/285/p/all`
- Baixado em: 01/08/2026
- Unidade: Quilogramas
- Período coberto: `1997-T1` a `2026-T1` (117 registros, granularidade trimestral)

### `abate_suinos.csv`

- Tabela SIDRA: 1093
- Variável: 285, "Peso total das carcaças"
- URL: `https://apisidra.ibge.gov.br/values/t/1093/n1/all/v/285/p/all`
- Baixado em: 01/08/2026
- Unidade: Quilogramas
- Período coberto: `1997-T1` a `2026-T1` (117 registros, granularidade trimestral)

### `abate_frangos.csv`

- Tabela SIDRA: 1094
- Variável: 285, "Peso total das carcaças"
- URL: `https://apisidra.ibge.gov.br/values/t/1094/n1/all/v/285/p/all`
- Baixado em: 01/08/2026
- Unidade: Quilogramas
- Período coberto: `1997-T1` a `2026-T1` (117 registros, granularidade trimestral)

### `producao_ovos.csv`

- Tabela SIDRA: 7524
- Variável: 29, "Quantidade de ovos produzidos" (a tabela também traz recorte por finalidade da
  produção; a variável 29 é o total)
- URL: `https://apisidra.ibge.gov.br/values/t/7524/n1/all/v/29/p/all`
- Baixado em: 01/08/2026
- Unidade: Mil dúzias
- Período coberto: `1987-T1` a `2026-T1` (157 registros, granularidade trimestral, série mais
  longa das cinco)

### `producao_leite.csv`

- Tabela SIDRA: 1086
- Variável: 282, "Quantidade de leite cru, resfriado ou não, adquirido" (é o volume formalmente
  captado pelos laticínios, não uma estimativa de produção total da pecuária leiteira)
- URL: `https://apisidra.ibge.gov.br/values/t/1086/n1/all/v/282/p/all`
- Baixado em: 01/08/2026
- Unidade: Mil litros
- Período coberto: `1997-T1` a `2026-T1` (117 registros, granularidade trimestral)

## Checagem de sanidade dos valores

Verificado manualmente que a ordem de grandeza de cada série é compatível com o que ela mede:

- **Abate de bovinos**: entre 782 milhões e quase 3 bilhões de quilogramas por trimestre. Casa dos
  bilhões de quilogramas é o esperado para peso de carcaça bovina no Brasil por trimestre.
- **Abate de suínos**: entre 236 milhões e 1,5 bilhão de quilogramas por trimestre. Plausível para
  peso de carcaça suína.
- **Abate de frangos**: entre 860 milhões e 3,7 bilhões de quilogramas por trimestre, a maior das
  três séries de abate, compatível com o Brasil ser um dos maiores produtores mundiais de carne de
  frango.
- **Produção de ovos**: entre 289 mil e 1,26 milhão de "mil dúzias" por trimestre (ou seja, entre
  cerca de 3,5 e 15 bilhões de dúzias de ovos por trimestre), plausível para produção nacional.
- **Produção de leite (captação formal)**: entre 2,4 e 7,4 bilhões de litros por trimestre,
  plausível para leite cru formalmente adquirido pelos laticínios (é menor que a produção total
  estimada da pecuária leiteira, porque não conta o leite não comercializado formalmente).

Em nenhum dos cinco arquivos os valores caem na casa das centenas ou milhares, o que seria sinal de
ter pego "número de informantes" em vez da série física real.

## Regeneração

```bash
python3 tools/baixar_dados.py
```

O script sobrescreve os cinco CSVs em `dados/`. Rodar `python3 -m pytest tools/tests/test_dados.py -v`
depois para validar o resultado (colunas do contrato, período em `AAAA-TN`, sem período repetido,
unidade única por arquivo, cobertura mínima de dez anos e ordem de grandeza plausível).

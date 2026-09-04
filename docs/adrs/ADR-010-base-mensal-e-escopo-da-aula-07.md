# ADR-010: A base do case passa a ser mensal a partir da Aula 07, e a Aula 07 reduz o próprio escopo de sete assuntos para três

**Data:** 04/09/2026
**Status:** Aceita
**Decisores:** Prof. Ovidio Lopes da Cruz Netto

## Contexto

A `ADR-003` registrou, em 03/08/2026, que "não existe versão mensal aberta" das cinco tabelas do
SIDRA que sustentam o case (1092, 1093, 1094, 7524 e 1086), e que a contraproposta era trabalhar
com horizonte de 8 trimestres, cobrindo os mesmos 24 meses que o TAPI da Louis Dreyfus Company
pede. Essa afirmação estava incompleta. As cinco tabelas trazem a classificação `c12716`,
"Referência temporal", com quatro categorias: "Total do trimestre", "No 1º mês", "No 2º mês" e "No
3º mês". `tools/baixar_dados.py` pedia a série sem informar essa classificação, e o filtro que
seleciona apenas as linhas marcadas como "Total" (usado para descartar recortes por tipo de
rebanho e tipo de inspeção) selecionava o trimestre em silêncio, sem que o script percebesse que
estava descartando os três meses junto.

Pedindo a série com a classificação `c12716` explícita, as cinco tabelas devolvem 351 registros
mensais em três das cinco séries (abate de bovinos, suínos e produção de leite, `1997-01` a
`2026-03`) e 471 na série mais longa (produção de ovos, `1987-01` a `2026-03`), contra 117 e 157
registros trimestrais, respectivamente. `dados/mensal/` versiona essa granularidade nova; `dados/`
trimestral fica intacto, porque as Aulas 01 a 06, já publicadas, leem dele e citam achados medidos
nele (113 linhas úteis após defasagem, MAPE de 1,60% no Modelo 1 da `ADR-008`, silhueta 0,4795 no
K-means da `ADR-009`).

Verificando a reconciliação entre as duas versões, a soma dos três meses bate exatamente com o
trimestre nas três séries de abate, medidas em quilogramas sem arredondamento. Em produção de ovos
e de leite, medidas em "Mil dúzias" e "Mil litros" com cada mês arredondado de forma independente
pelo IBGE, a soma diverge do trimestre em 1 unidade em 59 dos 157 trimestres de ovos e em 39 dos
117 de leite.

Paralelamente, a Aula 07 acontece hoje, 04/09/2026, e o roteiro em `PLANEJAMENTO_AULA_A_AULA.md`
previa sete assuntos: árvore de decisão, KNN, Random Forest, matriz de confusão, precisão e
revocação, Naive Bayes, regressão logística e SVM, com entropia calculada à mão como exercício. O
professor pediu o mesmo ajuste de ritmo que motivou a `ADR-009` na Aula 06: baby steps, menos
assuntos novos por encontro, mais profundidade em cada um. Adicionalmente, os quatro assuntos de
classificação (matriz de confusão, precisão, revocação e as três famílias de modelo associadas)
exigem rotular cada trimestre ou mês como "alta" ou "baixa" demanda, rótulo que nenhuma das cinco
séries do SIDRA carrega.

## Decisão

A base do case passa a ser mensal, da Aula 07 em diante. `dados/mensal/` é a fonte usada a partir
de hoje; `dados/` trimestral continua existindo, sem alteração, para as Aulas 01 a 06. Isso revoga
da `ADR-003` a afirmação de que não existe versão mensal aberta dessas séries. A decisão principal
da `ADR-003` continua de pé: regressão tabular com defasagens no lugar de séries temporais, e
validação por corte temporal de data. O horizonte muda de 8 trimestres para 24 meses, que é o
mesmo intervalo medido na granularidade que o TAPI pede desde o início.

O escopo da Aula 07 cai de sete assuntos para três. Ficam árvore de decisão, KNN e Random Forest.
Migram para a Aula 09: matriz de confusão, precisão, revocação, Naive Bayes, regressão logística,
SVM e entropia calculada à mão.

## Motivações

- **A afirmação revogada era factualmente errada, e um ADR não deve continuar afirmando algo que a
  própria fonte desmente.** A classificação `c12716` está documentada na API do SIDRA desde antes
  da `ADR-003`; o que faltou foi pedir essa dimensão explicitamente.
- **Medir 24 meses em meses elimina uma conversão que a `ADR-003` precisava justificar.** A
  contraproposta de 8 trimestres deixa de ser necessária porque o dado aberto entrega a mesma
  granularidade que o parceiro pediu, sem interpolar nenhuma observação.
- **`dados/` trimestral não pode mudar sob quatro aulas já publicadas.** Reprocessar as Aulas 01 a
  06 para a base mensal invalidaria achados já citados em sala e em material de apoio.
- **A avaliação do professor sobre o ritmo da turma é a mesma que motivou a `ADR-009`.** Baby steps
  na Aula 06 consolidaram Python e conceitos de modelagem; o mesmo raciocínio vale para a Aula 07
  não empilhar sete modelos e métricas novas no mesmo encontro.
- **Métricas de classificação exigem um rótulo que o dado não tem.** Matriz de confusão, precisão e
  revocação pressupõem classes (por exemplo, trimestre de "alta" ou "baixa" demanda). Nenhuma das
  cinco séries do SIDRA carrega esse rótulo, e criá-lo com cuidado é trabalho de aula, não um
  degrau que caiba junto com árvore de decisão, KNN e Random Forest no mesmo encontro.

## Riscos conhecidos

| Risco | Mitigação |
|---|---|
| A tabela de riscos da `ADR-003` já previa "a turma achar que trimestral foi preguiça nossa, não limitação da fonte", com mitigação de mandar a turma abrir a interface do IBGE. O risco se materializou, mas por um motivo que essa mitigação não cobria: a leitura incompleta da própria fonte, que pediu a série sem a classificação `c12716` e filtrou "Total" em silêncio. | `tools/baixar_dados.py` agora pede a classificação `c12716` explicitamente para as duas granularidades, e `tools/tests/test_dados_mensal.py` cobre a cobertura mensal sem buraco. `dados/README.md` documenta a existência das duas versões e a data em que a mensal foi descoberta. |
| A divergência de 1 unidade entre a soma dos três meses e o trimestre, em 59 de 157 trimestres de ovos e 39 de 117 de leite, pode ser lida como erro de extração. | `dados/README.md` documenta a causa (arredondamento independente de cada mês em "Mil dúzias" e "Mil litros") e a reconciliação exata nas três séries de abate. Os testes toleram essa divergência de 1 unidade só nessas duas séries. |
| `dados/` trimestral e `dados/mensal/` desalinharem com o tempo, por alguém atualizar um sem atualizar o outro. | `tools/baixar_dados.py` gera as duas granularidades na mesma execução, a partir da mesma chamada à API. `dados/` trimestral fica congelado como histórico das Aulas 01 a 06 e não recebe nova lógica de extração além da já existente. |
| O rótulo de "alta" e "baixa" demanda, necessário para os assuntos que migram para a Aula 09, ainda não existe em nenhuma das cinco séries. | Fica registrado como pendência para quem construir a Aula 09, com prazo até 15/09/2026, e citado nas Consequências negativas deste ADR. |

## Consequências

**Positivas.** O case passa a medir os mesmos 24 meses que o TAPI pede, na granularidade que o
TAPI pede, sem interpolar nenhuma observação e sem precisar sustentar a contraproposta de 8
trimestres em sala. A Aula 07 fica no mesmo padrão de nivelamento que a `ADR-009` trouxe para a
Aula 06, com três modelos supervisionados praticados em profundidade (árvore de decisão, KNN e
Random Forest, cada um comparado por RMSE e MAPE contra a baseline da `ADR-008`) em vez de sete
assuntos superficiais. `dados/` trimestral permanece estável, e as Aulas 01 a 06 já publicadas não
precisam de nenhum retrabalho.

**Negativas.** A Aula 09 herda uma dívida grande, do mesmo tipo que a Aula 08 herdou da `ADR-009`:
matriz de confusão, precisão, revocação, Naive Bayes, regressão logística, SVM e entropia
calculada à mão somam-se ao escopo já previsto (desbalanceamento de classes, maldição de
dimensionalidade, domain knowledge e mais feature engineering), e vai precisar de um corte
compensatório ainda não decidido. Há também um descompasso com o autoestudo da Semana 05: a turma
já leu, antes do encontro de hoje, os autoestudos "Matriz de confusão, precisão e revocação",
"Naive Bayes", "Regressão Logística", "SVM - Support Vector Machine" e "Árvore de Decisão e
Entropia" (com o opcional "Árvore de Decisão com cálculo de Entropia passo a passo"), esperando
encontrar esses assuntos na Aula 07 de hoje. Com a redução de escopo, eles só chegam à sala onze
dias depois, na Aula 09 de 15/09/2026. Falta ainda definir o rótulo de "alta" e "baixa" demanda
que os assuntos migrados vão precisar, decisão que fica para quem construir a Aula 09.

## ADRs relacionadas

- [ADR-003](ADR-003-regressao-tabular-em-vez-de-series-temporais.md): a decisão principal
  (regressão tabular com defasagens, corte temporal por data) continua de pé; este ADR revoga só a
  afirmação de que não existe versão mensal aberta das cinco séries.
- [ADR-007](ADR-007-base-analitica-a-partir-das-cinco-series-do-sidra.md): a base analítica das
  cinco séries do SIDRA, que agora existe também em granularidade mensal.
- [ADR-009](ADR-009-reducao-de-escopo-da-aula-06.md): a mesma lógica de redução de escopo por
  pedido de baby steps do professor, aplicada primeiro à Aula 06 e agora à Aula 07, com a mesma
  prática de registrar a dívida herdada pela aula seguinte.

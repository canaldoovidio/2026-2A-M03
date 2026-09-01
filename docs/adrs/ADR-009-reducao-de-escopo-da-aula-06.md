# ADR-009: A Aula 06 fixa K em 4, move Elbow Plot e Silhouette Analysis para a Aula 08, e usa metade do encontro para retomar as Aulas 01 a 05

**Data:** 31/08/2026
**Status:** Aceita
**Decisores:** Prof. Ovidio Lopes da Cruz Netto e José Romualdo

## Contexto

A Aula 06 estava roteirizada em `PLANEJAMENTO_AULA_A_AULA.md` como seis blocos de K-means, Elbow
Plot e Silhouette Analysis, terminando na interpretação de perfis de dieta. Antes de escrever
qualquer slide, dois problemas apareceram ao mesmo tempo.

O primeiro é uma avaliação do professor sobre o nível da turma, em quatro eixos simultâneos:
mecânica de Python e pandas, com duplas que não conseguem reproduzir o notebook na própria
máquina; conceitos de modelagem, com a turma acompanhando o código sem saber dizer o que o número
significa; densidade e ritmo, num acervo em que a Aula 05 tem 34 slides e três achados novos em
105 minutos; e amarração com a entrega, com a turma sem saber o que a ART.6 pede.

O segundo é uma medição que derruba a premissa do roteiro original. O roteiro promete
"interpretar os clusters encontrados (por exemplo, trimestres de maior demanda de milho versus de
farelo de soja) e o que isso sugere sobre sazonalidade de dieta". Rodando K-means com K=4 sobre as
cinco séries de `dados/`, o dado não entrega isso.

Agrupando os níveis de produção padronizados (117 linhas, 1997-T1 a 2026-T1), os quatro clusters
são blocos contíguos de tempo, silhueta 0,4795, e a concordância com o trimestre do calendário é
de 26,5%, ou seja, o acaso de quatro grupos equilibrados (25%). As cinco séries crescem ao longo
de 29 anos, e o algoritmo segmenta a linha do tempo, não a dieta.

Convertendo cada trimestre em participação no total do próprio ano, o que remove a tendência,
K=4 sobre as 116 linhas de anos completos recupera o trimestre do calendário em 114 das 116
linhas (98,3%), mas a silhueta cai para 0,2853. O agrupamento mais útil, o que separa os
trimestres do calendário, é o que a métrica de qualidade reprova.

A Aula 06 é a primeira da Sprint 3 (planning em 31/08) e alimenta a **ART.6 Preparação dos Dados e
Modelagem** (peso 6, `PLANO_DE_ENSINO.md` seção 4), Semana 06, com review em 11/09.

## Decisão

A Aula 06 fixa K em 4, move Elbow Plot e Silhouette Analysis para a Aula 08, e usa metade do
encontro (50 minutos, dos sete blocos, três primeiros) para retomar as Aulas 01 a 05 por
diagnóstico e revisão dirigida, antes de chegar a K-means.

## Motivações

- **A avaliação do professor sobre o nível da turma nos quatro eixos** exige uma aula que
  consolide antes de avançar, e não uma aula que empilhe mais um método novo sobre uma base ainda
  não firme.
- **A medição mostra que o agrupamento prometido pelo roteiro original não existe no dado.**
  Agrupar os níveis das cinco séries acerta o trimestre do calendário em 26,5% das linhas, que é o
  acaso de quatro grupos. Agrupar a participação no ano acerta 98,3%, e a silhueta cai de 0,4795
  para 0,2853 nesse agrupamento útil. Manter o roteiro original ensinaria um exemplo cuja premissa
  pedagógica (clusters revelam perfis de dieta) o próprio dado desmente.
- **Separar "agrupar sem rótulo" de "escolher K" deixa cada assunto com seu próprio exemplo.** A
  Aula 06 usa o contraste entre as duas execuções para ensinar o conceito de agrupamento e o
  cuidado com a tendência. A Aula 08 herda um exemplo concreto, onde a métrica de silhueta premia
  o agrupamento menos útil, o que torna Elbow Plot e Silhouette Analysis mais fáceis de motivar.

## Riscos conhecidos

- **A Aula 08 fica sobrecarregada.** Ela ganha Elbow Plot e Silhouette Analysis em cima do próprio
  escopo (PCA e sistemas de recomendação) e vai precisar de um corte compensatório. Mitigação: o
  corte é decidido quando a Aula 08 for construída, e a dívida fica registrada em
  `docs/ANDAMENTO.md` para quem construir aquela aula não descobrir tarde.
- **Descompasso entre autoestudo e aula.** Os alunos leram os autoestudos "Determinando K: Elbow
  Plot" e "Determinando K: Silhouette Analysis" no autoestudo de 01/09 (Semana 05) e só vão ver o
  método em sala em 10/09 (Aula 08). Mitigação: a Aula 06 usa a silhueta como número lido nos dois
  agrupamentos, mesmo sem ensinar o método de escolha de K, para que o autoestudo não fique sem
  nenhum uso em sala antes da Aula 08.

## Consequências

**Positivas.**

- O roteiro da Aula 06 deixa de prometer um resultado que o dado não sustenta, e passa a usar a
  própria medição (silhueta que piora no agrupamento melhor) como conteúdo central.
- A turma sai da Aula 06 com o ambiente rodando e o modelo da Aula 05 reproduzido, o que ataca
  diretamente o eixo de mecânica de Python apontado pelo professor.
- A Aula 08 recebe Elbow Plot e Silhouette Analysis com um exemplo já medido e concreto, em vez de
  precisar construir um do zero.

**Negativas.**

- A Aula 08 precisa de um corte compensatório ainda não decidido, o que adia uma decisão de escopo
  em vez de resolvê-la agora.
- Escolher K deixa de ser uma decisão que cada dupla toma sobre o próprio cluster na Aula 06, o que
  muda a linha do daily da Aula 07 (deixa de perguntar "qual K você escolheu" e passa a perguntar
  pelos perfis encontrados).

## ADRs relacionadas

- `ADR-005-quatro-artefatos-por-aula.md`: os quatro artefatos por aula que a Aula 06 continua
  produzindo, mesmo com o escopo reduzido.
- `ADR-007-base-analitica-a-partir-das-cinco-series-do-sidra.md`: a base sobre a qual o K-means da
  Aula 06 é medido.
- `ADR-008-corte-temporal-e-baseline-de-coeficiente-fixo.md`: o protocolo do Modelo 1, cujo MAPE de
  1,60% a Aula 06 usa como alvo de reprodução no bloco de retomada com as mãos.

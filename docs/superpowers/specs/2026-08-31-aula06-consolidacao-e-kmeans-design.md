# Design: Aula 06, consolidação das Aulas 01 a 05 e K-means sobre o case

**Data:** 31/08/2026
**Status:** Aprovado
**Decisores:** Prof. Ovidio Lopes da Cruz Netto (avaliação de nível da turma), José Romualdo
**Aula:** 06 · 01/09/2026 · Aprendizado Não Supervisionado - parte I · Sprint 3
**Turma:** GRAD IN03 · 2026-2A · T25

---

## 1. Contexto

A Aula 06 estava roteirizada em `PLANEJAMENTO_AULA_A_AULA.md` como seis blocos de K-means,
Elbow Plot e Silhouette Analysis, terminando na interpretação de perfis de dieta. O Prof. Ovidio
avaliou que o conteúdo do módulo está acima do que a turma acompanha, e apontou quatro
problemas simultâneos:

1. mecânica de Python e pandas, com duplas que não conseguem reproduzir o notebook na própria
   máquina;
2. conceitos de modelagem, com a turma acompanhando o código sem saber dizer o que o número
   significa;
3. densidade e ritmo, num acervo em que a Aula 05 tem 34 slides e três achados novos em 105
   minutos;
4. amarração com a entrega, com a turma sem saber o que a ART.6 pede.

A Aula 06 é a primeira da Sprint 3 (planning em 31/08) e alimenta a **ART. 6 Preparação dos Dados
e Modelagem**, peso 6, Semana 06, com review em 11/09. É a última janela grande antes da entrega,
porque a Aula 07 (04/09) traz árvores e ensembles e a Aula 08 (10/09) cai na véspera do review.

### 1.1 A medição que derruba a premissa do roteiro original

Antes de escrever qualquer slide, K-means foi rodado sobre as cinco séries de `dados/`. O roteiro
original promete "interpretar os clusters encontrados (por exemplo, trimestres de maior demanda de
milho versus de farelo de soja) e o que isso sugere sobre sazonalidade de dieta". O dado não
entrega isso.

**Agrupando os níveis de produção padronizados**, com K=4 sobre as 117 linhas de 1997-T1 a
2026-T1, os quatro clusters são blocos contíguos de tempo:

| Cluster | n | Intervalo |
|---|---|---|
| 2 | 30 | 1997-T1 a 2004-T2 |
| 0 | 28 | 2004-T3 a 2011-T2 |
| 3 | 34 | 2011-T3 a 2020-T2 |
| 1 | 25 | 2019-T3 a 2026-T1 |

Silhueta 0,4795 e inércia 60,21. A concordância com o trimestre do calendário é de **26,5%**,
ou seja, o acaso (25% com quatro grupos equilibrados). As cinco séries crescem ao longo de 29
anos, a tendência domina a variância da matriz, e o algoritmo segmenta a linha do tempo porque foi
isso que a entrada perguntou.

**Convertendo cada trimestre em participação no total do próprio ano**, o que remove a tendência,
K=4 sobre as 116 linhas de anos completos (1997 a 2025) recupera o trimestre do calendário em
**114 das 116 linhas, 98,3%**:

| Cluster | T1 | T2 | T3 | T4 |
|---|---|---|---|---|
| 3 | 29 | 0 | 0 | 0 |
| 1 | 0 | 28 | 0 | 0 |
| 0 | 0 | 1 | 29 | 1 |
| 2 | 0 | 0 | 0 | 28 |

Silhueta 0,2853 e inércia 207,03. **O agrupamento mais útil é o que a métrica reprova**, e esse
contraste é o conteúdo central da aula.

As duas linhas que escapam são **2008-T2 e 2008-T4**, as duas alocadas no cluster do T3.

O perfil sazonal, em participação média no total do ano, agrupado pelo trimestre do calendário:

| Trimestre | Bovinos | Suínos | Frangos | Ovos | Leite |
|---|---|---|---|---|---|
| T1 | 23,57% | 23,65% | 24,37% | 24,35% | 25,05% |
| T2 | 24,81% | 24,96% | 24,74% | 24,86% | 23,11% |
| T3 | 25,88% | 26,01% | 25,47% | 25,43% | 24,89% |
| T4 | 25,74% | 25,38% | 25,41% | 25,36% | 26,95% |

Amplitude sazonal, em pontos percentuais entre o trimestre de maior e o de menor participação:
leite 3,85, suínos 2,35, bovinos 2,31, frangos 1,10, ovos 1,08.

Dois achados que servem ao case:

- **O leite tem pico no T4 e as carnes no T3.** Picos em trimestres diferentes é informação direta
  para o Modelo 2 do TAPI, que converte produção em demanda de ração.
- **O leite tem mais que o triplo da amplitude sazonal do frango**, 3,85 p.p. contra 1,10. Frango e
  ovos ficam empatados no piso (1,10 e 1,08, diferença de 0,02 p.p., que é ruído). Frango é o alvo
  do Modelo 1, treinado na Aula 05, e a amplitude pequena explica por que os coeficientes de `sen`
  e `cos` daquela regressão são pequenos mesmo depois de padronizar. O teste trava a razão entre
  leite e frango, não a ordem entre frango e ovos, que a medição não separa.

## 2. Objetivos

1. Recuperar as Aulas 01 a 05 com diagnóstico ao vivo, não com revisão expositiva.
2. Garantir que toda dupla saia da aula com o ambiente rodando e o modelo da Aula 05 reproduzido.
3. Ensinar agrupamento sem rótulo pelo contraste entre duas execuções sobre o mesmo dado.
4. Deixar cada dupla com a lista escrita do que falta para a ART.6.
5. Manter o título e os autoestudos oficiais da Semana 05 honrados pela aula.

## 3. Não-objetivos

- Não ensinar Elbow Plot nem Silhouette Analysis como método de escolha de K. Migram para a
  Aula 08. A silhueta aparece na Aula 06 apenas como número lido em dois agrupamentos.
- Não transformar a aula em oficina de entrega. O bloco de ART.6 tem dez minutos.
- Não construir a Aula 08 hoje, nem decidir o corte compensatório que ela vai precisar.
- Não corrigir os achados abertos das Aulas 01 a 04 listados em `docs/ANDAMENTO.md`.

## 4. Decisões

### 4.1 Elbow e Silhouette saem da Aula 06 e vão para a Aula 08

K fica **fixo em 4** na Aula 06, com o motivo dito em voz alta em sala: escolher K é assunto da
Aula 08. A Aula 06 usa a silhueta como número lido nos dois agrupamentos, então a Aula 08 recebe o
conceito já com um exemplo concreto onde a métrica premia o agrupamento menos útil.

Custo: a Aula 08 ganha dois autoestudos da Semana 05 em cima do próprio escopo (PCA e sistemas de
recomendação) e vai precisar de um corte compensatório, decidido quando ela for construída.

Registrado em `docs/adrs/ADR-009`.

### 4.2 A revisão dirigida usa slides planos, não pilha vertical do Reveal

`tools/check_slides.py` mede apenas `.reveal .slides > section`. Uma pilha vertical (section
aninhada) faria o validador medir o wrapper em vez de cada slide, criando ponto cego de layout, e
quebraria a numeração de rodapé.

Os cinco módulos de revisão são slides de topo, precedidos de um slide-índice que dá o número de
destino de cada módulo. O professor navega por número de slide.

### 4.3 O bloco de ART.6 entra mesmo com o formato escolhido sendo quiz

O formato escolhido para a consolidação foi quiz diagnóstico com revisão dirigida, que não produz
entregável. Como "amarração com a entrega" é um dos quatro problemas relatados, os dez minutos
finais viram amarração explícita com a ART.6. Se o tempo apertar ao vivo, esse bloco cede tempo
para a prática, e a decisão fica registrada nas notas do professor.

## 5. Roteiro do encontro

08h00 - 10h00 Autoestudo (Semana 05, os cinco desta aula):
Determinando K: Elbow Plot · Determinando K: Silhouette Analysis · Introdução ao aprendizado não
supervisionado (IBM) · K-means · Opcional: PCA

10h00 - 10h15 Daily da equipe. Abertura da Sprint 3, cujo planning foi em 31/08.

| Horário | Min | Bloco | Conteúdo |
|---|---|---|---|
| 10h15 | 15 | 1. Diagnóstico | Seis perguntas de quiz sobre as Aulas 01 a 05, cada uma sobre uma decisão do case com número medido. |
| 10h30 | 20 | 2. Revisão dirigida | O professor entra só nos módulos que o quiz reprovou. Cinco módulos disponíveis, dois ou três visitados. |
| 10h50 | 15 | 3. Retomada com as mãos | Cada dupla roda o notebook até reproduzir o MAPE de 1,60% da Aula 05. |
| 11h05 | 15 | 4. K-means, o conceito | Agrupar sem rótulo, distância euclidiana, por que padronizar. |
| 11h20 | 20 | 5. Prática, ato 1 e ato 2 | K=4 sobre os níveis, depois sobre a participação no ano. |
| 11h40 | 10 | 6. Interpretação | Os quatro perfis, o pico deslocado do leite, e a silhueta que piora no agrupamento melhor. |
| 11h50 | 10 | 7. ART.6 | O que a entrega pede, o que já conta, e a pendência que cada dupla anota. |

### 5.1 Perguntas do diagnóstico

Cada pergunta cobre uma aula e tem resposta medida e verificável no acervo. Nenhuma é sintaxe.

| # | Aula | Pergunta | Resposta |
|---|---|---|---|
| 1 | 03 | Qual das cinco séries tem o histórico mais longo? | `producao_ovos`, 157 registros desde 1987-T1. As outras quatro têm 117, desde 1997-T1. |
| 2 | 02 | O TAPI pede previsão mensal e o SIDRA publica trimestre. O que o módulo fez? | Negociou a granularidade: 8 trimestres cobrem os mesmos 24 meses. Não interpolou. |
| 3 | 04 | Por que a base analítica tem 113 linhas e não 117? | As quatro primeiras saem porque `lag4` não existe para elas. |
| 4 | 05 | Por que o corte treino/teste é por data e não aleatório? | Sorteio usa o futuro para prever o passado. A LDC extrapola, não interpola. |
| 5 | 05 | O modelo ganha da baseline de coeficiente fixo por quanto? | 0,10 ponto percentual de MAPE, 1,60% contra 1,69%, na última janela. |
| 6 | 05 | No pipeline da Aula 05, o `fit` do `StandardScaler` viu quais linhas da base? | As 105 de treino. O teste passa só pelo `transform`, para não vazar média nem desvio do teste para dentro do treino. |

### 5.2 Módulos de revisão dirigida

Um por aula, dois slides cada, visitados sob demanda: Aula 01 (ler o CSV, tipos), Aula 02
(CRISP-DM e a decisão de granularidade), Aula 03 (as cinco séries e a EDA), Aula 04 (junção,
defasagens, sazonalidade codificada, padronização), Aula 05 (corte temporal, baseline, RMSE e
MAPE, overfitting).

## 6. Artefatos a produzir

| Artefato | Caminho | Observação |
|---|---|---|
| Deck | `aulas/aula06.html` | 35 slides, dez deles condicionais |
| Material de apoio | `materiais/aula06.html` | inclui o achado das duas exceções de 2008 |
| Referências | `referencias/aula06.html` | os cinco autoestudos da Semana 05 com título exato |
| Notebook | `notebooks/aula06.ipynb` | precisa rodar em Colab sem instalação |
| Notas do professor | `docs/notas-do-professor/aula06.md` | cabeçalho na forma nova, como a Aula 05 |
| Figuras | `tools/graficos_aula06.py` | fonte a partir de 18 pontos |
| Testes | `tools/tests/test_clusters_aula06.py` | trava os números da seção 1.1 |
| ADR | `docs/adrs/ADR-009-*.md` | a redução de escopo e o motivo medido |

### 6.1 Documentos de planejamento a atualizar

- `PLANEJAMENTO_AULA_A_AULA.md`: roteiro da Aula 06 substituído; linha de resgate da Aula 07
  mantida (os perfis existem); escopo da Aula 08 ganha Elbow e Silhouette.
- `PLANO_DE_ENSINO.md`: coluna "camada da espiral" das Aulas 06 e 08.
- `index.html`: resumo e quatro botões do card da Aula 06.
- `docs/ANDAMENTO.md`: a Aula 06 sai de "não iniciado"; o custo herdado pela Aula 08 fica escrito.

## 7. Riscos

| Risco | Mitigação |
|---|---|
| Uma aula não conserta mecânica de Python. | O notebook de retomada roda em Colab em uma célula. Se ainda assim travar, é sinal de que o problema precisa de atendimento fora da aula, e as notas do professor dizem isso. |
| O quiz revela que a turma erra os seis itens, e 20 minutos de revisão não bastam. | As notas do professor trazem a ordem de prioridade: perguntas 4 e 5 primeiro, que são pré-requisito da Aula 07. |
| O deck passa no macOS e reprova no Ubuntu do CI. | Folga vertical mínima de 80px por slide, medida antes do commit. |
| A Aula 08 fica sobrecarregada. | Registrado na ADR-009 e em `docs/ANDAMENTO.md` como dívida declarada. |

## 8. Critérios de aceite

1. `python3 tools/check_slides.py aulas/aula06.html` passa, com folga vertical mínima acima de
   80px em todos os slides.
2. `python3 tools/check_brand.py` e `python3 tools/check_links.py` passam no acervo inteiro.
3. `python3 -m pytest tools/tests/ -v` passa, incluindo `test_clusters_aula06.py`, que trava a
   concordância de 26,5% do ato 1, a de 98,3% do ato 2, as duas exceções de 2008 e a ordem das
   amplitudes sazonais.
4. O notebook executa de ponta a ponta em ambiente limpo, sem instalação além do que o Colab já
   traz.
5. Os cinco autoestudos da Semana 05 aparecem em `referencias/aula06.html` com o título exato de
   `docs/autoestudos-por-semana.md`.
6. Nenhum número do deck, do material ou das notas é inventado: todos vêm da seção 1.1 ou dos
   testes já existentes da Aula 05.

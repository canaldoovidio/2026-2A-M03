# Design: Aula 07, hipóteses declaradas, árvores de decisão e a migração para base mensal

**Data:** 03/09/2026
**Status:** Aprovado
**Decisores:** Prof. Ovidio Lopes da Cruz Netto, José Romualdo
**Aula:** 07 · 04/09/2026 · Aprendizado Supervisionado - parte II · Sprint 3
**Turma:** GRAD IN03 · 2026-2A · T25

---

## 1. Contexto

A Aula 07 estava roteirizada em `PLANEJAMENTO_AULA_A_AULA.md` como cinco blocos de conteúdo novo:
árvore de decisão com entropia, ensembles e Random Forest, e métricas de classificação (matriz de
confusão, precisão e revocação). O Prof. Ovidio pediu quatro ajustes sobre esse roteiro:

1. manter a lógica de baby steps que a `ADR-009` instalou na Aula 06;
2. trazer a importância da criação de hipóteses em modelos preditivos;
3. dar uma pincelada de KNN;
4. abandonar a granularidade trimestral, porque a interface do SIDRA permite escolher mensal.

O quarto item contradiz a `ADR-003` e o `dados/README.md`, que afirmam que não existe versão mensal
aberta dessas séries. A afirmação foi verificada contra a API antes de qualquer slide, e é falsa.

A aula é a segunda da Sprint 3 e alimenta a **ART. 6 Preparação dos Dados e Modelagem**, peso 6,
Semana 06, com review em 11/09.

### 1.1 A granularidade mensal existe, e as cinco tabelas a têm

As cinco tabelas do case (1092, 1093, 1094, 7524 e 1086) trazem a classificação **`c12716`,
"Referência temporal"**, com quatro categorias: `115236` "Total do trimestre", `115233` "No 1º mês",
`115234` "No 2º mês" e `115235` "No 3º mês".

`tools/baixar_dados.py` pedia a série sem essa classificação e filtrava as linhas em que as
dimensões extras vinham marcadas como "Total", o que selecionava silenciosamente "Total do
trimestre". O filtro estava correto para o que o script pedia; o que faltou foi pedir os meses.

Baixando `c12716/115233,115234,115235` e mapeando trimestre e posição do mês para `AAAA-MM`:

| série | linhas mensais | período | vazios | duplicatas |
|---|---|---|---|---|
| `abate_bovinos` | 351 | 1997-01 a 2026-03 | 0 | 0 |
| `abate_suinos` | 351 | 1997-01 a 2026-03 | 0 | 0 |
| `abate_frangos` | 351 | 1997-01 a 2026-03 | 0 | 0 |
| `producao_ovos` | 471 | 1987-01 a 2026-03 | 0 | 0 |
| `producao_leite` | 351 | 1997-01 a 2026-03 | 0 | 0 |

**A reconciliação com o trimestral já versionado é exata nas três séries de abate**: somando os
três meses de cada trimestre, as 117 linhas de `abate_bovinos`, `abate_suinos` e `abate_frangos`
batem sem uma única divergência.

Ovos e leite divergem em **1 unidade** em 59 dos 157 trimestres e em 39 dos 117, respectivamente.
A causa é arredondamento: as unidades são "Mil dúzias" e "Mil litros", o IBGE arredonda cada mês de
forma independente, e a soma de três valores arredondados não precisa igualar o total arredondado.
A divergência é de uma parte em um milhão e não afeta nenhuma decisão do modelo. Ela **entra na
aula** como checagem de sanidade, não é escondida.

### 1.2 A hipótese central da aula é falsa, e isso foi medido

Base analítica mensal, montada como a da Aula 04 mas com `lag12` no lugar de `lag4` e sazonalidade
de período 12: **339 linhas de 1998-01 a 2026-03**, treino de 315 meses (1998-01 a 2024-03) e teste
de 24 meses (2024-04 a 2026-03), que são os mesmos 24 meses de horizonte que o TAPI pede.

Features `lag1, lag12, sen, cos`. Baselines calculadas no treino, fator da LDC 1,05299.

| modelo | RMSE | MAPE |
|---|---|---|
| A. repete o mês anterior | 88.925.206 | 6,73% |
| B. repete o mesmo mês do ano anterior | 75.627.562 | 5,10% |
| C. coeficiente fixo da LDC | 54.523.588 | 3,71% |
| regressão linear (padronizada) | 63.225.293 | 4,25% |
| **árvore de decisão `max_depth=3`** | **109.534.336** | **7,66%** |
| random forest, 300 árvores | 82.070.325 | 5,35% |
| KNN k=5 padronizado | 128.029.380 | 9,37% |
| KNN k=5 sem padronizar | 83.496.528 | 5,62% |

A árvore perde da reta, das três baselines e do KNN sem padronizar. Ela só ganha do KNN
padronizado, que é o único modelo pior que ela na tabela.

### 1.3 O diagnóstico é uma linha de código

A árvore de `max_depth=3` tem 8 folhas, e prevê a média do alvo em cada folha. Logo, **a maior
previsão que ela consegue emitir é a média da folha mais alta**:

| medida | valor | quando |
|---|---|---|
| máximo do alvo no treino | 1.226.709.256 | 2023-03 |
| **maior previsão que a árvore emite** | **1.090.166.234** | teto estrutural |
| máximo real no teste | 1.301.022.625 | 2026-03 |

**23 dos 24 meses de teste estão acima do teto da árvore**, e 5 deles estão acima até do máximo do
treino. A árvore não erra por falta de capacidade: ela erra porque a série tem tendência de alta e
árvore não extrapola. O aluno verifica isso com `arvore.predict(X_teste).max()`.

### 1.4 O remédio funciona, e devolve a árvore à disputa

Trocando o alvo de nível para a razão `y / lag12`, que é estacionária, e multiplicando a previsão
de volta por `lag12`. Mesmas features, mesmo corte, mesma semente:

| modelo | MAPE em nível | MAPE em razão |
|---|---|---|
| árvore de decisão `max_depth=3` | 7,66% | **3,86%** |
| random forest, 300 árvores | 5,35% | 4,48% |
| KNN k=5 padronizado | 9,37% | 4,59% |
| KNN k=5 sem padronizar | 5,62% | **3,71%** |
| regressão linear | 4,25% | 4,73% |

A árvore corta o erro pela metade. O KNN sem padronizar cai de 5,62% para 3,71% e **empata em MAPE
com a baseline da LDC**, perdendo dela só no RMSE (56.355.917 contra 54.523.588).

### 1.5 Padronizar piora o KNN nesta base, e o motivo é mensurável

A regra de bolso que a Aula 05 deixou é padronizar quando as escalas diferem por ordens de
grandeza. Aplicada aqui sem pensar, ela quase dobra o erro do KNN, em todo `k` testado:

| k | MAPE padronizado | MAPE sem padronizar |
|---|---|---|
| 3 | 8,14% | 5,82% |
| 5 | 9,37% | 5,62% |
| 10 | 10,09% | 6,10% |

O motivo é a composição da distância. Sem padronizar, os desvios são 2,45e8 para `lag1`, 2,485e8
para `lag12` e cerca de 0,71 para `sen` e `cos`, então a distância euclidiana fica assim repartida:

| feature | participação na distância |
|---|---|
| `lag1` | 49,2775% |
| `lag12` | 50,7225% |
| `sen` | 0,0000% |
| `cos` | 0,0000% |

Sem padronizar, o KNN procura o mês mais parecido **em volume de produção**, que é a semelhança
certa para este problema. Padronizar dá a `sen` e `cos` metade do peso da distância e força a busca
a casar posição no calendário, o que é a semelhança errada aqui.

A regra da Aula 05 não é revogada: padronizar iguala a influência das features na distância, o que
é o certo quando não se sabe qual importa e o errado quando se sabe. A afirmação é sobre quando
aplicar a regra, não contra a regra.

### 1.6 O modelo que ganha

Regressão linear sobre a razão, com `lag1, lag2, lag3, lag12, sen, cos, dias` mais as quatro séries
defasadas em um mês, 11 features: **RMSE 46.724.434 e MAPE 3,32%**, contra 54.523.588 e 3,71% da
baseline da LDC. A dupla sai da aula com um vencedor medido para a ART.6, e com o fato de que o
vencedor não é o modelo mais novo que ela aprendeu hoje.

## 2. Objetivos

1. A turma sai sabendo declarar uma hipótese sobre um modelo preditivo, escolher a medição que a
   testa e registrar o veredito, inclusive quando o veredito é contrário.
2. A turma sai sabendo o que uma árvore de decisão faz (parte o espaço, prevê a média da folha) e
   qual é a consequência disso numa série com tendência.
3. A turma reconhece KNN, sabe que ele decide por semelhança e sabe que a escolha da escala define
   o que "parecido" significa.
4. Cada dupla termina com a base mensal montada e o quadro de hipóteses preenchido, que é insumo
   direto da ART.6.

## 3. Não-objetivos

1. **Métricas de classificação** (matriz de confusão, precisão, revocação) ficam de fora. O case é
   de regressão, e usá-las exigiria rotular meses como "alta" e "baixa" demanda, rótulo que não
   existe no dado e que seria inventado só para ter o que classificar.
2. **Entropia calculada passo a passo à mão** fica de fora. A árvore desta aula é de regressão, e o
   critério dela não é entropia.
3. **Naive Bayes, regressão logística e SVM** ficam de fora.
4. **Retrofit das Aulas 01 a 06 para base mensal** fica de fora, ver seção 4.1.
5. **Teoria de bagging e de amostragem bootstrap** fica de fora. Random Forest entra como média de
   árvores, uma célula e um número.

## 4. Decisões

### 4.1 A base mensal vale da Aula 07 em diante, e o trimestral não é reescrito

`dados/mensal/` recebe as cinco séries novas. `dados/` trimestral fica intacto, porque os notebooks
das Aulas 01 a 06 leem de lá e os achados publicados (113 linhas, MAPE 1,60%, silhueta 0,4795)
foram medidos nessa base e já foram vistos pela turma.

Reescrever quatro aulas publicadas na véspera de uma quinta não é viável, e apagar o caminho
percorrido seria pior pedagogicamente do que mostrá-lo: a Aula 02 ensinou CRISP-DM, e voltar do
Modeling para o Data Understanding porque a fonte foi lida por completo é o ciclo funcionando, não
um erro a esconder.

### 4.2 A ADR-003 é parcialmente revista, não substituída

A `ADR-010` revoga desta afirmação da `ADR-003`: "Não existe versão mensal aberta dessas séries".
O que continua de pé é a decisão principal, regressão tabular com defasagens em vez de séries
temporais, e o corte temporal por data. O horizonte de 8 trimestres vira 24 meses, que são o mesmo
intervalo. A `ADR-003` passa a Status "Aceita, parcialmente revista pela ADR-010".

Vale registrar que a tabela de riscos da `ADR-003` previa o risco "a turma achar que trimestral foi
preguiça nossa, não limitação da fonte" e o mitigava mandando a turma abrir a interface do IBGE. O
risco se materializou por um motivo que a mitigação não cobria: a leitura da fonte é que estava
incompleta.

### 4.3 As hipóteses são a estrutura da aula, não um bloco dela

Cada bloco prático da aula testa uma hipótese declarada antes de a célula rodar, e termina
registrando o veredito no mesmo quadro:

| | hipótese | veredito | evidência |
|---|---|---|---|
| H1 | A granularidade do case é trimestral porque a fonte só tem trimestre | falsa | `c12716` entrega 351 meses por série, e os três meses somam o trimestre já versionado |
| H2 | A árvore captura o que a reta não captura, logo vence | falsa | MAPE 7,66% contra 4,25% da reta e 3,71% da baseline |
| H3 | A árvore perde porque não extrapola tendência | verdadeira | teto de 1.090.166.234, com 23 dos 24 meses de teste acima dele |
| H4 | Alvo em razão devolve a árvore à disputa | verdadeira | MAPE de 7,66% para 3,86% |

O quadro preenchido é o entregável da aula e o modelo do que a ART.6 pede.

### 4.4 O corte do escopo repete a lógica da ADR-009

Sete assuntos novos em 105 minutos contradizem o pedido de baby steps. Ficam três: árvore de
decisão como técnica central, KNN como pincelada de doze minutos e Random Forest como média de
árvores. O custo é o descompasso com o autoestudo, tratado na seção 7.

## 5. Roteiro do encontro

| horário | bloco | conteúdo |
|---|---|---|
| 10h00-10h15 | Daily | Cada dupla relata os perfis de cluster da Aula 06. |
| 10h15-10h25 | Resgate e H1 | A turma abre o SIDRA e acha a referência temporal mensal. H1 cai ao vivo. Volta ao Data Understanding do CRISP-DM. |
| 10h25-10h40 | Base mensal | Prática: montar a base mensal, chegar em 339 linhas, reconciliar com o trimestral. |
| 10h40-10h55 | Árvore de decisão | Teoria: partir o espaço, prever a média da folha. Sem entropia à mão. |
| 10h55-11h10 | H2 e H3 | Prática: treinar, medir, perder. Depois `arvore.predict(X_teste).max()` e achar o teto. |
| 11h10-11h22 | KNN | Pincelada: decidir por semelhança, e a escala definir o que é parecido. A tabela de participação na distância. |
| 11h22-11h35 | H4 | Prática: alvo em razão. Árvore 3,86%, KNN sem padronizar 3,71%. |
| 11h35-11h45 | Random Forest | Média de árvores. Uma célula, um número, sem teoria de bagging. |
| 11h45-12h00 | ART.6 | O quadro de hipóteses vira o formulário da entrega. Peso citado do `PLANO_DE_ENSINO.md`. |

## 6. Artefatos a produzir

| arquivo | conteúdo |
|---|---|
| `tools/baixar_dados.py` | estendido com `c12716`, gerando `dados/mensal/` sem quebrar `dados/` |
| `dados/mensal/*.csv` | as cinco séries mensais, contrato `periodo` em `AAAA-MM` |
| `dados/README.md` | seção mensal, a correção da afirmação errada e a nota de arredondamento |
| `aulas/aula07.html` | deck, cerca de 30 slides |
| `materiais/aula07.html` | material de apoio |
| `referencias/aula07.html` | os doze autoestudos da Semana 05 que faltam |
| `notebooks/aula07.ipynb` | as quatro hipóteses executadas |
| `docs/notas-do-professor/aula07.md` | condução, ordem de corte e a resposta pronta sobre o autoestudo |
| `docs/adrs/ADR-010-base-mensal-e-escopo-da-aula-07.md` | a revisão da ADR-003 e o corte de escopo |
| `tools/graficos_aula07.py` | o gráfico do teto da árvore e o do antes e depois da razão |
| `tools/tests/test_modelos_aula07.py` | trava os vereditos das quatro hipóteses, não só os números |
| `tools/tests/test_dados.py` | estendido para o contrato mensal e a reconciliação com o trimestral |

### 6.1 Documentos de planejamento a atualizar

`PLANEJAMENTO_AULA_A_AULA.md` (roteiro da Aula 07 e o que migra para a Aula 09),
`PLANO_DE_ENSINO.md` (a linha da Aula 07 e a menção à granularidade), `index.html` (habilitar os
quatro botões do card) e `docs/ANDAMENTO.md`.

## 7. Riscos

| risco | mitigação |
|---|---|
| A turma leu "Matriz de confusão", "Naive Bayes", "Regressão logística" e "SVM" para hoje e a aula não toca neles | A Aula 09 os assume, registrado na `ADR-010`. As notas do professor trazem uma resposta de trinta segundos para quando a pergunta vier. |
| A dupla concluir que árvore é um modelo ruim | O bloco de H4 existe justamente para desfazer isso: a árvore volta a 3,86% quando o alvo é o certo. As notas do professor marcam esse bloco como o que não pode ser cortado. |
| A dupla concluir que padronizar é errado | A seção 1.5 do material declara que a regra da Aula 05 não é revogada, e que a decisão é sobre quando aplicá-la. |
| Números medidos com `random_state=42` mudarem em outra versão do scikit-learn | `tools/tests/test_modelos_aula07.py` trava semente e vereditos, e o CI executa o notebook. |
| A base mensal ter tendência mais ruidosa e a turma achar que piorou | O MAPE mensal não é comparável ao trimestral, porque o alvo é outro. O material declara isso e compara sempre contra as baselines da própria base mensal. |
| A rede da sala cair na hora de baixar o CSV | O notebook lê de `dados/mensal/` versionado e traz o `try`/`except` em português que a Aula 06 instalou. |

## 8. Critérios de aceite

1. `python3 tools/check_brand.py`, `python3 tools/check_slides.py` e `python3 tools/check_links.py`
   passam, e o CI do Ubuntu também.
2. `python3 -m pytest tools/tests/ -v` passa, incluindo os testes novos.
3. Todo número citado em slide, material ou notas sai de `tools/tests/test_modelos_aula07.py`, de
   `tools/graficos_aula07.py` ou de `notebooks/aula07.ipynb`, executados sobre `dados/mensal/`.
4. Os notebooks das Aulas 01 a 06 continuam executando sem alteração.
5. O quadro das quatro hipóteses aparece nos quatro artefatos com os mesmos vereditos.
6. `referencias/aula07.html` lista os doze autoestudos que faltavam, fechando os dezessete da
   Semana 05 com os cinco de `referencias/aula06.html`.

# Aula 07, roteiro de sala. 04/09/2026

**O que existe agora:** os dois gráficos em `assets/img/aula07-teto-da-arvore.png`
e `assets/img/aula07-nivel-versus-razao.png`, os CSVs mensais em `dados/mensal/`,
e todos os números abaixo travados em `tools/tests/test_modelos_aula07.py`.
**Não existe ainda:** deck, notebook, material, referências.

---

## A aula em quatro hipóteses

### H1. "A granularidade do case é trimestral porque a fonte só tem trimestre." FALSA.

Abrir o SIDRA com a turma. As cinco tabelas (1092, 1093, 1094, 7524, 1086) têm a
classificação **c12716, "Referência temporal"**, com quatro categorias: Total do
trimestre, No 1º mês, No 2º mês, No 3º mês.

O acervo pedia a série sem essa classificação, e o filtro de "Total" selecionava
o trimestre em silêncio. Não era limite da fonte, era leitura incompleta dela.

Ganho: de 117 trimestres para **351 meses** por série, 1997-01 a 2026-03.

Checagem de sanidade que vale mostrar: a soma dos três meses bate **exatamente**
com o trimestre nas três séries de abate. Em ovos e leite diverge 1 unidade em
59 de 157 e 39 de 117 trimestres, porque a unidade é "Mil dúzias" e "Mil litros"
e o IBGE arredonda cada mês sozinho.

**Pergunta para a sala:** o que mais a gente aceitou como limite do dado sem ter
lido a fonte inteira?

---

### H2. "A árvore captura o que a reta não captura, logo ganha." FALSA.

Base analítica mensal: **339 linhas**, 1998-01 a 2026-03. Treino 315 meses
(1998-01 a 2024-03), teste **24 meses** (2024-04 a 2026-03), que é o horizonte
que o TAPI pede. Features: `lag1, lag12, sen, cos`.

| modelo | RMSE | MAPE |
|---|---|---|
| A. repete o mês anterior | 88.925.206 | 6,73% |
| B. repete o mesmo mês do ano anterior | 75.627.562 | 5,10% |
| **C. coeficiente fixo da LDC** | **54.523.588** | **3,71%** |
| regressão linear | 63.225.293 | 4,25% |
| **árvore de decisão max_depth=3** | **109.534.336** | **7,66%** |
| random forest 300 árvores | 82.070.325 | 5,35% |
| KNN k=5 padronizado | 128.029.380 | 9,37% |
| KNN k=5 sem padronizar | 83.496.528 | 5,62% |

A árvore é o pior modelo da tabela, tirando o KNN padronizado. Perde das três
baselines.

---

### H3. "A árvore perde porque não extrapola tendência." VERDADEIRA.

**Mostrar `assets/img/aula07-teto-da-arvore.png`.**

Peça para a turma olhar a coluna de previsões antes de qualquer teoria:

- a árvore tem **8 folhas**, mas os 24 meses de teste caem **todos na mesma folha**;
- ela emite **um único número, 1.090.166.234 kg, nos 24 meses**, de abril de 2024
  a março de 2026;
- esse número é **7,77% abaixo da média real** do período;
- **23 dos 24 meses** de teste estão acima dele;
- o máximo do treino é 1.226.709.256 (2023-03) e o máximo do teste é
  1.301.022.625 (2026-03).

Árvore prevê a média da folha. A maior previsão possível é a média da folha mais
alta, e isso é um teto. Numa série com tendência de alta, o futuro está acima do
teto.

Verificação de uma linha, para a dupla rodar: `arvore.predict(X_teste).max()`

A reta não tem esse teto: ela extrapola.

---

### H4. "Trocar o alvo para razão devolve a árvore à disputa." VERDADEIRA.

**Mostrar `assets/img/aula07-nivel-versus-razao.png`.**

Treinar em `y / lag12` (estacionária) e multiplicar a previsão de volta por `lag12`.

| modelo | MAPE em nível | MAPE em razão |
|---|---|---|
| árvore max_depth=3 | 7,66% | **3,86%** |
| random forest | 5,35% | 4,48% |
| KNN k=5 padronizado | 9,37% | 4,59% |
| KNN k=5 sem padronizar | 5,62% | **3,71%** |
| regressão linear | 4,25% | 4,73% (piora) |

A árvore corta o erro pela metade. A reta **piora**, porque ela já extrapolava e
a razão tira dela a informação de nível. Isso impede a leitura de que razão é
sempre melhor.

---

## A pincelada de KNN

KNN decide por semelhança: procura os k meses mais parecidos e devolve a média
deles. A pergunta é o que "parecido" significa, e quem responde isso é a escala.

**Padronizar piora o KNN aqui, em todo k testado:**

| k | MAPE padronizado | MAPE sem padronizar |
|---|---|---|
| 3 | 8,14% | 5,82% |
| 5 | 9,37% | 5,62% |
| 10 | 10,09% | 6,10% |

O motivo, medido. Sem padronizar, os desvios são 2,45e8 (`lag1`), 2,485e8
(`lag12`) e cerca de 0,71 (`sen`, `cos`). A distância euclidiana fica assim:

| feature | participação na distância |
|---|---|
| `lag1` | 49,2775% |
| `lag12` | 50,7225% |
| `sen` | 0,0000% |
| `cos` | 0,0000% |

Sem padronizar, o KNN acha o mês mais parecido **em volume**, que é a semelhança
certa aqui. Padronizar dá metade do peso a `sen` e `cos` e força a busca a casar
posição no calendário.

**Dizer em voz alta, senão a turma aprende errado:** a regra da Aula 05 não caiu.
Padronizar iguala a influência das features na distância. Isso é o certo quando
você não sabe qual importa, e errado quando você sabe.

---

## O fecho, para a ART.6

O modelo que **ganha** da baseline da LDC: regressão linear sobre a razão, com
`lag1, lag2, lag3, lag12, sen, cos, dias` mais as quatro séries defasadas em um
mês. Onze features.

**RMSE 46.724.434 e MAPE 3,32%**, contra 54.523.588 e 3,71% da baseline.

O vencedor não é o modelo mais novo que a turma aprendeu hoje.

---

## Quadro que a dupla entrega na ART.6

| | hipótese | veredito | evidência |
|---|---|---|---|
| H1 | a granularidade é imposta pela fonte | falsa | c12716 entrega 351 meses por série |
| H2 | a árvore ganha da reta | falsa | 7,66% contra 4,25% e 3,71% |
| H3 | a árvore perde por não extrapolar | verdadeira | um único valor nos 24 meses, 23 acima dele |
| H4 | alvo em razão recupera a árvore | verdadeira | 7,66% cai para 3,86% |

**ART. 6 Preparação dos Dados e Modelagem, peso 6, review em 11/09.**

---

## Se a turma perguntar do autoestudo

Eles leram matriz de confusão, precisão, revocação, Naive Bayes, regressão
logística e SVM para hoje, e a aula não toca neles. Resposta: o case é de
regressão, e classificar mês em "alta" e "baixa" demanda exigiria inventar um
rótulo que o dado não tem. Esses assuntos entram na Aula 09.

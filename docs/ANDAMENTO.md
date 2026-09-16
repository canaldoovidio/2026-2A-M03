# Andamento do acervo

Estado atual do repositório, para quem estiver retomando o trabalho. Fonte: o plano
`docs/superpowers/plans/2026-08-01-fundacao-e-aula01.md` (16 tasks, fundação do acervo mais a
Aula 01 como padrão-ouro para as 13 aulas restantes).

## Pronto

- **Tokens da marca e validador de fidelidade** (`assets/css/inteli-brand.css`,
  `tools/check_brand.py`): paleta oficial, tipografia (Platypi no lugar da Azurio), segmento
  Graduação.
- **Logo e grafismo isométrico** em três versões (`assets/img/inteli-logo-*.svg`,
  `assets/img/inteli-grafismo-graduacao.svg`).
- **Tema do deck** (`assets/css/inteli-theme.css`, `assets/css/inteli-print.css`) e o deck de
  referência de cada classe (`aulas/_fixture-tema.html`).
- **Validador de layout** (`tools/check_slides.py`), via Playwright: estouro de 1280x720,
  sobreposição de bloco, título colidindo com o logo.
- **JavaScript do deck**: quiz interativo, zoom por teclado, exportação em PDF
  (`assets/js/inteli-quiz.js`, `assets/js/inteli-zoom.js`, `assets/js/inteli-print.js`).
- **Extração dos autoestudos da Adalove** (`tools/extrair_autoestudos.py` →
  `docs/autoestudos-por-semana.md`).
- **Dados do case**: os cinco CSVs trimestrais do IBGE/SIDRA versionados em `dados/`
  (`tools/baixar_dados.py`, `dados/README.md`).
- **Documentos de planejamento**: `PLANO_DE_ENSINO.md` e `PLANEJAMENTO_AULA_A_AULA.md`, com os
  14 títulos conferidos caractere a caractere contra a Adalove.
- **Portal e validador de links**: `index.html` com os cards das 14 aulas agrupados por sprint, e
  `tools/check_links.py`.
- **Skills globais** (`inteli-course-design`, `inteli-deck-design`): ver seção "Skills globais"
  abaixo.
- **Agentes, hook e documentação do repositório**: `.claude/agents/construtor-aulas.md`,
  `.claude/agents/revisor-slides.md`, `.claude/settings.json`, `CLAUDE.md`, `README.md`, este
  arquivo.
- **Estilo das páginas de leitura** (`assets/css/inteli-material.css`): usado por `materiais/` e
  `referencias/`. Só tokens, nenhuma cor ou `font-family` literal. A TOC lateral sai do layout
  abaixo de 900px e o grid volta para uma coluna sem deixar buraco.
- **Aula 01 completa, os quatro artefatos** (`aulas/aula01.html`, `materiais/aula01.html`,
  `referencias/aula01.html`, `notebooks/aula01.ipynb`) mais as notas do professor
  (`docs/notas-do-professor/aula01.md`). Os quatro botões do card da Aula 01 no portal estão
  habilitados.
- **Aula 02 completa, os quatro artefatos** (`aulas/aula02.html`, `materiais/aula02.html`,
  `referencias/aula02.html`, `notebooks/aula02.ipynb`) mais as notas do professor
  (`docs/notas-do-professor/aula02.md`). O notebook dela é a fase 2 do CRISP-DM executada: mede os
  seis pilares de qualidade sobre as cinco séries, ainda sem pandas. Os quatro botões do card no
  portal estão habilitados.
- **Aula 04 completa, os quatro artefatos** (`aulas/aula04.html`, `materiais/aula04.html`,
  `referencias/aula04.html`, `notebooks/aula04.ipynb`) mais as notas do professor
  (`docs/notas-do-professor/aula04.md`) e as duas figuras
  (`tools/graficos_aula04.py`). O notebook constrói a base analítica que a Aula 05 recebe: junção
  das cinco séries, defasagens, sazonalidade codificada e padronização. Os quatro botões do card no
  portal estão habilitados. O deck tem 30 slides, incluindo dois blocos pedidos pelo professor
  depois da primeira versão: dez minutos de revisão das Semanas 01 a 03, para a Ponderada 1 de
  Computação, e onze minutos de hipóteses declaradas para a ART.5.
- **Aula 05 completa, os quatro artefatos** (`aulas/aula05.html`, `materiais/aula05.html`,
  `referencias/aula05.html`, `notebooks/aula05.ipynb`) mais as notas do professor
  (`docs/notas-do-professor/aula05.md`), as duas figuras (`tools/graficos_aula05.py`), a
  `docs/adrs/ADR-008` e a suíte `tools/tests/test_modelo_aula05.py`. O deck tem 31 slides. É o
  primeiro modelo preditivo do case: regressão de `abate_frangos` sobre a base analítica de 113
  linhas que a Aula 04 deixou pronta, com corte temporal de 8 trimestres (2024-T2 a 2026-T1),
  RMSE e MAPE contra três baselines, e o ciclo de overfitting e reprodutibilidade. Os quatro
  botões do card no portal estão habilitados.
- **Três achados da Aula 05, todos medidos antes de o primeiro slide ser escrito.** (1) O modelo
  ganha da baseline de coeficiente fixo por apenas **0,10 ponto percentual** de MAPE na última
  janela (1,60% contra 1,69%), e vence nas **doze janelas** consecutivas medidas, com média de
  2,18% contra 3,14%. É a aula que ensina que uma janela de oito trimestres não decide. (2) **Sem
  padronizar, o solver zera os coeficientes de sazonalidade**: as defasagens estão na casa de 1e9
  e `sen`/`cos` na de 1, o número de condição da matriz chega a 1,08e10, e a decomposição em
  valores singulares descarta as direções pequenas. Isso **contradiz parcialmente a Aula 04**,
  que afirmou que padronizar não muda as previsões de uma regressão sem regularização: a
  afirmação vale em álgebra exata e falha nesta base em ponto flutuante. O deck, o material e as
  notas do professor tratam a divergência abertamente. (3) O leite, que a H2 da Aula 04 mandou
  ficar de fora, **piora o MAPE de teste de 1,60% para 1,89%** e confirma a hipótese fora da
  amostra.
- **A segunda forma de vazamento do material da Aula 05 foi medida, e é inofensiva neste
  modelo.** Ajustar o `StandardScaler` sobre treino e teste juntos desloca a média do escalador
  em 12% de um desvio e devolve MAPE idêntico até a nona casa, porque regressão linear sem
  regularização é invariante a transformação afim das entradas. O achado veio de um teste de
  mutação: essa mutação passava nos oito testes originais. Em vez de escrever uma asserção que
  nunca falha (seção 8.2 da `inteli-course-design`), o teste passou a travar a invariância, e o
  material declara que a disciplina de `fit` só no treino vale por causa de KNN, SVM, regressão
  regularizada e PCA, que aparecem entre as Aulas 06 e 08.
- **Aula 06 completa, os quatro artefatos** (`aulas/aula06.html`, `materiais/aula06.html`,
  `referencias/aula06.html`, `notebooks/aula06.ipynb`) mais as notas do professor
  (`docs/notas-do-professor/aula06.md`), a `docs/adrs/ADR-009` e a suíte
  `tools/tests/test_clusters_aula06.py`. Os quatro botões do card no portal estão habilitados. A
  aula deixou de ser conteúdo novo e virou retomada das Aulas 01 a 05 (diagnóstico por quiz,
  revisão dirigida e reprodução do MAPE de 1,60% da Aula 05), seguida de K-means com K fixo em 4,
  motivo registrado na `docs/adrs/ADR-009`.
- **A medição que motivou a redução de escopo da Aula 06, feita antes do primeiro slide.**
  Agrupando os níveis das cinco séries (117 linhas, 1997-T1 a 2026-T1), K=4 produz silhueta 0,4795
  e concordância de **26,5%** com o trimestre do calendário, que é o acaso de quatro grupos
  equilibrados: os clusters são blocos contíguos de tempo, não perfis de dieta. Convertendo cada
  trimestre em participação no total do próprio ano, o que remove a tendência, K=4 sobre as 116
  linhas de anos completos recupera o trimestre do calendário em **114 das 116 linhas (98,3%)**,
  com exceção de **2008-T2 e 2008-T4**, mas a silhueta cai para **0,2853**. O agrupamento mais útil
  é o que a métrica de qualidade reprova, e esse contraste é o conteúdo central da aula. O perfil
  sazonal resultante mostra o leite com pico no T4 e as carnes no T3, e amplitude sazonal de 3,85
  pontos percentuais contra 1,10 do frango.
- **A estatística da Aula 04 fecha o ciclo completo** (hipótese declarada, teste escolhido,
  decisão, consequência no projeto), com quatro testes sobre os CSVs reais: Shapiro-Wilk,
  Pearson, Kruskal-Wallis e teste t pareado. O achado que sustenta o bloco: a sazonalidade do
  leite **não** é detectada pelo teste sobre a série em nível (p = 0,0739) e aparece com p da
  ordem de 1e-06 depois de remover a tendência, porque a variação entre anos infla a variação
  dentro dos grupos. `tools/tests/test_hipoteses_aula04.py` trava as decisões, não só os números,
  e se pula sozinho onde não houver scipy.
- **Aula 07 completa, os quatro artefatos** (`aulas/aula07.html`, `materiais/aula07.html`,
  `referencias/aula07.html`, `notebooks/aula07.ipynb`) mais as notas do professor
  (`docs/notas-do-professor/aula07.md`), a `docs/adrs/ADR-010` e a suíte
  `tools/tests/test_modelos_aula07.py`. Os quatro botões do card no portal estão habilitados. A
  aula corrige a granularidade do case: a classificação c12716 do SIDRA entrega 351 meses por
  série (1997-01 a 2026-03, 471 em ovos), e a base analítica mensal soma 339 linhas (1998-01 a
  2026-03), com treino de 315 meses e teste de 24 meses (2024-04 a 2026-03), o mesmo horizonte
  que a LDC pediu.
- **Os achados medidos antes do primeiro slide da Aula 07.** (1) A árvore de decisão
  (`max_depth=3`) emite um único valor nos 24 meses de teste, 1.090.166.234 kg, com 23 dos 24
  meses reais acima desse teto: MAPE de 7,66% em nível, pior que as três baselines. (2) Trocar o
  alvo para razão (`y / lag12`) recupera a árvore, cujo MAPE cai para 3,86%. (3) O modelo do
  fecho, regressão linear sobre a razão com onze features, vence a baseline de coeficiente fixo da
  LDC: MAPE de 3,32% contra 3,71%. (4) Padronizar piora o KNN em todo k testado: MAPE de 8,14%
  contra 5,82% em k=3, 9,37% contra 5,62% em k=5, e 10,09% contra 6,10% em k=10, porque sem
  padronizar a distância euclidiana já reparte quase igualmente entre `lag1` (49,28%) e `lag12`
  (50,72%), e padronizar dá peso artificial a `sen` e `cos`.
- **Aula 08 completa, os quatro artefatos** (`aulas/aula08.html`, `materiais/aula08.html`,
  `referencias/aula08.html`, `notebooks/aula08.ipynb`) mais as notas do professor
  (`docs/notas-do-professor/aula08.md`), a `docs/adrs/ADR-011`, as três figuras
  (`tools/graficos_aula08.py`) e a suíte `tools/tests/test_pca_aula08.py`. O deck tem 32 slides e
  os quatro botões do card no portal estão habilitados. A aula fecha a Sprint 3 com escolha de K
  por Elbow Plot e Silhouette Analysis sobre as duas bases trimestrais da Aula 06, e PCA sobre as
  onze features da base mensal da Aula 07, com escalador e PCA ajustados só nos 315 meses de
  treino.
- **Os achados medidos antes do primeiro slide da Aula 08.** (1) Na base de participação de cada
  trimestre no total do próprio ano, a inércia aponta K=3 (queda de 25,1% de K=2 para K=3 e de
  14,3% de K=3 para K=4), a silhueta é máxima em K=2 (0,3785) e só K=4 recupera o trimestre do
  calendário, com 98,3% de concordância contra 75,0% em K=3 e 50,0% em K=2: os dois critérios
  internos discordam entre si e nenhum aponta o valor que serve ao case. (2) PC1 vale 68,21% da
  variância e pesa entre 0,336 e 0,362 nas oito colunas em quilos, com peso abaixo de 0,021 em
  `sen`, `cos` e `dias`. PC2 (11,85%) e PC3 (9,24%) carregam o calendário: agrupar os 315 meses de
  treino em doze grupos no plano PC2 por PC3 recupera o mês em 91,7% das linhas, com silhueta de
  0,8037 para os rótulos verdadeiros de mês, sem que nenhuma coluna da matriz seja o número do
  mês. Quatro componentes chegam a 96,07% da variância. (3) O corte custa MAPE. O modelo do fecho
  da Aula 07 sai de 3,32% para 4,92% com dois componentes, 4,94% com quatro e 6,20% com nove, e
  perde da baseline de coeficiente fixo da LDC (3,71%) em todo k de 1 a 9. Só k=10 devolve os
  3,32%, porque PC9 e PC10, que valem 0,21% e 0,17% da variância, recebem coeficiente 22 e 27
  vezes o do PC1. Com os onze componentes o MAPE é idêntico ao das onze features até a nona casa
  decimal, já que PCA sem descarte é rotação, o que confirma a invariância medida na Aula 05.
- **Aula 09 completa, os quatro artefatos** (`aulas/aula09.html`, `materiais/aula09.html`,
  `referencias/aula09.html`, `notebooks/aula09.ipynb`) mais as notas do professor
  (`docs/notas-do-professor/aula09.md`), a `docs/adrs/ADR-012`, as três figuras
  (`tools/graficos_aula09.py`) e a suíte `tools/tests/test_problemas_aula09.py`. O deck tem 33
  slides e os quatro botões do card no portal estão habilitados. A aula abre a Sprint 4 com cinco
  erros silenciosos medidos na base mensal: vazamento temporal, acurácia em alvo desbalanceado,
  entropia, imputação e dimensionalidade.
- **Aula 10 completa, os quatro artefatos** (`aulas/aula10.html`, `materiais/aula10.html`,
  `referencias/aula10.html`, `notebooks/aula10.ipynb`) mais as notas do professor
  (`docs/notas-do-professor/aula10.md`), a `docs/adrs/ADR-013`, as quatro figuras
  (`tools/graficos_aula10.py`) e a suíte `tools/tests/test_ajuste_aula10.py`, com treze conclusões
  travadas e quatro versões propositalmente quebradas documentadas. O deck tem 34 slides e os
  quatro botões do card no portal estão habilitados. A aula fecha a Semana 07 e é a primeira do
  acervo **sem bloco de resgate separado**: ver a seção da dívida da ADR-012 abaixo.
- **Os achados medidos antes do primeiro slide da Aula 10.** (1) A AUC desfaz o empate da Aula 09:
  baseline majoritária 0,500, árvore de entropia 0,500 (a curva dela tem dois pontos, porque ela
  prevê a mesma classe nos 24 meses) e SVM RBF 0,738, com os três marcando 83,3% de acurácia. A
  regressão logística tem a pior acurácia entre as que não desabam (79,2%) e a melhor AUC das cinco
  (0,800): ordenar por acurácia e ordenar por AUC dão listas diferentes. (2) O ajuste de
  hiperparâmetros leva a floresta de 5,04% para 4,21% de MAPE, e o ganho vem de podar, não de mais
  árvores: só `max_depth=4` vale 0,59 ponto, só `min_samples_leaf=5` vale 0,64, as duas juntas
  valem 0,91, e dobrar `n_estimators` sem podar **piora** de 5,04% para 5,20%. O
  `RandomizedSearchCV` com nove sorteios acha a mesma combinação da grade cheia, com 45 treinos em
  vez de 135. (3) Na primeira dobra do `KFold(5)`, os 252 meses de treino são todos posteriores ao
  início da validação, e quatro das cinco dobras têm treino no futuro; no `TimeSeriesSplit(5)` esse
  número é zero nas cinco. (4) O SHAP sobre os 24 meses de teste e a importância por impureza sobre
  o treino concordam em `lag12` e `lag3` e se separam da terceira posição: `abate_bovinos_lag1` é a
  terceira por SHAP e a sexta por impureza. O partial dependence de `lag12` cai de 1,0931 para
  1,0101, ou seja de 9,3% para 1,0% de crescimento previsto.
- **Os achados medidos antes do primeiro slide da Aula 09.** (1) O sorteio aleatório melhora o
  MAPE de quem memoriza vizinho e piora quem não memoriza: KNN de 7,64% para 5,29%, árvore de
  8,81% para 6,31%, random forest de 5,70% para 4,04%, e a regressão linear sobre a razão de 3,32%
  para 3,60%. O mecanismo está contado mês a mês: no sorteio, 24 dos 24 meses de teste têm um mês
  vizinho no treino, contra 1 dos 24 no corte por data. (2) O RMSE não pode ser comparado entre os
  dois cortes, porque o alvo médio do teste sorteado é 35% menor (765.719.266 kg contra
  1.181.946.133 kg), e parte da queda de RMSE é escala do período. (3) Com o alvo binário do case
  (o abate do mês supera o mesmo mês do ano anterior, 78,1% de positivos no treino e 83,3% no
  teste), a baseline que prevê sempre a classe majoritária acerta 83,3%, com revocação 1,000, e
  **nenhum dos cinco classificadores supera essa acurácia**: SVM RBF e árvore de entropia repetem
  as quatro métricas da baseline prevendo alta nos 24 meses, o SVM linear chega a 83,3% decidindo
  quatro quedas, a regressão logística fica em 79,2% e o Naive Bayes gaussiano em 16,7%, com
  precisão e revocação zero na classe positiva. (4) A entropia da raiz vale 0,7584 bits, o melhor
  corte é `lag12` com 0,0632 bits, e os dois candidatos de calendário ganham 0,0082 (`dias`) e
  0,0043 (`sen`); a árvore com critério de entropia escolhe o mesmo corte da conta à mão.
  (5) Nenhum dos dez CSVs versionados tem valor vazio: a ausência do acervo é de período, com a
  junção interna descartando 120 dos 471 meses da união (25,5%). Mascarando 16 meses do treino, a
  média erra 34,53%, a mediana 34,38%, o último valor 7,60%, a interpolação linear 7,27% e o mesmo
  mês do ano anterior corrigido pelo fator médio 4,44%. (6) De 2 para 11 features, a distância
  euclidiana média entre meses de treino cresce de 1,65 para 4,31, o KNN piora de 3,71% para 5,01%
  e a regressão linear melhora de 4,71% para 3,32%.
- **ADRs** (`docs/adrs/ADR-001` a `ADR-012`): as doze decisões de arquitetura do acervo, para o
  fan-out não relitigar nenhuma. Motor Reveal.js, Platypi no lugar da Azurio, regressão tabular em
  base trimestral, case só com fonte aberta, os quatro artefatos por aula, as skills globais, a
  base analítica montada a partir das cinco séries do SIDRA, o protocolo de corte temporal e
  baseline do Modelo 1, a redução de escopo da Aula 06 (K fixo em 4, Elbow e Silhouette para a
  Aula 08), e a correção de granularidade da Aula 07 (base mensal a partir da classificação
  c12716 do SIDRA, com matriz de confusão, precisão, revocação, Naive Bayes, regressão logística,
  SVM e entropia calculada à mão movidos para a Aula 09), e a base e o escopo do PCA da Aula 08
  (onze features da base mensal no lugar dos boletins do Sindirações, e sistemas de recomendação
  reduzido a fecho conceitual de dez minutos), e o escopo da Aula 09 (alvo binário criado a partir
  das séries, vazamento medido por MAPE, imputação por mascaramento e curva ROC adiada para a
  Aula 10).
- **Integração contínua** (`.github/workflows/validate.yml` e `.github/workflows/static.yml`):
  validação em push e pull_request (marca, links, layout, pytest e execução dos notebooks, mais um
  passo que reprova se a validação alterar arquivo versionado) e publicação da raiz do repositório
  no GitHub Pages a cada push em `main`.

**Com isso, as 16 tasks do plano estão implementadas.** O que falta do plano é só o portão de
saída, abaixo.

## Em andamento / não iniciado

- **Aula 01: revisão do professor no navegador.** É o portão de saída do plano e ainda não
  aconteceu. Os validadores passam, mas o que o professor aprovar na capa, na densidade dos
  slides e no tom do material é o que vira contrato para as 13 aulas seguintes. Ver "Achados
  abertos" abaixo: são justamente as decisões que dependem dele.
- **O site está no ar e atualizado.** `https://canaldoovidio.github.io/2026-2A-M03/` publica
  as Aulas 01, 02 e 03 com os quatro artefatos cada. A política de branch do ambiente
  `github-pages` foi corrigida pelo professor em 07/08/2026, e o `static.yml` passou a
  publicar normalmente a cada push em `main` (run 31142595526, 22s).

- **Aulas 11 a 14**: os cards dessas aulas no portal seguem com os quatro botões em
  `aria-disabled="true"`. As Aulas 01 a 10 já existem. A **Aula 11, em 24/09**, é a próxima da
  fila, fecha a Sprint 4 e traz AutoML com PyCaret, mais o risco de dependência registrado abaixo.
  O agente `construtor-aulas` existe para esse fan-out, mas as dez primeiras aulas foram escritas
  sem ele, à mão, seguindo as mesmas skills.
- **O que a Aula 05 deixa marcado para as aulas seguintes.** As quatro séries defasadas em um
  trimestre derrubam o MAPE de teste para 1,14%, contra 1,60% do modelo de hoje, e ficaram de
  fora de propósito: entram como candidata declarada na Aula 07. O reajuste do modelo sobre a
  base completa, depois de a avaliação terminar, fica para a Aula 12 junto com o `Pipeline`. A
  repetição em janelas feita à mão hoje vira `TimeSeriesSplit` na Aula 10.
- **O que a Aula 06 deixa marcado para as aulas seguintes.** Os quatro perfis de trimestre do
  calendário (K=4 sobre a participação de cada série no total do ano) ficam prontos para a Aula 07
  relatar no daily. K deixou de ser escolhido pela dupla, então a Aula 08 herda a decisão de como
  escolher K, com o exemplo da silhueta que piora no agrupamento útil já medido. A Aula 08
  assumiu essa decisão: ver a seção "Dívida da ADR-009, quitada na construção da Aula 08" abaixo.

## Dívida da ADR-009, quitada na construção da Aula 08 em 08/09/2026

A `docs/adrs/ADR-009` moveu Elbow Plot e Silhouette Analysis da Aula 06 para a Aula 08, e a
`docs/adrs/ADR-011` registrou como a Aula 08 acomodou os quatro assuntos em 105 minutos:

- **O corte compensatório saiu de sistemas de recomendação**, que foi de bloco com discussão
  dirigida de 15 minutos para fecho conceitual de 10 minutos, sem prática. É o único dos quatro
  assuntos sem dado no acervo para sustentar prática e o único inteiramente coberto pelos
  autoestudos da semana.
- **O exemplo que a Aula 08 herdou já estava medido**, e não precisou ser refeito: silhueta 0,4795 no
  agrupamento que só segue o calendário do tempo (concordância de 26,5% com o trimestre, o acaso),
  contra silhueta 0,2853 no agrupamento que recupera o trimestre do calendário em 98,3% das
  linhas. É o caso em que a métrica de qualidade premia o agrupamento menos útil, e serve como
  motivação de abertura para Elbow Plot e Silhouette Analysis, e é o que o deck usa.
- **Descompasso entre autoestudo e aula.** Os autoestudos "Determinando K: Elbow Plot" e
  "Determinando K: Silhouette Analysis" são da Semana 05 (lidos em 01/09, antes da Aula 06), e o
  método só é ensinado em sala em 10/09, na Aula 08. A Aula 06 usa a silhueta como número lido nos
  dois agrupamentos, sem ensinar o método, o que ameniza mas não fecha o descompasso.

## Dívida da ADR-012, quitada na construção da Aula 10 em 16/09/2026

A `docs/adrs/ADR-012` deslocou curva ROC e AUC para a Aula 10, que já tinha GridSearch,
RandomSearch, `TimeSeriesSplit`, SHAP e partial dependence nos mesmos 105 minutos. A
`docs/adrs/ADR-013` registrou como a aula os acomodou:

- **ROC e AUC ocuparam o bloco de resgate, em vez de virar um sexto bloco.** Esta é a primeira aula
  do acervo **sem bloco de resgate separado**: os 15 minutos de abertura desfazem o empate que a
  Aula 09 mediu, e com isso a retomada da aula anterior e o primeiro conteúdo novo são a mesma
  coisa. Quem comparar a anatomia dos decks vai encontrar uma ordem diferente aqui, e ela é
  deliberada.
- **O empate que a Aula 09 deixou já estava medido**, e não precisou ser refeito: baseline
  majoritária, SVM RBF e árvore de entropia marcam 83,3% de acurácia, 0,833 de precisão, 1,000 de
  revocação e 0,909 de F1, os quatro valores idênticos. A AUC separa: 0,500 na baseline, 0,500 na
  árvore (a curva dela tem dois pontos) e 0,738 no SVM RBF. E a regressão logística tem a pior
  acurácia entre as que não desabam (79,2%) e a melhor AUC das cinco (0,800).
- **A Semana 07 fechou em dezenove autoestudos.** `referencias/aula09.html` reivindica nove e
  `referencias/aula10.html` os dez restantes, com título exato da fonte.

## Duas listas de features convivem a partir da Aula 10

Confundi-las inverte conclusão, e isso precisa ser dito toda vez que os números aparecerem juntos:

- A **Aula 07** treinou a floresta de 300 árvores sobre **quatro** colunas (`lag1`, `lag12`, `sen`,
  `cos`) e publicou **4,48%** de MAPE de teste em `notebooks/aula07.ipynb`.
- A **Aula 09** expandiu a base para **onze** features e nunca republicou a floresta sobre elas. A
  mesma floresta, sem ajuste, erra **5,04%** ali: as sete features acrescentadas pioram o modelo que
  ninguém ajustou, que é a maldição de dimensionalidade daquela aula medida no modelo do case.
- A **Aula 10** ajusta sobre as onze, e leva o erro a **4,21%**. A floresta ajustada sobre as quatro
  da Aula 07 erra **3,95%**, então o ajuste recupera a maior parte do custo das features novas, não
  todo. Escolher features não é assunto da Aula 10, e fica como gancho aberto.

## O que a Aula 10 deixa marcado para as aulas seguintes

- **A Aula 11 recebe o termo de comparação pronto:** floresta com `max_depth=4`,
  `min_samples_leaf=5` e `n_estimators=600` a 4,21% de MAPE, ajustada à mão. A pergunta de abertura
  daquela aula é se o PyCaret bate isso.
- **A vantagem do `KFold` no teste é ruído medido, e está dita em sala.** Com onze features ele
  termina 0,08 ponto à frente do `TimeSeriesSplit`; com quatro, 0,04 atrás. A vantagem troca de
  sinal conforme o conjunto de features, e os dois validadores escolhem a mesma poda nos quatro
  casos. O argumento para trocar é a estimativa ser auditável (252 dos 252 meses de treino da
  primeira dobra do `KFold` são posteriores ao início da validação), não ser melhor. Ver a seção 11
  de `materiais/aula10.html` e a seção de pergunta difícil em `docs/notas-do-professor/aula10.md`.
- **`shap` entrou no `requirements-ci.txt`**, e é a única dependência nova do módulo inteiro. O
  notebook da Aula 10 instala o pacote com mensagem em português quando ele não está presente, e a
  primeira checagem das notas do professor manda instalar no começo da aula, não às 11h30.

## Achados que valem para o acervo inteiro, da construção da Aula 10

Dois achados que apareceram construindo a Aula 10 e não são específicos dela:

1. **Corpo 18 numa figura densa chega ilegível à projeção, e nenhum validador pega isso.** Os
   scripts de figura do acervo fixam corpo 18, que é o piso de legibilidade do tema. Isso funciona
   para figura esparsa (a da Aula 09 tem quatro barras e dez rótulos curtos) e falhou nas quatro
   primeiras versões das figuras da Aula 10. A conta: a `section` limita a figura a cerca de 350px
   de altura, uma imagem 16:9 cabe então em cerca de 620px de largura numa tela de 1280, e o corpo
   18 chega com menos da metade do tamanho. `check_slides.py` aprova, porque a figura cabe; o
   problema só aparece em captura de tela do slide, que é o passo 3 do fluxo da
   `inteli-deck-design`. As figuras da Aula 10 subiram para corpo 26 e perderam elementos até
   caber: a grade deixou de rotular as 27 barras, o painel das dobras trocou dez frases por dez
   números, e o painel de SHAP passou a mostrar seis features em vez de onze. **A regra prática:
   contar os elementos de texto da figura antes de escolher o corpo, e conferir por captura de
   tela dentro do deck, nunca olhando o PNG isolado.** Isto provavelmente pertence à seção 8 da
   skill `inteli-deck-design`, junto com a armadilha 8.8 (`max-height` em imagem), e ainda não foi
   levado para lá.
2. **A folga vertical do slide no macOS prevê a reprovação no Ubuntu, e dá para medi-la.** O
   `CLAUDE.md` já registra que o CI mede com métricas de fonte diferentes, sem dizer como
   antecipar. Medindo a distância entre o elemento mais baixo de cada slide e o topo do rodapé,
   com Playwright: a Aula 04, que ficou com o CI vermelho de 19/08 a 24/08, tem 39px e 73px nos
   dois slides que reprovaram; a Aula 09, que passou, tem 120px no pior slide. A Aula 10 foi
   construída com 97px e 103px nos dois piores, foi apertada de propósito (figura menor,
   referências mais curtas) e ficou com 142px. **Abaixo de 120px, apertar antes de commitar.**

## Bloqueio conhecido da Aula 11: o PyCaret não roda em Python 3.12

Medido em 16/09/2026, durante a construção da Aula 10, antes de a Aula 11 começar:

- **`pycaret` 3.3.2 recusa Python 3.12 na importação**, com `RuntimeError: Pycaret only supports
  python 3.9, 3.10, 3.11`. Não é incompatibilidade silenciosa: é uma checagem explícita no
  `__init__.py` do pacote, então nenhum ajuste de versão de dependência contorna.
- **A instalação arrasta o resto do acervo para trás.** No venv de teste, o `pip install pycaret`
  fixou `scikit-learn` 1.4.2, `numpy` 1.26.4 e `pandas` 2.1.4, contra 1.9.1, 2.x e 3.0.5 do
  ambiente atual. Pôr `pycaret` no `requirements-ci.txt` sem isolamento muda a versão sob a qual os
  outros dez notebooks são executados no CI.
- **Consequências a decidir quando a Aula 11 for construída**, e que precisam de uma ADR própria:
  se o notebook da Aula 11 fica fora da execução do CI, se o Colab (que hoje roda 3.12+) consegue
  rodar PyCaret, e se o roteiro da aula sobrevive com outro comparador automático caso não consiga.
  O roteiro em `PLANEJAMENTO_AULA_A_AULA.md` pede `setup()` e `compare_models()` do PyCaret sobre a
  base de frango, e a Aula 11 fecha a Sprint 4 em 24/09.

## Achados que valem para o acervo inteiro, da construção da Aula 06

Três achados que apareceram construindo a Aula 06 e não são específicos dela:

1. **Tratamento de erro no download dos CSVs precisa ser retroportado para as Aulas 04 e 05.** O
   notebook da Aula 06 passou a falhar com mensagem em português quando a rede da sala cai
   (`try`/`except` orientando a dupla a pedir a pasta `dados` para uma dupla vizinha), enquanto os
   notebooks das Aulas 04 e 05 ainda levantam o traceback cru do `urllib`/`pandas` nesse caso.
   Retroportar o mesmo tratamento é trabalho pendente, fora do escopo desta task.
2. **Slide que revisa outra aula precisa ser copiado da aula original, não reescrito de
   memória.** A revisão do deck da Aula 06 encontrou três erros de código nos módulos de revisão
   dirigida, porque os trechos de código dos slides que revisam as Aulas 01 a 05 foram escritos de
   memória em vez de copiados dos decks que eles revisavam. A lição vale para qualquer aula futura
   que inclua um bloco de retomada de conteúdo já publicado: copiar o trecho do arquivo de origem,
   nunca reconstruir de cabeça.
3. **A Semana 05 tem dezessete autoestudos na fonte** (`docs/autoestudos-por-semana.md`), não doze
   nem cinco isoladamente: cinco pertencem à Aula 06 (Determinando K: Elbow Plot · Determinando K:
   Silhouette Analysis · Introdução ao aprendizado não supervisionado (IBM) · K-means · Opcional:
   PCA) e doze à Aula 07. `referencias/aula06.html` lista os cinco da Aula 06;
   `referencias/aula07.html`, quando construída, precisa listar os outros doze para a semana
   fechar a conta.

## Corrigido em 18/08/2026, junto com a Aula 04

- **A validação de CI estava vermelha desde a Aula 03.** O passo de execução dos notebooks
  instalava apenas `pandas`, e o notebook da Aula 03 passou a importar `matplotlib` e `seaborn` sem
  que a lista de dependências fosse atualizada junto (`ModuleNotFoundError: No module named
  'matplotlib'`). A lista saiu da linha de comando do workflow e virou `requirements-ci.txt`, com o
  motivo de cada pacote ao lado, como o próprio comentário do workflow já previa. A Aula 04
  acrescenta `scipy` e `scikit-learn`.
- **O roteiro da Aula 04 citava o Sindirações como segunda fonte da junção**, em
  `PLANEJAMENTO_AULA_A_AULA.md`, `PLANO_DE_ENSINO.md` e no resumo do card do portal, mas não existe
  série aberta do Sindirações em `dados/`. Os três documentos foram corrigidos, e o motivo está em
  `docs/adrs/ADR-007`.

## Ampliação da Aula 05, pedida pelo professor em 24/08/2026

- **Cinco SVG animados** (`tools/svg_aula05.py`), inline no deck e gerados a partir dos CSVs
  reais: os mínimos quadrados minimizando os resíduos, o corte por data contra o
  `train_test_split`, o erro que se acumula ao longo do horizonte, a banda fixa em kg percorrendo
  a série, e interpolar contra extrapolar no slide de abertura. São inline, e não `<img src>`, porque um `.svg` externo não enxerga as custom
  properties do tema e precisaria de cor literal, o que `check_brand.py` reprova. A animação é
  SMIL, para não colocar regra de uma aula no tema compartilhado. Todo `<animate>` parte de um
  estado já legível, porque o PDF exportado congela o primeiro quadro.
- **Dois conceitos novos na aula, e o segundo veio de uma pergunta de aluno.** (1) Um aluno
  perguntou se faz sentido usar intervalo de confiança numa série cujos valores crescem. Faz, e
  não o de largura fixa: ±1,96 desvio-padrão vale **±17,02% em 1998 e ±4,01% em 2026**, e o
  resíduo cresce em quilos enquanto encolhe em proporção (4,10% para 2,84%). A aula passou a usar
  banda empírica dos erros relativos por horizonte, que cobriu 7 dos 8 trimestres. (2) Ao
  construir isso apareceu que **todas as métricas da aula eram de um passo à frente**: cada
  previsão usava o `frangos_lag1` real. Prevendo os oito de uma vez, de forma recursiva, que é o
  horizonte de 24 meses do TAPI, o MAPE vai de **1,60% para 2,85%**, com o erro crescendo de
  -1,02% em h=1 para -6,95% em h=8. Os 1,60% não estão errados: respondem outra pergunta, e a
  comparação com a baseline segue válida porque ela tem a mesma limitação.
- **O slide de abertura foi redesenhado.** Ele tinha a pergunta disparada em corpo de texto comum
  (`.quiz-question` só define `margin: 0`, então fora do `quiz-slide` ela não ganha destaque
  nenhum), quatro blocos de texto sem hierarquia e a metade inferior vazia. A pergunta passou a
  ter tamanho de subtítulo, o texto caiu para três linhas e o conceito virou animação: dois
  painéis com dados reais, um prevendo 2014-T3 com vizinhos dos dois lados (interpolar, o que o
  sorteio produz) e outro prevendo 2026-T1 com o histórico parando em 2024-T1 (extrapolar, o que
  a LDC enfrenta), com o leque de incerteza abrindo sobre a região sem medição.
- O deck foi de 31 para 34 slides, e `PLANEJAMENTO_AULA_A_AULA.md` registra o acréscimo na janela
  de 11h30. A ordem de corte ao vivo, se o tempo apertar, está nas notas do professor.
- `tools/tests/test_modelo_aula05.py` foi de 9 para 12 testes, travando as três conclusões novas.

## Corrigido em 24/08/2026, junto com a Aula 05

- **A validação de CI estava vermelha desde 19/08**, e a causa não era conteúdo: o slide 25 da
  Aula 04 tinha 58px de folga vertical no macOS e estourava 13px no Ubuntu do CI, porque as
  métricas de fonte diferem entre os dois sistemas e o mesmo parágrafo ocupa mais linhas no Linux.
  Os dois parágrafos do `side-by-side` foram encurtados de três para duas linhas cada, sem alterar
  nenhum número nem a conclusão do slide, e a folga subiu para 93px. Encolher a figura foi
  descartado: ela já está no piso de legibilidade (18px na tela a 900px de largura), e reduzi-la
  para 820px levaria os rótulos a 16px. A armadilha ficou registrada em `CLAUDE.md`.
- **O deck da Aula 05 passou limpo no Ubuntu na primeira tentativa** (31 slides, sem estouro,
  sobreposição ou título no logo). A menor folga vertical dele é de 84px e a menor folga entre
  título e logo é de 32px, contra 17px da Aula 04, que já passava.

## Achados abertos da revisão da Aula 04

Dois achados da revisão da Aula 04 que valem para o acervo inteiro, não só para ela:

1. **As figuras da Aula 02 têm fonte abaixo do piso de legibilidade em projeção.** Medido: com
   `dpi=160` e exibição entre 860px e 900px, um rótulo de N pontos chega à tela com cerca de N
   pixels, então os `fontsize` de 8,5 a 12 de `tools/graficos_aula02.py` chegam a projetar entre
   9px e 12px, contra o piso de 18px que o tema fixa para texto de slide. `tools/graficos_aula04.py`
   já parte de 18 pontos e traz a conta escrita no cabeçalho. Aplicar o mesmo ajuste às figuras da
   Aula 02 é trabalho pendente, e a Aula 03 usa figuras geradas em notebook, que precisam da mesma
   conferência.
2. **O cabeçalho das notas do professor usa uma construção que as diretivas de tom proíbem**
   ("Material de condução do encontro, não de distribuição ao aluno. Não é resumo do deck: são as
   perguntas..."). O texto é idêntico nas Aulas 01 a 04. A decisão de reescrever o cabeçalho nas
   quatro de uma vez é do professor. **A Aula 05 já nasceu na forma nova**, em conformidade com as
   diretivas, e registra a divergência no fim do próprio arquivo: alinhar as quatro anteriores é
   uma edição de dois minutos quando houver decisão.

## Achados abertos da revisão da Aula 01

Três achados da conferência da Aula 01 que são **decisão do professor**, não correção mecânica,
porque os três moram no tema compartilhado e valeriam para as 14 aulas:

1. **Espaço vazio na metade inferior dos slides de conteúdo.** O tema alinha o conteúdo ao topo
   da seção, então um slide com título e três cartões deixa cerca de 300px em branco embaixo. O
   comportamento é herdado: `aulas/_fixture-tema.html` faz igual. Fica assim, como respiro, ou o
   bloco de conteúdo passa a distribuir a altura?
2. **`.cover-eyebrow` não recebe o tamanho que o tema pede.** O tema declara
   `--escala-complementar` (14px) para a linha de olho da capa, mas `.reveal p` tem
   especificidade maior e o texto renderiza a 18px, medido com `getComputedStyle`. O CSS diz uma
   coisa e faz outra. Corrigir com o seletor composto `.cover-slide .cover-eyebrow` deixa a linha
   visivelmente menor na capa, então é mudança de aparência, não só de código.
3. **Centralização vertical se perde no PDF.** Nos slides `section-slide` e `end-slide` o
   conteúdo aparece centralizado na tela e colado no topo no PDF exportado. A causa é a regra
   `.reveal .slides section.present { display: flex !important; }` estar restrita a `.present`,
   classe que não existe no modo de impressão. Confirmado gerando o PDF de verdade com
   `Page.printToPDF`, não por captura de `?print-pdf`. O fundo dos slides está preservado (o bug
   antigo não voltou); é só o alinhamento.

## Skills globais

`inteli-course-design` e `inteli-deck-design` vivem em `~/.claude/skills/`, fora deste
repositório, de propósito: nasceram da fundação do acervo do 03 IN, mas descrevem metodologia
Inteli e identidade visual Inteli em geral, reutilizáveis em qualquer módulo futuro, não só neste.
Consequência prática: elas **não aparecem em `git log` nem em `git diff` deste repositório**, e
quem clonar o repositório em outra máquina precisa ter essas skills instaladas globalmente para os
agentes `construtor-aulas` e `revisor-slides` funcionarem como descrito. O `CLAUDE.md` aponta para
os caminhos exatos.

## Fora do git de propósito

- **`Turma.xlsx`**: a planilha oficial da Adalove, com dado pessoal de aluno (nome, presença,
  nota). Fonte de `PLANO_DE_ENSINO.md`, `docs/autoestudos-por-semana.md` e dos pesos de ART, mas
  nunca versionada. Regenerar os derivados publicáveis com `python3 tools/extrair_autoestudos.py`.
- **`TURMA-*-TAPI-*.pdf`** (o TAPI da Louis Dreyfus Company): tem seção de conteúdo restrito do
  parceiro. Fonte do escopo do case, nunca versionada.

Os dois estão listados em `.gitignore`, com o motivo documentado ali: o repositório é publicado
inteiro no GitHub Pages, então qualquer arquivo commitado fica público.

## Pendências abertas

- **Leitura complementar do professor, nas aulas 01 e 02.** A seção 2 de
  `referencias/aula01.html` e de `referencias/aula02.html` existe com a estrutura fixa que o
  fan-out replica, mas a curadoria do professor ainda não foi feita. Hoje elas listam as fontes
  efetivamente citadas no deck e no material (na Aula 01, a tabela 1092 do SIDRA e três páginas da
  documentação de Python; na Aula 02, as cinco tabelas do SIDRA, o guia do CRISP-DM, os seis
  pilares da DAMA UK e Stevens 1946). Substituir ou completar quando o professor indicar.
- **Um autoestudo oficial tem travessão em dash no título.** "Opcional: Riscos e benefícios da IA
  — AI4People (Floridi et al., 2018)", da Semana 01, citado em `referencias/aula02.html`. O
  caractere é proibido no texto que o acervo escreve, mas aqui é citação literal do título da
  Adalove: alterá-lo quebraria a conferência título por título contra
  `docs/autoestudos-por-semana.md`. Está preservado de propósito, com o motivo escrito na própria
  página, para ninguém "corrigir" depois.
- **`nbconvert` não está instalado no Python do sistema.** O Homebrew marca o ambiente como
  gerenciado externamente (PEP 668), então a execução do notebook da Aula 01 foi validada num
  venv descartável. O `validate.yml` instala `nbconvert` e `ipykernel` no runner, mas quem rodar a
  bateria localmente precisa de um venv próprio. **Feito em 18/08/2026:** a lista de dependências
  virou `requirements-ci.txt`, e o workflow instala a partir dele.
- **O notebook é versionado sem saída de execução, de propósito.** O plano previa
  `nbconvert --execute --inplace`, mas gravar a saída no arquivo entrega o gabarito: a célula do
  desafio imprime as respostas das duas primeiras perguntas, e a célula do `KeyError` mostra o
  traceback que o aluno deveria ler por conta própria. A validação, local e no CI, executa uma
  cópia fora da árvore de trabalho, e o `validate.yml` tem um passo final que reprova se algum
  arquivo versionado for alterado pela validação.
- **`--shots` do `check_slides.py` só salva PNG de slide com problema.** O plano supunha que ele
  fotografava todos os slides, e não é o caso: a conferência visual da Aula 01 foi feita com um
  script próprio de captura. Se a conferência a olho vai ser passo obrigatório de toda aula, vale
  dar ao validador uma opção que fotografe o deck inteiro.
- `python3 tools/check_slides.py` sem argumento agora encontra `aulas/aula01.html` e passa. O
  fixture do tema (`aulas/_fixture-tema.html`) continua fora da descoberta automática de
  propósito, porque começa com `_`; para medi-lo, passar o caminho explicitamente.

## Achados abertos da revisão da Aula 02 (07/08/2026)

Dois achados que a revisão independente levantou e que são **decisão do professor**, não conserto
mecânico. Nenhum bloqueou a publicação.

1. **A legenda do ciclo CRISP-DM fala em "duas voltas documentadas", e a fonte primária tem três.**
   A Figura 2 do guia CRISP-DM 1.0 confirma as duas setas duplas que o deck desenha (Negócio com
   Dados, Preparação com Modelagem), mas traz também uma terceira conexão interna, de sentido
   único, ligando Avaliação direto a Entendimento do Negócio, por dentro do círculo. O ponto
   pedagógico do slide continua verdadeiro, mas a contagem é leitura incompleta da própria fonte
   citada. Corrigir na próxima revisão do diagrama.
2. **32 slides podem não caber nos sete blocos de 15 minutos.** O bloco de qualidade e taxonomia
   passou de "seis pilares e taxonomia, com exercício" para seis unidades de conteúdo distintas,
   cada uma com fonte primária própria, antes de qualquer interação. É factível se o professor
   escolher quais diagramas narra em detalhe e quais só aponta. Decisão de condução, não de
   arquivo.

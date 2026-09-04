# Planejamento Aula a Aula: Módulo 03 IN

Roteiro minuto a minuto dos 14 Encontros de Instrução do Prof. Ovidio, no formato Inteli. Este
documento e o `PLANO_DE_ENSINO.md` são a fonte da verdade do acervo: nenhum deck, material,
página de referências ou notebook inventa data, título, escopo ou autoestudo. Os autoestudos
citados abaixo têm título exato conferido contra `docs/autoestudos-por-semana.md`.

**Estrutura do encontro, igual nas 14 aulas:**

- `08h00 - 10h00` Autoestudo, feito pelo aluno antes da aula.
- `10h00 - 10h15` Daily da equipe: o que fiz, o que vou fazer, impedimentos.
- `10h15 - 12h00` Instrução em metodologia ativa, em sete blocos de 15 minutos. **Nenhum bloco
  passa de 15 minutos sem interação direta dos alunos**: cada bloco abaixo termina com uma
  pergunta disparada, um exercício em dupla ou uma prática de mão na massa antes de fechar.

---

### Aula 01 - 04/08/2026 - Introdução ao Python  (Sprint 1)

08h00 - 10h00  Autoestudo
  Instalação do Python e Jupyter Notebooks em VS Code
  Migrando do Javascript para o Python
  Listas, Tuplas, Conjuntos e Dicionários em Python
  Aprendendo a ler erros em Python

10h00 - 10h15  Daily da equipe
  O que fiz, o que vou fazer, impedimentos. Primeira aula: instalação do ambiente confirmada em
  cada máquina antes de seguir.

10h15 - 12h00  Instrução em metodologia ativa

  10h15 - 10h30  Resgate e abertura: não há aula anterior. Apresentação do case Louis Dreyfus
    Company, dos três modelos encadeados do TAPI (produção de proteína animal, demanda de ração,
    macroingredientes) e do papel do Python como ferramenta do módulo. Pergunta disparada à
    turma: "o que vocês esperam prever a partir de um CSV de abate de bovinos?", respostas
    registradas no quadro.

  10h30 - 10h45  Teoria: tipos primitivos e estruturas (listas, tuplas, conjuntos, dicionários)
    em Python, comparando com objetos e arrays de Javascript (autoestudo "Migrando do
    Javascript"). Exercício ao vivo: cada aluno converte um objeto JS dado no enunciado em um
    dict Python equivalente.

  10h45 - 11h00  Prática guiada, em duplas: abrir `dados/abate_bovinos.csv` no Jupyter, ler com
    `csv.reader`, contar registros e identificar as três colunas do contrato do arquivo
    (`periodo`, `valor`, `unidade`).

  11h00 - 11h15  Teoria: como ler um traceback em Python. O instrutor provoca de propósito um
    `IndexError` e um `KeyError` sobre o mesmo CSV e decifra em conjunto com a turma.

  11h15 - 11h30  Prática, em duplas: cada dupla provoca e corrige dois erros no próprio código de
    leitura do CSV, documentando o que cada traceback significava.

  11h30 - 11h45  Discussão dirigida: reparar que a coluna `periodo` vem como `2025-T4`, não como
    um mês. Pergunta disparada: "por que vocês acham que o dado vem assim?". As respostas ficam
    em aberto, para a Aula 02 aprofundar.

  11h45 - 12h00  Amarração com a sprint: a leitura do CSV construída hoje é o primeiro passo do
    entendimento do dado real do case, alimentando **ART.1 Entendimento do negócio**. Próximos
    passos e abertura da Sprint 1 (planning em 03/08).

---

### Aula 02 - 07/08/2026 - Visão Geral do Aprendizado de Máquina, Inteligência Artificial e Ciência de Dados  (Sprint 1)

08h00 - 10h00  Autoestudo
  Aspectos da qualidade dos dados (6 pilares)
  Dados estruturados e não estruturados
  Fonte de dados e taxonomia do dado
  Mais sobre Machine Learning: Introdução ao Aprendizado de Máquina
  Melhor forma de aprender Python (Google Colab Notebook)
  O que é Machine Learning
  Opcional: Listas e Tuplas - o que são e como usar estes Tipos Agregados em Python
  Opcional: Os 4 tipos de análises em Ciência de Dados
  Opcional: Riscos e benefícios da IA — AI4People (Floridi et al., 2018)
  Tipos de dados (nominal, ordinal, intervalar e razão)
  Um guia contemporâneo de IA para iniciantes

10h00 - 10h15  Daily da equipe
  O que fiz, o que vou fazer, impedimentos. Checkpoint: todas as duplas conseguiram ler o CSV de
  abate bovino até o fim da Aula 01?

10h15 - 12h00  Instrução em metodologia ativa

  10h15 - 10h30  Resgate: a Aula 01 deixou pronto a leitura do CSV de abate bovino e o reparo de
    que o período vem em trimestres. Pergunta disparada: "o TAPI da LDC pede previsão mensal.
    Nosso dado é trimestral. O que fazemos com isso?"

  10h30 - 10h45  Teoria: o que é Machine Learning, Inteligência Artificial e Ciência de Dados, e
    os quatro tipos de análise (descritiva, diagnóstica, preditiva, prescritiva). Exercício em
    duplas: classificar quatro perguntas retiradas do TAPI em um desses quatro tipos.

  10h45 - 11h00  Teoria: as seis fases do CRISP-DM (Entendimento do negócio, Entendimento dos
    dados, Preparação dos dados, Modelagem, Avaliação, Implantação), aplicadas passo a passo ao
    problema da LDC. Exercício em duplas: uma frase por fase, aplicada ao case.

  11h00 - 11h15  Discussão dirigida: o descompasso entre o TAPI pedir "abate mensal" com
    horizonte de 24 meses e as tabelas do SIDRA só existirem em base trimestral. Apresentação da
    decisão do professor: o módulo trabalha em base trimestral, horizonte de 8 trimestres, que
    cobre os mesmos 24 meses. Votação levantando a mão: "vocês teriam aceitado o pedido do
    parceiro sem checar a fonte de dados primeiro?"

  11h15 - 11h30  Prática, em duplas: desenhar em papel os três modelos encadeados do TAPI
    (produção por categoria, demanda de ração, macroingredientes), indicando qual fonte (SIDRA ou
    Sindirações) alimenta cada um.

  11h30 - 11h45  Teoria: qualidade de dados (os seis pilares) e taxonomia do dado, aplicadas às
    cinco séries do case. Exercício: cada dupla aponta um risco de qualidade citado no
    `dados/README.md`.

  11h45 - 12h00  Amarração com a sprint: o entendimento de negócio formalizado hoje, incluindo a
    negociação explícita de granularidade entre o pedido do parceiro e o dado disponível,
    alimenta **ART.1 Entendimento do negócio** (peso 6). Fecha o primeiro ciclo da Sprint 1.

---

### Aula 03 - 11/08/2026 - Introdução ao Pandas, Numpy e bibliotecas gráficas - Exploração de Dados  (Sprint 1)

08h00 - 10h00  Autoestudo
  Bibliotecas gráficas: Matplotlib e Seaborn
  Como usar o Google COLAB para ANALISAR DADOS?
  Guia rápido de Pandas em Jupyter Notebook
  Introdução ao Numpy
  Introdução ao Pandas
  Visão geral de conceitos básicos de estatística descritiva

10h00 - 10h15  Daily e ativação
  Divide as cinco séries entre as duplas. Pergunta disparadora, sem revelar a resposta: qual das
  cinco séries é a mais longa? Cada dupla anota o palpite no notebook.

10h15 - 12h00  Instrução em metodologia ativa, em três blocos temáticos de 30 minutos (teoria,
  prática em duplas e correção rápida embutidas em cada bloco, para dar tempo real de depurar erro
  de sintaxe e de ambiente no Colab)

  10h15 - 10h45  Bloco 1, Pandas: carga, describe e validação de contrato

    10h15 - 10h27  Teoria: a transição de `csv.reader` (Aula 01) para `pandas.read_csv`.
      `DataFrame`, tipos de coluna, e as sete linhas do `describe()`.

    10h27 - 10h40  Prática em duplas: cada dupla carrega um dos cinco CSVs (`abate_bovinos`,
      `abate_suinos`, `abate_frangos`, `producao_ovos`, `producao_leite`), roda `describe()` e
      confere a faixa encontrada contra `dados/README.md`. Por que o `count` difere entre as
      séries?

    10h40 - 10h45  Correção rápida no quadro e dúvidas.

  10h45 - 11h15  Bloco 2, Numpy: vetorização e localização de picos

    10h45 - 10h57  Teoria: `np.diff`, o alinhamento de índices no fatiamento `valores[:-1]`, e
      por que vetorização em C bate laço `for` em Python puro.

    10h57 - 11h10  Prática em duplas: variação percentual trimestre a trimestre da própria série,
      `np.argmax(np.abs(...))` para achar o trimestre do maior salto.

    11h10 - 11h15  Correção rápida e dúvidas.

  11h15 - 11h45  Bloco 3, Visualização: tendência, sazonalidade e faltantes

    11h15 - 11h27  Teoria: `sns.lineplot` para a série no tempo, agregação por trimestre para
      expor sazonalidade, e como anotar o pico no gráfico. Nota de 2 min sobre dados faltantes:
      `isna()` checa, `fillna()` e `dropna()` agem.

    11h27 - 11h40  Prática em duplas: gráfico temporal, gráfico de sazonalidade, e anotação do
      maior pico encontrado no bloco 2.

    11h40 - 11h45  Correção rápida e dúvidas.

  11h45 - 12h00  Mapeamento cruzado e amarração com a sprint

    11h45 - 11h55  Cada dupla tem 1 minuto para dizer o comportamento da própria série. O
      professor monta no quadro o mapa comparativo das cinco (ex.: leite é sazonal, frango é
      quase linear, bovinos tem salto em 2005). É aqui que aparece o insight que nenhuma dupla
      via sozinha.

    11h55 - 12h00  Amarração: os gráficos e a leitura estatística de hoje alimentam a **ART.2
      UX parte 1** (peso 3), entregue em 14/08, e a **ART.1 Entendimento do negócio** (peso 6).

---

### Aula 04 - 19/08/2026 - Pré Processamento e Feature Engineering  (Sprint 2)

08h00 - 10h00  Autoestudo
  Adequação de variáveis numéricas e categóricas
  Diferenças entre Data Lakes e Data Warehouses
  Diferenças entre ETL e ELT
  Limpeza de dados com exemplos em Python (FreeCodeCamp)
  Ponderada 1 de Computação
  Pré-processamento de dados (conceito + prática)
  Seleção de característica

10h00 - 10h15  Daily da equipe
  O que fiz, o que vou fazer, impedimentos. Abertura da Sprint 2 (planning em 17/08): cada dupla
  relata em que ponto ficou a EDA da própria série.

10h15 - 12h00  Instrução em metodologia ativa, em três blocos temáticos (teoria, prática em
  duplas e correção rápida embutidas em cada bloco, no mesmo formato adotado na Aula 03), mais
  duas janelas no fim: oito minutos de revisão das Semanas 01 a 03 e onze minutos para as
  hipóteses da ART.5.

  Os três blocos foram comprimidos de 30 para 23, 28 e 25 minutos, para abrir duas janelas no
  fim: oito minutos de revisão das Semanas 01 a 03 e onze minutos para as hipóteses da ART.5. O
  corte sai da teoria de ETL e ELT (coberta por dois autoestudos desta semana), da teoria de
  defasagem e da teoria de escalonamento (que só passa a ser obrigatória na Aula 07, com KNN e
  SVM). As três práticas em duplas ficam intactas, com 13 minutos cada, porque são elas que
  produzem o que a dupla leva para a ART.3.

  10h15 - 10h22  Resgate e abertura

    A EDA da Aula 03 revelou sazonalidade e outliers nas cinco séries, e deixou registrada a
    escolha entre `fillna()` e `dropna()` como assunto de hoje. Pergunta disparada: "o que
    significa 'prever com defasagem' quando o dado é trimestral?"

  10h22 - 10h45  Bloco 1, Integração: as cinco séries viram uma base analítica

    10h22 - 10h27  Teoria (comprimida): ETL e ELT como enquadramento, e onde `dados/` (data lake)
      e a base analítica (data warehouse) se encaixam. A chave de junção é `periodo`, e a segunda
      fonte da junção é o próprio SIDRA: não existe série aberta do Sindirações em `dados/`, e a
      ADR-004 proíbe fabricar uma. Motivo completo em `docs/adrs/ADR-007`. O tratamento integral
      do tema fica na seção 1 do material de apoio.

    10h27 - 10h40  Prática em duplas: `pd.merge` unindo as cinco séries por trimestre, comparando
      `inner` (117 linhas) com `outer` (157 linhas, 40 ausentes em quatro colunas).

    10h40 - 10h45  Correção rápida: de onde vêm os 40 ausentes (`producao_ovos` começa em
      1987-T1, as outras quatro em 1997-T1) e o que cada opção de `fillna` afirmaria sobre o
      período sem medição.

  10h45 - 11h13  Bloco 2, Defasagem: o passado da série vira coluna

    10h45 - 10h55  Teoria: por que a proibição de modelos de série temporal do TAPI empurra o
      problema para regressão tabular. `shift(1)` e `shift(4)` como as duas defasagens do case, e
      a regra de nunca usar argumento negativo (vazamento temporal).

    10h55 - 11h08  Prática em duplas: criar `lag1` e `lag4` na série da dupla, contar os `NaN`
      gerados (1 e 4) e medir a correlação de cada defasagem com o valor corrente.

    11h08 - 11h13  Correção rápida: as duas defasagens lideram o ranking, e `producao_leite` é a
      única série em que `lag4` bate `lag1`. O desconforto a guardar: as outras quatro séries
      também correlacionam acima de +0,92.

  11h13 - 11h38  Bloco 3, Codificação e seleção

    11h13 - 11h20  Teoria: `trimestre` é categórica nominal, e as duas codificações possíveis
      (três dummies com `drop_first`, ou par seno/cosseno). Escala das variáveis numéricas e
      padronização z-score, citada aqui e retomada na Aula 07. Votação rápida: qual codificação a
      turma prefere testar primeiro, feita antes de mostrar os R² medidos.

    11h20 - 11h33  Prática em duplas: criar as dummies e o par seno/cosseno, padronizar as cinco
      colunas e medir a correlação da série da dupla com `abate_frangos` duas vezes, sobre o
      nível e sobre `.diff()`.

    11h33 - 11h38  Correção rápida: declarar a hipótese que a prática acabou de testar (H0: a
      correlação é zero) e ler o valor-p nos dois casos. Sobre o nível, p = 1,7e-64 para o leite e
      rejeita H0; sobre a primeira diferença, p = 0,667 e não rejeita. Mesma hipótese, mesma
      amostra, duas conclusões.

  11h38 - 11h46  Revisão das Semanas 01 a 03

    Bloco pedido pelo professor para preparar a turma para a **Ponderada 1 de Computação**, que
    consta dos autoestudos desta semana e é aplicada em sala. São quatro slides de revisão
    dirigida, um por tema: mutabilidade e cópia de lista em Python; dados estruturados,
    semiestruturados e não estruturados; as seis fases do CRISP-DM na ordem e os quatro
    paradigmas de aprendizado; e o conjunto mínimo de pandas (`read_csv`, `head`, `mean`,
    `median`, `describe`).

    O deck revisa os **temas**, com exemplos ancorados no case. Nenhum enunciado e nenhum
    gabarito da ponderada entra em artefato do acervo, porque o repositório inteiro é publicado
    no GitHub Pages. O arquivo da prova fica fora do git, junto com o `Turma.xlsx` e o TAPI.

  11h46 - 11h57  As hipóteses do dia, declaradas e decididas (ART.5)

    Este é o bloco que dá à ART.5 o formato que a entrega pede: hipótese escrita antes do
    resultado, teste compatível com o que se sabe dos dados, decisão, e efeito no projeto. Três
    hipóteses, todas sobre a base montada hoje:

    **H1. `abate_frangos` vem de uma distribuição normal.** O bloco abre pelo gráfico (histograma
    com a normal de mesma média sobreposta, e o quantil-quantil ao lado), que levanta a suspeita, e
    fecha no teste, que decide: Shapiro-Wilk, W = 0,9462, p = 0,00014, rejeita. As cinco séries rejeitam em nível; `abate_bovinos` deixa de rejeitar depois de
    `.diff()` (p = 0,217). Consequência: os testes seguintes usam Kruskal-Wallis no lugar da
    ANOVA, e a suposição de normalidade da regressão fica para os resíduos, na Aula 05.

    **H2. A correlação entre `producao_leite` e `abate_frangos` é zero.** Pearson devolve
    p = 1,7e-64 sobre o nível (rejeita) e p = 0,667 sobre a primeira diferença (não rejeita).
    Consequência: o leite fica fora das entradas do modelo de frango até que reduza o erro em
    dados que o modelo não viu.

    **H3. As médias dos quatro trimestres do leite são iguais.** Kruskal-Wallis sobre o nível dá
    p = 0,0739 e **não rejeita**; sobre o resíduo da tendência dá p = 1,6e-06 e rejeita. É o
    achado central do bloco: testar sazonalidade sem remover a tendência esconde o efeito sazonal
    mais forte da base, porque a variação entre anos infla a variação dentro dos grupos. O teste t
    pareado por ano (T4 contra T2) resolve o mesmo problema por construção: t = +16,18,
    p = 9,7e-16, efeito de +14,85% da média. Consequência: a codificação de sazonalidade entra na
    base do leite, com ganho de R² de 0,8896 para 0,9194.

    **Fecho do bloco, e a distinção que a turma leva para a ART.5:** o frango também rejeita o
    teste t pareado (t = +2,33, p = 0,027) e mesmo assim a feature fica de fora, porque o efeito é
    de +1,90% da média e o R² sobe 0,0004. Valor-p e tamanho de efeito respondem perguntas
    diferentes.

  11h57 - 12h00  Amarração com a sprint

    A base analítica de hoje alimenta a **ART.3 Exploração, Pré-processamento e Hipóteses**
    (peso 5) e a **ART.5 Distribuição normal e teste de hipótese** (peso 4). A Sprint 2 fecha em
    28/08.

---

### Aula 05 - 24/08/2026 - Aprendizado Supervisionado parte I  (Sprint 2)

08h00 - 10h00  Autoestudo
  Atividade ponderada - Competição de modelo preditivo (entrega na semana 9)
  Avaliação de modelos — Regressão (Scikit-learn)
  Exemplo de aplicação: Regressão Linear
  Exemplo prático de classificação com KNN (dois vídeos)
  Introdução a séries temporais
  Machine Learning, by Google
  Modelos não paramétricos e KNN (Russell & Norvig)
  Opcional: Classificação com k-vizinhos mais próximos (K-NN)
  Overfitting
  Primeiros passos com Scikit-Learn
  Reprodutibilidade e replicabilidade
  Separação de dados: treinamento e teste

10h00 - 10h15  Daily da equipe
  O que fiz, o que vou fazer, impedimentos. Cada dupla confirma que a base de frango com
  defasagem e sazonalidade da Aula 04 está pronta para treinar um modelo.

10h15 - 12h00  Instrução em metodologia ativa

  10h15 - 10h30  Resgate: a base com defasagem e sazonalidade construída na Aula 04. Hoje: o
    primeiro modelo supervisionado, uma regressão da produção de frango (Modelo 1 do TAPI).
    Pergunta disparada: "por que não podemos embaralhar os trimestres antes de separar treino e
    teste?"

  10h30 - 10h45  Teoria: regressão linear com scikit-learn (`LinearRegression`, `fit`,
    `predict`), aplicada à base de frango. Exercício imediato: cada dupla ajusta o primeiro
    modelo.

  10h45 - 11h00  Prática: separação treino/teste por corte de data, com os últimos 8 trimestres
    reservados como teste, nunca `train_test_split` aleatório. Discussão curta sobre por que
    embaralhar vazaria o futuro para o treino, ligando com o autoestudo "Introdução a séries
    temporais".

  11h00 - 11h15  Teoria: avaliação de modelos de regressão com scikit-learn, RMSE e MAPE
    (autoestudo "Avaliação de modelos — Regressão").

  11h15 - 11h30  Prática: cada dupla calcula RMSE e MAPE do próprio modelo e compara contra a
    baseline de coeficientes estáticos que a LDC usa hoje.

  11h30 - 11h45  Teoria: overfitting e reprodutibilidade (seed fixa, notebook versionado).
    Discussão dirigida: cada dupla aponta um sintoma de overfitting no próprio resultado, se
    houver.

    **Acréscimo de 24/08/2026, decidido pelo professor durante a construção da aula.** O bloco
    passou a incluir dois pontos que não estavam no roteiro original, e o motivo do primeiro foi
    uma pergunta trazida por um aluno:

    - **Intervalo de previsão numa série que cresce.** Um intervalo de ±1,96 desvio-padrão tem
      largura fixa em quilos, e a mesma banda vale ±17,02% em 1998 e ±4,01% em 2026. A alternativa
      medida é a banda empírica dos erros relativos, por horizonte, que cobriu 7 dos 8 trimestres
      reservados.
    - **Horizonte de previsão.** As métricas do bloco anterior são de um passo à frente, porque
      cada previsão usa o `frangos_lag1` real. Prevendo os oito de uma vez, de forma recursiva,
      que é o que o TAPI pede, o MAPE vai de 1,60% para 2,85%.

    O tempo saiu da teoria dos blocos 1 a 3, que ficaram mais enxutos. A ordem de corte ao vivo,
    se necessário, está em `docs/notas-do-professor/aula05.md`.

  11h45 - 12h00  Amarração com a sprint: o primeiro modelo de regressão e sua comparação com a
    baseline viram a segunda versão da comunicação visual do produto (histórico vs. previsão),
    alimentando **ART.4 UX parte 2** (peso 3). Fecha a Sprint 2 (review em 28/08).

---

### Aula 06 - 01/09/2026 - Aprendizado Não Supervisionado - parte I  (Sprint 3)

08h00 - 10h00  Autoestudo
  Determinando K: Elbow Plot
  Determinando K: Silhouette Analysis
  Introdução ao aprendizado não supervisionado (IBM)
  K-means
  Opcional: PCA

10h00 - 10h15  Daily da equipe
  O que fiz, o que vou fazer, impedimentos. Abertura da Sprint 3 (planning em 31/08).

10h15 - 12h00  Instrução em metodologia ativa

  10h15 - 10h30  Diagnóstico: seis perguntas de quiz sobre as Aulas 01 a 05, cada uma sobre uma
    decisão do case com número medido (granularidade, base analítica, corte treino/teste,
    comparação com a baseline, padronização).

  10h30 - 10h50  Revisão dirigida: o professor entra só nos módulos que o quiz reprovou. Cinco
    módulos disponíveis (Aula 01 a Aula 05), dois ou três visitados.

  10h50 - 11h05  Retomada com as mãos: cada dupla roda o notebook até reproduzir o MAPE de 1,60%
    da Aula 05.

  11h05 - 11h20  K-means, o conceito: agrupar sem rótulo, distância euclidiana, por que
    padronizar.

  11h20 - 11h40  Prática, ato 1 e ato 2: K=4 sobre os níveis das cinco séries, depois K=4 sobre a
    participação de cada trimestre no total do ano.

  11h40 - 11h50  Interpretação: os quatro perfis, o pico do leite deslocado, e a silhueta que
    piora no agrupamento melhor.

  11h50 - 12h00  Amarração com a sprint: o que a ART.6 pede, o que já existe e o que falta,
    alimentando **ART.6 Preparação dos Dados e Modelagem** (peso 6).

    **Redução de escopo decidida em 31/08/2026, registrada em `docs/adrs/ADR-009`.** O roteiro
    original tinha seis blocos de K-means, Elbow Plot e Silhouette Analysis, terminando em
    "interpretar os clusters e o que isso sugere sobre sazonalidade de dieta". A medição feita
    antes do primeiro slide mostrou que agrupar os níveis das cinco séries não revela perfis de
    dieta: revela épocas (concordância de 26,5% com o trimestre do calendário, o acaso de quatro
    grupos). K passou a ser fixo em 4, Elbow Plot e Silhouette Analysis migraram para a Aula 08, e
    metade do encontro (os três primeiros blocos) virou retomada diagnóstica das Aulas 01 a 05,
    por avaliação do professor sobre o nível da turma em mecânica de Python, conceitos de
    modelagem, densidade e amarração com a entrega.

---

### Aula 07 - 04/09/2026 - Aprendizado Supervisionado - parte II  (Sprint 3)

08h00 - 10h00  Autoestudo
  Matriz de confusão, precisão e revocação
  Naive Bayes
  Opcional: Feature Engineering - Notebook com respostas
  Opcional: Prática - Regressão Logística
  Opcional: Prática - SVM - Support Vector Machine
  Opcional: Random Forest - Exemplo prático
  Opcional: Árvore de Decisão com cálculo de Entropia passo a passo
  Random Forest
  Regressão Logística
  SVM - Support Vector Machine
  Árvore de Decisão e Entropia
  Árvore de Decisão na prática

10h00 - 10h15  Daily da equipe
  O que fiz, o que vou fazer, impedimentos. Cada dupla relata os perfis de cluster encontrados
  no agrupamento da Aula 06.

10h15 - 12h00  Instrução em metodologia ativa

  10h15 - 10h25  Resgate e H1: a turma abre o SIDRA e acha a classificação c12716, "Referência
    temporal", nas cinco tabelas do case. O filtro usado até a Aula 06 selecionava apenas a
    categoria "Total do trimestre" dessa classificação, o que produziu a leitura equivocada de
    que a fonte só publicava dado trimestral.

  10h25 - 10h40  Prática: cada dupla monta a base mensal (339 linhas, 1998-01 a 2026-03) e
    reconcilia a soma dos três meses com o valor trimestral já usado até a Aula 06.

  10h40 - 10h55  Teoria: árvore de decisão, como o algoritmo particiona o espaço de features e
    prevê a média dos valores da folha em que a observação cai.

  10h55 - 11h10  Prática, H2 e H3: cada dupla treina uma `DecisionTreeRegressor` (`max_depth=3`)
    sobre a base mensal, mede RMSE e MAPE contra a baseline da LDC e a regressão linear, e
    verifica com `arvore.predict(X_teste).max()` o teto da folha mais alta.

  11h10 - 11h22  Teoria: KNN, a pincelada. O algoritmo decide por semelhança entre os k vizinhos
    mais próximos, e a escala das features define o que conta como parecido.

  11h22 - 11h35  Prática, H4: cada dupla treina a árvore e o KNN com o alvo trocado para razão
    (`y / lag12`) e compara o MAPE com a versão em nível.

  11h35 - 11h45  Teoria: Random Forest, a média de várias árvores, e por que essa média reduz a
    variância em relação a uma árvore só.

  11h45 - 12h00  Amarração com a sprint: o quadro das quatro hipóteses (granularidade, disputa
    árvore contra reta, teto da árvore, recuperação em razão) e o modelo de fecho da aula, com
    RMSE e MAPE medidos contra a baseline da LDC, alimentam **ART.6 Preparação dos Dados e
    Modelagem** (peso 6).

    **Redução de escopo decidida em 03/09/2026, registrada em `docs/adrs/ADR-010`.** O roteiro
    original tinha um bloco de métricas de classificação (matriz de confusão, precisão,
    revocação) para um classificador auxiliar de "alta" ou "baixa" demanda, além de Naive Bayes,
    regressão logística, SVM e entropia calculada à mão no bloco de árvore. A medição feita antes
    do primeiro slide mostrou que a árvore de decisão perde da baseline da LDC em nível (MAPE
    7,66% contra 3,71%) e só volta à disputa com o alvo trocado para razão (MAPE 3,86%), o que
    abriu as quatro hipóteses da aula e não deixou tempo de sala para classificação. Esses
    assuntos migram para a Aula 09.

---

### Aula 08 - 10/09/2026 - Aprendizado Não Supervisionado Parte II  (Sprint 3)

08h00 - 10h00  Autoestudo
  Implementação: Sistemas de Recomendação I
  Kaggle: Sistemas de Recomendação II
  Ponderada 2 de Computação
  Sistemas de Recomendação
  Tipos de Sistemas de Recomendação

10h00 - 10h15  Daily da equipe
  O que fiz, o que vou fazer, impedimentos. Cada dupla relata o RMSE/MAPE do próprio Random
  Forest da Aula 07.

10h15 - 12h00  Instrução em metodologia ativa

  10h15 - 10h30  Resgate: os modelos de árvore e ensemble da Aula 07, já comparados com a
    baseline. Hoje: reduzir a dimensionalidade dos drivers macroeconômicos que alimentam o
    Modelo 2 e o Modelo 3. Pergunta disparada: "quantas variáveis macro vocês acham que
    realmente são independentes entre si?"

  10h30 - 10h45  Teoria: PCA, variância explicada, componentes principais.

  10h45 - 11h00  Prática: cada dupla roda PCA sobre as colunas de preço e disponibilidade dos
    macroingredientes (milho, farelo de soja, sorgo, trigo, DDGS) dos boletins do Sindirações.

  11h00 - 11h15  Teoria: como interpretar os dois primeiros componentes principais em termos dos
    ingredientes originais (loadings).

  11h15 - 11h30  Prática: cada dupla plota os trimestres no espaço dos dois primeiros
    componentes e aponta agrupamentos visíveis.

  11h30 - 11h45  Discussão dirigida: sistemas de recomendação como outra família de aprendizado
    não supervisionado, e por que o desdobramento de ração entre macroingredientes (Modelo 3) se
    parece com um problema de recomendação de mix. Cada dupla debate a analogia com a dupla
    vizinha.

  11h45 - 12h00  Amarração com a sprint: os componentes principais dos drivers macroeconômicos
    entram como features de menor dimensionalidade no Modelo 3, alimentando **ART.6 Preparação
    dos Dados e Modelagem** (peso 6). Fecha a Sprint 3 (review em 11/09).

    **Escopo ampliado em 31/08/2026, por causa da ADR-009.** Elbow Plot e Silhouette Analysis, que
    estavam roteirizados na Aula 06, migram para a Aula 08: a Aula 06 fixou K em 4 e usou a
    silhueta só como número lido em dois agrupamentos, sem ensinar o método de escolha de K. A
    Aula 08 herda o exemplo concreto da Aula 06, em que a silhueta piora (de 0,4795 para 0,2853)
    justamente no agrupamento que recupera o trimestre do calendário, e ensina Elbow Plot e
    Silhouette Analysis a partir desse contraste, antes do bloco de PCA. Isso soma dois assuntos
    novos ao escopo já previsto (PCA e sistemas de recomendação), e a Aula 08 vai precisar de um
    corte compensatório. O corte é decidido quando a aula for construída, não hoje.

---

### Aula 09 - 15/09/2026 - Problemas Comuns com Modelagem de IA e mais Feature Engineering  (Sprint 4)

08h00 - 10h00  Autoestudo
  Desbalanceamento das Classes
  Estudo de caso: Netflix (Learning a Personalized homepage)
  Formas de lidar com o desbalanceamento de Classes
  Maldição de dimensionalidade
  Modelagem do problema: Domain Knowledge
  Opcional: Estudo de caso - Airbnb
  PCA - Resolvendo o problema da dimensionalidade
  PCA: o que é e como usar em Python
  Tratando valores nulos com Imputer

10h00 - 10h15  Daily da equipe
  O que fiz, o que vou fazer, impedimentos. Abertura da Sprint 4 (planning em 14/09).

10h15 - 12h00  Instrução em metodologia ativa

  10h15 - 10h30  Resgate: o PCA da Aula 08 sobre os drivers macroeconômicos. Hoje: os erros
    silenciosos que estragam um modelo. Pergunta disparada: "o que aconteceria se separássemos
    treino e teste aleatoriamente numa série trimestral?"

  10h30 - 10h45  Teoria: vazamento temporal (temporal leakage), com demonstração ao vivo
    comparando `train_test_split` aleatório contra corte por data na base de frango, mostrando a
    queda artificial de RMSE no primeiro caso.

  10h45 - 11h00  Prática: cada dupla reproduz a demonstração na própria base e mede a diferença
    de RMSE entre os dois métodos de corte.

  11h00 - 11h15  Teoria: maldição de dimensionalidade e `Imputer` para os nulos que o IBGE marca
    quando suprime um dado, conforme o contrato descrito em `dados/README.md`.

  11h15 - 11h30  Prática: cada dupla aplica `SimpleImputer` nos vazios da própria série e discute
    se a estratégia de imputação escolhida é defensável para um dado trimestral.

  11h30 - 11h45  Teoria/discussão: domain knowledge na modelagem do problema, com os casos
    Netflix e Airbnb como referência de como conhecimento de negócio evita erros de modelagem.
    Exercício: cada dupla aponta um conhecimento de domínio da LDC que já mudou uma decisão de
    feature.

  11h45 - 12h00  Amarração com a sprint: o diagnóstico e a correção de vazamento temporal,
    dimensionalidade excessiva e nulos preparam os modelos para a comparação formal, alimentando
    **ART.7 Comparação de modelos** (peso 8).

    **Escopo ampliado em 03/09/2026, por causa da ADR-010.** Matriz de confusão, precisão,
    revocação, Naive Bayes, regressão logística, SVM e entropia calculada à mão, que estavam
    roteirizados na Aula 07, migram para a Aula 09: a Aula 07 mediu que a árvore de decisão só
    volta a competir com a baseline da LDC com o alvo trocado para razão, e as quatro hipóteses
    resultantes já preenchem o encontro, sem espaço de sala para um classificador auxiliar. Isso
    soma sete assuntos ao escopo já previsto (vazamento temporal, maldição de dimensionalidade,
    `Imputer` e domain knowledge), e a Aula 09 vai precisar de um corte compensatório. O corte é
    decidido quando a aula for construída, não hoje.

---

### Aula 10 - 17/09/2026 - Hiperparâmetros e Explicabilidade do Modelo  (Sprint 4)

08h00 - 10h00  Autoestudo
  Além da Transparência: Contextualizando a Necessidade de Explicabilidade na IA
  Como escolher um modelo preditivo
  Curva ROC e AUC
  Exemplo I: GridSearch e RandomSearch
  Exemplo II: GridSearch e RandomSearch
  Explicabilidade de Modelo com SHAP
  O que é hiperparâmetro?
  Opcional: Prática com GridSearch e RandomSearch
  Opcional: ROC e AUC na prática
  Validação Cruzada

10h00 - 10h15  Daily da equipe
  O que fiz, o que vou fazer, impedimentos. Cada dupla relata se encontrou vazamento temporal no
  próprio pipeline na Aula 09.

10h15 - 12h00  Instrução em metodologia ativa

  10h15 - 10h30  Resgate: os problemas de modelagem corrigidos na Aula 09. Hoje: ajustar os
    modelos e explicar suas decisões, requisito explícito do TAPI. Pergunta disparada: "o que é
    um hiperparâmetro, e em que ele difere de um parâmetro aprendido pelo modelo?"

  10h30 - 10h45  Teoria: GridSearch e RandomSearch para ajuste de hiperparâmetros do Random
    Forest treinado na Aula 07.

  10h45 - 11h00  Prática: cada dupla roda um GridSearch pequeno, com dois ou três
    hiperparâmetros, sobre o próprio modelo.

  11h00 - 11h15  Teoria: validação cruzada com corte temporal (`TimeSeriesSplit` do
    scikit-learn, mesmo sem usar um modelo de série temporal), retomando o cuidado da Aula 09.

  11h15 - 11h30  Prática: cada dupla aplica `TimeSeriesSplit` na validação do próprio GridSearch.

  11h30 - 11h45  Teoria: explicabilidade com SHAP e partial dependence plots, requisito
    explícito do parceiro. Exercício: cada dupla gera o gráfico SHAP do próprio modelo e
    identifica a feature mais influente.

  11h45 - 12h00  Amarração com a sprint: o modelo ajustado e explicado hoje é candidato direto na
    comparação de modelos, alimentando **ART.7 Comparação de modelos** (peso 8).

---

### Aula 11 - 24/09/2026 - AutoML - Pycaret  (Sprint 4)

08h00 - 10h00  Autoestudo
  O que é AutoML?
  O que é Pycaret?
  Prática: Pycaret para Classificação
  Prática: Pycaret para Classificação Multiclasse
  Prática: Pycaret para Regressão

10h00 - 10h15  Daily da equipe
  O que fiz, o que vou fazer, impedimentos. Cada dupla traz a feature mais influente encontrada
  via SHAP na Aula 10.

10h15 - 12h00  Instrução em metodologia ativa

  10h15 - 10h30  Resgate: o modelo ajustado e explicado da Aula 10. Hoje: comparar esse trabalho
    manual contra um comparador automático de candidatos. Pergunta disparada: "vocês acham que o
    AutoML vai bater o modelo que vocês ajustaram à mão?"

  10h30 - 10h45  Teoria: o que é AutoML e o que o PyCaret automatiza, comparando múltiplos
    algoritmos sob a mesma validação.

  10h45 - 11h00  Prática: cada dupla roda `setup()` e `compare_models()` do PyCaret sobre a base
    de frango (Modelo 1).

  11h00 - 11h15  Teoria: como o PyCaret reporta RMSE e MAPE por candidato, e como ler o ranking
    sem se enganar por overfitting.

  11h15 - 11h30  Prática: cada dupla repete `compare_models()` para uma segunda etapa do
    pipeline, Modelo 2 ou Modelo 3, conforme a escolha da dupla.

  11h30 - 11h45  Discussão dirigida: comparar o melhor candidato do PyCaret com o modelo ajustado
    manualmente na Aula 10. Votação: qual abordagem cada dupla vai levar adiante.

  11h45 - 12h00  Amarração com a sprint: a comparação sistemática de candidatos para os três
    modelos do case é a entrega central desta etapa, alimentando **ART.7 Comparação de modelos**
    (peso 8). Fecha a Sprint 4 (review em 25/09).

---

### Aula 12 - 29/09/2026 - Deploy de modelo e criação de pipeline de processamento  (Sprint 5)

08h00 - 10h00  Autoestudo
  Como Usar Pipelines no Scikit-Learn
  Como exportar um modelo preditivo
  MLflow: primeiros passos (rastreamento de experimentos)

10h00 - 10h15  Daily da equipe
  O que fiz, o que vou fazer, impedimentos. Abertura da Sprint 5 (planning em 28/09), última
  sprint do módulo.

10h15 - 12h00  Instrução em metodologia ativa

  10h15 - 10h30  Resgate: os candidatos comparados na Aula 11. Hoje: empacotar o vencedor para
    produção. Pergunta disparada: "o que precisa viajar junto com o modelo para ele funcionar
    fora do notebook?"

  10h30 - 10h45  Teoria: `Pipeline` do scikit-learn, encadeando pré-processamento (imputação,
    escala, defasagem) e o modelo escolhido num único objeto.

  10h45 - 11h00  Prática: cada dupla monta o `Pipeline` do próprio modelo vencedor da Aula 11.

  11h00 - 11h15  Teoria: exportação do modelo (`joblib`/`pickle`) e os riscos de divergência de
    versão de biblioteca entre treino e produção.

  11h15 - 11h30  Prática: cada dupla exporta o próprio `Pipeline` e recarrega numa célula nova
    para confirmar que o resultado é idêntico.

  11h30 - 11h45  Teoria: MLflow, rastreamento de experimentos, o que registrar (hiperparâmetros,
    métricas, versão dos dados). Exercício: cada dupla registra o próprio experimento no MLflow
    local.

  11h45 - 12h00  Amarração com a sprint: o `Pipeline` exportado e rastreado é o Modelo Final do
    case, alimentando **ART.8 Modelo Final** (peso 4).

---

### Aula 13 - 30/09/2026 - Deploy de modelos de Machine Learning  (Sprint 5)

08h00 - 10h00  Autoestudo
  How to Build a Machine Learning App using Streamlit
  Streamlit 101 - A faster way to build and share data apps

10h00 - 10h15  Daily da equipe
  O que fiz, o que vou fazer, impedimentos. Cada dupla confirma que o `Pipeline` exportado na
  Aula 12 recarrega sem erro.

10h15 - 12h00  Instrução em metodologia ativa

  10h15 - 10h30  Resgate: o `Pipeline` exportado e rastreado da Aula 12. Hoje: dar uma interface
    ao modelo. Pergunta disparada: "quem vai usar essa previsão na LDC, e o que essa pessoa
    precisa ver na tela?"

  10h30 - 10h45  Teoria: Streamlit, estrutura mínima de um app (`st.title`, `st.line_chart`,
    `st.selectbox`).

  10h45 - 11h00  Prática: cada dupla monta a primeira tela do app, carregando o `Pipeline` da
    Aula 12.

  11h00 - 11h15  Teoria: exibir histórico versus previsão de 8 trimestres no mesmo gráfico, com a
    categoria de proteína animal selecionável.

  11h15 - 11h30  Prática: cada dupla implementa o seletor de categoria e o gráfico de histórico
    versus previsão.

  11h30 - 11h45  Teoria: cenários (por exemplo, variar o preço do milho) como controles
    interativos que recalculam a previsão. Exercício: cada dupla adiciona um controle de cenário
    ao próprio app.

  11h45 - 12h00  Amarração com a sprint: o app com histórico, previsão e cenários é a peça
    central de comunicação da entrega final, alimentando **ART.9 Critérios de Publicação**
    (peso 3).

---

### Aula 14 - 06/10/2026 - Revisão e Futuro  (Sprint 5)

08h00 - 10h00  Autoestudo
  IA Generativa: técnicas, oportunidades e os desafios de autoria

10h00 - 10h15  Daily da equipe
  O que fiz, o que vou fazer, impedimentos. Última daily do módulo: cada dupla relata o que falta
  para a apresentação final.

10h15 - 12h00  Instrução em metodologia ativa

  10h15 - 10h30  Resgate: o app Streamlit da Aula 13. Hoje: revisar a cadeia completa dos três
    modelos e preparar a apresentação final. Pergunta disparada: "qual foi a decisão mais difícil
    do módulo, do CSV trimestral até o app?"

  10h30 - 10h45  Revisão guiada: reconstruir em conjunto, no quadro, a linha do tempo do case,
    do entendimento do negócio (Aula 02) até o deploy (Aulas 12 e 13). Exercício: cada dupla
    completa uma etapa da linha do tempo com o próprio resultado.

  10h45 - 11h00  Prática: ensaio cronometrado da apresentação final em duplas, com feedback
    cruzado entre duplas vizinhas.

  11h00 - 11h15  Discussão dirigida: o horizonte de 8 trimestres cobre os mesmos 24 meses
    pedidos pela LDC, mas não é o único jeito de negociar granularidade com um parceiro. Debate:
    o que mudaria se a LDC aceitasse esperar por uma série mensal futura do IBGE?

  11h15 - 11h30  Teoria: IA generativa, técnicas, oportunidades e desafios de autoria, como
    horizonte além deste módulo. Exercício: debate rápido sobre onde IA generativa poderia, ou
    não deveria, entrar no pipeline da LDC.

  11h30 - 11h45  Prática: revisão final dos critérios de publicação do app e do notebook antes da
    apresentação.

  11h45 - 12h00  Amarração com a sprint: o fechamento de hoje organiza a Apresentação final,
    alimentando **ART.10 Apresentação final** (peso 3), no encerramento da Sprint 5 e do módulo
    (07/10).

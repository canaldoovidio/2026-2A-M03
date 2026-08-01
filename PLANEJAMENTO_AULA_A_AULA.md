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

10h00 - 10h15  Daily da equipe
  O que fiz, o que vou fazer, impedimentos. Cada dupla escolhe qual das cinco séries vai explorar
  primeiro hoje.

10h15 - 12h00  Instrução em metodologia ativa

  10h15 - 10h30  Resgate: os três modelos mapeados e a decisão trimestral fechada na Aula 02.
    Hoje: explorar de fato as cinco séries com Pandas. Pergunta disparada: "qual das cinco
    categorias vocês acham que tem a série histórica mais longa?"

  10h30 - 10h45  Teoria: `pandas.read_csv`, `DataFrame`, tipos de coluna, `describe()`. Prática
    imediata: cada dupla carrega um dos cinco CSVs (`abate_bovinos`, `abate_suinos`,
    `abate_frangos`, `producao_ovos`, `producao_leite`) e roda `describe()`.

  10h45 - 11h00  Prática: estatística descritiva da série carregada (média, mediana, desvio
    padrão), comparando a ordem de grandeza encontrada com a checagem de sanidade documentada em
    `dados/README.md`.

  11h00 - 11h15  Teoria: Numpy para operações vetorizadas, calculando a variação percentual
    trimestre a trimestre com `np.diff`. Exercício: cada dupla calcula a variação da própria
    série e identifica o maior salto.

  11h15 - 11h30  Prática: Matplotlib e Seaborn, plotando a série no tempo com `periodo` no eixo
    x, procurando sazonalidade visual e outliers.

  11h30 - 11h45  Teoria: dados faltantes, quando o IBGE marca `valor` como ausente ou suprimido,
    e `isna()`. Exercício: cada dupla conta quantos vazios a própria série tem e onde eles caem.

  11h45 - 12h00  Amarração com a sprint: os gráficos e a leitura estatística produzidos hoje são
    a primeira versão da comunicação visual do produto de dados, alimentando **ART.2 UX parte 1**
    (peso 3). Fecha a Sprint 1 (review em 14/08).

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

10h15 - 12h00  Instrução em metodologia ativa

  10h15 - 10h30  Resgate: a EDA da Aula 03 revelou sazonalidade e outliers nas cinco séries. Hoje:
    transformar isso em features. Pergunta disparada: "o que significa 'prever com defasagem'
    quando o dado é trimestral?"

  10h30 - 10h45  Teoria: unir `abate_frangos.csv` (SIDRA) com os boletins do Sindirações pelo
    período, com ETL e ELT como enquadramento da união. Exercício: cada dupla identifica a chave
    de junção (`periodo`) e o tipo de junção necessário.

  10h45 - 11h00  Prática: `pd.merge` unindo as duas fontes num único `DataFrame` por trimestre.

  11h00 - 11h15  Teoria: features de defasagem (lag). Por que a proibição de modelos de séries
    temporais do TAPI empurra o problema para regressão tabular: colunas como `valor_t-1` e
    `valor_t-4` (mesmo trimestre do ano anterior) viram entradas do modelo.

  11h15 - 11h30  Prática: cada dupla cria as colunas de defasagem de 1 e de 4 trimestres na série
    de frango, usando `shift()`.

  11h30 - 11h45  Teoria: codificação de sazonalidade (dummy de trimestre ou seno/cosseno do
    trimestre do ano) e seleção de característica. Votação rápida: qual codificação a turma
    prefere testar primeiro.

  11h45 - 12h00  Amarração com a sprint: a base unificada, com defasagem e sazonalidade, alimenta
    **ART.3 Exploração, Pré-processamento e Hipóteses** (peso 5) e **ART.5 Distribuição normal e
    teste de hipótese** (peso 4), ao testar se as variáveis de entrada seguem distribuição normal
    antes da etapa de modelagem.

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

  10h15 - 10h30  Resgate: o modelo de regressão de frango e a comparação com a baseline da Aula
    05. Hoje: buscar padrões sem rótulo nos trimestres e nas dietas. Pergunta disparada: "quais
    meses vocês acham que se parecem entre si na demanda de ração?"

  10h30 - 10h45  Teoria: K-means, distância euclidiana entre observações padronizadas. Exercício:
    cada dupla padroniza as colunas de produção das cinco categorias antes de agrupar.

  10h45 - 11h00  Prática: cada dupla roda K-means sobre os trimestres, usando as colunas de
    produção das cinco categorias como features, agrupando "perfis de trimestre".

  11h00 - 11h15  Teoria: como escolher K, com Elbow Plot e Silhouette Analysis.

  11h15 - 11h30  Prática: cada dupla plota o próprio Elbow Plot e decide o valor de K a usar.

  11h30 - 11h45  Discussão dirigida: interpretar os clusters encontrados (por exemplo, trimestres
    de maior demanda de milho versus de farelo de soja) e o que isso sugere sobre sazonalidade de
    dieta.

  11h45 - 12h00  Amarração com a sprint: os perfis de dieta e de trimestre clusterizados hoje
    entram na preparação de dados do Modelo 2, alimentando **ART.6 Preparação dos Dados e
    Modelagem** (peso 6).

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
  O que fiz, o que vou fazer, impedimentos. Cada dupla relata o K escolhido na Aula 06 para os
  próprios clusters.

10h15 - 12h00  Instrução em metodologia ativa

  10h15 - 10h30  Resgate: os perfis de cluster da Aula 06. Hoje: modelos mais robustos que a
    regressão linear para o Modelo 1. Pergunta disparada: "o que uma árvore de decisão captura
    que uma reta não captura?"

  10h30 - 10h45  Teoria: árvore de decisão e entropia, aplicada à produção de frango com as
    features de defasagem da Aula 04.

  10h45 - 11h00  Prática: cada dupla treina uma `DecisionTreeRegressor` e compara RMSE e MAPE com
    a regressão linear da Aula 05.

  11h00 - 11h15  Teoria: ensembles e Random Forest, por que a média de várias árvores reduz
    variância em relação a uma árvore só.

  11h15 - 11h30  Prática: cada dupla treina um `RandomForestRegressor` sobre a mesma base e
    registra o ganho, ou a ausência de ganho, de RMSE e MAPE.

  11h30 - 11h45  Teoria: métricas de classificação (matriz de confusão, precisão, revocação),
    para o caso em que uma etapa auxiliar do pipeline classifica um trimestre como "alta" ou
    "baixa" demanda. Exercício: cada dupla monta a própria matriz de confusão de um classificador
    simples treinado sobre essa rotulagem.

  11h45 - 12h00  Amarração com a sprint: os modelos de árvore e ensemble, com RMSE e MAPE
    medidos contra a baseline da LDC, formam o núcleo do Modelo 1 e alimentam **ART.6 Preparação
    dos Dados e Modelagem** (peso 6).

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

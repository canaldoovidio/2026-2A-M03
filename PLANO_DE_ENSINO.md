# Plano de Ensino: Módulo 03 IN, Lógica para predição com inteligência artificial

Este documento e o `PLANEJAMENTO_AULA_A_AULA.md` são a fonte da verdade do acervo. Nenhum deck,
página de referências, material de apoio, notebook ou card do portal inventa data, título, escopo
ou peso de entrega: tudo desce destes dois arquivos, que por sua vez descem do `Turma.xlsx` (fonte
do cronograma e das ARTs, na Adalove) e do TAPI da Louis Dreyfus Company (fonte do escopo do case).

## 1. Identificação

| Campo | Valor |
|---|---|
| Módulo | 03 IN, Lógica para predição com inteligência artificial |
| Turma | GRAD IN03 · 2026-2A · T25 |
| Professor | Prof. Ovidio Lopes da Cruz Netto |
| Período | 03/08/2026 a 07/10/2026 |
| Duração | 10 semanas, 5 sprints, 14 Encontros de Instrução |
| Parceiro do case | Louis Dreyfus Company (LDC) |

## 2. O case: Louis Dreyfus Company

O módulo inteiro é ancorado em um projeto com parceiro real. O TAPI da LDC pede um modelo
preditivo de produção de proteína animal no Brasil, desdobrado em demanda de ração e depois em
macroingredientes, para apoiar decisões comerciais de originação de grãos.

**Três modelos encadeados**, conforme o TAPI:

1. projeção de produção de proteína animal por categoria (aves, suínos, bovinos, ovos, leite);
2. conversão dessa produção em demanda total de ração;
3. desdobramento da demanda de ração entre macroingredientes (milho, farelo de soja, sorgo,
   trigo, DDGS).

**Fontes de dados**, todas abertas e versionadas em `dados/` (ver `dados/README.md`):

- IBGE/SIDRA: tabela 1092 (abate de bovinos), 1093 (abate de suínos), 1094 (abate de frangos),
  7524 (produção de ovos), 1086 (produção de leite);
- Sindirações: boletins informativos do setor de rações, 2021 a 2025.

**Métricas.** RMSE e MAPE, comparados contra a abordagem de coeficientes estáticos que a LDC usa
hoje. **Explicabilidade** (SHAP e partial dependence plots) é requisito do parceiro, não enfeite.

**A restrição que organiza o módulo.** O TAPI proíbe explicitamente o uso de modelos de séries
temporais. As aulas 04 a 07 ensinam previsão de horizonte longo por regressão tabular com features
de defasagem, janelas móveis e codificação de sazonalidade, e a Aula 09 trata vazamento temporal
com validação por corte de data em vez de embaralhamento aleatório.

### 2.1 O ajuste de granularidade: de mensal para trimestral

O TAPI fala em "abate mensal" e pede "projeções mensais" com horizonte de 24 meses. Ao verificar
essa exigência contra a API do IBGE, na Fase 1 deste acervo, confirmou-se que as cinco tabelas do
SIDRA usadas no case pertencem à **Pesquisa Trimestral** de abate de animais e de produção de ovos
e leite: o dado publicado é trimestral (117 trimestres de 1997-T1 a 2026-T1, nas quatro séries mais
curtas), não existe versão mensal aberta, e os boletins do Sindirações são anuais. Interpolar um
trimestre em três meses inventaria uma observação que o IBGE nunca mediu, o que contaminaria
qualquer métrica de erro do próprio modelo preditivo.

Decisão do professor, tomada com esse fato confirmado: **o módulo trabalha em base trimestral, com
horizonte de previsão de 8 trimestres**, o que cobre os mesmos 24 meses pedidos pelo parceiro, na
granularidade que o dado realmente permite medir.

Esse descompasso entre o que o parceiro pediu e o que a fonte de dados aberta permite não é uma
nota de rodapé técnica: é conteúdo do módulo. A **Aula 02** (Visão Geral de ML, IA e Ciência de
Dados, com CRISP-DM) e a **ART.1 Entendimento do negócio** tratam essa diferença explicitamente.
Negociar granularidade com quem encomenda o modelo é trabalho real de ciência de dados, e é
exatamente o tipo de lacuna que a etapa de entendimento de negócio do CRISP-DM existe para
capturar antes que ela vire um modelo entregue no compasso errado.

## 3. Cronograma das 14 aulas

| # | Data | Sprint | Aula | Camada da espiral sobre o case |
|---|---|---|---|---|
| 01 | 04/08 | 1 | Introdução ao Python | ler o CSV do SIDRA de abate bovino; tipos, listas, dicionários |
| 02 | 07/08 | 1 | Visão Geral do Aprendizado de Máquina, Inteligência Artificial e Ciência de Dados | enquadrar os 3 modelos do TAPI; CRISP-DM sobre o problema da LDC |
| 03 | 11/08 | 1 | Introdução ao Pandas, Numpy e bibliotecas gráficas - Exploração de Dados | EDA das 5 séries de proteína animal |
| 04 | 19/08 | 2 | Pré Processamento e Feature Engineering | unir as cinco séries do SIDRA; defasagens e sazonalidade |
| 05 | 24/08 | 2 | Aprendizado Supervisionado parte I | regressão da produção de frango; corte temporal treino/teste |
| 06 | 01/09 | 3 | Aprendizado Não Supervisionado - parte I | clusterização de perfis de dieta e de meses |
| 07 | 04/09 | 3 | Aprendizado Supervisionado - parte II | árvores e ensembles no Modelo 1; RMSE e MAPE |
| 08 | 10/09 | 3 | Aprendizado Não Supervisionado Parte II | PCA nos drivers macroeconômicos |
| 09 | 15/09 | 4 | Problemas Comuns com Modelagem de IA e mais Feature Engineering | vazamento temporal, dimensionalidade, nulos do IBGE |
| 10 | 17/09 | 4 | Hiperparâmetros e Explicabilidade do Modelo | GridSearch, validação cruzada, SHAP, partial dependence |
| 11 | 24/09 | 4 | AutoML - Pycaret | comparar candidatos para os 3 modelos |
| 12 | 29/09 | 5 | Deploy de modelo e criação de pipeline de processamento | `Pipeline` do scikit-learn, export do modelo, MLflow |
| 13 | 30/09 | 5 | Deploy de modelos de Machine Learning | app Streamlit com histórico vs. forecast e cenários |
| 14 | 06/10 | 5 | Revisão e Futuro | fechamento do módulo e horizontes |

As 14 datas conferem, uma a uma, com os Encontros de Instrução do Prof. Ovidio registrados em
`docs/autoestudos-por-semana.md`.

## 4. Sprints e entregas

Os pesos abaixo são citados exatamente como registrados na Adalove (`Turma.xlsx`). Nenhum peso é
calculado ou inventado neste documento.

| Sprint | Planning | Review | Entregas com peso |
|---|---|---|---|
| 1 | 03/08 | 14/08 | ART.1 Entendimento do negócio (6) · ART.2 UX parte 1 (3) |
| 2 | 17/08 | 28/08 | ART.3 Exploração, Pré-processamento e Hipóteses (5) · ART.4 UX parte 2 (3) · ART.5 Distribuição normal e teste de hipótese (4) |
| 3 | 31/08 | 11/09 | ART.6 Preparação dos Dados e Modelagem (6) |
| 4 | 14/09 | 25/09 | ART.7 Comparação de modelos (8) |
| 5 | 28/09 | 07/10 | Prova 02/10 (20) · ART.8 Modelo Final (4) · ART.9 Critérios de Publicação (3) · ART.10 Apresentação final (3) |

## 5. Matriz de rastreabilidade

Para cada aula: os autoestudos da semana que ela pressupõe (título exato, extraído de
`docs/autoestudos-por-semana.md`) e a ART que ela alimenta. Quando uma semana tem dois Encontros de
Instrução, os autoestudos daquela semana estão divididos entre as duas aulas por afinidade de
tema; a lista completa da semana está em `docs/autoestudos-por-semana.md`.

| # | Aula | Semana | ART que alimenta |
|---|---|---|---|
| 01 | Introdução ao Python | Semana 01 | ART.1 Entendimento do negócio |
| 02 | Visão Geral do Aprendizado de Máquina, Inteligência Artificial e Ciência de Dados | Semana 01 | ART.1 Entendimento do negócio |
| 03 | Introdução ao Pandas, Numpy e bibliotecas gráficas - Exploração de Dados | Semana 02 | ART.2 UX parte 1 |
| 04 | Pré Processamento e Feature Engineering | Semana 03 | ART.3 Exploração, Pré-processamento e Hipóteses · ART.5 Distribuição normal e teste de hipótese |
| 05 | Aprendizado Supervisionado parte I | Semana 04 | ART.4 UX parte 2 |
| 06 | Aprendizado Não Supervisionado - parte I | Semana 05 | ART.6 Preparação dos Dados e Modelagem |
| 07 | Aprendizado Supervisionado - parte II | Semana 05 | ART.6 Preparação dos Dados e Modelagem |
| 08 | Aprendizado Não Supervisionado Parte II | Semana 06 | ART.6 Preparação dos Dados e Modelagem |
| 09 | Problemas Comuns com Modelagem de IA e mais Feature Engineering | Semana 07 | ART.7 Comparação de modelos |
| 10 | Hiperparâmetros e Explicabilidade do Modelo | Semana 07 | ART.7 Comparação de modelos |
| 11 | AutoML - Pycaret | Semana 08 | ART.7 Comparação de modelos |
| 12 | Deploy de modelo e criação de pipeline de processamento | Semana 09 | ART.8 Modelo Final |
| 13 | Deploy de modelos de Machine Learning | Semana 09 | ART.9 Critérios de Publicação |
| 14 | Revisão e Futuro | Semana 10 | ART.10 Apresentação final |

O roteiro minuto a minuto de cada autoestudo citado nesta matriz está em
`PLANEJAMENTO_AULA_A_AULA.md`, junto com o bloco `08h00 - 10h00 Autoestudo` de cada aula.

## 6. A espiral: o que cada aula deixa pronto para a próxima

O módulo é construído em aprendizagem espiral: toda aula começa resgatando o que a anterior deixou
pronto sobre o case da LDC, antes de avançar.

| # | Aula | O que a aula anterior deixou pronto |
|---|---|---|
| 01 | Introdução ao Python | Primeira aula do módulo: não há aula anterior a resgatar. |
| 02 | Visão Geral do Aprendizado de Máquina, Inteligência Artificial e Ciência de Dados | A Aula 01 deixou pronto a leitura do CSV de abate bovino do SIDRA em Python, com tipos, listas e dicionários prontos para enquadrar o problema da LDC. |
| 03 | Introdução ao Pandas, Numpy e bibliotecas gráficas - Exploração de Dados | A Aula 02 deixou pronto os três modelos do TAPI mapeados no CRISP-DM e a decisão de trabalhar em base trimestral, prontos para orientar a exploração das cinco séries. |
| 04 | Pré Processamento e Feature Engineering | A Aula 03 deixou pronto a EDA das cinco séries de proteína animal, com padrões, sazonalidade e problemas de qualidade já identificados. |
| 05 | Aprendizado Supervisionado parte I | A Aula 04 deixou pronto a base analítica com as cinco séries do SIDRA unidas por trimestre, com features de defasagem e de sazonalidade, pronta para alimentar o primeiro modelo. |
| 06 | Aprendizado Não Supervisionado - parte I | A Aula 05 deixou pronto o primeiro modelo de regressão da produção de frango, com corte temporal treino/teste validado. |
| 07 | Aprendizado Supervisionado - parte II | A Aula 06 deixou pronto os perfis de clusterização de dieta e de meses, que revelam agrupamentos a testar como features. |
| 08 | Aprendizado Não Supervisionado Parte II | A Aula 07 deixou pronto os modelos de árvore e ensemble do Modelo 1, com RMSE e MAPE medidos contra a baseline de coeficientes estáticos da LDC. |
| 09 | Problemas Comuns com Modelagem de IA e mais Feature Engineering | A Aula 08 deixou pronto os componentes principais dos drivers macroeconômicos via PCA, prontos para entrar como features de menor dimensionalidade. |
| 10 | Hiperparâmetros e Explicabilidade do Modelo | A Aula 09 deixou pronto o diagnóstico e a correção de vazamento temporal, dimensionalidade excessiva e nulos do IBGE. |
| 11 | AutoML - Pycaret | A Aula 10 deixou pronto os melhores hiperparâmetros e as explicações via SHAP e partial dependence dos modelos ajustados manualmente. |
| 12 | Deploy de modelo e criação de pipeline de processamento | A Aula 11 deixou pronto a comparação sistemática de candidatos via PyCaret para os três modelos do case, com o melhor candidato de cada etapa selecionado. |
| 13 | Deploy de modelos de Machine Learning | A Aula 12 deixou pronto o `Pipeline` do scikit-learn exportado e rastreado no MLflow. |
| 14 | Revisão e Futuro | A Aula 13 deixou pronto o app Streamlit funcionando com histórico e cenários, encerrando a cadeia de entregas técnicas. |

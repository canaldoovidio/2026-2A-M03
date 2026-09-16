# ADR-014: A Aula 11 usa o PyCaret 4.0.0a8, que roda no Python atual, e passa a ensinar que o AutoML varre a família de modelos e não conserta o protocolo

**Data:** 16/09/2026
**Status:** Aceita
**Decisores:** Prof. Ovidio Lopes da Cruz Netto e José Romualdo

## Contexto

A Aula 11, em 24/09/2026, fecha a Sprint 4 e tem o roteiro inteiro em cima do PyCaret: o
`PLANEJAMENTO_AULA_A_AULA.md` pede `setup()` e `compare_models()` sobre a base de frango, depois a
repetição para uma segunda etapa do pipeline, e a comparação do melhor candidato automático contra o
modelo que a dupla ajustou à mão na Aula 10.

Dois problemas apareceram na medição, antes de qualquer slide.

**A versão estável do PyCaret não roda no Python do acervo.** O `pycaret` 3.3.2, que é a última
versão estável e a que todos os cinco autoestudos da Semana 08 ensinam, **recusa Python 3.12 na
importação**, com `RuntimeError: Pycaret only supports python 3.9, 3.10, 3.11. Please DOWNGRADE your
Python version.`. Não é incompatibilidade de dependência que se resolva com pin: é uma checagem
explícita no `__init__.py` do pacote. Além disso, instalá-lo arrasta `scikit-learn` para 1.4.2,
`numpy` para 1.26.4 e `pandas` para 2.1.4, contra 1.9.1, 2.5.x e 3.0.5 do ambiente atual, o que
mudaria a versão sob a qual os outros dez notebooks do acervo são executados no CI.

A linha 4.0, ainda em alpha (`4.0.0a8`), importa e roda em 3.12 **sem mexer em nenhuma dessas três
versões**, e expõe `compare_models`, `tune_model`, `interpret_model`, `finalize_model` e
`predict_model`. O que ela não tem é a API funcional: `setup()` não existe mais, e o fluxo passa a
ser `RegressionExperiment(...).fit(X, y)` seguido de `compare_models()`. O próprio pacote declara o
motivo na mensagem de erro que devolve a qualquer argumento antigo: "The legacy escape hatch was
removed in phase 6."

**O roteiro pergunta se o AutoML bate o modelo ajustado à mão, e a resposta medida é maior que a
pergunta.** Com a base das Aulas 07 a 10 (339 linhas, 315 meses de treino, 24 de teste, onze
features), o quadro de referência é este:

| modelo | MAPE nos 24 meses de teste |
| --- | --- |
| regressão linear sobre o alvo em **nível** | **2,86%** |
| regressão linear sobre o alvo em razão, o fecho da Aula 07 | 3,32% |
| baseline de coeficiente fixo da LDC, `ADR-008` | 3,71% |
| floresta ajustada à mão na Aula 10 | 4,21% |

O `compare_models()` do PyCaret roda 22 candidatos em poucos segundos e coloca modelos lineares no
topo em todas as configurações testadas. Os quatro quadrantes de alvo por protocolo, todos medidos
nos mesmos 24 meses de teste:

| alvo | protocolo | meses de treino | MAPE estimado | MAPE de teste | diferença |
| --- | --- | --- | --- | --- | --- |
| nível | default | 220 | 3,63% | **2,81%** | 0,82 |
| nível | temporal | 311 | 3,35% | **2,84%** | 0,51 |
| razão | default | 220 | 3,73% | 3,26% | 0,47 |
| razão | temporal | 311 | 3,51% | 3,34% | 0,17 |

O campeão erra menos que qualquer número já publicado no acervo, e menos que os dois encontros de
ajuste manual das Aulas 07 e 10.

O ganho não vem de o AutoML achar um modelo exótico. Vem de ele varrer a **família** de modelos, e
com isso expor uma decisão que o acervo tomou uma vez e nunca reexaminou: o alvo em razão foi
escolhido na Aula 07 porque ele resolvia o teto da árvore de decisão, e ficou valendo para todos os
modelos seguintes. Para um modelo linear, ele custa 0,46 ponto percentual.

A Aula 11 alimenta a **ART.7 Comparação de modelos** (peso 8, `PLANO_DE_ENSINO.md` seção 4) e fecha
a Sprint 4, com review em 25/09.

## Decisão

A Aula 11 usa o `pycaret` 4.0.0a8, com a API de objeto, e declara em sala que ela difere da API dos
autoestudos. A tese da aula deixa de ser "o AutoML bate o modelo ajustado à mão?" e passa a ser
**o AutoML varre a família de modelos, e não conserta o protocolo**: ele encontrou em 4 segundos um
ganho que dois encontros de ajuste manual não encontraram, e ao mesmo tempo vem com dois vazamentos
temporais ligados por padrão, que a dupla precisa desligar por conta.

A divisão dos 105 minutos fica assim:

| Bloco | Minutos |
| --- | --- |
| Resgate das Aulas 07 a 10 e a pergunta disparada | 15 |
| O que o `compare_models()` faz em 4 segundos, e o que ele não decide | 15 |
| Prática: o leaderboard do Modelo 1 | 15 |
| Ler o leaderboard sem se enganar: o R2 que despenca e os dois defaults temporais | 15 |
| Prática: trocar o `fold_strategy` e comparar a estimativa com o teste | 15 |
| O que o AutoML achou que duas aulas não acharam | 15 |
| Amarração com a ART.7 e fecho da Sprint 4 | 15 |

## Motivações

- **Entre uma alpha que roda e uma estável que não importa, a alpha é a única opção real.** A
  alternativa seria pedir que cada dupla instalasse um Python 3.11 paralelo, no dia em que a Sprint 4
  fecha, e ainda assim o Colab, que é o ambiente de contingência do acervo desde a Aula 01, ficaria
  de fora. O custo da alpha é a diferença de API, que se resolve com uma tabela de conversão de
  três linhas e uma nota na página de referências.
- **A diferença de API é conteúdo, não obstáculo.** Os autoestudos ensinam `setup()`, e a aula usa
  `RegressionExperiment().fit()`. Dizer isso em voz alta, com o motivo, ensina algo que a ART.7 vai
  cobrar de qualquer forma: a versão da biblioteca faz parte da descrição do experimento, e um
  resultado sem versão declarada não é reproduzível.
- **O achado do alvo é o melhor conteúdo que esta aula podia ter.** A decisão de treinar sobre a
  razão foi correta na Aula 07, pelo motivo certo, e ficou errada quando a família de modelos mudou.
  Nenhuma dupla teria encontrado isso ajustando hiperparâmetros, porque hiperparâmetro não muda o
  alvo. É o argumento mais forte possível para gastar quatro segundos rodando um comparador antes de
  gastar trinta minutos ajustando um candidato.
- **Os dois defaults temporais do PyCaret fecham a espiral com a Aula 10.** O construtor traz
  `train_size=0.7`, que separa 95 dos 315 meses de treino por sorteio, e `fold_strategy="kfold"`,
  que é exatamente o validador que a Aula 10 mostrou pondo 252 meses de treino no futuro. A
  ferramenta que promete automatizar a comparação entrega, por padrão, os dois erros de protocolo
  que a aula anterior ensinou a reconhecer.
- **A estimativa do `TimeSeriesSplit` erra menos, e isso agora está medido dentro do PyCaret.** Com
  o fold default, o leaderboard estima 3,73% e o modelo erra 3,26% no teste, uma diferença de 0,47
  ponto; com `fold_strategy=TimeSeriesSplit(5)`, estima 3,51% contra 3,34% de teste, diferença de
  0,17. É a confirmação, dentro da ferramenta nova, do que a Aula 10 defendeu como regra de
  protocolo.

### Correção aplicada depois da revisão do `revisor-slides`

A primeira versão desta aula usava o campeão dos **defaults** (2,81%) como número de destaque, na
figura que o compara com os quatro modelos de referência do acervo. O revisor apontou, e a medição
confirmou, que aquele modelo treina com 220 dos 315 meses, sorteados, enquanto os quatro de
referência treinam com os 315 inteiros: o gráfico comparava família **e** volume de dado ao mesmo
tempo, e usava como troféu o produto do protocolo que a própria aula ensina a desconfiar.

O quadrante que faltava foi medido (nível com protocolo temporal, 311 meses de treino) e erra
**2,84%**. É esse o campeão da figura, e o 2,81% passou a aparecer só no bloco em que o protocolo é
o assunto. O achado vale como registro: a comparabilidade de volume de treino é tão parte do
protocolo quanto o corte por data, e nenhum validador do acervo a checa.

## Riscos conhecidos

- **`4.0.0a8` é uma versão alpha, e pode sair do ar ou mudar de API antes de 24/09.** Mitigação: a
  versão é fixada exatamente no `requirements-ci.txt`, contra a política do arquivo de não fixar
  versão, e o motivo fica escrito ao lado. O notebook instala a mesma versão exata. Se a alpha
  quebrar, o plano B é a aula rodar sobre o leaderboard já medido e versionado nas figuras, com a
  prática virando leitura dirigida.
- **A API da aula não é a API dos autoestudos.** Mitigação: `referencias/aula11.html` declara a
  diferença item por item, e o deck traz a tabela de conversão entre `setup()` e
  `RegressionExperiment().fit()` antes da primeira prática.
- **Dizer que o AutoML bateu duas aulas de trabalho manual pode ser lido como "não precisava ter
  feito as Aulas 07 a 10".** Mitigação: o bloco de fecho declara o contrário, com o argumento que a
  medição sustenta: sem o protocolo das Aulas 09 e 10, a dupla não teria como saber que 2,86% é um
  número honesto, e teria aceitado o 3,63% estimado pelo leaderboard com o fold errado. O AutoML
  ordena candidatos; ele não diz se a ordenação é confiável.
- **O ganho do alvo em nível depende das defasagens curtas.** `lag1`, `lag2` e `lag3` entram como
  features, e um modelo em nível se apoia mais nelas que um modelo em razão. Isso é premissa do
  acervo inteiro desde a Aula 07, não uma escolha desta aula, e continua valendo a ressalva de que a
  LDC precisa das defasagens disponíveis no momento da previsão.

## Consequências

Positivas:

- A ART.7 recebe o argumento que fecha o protocolo das quatro aulas da sprint: varrer a família
  antes de ajustar o candidato, e declarar versão, alvo e validador junto de cada número.
- A decisão de alvo da Aula 07, que estava implícita desde então, fica reexaminada e medida, e a
  Aula 12 recebe o modelo campeão real do acervo para empacotar no `Pipeline`.
- O acervo passa a ter uma dependência declaradamente experimental, com o motivo e o plano B
  escritos, em vez de uma dependência que simplesmente não roda.

Negativas:

- É a primeira vez que o acervo fixa a versão exata de um pacote no `requirements-ci.txt`, contra a
  política declarada no topo daquele arquivo, e a exceção precisa ser lida junto com a política.
- Os cinco autoestudos da Semana 08 descrevem uma API que a aula não usa. O descompasso é declarado,
  mas não desaparece, e é o segundo da sprint, depois do de curva ROC registrado na `ADR-013`.
- A aula termina com o melhor modelo do acervo sendo um que nenhuma aula construiu à mão, o que
  desloca o fecho da Sprint 4 do trabalho da dupla para o resultado de uma ferramenta. O bloco de
  fecho existe para não deixar essa leitura de pé.

## ADRs relacionadas

- `ADR-008`, que fixou o corte temporal e a baseline de coeficiente fixo usados como referência aqui.
- `ADR-010`, que estabeleceu a base mensal e escolheu o alvo em razão para resolver o teto da árvore
  de decisão na Aula 07. É a decisão que esta aula reexamina.
- `ADR-013`, que ajustou a floresta a 4,21% e fixou a validação temporal como regra de protocolo,
  que é o que a Aula 11 aplica dentro do PyCaret.

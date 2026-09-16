# ADR-013: A Aula 10 abre com curva ROC no lugar do resgate, ajusta a floresta sobre as onze features da Aula 09, e trata a vantagem do KFold no teste como ruído medido

**Data:** 16/09/2026
**Status:** Aceita
**Decisores:** Prof. Ovidio Lopes da Cruz Netto e José Romualdo

## Contexto

A Aula 10, em 17/09/2026, fecha a Semana 07 e chegou à construção com seis assuntos para 105
minutos. Quatro vinham do roteiro original em `PLANEJAMENTO_AULA_A_AULA.md` (GridSearch,
RandomSearch, validação cruzada com `TimeSeriesSplit`, e explicabilidade com SHAP e partial
dependence), e dois entraram pela `ADR-012`, que os moveu da Aula 09: curva ROC e AUC. O registro
daquela decisão já dizia que a dívida de tempo se deslocava em vez de desaparecer.

Três problemas apareceram na medição, antes de qualquer slide.

**O roteiro manda ajustar "o Random Forest treinado na Aula 07" sem dizer sobre qual conjunto de
features.** A Aula 07 treinou a floresta sobre quatro (`lag1`, `lag12`, `sen`, `cos`) e publicou
4,48% de MAPE de teste. A Aula 09 expandiu a base para onze features e nunca republicou a floresta
sobre elas. Medindo agora, a mesma floresta de 300 árvores com alvo em razão erra 5,04% com as onze
features, contra 4,48% com as quatro: **as sete features que a Aula 09 acrescentou pioram a
floresta que ninguém ajustou**, o que é a maldição de dimensionalidade que a própria Aula 09
ensinou, medida no modelo do case.

**O bloco de validação cruzada estava roteirizado para provar algo que o dado não prova.** A
expectativa natural é que trocar o `KFold(5)`, padrão do `GridSearchCV`, pelo `TimeSeriesSplit(5)`
melhore o resultado. Não melhora. Com as onze features, o `KFold` escolhe `max_depth=4`,
`min_samples_leaf=5` e `n_estimators=300`, que erra 4,13% no teste, e o `TimeSeriesSplit` escolhe a
mesma poda com 600 árvores, que erra 4,21%: o validador com vazamento termina 0,08 ponto percentual
à frente. Com as quatro features da Aula 07 o sinal se inverte, 3,99% contra 3,95%. A vantagem
troca de sinal conforme o conjunto de features, então ela é ruído, e um bloco que prometesse
"`TimeSeriesSplit` melhora o modelo" estaria ensinando a conclusão errada a partir de uma
coincidência de amostra.

O que o dado prova é outra coisa, e é maior. Na primeira dobra do `KFold(5)` sobre os 315 meses de
treino, **os 252 meses de treino são todos posteriores ao início da validação**, e quatro das cinco
dobras têm mês de treino no futuro (252, 189, 126, 63 e 0). No `TimeSeriesSplit(5)` esse número é
zero nas cinco dobras, e o treino cresce de 55 para 263 meses.

**O empate que a Aula 09 deixou tem uma leitura que a Aula 09 não pôde dar.** Naquela aula,
baseline majoritária, SVM RBF e árvore de entropia marcaram os quatro mesmos valores: 83,3% de
acurácia, 0,833 de precisão, 1,000 de revocação e 0,909 de F1. A AUC os separa: 0,500 na baseline,
0,500 na árvore e 0,738 no SVM RBF. E a ordem por acurácia não é a ordem por AUC: a regressão
logística tem a pior acurácia entre os que não desabam (79,2%) e a melhor AUC dos cinco (0,800).

A Aula 10 alimenta a **ART.7 Comparação de modelos** (peso 8, `PLANO_DE_ENSINO.md` seção 4), e fecha
a Semana 07.

## Decisão

A Aula 10 abre com curva ROC e AUC sobre o empate já medido da Aula 09, no lugar de um bloco de
resgate próprio; ajusta a floresta da Aula 07 sobre as onze features que a Aula 09 deixou, e não
sobre as quatro originais; e ensina `TimeSeriesSplit` como regra de protocolo, declarando em sala
que a vantagem do `KFold` no teste desta rodada é ruído medido, e não um resultado a ser escondido.

A divisão dos 105 minutos fica assim:

| Bloco | Minutos |
| --- | --- |
| Curva ROC e AUC sobre o empate da Aula 09, com a pergunta disparada | 15 |
| Hiperparâmetros, GridSearch e RandomSearch, com prática da dupla | 30 |
| Validação cruzada temporal com `TimeSeriesSplit`, com prática da dupla | 30 |
| Explicabilidade com SHAP e partial dependence, com prática da dupla | 20 |
| Amarração com a ART.7 | 10 |

## Motivações

- **ROC e AUC são o resgate da Aula 09, e não um assunto a mais.** O bloco de abertura de toda aula
  do acervo resgata o que a anterior deixou pronto. O que a Aula 09 deixou pronto é exatamente um
  empate de quatro métricas que ela não teve instrumento para desfazer. Usar os 15 minutos de
  abertura para desfazê-lo paga a dívida da `ADR-012` sem tirar tempo de nenhum dos quatro assuntos
  já roteirizados, e é o encaixe mais justo que a espiral permite.
- **A AUC 0,500 da árvore de entropia é o argumento, não a AUC 0,738 do SVM.** A árvore prevê a
  classe majoritária para os 24 meses de teste, e a curva ROC dela tem dois pontos: é a diagonal, a
  mesma da baseline. O SVM RBF decide igual no limiar padrão, mas ordena os meses corretamente, e
  isso aparece só na curva. A dupla sai sabendo que duas coisas com as mesmas quatro métricas podem
  ter valor de negócio diferente, que é o que a ART.7 cobra.
- **Ajustar sobre as onze features fecha a conta que a Aula 09 abriu.** Com a grade, o erro vai de
  5,04% para 4,21%, então o ajuste de hiperparâmetros recupera a maior parte do que as sete features
  extras custaram. Não recupera tudo: a floresta ajustada sobre as quatro features da Aula 07 erra
  3,95%. Declarar esses três números em sala é mais honesto, e mais útil para a ART.7, do que
  escolher a base que faz o ajuste parecer melhor.
- **O ganho vem de podar, e isso é verificável na grade inteira.** As 27 combinações mostram que
  `max_depth` e `min_samples_leaf` movem o erro, e `n_estimators` quase não move: as três
  combinações que só diferem no número de árvores ficam dentro de 0,2 ponto percentual. É o
  contraste que justifica gastar orçamento de busca em poda, não em tamanho.
- **O RandomSearch acha o mesmo com um terço do orçamento.** Nove sorteios das 27 combinações, com
  `TimeSeriesSplit`, chegam na mesma escolha da grade cheia: 45 treinos em vez de 135. É a
  justificativa prática do RandomSearch, medida no case, e não uma afirmação genérica sobre
  espaços grandes de busca.
- **O argumento de protocolo é mais forte que o argumento de resultado, e o acervo já tem
  precedente.** A `ADR-012` fixou a mesma forma de raciocínio: lá, a regressão linear sobre a razão
  não melhorava com o sorteio aleatório, e foi isso que tornou o corte por data uma regra válida
  antes de saber qual modelo venceria. Aqui, a vantagem do `KFold` troca de sinal com o conjunto de
  features, o que a torna ruído, e os 252 meses de treino no futuro da primeira dobra continuam
  sendo 252 em qualquer rodada.
- **SHAP entrega um achado que a importância por impureza não entrega.** As duas leituras concordam
  nas duas primeiras posições (`lag12` e `lag3`) e discordam da terceira em diante:
  `abate_bovinos_lag1` é a terceira por SHAP sobre os meses de teste e a sexta por impureza. O
  exercício do bloco, que é a dupla identificar a feature mais influente do próprio modelo, tem
  resposta diferente conforme o instrumento, e essa diferença é o conteúdo.

## Riscos conhecidos

- **Declarar em sala que o validador com vazamento ganhou pode ser lido como permissão para usá-lo.**
  Mitigação: a figura das dobras vem antes do número, e o bloco fecha com os 252 meses de treino no
  futuro, não com o MAPE. As notas do professor trazem a resposta pronta para a pergunta "então por
  que não usar o `KFold`?".
- **A grade de 27 combinações com `TimeSeriesSplit(5)` são 135 treinos, e a sala tem 15 minutos de
  prática.** Mitigação: a grade roda em 9 segundos com `n_jobs=-1` e em 19 segundos num único
  núcleo, medido na construção, porque a base tem só 315 linhas de treino. O notebook traz a grade
  já dimensionada, e a ordem de corte ao vivo está nas notas do professor.
- **O SHAP é a única dependência nova do acervo, e é pesada.** Mitigação: `shap` entra no
  `requirements-ci.txt` com o motivo ao lado, e a célula de importação do notebook instala o pacote
  com mensagem em português quando ele não estiver presente, como já se faz com o download dos CSVs.
- **O alvo binário volta à tela no bloco de abertura, e a dupla pode achar de novo que o case virou
  classificação.** Mitigação: o bloco repete a ressalva da `ADR-012`, que o alvo existe para ensinar
  métricas de classificação sobre dado real e que os três modelos do TAPI seguem sendo de regressão.

## Consequências

Positivas:

- A dívida da `ADR-012` fica quitada dentro da própria Semana 07, sem empurrar ROC e AUC para a
  Aula 11, que já tem PyCaret inteiro pela frente.
- A ART.7 recebe o que ela cobra para comparar modelos: uma métrica que separa modelos empatados,
  um protocolo de busca de hiperparâmetros com validação auditável, e duas leituras de importância
  de feature que discordam entre si.
- A Aula 11 herda o termo de comparação pronto: a floresta ajustada a 4,21% com `max_depth=4`,
  `min_samples_leaf=5` e `n_estimators=600` é o modelo manual contra o qual o PyCaret vai ser medido.

Negativas:

- A Aula 10 não tem um bloco de resgate separado, e é a primeira aula do acervo em que a retomada da
  aula anterior e o primeiro conteúdo novo ocupam o mesmo bloco. Quem comparar o roteiro dos decks
  vai encontrar uma anatomia diferente aqui.
- O número que a Aula 07 publicou (4,48%) e o que a Aula 10 usa como ponto de partida (5,04%) são a
  mesma floresta sobre bases diferentes, e isso precisa ser dito toda vez que os dois aparecerem
  juntos, sob pena de parecer erro de medição.
- A floresta ajustada sobre as onze features (4,21%) continua perdendo para a ajustada sobre as
  quatro (3,95%), então a aula termina sem o melhor modelo possível na mesa. A escolha de features
  não é assunto da Aula 10, e fica registrada aqui como gancho para a Aula 11.

## ADRs relacionadas

- `ADR-008`, que fixou o corte temporal e a baseline de coeficiente fixo usados como referência aqui.
- `ADR-010`, que estabeleceu a base mensal e deixou a floresta de 300 árvores da Aula 07 sobre
  quatro features.
- `ADR-012`, que deslocou curva ROC e AUC para esta aula e deixou os dois ganchos de
  `TimeSeriesSplit` (as janelas à mão da Aula 05 e o corte único por data da Aula 09).

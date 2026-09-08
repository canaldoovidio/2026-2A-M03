# ADR-012: A Aula 09 cria um alvo binário a partir das séries do SIDRA, mede o vazamento por MAPE em vez de RMSE, troca o exercício de imputação e reduz dimensionalidade e domain knowledge ao bloco de fecho

**Data:** 08/09/2026
**Status:** Aceita
**Decisores:** Prof. Ovidio Lopes da Cruz Netto e José Romualdo

## Contexto

A Aula 09, em 15/09/2026, chegou à construção com onze assuntos para 105 minutos. Quatro vinham do
roteiro original em `PLANEJAMENTO_AULA_A_AULA.md` (vazamento temporal, maldição de
dimensionalidade, `Imputer` para nulos e domain knowledge) e sete entraram pela `ADR-010`, que os
moveu da Aula 07: matriz de confusão, precisão, revocação, Naive Bayes, regressão logística, SVM e
entropia calculada à mão. O registro da ampliação já dizia que a aula precisaria de um corte
compensatório, deixando a decisão para o momento da construção.

Três problemas apareceram na medição, antes de qualquer slide.

**O roteiro promete uma demonstração que o dado sustenta pela metade.** O bloco de vazamento
temporal está escrito como "demonstração ao vivo comparando `train_test_split` aleatório contra
corte por data na base de frango, mostrando a queda artificial de RMSE no primeiro caso". O RMSE
cai mesmo, mas os dois números não são comparáveis: o alvo médio dos 24 meses sorteados fica entre
723 e 812 milhões de quilogramas, contra 1,182 bilhão nos 24 últimos meses, porque o sorteio pega
majoritariamente anos antigos, quando o abate era menor. Parte da queda de RMSE é escala do
período sorteado, não habilidade do modelo.

Medido pelo MAPE, que não depende de escala, o vazamento aparece e é grande, mas só nos modelos
que memorizam vizinho. Com o alvo em nível e as 11 features, o KNN com k=5 vai de 7,64% com corte
por data para 5,29% com sorteio, a árvore de profundidade 3 vai de 8,81% para 6,31% e a random
forest de 300 árvores vai de 5,70% para 4,04%. A regressão linear sobre a razão, que é o modelo do
fecho da Aula 07, não melhora: 3,32% com corte por data contra 3,60% com sorteio. O mecanismo está
contado mês a mês: no sorteio, todos os 24 meses de teste têm um mês vizinho no treino, contra 1
dos 24 no corte por data.

**O exercício de imputação não tem dado.** O roteiro pede que "cada dupla aplique `SimpleImputer`
nos vazios da própria série e discuta se a estratégia de imputação escolhida é defensável".
Nenhum dos dez CSVs versionados tem valor vazio. A ausência real do acervo é de período: a união
das cinco séries mensais tem 471 meses e a interseção 351, porque `producao_ovos` começa em 1987-01
e as outras quatro em 1997-01. A junção interna descarta 25,5% dos períodos, e 20,4% das 2.355
células da matriz período por série estão vazias.

**Os sete assuntos migrados são de classificação, e o case é de regressão.** Os três modelos
encadeados do TAPI preveem quantidade, não classe. Sem um alvo categórico ancorado no dado real,
matriz de confusão, precisão, revocação, Naive Bayes, regressão logística e SVM não têm sobre o que
rodar, e dado sintético é proibido.

Construindo o alvo binário mais direto que as séries permitem, "o abate do mês supera o mesmo mês
do ano anterior", o resultado é o conteúdo da aula. O treino tem 78,1% de positivos (246 de 315
meses) e o teste 83,3% (20 de 24). A baseline que prevê sempre a classe majoritária acerta 83,3%,
com revocação 1,000 e precisão 0,833, e **nenhum dos cinco classificadores supera essa acurácia**:
regressão logística 79,2%, SVM linear 83,3%, SVM RBF e árvore de entropia 83,3% prevendo quase
sempre a classe majoritária, e Naive Bayes gaussiano 16,7%, com precisão e revocação zero na classe
positiva.

A Aula 09 abre a Sprint 4 (planning em 14/09) e alimenta a **ART.7 Comparação de modelos** (peso 8,
`PLANO_DE_ENSINO.md` seção 4).

## Decisão

A Aula 09 cria o alvo binário "o abate do mês supera o mesmo mês do ano anterior" a partir das
séries do SIDRA e o usa nos sete assuntos de classificação; mede o vazamento temporal por MAPE, com
a ressalva de escala do RMSE declarada em sala; troca o exercício de `SimpleImputer` sobre vazios
inexistentes por um exercício de mascarar 5% dos meses de treino e medir cada estratégia contra a
verdade conhecida; e reduz maldição de dimensionalidade e domain knowledge de blocos próprios para
o bloco de fecho.

A divisão dos 105 minutos fica assim:

| Bloco | Minutos |
| --- | --- |
| Resgate do PCA da Aula 08 e pergunta disparada | 10 |
| Vazamento temporal, com prática da dupla | 25 |
| Classificação, matriz de confusão e desbalanceamento | 30 |
| Entropia passo a passo | 15 |
| Ausência e imputação, demonstração do professor | 10 |
| Dimensionalidade, domain knowledge e amarração com a ART.7 | 15 |

## Motivações

- **A ressalva de escala é o conteúdo, não uma nota de rodapé.** A aula é sobre erros silenciosos de
  modelagem, e comparar RMSE entre dois conjuntos de teste com médias que diferem em 35% é
  exatamente um desses erros. Ensinar a demonstração original sem a ressalva ensinaria a diagnosticar
  vazamento com um instrumento que também responde a outra coisa.
- **O vazamento medido por modelo impede a generalização errada.** Se a aula mostrasse só o KNN, a
  dupla sairia acreditando que sorteio sempre infla a métrica. A regressão linear sobre a razão
  piora com o sorteio, e isso torna a disciplina de corte por data uma regra de protocolo, válida
  antes de saber qual modelo vai ganhar.
- **Mascarar 5% e medir contra a verdade conhecida é mais forte que imputar sem gabarito.** O
  exercício devolve números: média erra 34,53%, mediana 34,38%, último valor 7,60%, interpolação
  linear 7,27% e o mesmo mês do ano anterior corrigido pelo fator médio erra 4,44%. A dupla vê que a
  estratégia que usa a estrutura sazonal já medida nas Aulas 04 a 08 é a que erra menos, e a
  ausência real da junção entra como enquadramento do case.
- **O alvo binário mantém os sete assuntos migrados ancorados em dado real e conversa com os
  autoestudos da semana.** "Desbalanceamento das Classes" e "Formas de lidar com o desbalanceamento
  de Classes" são autoestudos da Semana 07 (`docs/autoestudos-por-semana.md`), e o alvo do case é
  desbalanceado por natureza: o abate de frangos no Brasil cresceu em 78,1% dos meses medidos. O
  bloco não precisa de exemplo externo.
- **Nenhum classificador superar a baseline majoritária é o melhor argumento possível para matriz
  de confusão, precisão e revocação.** A acurácia de 83,3% do SVM parece boa até a matriz mostrar
  que ele prevê "cresce" quase sempre. É o mesmo padrão pedagógico das Aulas 05 a 08: a métrica
  que a técnica oferece por padrão não é a métrica que responde à pergunta do case.
- **Dimensionalidade cabe em uma tabela medida.** Indo de 2 para 11 features, a distância euclidiana
  média entre meses de treino cresce de 1,65 para 4,31, o KNN piora de 3,71% para 5,01% de MAPE e a
  regressão linear melhora de 4,71% para 3,32%. O ponto é o contraste, e ele não precisa de teoria
  nem de prática própria para ser lido.

## Riscos conhecidos

- **O alvo binário não é o alvo do TAPI, e a dupla pode achar que o case virou classificação.**
  Mitigação: o bloco declara que o alvo existe para ensinar as métricas de classificação sobre dado
  real, que os três modelos do TAPI seguem sendo de regressão, e que a entrega da ART.7 compara
  modelos de regressão.
- **A demonstração de imputação usa mascaramento sorteado, e o resultado depende da semente.**
  Mitigação: a semente é fixa em 42, o número mascarado é declarado (16 de 315 meses) e a suíte
  `tools/tests/test_problemas_aula09.py` trava a ordem das cinco estratégias, que é a conclusão, e
  não apenas cada valor.
- **Entropia à mão em 15 minutos é apertado.** Mitigação: a conta usa um único nó, a raiz, com
  0,7584 bits, e compara três cortes candidatos já medidos (`lag12` com ganho de 0,0632 bits, `dias`
  com 0,0082 e `sen` com 0,0043), mais o caso degenerado de `dias <= 31`, que deixa os 315 meses do
  mesmo lado. A árvore com critério de entropia escolhe o mesmo corte da conta à mão, o que fecha o
  bloco sem precisar percorrer a árvore inteira.
- **Domain knowledge fica com metade do tempo previsto e sem os dois estudos de caso em
  profundidade.** Netflix e Airbnb são autoestudos da Semana 07 e continuam citados, mas em sala
  entram como referência dentro do bloco de fecho.
- **Onze assuntos em cinco blocos de conteúdo mantém a aula densa.** Mitigação: a ordem de corte ao
  vivo fica nas notas do professor, e o bloco de ausência e imputação é o primeiro a encolher,
  porque é demonstração e não prática.

## Consequências

Positivas:

- A ART.7 recebe o protocolo de comparação que ela cobra: corte por data, métrica que não depende
  de escala e matriz de confusão quando o alvo for categórico.
- A aula corrige duas afirmações do próprio planejamento com medição, e as duas correções ficam
  registradas em teste, não só em prosa.
- A Aula 10 herda o gancho pronto para hiperparâmetros e validação cruzada: a repetição em janelas
  feita à mão na Aula 05 e o corte único por data desta aula viram `TimeSeriesSplit`.

Negativas:

- Curva ROC e AUC, que são autoestudos da Semana 07, não entram na Aula 09 e ficam para a Aula 10,
  que já tem GridSearch, validação cruzada, SHAP e partial dependence no escopo. A dívida de tempo
  se desloca em vez de desaparecer.
- O alvo binário é conteúdo criado para a aula, e não uma pergunta que a LDC fez. É a primeira vez
  no acervo que um alvo não vem do TAPI, e isso precisa ficar dito em sala.
- A citação do `SimpleImputer` sai do exercício da dupla e passa a aparecer só na demonstração do
  professor, então quem consultar o roteiro antigo vai encontrar outro exercício na tela.

## ADRs relacionadas

- `ADR-008`, que fixou o corte temporal e a baseline de coeficiente fixo usados como referência
  aqui.
- `ADR-010`, que moveu os sete assuntos de classificação da Aula 07 para esta aula e estabeleceu a
  base mensal.
- `ADR-011`, que mediu o efeito de ajustar escalador e PCA fora do treino e deixou o gancho do
  bloco de vazamento temporal.

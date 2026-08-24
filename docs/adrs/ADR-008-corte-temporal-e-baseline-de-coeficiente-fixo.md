# ADR-008: O protocolo de avaliação do Modelo 1, com corte temporal de oito trimestres, baseline de coeficiente fixo e repetição em doze janelas

**Data:** 24/08/2026
**Status:** Aceita
**Decisores:** Prof. Ovidio Lopes da Cruz Netto

## Contexto

A Aula 05 treina o primeiro modelo preditivo do case, a regressão de `abate_frangos` que é o
Modelo 1 do TAPI. Um modelo só significa alguma coisa depois de avaliado, e a forma de avaliar
precisa ser fixada uma vez, porque as Aulas 07 (árvores e ensembles), 10 (hiperparâmetros e
explicabilidade) e 11 (AutoML) comparam os resultados delas contra o número medido aqui. Uma
mudança silenciosa de protocolo entre aulas invalidaria essas comparações sem que ninguém
percebesse.

Três decisões precisavam ser tomadas juntas, porque cada uma condiciona a leitura das outras.

**Como separar treino de teste.** O autoestudo da Semana 04 apresenta `train_test_split`, cujo
padrão é `shuffle=True`. Aplicado a esta base, o sorteio coloca trimestres de 2026 no treino e
trimestres de 2019 no teste, o que mede a capacidade de interpolar dentro de um histórico
conhecido dos dois lados. A LDC precisa da outra medida: o erro ao projetar um trimestre que ainda
não aconteceu.

**Contra o que comparar.** O `PLANO_DE_ENSINO.md`, seção 4, define RMSE e MAPE comparados contra a
abordagem de coeficientes estáticos que a LDC usa hoje. Essa baseline precisava de uma definição
operacional, porque "coeficiente estático" descreve uma família de previsores, e não um previsor.

**Quantas medições fazer.** Medido uma vez, no corte mais recente, o modelo vence a baseline por
0,10 ponto percentual de MAPE (1,60% contra 1,69%). Oito trimestres são uma amostra pequena, e uma
diferença dessa ordem numa amostra dessas cabe dentro do que a escolha do corte explicaria
sozinha. Recomendar um modelo ao parceiro com base nessa única medida seria frágil.

## Decisão

O protocolo de avaliação do Modelo 1 tem três partes, e vale para todas as aulas que retomarem
este alvo:

1. **Corte temporal com os últimos 8 trimestres reservados**, por `iloc` sobre a base ordenada
   por `periodo`. Nenhuma função de sorteio participa da separação.
2. **Baseline de coeficiente fixo**: a previsão é o valor do mesmo trimestre do ano anterior
   multiplicado por um fator constante, estimado como a razão média entre valor corrente e
   `lag4` **no conjunto de treino apenas**.
3. **Repetição da medição em doze janelas consecutivas**, deslocando o corte um trimestre por
   vez. A recomendação ao parceiro se apoia no resultado agregado das doze, e não no da última.

## Motivações

- **O corte por data é o que corresponde ao uso real.** O TAPI pede projeção com horizonte de 24
  meses, e oito trimestres são exatamente esses dois anos. O conjunto de teste imita a situação de
  produção: tudo até 2024-T1 é conhecido, e o que vem depois precisa ser previsto.
- **A baseline precisa ser reproduzível em duas linhas de código.** A definição escolhida usa
  apenas colunas que a base analítica já tem (`frangos_lag4`), o que permite a qualquer dupla
  recalculá-la para a própria série sem material adicional do parceiro.
- **Estimar o fator só no treino é a mesma disciplina aplicada ao `StandardScaler`.** Calcular a
  razão média sobre a base inteira deixaria os oito trimestres reservados entrarem no cálculo,
  o que é vazamento, mesmo que discreto.
- **Doze janelas transformam um resultado apertado em um resultado defensável.** O modelo vence a
  baseline nas doze, com MAPE médio de 2,18% contra 3,14%, e margem que varia de 0,10 a 1,56 ponto
  percentual. É esse conjunto que sustenta uma recomendação, e é ele que as Aulas 07, 10 e 11
  precisam bater.

## Riscos conhecidos

- **Oito trimestres de teste continuam pouco, mesmo repetidos doze vezes.** As doze janelas se
  sobrepõem entre si, então as medidas não são independentes: elas reduzem o risco de conclusão
  por acaso de calendário, e não equivalem a doze amostras independentes. Mitigação: a Aula 09
  retoma o tema com validação por corte de data, e a Aula 10 introduz validação cruzada, onde o
  `TimeSeriesSplit` do scikit-learn formaliza esta mesma ideia.
- **A baseline escolhida é uma leitura nossa do que a LDC faz.** O TAPI descreve a abordagem de
  coeficientes estáticos sem publicar o coeficiente em uso. A definição operacional acima é
  adaptação nossa, declarada como tal no material de apoio, e não citação do parceiro. Mitigação:
  o número real, se o parceiro fornecer, entra no lugar do fator estimado sem mudar nada do
  protocolo.
- **Fixar o protocolo cedo pode engessar aulas posteriores.** Mitigação: o que está fixo é a forma
  de medir, e não o modelo. Qualquer estimador novo é avaliado sobre o mesmo corte e a mesma
  baseline, que é justamente o que torna as aulas comparáveis.

## Consequências

**Positivas.**

- As Aulas 07, 10 e 11 têm um número de referência para bater, medido sobre dados reais e com
  procedimento documentado.
- O vazamento temporal deixa de ser assunto abstrato: a Aula 05 mede o que acontece ao colocar o
  trimestre seguinte como entrada (o MAPE cai de 1,69% para 1,13%), e a Aula 09 retoma o mesmo
  exemplo.
- A ART.4 recebe uma figura de histórico contra previsão que já está ancorada no protocolo, sem
  precisar ser refeita quando o modelo mudar.

**Negativas.**

- O treino perde os oito trimestres mais recentes, que são também os de maior volume da série.
  O modelo entregue ao parceiro em produção precisaria ser reajustado sobre a base completa depois
  de a avaliação terminar, e essa etapa fica para a Aula 12, junto com o `Pipeline`.
- A repetição em doze janelas acrescenta uma seção ao notebook da Aula 05, que já é o mais longo
  do módulo até aqui.

## ADRs relacionadas

- `ADR-003-regressao-tabular-em-vez-de-series-temporais.md`: por que o case usa regressão tabular,
  o que torna a separação por data uma decisão de protocolo, e não uma consequência automática do
  método.
- `ADR-004-case-ancorado-em-fontes-abertas.md`: por que a baseline é reconstruída a partir das
  séries abertas, em vez de usar um coeficiente informado sem fonte verificável.
- `ADR-007-base-analitica-a-partir-das-cinco-series-do-sidra.md`: a base de 113 linhas sobre a qual
  este protocolo é aplicado.

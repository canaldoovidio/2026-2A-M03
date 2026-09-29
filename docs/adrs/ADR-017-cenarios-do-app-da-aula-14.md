# ADR-017: O cenário do app da Aula 14 é um choque percentual em grupos de entradas que o modelo lê, conferido nos dois ajustes do modelo

**Data:** 28/09/2026
**Status:** Aceita
**Decisores:** Prof. Ovidio Lopes da Cruz Netto e José Romualdo

## Contexto

O roteiro da Aula 14 (`PLANEJAMENTO_AULA_A_AULA.md`) pede "cenários como controles interativos que
recalculam a previsão", e cada dupla adiciona um controle de cenário ao próprio app. Não diz sobre
qual variável. O modelo que o app carrega é o `Pipeline` da Aula 12 (`ADR-015`): regressão linear
sobre o alvo em nível, com onze features (`lag1`, `lag2`, `lag3` e `lag12` do abate de frangos,
`sen`, `cos`, `dias`, e o mês anterior de bovinos, suínos, ovos e leite).

Três problemas apareceram antes de qualquer tela.

**O cenário que a LDC pediria primeiro não existe no modelo.** A pergunta natural de um trader de
grãos é "e se o milho subir 10%?". O modelo não tem preço entre as onze entradas. Um controle de
milho na tela mexeria num número que o `Pipeline` nunca lê, e a previsão não mudaria um
quilograma: um controle decorativo, que ensinaria ao usuário uma relação que o modelo não tem.

**Cenário é leitura de coeficiente, e a Aula 12 mediu que o coeficiente não é estável.** Reajustar
de 315 para 339 meses desloca os coeficientes numa mediana de 17,2% e faz o de
`abate_bovinos_lag1` trocar de sinal. Medido agora como cenário, com choque de +10% nos 24 meses de
teste:

| Choque de +10% em | Modelo exportado (339 meses) | Modelo avaliado (315 meses) |
|---|---|---|
| `lag1`, `lag2`, `lag3` e `lag12` juntos | +9,624% | +9,630% |
| bovinos, suínos, ovos e leite do mês anterior, juntos | +0,394% | +0,347% |
| só `lag1` | +0,241% | +0,453% |
| só `abate_bovinos_lag1` | +0,151% | -0,005% |

O choque no grupo de defasagens do frango é estável até a terceira casa, porque a soma dos
coeficientes de um grupo colinear é bem determinada mesmo quando a partilha entre eles não é. O
choque numa coluna isolada lê a partilha, que é justamente o que o reajuste move: `lag1` sozinho
quase dobra, e bovinos troca de sinal.

**As 24 previsões de teste são de um passo à frente.** Cada mês usa o `lag1` real. Um choque
aplicado a elas responde "quanto a previsão deste mês mudaria se a entrada tivesse sido X%
diferente", e não "o que aconteceria nos próximos 24 meses". Propagar o choque de forma recursiva
exigiria prever as outras quatro séries, e isso não existe no acervo.

## Decisão

O cenário do app é um choque percentual, de -20% a +20%, aplicado a um grupo de colunas que são
features do modelo, nos 24 meses de teste; o app oferece dois grupos (as quatro defasagens do
frango e as quatro outras séries do mês anterior) e um cenário de coluna isolada (bovinos),
recalcula o mesmo choque no modelo avaliado a cada movimento, e avisa quando os dois ajustes dão
efeito de sinal oposto. Cenário sobre variável fora das onze features é recusado com `ValueError`,
e o que faltaria para o milho entrar é declarado na tela.

## Motivações

- **Honestidade com o modelo.** Só entra controle que muda alguma coisa que o modelo lê.
  `aplicar_choque` recusa coluna fora de `FEATURES` em voz alta, e o teste confere que a recusa
  não é silenciosa.
- **O critério da ART.8 aplicado à tela.** A Aula 12 deixou para a ART.8 o critério de que a
  explicação publicada precisa ser tão estável quanto o número. Um cenário é uma explicação em
  forma de controle, então o mesmo critério vale para a ART.9, com uma medida concreta: mesmo
  sinal e mesma ordem de grandeza nos dois ajustes.
- **O cenário instável fica na tela de propósito.** Ele é o exemplo que ensina o critério. Tirar o
  cenário de bovinos deixaria a tela mais limpa e esconderia a razão de existir do aviso.
- **Custo zero de medição.** O modelo avaliado é reajustado a partir dos CSVs em milissegundos, e
  a comparação roda a cada movimento do controle sem cache.

## Riscos conhecidos

- **O choque no patamar do frango quase reproduz o próprio choque** (+10% vira +9,62%), e alguém
  pode ler isso como descoberta. É a soma dos coeficientes das defasagens (0,976 no exportado),
  próxima de 1 porque o abate de um mês é parecido com o dos anteriores. Mitigação: o material e as
  notas do professor dizem isso com essas palavras.
- **O cenário não é previsão causal.** Mitigação: a tela diz "análise de sensibilidade do modelo:
  ela não prevê o que aconteceria na economia", e o slide do bloco repete.
- **Duas duplas podem implementar cenários que não passam no critério e apresentá-los.** Mitigação:
  a função `estabilidade_do_cenario` está no módulo e o exercício das 11h00 manda usá-la.

## Consequências

- **Positivas:** o app tem um controle que muda a previsão de forma mensurável e defensável, o
  achado da Aula 12 ganha uso prático na Sprint 5, e o descompasso entre o que o parceiro
  perguntaria (milho) e o que o modelo sabe responder vira conteúdo, como o descompasso de
  granularidade virou na Aula 02.
- **Negativas:** o controle mais pedido pelo parceiro não existe na tela, e o app precisa explicar
  por quê. O app faz duas previsões a cada movimento, em vez de uma.

## ADRs relacionadas

- `ADR-015`: o `Pipeline` exportado, o achado do reajuste e o número de 2,86% que acompanha o app.
- `ADR-016`: a mudança do app Streamlit da Aula 13 para a Aula 14.
- `ADR-008`: o corte temporal que define os 24 meses de teste.

# Notas do professor: Aula 04

**19/08/2026 &middot; Pré-processamento e Feature Engineering &middot; Sprint 2**

Material de condução do encontro, não de distribuição ao aluno. Não é resumo do deck: são as
perguntas que abrem a sala quando ela travar, cada uma com a resposta esperada e o erro que a
pergunta costuma revelar.

Ordem igual à do roteiro em `PLANEJAMENTO_AULA_A_AULA.md`.

**Aviso de condução:** esta é a primeira aula da Sprint 2, aberta em 17/08. A turma sai daqui com a
base que a Aula 05 usa para treinar o primeiro modelo, então a prática de hoje precisa terminar
com a tabela montada em cada máquina. Se o tempo apertar, corte a discussão de ELT (slide 5) e
preserve as três práticas em duplas.

**Mudança em relação ao roteiro original:** o roteiro previa unir `abate_frangos.csv` com os
boletins do Sindirações. Não existe série aberta do Sindirações em `dados/`, e fabricar uma
violaria a ADR-004. A junção de hoje é entre as cinco séries do SIDRA, pela mesma chave `periodo`,
com o mesmo conteúdo de aprendizagem. Motivo completo em `docs/adrs/ADR-007`. Se algum aluno
perguntar pela ração, a resposta honesta é que o segundo e o terceiro modelos do TAPI continuam sem
fonte aberta, e que isso é o mesmo tipo de descompasso que a Aula 02 tratou com a granularidade.

---

## 10h00 - 10h15 &middot; Daily e abertura da Sprint 2

**Checkpoint de abertura:** cada dupla relata em que ponto ficou a EDA da própria série. Anote no
quadro quem terminou os três blocos da Aula 03 e quem parou antes: as duplas atrasadas precisam da
base `inner` pronta antes do Bloco 2 de hoje, senão perdem as duas práticas seguintes.

Confirme também quem já abriu a Ponderada 1 de Computação, que é da mesma semana e disputa o mesmo
tempo de estudo.

---

## 10h15 - 10h30 &middot; Resgate e abertura

**P1. O que significa "prever com defasagem" quando o dado é trimestral?**

Pergunta disparada do roteiro. Não responda: colete duas ou três formulações da turma e deixe em
aberto até o Bloco 2.

- *Resposta esperada real:* significa colocar o valor de trimestres anteriores como coluna da linha
  do trimestre corrente, porque o modelo é tabular e não enxerga a ordem das linhas. Com base
  trimestral, "um trimestre atrás" é `shift(1)` e "o mesmo trimestre do ano passado" é `shift(4)`.
- *O erro que revela:* a expectativa de que o modelo "aprenda a sequência sozinho". Um regressor
  tabular trata as 117 linhas como independentes; embaralhar as linhas não muda nada no resultado
  dele, e é isso que torna a defasagem obrigatória.

**P2. A Aula 03 terminou com `isna()` devolvendo zero. Por que ainda vamos falar de dados
ausentes hoje?**

- *Resposta esperada:* porque a junção de hoje cria ausentes que não existiam nos arquivos
  separados.
- *O erro que revela:* tratar qualidade de dado como propriedade fixa do arquivo. A mesma base
  passa em `isna()` antes da junção e reprova depois, sem que nenhum arquivo tenha mudado. A
  integração é um ponto de entrada de ausência tanto quanto a coleta.

---

## 10h15 - 10h45 &middot; Bloco 1, Integração

**P3. Qual é a chave de junção, e por que ela funciona?**

- *Resposta esperada:* `periodo`, porque está presente nos cinco arquivos, no mesmo formato de
  texto (`"1997-T1"`) e com o mesmo significado (o trimestre da medição).
- *O erro que revela:* propor juntar por índice de linha. Funcionaria por acidente nas quatro
  séries que começam em 1997 e produziria alinhamento errado com `producao_ovos`, que começa dez
  anos antes. Se alguém propuser isso, aceite e peça para conferir a linha 1: ovos de 1987
  apareceria ao lado de bovinos de 1997.

**P4 (durante a prática). Por que `outer` deu 157 linhas, se o maior arquivo tem 157?**

- *Resposta esperada:* porque `producao_ovos` cobre todo o período das outras quatro. A união dos
  cinco conjuntos de trimestres é exatamente o conjunto de trimestres de ovos.
- *O erro que revela:* esperar que `outer` sempre produza mais linhas que qualquer arquivo isolado.
  Ele produz a união, e aqui uma série contém as outras.

**P5 (na correção). `fillna(0)` resolveria os 40 ausentes?**

Pergunta para provocar. Alguém sempre propõe.

- *Resposta esperada:* resolveria o `NaN` e criaria uma afirmação falsa: que o Brasil abateu zero
  boi entre 1987 e 1996. O modelo aprenderia uma queda histórica que nunca existiu.
- *O erro que revela:* tratar `NaN` como problema de formato, quando ele é informação sobre o
  mundo. A pergunta certa antes de preencher é sempre "que afirmação eu estou fazendo sobre o
  valor que faltou?".

**Se a sala travar aqui:** peça para alguém rodar `base_outer.head(3)` e ler em voz alta o que a
linha de 1987-T1 diz sobre abate de bovinos. A resposta ("nada") costuma resolver a discussão
sozinha.

---

## 10h45 - 11h15 &middot; Bloco 2, Defasagem

**P6. Por que `shift(4)` e não `shift(12)`?**

- *Resposta esperada:* porque a base é trimestral, e quatro trimestres formam um ano. `shift(12)`
  olharia três anos para trás e custaria 12 das 117 linhas.
- *O erro que revela:* trazer o hábito de base mensal sem converter a unidade. É o mesmo cuidado de
  granularidade da Aula 02, aplicado agora à construção de feature.

**P7. Podemos usar `shift(-1)` para o modelo enxergar o próximo trimestre?**

Se ninguém perguntar, faça você. É o conceito mais caro do dia.

- *Resposta esperada:* não. `shift(-1)` traz o futuro para a linha de hoje. O modelo treinado assim
  acerta em validação (recebeu a resposta como entrada) e falha em produção, porque no momento da
  previsão o próximo trimestre ainda não aconteceu.
- *O erro que revela:* confundir métrica alta com modelo bom. Vale insistir num ponto: nenhum aviso
  é emitido. O código roda, o R² sobe, e o problema só aparece em operação.

**P8 (na correção). Por que leite é a única série em que `lag4` ganha de `lag1`?**

- *Resposta esperada:* porque é a série mais sazonal das cinco (14,85 pontos percentuais de
  amplitude entre o trimestre mais alto e o mais baixo, contra 2,55 do frango). Quando a estação do
  ano domina, o trimestre mais parecido é o mesmo do ano anterior.
- *O erro que revela:* tratar defasagem como escolha genérica de hiperparâmetro. A defasagem que
  funciona depende do comportamento da série, e a Aula 03 já tinha mostrado esse comportamento no
  mapa cruzado.

---

## 11h15 - 11h45 &middot; Bloco 3, Codificação e seleção

**P9. Por que descartar uma das quatro dummies?**

- *Resposta esperada:* porque a soma das quatro é sempre 1, então a quarta é combinação linear das
  outras três e a matriz perde posto. Em regressão linear os coeficientes ficam indeterminados. A
  categoria descartada vira a referência de comparação.
- *O erro que revela:* achar que `drop_first=True` economiza memória. A razão é algébrica.

**Votação prevista no roteiro (dummies ou seno/cosseno).** Faça a votação **antes** de mostrar os
R². Depois mostre os números do leite (0,8896 para 0,9194 e 0,9193) e pergunte se alguém mudaria o
voto. A resposta técnica é que com quatro trimestres as duas empatam, e a vantagem do seno/cosseno
só aparece com ciclos longos (12 meses, 52 semanas).

**P10 (na correção, a pergunta central do dia). A correlação entre leite e frango é +0,96 em nível
e -0,04 em primeira diferença. Qual das duas está certa?**

- *Resposta esperada:* as duas. Elas respondem perguntas diferentes. O +0,96 mede que as duas
  séries subiram ao longo de 29 anos. O -0,04 mede que a variação de um trimestre para o outro em
  uma delas não informa nada sobre a da outra. Para selecionar característica de um modelo
  preditivo, a segunda é a pergunta relevante.
- *O erro que revela:* ranquear variável por correlação com o alvo e cortar as mais fracas. Nesta
  base, esse procedimento selecionaria a tendência cinco vezes seguidas e chamaria isso de cinco
  preditoras.

**Se sobrar tempo:** pergunte o que aconteceria se uma sexta série, completamente sem relação com
proteína animal (o PIB, por exemplo), fosse adicionada à base. Resposta: correlacionaria alto em
nível pelo mesmo motivo.

---

## 11h45 - 12h00 &middot; ART.5 e amarração com a sprint

**P11. As cinco séries rejeitam normalidade. Isso invalida a regressão da Aula 05?**

- *Resposta esperada:* não. Mínimos quadrados não exige entradas normais. A suposição de
  normalidade em regressão linear é sobre os **resíduos** do modelo ajustado, e serve para os
  testes de significância dos coeficientes e para os intervalos de confiança. O teste de hoje é
  sobre as variáveis, e é o que a ART.5 pede.
- *O erro que revela:* a regra decorada de que "os dados precisam ser normais para usar regressão".
  Vale nomear onde a suposição realmente mora, porque essa confusão volta na Aula 05.

**Fechamento (11h55 - 12h00).** Peso citado da fonte oficial (`PLANO_DE_ENSINO.md`, seção 4):
**ART.3 Exploração, Pré-processamento e Hipóteses, peso 5**, e **ART.5 Distribuição normal e teste
de hipótese, peso 4**. A Sprint 2 fecha em **28/08**. Deixe explícito o que cada dupla leva pronto:
base larga, defasagens, sazonalidade codificada, colunas padronizadas e o valor-p do teste de
normalidade da própria série.

---

## Checklist de material antes do encontro

- [ ] `notebooks/aula04.ipynb` aberto e executado uma vez, do início ao fim, na máquina do
      professor (a execução leva menos de um minuto e não depende de rede).
- [ ] Os cinco CSVs presentes em `dados/`, para quem estiver com o repositório clonado.
- [ ] O quadro dividido em cinco colunas, uma por série, para a comparação do Bloco 2.
- [ ] O PDF do deck **não** distribuído antes da aula: o botão de exportação revela o gabarito do
      quiz, conforme documentado em `inteli-deck-design` seção 8.6.

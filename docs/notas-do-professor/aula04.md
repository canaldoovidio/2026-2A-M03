# Notas do professor: Aula 04

**19/08/2026 &middot; Pré-processamento e Feature Engineering &middot; Sprint 2**

Material de condução do encontro, não de distribuição ao aluno. Não é resumo do deck: são as
perguntas que abrem a sala quando ela travar, cada uma com a resposta esperada e o erro que a
pergunta costuma revelar.

Ordem igual à do roteiro em `PLANEJAMENTO_AULA_A_AULA.md`.

**Aviso de condução:** esta é a primeira aula da Sprint 2, aberta em 17/08. A turma sai daqui com a
base que a Aula 05 usa para treinar o primeiro modelo, então a prática de hoje precisa terminar
com a tabela montada em cada máquina.

**Os três blocos já vêm comprimidos** (23, 28 e 25 minutos, contra os 30 originais) para abrir as
duas janelas do fim: oito minutos de revisão das Semanas 01 a 03 e onze minutos para as hipóteses
da ART.5. O corte saiu da teoria, e as três práticas em duplas seguem com 13 minutos cada. Se o
tempo apertar mesmo assim, o próximo corte é a teoria de escalonamento (slide 16), que só passa a
ser obrigatória na Aula 07.

**Onde está o peso desta aula:** o bloco de 11h46 é o que dá à ART.5 o formato que a entrega pede.
Três hipóteses declaradas, testadas e levadas até a consequência no projeto. Se algum bloco tiver
de encolher ao vivo, que não seja esse.

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

## 10h15 - 10h22 &middot; Resgate e abertura

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

## 10h22 - 10h45 &middot; Bloco 1, Integração

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

## 10h45 - 11h13 &middot; Bloco 2, Defasagem

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

## 11h13 - 11h38 &middot; Bloco 3, Codificação e seleção

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

## 11h38 - 11h46 &middot; Revisão das Semanas 01 a 03

Bloco de preparação para a **Ponderada 1 de Computação**, aplicada em sala. São quatro slides, um
por tema, e o tempo é curto: cerca de dois minutos e meio cada. Conduza como revisão dirigida, com
a turma respondendo, e não como exposição.

**Regra que vale para este bloco inteiro:** o deck revisa os temas com exemplos do case, e nenhum
enunciado ou gabarito da prova aparece em artefato do acervo, porque tudo aqui é publicado no
GitHub Pages. O arquivo da ponderada fica fora do git, junto com o `Turma.xlsx` e o TAPI. Se for
resolver alguma questão específica com a turma, faça no quadro.

**P11 (slide 21). A mesma coisa acontece com `numero_b = numero_a`, sendo `numero_a` um inteiro?**

Pergunta que o slide deixa em aberto. É a que separa quem decorou de quem entendeu.

- *Resposta esperada:* o comportamento observável é diferente, porque inteiro é imutável. Somar 1 a
  `numero_a` cria um objeto novo e reaponta o nome, sem afetar `numero_b`. Com lista, `append`
  altera o objeto que os dois nomes compartilham.
- *O erro que revela:* achar que a diferença está no `=`. A atribuição faz a mesma coisa nos dois
  casos (liga um nome a um objeto); o que muda é a mutabilidade do tipo.

**P12 (slide 22). Um e-mail é dado estruturado, porque tem remetente e data?**

- *Resposta esperada:* um e-mail reúne cabeçalho com campos fixos e corpo em texto livre, o que o
  coloca no caso clássico de semiestruturado. Classificá-lo pelo cabeçalho ignora onde está a maior
  parte do conteúdo.
- *O erro que revela:* classificar o arquivo pelo campo mais fácil de ver.

**P13 (slide 22). Uma coluna de texto é dado não estruturado?**

- *Resposta esperada:* não necessariamente. A coluna `unidade` dos CSVs do case é texto, é
  qualitativa, e está dentro de uma tabela com esquema fixo, portanto é estruturada. Formato e
  natureza do valor são classificações independentes.
- *O erro que revela:* colar "texto" em "não estruturado" e "número" em "estruturado".

**P14 (slide 24). Por que `periodo` fica de fora do `describe()`?**

- *Resposta esperada:* porque `describe()` resume, por padrão, apenas colunas numéricas, e
  `periodo` chega como `object` (texto). Média de `"1997-T1"` não existe.
- *O erro que revela:* supor que `describe()` descreve o `DataFrame` inteiro. Vale citar que
  `describe(include="all")` traz as colunas de texto, com outras estatísticas (contagem, valores
  únicos, mais frequente).

---

## 11h46 - 11h57 &middot; As hipóteses do dia, declaradas e decididas (ART.5)

O bloco mais denso do encontro, e o que a ART.5 cobra diretamente. A sequência é sempre a mesma,
três vezes: escrever a hipótese, escolher o teste, ler a decisão, dizer o que muda no projeto.
Conduza pelo quadro do slide 25 e feche pelo slide 26, que é a coluna de consequência.

**Conduza o bloco começando pelo slide 25**, que traz o histograma e o gráfico quantil-quantil de
`abate_frangos`. Pergunte à turma o que os dois painéis sugerem antes de mostrar o valor-p: a
leitura visual levanta a suspeita, e o número no slide seguinte é o que fecha a decisão. Serve
também para nomear o limite da inspeção visual, que na Aula 03 foi o único instrumento disponível.

**P15. Por que H3 usa Kruskal-Wallis, e não ANOVA?**

- *Resposta esperada:* porque H1 foi rejeitada logo antes. A ANOVA supõe normalidade dentro dos
  grupos, e a série não é normal. Kruskal-Wallis compara os grupos sem essa exigência.
- *O erro que revela:* escolher o teste pelo que se lembra da aula de estatística, sem checar se as
  suposições dele valem para o dado em mãos. A ordem H1 antes de H3 no slide não é decorativa: é a
  dependência entre as duas decisões.

**P16 (a pergunta central do bloco). O teste diz que o leite não tem sazonalidade (p = 0,0739).
A Aula 03 mostrou o gráfico com T2 baixo e T4 alto. Quem está errado?**

- *Resposta esperada:* nenhum dos dois. O teste está certo sobre a pergunta que respondeu, e a
  pergunta estava mal formulada. Kruskal-Wallis compara a variação entre os quatro grupos com a
  variação dentro de cada grupo; com 29 anos de crescimento, dois T2 distantes no tempo diferem
  muito mais entre si do que um T2 difere do T4 do mesmo ano. A tendência infla a variação dentro
  dos grupos e afoga o efeito sazonal.
- *A demonstração:* refeito o mesmo teste sobre o resíduo da tendência, p cai para 1,6e-06. Refeito
  como teste t pareado por ano, t = +16,18 e p = 9,7e-16.
- *O erro que revela:* aceitar "não rejeitamos H0" como "não existe efeito". Um valor-p alto pode
  significar ausência de efeito, amostra pequena, ou teste inadequado para a estrutura do dado.
  Aqui é o terceiro caso, e é o mais difícil de perceber sozinho.

**P17. Por que o pareamento por ano resolve o problema sem ajustar reta nenhuma?**

- *Resposta esperada:* porque cada par carrega o nível daquele ano nos dois lados. Ao subtrair
  T2 de T4 do mesmo ano, o nível se cancela, e sobra a diferença sazonal. O controle da tendência
  vem do desenho do teste, sem passar por modelagem.
- *O erro que revela:* achar que teste pareado serve só para "antes e depois" de intervenção.

**P18 (fecho). O frango também rejeita o teste t pareado, com p = 0,027. Por que a feature de
sazonalidade dele fica de fora?**

- *Resposta esperada:* porque o efeito é de +1,90% da média, contra +14,85% do leite, e o R² do
  frango sobe 0,0004 com as dummies, contra 0,0298 do leite. O valor-p responde apenas se o
  efeito provavelmente existe. O tamanho dele, que é o critério de inclusão, sai de outra conta.
- *O erro que revela:* usar p < 0,05 como critério único de inclusão de variável. É o erro que a
  ART.7 (comparação de modelos) vai cobrar de novo, com outro nome.

**Se sobrar tempo:** pergunte quantos testes foram feitos hoje somando tudo (cinco séries vezes
quatro hipóteses) e o que acontece com a chance de um falso positivo quando se testa muita coisa a
5%. Não precisa fechar em Bonferroni; basta a turma perceber o problema.

---

## 11h57 - 12h00 &middot; Amarração com a sprint

**Fechamento.** Peso citado da fonte oficial (`PLANO_DE_ENSINO.md`, seção 4): **ART.3 Exploração,
Pré-processamento e Hipóteses, peso 5**, e **ART.5 Distribuição normal e teste de hipótese,
peso 4**. A Sprint 2 fecha em **28/08**. Deixe explícito o que cada dupla leva pronto: base larga,
defasagens, sazonalidade codificada, colunas padronizadas, e as três hipóteses da própria série
escritas no formato hipótese, teste, decisão, consequência.

---

## Checklist de material antes do encontro

- [ ] `notebooks/aula04.ipynb` aberto e executado uma vez, do início ao fim, na máquina do
      professor (a execução leva menos de um minuto e não depende de rede).
- [ ] Os cinco CSVs presentes em `dados/`, para quem estiver com o repositório clonado.
- [ ] O quadro dividido em cinco colunas, uma por série, para a comparação do Bloco 2.
- [ ] O PDF do deck **não** distribuído antes da aula: o botão de exportação revela o gabarito do
      quiz, conforme documentado em `inteli-deck-design` seção 8.6.
- [ ] O arquivo da ponderada **fora** de qualquer pasta do repositório. O `.gitignore` já cobre os
      padrões `Ponderada*.pdf` e `*-gabarito*.pdf`, mas um arquivo com outro nome commitado por
      engano vai ao ar no push seguinte.

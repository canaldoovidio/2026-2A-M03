# Notas do professor: Aula 03

**11/08/2026 &middot; Introdução ao Pandas, Numpy e bibliotecas gráficas, Exploração de Dados
&middot; Sprint 1**

Material de condução do encontro, não de distribuição ao aluno. Não é resumo do deck: são as
perguntas que abrem a sala quando ela travar, cada uma com a resposta esperada e o erro que a
pergunta costuma revelar.

Ordem igual à do roteiro em `PLANEJAMENTO_AULA_A_AULA.md`.

**Aviso de condução:** esta é a última aula antes da entrega da Sprint 1. O notebook fica aberto o
encontro inteiro, e cada um dos seis blocos tem prática de verdade, não só teoria. Reserve os
últimos cinco minutos de cada bloco para andar entre as duplas em vez de ficar na frente.

---

## 10h00 - 10h15 &middot; Daily

**Checkpoint de abertura:** cada dupla escolhe qual das cinco séries vai explorar primeiro
(`abate_bovinos`, `abate_suinos`, `abate_frangos`, `producao_ovos`, `producao_leite`). Escrever os
cinco nomes no quadro e marcar quem pegou o quê, para o exercício de comparação do bloco de Numpy
(11h00) ter variedade entre as duplas.

---

## 10h15 - 10h30 &middot; Resgate e abertura

**P1. Qual das cinco categorias vocês acham que tem a série histórica mais longa?**

Pergunta do roteiro. Peça palpite de mão levantada antes de qualquer dupla abrir o notebook.

- *Resposta esperada real:* `producao_ovos`, com 157 registros desde `1987-T1`. As outras quatro
  têm 117, desde `1997-T1`.
- *O erro que revela:* a maioria costuma apostar em bovinos ou leite, por serem mais "visíveis" no
  discurso público sobre agropecuária. O achado real (ovos) é surpreendente de propósito: força a
  turma a checar em vez de assumir, que é o espírito da aula inteira.

**P2. A Aula 02 mapeou os três modelos e fechou a decisão de granularidade. O que muda hoje?**

- *Resposta esperada:* a ferramenta. Os mesmos números (contagem, unidade, período) que a Aula 02
  calculou na mão, com dicionário e laço, hoje saem de `describe()` e `isna()` em uma linha.
- *O erro que revela:* achar que Pandas traz conteúdo novo de negócio. Não traz: traz velocidade.
  O conteúdo de negócio (o que os números significam) continua sendo o mesmo da Aula 02.

---

## 10h30 - 10h45 &middot; Pandas: DataFrame

**P3. Por que `periodo` não vira uma coluna de data (`datetime64`)?**

A pergunta mais importante deste bloco, mesmo sem estar escrita no roteiro como pergunta disparada.

- *Resposta esperada:* porque `"2025-T4"` não é uma data de calendário, é um rótulo de trimestre.
  Converter para `datetime64` obrigaria escolher um mês arbitrário (janeiro? outubro?) para
  representar o trimestre inteiro, reintroduzindo o erro de granularidade que a Aula 02 evitou.
- *O erro que revela:* o hábito de "sempre converter data para datetime". Aqui a conversão erra
  antes mesmo de rodar: o dado não é mensal, e fingir que é resolve um problema de tipagem criando
  um problema de conteúdo, pior que o original.

**Prática imediata (o roteiro chama assim, não é opcional).** Cada dupla carrega o CSV que
escolheu no daily e roda `describe()`.

**P4. `count` deu diferente de 117. O que isso significa?**

Só para as duplas que pegaram `producao_ovos`.

- *Resposta esperada:* não é erro de leitura, é a série real, mais longa que as outras quatro.
- *O erro que revela:* assumir que uma contagem diferente do resto do grupo é sinal de bug no
  próprio código, antes de checar se o arquivo em si é diferente.

---

## 10h45 - 11h00 &middot; Estatística descritiva

**P5. A sua média bate com a faixa que `dados/README.md` documenta?**

- *Resposta esperada:* sim, nas cinco séries, célula por célula.
- *O erro que revela:* se não bater, o instinto errado é desconfiar do arquivo. Corrija: se o
  arquivo já passa nos testes automatizados de `tools/tests/test_dados.py`, o problema quase
  sempre está na leitura ou no cálculo da dupla, não no dado. Volte uma célula antes de suspeitar
  do CSV.

**P6. `producao_ovos` tem o segundo maior coeficiente de variação (44,9%), mas o menor salto
trimestral médio (1,91%, visto só no bloco seguinte). Como as duas coisas coexistem?**

Pergunta para puxar depois que a seção de Numpy já tiver rodado; volte a ela então, ou adiante se a
turma estiver rápida.

- *Resposta esperada:* o coeficiente de variação, calculado sobre décadas, mistura crescimento de
  longo prazo com oscilação de curto prazo. Uma série que cresce de forma suave e constante ainda
  tem desvio padrão alto, porque o início e o fim da série estão muito distantes.
- *O erro que revela:* tratar "dispersão alta" como sinônimo de "instável". São coisas diferentes,
  e confundir as duas é um erro que volta na Aula 04, quando a turma for decidir que tipo de
  feature de defasagem faz sentido para cada série.

---

## 11h00 - 11h15 &middot; Numpy

**P7. Por que a variação usa `valores[:-1]` no denominador, e não `valores[1:]`?**

O bug mais comum desta célula, e não levanta exceção.

- *Resposta esperada:* `np.diff(valores)` tem um elemento a menos que `valores`; a posição 0 do
  resultado é a diferença entre o segundo e o primeiro elemento. Dividir por `valores[:-1]` compara
  cada diferença com o valor **anterior** a ela, que é a definição de variação percentual. Usar
  `valores[1:]` compararia com o valor seguinte, invertendo a lógica sem travar nada.
- *O erro que revela:* não conferir manualmente os dois ou três primeiros valores do array
  resultante contra uma conta feita na calculadora. É o mesmo hábito de verificação que salvou a
  Aula 02 no caso do leite.

**Exercício (o roteiro pede cálculo do maior salto por dupla).**

**P8. Comparando as cinco duplas: qual série tem o salto mais violento?**

- *Resposta esperada:* `producao_leite`, com +18,87% entre `2000-T3` e `2000-T4`.
- *O erro que revela:* nenhum, é fechamento de exercício. Aproveite para perguntar em seguida: "e
  o maior salto **em módulo absoluto** (`np.diff` sem dividir por `valores[:-1]`), é da mesma
  série?" (não é: o maior deslocamento absoluto é de `abate_bovinos`, cerca de 302,5 milhões de kg
  entre `2025-T4` e `2026-T1`, mesmo o percentual dessa queda sendo pequeno frente ao nível já
  alto da série. É outro lembrete de que percentual e valor absoluto respondem perguntas
  diferentes.)

---

## 11h15 - 11h30 &middot; Matplotlib e Seaborn

**P9. O ponto que vocês marcaram como "maior salto" é também o ponto mais alto do gráfico?**

- *Resposta esperada:* não necessariamente (e no exemplo de `abate_bovinos`, não é: o pico da série
  inteira é em 2025/2026, muito depois do salto de 2005). Salto maior é sobre a taxa de mudança
  entre dois trimestres consecutivos, não sobre o nível absoluto.
- *O erro que revela:* olhar o gráfico e apontar o pico visual como resposta para "onde está o
  maior salto". São perguntas diferentes que o olho tende a confundir.

**P10. O gráfico de sazonalidade do leite mostra T2 sempre mais baixo. Isso prova a causa?**

- *Resposta esperada:* não. Mostra que o padrão é estável ano após ano (não é ruído de um ano
  isolado), mas nenhum dos cinco CSVs tem coluna de clima, estação ou sistema de criação. Qualquer
  explicação é hipótese.
- *O erro que revela:* é o mesmo erro que a Aula 02 nomeou para análise diagnóstica ("o dado mostra
  a queda, a causa está fora dele"). Se a turma já usa esse vocabulário de cabeça, é sinal de que a
  espiral está funcionando.

**Exercício (plotar a série escolhida, procurar sazonalidade e outlier).** Ande pelas duplas
perguntando "qual trimestre do ano costuma ser mais alto na sua série?" antes delas mostrarem o
gráfico. Forçar o palpite antes do olhar é o que torna o exercício uma verificação, não uma
confirmação do que já se esperava ver.

---

## 11h30 - 11h45 &middot; Dados faltantes

**P11. `isna().sum()` deu zero nas cinco séries. Isso significa que os dados estão sem
problema?**

A pergunta central do bloco, análoga à P11 da Aula 02.

- *Resposta esperada:* não. Zero significa zero **célula vazia**. `tools/baixar_dados.py` já
  filtra os marcadores de ausência do SIDRA antes de gravar o CSV; `isna()` está confirmando esse
  filtro, não atestando qualidade geral.
- *O erro que revela:* o mesmo da Aula 02, com `producao_leite`: confundir teste verde com
  qualidade garantida. Se a turma lembrar sozinha do caso do leite (adquirido vs. produzido) aqui,
  ótimo sinal de retenção; se não, puxe.

**P12. Se o `isna()` desse maior que zero, o que vocês fariam: `dropna()` ou `fillna()`?**

Pergunta de antecipação, não tem resposta certa hoje.

- *Resposta esperada:* depende de quantas linhas seriam perdidas e de onde elas caem na série
  (início, fim, meio). Não há regra universal.
- *O erro que revela:* nenhum, se a turma disser "depende". O erro seria alguém responder com
  confiança absoluta uma das duas opções sem perguntar mais nada. Registre que essa decisão volta
  na Aula 04.

**Exercício (contar vazios da própria série e apontar o risco de qualidade que sobrevive ao
`isna()` zerado).**

---

## 11h45 - 12h00 &middot; Amarração com a sprint

**P13. Se vocês tivessem que fechar a ART.2 agora, o que já está pronto?**

- *Resposta esperada:* o `describe()` das cinco séries, o maior salto de cada uma, ao menos um
  gráfico com sazonalidade ou outlier apontado, e a confirmação (com ressalva) de `isna()`.
- *O erro que revela:* achar que falta "mais gráfico" ou "mais número". O que costuma faltar é a
  **explicação** ao lado do gráfico: por que aquele padrão importa para o case da LDC, não só que
  ele existe.

Lembrar: Sprint 1 fecha em **14/08**, com **ART.1 Entendimento do negócio (peso 6)** e **ART.2 UX
parte 1 (peso 3)**. Próximo encontro em **19/08**, Sprint 2, Pré-processamento e Feature
Engineering.

---

## Se a sala travar

- **A turma trava na fatia `valores[:-1]` do Numpy.** Peça para rodarem, isoladamente, `np.diff([10,
  12, 9])` e compararem o resultado (`[2, -3]`) com a conta na mão. Ver o array pequeno resolve mais
  rápido que qualquer explicação verbal.
- **O exercício de sazonalidade vira debate sobre a causa do padrão do leite.** Corte com a P10 e
  registre a hipótese no quadro, sem resolver. É conteúdo da Aula 04 em diante, não de hoje.
- **Sobrou tempo.** Peça para calcularem o coeficiente de variação de todas as cinco séries (é o
  item 1 do desafio) e ordenarem da maior para a menor. A surpresa de `producao_ovos` liderar essa
  lista reabre a P6 com mais tempo de discussão.
- **Faltou tempo.** O bloco que pode ser cortado para leitura assíncrona é o de Matplotlib e Seaborn
  (11h15): mande o exercício de plotagem como parte da preparação da ART.2, mas não corte o bloco
  de dados faltantes (11h30), porque ele é o argumento central da aula.

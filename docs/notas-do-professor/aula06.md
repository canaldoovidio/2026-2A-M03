# Notas do professor: Aula 06

**01/09/2026 &middot; Aprendizado Não Supervisionado parte I &middot; Sprint 3**

Material de condução do encontro. O conteúdo abaixo reúne as perguntas que abrem a sala quando ela
travar, cada uma com a resposta esperada e o erro que a pergunta costuma revelar. A ordem segue o
roteiro dos sete blocos desta aula, registrado no cabeçalho de `aulas/aula06.html`.

**Esta aula trocou conteúdo novo por retomada.** O módulo estava acima do que a turma acompanhava
em quatro eixos ao mesmo tempo: mecânica de Python, conceitos de modelagem, densidade de conteúdo e
amarração com a entrega. A resposta foi reduzir o escopo do encontro a uma única técnica nova,
K-means com K fixo em 4, e usar a primeira hora em diagnóstico e revisão dirigida das Aulas 01 a
05. Elbow Plot e Silhouette Analysis, que o roteiro previa para hoje, migraram para a Aula 08. A
decisão e o custo dela estão em `docs/adrs/ADR-009`.

**Onde está o peso desta aula:** o slide 29, em que a silhueta cai de 0,4795 para 0,2853 justamente
quando a concordância com o calendário sobe de 26,5% para 98,3%. Um aluno que saia daqui sabendo
rodar `KMeans` e sem saber que a métrica interna não mede utilidade não aprendeu o que a aula
ensina. Se algum bloco tiver de encolher ao vivo, que não seja esse.

**Navegação, e ela é necessária hoje.** Os slides 11 a 20 são cinco módulos de revisão visitados
sob demanda, e o professor entra em dois ou três deles. No Reveal 5.1.0 a ida direta a um slide é
`G`, o número do slide e `Enter`. O índice do slide 10 traz o destino de cada módulo. Vale testar a
combinação uma vez antes de a aula começar, porque procurar o slide com as setas na frente da turma
custa o tempo que o bloco de revisão não tem.

---

## Checkpoint de abertura, antes de qualquer coisa

**A pergunta que abre a sala:** quais duplas conseguiram rodar a base analítica da Aula 04 na
própria máquina? Peça o `shape`, que é `(113, 15)`. Levante a mão de quem não tem.

Quem não conseguiu **não acompanha o bloco das 10h50 nem os dois atos da prática**, e o conserto é
imediato: abrir `notebooks/aula06.ipynb` pelo badge do Colab da primeira célula. A seção 1 do
notebook é autocontida, baixa os cinco CSVs e reconstrói a base do zero em uma célula só, sem
depender de nada instalado localmente.

**O critério de sucesso da célula é explícito:** sair MAPE de 1,60% para o modelo e 1,69% para a
baseline de coeficiente fixo. Quem obtiver esses dois números está pronto para o resto da aula.
Quem obtiver outros dois, ou um erro, precisa de atendimento antes das 11h20, porque depurar
ambiente no meio da prática custa o bloco inteiro.

Registre no papel quais duplas ficaram no Colab. Elas vão precisar do mesmo caminho na Aula 07.

---

## Ordem de prioridade da revisão dirigida

O quiz das 10h15 tem seis perguntas e o bloco de revisão vai das 10h30 às 10h50. **Vinte minutos
não cobrem seis tópicos.** Se o diagnóstico reprovar tudo, a ordem abaixo é a que preserva o que a
Aula 07 vai precisar.

| ordem | pergunta | tópico | slide | por que nesta posição |
| --- | --- | --- | --- | --- |
| 1 | 4 e 5 | Aula 05: corte temporal e baseline | 19 | Pré-requisito da Aula 07, que compara árvores e ensembles contra os mesmos 1,60% e 1,69% no mesmo protocolo. Sem isto, a comparação de quinta-feira não significa nada. |
| 2 | 3 | Aula 04: junção e as 113 linhas | 17 | O aluno que não sabe de onde vêm as 113 linhas não confia no próprio `shape`, e trava de novo na primeira célula de toda aula prática. |
| 3 | 1 e 2 | Aulas 03 e 02: as cinco séries e a granularidade | 15 e 13 | Enquadramento do case. Custa pouco tempo e nenhuma das duas é pré-requisito técnico do que vem hoje. |
| 4 | 6 | Aula 04: condicionamento numérico | 18 | Última da fila. O material de apoio da Aula 05, seção 9, cobre o assunto inteiro por escrito, com a tabela de antes e depois da padronização. |

A pergunta 6 sai da fila de sala com boa consciência. O que vale dizer em voz alta, mesmo sem abrir
o slide 18, é a regra prática: padronizar as entradas sempre que as escalas diferirem por várias
ordens de grandeza. Ela reaparece hoje no K-means, por um motivo diferente, e a seção 2 do material
de apoio da Aula 06 faz a ponte entre os dois usos.

O slide 11, da Aula 01, fica fora dessa ordem de propósito: ele não tem pergunta no quiz. Abra-o
apenas se alguém travar em `read_csv` durante a retomada das 10h50, e nesse caso o atendimento é
individual, sem parar a sala.

---

## Ordem de corte, se o tempo apertar

A sequência abaixo diz o que cede primeiro. Ela vale para decisão ao vivo, quando o relógio já
passou do previsto.

1. **Bloco de ART.6, das 11h50.** É o primeiro a ceder, e cortá-lo tem custo declarado: a
   amarração com a entrega foi um dos quatro problemas que motivaram esta aula. Se cair, mande o
   conteúdo do slide 33 por escrito no mesmo dia e cobre a pendência de cada dupla no daily de
   04/09. Não deixe a turma sair sem saber que a ART.6 fecha na Sprint 3, com review em 11/09.
2. **Bloco de interpretação, das 11h40.** O perfil sazonal e as duas exceções de 2008 estão nas
   seções 6 e 8 do material de apoio, com a tabela de participação absoluta que o slide não
   mostra. O material continua disponível à turma, então o que se perde é a discussão em sala.
3. **Revisão dirigida, das 10h30.** Encolher para um único módulo, seguindo a ordem de prioridade
   acima. O quiz já terá feito o diagnóstico, que é metade do valor do bloco.
4. **Retomada com as mãos, das 10h50.** Último recurso antes do núcleo. Cortar aqui deixa quem
   está com o ambiente quebrado sem conserto, então prefira cortar o item 3.
5. **O par ato 1 e ato 2, das 11h20, com o slide 29.** É a aula. Não cai.

---

## 10h00 - 10h15 &middot; Daily

Abertura da Sprint 3, com planning em 31/08 e review em 11/09. Além do checkpoint de ambiente
registrado acima, confirme quem já leu os cinco autoestudos da semana, em especial o de K-means: o
bloco das 11h05 assume a leitura feita e apresenta o algoritmo em um slide só.

---

## 10h15 - 10h30 &middot; Bloco 1: diagnóstico

Seis perguntas de múltipla escolha, slides 4 a 9, uma por vez. **Não corrija durante o quiz.**
Anote quantas duplas erraram cada item e siga. A correção acontece no bloco seguinte, e só nos
tópicos que reprovaram.

O que cada pergunta revela, quando erra:

- **Pergunta 1 (Aula 03, qual série tem o histórico mais longo).** Quem responde `abate_frangos`
  está confundindo o alvo do Modelo 1 com o tamanho da série. A resposta é `producao_ovos`, com 157
  registros desde 1987-T1, e os quarenta a mais não sobrevivem à junção.
- **Pergunta 2 (Aula 02, o descompasso mensal contra trimestral).** Quem escolhe interpolar não
  percebeu que interpolação não cria informação. É o erro conceitual mais caro do quiz, porque ele
  reaparece em qualquer projeto com fonte de granularidade errada.
- **Pergunta 3 (Aula 04, de 117 para 113 linhas).** Quem responde "valores extremos" ou "conjunto
  de teste" não associa o `dropna()` ao `shift(4)`. Esse aluno vai ter medo do próprio `shape` a
  cada aula prática.
- **Pergunta 4 (Aula 05, por que o corte é por data).** Quem escolhe "produz um MAPE menor" inverteu
  o argumento: o corte por data costuma dar erro maior, e é isso que o torna honesto.
- **Pergunta 5 (Aula 05, a margem contra a baseline).** Quem responde "mais de um ponto percentual"
  está lembrando da média das doze janelas (2,18% contra 3,14%) e aplicando ao teste. A margem da
  janela de teste é de 0,10 ponto percentual.
- **Pergunta 6 (Aula 05, padronização e condicionamento).** Quem erra aqui costuma achar que
  `StandardScaler` remove linha. Tópico de menor prioridade na revisão, pelo motivo já registrado.

**Se a turma acertar quase tudo:** encurte a revisão para um módulo e devolva o tempo ao bloco de
interpretação das 11h40, que é onde a discussão rende mais.

---

## 10h30 - 10h50 &middot; Bloco 2: revisão dirigida

Conduzida pelo índice do slide 10, na ordem de prioridade da seção acima. Dois ou três destinos, no
máximo.

**Como conduzir cada módulo:** abra o slide, peça a alguém que errou a pergunta correspondente para
ler o código em voz alta e explique só o que a pergunta revelou. Percorrer o slide inteiro consome
o bloco em um destino.

**Erro comum de condução, e vale evitar:** transformar a revisão em reapresentação da aula
original. A turma já viu esse conteúdo, e o que falta é a ligação entre o comando e o motivo dele.
Duas ou três frases por slide bastam.

**Se ninguém errou nada:** pule para as 10h50 e diga por quê. A turma precisa saber que o
diagnóstico teve consequência, senão o quiz da próxima aula vira formalidade.

---

## 10h50 - 11h05 &middot; Bloco 3: retomada com as mãos

Todos rodam a célula única da seção 1 do notebook e conferem 1,60% contra 1,69%.

**Pergunta enquanto a célula roda:** "Essa célula ajusta o escalador em quais linhas?"

**Resposta esperada:** só nas 105 de treino.

**Erro comum:** responder "nas 113". Quem responde isso vai ajustar escalador na base inteira nos
dois atos de hoje, e é bom corrigir agora, porque o K-means padroniza tudo de propósito e a
diferença entre os dois casos precisa estar clara antes das 11h20.

**Tropeço técnico previsível:** rede da sala. A célula baixa os cinco CSVs quando não encontra a
pasta `dados/` ao lado do notebook. Se a rede falhar, a mensagem de erro do notebook orienta a
pedir a pasta a uma dupla que tenha o repositório clonado. Tenha uma cópia da pasta em pendrive ou
compartilhada, para não perder o bloco.

---

## 11h05 - 11h20 &middot; Bloco 4: K-means como conceito

Slide 24, um slide só. A leitura do autoestudo é pressuposta.

**Pergunta disparada:** "Se eu não padronizar as cinco colunas antes de agrupar, o que acontece?"

**Resposta esperada:** a série de maior magnitude domina a distância e as outras quatro deixam de
influenciar o resultado.

**O que extrair disso:** na Aula 05 a padronização resolvia um problema numérico do solver. Aqui
ela define o que o algoritmo considera parecido, porque a distância euclidiana soma as diferenças
de todas as colunas com o mesmo peso. É a mesma linha de código com duas funções diferentes, e
vale nomear as duas.

**Segunda pergunta, sobre `random_state`:** "Por que a regressão da Aula 05 não precisava de
semente e esta precisa?"

**Resposta esperada:** mínimos quadrados tem solução fechada, e o K-means começa de centros
sorteados.

**Erro comum:** achar que `n_init=50` e `random_state=42` fazem a mesma coisa. `n_init=50` roda o
algoritmo cinquenta vezes e fica com a melhor delas pela inércia. `random_state=42` faz com que
essas cinquenta sejam sempre as mesmas, de uma execução para outra.

---

## 11h20 - 11h40 &middot; Bloco 5: os dois atos, e o slide 29

**Antes de rodar o ato 1, cobre a aposta.** Cada dupla escreve se acredita que o K-means vai
separar T1, T2, T3 e T4. A maioria vai apostar que sim. A aposta escrita é o que faz o resultado do
slide 26 valer alguma coisa.

**Pergunta depois do ato 1:** "Vocês acertaram a aposta? O que os quatro grupos são, afinal?"

**Resposta esperada:** blocos contíguos de tempo, com concordância de 26,5% contra os 25% do acaso.

**O que extrair:** as cinco séries crescem ao longo de 29 anos, e o nível de produção domina a
distância entre os pontos padronizados. A estrutura que o algoritmo achou é verdadeira, e a
pergunta do case pedia outra.

**Ponto que costuma passar despercebido, e vale forçar:** os grupos 3 e 4 se sobrepõem entre
2019-T3 e 2020-T2. Se alguma dupla apontar isso, é o melhor momento do bloco: a transição entre
épocas acontece ao longo de alguns trimestres, e a coluna da direita do slide 26 informa o
intervalo que cada grupo cobre.

**Pergunta depois do ato 2, e é a mais importante do dia:** "O que exatamente mudou entre os dois
atos?"

**Resposta esperada:** só a transformação da entrada. Mesmo algoritmo, mesmo K, mesma semente,
mesmos dados.

**O que registrar:** a escolha de como representar o dado pesou mais no resultado do que a escolha
do algoritmo, e essa escolha é de quem escreve o código.

### O slide 29, que é o núcleo da aula

**Pergunta antes de mostrar a tabela:** "Qual dos dois agrupamentos vocês acham que tem a melhor
silhueta?"

**Resposta esperada da turma:** o ato 2, porque acertou o calendário.

**O que sai:** o ato 1, com 0,4795 contra 0,2853. A métrica premia o agrupamento que não responde
à pergunta do case.

**Como conduzir sem virar paradoxo:** a silhueta mede separação geométrica e faz isso corretamente.
No ato 1 as épocas caem em regiões distantes do espaço padronizado; no ato 2 todas as linhas ficam
comprimidas em torno de um quarto do total anual, porque nenhum trimestre deixa de produzir. O
número que decidiu a aula veio de fora do agrupamento: a concordância usa o trimestre do
calendário, um rótulo que o `KMeans` nunca recebeu.

**Erro comum:** concluir que a silhueta "não presta". Ela responde bem à pergunta para a qual foi
construída, e é o que sobra quando não existe rótulo externo nenhum, que é o caso mais comum em
produção. O erro está em ler a resposta dela como medida de utilidade. Diga que a Aula 08 volta a
usá-la para escolher K, e que o cuidado de hoje vale integralmente lá.

**Se sobrar tempo, o desafio do notebook reforça o mesmo achado duas vezes.** Incluir 2026-T1 na
conta de participação faz um dos quatro grupos ficar com essa única linha, funde o T3 com o T4 e
derruba a concordância, e a silhueta sobe. Rodar o ato 2 com `n_clusters=2` separa o primeiro
semestre do segundo, perde a distinção entre o pico do leite e o das carnes, e a silhueta sobe de
novo. As respostas completas estão na seção 9 do material de apoio.

---

## 11h40 - 11h50 &middot; Bloco 6: interpretação

**Pergunta disparada:** "Olhando o perfil sazonal, qual série o Modelo 2 vai errar mais se tratar
todas com um fator sazonal único?"

**Resposta esperada:** o leite, que tem amplitude de 3,85 p.p. e pico no T4, enquanto as três
carnes picam no T3.

**Cuidado ao conduzir a comparação entre frango e ovos:** os dois estão a 0,02 ponto percentual um
do outro, 1,10 contra 1,08. **Não declare qual é o menor.** Uma diferença desse tamanho sobre 29
anos de média é ruído, e qualquer revisão de dado do SIDRA pode inverter a ordem. O que se afirma é
que os dois empatam no piso, bem abaixo das outras três séries. Se um aluno perguntar qual é o
menor, essa é a resposta, e ela ensina mais do que o número.

**Sobre as duas exceções de 2008:** a coincidência com a crise financeira internacional é a
hipótese óbvia, e a base não tem como testá-la. Nenhuma coluna aqui mede crédito, câmbio, preço de
insumo ou exportação. Conduza como uso legítimo de método não supervisionado: o agrupamento reduziu
116 linhas a duas que merecem investigação, e apontar onde olhar já é entrega. Atribuir causa exige
outra fonte.

**Ponto técnico que vale explicar, porque ninguém percebe sozinho:** as exceções aparecem em par
dentro do mesmo ano por causa da transformação. A participação é fração do total do próprio ano,
então uma observação atípica desloca os outros três trimestres junto, mesmo sem nada de anormal ter
acontecido neles.

---

## 11h50 - 12h00 &middot; Bloco 7: ART.6

**O que declarar:** a ART.6 Preparação dos Dados e Modelagem, peso 6, é a única entrega que a
matriz do `PLANO_DE_ENSINO.md` (seção 5) amarra a esta aula, e ela fecha na Sprint 3, com review em
11/09. O slide 33 mostra o que já existe e o que falta em cada uma das três frentes.

**A tarefa concreta do bloco:** cada dupla anota agora a própria pendência da terceira coluna, com
nome e prazo. Sem isso, o bloco vira leitura de tabela.

**Cuidado com o número que vai para o relatório.** O MAPE de 1,60% mede oito previsões de um
trimestre à frente. Prevendo os oito de uma vez, realimentando a própria saída, o erro sobe para
2,85%. A entrega precisa dizer em qual dos dois regimes o número foi medido.

**Ponte para a Aula 07:** o alvo volta a existir, e o protocolo continua o mesmo. Árvores e
ensembles serão comparados contra 1,60% e 1,69%, no mesmo corte temporal, e é por isso que as
perguntas 4 e 5 do quiz de hoje têm prioridade na revisão.

---

## O aviso sobre a divergência com o planejamento, para assumir em sala

O roteiro em `PLANEJAMENTO_AULA_A_AULA.md` prometia, para a janela das 11h30, interpretar os
clusters como perfis de dieta, com o exemplo de trimestres de maior demanda de milho contra farelo
de soja. **Essa entrega não existe nesta aula, e o motivo é o dado.** As cinco séries do SIDRA
medem abate e produção animal, e nenhuma delas mede consumo de macroingrediente. A conversão de
produção em composição de ração é o Modelo 3 do TAPI, que depende de coeficientes técnicos de
formulação sem fonte aberta.

O que o agrupamento entrega para o mesmo destino é o perfil sazonal por espécie: em que trimestre
cada produto concentra a produção e com que amplitude. É uma entrada real para o Modelo 2, medida
em dado aberto.

**Assuma isso em sala, com o mesmo tratamento que a Aula 05 deu à divergência com a Aula 04.**
Naquela aula, uma afirmação sobre padronização feita na Aula 04 não se confirmou na medição, e o
material registrou a correção por escrito. Aqui a situação é a mesma em natureza: um roteiro
escrito antes de o dado ser explorado descreve uma expectativa, e a expectativa se revisa quando a
medição chega. A turma está aprendendo a fazer exatamente isso, e ver o professor fazendo vale mais
do que o slide que teria sido apresentado. A seção 10 do material de apoio traz o registro
completo, incluindo as outras duas reduções de escopo.

---

## Perguntas soltas, para quando sobrar tempo

- "Se o K-means não tem rótulo, como saber se o resultado está certo?" Resposta: não existe "certo"
  no sentido da Aula 05. O critério passa a ser a utilidade, medida contra a pergunta do parceiro,
  com informação que vem de fora do agrupamento. Hoje esse papel coube ao trimestre do
  calendário.
- "Por que 2026-T1 fica na base do ato 1 e sai na do ato 2?" Resposta: no ato 1 o valor é o nível
  de produção, que existe para qualquer trimestre isolado. A conta do ato 2 divide cada valor pelo
  total do próprio ano, e o ano de 2026 ainda não tem total.
- "Dá para usar os grupos do ato 1 como coluna no modelo da Aula 05?" Resposta: dá, e é uma ideia
  natural para a ART.6. O cuidado é que o rótulo do grupo carrega informação de toda a série, o que
  põe futuro dentro do treino se o agrupamento for ajustado na base inteira. É a segunda forma de
  vazamento da Aula 05, e a Aula 12 resolve o caso com `Pipeline`.

---

## Registro editorial

O cabeçalho deste arquivo segue a forma nova, inaugurada em `docs/notas-do-professor/aula05.md`. As
Aulas 01 a 04 usam uma construção de paralelismo negativo que as diretivas de tom do acervo
proíbem, e o alinhamento das quatro está listado em `docs/ANDAMENTO.md` como decisão pendente do
professor.

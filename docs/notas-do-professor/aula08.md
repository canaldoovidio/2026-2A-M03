# Notas do professor: Aula 08

**10/09/2026 &middot; Aprendizado Não Supervisionado Parte II &middot; Sprint 3**

Material de condução do encontro. O conteúdo abaixo reúne as perguntas que abrem cada bloco quando
a sala travar, cada uma com a resposta esperada e o erro que a pergunta costuma revelar. A ordem
segue os cinco blocos da divisão dos 105 minutos registrada na `docs/adrs/ADR-011-escopo-e-base-do-pca-da-aula-08.md`,
e todos os números vêm de `tools/tests/test_pca_aula08.py`, que trava as oito conclusões da aula.

**Onde está o peso desta aula:** a tabela de MAPE por número de componentes, no terceiro
sub-bloco do PCA. O modelo do fecho da Aula 07 tem MAPE de teste de 3,32% com as 11 features, e a
baseline de coeficiente fixo da LDC tem 3,71%. Reduzir a dimensionalidade por PCA leva o MAPE a
4,92% com dois componentes, 4,94% com quatro (os mesmos quatro que retêm 96,07% da variância) e
6,20% com nove, e o modelo perde da baseline em todo k de 1 a 9. Só k=10 devolve os 3,32%. Um
aluno que saia daqui sabendo rodar `PCA()` e sem saber que 96,07% da variância retida custou 1,6
ponto percentual de MAPE não aprendeu o que a aula ensina. Se algum bloco tiver de encolher ao
vivo, que não seja esse, nem o contraste dos três critérios na escolha de K.

---

## Checkpoint de abertura, antes de qualquer coisa

**A pergunta que abre a sala:** quais duplas ainda têm a base mensal da Aula 07 rodando na própria
máquina? Peça o `shape`, que é `(339, 18)` depois do `dropna()`. Levante a mão de quem não tem.

Quem não tem não acompanha o bloco de PCA, e o conserto é imediato: abrir `notebooks/aula08.ipynb`
pelo badge do Colab da primeira célula e ir direto à seção 4. Aquela célula é autocontida por
decisão registrada na `ADR-011`: ela lê as cinco séries de `dados/mensal/`, remonta a base de 339
linhas, corta os 315 meses de treino e ajusta escalador e PCA sozinha, sem depender de nenhuma
célula anterior do notebook.

Registre no papel quais duplas ficaram no Colab. É a mesma lista que vai importar no bloco de
prática, 40 minutos depois.

---

## Ordem de corte, se o tempo apertar

1. **A seção 10 do notebook, o PCA sem padronizar.** É o primeiro a ceder. O achado cabe em uma
   frase dita em voz alta: sem padronizar, PC1 explica 96,72% da variância e seus maiores pesos
   são `lag12` com 0,481, `lag3` com 0,475 e `lag1` com 0,475, porque o desvio-padrão de `lag1` no
   treino é 244.980.297 contra 0,708 de `sen`. É o mesmo achado de condicionamento da Aula 05, e o
   material de apoio cobre o resto por escrito.
2. **A tabela de correlação e o número de condição.** Encolher para os dois números: 20 dos 55
   pares de features têm correlação absoluta acima de 0,9, o maior deles é `lag1` com `lag3` em
   0,9810, e o número de condição da matriz padronizada de treino é 28,50. É a resposta medida da
   pergunta disparada de abertura, e ela não pode simplesmente desaparecer: diga os números mesmo
   sem projetar a tabela.
3. **A base de níveis, na seção 3 do notebook.** Encolher para a leitura: na base de níveis a
   silhueta é mais alta em todo K, de 0,5639 em K=2 a 0,4247 em K=8, e a concordância com o
   calendário fica entre 25,6% e 29,1%, o acaso de quatro trimestres. Os dois números que a Aula
   06 publicou (silhueta 0,4795 com concordância de 26,5% nos níveis, contra 0,2853 com 98,3% na
   participação, os dois em K=4) já sustentam o ponto sozinhos.
4. **Sistemas de recomendação cai de 10 para 5 minutos**, mantendo a analogia com o Modelo 3 e o
   apontamento dos cinco autoestudos da semana. É o único bloco sem prática e sem dado no acervo,
   então é o que menos perde ao encolher, mas ele não sai: a Semana 06 tem cinco autoestudos sobre
   o assunto e a turma vai perguntar.
5. **A tabela de MAPE por k e o contraste dos três critérios de K não saem.** São a aula. Sem a
   tabela de MAPE, ninguém sai sabendo o preço do corte. Sem o contraste de K, o bloco de escolha
   de K vira receita de Elbow Plot, que é exatamente o que o autoestudo já entregou.

---

## A resposta de trinta segundos sobre o autoestudo

A turma leu, para hoje, cinco autoestudos e os cinco são de sistemas de recomendação:
"Implementação: Sistemas de Recomendação I", "Kaggle: Sistemas de Recomendação II", "Ponderada 2
de Computação", "Sistemas de Recomendação" e "Tipos de Sistemas de Recomendação". A aula gasta 10
minutos nesse assunto e 70 nos outros dois, e alguém vai notar.

**O descompasso, dito sem rodeio se perguntarem.** "Determinando K: Elbow Plot" e "Determinando K:
Silhouette Analysis" são autoestudos da Semana 05, lidos em 01/09, antes da Aula 06, e o método só
é ensinado em sala hoje, 10/09, nove dias depois. A Aula 06 usou a silhueta como número lido em
dois agrupamentos, sem ensinar o método, o que ameniza e não fecha o descompasso. O registro está
em `docs/ANDAMENTO.md`.

O mesmo vale para o outro lado do calendário: PCA tem um autoestudo opcional na Semana 05
("Opcional: PCA") e dois obrigatórios na Semana 07, "PCA - Resolvendo o problema da
dimensionalidade" e "PCA: o que é e como usar em Python", que serão lidos depois da aula que
ensina PCA. Quem quiser reforço do bloco de hoje tem leitura marcada para a semana que vem, e a
Aula 09 retoma o assunto no bloco de maldição de dimensionalidade.

Sistemas de recomendação, em compensação, tem cinco autoestudos lidos hoje e a Ponderada 2 de
Computação como exercício da mesma semana. É onde o assunto se aprofunda, e vale dizer isso em voz
alta ao abrir o quarto bloco, para que os 10 minutos de sala não sejam lidos como desprezo pelo
tema.

---

## Se a prática de PCA falhar no ambiente da dupla

O bloco de PCA tem 45 minutos e um único momento de mão no código. Se o ambiente da dupla falhar
ali, ela perde o bloco inteiro, e é por isso que a `ADR-011` registra este risco com mitigação
escrita. A sequência de conserto, na ordem, sem passar de cinco minutos por dupla:

1. **Colab, pelo badge da primeira célula do notebook.** A célula da seção 4 é autocontida e não
   precisa de nada instalado localmente. Duas falhas locais respondem por quase tudo:
   `ModuleNotFoundError: No module named 'sklearn'` e uma cópia velha de `dados/mensal/`. As duas
   somem no Colab.
2. **Rede da sala caída.** A célula tem `try`/`except` em volta do download e falha com mensagem
   em português: ela orienta a dupla a pedir a pasta `dados` para uma dupla vizinha que tenha o
   repositório clonado e a colocar ao lado do notebook. Confirme que existe pelo menos uma dupla
   com o repositório clonado na sala antes de começar o bloco, e diga em voz alta quem é.
3. **Pareamento.** Se nem Colab nem pasta emprestada resolverem, junte a dupla travada com a
   vizinha na mesma máquina. O produto do bloco é a leitura dos números.
4. **A aula continua sem ninguém rodando nada.** As três figuras já estão geradas em
   `assets/img/`: `aula08-escolha-de-k.png`, `aula08-plano-pc2-pc3.png` e
   `aula08-corte-custa-mape.png`. Se metade da sala travar, projete as figuras e conduza a leitura
   dos números por elas, e mande o notebook por escrito no mesmo dia com a instrução de rodar as
   seções 4 a 10 em casa.

Não gaste o bloco depurando ambiente. A dupla que ficou no Colab acompanha tudo, e quem perdeu a
execução precisa sair da sala com três números anotados: 68,21% de PC1, 96,07% com quatro
componentes e 4,94% de MAPE nesses mesmos quatro.

---

## A pergunta difícil: por que o PCA piorou o modelo?

Alguém vai perguntar, e a resposta tem três partes. Dê as três, na ordem.

**Primeiro, o custo vem do corte de componentes.** Com os 11 componentes, o MAPE é 3,32%,
idêntico ao das 11 features sem PCA até a nona casa decimal (a diferença medida é da ordem de
1e-15). A Aula 05 já havia medido que regressão linear sem regularização é invariante a
transformação afim das entradas, e PCA sem descarte é uma rotação. O que custa MAPE é jogar
componentes fora.

**Segundo, o PCA descarta pela variância, e a variância não é a medida que a regressão usa.** PC1
vale 68,21% da variância e recebe coeficiente -0,009222. PC9 vale 0,21% e recebe -0,203820, 22
vezes o de PC1. PC10 vale 0,17% e recebe 0,250588, 27 vezes o de PC1. Cortar em k=4 elimina
exatamente os dois componentes de que o modelo mais depende. A causa é estrutural: o PCA nunca vê
o alvo, então ele ordena as direções por dispersão das entradas, sem saber quais delas guardam
relação com a saída.

**Terceiro, o escopo da conclusão, que precisa ser dito com as condições na frente.** "Nesta base,
com regressão linear sem regularização, 11 features, 339 linhas mensais e alvo em razão, reduzir
por PCA custa MAPE." Não é afirmação geral sobre PCA, e o material de apoio declara isso por
escrito. Onde a redução compensa: o KNN da Aula 07, cuja distância euclidiana soma a diferença de
todas as colunas e por isso é sensível ao número delas, e o bloco de maldição de dimensionalidade
da Aula 09. A segunda pergunta do desafio do notebook manda a dupla medir esse caso com as
próprias mãos.

Se a pergunta vier como "então PCA é inútil?", devolva com a seção 7: os 12 grupos no plano PC2
por PC3 recuperam o mês em 91,7% dos 315 meses de treino, com silhueta de 0,8037 para os rótulos
verdadeiros de mês, sem que nenhuma coluna da matriz seja o número do mês. O PCA encontrou o
calendário que estava espalhado em `sen`, `cos` e `dias`. O ganho do PCA aqui é diagnóstico da
base, e o corte de componentes é o que não se sustenta neste modelo.

---

## A pergunta que abre cada bloco

### 1. Resgate e pergunta disparada (10h15-10h30, 15 minutos)

**Resgate, em uma frase:** a Aula 07 deixou pronta a base analítica mensal de 339 linhas e um
modelo que bate a baseline da LDC, regressão linear sobre 11 features com alvo em razão, MAPE de
3,32% contra 3,71%, com árvore, Random Forest e KNN medidos e perdendo.

**Pergunta disparada:** "quantas das 11 features vocês acham que são realmente independentes entre
si?"

**Resposta esperada:** a turma chuta um número entre 5 e 11, e a medição responde: 20 dos 55 pares
têm correlação absoluta acima de 0,9, o par mais correlacionado é `lag1` com `lag3` em 0,9810, e o
número de condição da matriz padronizada de treino é 28,50. As oito colunas em quilos sobem e
descem quase juntas, porque todas carregam o mesmo crescimento de longo prazo. Quatro componentes
já cobrem 96,07% da variância das onze colunas.

**O que a pergunta revela quando erra:** quem responde "11, cada uma mede uma coisa diferente"
está confundindo nome de coluna com direção de informação. `lag1`, `lag2`, `lag3` e `lag12` são a
mesma série em quatro pontos do tempo, e a correlação de 0,98 entre `lag1` e `lag3` é o que sobra
disso.

### 2. Escolha de K (10h30-10h55, 25 minutos)

O bloco tem 25 minutos e por isso quebra em dois: até 10h42 a leitura das três medidas na base de
participação, com a pergunta abaixo fechando a primeira metade, e de 10h42 a 10h55 a base de
níveis mais a decisão de K para o case, com a segunda pergunta.

**Pergunta disparada, primeira metade:** "a inércia cai sempre que K aumenta. Então por que não
escolher o maior K possível?"

**Resposta esperada:** porque a inércia com K igual ao número de pontos é zero, e um cluster por
observação não descreve nada. O Elbow Plot procura o K depois do qual a queda deixa de compensar:
25,1% de queda de K=2 para K=3, 14,3% de K=3 para K=4, e depois 12,2%, 10,6%, 7,6% e 6,5%. O
joelho está em K=3.

**O que a pergunta revela quando erra:** quem responde "escolher o K de menor inércia" tratou a
inércia como métrica de qualidade comparável entre modelos, e não como uma soma que depende do
número de centroides. É o mesmo erro de quem compara R² entre modelos com número diferente de
features.

**Pergunta disparada, segunda metade:** "o Elbow aponta K=3 e a silhueta aponta K=2. Qual dos dois
serve ao case?"

**Resposta esperada:** nenhum. Na base de participação, a concordância com o trimestre do
calendário é de 50,0% em K=2, 75,0% em K=3 e 98,3% em K=4, e a silhueta em K=4 é a pior das três,
0,2853 contra 0,3785 em K=2 e 0,3389 em K=3. O K que o Modelo 2 do TAPI precisa é 4, e os dois
critérios internos apontam para longe dele. Na base de níveis a situação piora: a silhueta é mais
alta em todo K, de 0,5639 a 0,4247, e a concordância fica entre 25,6% e 29,1%, o acaso.

**O que a pergunta revela quando erra:** quem responde "a silhueta está errada" não entendeu o que
ela mede. Ela mede separação geométrica entre clusters, e a mede corretamente: na participação no
ano, a diferença entre um pouco mais no terceiro trimestre e um pouco menos no primeiro é sutil por
natureza, porque a produção nunca desaparece num trimestre e dobra no seguinte. O erro está em
usar uma medida de separação para decidir utilidade.

### 3. PCA (10h55-11h40, 45 minutos, três sub-blocos)

Quarenta e cinco minutos não passam sem interação, então o bloco vai em três de 15, cada um com o
seu fecho. A divisão em três é interpretação da construção, e o que a `ADR-011` fixa é o total de
45 minutos com uma prática dentro.

#### 3a. Variância explicada (10h55-11h10)

**Pergunta disparada:** "o que o PCA maximiza, e o que ele nunca olha?"

**Resposta esperada:** ele procura a direção de maior variância das entradas, depois a de maior
variância ortogonal à primeira, e assim por diante. Ele nunca olha o alvo. Nesta base, PC1 vale
68,21%, PC2 11,85%, PC3 9,24% e PC4 6,77%, o que dá 80,06% em dois componentes e 96,07% em quatro.

**O que a pergunta revela quando erra:** quem responde "ele escolhe as features mais importantes"
confundiu PCA com seleção de features. Nenhuma coluna original é escolhida ou descartada: cada
componente é uma combinação linear de todas as onze, e é por isso que interpretar exige ler os
loadings.

#### 3b. Loadings e o plano PC2 por PC3 (11h10-11h25, a prática)

**Prática:** cada dupla roda a seção 4 do notebook (a célula autocontida), lê a variância
explicada, imprime os loadings de PC1, PC2 e PC3 e plota os 315 meses de treino no plano PC2 por
PC3. O plano substitui a prática do roteiro original, que pedia os trimestres no espaço dos dois
primeiros componentes: nesta base o calendário está em PC2 e PC3, não em PC1, e a mudança está
registrada nas consequências da `ADR-011`.

**Pergunta disparada:** "PC1 vale 68,21% da variância. O que ele significa em termos das colunas
originais?"

**Resposta esperada:** o nível comum das cinco séries. PC1 pesa entre 0,336 e 0,362 em cada uma
das oito colunas em quilos e no máximo 0,0196 em `sen`, `cos` e `dias`. Ele é a tendência de 28
anos que as cinco séries compartilham, e não tem nenhuma informação de sazonalidade. PC2 pesa
0,692 em `dias`, -0,619 em `sen` e -0,341 em `cos`; PC3 pesa 0,885 em `cos` e -0,432 em `sen`. O
calendário está nesses dois, que juntos valem 21,09% da variância.

**O fecho da prática:** os 12 grupos no plano PC2 por PC3 recuperam o mês em 91,7% dos 315 meses
de treino, com silhueta de 0,8037 para os rótulos verdadeiros de mês. Fevereiro fica isolado no
extremo negativo de PC2, em -2,885 contra -0,885 do segundo mais negativo, porque é o mês com 28
ou 29 dias. Peça para a dupla apontar fevereiro na figura antes de você dizer qual é.

**O que a pergunta revela quando erra:** quem responde "PC1 é o `lag1`" leu o maior loading e
parou. Os oito pesos em quilos são praticamente iguais entre si, e é essa igualdade que diz que o
componente é o nível comum, e não uma coluna específica.

#### 3c. O preço do corte (11h25-11h40)

**Pergunta disparada:** "quatro componentes retêm 96,07% da variância. Quanto custa jogar os
outros sete fora?"

**Resposta esperada:** 1,6 ponto percentual de MAPE, e a liderança sobre a baseline da LDC. O
modelo das 11 features tem 3,32%, a baseline tem 3,71%, e com quatro componentes o MAPE vai a
4,94%. Em todo k de 1 a 9 o modelo perde da baseline (4,92% em k=1 e k=2, 4,94% de k=3 a k=5,
5,12%, 4,99%, 5,17% e 6,20% até k=9), e só k=10 devolve os 3,32%.

**O que a pergunta revela quando erra:** quem responde "quase nada, são só 3,93% da variância"
tratou variância retida como informação retida. A resposta completa está nos coeficientes: PC9 e
PC10, com 0,21% e 0,17% da variância, recebem os dois maiores coeficientes da regressão, 22 e 27
vezes o de PC1.

### 4. Sistemas de recomendação (11h40-11h50, 10 minutos)

**Pergunta disparada:** "por que recomendar filme e desdobrar ração em macroingredientes são o
mesmo tipo de problema?"

**Resposta esperada:** os dois preenchem uma matriz esparsa de combinações a partir de padrões
observados em combinações parecidas. No Modelo 3 do TAPI, a matriz é ração por macroingrediente, e
o que se procura é o mix plausível dado o que se observou em situações semelhantes. Como no
K-means e no PCA, não existe rótulo dizendo qual é o mix certo: a estrutura vem da própria matriz.

**O que a pergunta revela quando erra:** quem responde "recomendação é classificação de gosto"
está procurando um alvo que não existe na formulação. E vale registrar a limitação em voz alta:
não existe série aberta de preço ou disponibilidade de macroingrediente em `dados/`, então o
Modelo 3 continua sem dado próprio no acervo, e é por isso que este bloco não tem prática. A
citação dos boletins do Sindirações saiu do roteiro por esse motivo, o mesmo que já havia tirado a
citação da Aula 04 (`ADR-004` e `ADR-007`).

### 5. ART.6 e a Sprint 3 (11h50-12h00, 10 minutos)

**Pergunta disparada:** "o que desta aula entra na entrega, se o PCA não entrou no modelo?"

**Resposta esperada:** a justificativa medida das duas decisões. K=4 na base de participação, com
98,3% de concordância com o calendário, escolhido apesar de a silhueta apontar K=2 e o Elbow
apontar K=3. E o modelo sem redução de dimensionalidade, com as 11 features e MAPE de 3,32%,
porque reduzir por PCA nesta base custa 1,6 ponto percentual e derruba o modelo para trás da
baseline da LDC. Uma decisão registrada com número medido vale na entrega tanto quanto uma técnica
aplicada.

**O que a pergunta revela quando erra:** quem responde "nada, o PCA não funcionou" acha que só
resultado positivo entra em relatório de modelagem. A tabela de MAPE por k é resultado, e é o tipo
de resultado que impede a próxima pessoa do projeto de repetir a tentativa.

**O que declarar:** a **ART.6 Preparação dos Dados e Modelagem, peso 6**, é a entrega que a matriz
do `PLANO_DE_ENSINO.md` (seção 5) amarra a esta aula, na Sprint 3, que fecha com review em 11/09,
no dia seguinte. Esta é a última aula da Sprint 3.

---

## Leituras erradas a desfazer em voz alta

**"Silhueta alta significa agrupamento melhor."** Não nesta base. Os dois agrupamentos da Aula 06
em K=4 são o contraexemplo medido: silhueta 0,4795 com 26,5% de concordância com o calendário nos
níveis, contra silhueta 0,2853 com 98,3% na participação no ano. A silhueta mede separação
geométrica e mede bem; ela só não sabe qual pergunta o case está fazendo.

**"Variância explicada mede quanta informação sobrou."** Mede dispersão das entradas. Nesta base,
99,53% da variância (os oito primeiros componentes) deixa de fora PC9 e PC10, que são os dois
componentes de que a regressão mais depende. O aluno pode guardar uma regra prática: variância
explicada é um diagnóstico da matriz de entrada, e o corte de componentes precisa ser validado
contra a métrica do problema, que aqui é o MAPE de teste.

**"O PCA fracassou na aula de hoje."** Ele respondeu duas perguntas e falhou numa terceira que não
é dele. Encontrou a redundância das 11 colunas (20 dos 55 pares acima de 0,9) e reencontrou o
calendário no plano PC2 por PC3, com 91,7% de recuperação do mês. O que ele não fez foi melhorar a
previsão de um modelo linear que já usava as onze colunas sem custo nenhum de dimensionalidade.

**"Padronizar é opcional no PCA."** Não é, quando as colunas têm unidades diferentes. Sem
padronizar, PC1 sai de 68,21% para 96,72% e seus maiores pesos passam a ser as colunas em quilos,
com `sen`, `cos` e `dias` em peso abaixo de 1e-6. O desvio-padrão de `lag1` no treino é
244.980.297 e o de `sen` é 0,708: o componente descreve a unidade de medida das colunas antes de
descrever qualquer estrutura dos dados.

**"Ajustar o escalador na base inteira não muda nada."** Muda pouco, e sempre na direção
otimista, que é o que torna o erro difícil de perceber. Medido nesta base: PC1 vai de 68,21% para
68,52% e o MAPE de k=4 vai de 4,94% para 4,91%. É a primeira pergunta do desafio do notebook, e o
gancho para o bloco de vazamento temporal da Aula 09.

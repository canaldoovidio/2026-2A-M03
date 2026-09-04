# Notas do professor: Aula 07

**04/09/2026 &middot; Aprendizado Supervisionado parte II &middot; Sprint 3**

Material de condução do encontro. O conteúdo abaixo reúne as perguntas que abrem cada bloco quando
a sala travar, cada uma com a resposta esperada e o erro que a pergunta costuma revelar. A ordem
segue os oito blocos do roteiro, registrados em `ROTEIRO-AULA07-AGORA.md` e no cabeçalho de
`aulas/aula07.html`.

**Onde está o peso desta aula:** os slides 15 a 17, o teto da árvore. A árvore de decisão
`max_depth=3` tem 8 folhas, mas os 24 meses de teste caem todos na mesma folha: ela emite um único
valor, 1.090.166.234 kg, de abril de 2024 a março de 2026, 7,77% abaixo da média real do período,
com 23 dos 24 meses acima dele. Um aluno que saia daqui sabendo rodar `DecisionTreeRegressor` e sem
saber que ela não extrapola não aprendeu o que a aula ensina. Se algum bloco tiver de encolher ao
vivo, que não seja esse, nem o bloco de H4 que devolve a árvore à disputa.

---

## Checkpoint de abertura, antes de qualquer coisa

**A pergunta que abre a sala:** quais duplas conseguiram montar a base mensal na própria máquina?
Peça o `shape`, que é `(339, ...)`. Levante a mão de quem não tem.

Quem não conseguiu não acompanha os blocos de árvore, KNN e Random Forest, e o conserto é
imediato: abrir `notebooks/aula07.ipynb` pelo badge do Colab da primeira célula. A seção 1 do
notebook lê as cinco séries de `dados/mensal/`, monta a base analítica sozinha e devolve as mesmas
339 linhas, de 1998-01 a 2026-03, sem depender de nada instalado localmente.

Registre no papel quais duplas ficaram no Colab.

---

## Ordem de corte, se o tempo apertar

1. **Random Forest, das 11h35.** É o primeiro a ceder. O achado do bloco cabe em uma frase dita em
   voz alta: a média de várias árvores tira o teto de uma árvore só, RMSE 82.070.325 e MAPE 5,35%
   contra 109.534.336 e 7,66% da árvore isolada, ainda atrás das três baselines. O material de
   apoio, seção 9, cobre o resto por escrito.
2. **O modelo do fecho, no slide 26.** Se cair, mande os dois números por escrito no mesmo dia:
   RMSE 46.724.434 e MAPE 3,32%, contra 54.523.588 e 3,71% da baseline da LDC. A turma precisa
   saber que existe um modelo que ganha da baseline antes de sair da sala.
3. **A tabela de participação na distância do KNN, nos slides 18 a 21.** Encolher para a conclusão
   sem passar pela tabela: sem padronizar, `lag1` responde por 49,2775% da distância e `lag12` por
   50,7225%, e `sen` e `cos` não pesam nada. A tabela completa fica no material de apoio, seção 7.
4. **O bloco do teto (slides 15 a 17) e o bloco de H4 não saem.** São a aula. Sem o teto, ninguém
   sai sabendo por que a árvore perdeu. Sem H4, ninguém sai sabendo que a árvore não é dispensável,
   só mal especificada para uma série com tendência.

---

## A resposta de trinta segundos sobre o autoestudo

A turma leu matriz de confusão, precisão, revocação, Naive Bayes, regressão logística e SVM para
hoje, e a aula não toca em nenhum dos seis. A resposta, se perguntarem: o case do Modelo 1 é de
regressão, prevê quilogramas de abate, não uma classe. Classificar um mês em "alta" ou "baixa"
demanda exigiria inventar um rótulo que o dado não tem, nenhuma das cinco séries de `dados/mensal/`
traz esse corte. A Aula 09 assume os quatro assuntos. A decisão está registrada na `ADR-010`.

---

## A pergunta que abre cada bloco

### 1. Resgate e H1 (10h15-10h25, slides 2 a 6)

**Pergunta disparada:** "O SIDRA só tinha o trimestre, ou a gente só olhou o trimestre?"

**Resposta esperada:** a turma abre o SIDRA em sala e acha a classificação **c12716, "Referência
temporal"**, com quatro categorias: Total do trimestre, No 1º mês, No 2º mês, No 3º mês. O mês
sempre esteve disponível, na mesma tabela.

**O que a pergunta revela quando erra:** quem responde "só tinha o trimestre" está repetindo uma
leitura da fonte que nunca foi verificada até hoje, o mesmo tipo de suposição não checada que a
Aula 06 corrigiu sobre a silhueta. H1 cai ao vivo, com a turma olhando a tabela, não com o professor
anunciando o resultado.

### 2. Base mensal (10h25-10h40, slides 7 a 8)

**Pergunta disparada:** "Por que a base mensal tem 339 linhas e não 351?"

**Resposta esperada:** as séries mensais têm 351 linhas cada (471 em ovos), de 1997-01 a 2026-03,
mas `lag12` só existe a partir do décimo terceiro mês, então os primeiros 12 meses de 1997 saem no
`dropna()`. Sobram 339 linhas, de 1998-01 a 2026-03.

**O que a pergunta revela quando erra:** quem responde "arredondamento" ou "valor ausente do
IBGE" está confundindo o corte de `lag12` com dado faltante na fonte. As cinco séries mensais não
têm nenhum valor ausente, a perda é inteiramente da engenharia de atributos.

### 3. Árvore de decisão (10h40-10h55, slides 9 a 11)

**Pergunta disparada:** "O que uma árvore de decisão captura que uma reta não captura?"

**Resposta esperada:** a árvore parte o espaço de entrada em regiões e prevê a média de cada
região, então ela captura relações não lineares e interações entre `lag1`, `lag12`, `sen` e `cos`
sem que ninguém precise especificar a forma da relação.

**O que a pergunta revela quando erra:** quem responde "ela aprende mais rápido" ou "ela é mais
precisa" está confundindo flexibilidade com desempenho, exatamente a leitura errada que o bloco de
H2 desfaz na sequência.

### 4. H2 e H3 (10h55-11h10, slides 12 a 17)

**Pergunta disparada, para abrir H2:** "Uma árvore mais flexível bate a reta simples?"

**Resposta esperada:** não. RMSE 109.534.336 e MAPE 7,66% para a árvore, contra 63.225.293 e 4,25%
da reta. A árvore perde até das baselines A e B, e fica atrás de tudo na tabela menos do KNN
padronizado.

**Pergunta disparada, para abrir H3:** "Por que uma árvore mais flexível perde de uma reta mais
simples?"

**Resposta esperada:** rodar `arvore.predict(X_teste).max()` em sala. O resultado é 1.090.166.234,
o mesmo valor nos 24 meses de teste. A árvore prevê a média da folha, a maior previsão possível é a
média da folha mais alta, e isso é um teto. Numa série com tendência de alta, o futuro fica acima
do teto: 23 dos 24 meses de teste superam esse valor, e o máximo real do teste, 1.301.022.625 em
2026-03, fica bem acima do máximo visto no treino, 1.226.709.256 em 2023-03.

**O que a pergunta revela quando erra:** quem aponta para "overfitting" ou "profundidade errada"
está procurando o erro no ajuste da árvore aos dados de treino. O problema não é ajuste, é
estrutura: nenhuma profundidade de árvore de decisão extrapola além do maior valor visto no treino,
porque toda folha prevê uma média.

### 5. KNN (11h10-11h22, slides 18 a 21)

**Pergunta disparada:** "KNN decide por semelhança. Semelhança segundo o quê?"

**Resposta esperada:** segundo a escala das features na distância euclidiana. Sem padronizar,
`lag1` responde por 49,2775% da distância e `lag12` por 50,7225%, e o KNN acha o mês mais parecido
em volume de produção, RMSE 83.496.528 e MAPE 5,62%. Padronizando, `sen` e `cos` passam a valer
tanto quanto `lag1` e `lag12`, e o KNN passa a buscar posição no calendário, RMSE 128.029.380 e
MAPE 9,37%, pior em todo k testado (k=3: 8,14% padronizado contra 5,82%; k=5: 9,37% contra 5,62%;
k=10: 10,09% contra 6,10%).

**O que a pergunta revela quando erra:** quem responde "a distância euclidiana é sempre neutra"
não fechou o ciclo da Aula 05. A distância soma as diferenças de todas as colunas com o mesmo peso,
e isso não é neutro quando as escalas diferem em ordens de grandeza.

### 6. H4 (11h22-11h35, slides 22 a 24)

**Pergunta disparada:** "Trocar o alvo de nível para razão devolve a árvore à disputa?"

**Resposta esperada:** sim, para a árvore e para o KNN sem padronizar. Treinando em `y / lag12` e
multiplicando a previsão de volta por `lag12`, a árvore cai de 7,66% para 3,86% de MAPE, e o KNN
sem padronizar cai de 5,62% para 3,71%. A reta piora, de 4,25% para 4,73%, porque a razão remove a
informação de nível que ela já usava bem.

**O que a pergunta revela quando erra:** quem conclui que "razão é sempre melhor" está generalizando
de dois casos para todos os modelos. A regressão linear piora, e isso impede exatamente essa
generalização.

### 7. Random Forest (11h35-11h45, slide 25)

**Pergunta disparada:** "Uma média de várias árvores tira o teto de uma árvore só?"

**Resposta esperada:** reduz o efeito, sem eliminar. Random Forest com 300 árvores dá RMSE
82.070.325 e MAPE 5,35% em nível, melhor que a árvore isolada (7,66%), mas ainda atrás da reta
(4,25%) e da baseline C (3,71%). Em razão, o Random Forest fica em 4,48%, atrás da árvore isolada
em razão (3,86%).

**O que a pergunta revela quando erra:** quem espera que o ensemble vença sempre a árvore isolada
não percebeu que cada árvore do Random Forest ainda prevê a média de uma folha. A média de várias
médias continua limitada pelo maior valor visto no treino, só que a limitação fica menos rígida.

### 8. ART.6 (11h45-12h00, slides 26 a 30)

**Pergunta disparada:** "Qual modelo, entre todos os medidos hoje, ganha da baseline da LDC?"

**Resposta esperada:** o modelo do fecho, regressão linear sobre a razão com onze features
(`lag1, lag2, lag3, lag12, sen, cos, dias` e as quatro séries defasadas em um mês). RMSE 46.724.434
e MAPE 3,32%, contra 54.523.588 e 3,71% da baseline C. Não é o modelo mais novo que a turma aprendeu
hoje.

**O que a pergunta revela quando erra:** quem aposta na árvore ou no Random Forest não fechou o
quadro de hipóteses da aula. Nenhum modelo de árvore, isolado ou em ensemble, bate a baseline hoje,
nem em nível nem em razão.

**O que declarar:** a **ART.6 Preparação dos Dados e Modelagem, peso 6**, é a entrega que a matriz
do `PLANO_DE_ENSINO.md` (seção 5) amarra a esta aula, na Sprint 3, com review em 11/09. O quadro de
quatro hipóteses do roteiro vira o formulário da entrega: H1 falsa (c12716 entrega 351 meses por
série), H2 falsa (7,66% contra 4,25% e 3,71%), H3 verdadeira (um único valor nos 24 meses, 23
acima dele), H4 verdadeira (7,66% cai para 3,86%).

---

## Duas leituras erradas a desfazer em voz alta

**"Árvore é modelo ruim."** Não é o veredito da aula. A árvore perde em nível porque a série tem
tendência e ela não extrapola, mas o bloco de H4 existe justamente para desfazer essa leitura: em
razão, a mesma árvore cai de 7,66% para 3,86% de MAPE, o segundo melhor MAPE em razão depois do
KNN sem padronizar (3,71%). O problema nunca foi o modelo, foi o alvo escolhido para ele.

**"Padronizar é errado."** Também não é o veredito. A regra da Aula 05 continua valendo: padronizar
iguala a influência das features na distância, e isso é o certo quando não se sabe qual delas
importa. O que a aula de hoje acrescenta é que existe um caso em que se sabe, o KNN sobre `lag1` e
`lag12` em quilogramas, e nesse caso padronizar piora o resultado em todo k testado. A decisão é
sobre quando aplicar a regra, não sobre revogá-la.

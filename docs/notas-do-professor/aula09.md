# Notas do professor: Aula 09

**15/09/2026 &middot; Problemas Comuns com Modelagem de IA e mais Feature Engineering &middot; Sprint 4**

Material de condução do encontro. O conteúdo abaixo reúne as perguntas que abrem cada bloco quando
a sala travar, cada uma com a resposta esperada e o erro que a pergunta costuma revelar. A ordem
segue os seis blocos da divisão dos 105 minutos registrada na
`docs/adrs/ADR-012-escopo-e-alvo-de-classificacao-da-aula-09.md`, e todos os números vêm de
`tools/tests/test_problemas_aula09.py`, que trava as doze conclusões da aula.

**Onde está o peso desta aula:** a tabela dos quatro modelos nos dois cortes, no bloco de
vazamento. KNN, árvore e random forest melhoram com o sorteio aleatório (7,64% para 5,29%, 8,81%
para 6,31% e 5,70% para 4,04% de MAPE), e a regressão linear sobre a razão piora, de 3,32% para
3,60%. As duas metades importam. Um aluno que saia daqui achando que sorteio sempre infla a
métrica vai tratar o corte por data como conserto de um modelo específico, e não como disciplina
de protocolo que vale antes de saber qual modelo ganha. Se algum bloco tiver de encolher ao vivo,
que não seja esse, nem a matriz de confusão do bloco de classificação.

---

## Checkpoint de abertura, antes de qualquer coisa

**A pergunta que abre a sala:** quais duplas ainda têm a base mensal das Aulas 07 e 08 rodando na
própria máquina? Peça o `shape`, que é `(339, 18)` depois do `dropna()`. Levante a mão de quem não
tem.

Quem não tem não acompanha a prática do bloco de vazamento, e o conserto é imediato: abrir
`notebooks/aula09.ipynb` pelo badge do Colab da primeira célula e rodar a seção 1, que lê as cinco
séries de `dados/mensal/`, remonta a base de 339 linhas e corta os 315 meses de treino sem depender
de nenhum outro arquivo do repositório.

Registre no papel quais duplas ficaram no Colab. É a mesma lista que vai importar na prática do
bloco de classificação, 40 minutos depois.

---

## Ordem de corte, se o tempo apertar

1. **O bloco de ausência e imputação, que já entra com 10 minutos.** É o primeiro a ceder, porque
   é demonstração e não prática. O achado cabe em duas frases ditas em voz alta: a média da série
   erra 34,53% dos valores mascarados e o mesmo mês do ano anterior corrigido pelo fator médio erra
   4,44%, porque a série cresce por 28 anos e nenhuma estatística global descreve um mês
   específico. O material de apoio cobre o resto por escrito.
2. **A varredura completa de ganho de informação, no bloco de entropia.** Encolher para quatro
   linhas: a raiz vale 0,7584 bits, `lag12` ganha 0,0632, `dias` ganha 0,0082 e `sen` ganha 0,0043.
   O contraste entre o campeão e os dois candidatos de calendário é o que sustenta o bloco; a
   tabela das onze features é conforto, não conteúdo.
3. **O corte degenerado `dias <= 31`.** Encolher para a frase: um limiar acima do máximo da coluna
   deixa os 315 meses do mesmo lado, e um nó que não parte a amostra não tem ganho a medir. Vale
   dizer mesmo sem projetar a tabela, porque é a explicação de por que a varredura só considera
   pontos médios entre valores distintos.
4. **Domain knowledge cai de 5 para 3 minutos**, mantendo a tabela das quatro decisões de feature
   deste acervo e o apontamento dos autoestudos Netflix e Airbnb. Ele não sai: são três autoestudos
   da semana, e a turma vai perguntar.
5. **A tabela dos dois cortes e a matriz de confusão não saem.** São a aula. Sem a primeira,
   ninguém sai sabendo que o erro de protocolo melhora a métrica; sem a segunda, a turma sai
   achando que 83,3% de acurácia é um bom resultado.

---

## A resposta de trinta segundos sobre o autoestudo

A turma leu, para hoje, nove autoestudos, e dois deles são de PCA: "PCA - Resolvendo o problema da
dimensionalidade" e "PCA: o que é e como usar em Python". A Aula 08 ensinou PCA em 10/09, cinco
dias antes desta leitura, e alguém vai notar.

**O descompasso, dito sem rodeio se perguntarem.** A Semana 07 tem dezenove autoestudos e dois
Encontros de Instrução, hoje e 17/09, com uma lista única. Os dois itens de PCA chegam depois do
encontro que ensinou PCA, e servem de revisão: o resgate de abertura de hoje usa exatamente os
números daquele encontro (PC1 com 68,21% da variância, quatro componentes com 96,07%, e o corte
levando o MAPE de 3,32% para 4,94%). A página de referências da Aula 08 já registra o outro lado do
mesmo descompasso, porque os cinco autoestudos daquela semana eram todos de sistemas de
recomendação.

**Se perguntarem por curva ROC e AUC**, que também são autoestudo desta semana: eles ficam para a
Aula 10, em 17/09, junto com GridSearch, validação cruzada e SHAP. A decisão está na `ADR-012`, e o
motivo é honesto: esta aula já entra com onze assuntos em 105 minutos, e a dívida de tempo se
desloca em vez de desaparecer.

---

## Se a prática de vazamento falhar no ambiente da dupla

Três falhas prováveis, com o conserto de cada uma:

- **`train_test_split` devolvendo tamanho errado.** `test_size=24/339` é fração, não contagem. Se a
  dupla escrever `test_size=24`, o scikit-learn interpreta como número absoluto e o resultado ainda
  é 24, mas se escrever `test_size=0.24` o teste vai a 81 meses e nada compara com nada. Peça o
  `len` dos dois conjuntos antes de qualquer métrica.
- **MAPE calculado com o alvo em razão contra o real em nível.** O modelo do fecho da Aula 07 prevê
  `y / lag12`, e a previsão precisa ser multiplicada de volta por `lag12` antes de comparar com o
  abate em quilogramas. Sem isso o MAPE vira algo próximo de 100%.
- **Sorteio com uma semente só.** Uma semente isolada pode dar 20 de 24 meses com vizinho, em vez
  de 24 de 24. A célula do notebook roda dez sementes e reporta a média, e a leitura da aula é
  sobre a média, não sobre um sorteio específico.

---

## A pergunta difícil: por que criar um alvo que não é do TAPI?

Vai aparecer, e a resposta precisa ser direta: **porque os seis assuntos de classificação desta
aula precisam de um alvo categórico, e os três modelos do TAPI preveem quantidade.** Sem alvo
categórico, matriz de confusão, precisão, revocação, Naive Bayes, regressão logística e SVM não têm
sobre o que rodar. Inventar uma base de classificação seria dado sintético, que o acervo proíbe
onde existe dado aberto real.

O alvo escolhido, "o abate do mês supera o mesmo mês do ano anterior", usa uma coluna que a base já
tinha (`lag12`), não inventa valor nenhum e é desbalanceado por característica do fenômeno, com
78,1% de positivos no treino. Ele é o exemplo mais direto que as cinco séries permitem.

**O que precisa ficar dito na mesma frase:** é a primeira vez no acervo que um alvo não vem do
TAPI, os três modelos do case seguem sendo de regressão, e a ART.7 compara modelos de regressão.
Uma dupla que entregar classificação na ART.7 por causa desta aula terá entendido o exemplo como se
fosse o case.

---

## A pergunta que abre cada bloco

### 1. Resgate e pergunta disparada (10h15-10h25, 10 minutos)

**Pergunta:** o que aconteceria com o MAPE se separássemos treino e teste por sorteio aleatório
nesta base?

**Resposta esperada:** que ele melhoraria, porque o modelo passaria a ver meses vizinhos dos meses
de teste. Poucas duplas chegam a isso sozinhas; a maioria responde "não mudaria nada" ou "pioraria,
porque o teste fica mais difícil".

**O erro que a pergunta revela:** tratar as linhas da base como observações independentes. Elas não
são: o mês seguinte parece muito com o anterior, e é isso que o sorteio entrega de graça ao modelo.

**Se travar:** volte ao gancho da Aula 08. Ajustar escalador e PCA na base inteira levou PC1 de
68,21% para 68,52% e o MAPE de quatro componentes de 4,94% para 4,91%. Pergunte: em que direção o
erro de protocolo empurrou a métrica? Sempre para melhor. É o que torna esse tipo de erro difícil
de perceber.

### 2. Vazamento temporal (10h25-10h50, 25 minutos)

**Pergunta:** o RMSE do KNN cai de 104.945.482 para 48.382.751 com o sorteio. Isso é vazamento?

**Resposta esperada:** só em parte. O alvo médio do teste sorteado é 765.719.266 kg contra
1.181.946.133 kg do teste por data, 35% menor, e o RMSE está em quilogramas. Parte da queda é
escala do período, e é por isso que a leitura usa MAPE.

**O erro que a pergunta revela:** comparar métrica dependente de escala entre conjuntos de teste
diferentes. É o mesmo tipo de erro que a aula inteira trata, e ele aparece justamente na ferramenta
de diagnóstico.

**Fecho do bloco, na prática da dupla:** contar quantos meses de teste têm vizinho no treino em
cada corte. Um de 24 no corte por data, 24 de 24 nas duas primeiras sementes de sorteio. É o
mecanismo inteiro, sem estatística nenhuma.

**Se sobrar tempo:** peça para alguém explicar por que a regressão sobre a razão piora com o
sorteio. A resposta é que ela não guarda observação nenhuma, então não ganha nada com vizinhos, e
ainda troca um teste concentrado no regime recente por um teste espalhado por 28 anos.

### 3. Classificação, matriz de confusão e desbalanceamento (10h50-11h20, 30 minutos)

**Pergunta:** a árvore de entropia acerta 83,3% dos 24 meses de teste. Isso é bom?

**Resposta esperada:** não dá para saber pela acurácia. A baseline que responde "cresce" sempre
também acerta 83,3%, com precisão 0,833 e revocação 1,000, e a árvore repete as quatro métricas
dela porque prevê alta nos 24 meses.

**O erro que a pergunta revela:** ler acurácia sem baseline declarada. Em alvo desbalanceado, a
acurácia da classe majoritária é o piso, não o resultado.

**O momento da matriz de confusão:** projete a da regressão logística (2 e 2 na linha de queda, 3 e
17 na de alta). Ela é a que arrisca mais quedas, acerta duas das quatro e paga com três altas
classificadas como queda, o que a leva a 79,2%, abaixo da baseline. Pergunte qual dos dois erros
custa mais para a LDC: ração parada em silo ou cliente sem entrega. Não existe resposta única, e é
esse o ponto.

**Se alguém perguntar do Naive Bayes:** ele prevê queda nos 24 meses e termina com 16,7% de
acurácia e zero de precisão e revocação na classe positiva. A suposição de independência entre as
features está contradita pela própria base, onde 20 dos 55 pares passam de 0,9 de correlação
absoluta, medido na Aula 08.

### 4. Entropia passo a passo (11h20-11h35, 15 minutos)

**Pergunta:** por que o corte `dias <= 31` tem ganho zero?

**Resposta esperada:** porque `dias` vai no máximo a 31, então o corte deixa os 315 meses do mesmo
lado. Um nó que não parte a amostra tem a entropia do pai como entropia do filho.

**O erro que a pergunta revela:** achar que a árvore testa qualquer número. Ela varre os pontos
médios entre valores distintos e consecutivos, e um limiar fora do intervalo da coluna não é
candidato.

**A conta que precisa aparecer na lousa:** a raiz, com 246 positivos em 315 meses, vale 0,7584
bits. O corte `lag12 <= 737.169.694` deixa 144 meses de um lado, com 0,4374 bits, e 171 do outro,
com 0,9123 bits, o que dá 0,0632 bits de ganho. A árvore com `criterion="entropy"` escolhe esse
mesmo corte, com dois quilogramas de diferença no limiar.

**A pergunta de fecho:** por que o lado de abate baixo há um ano é o mais previsível? Porque reúne
os anos mais antigos, quando o crescimento anual era mais consistente. O lado direito, com os anos
recentes, fica quase meio a meio entre alta e queda.

### 5. Ausência e imputação (11h35-11h45, 10 minutos, demonstração)

**Pergunta:** quantos valores vazios existem nos CSVs do acervo?

**Resposta esperada:** nenhum. A ausência é de período: a união das cinco séries mensais tem 471
meses, a interseção tem 351, e a junção interna descarta 120 meses, 25,5% da união, porque
`producao_ovos` começa dez anos antes das outras quatro.

**O erro que a pergunta revela:** procurar `NaN` e concluir que não há problema de dado ausente. A
matriz período por série tem 480 células vazias em 2.355, 20,4%, e a decisão de descartar dez anos
de ovos é de modelagem, não de limpeza.

**A demonstração, com os números na tela:** 16 meses do treino mascarados com semente 42, e as
cinco estratégias medidas contra o valor escondido. Média 34,53%, mediana 34,38%, último valor
7,60%, interpolação linear 7,27% e mesmo mês do ano anterior com fator 1,05378 em 4,44%. O que se
afirma é a ordem e a razão dela, não o valor exato: a série cresce por 28 anos, então qualquer
estatística global do histórico erra muito.

### 6. Dimensionalidade, domain knowledge e ART.7 (11h45-12h00, 15 minutos)

**Pergunta:** acrescentar features melhora ou piora o modelo?

**Resposta esperada:** depende da família. Indo de 2 para 11 features, a distância euclidiana média
entre meses de treino cresce de 1,65 para 4,31, o KNN piora de 3,71% para 5,01% e a regressão
linear melhora de 4,71% para 3,32%.

**O erro que a pergunta revela:** procurar uma regra geral onde existe uma dependência. O que
cresce sempre é a distância média; os dois modelos reagem em direções opostas ao mesmo
crescimento.

**Domain knowledge, em três minutos:** a tabela das quatro decisões de feature deste acervo (alvo
em razão, leite fora da base, horizonte de 24 meses, granularidade mensal), cada uma com o
conhecimento de domínio que a motivou. O exercício em dupla é apontar uma decisão equivalente no
projeto da própria dupla.

**Amarração, com o peso citado da fonte:** ART.7 Comparação de modelos, peso 8, na Sprint 4, com
planning em 14/09 e review em 25/09, conforme a seção 4 do `PLANO_DE_ENSINO.md`. O que a aula
entrega é o protocolo da comparação: mesmo corte por data em todo candidato, baseline declarada,
métrica sem dependência de escala, estratégia de imputação medida e número de features declarado
junto com a família de modelo.

---

## Leituras erradas a desfazer em voz alta

1. **"Sorteio aleatório sempre infla a métrica."** Não nesta base: a regressão linear sobre a razão
   piora, de 3,32% para 3,60%. O que a aula ensina é protocolo, e protocolo vale antes de saber
   qual modelo vai ganhar.

2. **"O RMSE prova o vazamento."** O RMSE cai no sorteio em parte porque o teste sorteado é 35%
   menor em escala. Quem quiser medir vazamento entre conjuntos de períodos diferentes precisa de
   métrica que não dependa de escala.

3. **"Nenhum classificador supera a baseline, então classificação não serve para o case."** A
   conclusão é sobre a métrica, e o teste tem 24 linhas. O que a aula mede é que acurácia sozinha
   não distingue um modelo que decide de um que responde sempre a mesma coisa.

4. **"O alvo binário é o novo alvo do projeto."** Ele existe para ensinar métrica de classificação
   sobre dado real. Os três modelos do TAPI preveem quantidade, e a ART.7 compara modelos de
   regressão.

5. **"A interpolação linear é sempre uma boa imputação."** Ela erra 7,27% neste mascaramento porque
   os meses escondidos foram sorteados e quase sempre têm vizinho medido. Com uma lacuna contígua,
   ela perde os vizinhos e passa a errar como a média.

6. **"Menos features é melhor, porque a distância cresce."** A regressão linear melhora com as onze
   features, e é ela o modelo do fecho da Aula 07. A tabela mostra uma dependência, não uma regra.

7. **"`lag12` é o melhor corte da árvore."** É o melhor corte **da raiz**, medido nos 315 meses de
   treino. Abaixo dela a árvore escolhe outros cortes, e a aula não percorre a árvore inteira.

# Notas do professor: Aula 11

**24/09/2026 &middot; AutoML com PyCaret &middot; Sprint 4**

Material de condução do encontro. O conteúdo abaixo reúne as perguntas que abrem cada bloco quando
a sala travar, cada uma com a resposta esperada e o erro que a pergunta costuma revelar. A ordem
segue os sete blocos da divisão dos 105 minutos registrada na
`docs/adrs/ADR-014-pycaret-4-alpha-e-escopo-da-aula-11.md`, e todos os números vêm de
`tools/tests/test_automl_aula11.py`, que trava as nove conclusões da aula.

**Onde está o peso desta aula:** o slide 19, com as duas linhas do alvo. Para o modelo linear o alvo
em razão custa 0,46 ponto; para a floresta ele vale 1,46 ponto. As duas linhas dizem coisas opostas
e as duas estão certas, e é isso que a turma precisa levar. Um aluno que saia daqui achando que "o
alvo em razão era errado" aprendeu a coisa errada e vai jogar fora a decisão certa da Aula 07. O que
ele precisa levar é que a decisão saiu do caso em que foi tomada.

**Esta aula fecha a Sprint 4, e a ART.7 é amanhã.** O bloco de amarração não é protocolar: a turma
entrega em 25/09, e o slide 24 é o checklist do que precisa estar no relatório.

---

## Checkpoint de abertura, antes de qualquer coisa

**A pergunta que abre a sala:** quem conseguiu instalar o PyCaret?

Esta é a checagem mais importante do módulo inteiro, e por isso ela vem antes de tudo. A célula de
instalação de `notebooks/aula11.ipynb` fixa a versão exata (`pycaret==4.0.0a8`) e leva alguns
minutos na primeira vez, porque arrasta `lightgbm`, `numba` e `llvmlite`. **Mande instalar no
começo**, não às 10h45: vinte máquinas baixando isso ao mesmo tempo, no wi-fi da sala, é o tipo de
coisa que come um bloco inteiro.

Se alguma dupla falhar, o conserto é o Colab, pelo badge da primeira célula. Registre no papel quais
duplas ficaram no Colab; é a mesma lista que vai importar na prática das 11h15.

**A segunda pergunta, se sobrar tempo no checkpoint:** cada dupla traz do daily a feature mais
influente encontrada via SHAP na Aula 10. Peça duas ou três em voz alta e confira se elas declararam
qual leitura usaram. Quem não declarou acabou de ilustrar o item 4 do checklist da ART.7.

---

## Ordem de corte, se o tempo apertar

1. **O slide 14, da ordem do leaderboard.** É o primeiro a ceder, porque cabe em uma frase dita em
   voz alta apontando para a tabela do slide anterior: o leaderboard vem ordenado por R2, e a quarta
   linha tem MAPE maior que a quinta. O material de apoio cobre o resto.
2. **O slide 9, do que o `compare_models` não decide, encolhe para as três últimas linhas.** As duas
   primeiras (família e hiperparâmetro) a turma já entende do autoestudo; as três últimas (alvo,
   validação, features) são o conteúdo.
3. **A segunda metade da prática 2 sai**, ou seja, repetir o exercício para o Modelo 2 ou 3. O que
   não pode sair é a comparação entre estimado e medido nas duas configurações, que é o ponto do
   bloco.
4. **O slide 7, da tabela de conversão de API, vira dois minutos de tela**, sem discussão. A dupla
   precisa da tabela para rodar o notebook, não de um debate sobre versionamento.
5. **Os slides 19 e 21 não saem.** São a aula. Sem o 19, o achado do alvo não acontece; sem o 21, a
   turma sai achando que as quatro aulas anteriores foram perda de tempo.

---

## A resposta de trinta segundos sobre o autoestudo

A turma leu cinco autoestudos de PyCaret, e todos ensinam `setup()`. A aula usa
`RegressionExperiment().fit()`. Alguém vai perguntar na primeira prática, se não antes.

**A resposta, sem rodeio:** a versão estável do PyCaret recusa o Python 3.12 na importação, com uma
checagem explícita dentro do pacote, e instalá-la rebaixaria `scikit-learn`, `numpy` e `pandas` para
versões anteriores às dos outros dez notebooks do acervo. A linha 4.0 roda no Python atual sem mexer
em nada. A tabela de conversão está no slide 7 e tem três linhas.

**E o aproveitamento pedagógico, que é melhor que a desculpa:** isto é o item 3 do checklist da
ART.7. A versão da biblioteca faz parte da descrição do experimento. Um relatório que diga "usamos
PyCaret" sem dizer qual versão não é reproduzível, e neste caso específico a diferença entre as duas
versões é o próprio Python em que elas rodam.

---

## A pergunta difícil: então as Aulas 07 a 10 foram perdidas?

Ela vai ser feita, provavelmente no slide 19, e merece resposta preparada. É a pergunta mais
perigosa desta aula, porque a resposta errada desmonta a sprint inteira na cabeça da turma.

**A resposta curta:** o leaderboard que vocês veem primeiro estima 3,63%, e o modelo erra 2,81% de
verdade. Esse 3,63% não corresponde a nada: saiu de 220 meses sorteados e de um validador que treina
com o futuro. Quem sabe disso são vocês, por causa das Aulas 09 e 10.

**A resposta longa, se insistirem.** Três pontos:

1. **O número da tela estava errado, e por sorte para o lado pessimista.** Dessa vez a dupla teria
   sorte. No bloco de vazamento da Aula 09, o mesmo tipo de erro empurrava a métrica para o lado
   otimista, que é o lado que não dispara alarme. Não há garantia de direção.
2. **O AutoML ordena candidatos e não audita a ordenação.** Ele não sabe que o dado é uma série, não
   sabe que o R2 não é comparável entre os dois alvos, e não tem opinião sobre qual alvo usar. Todas
   essas três perguntas foram respondidas nas aulas anteriores.
3. **O que o AutoML fez, vocês poderiam ter feito à mão.** Rodar uma regressão linear sobre o alvo em
   nível é uma linha de código. Ninguém rodou porque a decisão de alvo estava fechada desde a Aula
   07. O valor do comparador é ele não ter memória nem apego.

**O que não fazer:** não minimizar o resultado, não dizer que 2,81% "é quase igual" a 4,21%, e não
prometer que o modelo ajustado à mão vai ganhar na entrega. Ele não ganha.

---

## Se o compare_models demorar demais na máquina da dupla

Medido na construção da aula, sobre os 315 meses de treino: **poucos segundos por rodada**, entre 3
e 7, com 22 candidatos. Se alguma dupla estiver em minutos, três causas prováveis, nesta ordem:

1. **A primeira rodada inclui o aquecimento das bibliotecas.** A segunda é mais rápida. Peça para
   rodar de novo antes de investigar.
2. **O `n_jobs` do construtor está em 1.** O default é -1, mas alguém pode ter mexido.
3. **A base cresceu.** Se a dupla passou as 339 linhas em vez das 315 de treino, o PyCaret está
   usando o conjunto de teste, e o problema é maior que o tempo: é o erro de protocolo que a Aula 09
   inteira tratou. Aproveite para mostrar à sala.

---

## A pergunta que abre cada bloco

### 1. O quadro de referência (10h15-10h30, 15 minutos)

**Pergunta:** vocês acham que o AutoML vai bater o modelo que vocês ajustaram à mão? E se bater, o
que exatamente ele terá feito de diferente?

**Resposta esperada:** a maioria responde que sim para a primeira parte, por confiança na
ferramenta, e trava na segunda. A segunda parte é a que interessa, e é para ela que a aula caminha.

**O erro que a pergunta revela:** achar que "melhor modelo" é uma propriedade do algoritmo, e não do
conjunto de decisões que cercam o algoritmo.

**O momento de virar a chave:** a figura do slide 4. A floresta que a Aula 10 ajustou é a **pior**
das quatro referências, e perde para a baseline que a LDC já usava. Deixe o silêncio acontecer antes
de explicar.

**Se travar:** pergunte o que um `GridSearchCV` pode e não pode mudar. Ele muda profundidade, número
de árvores, tamanho de folha. Ele não muda a família nem o alvo. A partir daí a sala chega sozinha.

### 2. O que o compare_models faz (10h30-10h45, 15 minutos)

**Pergunta:** o que exatamente vocês esperam que um comparador automático automatize?

**Resposta esperada:** "escolher o melhor modelo". Quase ninguém separa espontaneamente as camadas:
família, hiperparâmetro, alvo, validação e features.

**O erro que a pergunta revela:** tratar "o modelo" como uma coisa só. A tabela do slide 9 existe
para quebrar isso em cinco decisões com donos diferentes.

**O momento de virar a chave:** os oito primeiros colocados do leaderboard são lineares, e nenhum é
árvore. O comparador não ajustou hiperparâmetro nenhum: ele treinou cada família com os valores
padrão dela.

### 3. Prática: o leaderboard do Modelo 1 (10h45-11h00, 15 minutos)

**O que cobrar ao circular pela sala:** que a dupla anote o campeão, o MAPE estimado e o tempo. E que
rode `len(exp.X_train)`, que é o gancho do bloco seguinte.

**A pergunta a plantar em quem terminar cedo:** vocês entregaram 315 meses. Quantos ele usou?

### 4. Ler o leaderboard sem se enganar (11h00-11h15, 15 minutos)

**Pergunta:** o R2 do mesmo leaderboard vale 0,977 com o alvo em nível e 0,483 com o alvo em razão.
O modelo piorou pela metade?

**Resposta esperada:** boa parte da sala responde que sim, ou hesita. É o resultado esperado da
pergunta, e é por isso que ela abre o bloco.

**O erro que a pergunta revela:** ler R2 como nota de qualidade absoluta, em vez de fração da
variância do alvo.

**O momento de virar a chave:** o MAPE dos mesmos modelos fica em 3,63% e 3,73%. Se o modelo tivesse
piorado pela metade, o erro relativo teria subido junto. Amarre com a Aula 09: é o mesmo problema do
RMSE entre conjuntos de escalas diferentes.

**A consequência prática, que fecha o bloco:** o leaderboard vem ordenado por R2, e a quarta linha
tem MAPE maior que a quinta.

### 5. Prática: consertar o protocolo (11h15-11h30, 15 minutos)

**O que cobrar:** que a dupla passe `fold_strategy=TimeSeriesSplit(n_splits=5)` e
`train_size=0.99`, e compare a diferença entre estimado e medido nas duas configurações.

**A pergunta que fecha:** qual das duas estimativas chegou mais perto do teste? E isso é argumento a
favor de qual protocolo?

**Cuidado ao circular:** alguém vai dizer que o MAPE de teste piorou com o fold temporal (3,34%
contra 3,26%). Está certo, e é a mesma situação do slide 21 da Aula 10: a diferença é ruído, e o que
se ganha é a estimativa.

### 6. O achado do alvo (11h30-11h45, 15 minutos)

**Pergunta:** o AutoML bateu. O que ele fez que vocês não fizeram?

**Resposta esperada:** "testou mais modelos". Está certo, mas incompleto, e a tabela do slide 19
completa: ao testar a família linear, ele pôde testar também o alvo em nível, que nenhum modelo do
acervo usava desde a Aula 07.

**O erro que a pergunta revela:** achar que trocar de família é uma decisão isolada. Famílias
diferentes têm necessidades diferentes de preparação de dado, e é isso que amarra alvo e família.

**O momento de virar a chave, e é o mais importante da aula:** a segunda linha da tabela. Para a
floresta, o alvo em razão continua melhor, e por muito, 4,21% contra 5,67%. **A decisão da Aula 07
não estava errada.** Ela estava sendo aplicada fora do caso em que foi tomada.

**Se sobrar tempo:** pergunte que outras decisões do acervo foram tomadas por causa de um modelo
específico e ficaram valendo para todos. A resposta que a turma deve alcançar é a escolha das onze
features, que veio da Aula 09 e nunca foi reaberta. É o gancho da Aula 12.

### 7. Quiz e amarração com a ART.7 (11h45-12h00, 15 minutos)

Os dois quizzes cobrem o que mais escorrega: o R2 que despenca sem o modelo piorar, e de onde veio
o ganho do AutoML.

**A amarração, dita em voz alta:** a ART.7 é amanhã. O melhor candidato do acervo é um modelo linear
sobre o alvo em nível, e não a floresta que duas aulas ajustaram. O relatório precisa declarar, para
cada candidato: a família, o alvo, o protocolo de validação, a grade buscada e a versão da
biblioteca.

**O que vai para a Aula 12:** o campeão linear é o que entra no `Pipeline` do scikit-learn e no
MLflow, e a decisão de alvo entra no pipeline junto com ele, para não se perder de novo.

---

## Leituras erradas a desfazer em voz alta

1. **"O alvo em razão era errado."** Não era. Para a floresta ele vale 1,46 ponto percentual, e foi
   por isso que a Aula 07 o escolheu. Ele custa 0,46 ponto para o modelo linear, que não precisa da
   proteção que ele oferece.

2. **"As Aulas 07 a 10 foram perda de tempo."** Sem elas, a dupla aceitaria o 3,63% que o leaderboard
   estima com os defaults ligados, e entregaria à LDC uma estimativa que não corresponde a nada.

3. **"O AutoML ajustou melhor os hiperparâmetros."** Ele não ajustou nenhum no `compare_models`:
   treinou cada família com os valores padrão dela. Quem ajustou hiperparâmetro foi a Aula 10.

4. **"O modelo em nível é duas vezes melhor, o R2 diz."** O R2 não é comparável entre alvos de
   variâncias diferentes. Ele é melhor por 0,46 ponto de MAPE, que é a métrica que atravessa a
   troca.

5. **"O PyCaret tem um defeito de validação."** O default dele é correto para dado tabular sem
   ordem, que é o caso da maior parte de quem usa a biblioteca. Nada no `DataFrame` diz que este
   dado é uma série temporal. Declarar o protocolo é de quem conhece o dado.

6. **"Então é só rodar `compare_models` na ART.7."** É só rodar, e depois responder às quatro
   perguntas que ele não responde: qual alvo, qual validação, quais features e se a ordenação da
   tela é confiável.

7. **"O fold temporal deu um modelo pior."** Deu um MAPE de teste 0,08 ponto maior, com o mesmo
   campeão. O que ele deu de melhor foi a estimativa, que passou a errar 0,17 em vez de 0,47.

8. **"Achamos o melhor modelo possível."** Achamos o melhor entre 22 famílias, com onze features
   fixadas desde a Aula 09 e dois alvos testados. A escolha de feature nunca foi reaberta, e é o
   próximo candidato ao mesmo tipo de reexame.

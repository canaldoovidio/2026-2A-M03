# Notas do professor: Aula 10

**17/09/2026 &middot; Hiperparâmetros e Explicabilidade do Modelo &middot; Sprint 4**

Material de condução do encontro. O conteúdo abaixo reúne as perguntas que abrem cada bloco quando
a sala travar, cada uma com a resposta esperada e o erro que a pergunta costuma revelar. A ordem
segue os cinco blocos da divisão dos 105 minutos registrada na
`docs/adrs/ADR-013-escopo-e-base-de-ajuste-da-aula-10.md`, e todos os números vêm de
`tools/tests/test_ajuste_aula10.py`, que trava as treze conclusões da aula.

**Onde está o peso desta aula:** o slide 21, com as quatro linhas do `KFold` contra o
`TimeSeriesSplit`. Com onze features o `KFold` termina 0,08 ponto à frente no teste; com quatro,
0,04 atrás. É o slide mais difícil de conduzir do acervo até aqui, porque o número contraria o que
a aula quer ensinar, e é justamente por isso que ele fica. Um aluno que saia daqui achando que
`TimeSeriesSplit` "dá um modelo melhor" aprendeu a coisa errada e vai abandonar a prática assim que
o número não confirmar. O que ele precisa levar é que a estimativa do `KFold` responde a uma
pergunta que ninguém vai fazer. Se algum bloco tiver de encolher ao vivo, que não seja esse.

**Esta aula não tem bloco de resgate separado.** É a primeira do acervo assim, e é decisão
registrada na `ADR-013`: os quinze minutos de abertura desfazem o empate que a Aula 09 deixou, e
com isso o resgate e o primeiro conteúdo novo são a mesma coisa. Quem estiver acostumado com a
anatomia das nove aulas anteriores vai sentir falta do bloco, e ele não está faltando.

---

## Checkpoint de abertura, antes de qualquer coisa

**A pergunta que abre a sala:** quais duplas conseguiram rodar `import shap` na própria máquina?
Peça para levantar a mão.

O `shap` é a única dependência nova do módulo inteiro, e é a mais pesada. Quem não tiver não
acompanha a prática do quarto bloco. O conserto está na primeira célula de
`notebooks/aula10.ipynb`, que instala o pacote com mensagem em português quando ele não está
presente, e leva cerca de um minuto. **Mande instalar agora**, no começo da aula, não às 11h30:
rodar `pip install` em vinte máquinas ao mesmo tempo, com o wi-fi da sala, é o tipo de coisa que
come dez minutos de um bloco de vinte.

Segunda checagem, mais rápida: quem tem a base mensal das Aulas 07 a 09 rodando? O `shape` é
`(339, 18)` depois do `dropna()`. Quem não tem abre o notebook pelo badge do Colab e roda a seção 1.

---

## Ordem de corte, se o tempo apertar

1. **O RandomSearch, no segundo bloco.** É o primeiro a ceder, porque o achado cabe em duas frases:
   nove sorteios das 27 combinações chegam na mesma escolha, com 45 treinos em vez de 135, porque
   das três dimensões da grade só duas movem o erro. O material de apoio cobre o resto, e o
   autoestudo "Exemplo II: GridSearch e RandomSearch" já traz o argumento.
2. **A tabela de acurácia contra AUC dos seis modelos (slide 6) encolhe para três linhas.**
   Baseline, árvore e SVM RBF bastam para o argumento. As linhas da logística e do Naive Bayes são
   a segunda camada, e a logística dá para mencionar em voz alta: pior acurácia entre as que não
   desabam, melhor AUC das cinco.
3. **O partial dependence (slide 28) vira demonstração de dois minutos**, mantendo a frase de
   negócio: 9,3% de crescimento previsto na base pequena contra 1,0% na base grande, e a floresta
   aprendeu isso sem ninguém programar. A prática 4 continua pedindo a curva, e a dupla faz fora de
   sala se precisar.
4. **A tabela dobra a dobra (slide 20) sai, se a figura das dobras (slide 19) já tiver passado.**
   A figura é mais forte que a tabela, e as duas dizem a mesma coisa. Nunca corte as duas.
5. **O slide 21 e o slide 22 não saem.** São a aula. Sem o 21, ninguém vê que o número contraria a
   expectativa; sem o 22, a turma sai achando que o `KFold` é aceitável.

---

## A resposta de trinta segundos sobre o autoestudo

A turma leu dez autoestudos para hoje, e dois deles são de curva ROC: "Curva ROC e AUC" e
"Opcional: ROC e AUC na prática". Alguém pode perguntar por que eles não foram usados na aula
passada, que foi a de classificação.

**A resposta, sem rodeio:** a Semana 07 tem dezenove autoestudos e dois Encontros de Instrução, com
uma lista única. A Aula 09 entrou com onze assuntos em 105 minutos, e a `ADR-012` registrou que ROC
e AUC ficariam para hoje. Hoje eles abrem a aula, sobre o resultado que a Aula 09 mediu e não
conseguiu ler. Quem quiser conferir a contagem: nove itens em `referencias/aula09.html` e dez em
`referencias/aula10.html`.

Se alguém perguntar por que não foi o contrário, com ROC na Aula 09 e alguma outra coisa aqui: a
resposta honesta é que a Aula 09 precisava do empate medido para que a AUC tivesse sobre o que
falar. A ordem funciona melhor assim do que funcionaria junta.

---

## Se a busca em grade demorar demais na máquina da dupla

A grade de 27 combinações com `TimeSeriesSplit(5)` são 135 treinos. Medido na construção da aula:
**9 segundos com `n_jobs=-1` e 19 segundos em um único núcleo**, porque a base tem só 315 linhas de
treino.

Se alguma dupla estiver em minutos em vez de segundos, três causas prováveis, nesta ordem:

1. **`n_jobs` não foi passado.** O default é 1. Mandar `n_jobs=-1`.
2. **A grade cresceu.** Alguém acrescentou `max_features` ou `min_samples_split` e não percebeu que
   o número de treinos é o produto, não a soma. Voltar para três hiperparâmetros.
3. **O modelo não é a floresta.** Um `SVC` ou um `GradientBoosting` com a mesma grade custa muito
   mais. Nesse caso, reduzir `n_splits` para 3 antes de reduzir a grade: perde-se precisão da
   estimativa, não a estrutura do exercício.

---

## A pergunta difícil: se o KFold ganhou, por que trocar?

Ela vai ser feita, provavelmente no slide 21, e merece resposta preparada.

**A resposta curta:** porque o número do `KFold` não responde a nenhuma pergunta que a LDC vá fazer.
Quando ele estima 6,03%, essa estimativa saiu de um procedimento em que o modelo estudou 2024 para
ser cobrado sobre 1998. Nenhum modelo em produção terá esse privilégio.

**A resposta longa, se insistirem.** Três pontos, nesta ordem:

1. **A vantagem troca de sinal.** Com onze features o `KFold` ganha 0,08; com quatro, perde 0,04.
   Uma vantagem que depende do conjunto de features não é vantagem do validador, é ruído de um teste
   de 24 meses.
2. **Os dois escolhem a mesma poda.** `max_depth=4` e `min_samples_leaf=5` nos quatro casos. A única
   diferença é o número de árvores, que a tabela do slide 14 já mostrou ser a dimensão que quase não
   importa. O vazamento do `KFold` não mudou a decisão relevante nesta base, e não há garantia de
   que não mude na próxima.
3. **É o mesmo argumento da Aula 09.** Lá, a regressão sobre a razão não melhorava com o sorteio
   aleatório, e o corte por data virou regra mesmo assim. Regra de protocolo vale antes de saber
   quem vai ganhar. Escolher o validador depois de ver o resultado é a mesma armadilha de escolher a
   combinação de hiperparâmetros pela métrica de teste.

**O que não fazer:** não esconder o número, não dizer que a diferença "não importa" sem dizer que
ela troca de sinal, e não prometer que o `TimeSeriesSplit` vai dar um modelo melhor na ART.7. Ele
pode não dar.

---

## A pergunta que abre cada bloco

### 1. Curva ROC e AUC (10h15-10h30, 15 minutos)

**Pergunta:** se dois modelos acertam a mesma quantidade de meses, o que ainda pode diferenciar um
do outro?

**Resposta esperada:** a confiança com que cada um acerta, ou a ordem em que eles colocariam os
meses. A maioria responde "nada" ou parte para "o mais simples é melhor", que é resposta de outro
assunto.

**O erro que a pergunta revela:** achar que a métrica esgota o que o modelo produziu. Todo
classificador calcula uma quantidade contínua antes de decidir, e as quatro métricas da Aula 09 são
medidas depois da decisão, sobre a mesma matriz de confusão.

**O momento de virar a chave:** a árvore de entropia tem AUC 0,500 e dois pontos na curva. Não é uma
AUC baixa, é ausência de ordenação: ela prevê a mesma classe nos 24 meses e não existe limiar
intermediário para varrer. Em termos de ordenação, ela é a baseline.

**Se sobrar tempo:** peça para alguém explicar por que o SVM RBF, com a mesma acurácia, tem AUC
0,738. A resposta é que a distância até a fronteira ordena os meses mesmo quando o sinal dela decide
sempre igual, e isso é um problema com conserto por limiar.

**Se travar:** volte para a tabela do slide 3 e pergunte que matriz de confusão produz acurácia
0,833, precisão 0,833 e revocação 1,000. É 20 verdadeiros positivos e 4 falsos positivos, zero
verdadeiros negativos. Os três modelos produzem essa matriz, e nenhuma função dela pode distingui-los.

### 2. Hiperparâmetros, GridSearch e RandomSearch (10h30-11h00, 30 minutos)

**Pergunta:** o que é um hiperparâmetro, e em que ele difere de um parâmetro aprendido pelo modelo?

**Resposta esperada:** o hiperparâmetro é escolhido antes do `fit` e decide como o `fit` acontece; o
parâmetro é o que o `fit` calcula. Boa parte da turma sabe dizer isso do autoestudo "O que é
hiperparâmetro?", e a pergunta serve mais para ancorar o vocabulário do que para descobrir algo.

**A segunda pergunta, que é a que trabalha:** a floresta da Aula 07 tem quantos hiperparâmetros
escolhidos? A resposta é **um**, `n_estimators=300`. Os outros quatro da tabela do slide 10 são
default.

**O erro que a pergunta revela:** tratar default como ausência de decisão. `max_depth=None` com
`min_samples_leaf=1` manda cada árvore crescer até isolar uma linha por folha, e isso é uma decisão
com consequência medida.

**O momento de virar a chave:** as sete features que a Aula 09 acrescentou pioram a floresta sem
ajuste, de 4,48% para 5,04%. Pergunte à sala se a culpa é das features ou da floresta, deixe as duas
hipóteses no quadro, e rode a grade. A resposta é a floresta: com poda, as onze features chegam a
4,21%.

**Fecho do bloco, na prática da dupla:** cada dupla mede o próprio modelo **sem ajuste primeiro**.
Sem o número de partida, o ganho não existe, e é o erro mais comum desta prática.

### 3. Validação cruzada temporal (11h00-11h30, 30 minutos)

**Pergunta:** o `GridSearchCV` que acabamos de rodar tinha `cv=TimeSeriesSplit(5)`. O que teria
acontecido sem esse argumento?

**Resposta esperada:** que ele usaria outra forma de cortar os dados. Quase ninguém sabe qual, e
quem leu "Validação Cruzada" responde "`KFold`" sem perceber o que isso implica numa série.

**O erro que a pergunta revela:** ler a validação cruzada como técnica de amostragem neutra. Ela
corta por posição na tabela, e a tabela do case está em ordem de calendário.

**O momento de virar a chave:** a figura das dobras, slide 19. Na primeira dobra do `KFold`, os 252
meses de treino são **todos** posteriores ao início da validação. Deixe o número no ar antes de
mostrar o `TimeSeriesSplit`.

**A pergunta que vem depois, e para a qual existe seção própria acima:** se o `KFold` escolheu um
modelo que erra menos no teste, por que trocar?

**Fecho do bloco, na prática da dupla:** percorrer `cv.split(Xtr)` e imprimir o primeiro e o último
mês de treino e de validação, dobra a dobra. Ver a janela crescer vale mais que ouvir a explicação.

### 4. Explicabilidade com SHAP e partial dependence (11h30-11h50, 20 minutos)

**Pergunta:** a floresta tem 600 árvores podadas. Como explicar para a LDC o que ela usa?

**Resposta esperada:** olhando a importância das features. Quase todo mundo chega a
`feature_importances_`, que é o que vem de graça, e é exatamente aí que o bloco trabalha.

**O erro que a pergunta revela:** achar que existe **uma** importância. Existem duas leituras, que
medem coisas diferentes sobre conjuntos diferentes, e elas discordam a partir da terceira posição
nesta base.

**O momento de virar a chave:** a tabela do slide 27. `abate_bovinos_lag1` é a terceira por SHAP e a
sexta por impureza. Pergunte qual está certa. A resposta é que a pergunta está mal feita: uma mede
redução de impureza no treino, a outra mede contribuição por previsão no teste.

**O fecho que amarra com o parceiro:** o partial dependence de `lag12`, que cai de 9,3% para 1,0% de
crescimento previsto. Peça que alguém diga isso em uma frase sem citar nome de algoritmo. A frase
boa é algo como "o modelo prevê crescimento menor quando a base do ano anterior já é grande", e é
essa frase que vai para o parceiro.

**Se sobrar tempo:** pergunte o que fazer se a curva contrariasse o que o especialista do setor
sabe. A resposta é que o achado passaria a ser sobre o modelo, e viraria pergunta para o parceiro em
vez de resultado a reportar.

### 5. Quiz e amarração com a ART.7 (11h50-12h00, 10 minutos)

Os dois quizzes cobrem os dois pontos que mais escorregam: a AUC 0,500 da árvore, que é ausência de
ordenação e não ordenação ruim, e o que fazer com o resultado do `KFold` que contraria a aula.

**A amarração, dita em voz alta:** o modelo que sai daqui, `max_depth=4`, `min_samples_leaf=5`,
`n_estimators=600`, a 4,21% de MAPE, é o candidato ajustado à mão. Na Aula 11 ele é o termo de
comparação contra o PyCaret, e a pergunta de abertura daquele encontro já pode ser plantada hoje:
vocês acham que o AutoML vai bater o modelo que vocês ajustaram sabendo o que estavam fazendo?

**O que cada dupla leva de tarefa para o daily de 24/09:** a feature mais influente do próprio
modelo, encontrada via SHAP, com a leitura declarada.

---

## Leituras erradas a desfazer em voz alta

1. **"O `TimeSeriesSplit` dá um modelo melhor."** Nesta base, com onze features, ele dá um modelo
   0,08 ponto pior no teste. O que ele dá é uma estimativa de validação que responde à pergunta do
   parceiro. A troca é de protocolo, não de desempenho.

2. **"AUC 0,500 significa que o modelo é ruim."** Significa que ele não ordena. A árvore de entropia
   tem AUC 0,500 e 83,3% de acurácia ao mesmo tempo, e mexer no limiar não a melhoraria, porque não
   há nada para reordenar. Já o SVM RBF, com a mesma acurácia e AUC 0,738, tem conserto por limiar.

3. **"Mais árvores é sempre melhor."** Dobrar `n_estimators` de 300 para 600 sem podar piora o erro,
   de 5,04% para 5,20%. Mais árvores reduzem a variância da média, não o viés de cada árvore, e aqui
   cada árvore está decorando.

4. **"O melhor da grade erra 4,07%."** Erra, no conjunto de teste, e esse ponto não é alcançável: o
   `GridSearchCV` escolhe olhando só o treino e chega em 4,21%. Escolher a combinação pela métrica de
   teste é escolher pela resposta.

5. **"O SHAP é a importância certa e a impureza é a errada."** As duas respondem perguntas
   diferentes. O que a ART.7 cobra é que a leitura usada esteja declarada junto do resultado, com o
   conjunto sobre o qual foi medida.

6. **"Com o ajuste, as onze features passaram a ser melhores que as quatro."** Não passaram: a
   floresta ajustada sobre as quatro features da Aula 07 erra 3,95%, contra 4,21% das onze. O ajuste
   recupera a maior parte do custo das features novas, não todo. Escolher features não é assunto
   desta aula.

7. **"O `RandomizedSearchCV` sempre acha o mesmo com menos treinos."** Aqui achou, porque das três
   dimensões da grade só duas movem o erro, e isso foi medido antes. Quem usa busca aleatória sem
   ter medido quais dimensões importam está apostando.

8. **"O alvo binário virou o alvo do projeto."** Continua existindo só para dar às métricas de
   classificação um dado real sobre o que rodar. Os três modelos do TAPI preveem quantidade, e a
   ART.7 compara modelos de regressão.

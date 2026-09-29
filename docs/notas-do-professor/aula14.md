# Notas do professor: Aula 14

**06/10/2026 &middot; Revisão e Futuro &middot; Sprint 5**

Material de condução do encontro. O conteúdo abaixo reúne as perguntas que abrem cada bloco quando
a sala travar, cada uma com a resposta esperada e o erro que a pergunta costuma revelar. A ordem
segue os sete blocos do roteiro em `PLANEJAMENTO_AULA_A_AULA.md`, e todos os números saem de
`app/logica.py` e estão travados em `tools/tests/test_app_aula14.py`. A definição dos cenários está
em `docs/adrs/ADR-017`.

**Onde está o peso desta aula:** os slides 14 e 15. O mesmo choque de +10%, em dois ajustes do mesmo
modelo, dá +9,62% e +9,63% quando aplicado às quatro defasagens do frango juntas, e +0,151% contra
-0,005% quando aplicado só ao abate de bovinos. A turma precisa sair com o critério que isso
produz para a ART.9: cenário vai para a apresentação só com o mesmo sinal nos dois ajustes.

**É a última aula do módulo, e não se fala da prova de 02/10.** Nenhuma questão, nenhum resultado.
Se alguém perguntar, a resposta é que a devolutiva sai pelo canal da Adalove.

---

## Checkpoint de abertura, na daily

**A pergunta:** o `streamlit run app/app.py` sobe na máquina de todo mundo?

O `streamlit` não estava na lista de pacotes das aulas anteriores. Mande instalar na daily, com
`pip install -r app/requirements.txt`, e não às 10h45. Quem estiver no Colab roda o notebook, que usa
a mesma lógica sem servidor, e sobe o app depois em casa.

Se aparecer `InconsistentVersionWarning` na carga do modelo, é o `scikit-learn` da máquina diferente
de 1.9.1. A Aula 12 mediu: três avisos, previsão idêntica. Não precisa parar a aula por isso.

---

## Ordem de corte, se o tempo apertar

1. **O slide 23, das técnicas de IA generativa.** Cabe em uma frase apontando a tabela, e o debate
   do slide 25 não depende dele.
2. **O slide 9, do passo à frente.** Vira uma frase dita no slide 8: as 24 previsões usam o abate
   real do mês anterior, e o único mês futuro é 2026-04.
3. **O exercício do slide 21 vira tarefa da dupla** para a apresentação, porque ele já é o esqueleto
   da ART.10.

**O que nunca cai:** os slides 14 e 15, e o ensaio do slide 26.

---

## Bloco 1, 10h15 às 10h30. Resgate e a pergunta disparada

**A pergunta (do roteiro):** quem vai usar essa previsão na LDC, e o que essa pessoa precisa ver na
tela?

**Resposta esperada:** alguém da área comercial ou de originação de grãos, que decide quanto milho e
farelo comprar e quando. Essa pessoa precisa ver o número previsto com a unidade, o quanto o modelo
costuma errar, e o que acontece se uma premissa mudar. Três elementos que a tela do app tem: o
cartão de MAPE, o gráfico de histórico contra previsão e o controle de cenário.

**Erro comum que ela revela:** a turma responde "o gráfico" e para. Pergunte: "o gráfico sem o erro
ao lado serve para decidir compra de milho?". Não serve: um número sem a incerteza dele é um palpite
com casas decimais. O segundo erro é responder "o cientista de dados": o usuário da tela não é
quem fez o modelo.

---

## Bloco 2, 10h30 às 10h45. Streamlit e o app de `app/`

**Pergunta 1:** o app carrega o modelo exportado, que erra 2,65% nos 24 meses do gráfico. Por que o
cartão mostra 2,86%?

**Resposta esperada:** o exportado foi reajustado sobre os 339 meses e já viu os 24 de teste. O
2,65% é erro sobre dado visto. O 2,86% é do objeto avaliado, que nunca viu esses meses, e é a única
estimativa honesta. É a lição da Aula 12, aplicada à tela.

**Erro comum:** achar que o número menor é o mais atual e por isso o melhor. Devolva: "se eu
treinar com a prova, minha nota na prova diz alguma coisa?".

**Pergunta 2 (quiz do slide 10):** por que o modelo fica em `@st.cache_resource`?

**Resposta esperada:** o Streamlit reexecuta o script inteiro a cada clique. Sem cache, cada
movimento do controle relê o `.joblib` do disco.

**Erro comum:** pensar que o Streamlit funciona por evento, como um `onclick` de JavaScript. Mostre
um `print` no topo do `app.py` e mova um controle: o terminal imprime de novo.

---

## Bloco 3, 10h45 às 11h00. Prática

**A pergunta que destrava:** a dupla escolheu produção de leite no seletor. O que o app deve mostrar?

**Resposta esperada:** só o histórico, com aviso. O modelo prevê abate de frangos; o leite entra
nele como entrada defasada de um mês. Inventar uma previsão para o leite seria mostrar um número que
nenhum modelo produziu.

**Erro comum:** a dupla reaproveita o `Pipeline` do frango para "prever" o leite, passando as
features do leite. Roda, porque são onze números, e devolve lixo em quilogramas de frango.

---

## Bloco 4, 11h00 às 11h15. Cenários

**Pergunta 1:** por que o app não tem um controle de preço do milho, se é o que a LDC mais pergunta?

**Resposta esperada:** porque nenhuma das onze entradas é preço. O controle mexeria num número que
o modelo nunca lê, e a previsão não mudaria. Para o milho entrar precisa de série aberta de preço,
defasagem declarada e modelo reavaliado no mesmo corte.

**Erro comum:** "então o milho não afeta o frango". Não: o modelo não testou isso. Sem a
feature, o efeito do milho fica sem medir.

**Pergunta 2 (quiz do slide 16):** a dupla quer mostrar que 10% a mais de bovinos aumenta o frango
previsto em 0,15%. Pode?

**Resposta esperada:** não. No avaliado o efeito é -0,005%: o sinal troca com 24 meses de dado a
mais. As defasagens e as outras séries são colineares, e o reajuste move a partilha de peso entre
elas. O cenário estável é o do grupo inteiro.

**Erro comum:** propor um choque maior "para ficar visível". O modelo é linear: o choque maior
multiplica os dois efeitos e mantém a troca de sinal.

**A pergunta difícil que pode aparecer:** "+10% no patamar dá +9,62%. O modelo descobriu que o
frango cresce com o próprio passado?" Não descobriu nada de novo: a soma dos coeficientes das
defasagens é 0,976, perto de 1, e diz que o abate de um mês acompanha o dos anteriores. O valor do
cenário está na estabilidade entre os dois ajustes.

---

## Bloco 5, 11h15 às 11h30. Linha do tempo e critérios de publicação

**A pergunta:** das quatorze aulas, qual decisão mudou mais o resultado final?

**Resposta esperada, com número:** duas disputam. A correção de granularidade da Aula 07 (de 117
trimestres para 339 meses, no horizonte que o TAPI pediu) e a decisão de alvo da Aula 11 (o alvo em
razão custava 0,46 ponto ao modelo linear). Aceite qualquer uma que venha com o número.

**Erro comum:** responder com o algoritmo ("a floresta", "o PyCaret"). A floresta ajustada ficou em
4,21%, pior que o linear a 2,86%. As decisões que mais pesaram foram de dado e de protocolo.

**Sobre o checklist do slide 20:** é proposta do acervo. A rubrica da ART.9 é a da Adalove, e isso
precisa ser dito, para ninguém tratar o slide como gabarito da entrega.

---

## Bloco 6, 11h30 às 11h45. IA generativa

**A pergunta (do roteiro):** onde a IA generativa poderia entrar no pipeline da LDC, e onde não
deveria?

**Resposta esperada:** poderia entrar onde o resultado é conferível por outro caminho: extrair
tabela de boletim em PDF (confere somando contra o total), rascunho de código (confere com teste que
já falhou), redação do relatório (confere com a fonte de cada número). Não deveria gerar o número da
previsão, porque ele não teria erro medido, corte temporal nem reprodutibilidade.

**Erro comum 1, o entusiasmo:** "o modelo de linguagem prevê melhor porque leu tudo". Pergunte qual
é o MAPE dele nos 24 meses de teste. Não existe, e sem ele não há como comparar com 2,86%.

**Erro comum 2, a recusa:** "IA generativa não serve para nada sério". Aponte a linha dos boletins
em PDF: dado não estruturado virando tabela é um uso real, e o risco dele é conhecido e conferível.

**Sobre autoria:** a posição do COPE é que a ferramenta não é autora porque não responde pelo
trabalho. Na ART.10, quem responde por cada número é a dupla.

---

## Bloco 7, 11h45 às 12h00. Amarração e ensaio

**ART.9 Critérios de Publicação, peso 3**, e **ART.10 Apresentação final, peso 3**, citados de
`PLANO_DE_ENSINO.md`. A Sprint 5 e o módulo fecham em **07/10**.

O roteiro pede "ensaio curto da apresentação em dupla" e não fixa formato. O deck sugere três
minutos por dupla, para a dupla vizinha, com a vizinha anotando a frase que aparecer sem número.
É sugestão de condução, e a regra da entrega é a da Adalove; ajuste o tempo ao número de duplas presentes.

**A pergunta de fechamento:** qual frase da apresentação de vocês não tem um número atrás?

---

## Registro de interpretação

- **O roteiro não diz sobre qual variável o cenário atua.** A decisão (grupos de entradas que o
  modelo lê, conferidos nos dois ajustes, e milho recusado) está em `docs/adrs/ADR-017`.
- **O roteiro fala em "previsão dos 24 meses de teste".** O app mostra essas 24 previsões, que são
  de um passo à frente, e acrescenta a previsão de 2026-04, o único mês futuro que o modelo prevê só
  com dado medido.
- **Os dois quizzes estão dentro dos blocos** (slides 10 e 16), para que cada
  bloco teórico feche em interação dentro dos 15 minutos.
- **O checklist de publicação é proposta do acervo**, porque nenhuma fonte do repositório descreve a
  rubrica da ART.9.

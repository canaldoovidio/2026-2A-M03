# Notas do professor: Aula 13

**30/09/2026 &middot; Revisão para a Prova de 02/10 (registro na Adalove: Deploy de modelos de
Machine Learning) &middot; Sprint 5**

Material de condução do encontro. Reúne o protocolo da votação, a correção cruzada e as perguntas
que destravam cada bloco, com a resposta esperada e o erro que cada pergunta costuma revelar. Os
números vêm de `tools/graficos_aula13.py` e estão travados em `tools/tests/test_revisao_aula13.py`.
A decisão de converter o encontro está em `docs/adrs/ADR-016`.

**Regra do encontro.** Nenhuma pergunta, cenário ou número da Prova entra na fala, no quadro ou
nos exemplos improvisados. Quando um aluno pedir "cai assim?", a resposta é o tema, nunca a
questão. Todo exemplo improvisado usa o case da LDC.

**Onde está o peso desta aula:** as Revisões 3 e 4. Matriz de confusão é o tema com mais passos
encadeados, e ETL/ELT e recomendação tiveram um slide e dez minutos de sala no módulo inteiro.

---

## Antes do encontro

- Na noite anterior, confira quantas duplas rodaram o autodiagnóstico. Quem não rodou chega sem
  as duas dúvidas, e a daily perde a função.
- Leve cartões A, B, C e D, ou combine a votação por dedos. A votação precisa ser simultânea: quem
  vota depois olha o vizinho.
- Na daily, anote no quadro as dúvidas de todas as duplas, agrupadas pelos oito temas do slide 36.
  O tema com mais marcas ganha os minutos de folga do fim.
- **Não use o botão Exportar PDF para distribuir o deck antes da aula**: o PDF sai com o gabarito
  dos oito quizzes marcado (`inteli-deck-design`, seção 8.6).

---

## Como conduzir a votação (slides 3, 6 a 9 e os quatro "Pares")

O protocolo é o de Crouch e Mazur (2001), e a regra de decisão está no slide 3.

1. **Leia a pergunta em voz alta** e dê um minuto. Ninguém fala.
2. **Todos levantam o cartão ao mesmo tempo.** Conte por alto e anote no quadro: letra e
   proporção.
3. **Decida pela proporção de acerto no primeiro voto:**
   - acima de 70%: clique na alternativa, explique em uma frase e siga;
   - entre 35% e 70%: dois minutos em dupla, com a regra de conversar com quem votou diferente,
     e revoto;
   - abaixo de 35%: não abra discussão, porque dupla que não sabe convence dupla que não sabe.
     Volte ao slide de conteúdo do tema, explique, e só então revote.
4. **Só clique depois do revoto.** O clique revela a resposta e a mensagem de feedback, e depois
   dele a pergunta não serve mais para medir nada.
5. **Registre as duas contagens.** A diferença entre o primeiro e o segundo voto é o dado que diz
   se a discussão funcionou.

Nos quatro diagnósticos (slides 6 a 9) **não há discussão**: é voto único, e o clique fica para o
fim do bloco. Eles medem o ponto de partida. Volte a cada um no fim da revisão correspondente e
peça um voto rápido: se a proporção de acerto não subiu, o bloco não resolveu.

**Letra pela posição.** As alternativas não têm letra impressa; A é a de cima. Diga isso uma vez,
no slide 3.

---

## Como conduzir a correção cruzada (slides 34 e 35)

1. Às 11h30 cada dupla começa a prática da seção 9 do notebook, numa folha ou num arquivo.
2. Às 11h40 a folha vai para a dupla da direita. A última da fila entrega para a primeira.
3. A dupla corretora marca **atende** ou **não atende** em cada um dos sete critérios do slide 35
   e escreve uma frase só sobre o critério que falhou. Não dá nota.
4. Às 11h44 a folha volta. A dupla autora lê a frase e decide se concorda.
5. Circule pela sala. O que mais vale ouvir: a dupla corretora dizendo "vocês sortearam" e a
   autora respondendo por quê. É o critério da divisão, e ele tem resposta certa para a pergunta
   da LDC.

**Os três critérios que mais falham, em ordem:** o momento do dado (a dupla escolhe x = suínos do
próprio trimestre), a divisão (sorteio sem justificativa) e a inclinação (lida como causa, ou sem
unidade).

---

## Ordem de corte, se o tempo apertar

1. **O slide 20**, da reta cronológica. Vira uma frase dita no slide 19: a reta ajustada até
   2020-T1 superestima os 24 trimestres seguintes.
2. **O slide 21**, das sementes. Vira uma frase: com teste de 4 trimestres o R² desce até -0,25.
3. **A correção cruzada** encurta para a troca de folhas sem o retorno.

**O que nunca cai:** os diagnósticos e o slide 36, dos temas. São a forma de a turma saber onde
estudar até sexta.

---

## Bloco 1, 10h15 às 10h30. Resgate e diagnóstico

**A pergunta disparada:** em que momento cada coluna da base da LDC passa a existir?

**A resposta esperada:** calendário sempre; defasagens quando o mês correspondente é publicado;
as outras séries do mês t só junto com o alvo.

**O erro que ela revela:** tratar o CSV como fotografia do presente. No arquivo, toda coluna
existe; no dia da previsão, não.

**Se alguém perguntar sobre o `lag1`:** a base supõe que t-1 já foi publicado. O
`dados/README.md` diz que o SIDRA publica o trimestre e os três meses juntos, então essa premissa
precisa ser conferida com o calendário de publicação. Não resolva em sala: é um bom item para a
dupla levar à LDC. Está na seção 2 do material.

---

## Bloco 2, 10h30 às 10h45. Revisão 1

**A pergunta:** as séries do próprio mês levam o MAPE de 2,86% para 2,43%. Por que não usar?

**A resposta esperada:** porque no dia da previsão elas estão vazias; o ganho é o que o modelo
perde no primeiro uso real.

**O erro que ela revela:** escolher X pela métrica de teste. A métrica premia a coluna que vaza.

**A pergunta do slide 13:** a árvore com o número da linha erra 0,00% no treino. Isso é bom?

**A resposta esperada:** é o sintoma. Treino perfeito com uma feature sem significado é
memorização, e o teste mostra um único valor previsto para os 24 meses.

**A pergunta do slide 14:** medir em 100 meses em vez de 24 conserta a floresta ajustada em tudo?

**A resposta esperada:** não, continua 1,31%. O que decide a validade é o modelo não ter visto as
linhas medidas.

---

## Bloco 3, 10h45 às 11h00. Revisão 2

**A pergunta do slide 17:** por que `df[["suinos_lag1"]]` e não `df["suinos_lag1"]`?

**A resposta esperada:** X precisa ser 2D; com colchete simples vem uma Series e o `fit` levanta
`ValueError: Expected 2D array`.

**A pergunta do slide 19:** o R² de 0,95 está errado?

**A resposta esperada:** está certo para a pergunta que ele responde, que é interpolar entre
trimestres conhecidos. A pergunta da LDC é outra.

**A pergunta do slide 22:** por que o R² é 0,54 se o MAPE é 2,86%?

**A resposta esperada:** porque os 24 meses de teste variam pouco; o R² mede a fração dessa
variância que o modelo explica, e com pouca variância um erro pequeno pesa muito.

**O erro que ela revela:** ler R² como "porcentagem de acerto".

---

## Bloco 4, 11h00 às 11h15. Revisão 3

**A pergunta do slide 25:** fev/25 foi real alta e previsto queda. Que caso é?

**A resposta esperada:** FN. A segunda letra é o que o modelo previu (negativo, queda); a
primeira diz que errou.

**O erro que ela revela:** classificar pela classe real. É o erro mais frequente do tema; volte
ao critério do slide 25 sempre que aparecer.

**A pergunta do slide 27:** o SVM linear e a baseline têm 83,3%. São equivalentes?

**A resposta esperada:** não. A baseline tem revocação zero na queda; o SVM encontra 2 das 4.

**A pergunta do slide 28:** qual limiar é o certo?

**A resposta esperada:** depende do custo de cada erro, que é declarado pela LDC antes. Se FN
custa mais, desce; se FP custa mais, sobe.

---

## Bloco 5, 11h15 às 11h30. Revisão 4

**A pergunta do slide 31:** o acervo é ETL ou ELT?

**A resposta esperada:** ELT. `dados/` guarda o cru; cada aula transforma quando precisa.

**O erro que ela revela:** achar que "tem transformação, então é ETL". A diferença é a ordem, não
a existência da transformação.

**A pergunta do slide 32:** e se a granja nova informar no cadastro o que ela cria e em que fase?

**A resposta esperada:** então a baseada em conteúdo passa a ter um perfil declarado para
comparar com os atributos das formulações. O cold start de usuário é falta de dado sobre o
usuário, e cadastro é dado.

---

## Bloco 7, 11h45 às 12h00. Amarração

- Prova 02/10, peso 20. ART.8 Modelo Final, peso 4, review em 07/10. ART.9 Critérios de
  Publicação, peso 3: o app Streamlit, na Aula 14, em 06/10.
- Mostre o slide 36 e diga que a tabela é de temas e de onde revisar, e mais nada. Não comente
  formato, quantidade ou ordem de questões.
- Peça que cada dupla escolha, antes de sair, os dois temas do slide 36 que vai estudar primeiro,
  a partir das contagens do quadro.

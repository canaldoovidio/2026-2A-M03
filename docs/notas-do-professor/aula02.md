# Notas do professor: Aula 02

**07/08/2026 &middot; Visão Geral do Aprendizado de Máquina, Inteligência Artificial e Ciência de
Dados &middot; Sprint 1**

Material de condução do encontro, não de distribuição ao aluno. Não é resumo do deck: são as
perguntas que abrem a sala quando ela travar, cada uma com a resposta esperada e o erro que a
pergunta costuma revelar.

Ordem igual à do roteiro em `PLANEJAMENTO_AULA_A_AULA.md`.

**Aviso de condução:** esta é a aula em que menos se digita e mais se decide. A tentação é
transformá-la em palestra. O roteiro tem quatro momentos de mão na massa (dois exercícios em
duplas, uma votação e um desenho em papel) justamente para isso não acontecer.

---

## 10h00 - 10h15 &middot; Daily

**Checkpoint obrigatório antes de começar:** todas as duplas conseguiram ler o CSV de abate bovino
até o fim da Aula 01?

Quem não conseguiu não acompanha o notebook de hoje, que carrega cinco arquivos de uma vez.
Resolver agora, mandando para o Colab pelo badge do notebook se for problema de ambiente local.

---

## 10h15 - 10h30 &middot; Resgate e abertura

**P1. O TAPI pede previsão mensal. Nosso dado é trimestral. O que fazemos com isso?**

Pergunta do roteiro. **Peça a resposta pelo lado do projeto, não pelo lado técnico**, senão a
turma inteira responde "interpola" nos primeiros dez segundos e a discussão morre.

- *Resposta esperada:* voltar ao parceiro, mostrar a limitação da fonte e propor uma alternativa
  que cubra o mesmo período.
- *O erro que revela:* tratar uma questão de escopo como problema de implementação. Se aparecer
  "interpola", não descarte: escreva no quadro e volte a ele em P5.

**P2. Alguém percebeu isso na Aula 01, ou só agora?**

- *Resposta esperada:* o reparo apareceu na Aula 01, ao ler a coluna `periodo`.
- *O erro que revela:* a turma acha que "entendimento dos dados" é uma etapa que alguém faz antes
  do projeto começar. Foi a leitura do arquivo, na mão, que produziu o achado.

---

## 10h30 - 10h45 &middot; ML, IA e Ciência de Dados

**P3. O coeficiente fixo que a LDC usa hoje é inteligência artificial?**

A melhor pergunta da aula, porque a resposta é "sim" e ninguém espera.

- *Resposta esperada:* é um sistema de regras, então é IA sem Machine Learning. E funciona.
- *O erro que revela:* a equação "IA igual a modelo treinado". Emenda direto no ponto seguinte,
  que é o mais importante do dia para o projeto.

**P4. Então contra o que vamos comparar o nosso modelo?**

- *Resposta esperada:* contra o coeficiente fixo que já está em produção.
- *O erro que revela:* querer comparar contra zero, contra a média ou contra nada. Um modelo com
  RMSE baixo que perde do coeficiente fixo não entrega valor nenhum ao parceiro, e essa é a
  comparação que a ART.7 vai cobrar.

**Exercício (6 min).** As quatro perguntas do slide 7, classificadas em descritiva, diagnóstica,
preditiva ou prescritiva. As perguntas 2 e 4 admitem discussão: a 2 é preditiva mas encosta em
prescritiva, e a 4 é prescritiva mas depende de uma predição. **A discussão é o exercício**, não a
resposta.

---

## 10h45 - 11h00 &middot; CRISP-DM

**P5. Em qual fase do CRISP-DM a gente descobriu que o dado era trimestral?**

- *Resposta esperada:* na fase 2, Entendimento dos dados.
- *O erro que revela:* achar que descobrir isso na fase 2 significa que a fase 1 foi mal feita. Não
  significa: é a função da fase 2. O que seria erro é seguir para a fase 3 sem voltar.

**P6. Para onde a gente foi depois de descobrir?**

- *Resposta esperada:* de volta para a fase 1, renegociar granularidade.
- *O erro que revela:* a leitura do CRISP-DM como lista linear de tarefas. Aqui é o momento de
  desenhar as setas de volta no quadro. Se a turma tiver decorado as seis fases em ordem e nunca
  visto as setas, este é o conteúdo novo da aula.

**Exercício (6 min).** Uma frase por fase, aplicada ao case, dizendo o que a dupla vai fazer, não o
que a fase significa. **O item 2 do slide é o que importa:** marcar qual das seis frases eles ainda
não conseguem escrever. Se todas as duplas conseguirem escrever as seis, elas escreveram genérico:
peça para reescrever a frase da fase 5 dizendo contra o que vão comparar.

---

## 11h00 - 11h15 &middot; O descompasso e a decisão

**P7. Quantas observações da base seriam inventadas se a gente interpolasse?**

Deixe a turma fazer a conta. São 117 medidas e 234 inventadas, dois terços.

- *Resposta esperada:* dois terços.
- *O erro que revela:* a intuição de que interpolar "só suaviza". Complete: o RMSE passaria a medir
  o quanto o modelo acerta um número que ninguém observou.

**P8. Votação, levantando a mão: vocês teriam aceitado o pedido do parceiro sem checar a fonte de
dados primeiro?**

Votação do roteiro. **Conte os dois lados em voz alta antes de seguir.** O objetivo não é
constranger quem levantou a mão: é mostrar que a maioria aceitaria, e que é exatamente por isso que
o CRISP-DM tem uma fase para isso.

- *O erro que revela:* nenhum. Aqui o valor está no registro do próprio comportamento da turma,
  que volta na Sprint Review.

---

## 11h15 - 11h30 &middot; Prática no papel

**Instrução de condução:** papel e caneta, sem computador aberto. Doze minutos.

Os três modelos em caixas, com as setas, e a fonte anotada ao lado de cada um. O item 3 (marcar com
um X onde a granularidade muda de trimestral para anual) é o que separa a dupla que entendeu da
dupla que copiou o slide.

**P9. Por que a Sindirações entra só no Modelo 2?**

- *Resposta esperada:* porque é ela que dá a relação entre proteína produzida e ração consumida; o
  SIDRA não tem essa informação.
- *O erro que revela:* achar que mais fonte é sempre melhor, sem perguntar o que cada uma responde.

**P10. O que acontece quando um modelo trimestral alimenta um modelo anual?**

- *Resposta esperada:* alguém tem que decidir se agrega o trimestral ou se reparte o anual, e as
  duas decisões introduzem erro.
- *O erro que revela:* nenhum, se a turma chegar aqui. Deixe a resposta **em aberto**: é o problema
  da Aula 04 e da Sprint 2. Anote no quadro e não resolva hoje.

---

## 11h30 - 11h45 &middot; Qualidade e taxonomia

**P11. Todos os cinco arquivos passam em todos os testes. A base está boa?**

- *Resposta esperada:* não necessariamente. A série de leite mede leite *adquirido* pelos
  laticínios, não produzido.
- *O erro que revela:* confiar em teste verde como prova de qualidade. Este é o argumento central
  da aula, e vale escrever no quadro: **nenhum script sabe que "adquirido" não é "produzido"**.

**P12. Qual a média da coluna `unidade`?**

Pergunta com resposta impossível, de propósito.

- *Resposta esperada:* não existe. `unidade` é nominal.
- *O erro que revela:* o hábito de calcular o que a biblioteca aceita calcular. Emenda em: e a média
  de `periodo`? Também não, enquanto for rótulo; passa a existir depois de virar índice de tempo,
  que é a Aula 04.

**Exercício (5 min).** Cada dupla escolhe em `dados/README.md` um risco de qualidade que não
apareceu no slide, diz a qual pilar pertence e o que aconteceria com o Modelo 1 se ninguém tivesse
notado. Riscos repetidos não valem: quem vier depois procura outro. Isso força a turma a ler o
arquivo inteiro em vez de pegar o primeiro.

---

## 11h45 - 12h00 &middot; Amarração com a sprint

**P13. Se vocês tivessem que entregar a ART.1 hoje, o que já está pronto?**

- *Resposta esperada:* a granularidade medida, a negociação, os três modelos com as fontes, as seis
  frases do CRISP-DM e o baseline do coeficiente fixo.
- *O erro que revela:* achar que falta "a parte técnica". A ART.1 é entendimento do negócio: o que
  falta nela é o que a dupla não conseguiu escrever no exercício do CRISP-DM, e isso é conteúdo, não
  lacuna.

Lembrar: Sprint 1 fecha em **14/08**, com **ART.1 Entendimento do negócio (peso 6)** e ART.2 UX
parte 1 (peso 3). Próximo encontro em **11/08**, com Pandas sobre as cinco séries.

---

## Se a sala travar

- **A turma acha a aula abstrata e dispersa.** Abra o notebook e rode a célula da soma sem sentido
  (seção 4). O número aparece, ninguém reclama, e a sala entende a aula inteira em trinta segundos.
- **A discussão de granularidade vira debate sem fim.** Corte com a votação (P8) e apresente a
  decisão dos 8 trimestres. A decisão já está tomada e registrada na ADR-003: hoje ela é comunicada,
  não construída.
- **Sobrou tempo.** Peça para calcularem, no notebook, quantos ovos em unidades o pico da série
  representa. É o item 2 do desafio, e obriga a passar por "mil dúzias" com atenção, que é o mesmo
  erro de unidade que estava documentado errado no `dados/README.md` até 03/08.
- **Faltou tempo.** Corte o bloco de taxonomia (slide 19) e mande como leitura no material. O bloco
  de qualidade (slides 18 e 20) não pode cair: é o que alimenta a ART.1.

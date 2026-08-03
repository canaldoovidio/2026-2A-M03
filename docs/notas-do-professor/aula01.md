# Notas do professor: Aula 01

**04/08/2026 &middot; Introdução ao Python &middot; Sprint 1**

Material de condução do encontro, não de distribuição ao aluno. Não é resumo do deck: são
as perguntas que abrem a sala quando ela travar, cada uma com a resposta esperada e o erro
que a pergunta costuma revelar.

Ordem igual à do roteiro em `PLANEJAMENTO_AULA_A_AULA.md`.

---

## 10h15 - 10h30 &middot; Abertura do case

**P1. O que vocês esperam prever a partir de um CSV de abate de bovinos?**

Esta é a pergunta do roteiro, e o valor dela está em registrar as respostas no quadro antes
de qualquer um ter aberto o arquivo. No fim da aula, voltar ao quadro e riscar o que o
arquivo não sustenta.

- *Resposta esperada:* varia. Costumam aparecer "preço da carne", "exportação", "consumo".
- *O erro que revela:* a turma projeta no dado aquilo que ela gostaria que estivesse lá.
  O arquivo tem três colunas e uma série de volume abatido. Nada de preço, nada de
  exportação, nada de consumo. Esse contraste é o gancho para o resto da aula.

**P2. Se o Modelo 1 errar 10% na produção de frango, o que acontece com a previsão de
compra de milho?**

- *Resposta esperada:* o erro propaga pelos três modelos, porque cada um consome a saída do
  anterior.
- *O erro que revela:* achar que "o modelo do fim corrige o do começo". Não corrige. É o
  argumento de por que a primeira aula é sobre o dado de entrada.

---

## 10h30 - 10h45 &middot; Tipos e estruturas

**P3. Por que `"10" + "2"` devolve `"102"` e não `12`?**

- *Resposta esperada:* porque os dois são texto, e `+` entre textos concatena.
- *O erro que revela:* a expectativa de que a linguagem "entenda" que aquilo parece número.
  Emenda direto no ponto seguinte: tudo que sai do CSV é texto.

**P4. Quando vocês usariam tupla em vez de lista aqui?**

- *Resposta esperada:* para um registro já formado, `("2025-T4", 2937449898.0)`, que não
  deveria poder ser alterado por acidente.
- *O erro que revela:* responder "quando quero que seja mais rápido". A pergunta que decide
  a estrutura não é velocidade, é **o que a estrutura precisa proibir**. Se ninguém chegar
  lá, perguntar: "o que você quer que o programa te impeça de fazer com esse registro?".

**P5. Como vocês descobririam, sem abrir o arquivo no Excel, se a série está toda na mesma
unidade?**

- *Resposta esperada:* montar o conjunto da coluna `unidade` e olhar o tamanho.
- *O erro que revela:* propor um laço com `if` e uma lista de vistos, reinventando o
  conjunto. Aceitar a resposta e mostrar que a linguagem já tem a estrutura com essa
  semântica.

---

## 10h45 - 11h00 &middot; Prática guiada em duplas

**P6. Quem chegou em 118 registros?**

Perguntar assim, com o número errado. Quem contou o cabeçalho junto levanta a mão sem
perceber que errou, e a correção sai da própria turma.

- *Resposta esperada:* 117. O `next()` consome o cabeçalho justamente para isso.
- *O erro que revela:* contar a linha de cabeçalho como dado. É o mesmo erro que, num
  dataset de treino, entra como uma observação de lixo.

**P7. A soma dos quatro trimestres de 2025 bateu 11.103.215.151?**

- *Resposta esperada:* sim, se converteram antes de somar.
- *O erro que revela:* quem começou o acumulador em `""` não recebeu erro nenhum e tem uma
  string enorme na mão. Quem começou em `0` recebeu `TypeError`. Vale mostrar os dois:
  **o que falhou é o caso bom**.

---

## 11h00 - 11h30 &middot; Ler o traceback

**P8. Onde eu leio primeiro num traceback?**

- *Resposta esperada:* na última linha, que dá o tipo e a causa.
- *O erro que revela:* a turma lê de cima para baixo, se perde no caminho de arquivos e
  conclui que "deu erro no Python". Insistir: última linha primeiro, depois subir.

**P9. `linha[3]` falhou. Qual índice devolve a unidade?**

- *Resposta esperada:* 2.
- *O erro que revela:* contar de 1. Se aparecer "3", não corrigir de imediato: pedir para
  imprimir `linha[0]` e deixar a turma concluir.

**P10. `float("2025-T4")` dá `ValueError` e `float(None)` dá `TypeError`. Por que erros
diferentes?**

- *Resposta esperada:* no primeiro, o tipo está certo (é texto) e o conteúdo não serve; no
  segundo, o tipo não serve.
- *O erro que revela:* tratar os dois como "erro de conversão". A distinção importa porque
  o tratamento é diferente: o primeiro se resolve limpando dado, o segundo se resolve
  arrumando de onde o valor veio.

**P11. Em Javascript, `linha.mes` devolveria `undefined` e o programa seguiria. Isso é
melhor ou pior?**

- *Resposta esperada:* pior, porque o erro aparece longe da causa.
- *O erro que revela:* a intuição de que "não quebrar" é sempre melhor. Numa cadeia de três
  modelos, falhar cedo e perto da causa é o comportamento desejável. É a primeira vez no
  módulo que "falhar" aparece como qualidade.

---

## 11h30 - 11h45 &middot; Discussão dirigida: o período

**P12. Por que vocês acham que o dado vem em `2025-T4` e não em mês?**

Pergunta do roteiro. **As respostas ficam em aberto de propósito**: a Aula 02 abre o
CRISP-DM exatamente aqui. Não fechar a discussão hoje.

- *Resposta esperada:* qualquer hipótese defensável sobre custo e periodicidade de coleta
  do IBGE. O ponto não é acertar, é perceber que a granularidade é uma decisão de quem
  coletou, não uma propriedade da realidade.
- *O erro que revela:* a proposta de "dividir o trimestre por 3 para virar mês". Não
  descartar de bate-pronto: perguntar o que aconteceria com o erro do modelo se dois terços
  das observações fossem inventadas. Deixar a resposta em aberto até a Aula 02.

**P13. O parceiro pediu 24 meses. Nosso dado é trimestral. Vocês aceitariam o pedido do
jeito que ele veio?**

- *Resposta esperada:* não sem antes conferir a fonte, e a contraproposta é horizonte de 8
  trimestres, que cobre os mesmos 24 meses.
- *O erro que revela:* aceitar o escopo sem checar a fonte de dados. Este é o conteúdo
  central da ART.1, e vale dizer isso em voz alta: negociar granularidade com quem pede o
  modelo é trabalho de projeto, não desculpa técnica.

---

## 11h45 - 12h00 &middot; Amarração com a sprint

**P14. Das coisas de hoje, o que entra na ART.1?**

- *Resposta esperada:* os 117 registros trimestrais como granularidade real da fonte, a
  discrepância com o pedido mensal, e a verificação de que a série tem unidade única.
- *O erro que revela:* achar que "entendimento do negócio" é texto sobre a empresa. A
  evidência de hoje é medida, não redigida.

Lembrar: Sprint 1 fecha em **14/08**, com **ART.1 Entendimento do negócio (peso 6)** e
ART.2 UX parte 1 (peso 3). Próximo encontro em **07/08**.

---

## Se a sala travar

- **Ninguém instalou o ambiente.** Mandar todos para o Colab pelo badge do notebook e seguir
  a aula. A célula de caminho do notebook já resolve o download do CSV.
- **A turma acha Python fácil demais e dispersa.** Antecipar a pergunta P10 (`ValueError`
  contra `TypeError`) e depois pedir para escreverem o agrupamento por trimestre sem olhar o
  notebook.
- **A turma travou na sintaxe e o tempo está estourando.** Cortar o bloco de conjunto (P5) e
  ir direto ao dicionário: o agrupamento por ano é o que alimenta a ART.1, o conjunto é
  reforço.

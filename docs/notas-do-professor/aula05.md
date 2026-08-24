# Notas do professor: Aula 05

**24/08/2026 &middot; Aprendizado Supervisionado parte I &middot; Sprint 2**

Material de condução do encontro. O conteúdo abaixo reúne as perguntas que abrem a sala quando ela
travar, cada uma com a resposta esperada e o erro que a pergunta costuma revelar. A ordem segue o
roteiro em `PLANEJAMENTO_AULA_A_AULA.md`.

**Aviso de condução:** esta é a aula que fecha a Sprint 2, com review em 28/08. A turma sai daqui
com o primeiro modelo do TAPI treinado e avaliado, e com a figura que alimenta a ART.4. A prática
precisa terminar com o número medido em cada máquina, porque a entrega pede o número, e não o
código que o produziria.

**Onde está o peso desta aula:** o Bloco 3 (11h00 a 11h30), que compara o modelo contra a baseline
da LDC. Um aluno que saia daqui sabendo ajustar `LinearRegression` e sem saber contra o que
comparar não aprendeu o que a aula ensina. Se algum bloco tiver de encolher ao vivo, que não seja
esse.

**O resultado desta aula é apertado, e isso é proposital.** O modelo ganha da baseline por 0,10
ponto percentual de MAPE. A tentação natural da turma será procurar uma métrica que favoreça o
modelo, ou concluir que modelar não valeu a pena. As duas reações são material de aula: a resposta
certa é medir mais vezes, que é o que o Bloco 4 faz com as doze janelas.

**Achado que contradiz a Aula 04, e precisa ser conduzido com cuidado.** A Aula 04 afirmou que
padronizar não muda as previsões de uma regressão sem regularização. Medido nesta base, o MAPE vai
de 1,71% para 1,60%, porque sem padronizar o solver zera os coeficientes de sazonalidade. A
afirmação da aula passada está correta em álgebra exata, e a aritmética de ponto flutuante tem um
limite que esta base atravessa. Vale assumir isso abertamente na sala: uma afirmação anterior sendo
refinada por medição nova é exatamente o que o método faz, e esconder a divergência ensinaria o
oposto.

**Dependência da aula anterior:** cada dupla precisa da base analítica da Aula 04 rodando. Quem não
tiver, abre `notebooks/aula05.ipynb`, cuja seção 2 reconstrói a base inteira a partir dos CSVs
crus, numa única célula. Ninguém fica parado por causa disso.

---

## 10h00 - 10h15 &middot; Daily

**Checkpoint de abertura:** cada dupla confirma que a base de frango com defasagem e sazonalidade
está pronta para treinar. Pergunte pelo `shape`: a resposta certa é `(113, 15)`. Quem responder
`(117, ...)` não aplicou o `dropna()` depois do `shift(4)`, e vai receber erro na primeira chamada
de `fit`.

Confirme também quem já começou a ART.4, porque a figura produzida hoje é o material dela e o prazo
é 28/08.

---

## 10h15 - 10h30 &middot; Resgate e pergunta de abertura

**Pergunta disparada:** "Por que não podemos embaralhar os 113 trimestres antes de separar treino e
teste?"

**Resposta esperada da turma:** "porque a ordem importa em série temporal."

**O que fazer com ela:** aceitar e ir adiante com "importa para quê?". A resposta rasa está certa e
não sustenta uma decisão de projeto. A resposta que interessa é que as duas formas de separar
respondem a perguntas diferentes, e só uma corresponde ao que a LDC vai fazer com o modelo:
projetar um trimestre que ainda não aconteceu.

**Erro comum que esta pergunta revela:** a turma costuma acreditar que embaralhar sempre infla a
métrica. Nesta base isso não acontece: o teste sorteado cobre períodos antigos, de menor volume, e
o MAPE ali sai pior. Se alguém levantar isso, é o melhor momento da aula. O argumento contra o
sorteio não depende de a métrica melhorar, e sim de ela deixar de responder à pergunta do parceiro.

**Se a sala travar:** pergunte quantos deles usariam um modelo que acerta o passado e nunca foi
testado no futuro.

---

## 10h30 - 10h45 &middot; Teoria: regressão linear, e a primeira prática

**Pergunta depois do ajuste:** "Somem os coeficientes de `frangos_lag1` e `frangos_lag4`. Que
número deu?"

**Resposta esperada:** 0,9966, praticamente 1.

**O que extrair disso:** o modelo aprendeu sozinho a prever cada trimestre como média ponderada
entre o passado recente (peso 0,68) e o mesmo trimestre do ano anterior (peso 0,31). Ninguém impôs
essa restrição. É o primeiro momento do módulo em que o modelo descobre uma estrutura que a turma
não programou, e vale nomear isso.

**Pergunta de fechamento do bloco:** "O `score` que vocês leram foi calculado sobre quais linhas?"

**Resposta esperada:** as mesmas do treino.

**Erro comum:** celebrar o R² de 0,99. Ele responde se o modelo reproduz o que já viu, que é a
pergunta mais fácil possível. Use isso como gancho para o Bloco 2.

**Tropeço técnico previsível:** passar uma `Series` como `X`, o que levanta erro de forma. A causa
é usar `analitica["frangos_lag1"]` em vez de `analitica[["frangos_lag1"]]`. Vale antecipar no
slide, porque trava quase toda dupla na primeira execução.

---

## 10h45 - 11h00 &middot; Prática: separação treino e teste

**Pergunta depois do sorteio:** "Com `train_test_split`, algum trimestre de 2025 foi parar no
treino? O que o modelo passou a saber que não deveria?"

**Resposta esperada:** sim, e o modelo passou a conhecer o nível de produção de um período
posterior ao que ele precisa prever.

**Erro comum:** achar que o problema é o modelo "ver a resposta". Não é bem isso: no sorteio ele vê
trimestres vizinhos, e não a linha de teste em si. O problema é a tarefa mudar de extrapolar para
interpolar, e a métrica passar a medir a tarefa fácil.

**O caso extremo, se sobrar tempo:** a demonstração com `shift(-1)` derruba o MAPE de 1,69% para
1,13%, sem erro nenhum no console. Use para fechar: a métrica de um modelo vazado é justamente a
que parece boa, então ela não serve de alarme.

**Cuidado técnico ao conduzir:** a coluna do futuro precisa ser criada numa cópia da base.
`shift(-1)` seguido de `dropna()` consome a última linha, e todas as métricas mudam junto. Se
alguma dupla obtiver números diferentes dos do slide, é quase sempre isso.

---

## 11h00 - 11h15 &middot; Teoria: RMSE e MAPE

**Pergunta disparada:** "Se eu disser que o modelo erra 67 milhões de quilos, isso é muito ou
pouco?"

**Resposta esperada:** depende do tamanho da produção, que é da ordem de 3,5 bilhões de kg no
período. Daí sai a necessidade da segunda métrica.

**O que registrar:** RMSE conversa com o parceiro na unidade em que ele compra ração; MAPE permite
comparar entre séries de tamanhos diferentes. As duas armadilhas do MAPE (explodir perto de zero, e
ser assimétrico entre subestimar e superestimar) valem ser ditas, porque a turma vai usar MAPE em
todas as aulas seguintes.

**Erro comum:** tratar R² como métrica de avaliação. Ele compara contra prever sempre a média, que
é uma régua fraca numa série com tendência de crescimento. A régua útil é o processo atual da LDC.

---

## 11h15 - 11h30 &middot; Prática: métricas e baseline

**Pergunta de fechamento, e é a mais importante do dia:** "Pelo que vocês mediram, vocês
recomendariam este modelo à LDC no lugar do processo atual?"

**Resposta esperada:** hesitação. O modelo ganha por 0,10 ponto percentual, e oito trimestres são
poucos.

**O que fazer com a hesitação:** validá-la. Ela é a resposta tecnicamente correta neste ponto da
aula, e é ela que motiva o Bloco 4. Um aluno que responda "sim, claro" com esse número não leu a
margem; um que responda "não, nunca" está descartando o modelo cedo demais.

**Ponto que costuma passar despercebido, e vale forçar:** a baseline B (repetir o ano anterior sem
correção) erra 4,54%, e a baseline C (com o fator de 1,05) erra 1,69%. Uma linha de aritmética
resolveu a maior parte do problema, antes de qualquer modelo. Pergunte quanto do trabalho de hoje
seria dispensável se ninguém tivesse medido a baseline.

**Sobre o leite:** quem acrescentou `producao_leite` viu o MAPE de treino cair e o de teste subir.
Esse é o exemplo de overfitting da aula, e ele fecha a hipótese que a Aula 04 deixou aberta. Não
antecipe o resultado: deixe cada dupla medir.

---

## 11h30 - 11h45 &middot; Overfitting e reprodutibilidade

**Discussão dirigida:** cada dupla aponta um sintoma de overfitting no próprio resultado, ou declara
que não encontrou nenhum e mostra os dois MAPE que sustentam isso.

**Resposta esperada:** a distância entre MAPE de treino e de teste, e o caso do leite.

**Erro comum:** confundir "erro de teste maior que o de treino" com overfitting. Nesta base o erro
de teste é *menor* que o de treino (1,60% contra 2,53%), porque os oito trimestres reservados
são um período mais estável que os 29 anos do treino. Overfitting se caracteriza pela direção do
movimento ao acrescentar característica, e não pelo nível absoluto das duas métricas.

**As doze janelas:** conduza como resposta à hesitação do bloco anterior. O modelo vence nas doze,
com média de 2,18% contra 3,14%. A vantagem apertada da última janela é o pior caso das doze.
Diga também a ressalva: as janelas se sobrepõem, então não são doze medidas independentes.

**Pergunta de fechamento:** "Se a LDC pedisse previsão para 2026-T2, o que vocês precisariam ter em
mãos que hoje ainda não têm?"

**Resposta esperada:** o valor de 2026-T1 (que a base já tem) e a decisão de reajustar o modelo
sobre a base completa, incluindo os oito trimestres reservados. Esse reajuste é assunto da Aula 12,
com `Pipeline`, e vale deixar registrado como pendência conhecida.

---

## 11h45 - 12h00 &middot; Amarração com a sprint

**O que declarar:** a ART.4 (UX parte 2, peso 3) recebe a figura de histórico contra previsão, e
é a única ART que a matriz do `PLANO_DE_ENSINO.md` (seção 5) amarra a esta aula. O Shapiro-Wilk
dos resíduos fecha o ciclo aberto na Aula 04 sobre as variáveis, e a ART.5 está amarrada lá, não
aqui: vale dizer isso à turma, para ninguém achar que a entrega de hoje mudou. A Sprint 2 fecha em
28/08, e a Sprint 3 abre em 31/08.

**Três cuidados a passar sobre a figura da ART.4**, porque é o que separa uma entrega boa de uma
mediana: marcar onde termina o histórico e começa a projeção; mostrar a baseline junto do modelo; e
declarar o erro em número dentro da própria figura.

**Ponte para a Aula 06:** o alvo muda. Hoje existe uma coluna-resposta contra a qual medir o erro; a
Aula 06 procura estrutura sem nenhuma resposta disponível. Vale plantar a pergunta que abre lá:
quais trimestres se parecem entre si na demanda de ração?

---

## Perguntas soltas, para quando sobrar tempo

- "Por que o modelo erra sempre para o mesmo lado nos oito trimestres de teste?" (sete dos oito
  ficam abaixo do realizado). Resposta: viés de nível, provavelmente por a tendência recente ser
  mais forte que a média dos 29 anos de treino. Um erro sistemático se corrige com um ajuste de
  nível, e é por isso que vale a pena olhar o sinal dos resíduos antes do tamanho deles.
- "As outras quatro séries defasadas derrubam o MAPE para 1,14%. Por que não usamos?" Resposta: nós
  vamos, na Aula 07. Hoje o objetivo é o ciclo completo com o modelo mais simples que funciona.
- "O que aconteceria se usássemos `producao_leite` do mesmo trimestre?" Resposta: exigiria conhecer
  a produção de leite de 2026-T1 para prever o frango de 2026-T1, e as duas são publicadas juntas.
  É vazamento, e ele passa despercebido porque a coluna não tem nada de "futuro" no nome.

---

## Registro de divergência editorial

O cabeçalho deste arquivo difere do das Aulas 01 a 04. As quatro anteriores usam uma construção de
paralelismo negativo que as diretivas de tom do acervo proíbem, e o alinhamento das quatro está
listado em `docs/ANDAMENTO.md` como decisão pendente do professor. Este arquivo já nasce na forma
nova. Alinhar os quatro anteriores é uma edição de dois minutos, quando houver decisão.

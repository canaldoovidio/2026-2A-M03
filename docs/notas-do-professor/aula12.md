# Notas do professor: Aula 12

**29/09/2026 &middot; Deploy de modelo e criação de pipeline de processamento &middot; Sprint 5**

Material de condução do encontro. O conteúdo abaixo reúne as perguntas que abrem cada bloco quando
a sala travar, cada uma com a resposta esperada e o erro que a pergunta costuma revelar. A ordem
segue os sete blocos da divisão dos 105 minutos registrada na
`docs/adrs/ADR-015-empacotamento-do-modelo-e-escopo-da-aula-12.md`, e todos os números vêm de
`tools/tests/test_pipeline_aula12.py`, que trava as quinze conclusões da aula.

**Onde está o peso desta aula:** o slide 12, com a figura do deslocamento. Os coeficientes se movem
numa mediana de 17,2% e um deles troca de sinal; a previsão não chega a 1%. A turma precisa sair
com a consequência disso, que é um critério de entrega: o número que a dupla publica é estável, e
a frase explicativa que ela publica precisa ser conferida antes. Um aluno que saia daqui achando
que "o modelo ficou instável" aprendeu a coisa errada e vai querer desfazer um reajuste que está
certo.

**Esta aula abre a Sprint 5, e há duas coisas no radar da turma além da ART.8.** A Prova 02/10 vale
20, e a Aula 13 é amanhã. O bloco de amarração precisa deixar as três datas na parede.

---

## Checkpoint de abertura, antes de qualquer coisa

**A pergunta que abre a sala:** todo mundo tem o modelo da Aula 11 rodando?

A aula inteira parte de um modelo já escolhido. Quem não fechou a Aula 11 não tem o que empacotar,
e o conserto é a seção 1 do `notebooks/aula12.ipynb`, que remonta a base e reajusta o vencedor em
uma célula. **Mande rodar essa célula no começo**, porque ela é o pré-requisito das três práticas.

O `mlflow` é instalado pela seção 5 do notebook e demora um pouco na primeira vez. Se o wi-fi da
sala for ruim, mande instalar já no checkpoint, e não às 11h30.

**A segunda pergunta, se sobrar tempo:** a Sprint 5 teve planning ontem. Peça a duas ou três duplas
o que elas colocaram como Modelo Final no board. Quem respondeu "o notebook da Aula 11" acabou de
ilustrar a pergunta disparada do slide 4.

---

## Ordem de corte, se o tempo apertar

1. **O slide 14, da distinção com a Aula 05.** É o primeiro a ceder, porque cabe em uma frase dita
   apontando para a tabela: padronizar levou o condicionamento de 3,22e9 para 28,5 e deixou o VIF
   em 69, são problemas diferentes. A seção 6 do material cobre o resto com calma.
2. **O slide 17, da divergência de versão.** Cede em segundo lugar, virando uma frase: o aviso
   aparece três vezes, a previsão não muda, e voltar para a versão antiga no Python 3.14 nem
   instala. O que **não** pode cair é a conclusão prática, que é declarar a versão junto com o
   modelo, porque ela entra no checklist da ART.8.
3. **A prática das 11h15 pode virar dever de casa**, se as duas primeiras práticas atrasarem. É a
   menos arriscada de deslocar, porque o notebook faz o caminho inteiro e a dupla só precisa
   repetir na própria base.

**O que nunca cai:** os slides 11 e 12. São o achado da aula e o critério da ART.8.

---

## Bloco 1, 10h15 às 10h30. Resgate e a pergunta disparada

**A pergunta:** a dupla de vocês manda por e-mail, hoje, o modelo da Aula 11 para a LDC. O que
exatamente vai anexado?

**A resposta esperada:** o objeto do modelo. É a resposta que quase toda sala dá, e ela está
incompleta.

**O que a pergunta revela:** que o escalador some da conta. O modelo foi ajustado sobre entradas
padronizadas, com onze médias e onze desvios medidos no treino, e esses 22 números não estão dentro
do objeto `modelo`. Do outro lado, alguém passa a base de setembro em unidades de 1e9 a um modelo
que espera valores em torno de zero, e a previsão sai `2,63e17` quilogramas num mês em que o IBGE
mediu `1,19e9`: **231 milhões de vezes maior**, sem que nada no código acuse.

**Se a sala responder certo de primeira**, aprofunde: além do escalador, o que mais? A resposta
completa tem quatro itens, e três não estão dentro de nenhum objeto do scikit-learn: a ordem das
colunas, a definição de cada feature derivada e a versão da biblioteca. Esse é o gancho para o
bloco das 11h00.

---

## Bloco 2, 10h30 às 10h45. O que o `Pipeline` encapsula

**A pergunta:** encapsular os dois objetos num `Pipeline` melhora o resultado?

**A resposta esperada:** não. MAPE de 2,8620136234% pelos dois caminhos, e `array_equal` verdadeiro
nas 24 previsões.

**O que a pergunta revela:** o hábito de supor que toda boa prática traz ganho de métrica. Esta não
traz, e dizer isso com todas as letras é o que dá credibilidade ao argumento verdadeiro, que vem em
seguida.

**Cuidado com um atalho tentador.** Vai aparecer a resposta "o `Pipeline` evita vazamento". Nesta
base, não evita nada mensurável: a Aula 05 mediu que ajustar o escalador sobre treino e teste
juntos devolve MAPE idêntico até a nona casa, porque regressão linear sem regularização é
invariante a transformação afim das entradas. **Não deixe essa resposta passar como certa.** O
argumento correto é o do slide 8: dentro do `TimeSeriesSplit` da Aula 10, o escalador precisa ser
reajustado por dobra, e o `Pipeline` tira isso da memória de quem escreve o laço.

Se alguém insistir que o vazamento importa, está parcialmente certo e vale reconhecer: importa com
KNN, SVM, regressão regularizada e PCA, que o acervo usou entre as Aulas 06 e 08.

---

## Bloco 3, 10h45 às 11h00. Prática do `Pipeline`

**Circule olhando uma coisa só:** se as previsões do caminho antigo e do novo batem. Quando não
batem, o motivo quase sempre é a ordem das colunas, e não o `Pipeline`.

**A pergunta para quem terminar cedo:** quantos números o objeto carrega além dos coeficientes?
Resposta: 22, as onze médias e os onze desvios. É o mesmo número da pergunta disparada do bloco 1,
e fechar esse ciclo em voz alta ajuda a sala inteira.

---

## Bloco 4, 11h00 às 11h15. O que se exporta

**É o bloco mais denso da aula, e isso é deliberado** (`ADR-015`). São três assuntos: o reajuste, o
`joblib` e a divergência de versão. Sugestão de repartição: sete minutos no reajuste, três no
`joblib`, cinco na versão.

**A pergunta:** a avaliação terminou e o modelo está escolhido. Vocês exportam o objeto que foi
avaliado, treinado em 315 meses, ou reajustam sobre os 339?

**A resposta esperada:** reajustar. Deixar 24 meses de dado real do IBGE fora do modelo que vai
para a LDC é desperdício, e não há mais nada a decidir que pudesse ser contaminado.

**A segunda pergunta, e é onde a aula acontece:** então qual MAPE vai no relatório? O reajustado
erra 2,65% nos 24 meses de teste, e o avaliado erra 2,86%.

**O que a pergunta revela:** metade da sala vai escolher o 2,65%, porque descreve o objeto que de
fato foi exportado, e é um raciocínio razoável. O erro é que esse objeto treinou com esses 24
meses. É o vazamento da Aula 09 numa forma nova, e ela aparece exatamente no momento de empacotar,
que é quando ninguém está mais desconfiado.

**Depois disso, mostre a figura do slide 12 sem antecipar a conclusão.** Pergunte o que a turma
espera que tenha acontecido com a previsão, dado que um coeficiente trocou de sinal. A expectativa
natural é que a previsão tenha mudado muito. Ela mudou 0,97% no pior mês.

**A pergunta de fechamento do bloco:** se os coeficientes se movem tanto e a previsão não, o que
isso diz sobre usar coeficiente como explicação?

---

## Bloco 5, 11h15 às 11h30. Prática do export

**Circule olhando duas coisas:** se a dupla reajustou antes de exportar, e se ela anotou o MAPE do
objeto **avaliado** junto do arquivo.

**A pergunta para o fechamento:** algum coeficiente trocou de sinal na base de vocês? Colha duas ou
três respostas em voz alta. Quem tiver features menos correlacionadas vai ver deslocamento menor, e
isso é conteúdo: o efeito é da colinearidade, e não uma propriedade universal de reajuste.

---

## Bloco 6, 11h30 às 11h45. MLflow

**Avise no começo do bloco que o comando do autoestudo não funciona.** Não é erro da dupla: a
versão atual da biblioteca recusa a pasta `mlruns/` e devolve
`MlflowException: The filesystem tracking backend is in maintenance mode`. A aula usa
`sqlite:///mlflow.db`. Mudam duas linhas, e o slide 20 tem as duas.

Se não avisar antes, o bloco inteiro vira suporte técnico.

**A pergunta:** olhando só para a tela do MLflow, daqui a três meses alguém consegue refazer este
modelo?

**A resposta esperada:** depende do que foi registrado. Com modelo, alvo, features, meses de
treino, corte de teste, versão do scikit-learn e último mês da base, consegue.

**O que a pergunta revela:** o que ficou de fora. Quase nenhuma dupla registra a versão da
biblioteca de primeira, e é justamente o item que o bloco anterior mostrou ser decisivo.

**O ponto do slide 21, e vale insistir:** a execução de produção é registrada **sem** `mape_teste`,
com uma tag explicando a ausência. Pergunte por que não se repete ali o 2,86% da outra execução. A
resposta é que aquele número descreve outro objeto, e um registro que o copiasse estaria mentindo
para quem ler daqui a três meses.

---

## Bloco 7, 11h45 às 12h00. Quiz e amarração com a ART.8

**O quiz 1 é sobre os dois MAPE**, e é a armadilha central da aula. Se a maioria acertar de
primeira, ótimo, siga. Se errar, volte ao slide 11 e refaça a pergunta: qual dos dois objetos viu
os 24 meses de teste?

**O quiz 2 é sobre a colinearidade.** A alternativa errada mais atraente é a de que faltou
padronizar, porque ela mistura esta aula com a Aula 05. Se alguém a escolher, use a tabela do slide
14 para desarmar.

**Na amarração, três datas na parede:** Aula 13 amanhã, 30/09; Prova 02/10, peso 20; review da
Sprint 5 em 07/10, com a ART.8 valendo 4.

**A última frase da aula,** que prepara a de amanhã: o arquivo de 1,5 KB que a dupla acabou de
exportar é o que vai ser carregado dentro do app Streamlit, e a partir dali quem olha para o modelo
não é mais a dupla, é a LDC.

---

## Erros que a turma costuma cometer nesta aula

| Erro | Onde ele aparece | Como desarmar |
| --- | --- | --- |
| Publicar o MAPE do modelo reajustado | prática das 11h15 e ART.8 | Perguntar qual objeto viu os 24 meses de teste |
| Concluir que o modelo ficou instável | depois do slide 12 | A previsão se move 0,97%; o modelo está bom |
| Achar que faltou padronizar | slide 13, e no quiz 2 | Tabela do slide 14, condicionamento contra VIF |
| Dizer que o `Pipeline` evita vazamento | bloco 2 | Nesta base não evita; o argumento é a dobra |
| Exportar sem o escalador | prática das 11h15 | É a pergunta disparada do bloco 1, de volta |
| Registrar sem a versão da biblioteca | bloco 6 | O bloco 4 acabou de mostrar por que ela importa |
| Usar `mlruns/` porque o autoestudo usa | bloco 6 | Avisar antes do bloco, não durante |

---

## Números da aula, para consulta rápida

| Medida | Valor |
| --- | --- |
| Base | 339 linhas, 1998-01 a 2026-03 |
| Treino do objeto avaliado | 315 meses, até 2024-03 |
| Teste | 24 meses, 2024-04 a 2026-03 |
| MAPE do avaliado, o número honesto | 2,8620% |
| MAPE do reajustado no mesmo teste | 2,6492%, sem significado |
| `Pipeline` contra passo a passo | idêntico bit a bit |
| Deslocamento dos coeficientes | mediana de 17,2%, máximo de 3.439% |
| Coeficiente que troca de sinal | `abate_bovinos_lag1`, de -93.404 para +3.118.714 |
| Deslocamento das previsões | 0,65% em média, 0,97% no máximo |
| Pares de features com r acima de 0,90 | 20 |
| Maior VIF | 69,0 em `lag1`; sete das onze acima de 10 |
| Condicionamento, cru e padronizado | 3,22e9 e 28,5 |
| Tamanho do `.joblib` | 1.481 bytes |
| Avisos ao carregar 1.7.2 na 1.9.1 | 3, e previsão idêntica |
| Previsão sem o escalador | `2,63e17` contra `1,19e9`, 231 milhões de vezes maior |

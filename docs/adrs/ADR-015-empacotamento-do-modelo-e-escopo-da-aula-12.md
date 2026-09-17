# ADR-015: A Aula 12 exporta o modelo reajustado sobre a base completa, versiona o binário junto com o script que o produz, e usa o MLflow sobre SQLite no lugar da pasta que o autoestudo ensina

**Data:** 17/09/2026
**Status:** Aceita
**Decisores:** Prof. Ovidio Lopes da Cruz Netto e José Romualdo

## Contexto

A Aula 12, em 29/09/2026, abre a Sprint 5 e tem o roteiro do
`PLANEJAMENTO_AULA_A_AULA.md` dividido em três ferramentas: `Pipeline` do scikit-learn, exportação
com `joblib` e rastreamento com MLflow. O modelo a empacotar é o vencedor da Aula 11 (`ADR-014`),
regressão linear sobre o alvo em nível, com 2,86% de MAPE nos 24 meses de teste.

Quatro problemas apareceram na medição, antes de qualquer slide.

**O roteiro não diz sobre qual ajuste o modelo é exportado.** Ele manda "exportar o próprio
`Pipeline`", e existem dois objetos possíveis: o avaliado, treinado nos 315 meses e medido nos 24
que não viu, e um reajustado sobre as 339 linhas. O `docs/ANDAMENTO.md` já registrava, desde a
construção da Aula 05, que "o reajuste do modelo sobre a base completa, depois de a avaliação
terminar, fica para a Aula 12 junto com o `Pipeline`". A dívida chegou sem estar resolvida.

**Medindo os dois, o resultado é maior que a pergunta.** Passar de 315 para 339 meses desloca os
coeficientes numa mediana de **17,2%**, e o de `abate_bovinos_lag1` **troca de sinal**, de -93.404
para +3.118.714, um deslocamento relativo de 3.439%. A previsão nos mesmos 24 meses se move
**0,65% em média e 0,97% no máximo**. A razão entre as duas grandezas é de cerca de 27 vezes.

A causa está medida: na matriz de correlação do treino padronizado, **vinte pares de features
passam de r = 0,90**, e o fator de inflação da variância chega a **69,0** em `lag1`, com sete das
onze features acima do limiar usual de 10. Com entradas colineares, muitas combinações de
coeficientes produzem quase o mesmo ajuste, e um punhado de linhas novas basta para inclinar a
escolha entre elas.

Há uma armadilha adjacente, e ela é do próprio acervo. A Aula 05 mediu número de condição de
1,08e10 nesta mesma família de dados e resolveu o problema padronizando. **Aqui padronizar não
resolve**: o número de condição cai de 3,22e9 para 28,5 e o VIF de `lag1` continua em 69,0.
Condicionamento numérico e colinearidade estatística são problemas diferentes com a mesma
aparência, e um material que não fizesse a distinção levaria a dupla a concluir que a Aula 05
estava errada.

**O `Pipeline` não produz o ganho que se espera dele.** Encapsular `StandardScaler` e
`LinearRegression` devolve previsão **idêntica bit a bit** ao passo a passo da Aula 11, com MAPE de
2,8620136234% nos dois caminhos e `numpy.array_equal` verdadeiro. O argumento a favor dele não pode
ser precisão. E o argumento fácil seguinte, o de vazamento, também não se sustenta nesta base: a
Aula 05 já tinha medido que ajustar o escalador sobre treino e teste juntos devolve MAPE idêntico
até a nona casa, porque regressão linear sem regularização é invariante a transformação afim das
entradas.

**O MLflow atual recusa o backend que o autoestudo ensina.** O item "MLflow: primeiros passos
(rastreamento de experimentos)", da Semana 09, usa a pasta `mlruns/`, que foi o padrão da
ferramenta por anos. A versão instalada (3.16.1) devolve, na abertura:

```
MlflowException: The filesystem tracking backend (e.g., './mlruns') is in maintenance mode
and will not receive further updates. Please migrate to a database backend
(e.g., 'sqlite:///mlflow.db')
```

É o mesmo tipo de descompasso entre autoestudo e biblioteca que a `ADR-014` registrou para o
PyCaret, com uma diferença importante: aqui não há custo de ambiente. Instalar o `mlflow` não
rebaixou `scikit-learn` (1.9.1), `pandas` (3.0.5) nem `numpy` (2.5.2), conferidos depois da
instalação.

## Decisão

A aula exporta o `Pipeline` **reajustado sobre as 339 linhas**, publica junto dele o MAPE medido no
objeto **avaliado**, versiona o binário em `app/` acompanhado do script que o gera, e usa
`sqlite:///mlflow.db` como backend do MLflow.

## Motivações

**Exportar o reajustado, e publicar o número do avaliado.** A avaliação terminou na Aula 11: não há
mais nada a decidir, e deixar 24 meses de dado real do IBGE fora do modelo que vai para a LDC seria
desperdício. Mas o MAPE do objeto reajustado nos mesmos 24 meses é 2,6492%, melhor que o 2,86% e
sem significado, porque ele treinou com esses meses. Os dois números convivem na aula de propósito,
e o slide 11 existe para a dupla não publicar o menor. É o vazamento da Aula 09 numa forma nova,
que aparece justamente no momento de empacotar.

**O achado do reajuste vira o centro do bloco de export, no lugar de uma descrição de risco.** O
contraste entre 17,2% nos coeficientes e 0,97% na previsão dá à aula o que ela precisava: uma razão
concreta para a dupla não publicar leitura de coeficiente sem conferir a estabilidade dela. Isso
amarra a Aula 10, que ensinou SHAP e partial dependence, ao momento de entrega da ART.8, e
transforma uma recomendação abstrata em critério verificável.

**Versionar o `.joblib`, e junto o comando que o produz.** A Aula 13 carrega este arquivo dentro do
app Streamlit, então ele precisa existir no repositório. São 1.481 bytes. Um binário commitado sem
comando declarado é um arquivo que ninguém pode auditar, por isso ele é gerado por
`tools/exportar_modelo_aula12.py` e `tools/tests/test_pipeline_aula12.py` regenera o modelo do zero
e compara **coeficientes e previsões** com o arquivo versionado.

O teste nunca compara o hash do arquivo: o pickle grava metadado de ambiente e o mesmo modelo
produz bytes diferentes em máquinas diferentes. O que precisa ser reproduzível é o modelo, não o
binário.

**Versionar também o `.joblib` gravado com scikit-learn 1.7.2.** O acervo tem um segundo binário,
`app/modelo_aula12_sk172.joblib`, de 1.481 bytes, cuja única função é ser o fixture do teste de
divergência de versão. Sem ele, a afirmação "três avisos e previsão idêntica bit a bit" ficaria sem
cobertura no CI, porque gerá-lo exige um segundo interpretador. Com ele, o CI verifica a afirmação
a cada push.

Procedimento para regerá-lo, se um dia for preciso: criar um ambiente virtual, instalar
`scikit-learn==1.7.2` nele, ajustar o mesmo `Pipeline` sobre a base completa e gravar no destino. A
versão 1.7.2 foi escolhida por ser **a mais antiga com wheel para o Python 3.14**, o que a torna o
maior salto de versão testável sem compilar do zero.

**SQLite no MLflow.** É a alternativa que a própria mensagem de erro indica, é um arquivo só, não
exige servidor e roda igual no Colab. Mudam duas linhas em relação ao autoestudo, a do
`set_tracking_uri` e a do `mlflow ui`, e tudo o que a leitura ensina sobre *o que* registrar
continua valendo.

**A execução de produção é registrada sem `mape_teste`.** Ela não pode ter essa métrica, porque não
existe conjunto fora da amostra para ela, e no lugar do número entra uma tag declarando a ausência.
É o que torna o registro capaz de dizer que uma execução não tem determinada métrica, em vez de
repetir o número da vizinha.

## Riscos conhecidos

**O bloco das 11h00 carrega três assuntos em 15 minutos** (reajuste, `joblib` e divergência de
versão). Foi mantido inteiro em vez de dividido, porque dividir exigiria tirar tempo de outro
bloco, e o candidato natural, a prática das 10h45, é onde a dupla monta o próprio `Pipeline`, que é
o pré-requisito de tudo o que vem depois. Mitigação: a profundidade dos três está nas seções 4, 8 e
9 do material e nas seções 3 e 4 do notebook, e as notas do professor trazem a ordem de corte.

**Dois números de MAPE circulando na mesma aula é convite a confusão.** Um aluno que troque o 2,86%
pelo 2,65% inverte a lição inteira. Mitigação: os dois aparecem sempre na mesma tabela, com o
objeto declarado na linha, o quiz 1 é exatamente sobre essa distinção, e o cabeçalho do deck marca
o ponto como a armadilha central.

**A distinção entre condicionamento e colinearidade é sutil e contradiz a intuição construída na
Aula 05.** Mitigação: a seção 6 do material apresenta as duas medidas lado a lado, antes e depois
de padronizar, e afirma explicitamente que a Aula 05 continua certa.

**A medição de divergência de versão não generaliza.** Ela atravessou três versões menores num
`Pipeline` de dois estimadores simples. Um estimador com atributo renomeado entre versões falha na
carga. Mitigação: a seção 9 do material declara o escopo e reposiciona a conclusão no ponto que
generaliza, que é o aviso não distinguir os dois casos.

**O `mlflow` entra no `requirements-ci.txt` sem versão fixada**, como o resto do arquivo. Se uma
versão futura mudar de novo o backend recomendado, o notebook quebra no CI. Mitigação: é o mesmo
risco que o acervo já aceita para as outras dependências, e o CI executa os notebooks a cada push,
então a quebra aparece no dia em que acontece e não no dia da aula.

## Consequências

**Positivas.** A aula ganhou um achado medido no lugar de uma descrição de risco, e ele amarra a
explicabilidade da Aula 10 ao empacotamento da Sprint 5. A dívida registrada desde a Aula 05 sobre
o reajuste está quitada. O CI passa a cobrir também a divergência de versão, que antes seria uma
afirmação sem teste. A Aula 13 recebe um arquivo pronto, versionado e auditável.

**Negativas.** O repositório passa a ter dois binários versionados, o que é uma novidade no acervo
e exige a disciplina do script gerador. A aula carrega dois números de MAPE que precisam ser
distinguidos o tempo todo. O bloco das 11h00 fica denso. E a aula diverge do autoestudo em um
ponto, o backend do MLflow, o que exige o parágrafo de conversão no material e nas referências.

**Entradas novas no `.gitignore`:** `saida/`, `mlflow.db`, `mlruns/` e `mlartifacts/`. O notebook
grava o modelo em `notebooks/saida/` e registra os experimentos num banco local, e os três
reprovariam o passo "A árvore de trabalho precisa continuar limpa" do CI, como o `logs.log` do
PyCaret já reprovou na Aula 11.

## ADRs relacionadas

- `ADR-014`, que escolheu o modelo que esta aula empacota, e que registrou o primeiro descompasso
  entre autoestudo e versão de biblioteca do acervo.
- `ADR-013`, que fixou o `TimeSeriesSplit` como validador da trilha, e é o motivo pelo qual o
  `Pipeline` importa apesar de não mudar número nenhum.
- `ADR-008`, que fixou o corte temporal de que sai o 2,86%.
- `ADR-007`, que definiu a base analítica cujas features colineares produzem o achado desta aula.

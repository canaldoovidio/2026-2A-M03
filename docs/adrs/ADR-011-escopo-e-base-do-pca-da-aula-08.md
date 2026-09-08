# ADR-011: A Aula 08 roda PCA sobre as 11 features da base mensal, ensina escolha de K pelo contraste já medido e reduz sistemas de recomendação a fecho conceitual

**Data:** 08/09/2026
**Status:** Aceita
**Decisores:** Prof. Ovidio Lopes da Cruz Netto e José Romualdo

## Contexto

A Aula 08, em 10/09/2026, chegou à construção com quatro assuntos para 105 minutos de instrução.
Dois vinham do roteiro original em `PLANEJAMENTO_AULA_A_AULA.md` (PCA nos drivers macroeconômicos
e sistemas de recomendação) e dois entraram pela `ADR-009`, que moveu Elbow Plot e Silhouette
Analysis da Aula 06 para cá. O próprio registro da ampliação já dizia que a aula precisaria de um
corte compensatório, deixando a decisão para o momento da construção.

Além do excesso de assuntos, o roteiro tinha um problema de fonte. A prática de PCA estava escrita
como "cada dupla roda PCA sobre as colunas de preço e disponibilidade dos macroingredientes
(milho, farelo de soja, sorgo, trigo, DDGS) dos boletins do Sindirações". Não existe série aberta
do Sindirações em `dados/`, e a `ADR-007` já havia corrigido a mesma citação na Aula 04: o acervo
tem as cinco séries do IBGE/SIDRA e nada mais. Como dado sintético é proibido onde deveria haver
dado real, a prática não podia ser escrita como estava.

Antes de qualquer slide, os dois blocos foram medidos sobre os CSVs versionados, e as duas
medições apontam para a mesma conclusão.

**Escolha de K, sobre as duas bases trimestrais da Aula 06.** Na base de participação de cada
trimestre no total do próprio ano, a queda de inércia é de 25,1% de K=2 para K=3 e de 14,3% de
K=3 para K=4, então o Elbow Plot aponta K=3. A silhueta é máxima em K=2 (0,3785) e cai para
0,2853 em K=4. O único K que recupera o trimestre do calendário é 4, com 98,3% de concordância,
contra 75,0% em K=3 e 50,0% em K=2. Os dois critérios internos apontam valores diferentes entre
si, e nenhum dos dois aponta o valor que serve ao case. Na base de níveis, a silhueta é maior em
todo K (de 0,4247 a 0,5639) e a concordância com o calendário fica entre 25,6% e 29,1%, que é o
acaso.

**PCA, sobre as 11 features da base mensal da Aula 07** (339 linhas, treino de 315 meses, teste de
24). PC1 vale 68,21% da variância e pesa entre 0,336 e 0,362 nas oito colunas em quilos, com peso
abaixo de 0,021 em `sen`, `cos` e `dias`: é o nível comum das cinco séries. PC2 (11,85%) e PC3
(9,24%) carregam o calendário, e agrupar os 315 meses de treino em 12 grupos no plano PC2 por PC3
recupera o mês em 91,7% das linhas, com silhueta de 0,8037 para os rótulos verdadeiros de mês,
sem que nenhuma coluna da matriz seja o número do mês. Quatro componentes chegam a 96,07% da
variância.

O ponto que decide o desenho da aula é o custo do corte. O modelo do fecho da Aula 07 tem MAPE de
teste de 3,32% com as 11 features, contra 3,71% da baseline de coeficiente fixo da LDC. Reduzindo
a dimensionalidade por PCA, o MAPE vai a 4,92% com dois componentes, 4,94% com quatro e 6,20% com
nove, e o modelo perde da baseline em todo k de 1 a 9. Só k=10 devolve os 3,32%. O motivo está nos
coeficientes: PC9 e PC10, que valem 0,21% e 0,17% da variância, recebem coeficiente 22 e 27 vezes
o do PC1. Com os 11 componentes o MAPE é idêntico ao das 11 features até a nona casa decimal,
porque PCA sem descarte é rotação, o que confirma a invariância medida na Aula 05.

## Decisão

A Aula 08 roda PCA sobre as 11 features da base analítica mensal que a Aula 07 deixou pronta,
ensina Elbow Plot e Silhouette Analysis a partir do contraste já medido nas bases da Aula 06, e
reduz sistemas de recomendação de bloco com discussão dirigida de 15 minutos para fecho conceitual
de 10 minutos, sem prática.

A divisão dos 105 minutos fica assim:

| Bloco | Minutos |
| --- | --- |
| Resgate da Aula 07 e pergunta disparada | 15 |
| Escolha de K por Elbow Plot e Silhouette Analysis | 25 |
| PCA: variância explicada, loadings e uma prática | 45 |
| Sistemas de recomendação como fecho conceitual | 10 |
| Amarração com a ART.6 e a Sprint 3 | 10 |

Escalador e PCA são ajustados apenas nos 315 meses de treino, nunca na base inteira.

## Motivações

- **A prática de PCA precisava de dado real, e as 11 features são o dado real mais próximo do que
  o roteiro queria.** O roteiro pedia redução de dimensionalidade nos drivers que alimentam o
  Modelo 2 e o Modelo 3. As 11 features são exatamente os drivers do Modelo 1 já construídos e
  validados, com 20 dos 55 pares de colunas acima de 0,9 de correlação absoluta, o que dá à
  pergunta disparada do roteiro ("quantas variáveis vocês acham que realmente são independentes
  entre si?") uma resposta medida na própria base do case.
- **Os dois blocos passam a sustentar a mesma tese, e isso é o que permite cortar tempo sem
  perder conteúdo.** Inércia, silhueta e variância explicada são critérios internos da técnica, e
  nas duas medições eles apontam para longe do que o case precisa: o K que recupera o calendário
  tem a pior silhueta, e os componentes de menor variância são os que fazem o modelo bater a
  baseline. Uma aula com uma tese e dois exemplos cabe em 105 minutos; quatro assuntos
  independentes não cabem.
- **Sistemas de recomendação é o assunto que menos perde com o corte.** É o único dos quatro sem
  dado no acervo para sustentar prática, e os cinco autoestudos da Semana 06 são inteiramente
  sobre ele (`docs/autoestudos-por-semana.md`), incluindo duas implementações. A analogia com o
  desdobramento de ração entre macroingredientes do Modelo 3 continua na aula, como fecho.
- **Ajustar o PCA só no treino mantém a disciplina que a Aula 05 estabeleceu** e prepara o bloco
  de vazamento temporal da Aula 09. Medido nesta base, ajustar na base inteira leva PC1 de 68,21%
  para 68,52% e o MAPE de k=4 de 4,94% para 4,91%: o efeito é pequeno e sempre na direção
  otimista, que é justamente o que torna o erro difícil de perceber sem disciplina.

## Riscos conhecidos

- **A aula afirma que PCA piora este modelo, e a dupla pode generalizar a afirmação.** Mitigação:
  o material e as notas do professor declaram o escopo da conclusão (regressão linear sem
  regularização, 11 features, 339 linhas) e citam o caso medido em que a redução compensa. No
  mesmo protocolo, `KNeighborsRegressor(n_neighbors=5)` sobre quatro componentes tem MAPE de
  **4,78%**, contra 5,01% sobre as 11 features padronizadas: no KNN o corte melhora a previsão,
  ainda que o modelo siga acima da baseline de 3,71% da LDC. A direção do efeito depende do
  modelo, e a Aula 09 retoma o assunto no bloco de dimensionalidade.
- **A prática única de PCA concentra o risco de execução.** Se o ambiente da dupla falhar, ela
  perde o único momento de mão no código do bloco. Mitigação: o notebook traz a célula de PCA
  independente das anteriores, com os dados carregados do CSV versionado e o mesmo tratamento de
  erro de rede que a Aula 06 introduziu.
- **Sistemas de recomendação fica com 10 minutos e cinco autoestudos.** A Semana 06 pede o assunto
  em profundidade que a aula não vai cobrir. Mitigação: a página de referências da Aula 08 lista os
  cinco autoestudos com título exato e aponta o que cada um cobre, e a Ponderada 2 de Computação,
  que é autoestudo da mesma semana, permanece como o exercício do tema.
- **O contraste de escolha de K depende dos CSVs trimestrais e o de PCA dos mensais.** Se o SIDRA
  revisar uma série, uma conclusão pode virar. Mitigação: `tools/tests/test_pca_aula08.py` trava as
  oito conclusões da aula, e as quatro mutações declaradas no cabeçalho dele foram executadas e
  reprovam.

## Consequências

Positivas:

- A Aula 08 fecha com uma tese medida em duas famílias de técnica não supervisionada, e o exemplo
  que a `ADR-009` reservou para ela é usado como abertura do bloco de escolha de K, sem
  reconstrução.
- A ART.6 recebe um resultado utilizável: a dupla sabe que reduzir dimensionalidade por PCA nesta
  base custa 1,6 ponto percentual de MAPE, e leva a justificativa medida para a entrega.
- A Aula 09 herda dois ganchos prontos, o efeito medido do ajuste fora do treino e a diferença
  entre variância e informação, para os blocos de vazamento temporal e maldição de
  dimensionalidade.

Negativas:

- Sistemas de recomendação permanece coberto de forma assimétrica: cinco autoestudos e 10 minutos
  de sala. Se o professor quiser o assunto com prática, ele volta a competir por tempo com PCA.
- A citação dos boletins do Sindirações sai do roteiro da Aula 08, e é a segunda aula em que essa
  fonte é removida por não existir no acervo. Enquanto não houver série aberta de preço de
  macroingrediente, o Modelo 3 continua sem dado próprio, e as Aulas 12 e 13 vão encontrar a mesma
  parede.
- A prática de plotar os trimestres no espaço dos dois primeiros componentes, prevista no roteiro,
  passa a plotar meses no plano PC2 por PC3, porque é ali que o calendário aparece nesta base. O
  professor que consultar só o roteiro antigo vai encontrar outra figura na tela.

## ADRs relacionadas

- `ADR-004`, que ancorou o case em fonte aberta e é o motivo de a prática do Sindirações não
  existir.
- `ADR-007`, que removeu a mesma citação do Sindirações do roteiro da Aula 04.
- `ADR-008`, que fixou o corte temporal e a baseline de coeficiente fixo usada aqui como
  referência de 3,71%.
- `ADR-009`, que moveu Elbow Plot e Silhouette Analysis para esta aula e mediu o contraste de
  silhueta usado no bloco de escolha de K.
- `ADR-010`, que estabeleceu a base mensal e as 11 features sobre as quais o PCA desta aula roda.

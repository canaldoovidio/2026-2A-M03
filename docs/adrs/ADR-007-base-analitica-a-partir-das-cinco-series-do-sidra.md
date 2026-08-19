# ADR-007: A base analítica da Aula 04 vem do merge das cinco séries do SIDRA entre si

**Data:** 18/08/2026
**Status:** Aceita
**Decisores:** Prof. Ovidio Lopes da Cruz Netto

## Contexto

O roteiro original da Aula 04 em `PLANEJAMENTO_AULA_A_AULA.md` previa, no bloco de integração de
dados, unir `abate_frangos.csv` (IBGE/SIDRA) com "os boletins do Sindirações" por meio de
`pd.merge`, usando `periodo` como chave. Esse bloco é o que ensina junção de tabelas, chave de
junção e tipo de junção, e é ele que produz a base analítica que a Aula 05 usa para treinar o
primeiro modelo.

Ao construir a aula, a conferência do acervo mostrou que **não existe nenhum arquivo do Sindirações
em `dados/`**. As cinco séries versionadas são todas do SIDRA (abate de bovinos, suínos e frangos,
produção de ovos e de leite), conforme `dados/README.md`. O Sindirações publica os números de
produção de ração em boletins, sem série aberta em formato tabular com granularidade trimestral
equivalente à das tabelas do SIDRA.

Isso deixava três caminhos: fabricar uma série de ração para a aula, buscar e versionar uma nova
fonte aberta de insumo na véspera do encontro, ou fazer a junção entre as séries que já existem.

A ADR-004 já fecha a primeira porta: dado sintético é proibido onde existir dado aberto real. A
segunda porta adiciona risco de rede e de granularidade incompatível a menos de 24 horas do
encontro, e não é o objeto de aprendizagem do dia.

## Decisão

O bloco de integração da Aula 04 une **as cinco séries do SIDRA entre si**, pela chave `periodo`,
produzindo uma base larga trimestral com uma coluna por série.

## Motivações

- **O objeto de aprendizagem é preservado inteiro.** Chave de junção, tipo de junção e o que
  acontece com as linhas que não casam continuam sendo exatamente o conteúdo do bloco. As cinco
  séries têm coberturas diferentes (`producao_ovos` começa em 1987-T1; as outras quatro, em
  1997-T1), então `inner` devolve 117 linhas e `outer` devolve 157 com 40 ausentes em quatro
  colunas. O contraste entre os dois tipos de junção sai do dado real do acervo.
- **A decisão entre `fillna` e `dropna` deixa de ser hipotética.** A Aula 03 fechou com
  `isna()` devolvendo zero nas cinco séries e registrou que a escolha entre preencher e descartar
  era assunto da Aula 04. O `outer join` produz os primeiros valores ausentes reais do acervo, e é
  sobre eles que a escolha é discutida.
- **A base resultante é a que a Aula 05 precisa**, com uma coluna por série mais as features de
  defasagem e de sazonalidade, sem nenhuma dependência externa nova.
- **ETL e ELT continuam como enquadramento teórico do bloco**, citando os autoestudos da Semana 03,
  sem depender de qual é a segunda fonte concreta.

## Riscos conhecidos

- **O TAPI da LDC desdobra produção de proteína em demanda de ração e depois em macroingredientes.**
  Sem uma série de ração, o segundo e o terceiro modelos do case continuam sem fonte de dados
  aberta. Mitigação: isso já era verdade antes desta ADR, e a Aula 02 tratou explicitamente o
  descompasso entre o que o TAPI pede e o que a fonte aberta permite. A Aula 04 registra a
  limitação no material de apoio em vez de escondê-la.
- **Correlação alta entre séries que compartilham tendência pode ser lida como sinal.** As cinco
  séries crescem no tempo, e a correlação de Pearson entre elas em nível fica entre +0,92 e +0,97.
  Mitigação: isso virou conteúdo do bloco de seleção de característica, comparando a correlação em
  nível com a correlação nas primeiras diferenças, que cai para a faixa de -0,04 a +0,20.

## Consequências

**Positivas**

- A Aula 04 fica autocontida no acervo versionado, sem dependência de rede em tempo de aula.
- O acervo ganha um exemplo real de `outer join` com ausentes, que sustenta a discussão de
  `fillna` e `dropna` prometida pela Aula 03.
- A comparação entre correlação em nível e em diferença dá conteúdo mensurado ao autoestudo
  "Seleção de característica".

**Negativas**

- `PLANEJAMENTO_AULA_A_AULA.md`, `PLANO_DE_ENSINO.md` e o resumo do card da Aula 04 no portal
  precisaram ser corrigidos, porque os três citavam o Sindirações como segunda fonte.
- A menção ao Sindirações na Aula 02 (mapeamento dos três modelos do TAPI) continua válida como
  fonte prevista do case, mas agora sem contrapartida versionada em `dados/`.

## ADRs relacionadas

- **ADR-003**: regressão tabular em vez de séries temporais. É ela que torna as features de
  defasagem e de sazonalidade obrigatórias, e portanto o que a base unificada precisa carregar.
- **ADR-004**: case ancorado em fontes abertas. É ela que proíbe fabricar a série do Sindirações.

# Andamento do acervo

Estado atual do repositório, para quem estiver retomando o trabalho. Fonte: o plano
`docs/superpowers/plans/2026-08-01-fundacao-e-aula01.md` (16 tasks, fundação do acervo mais a
Aula 01 como padrão-ouro para as 13 aulas restantes).

## Pronto

- **Tokens da marca e validador de fidelidade** (`assets/css/inteli-brand.css`,
  `tools/check_brand.py`): paleta oficial, tipografia (Platypi no lugar da Azurio), segmento
  Graduação.
- **Logo e grafismo isométrico** em três versões (`assets/img/inteli-logo-*.svg`,
  `assets/img/inteli-grafismo-graduacao.svg`).
- **Tema do deck** (`assets/css/inteli-theme.css`, `assets/css/inteli-print.css`) e o deck de
  referência de cada classe (`aulas/_fixture-tema.html`).
- **Validador de layout** (`tools/check_slides.py`), via Playwright: estouro de 1280x720,
  sobreposição de bloco, título colidindo com o logo.
- **JavaScript do deck**: quiz interativo, zoom por teclado, exportação em PDF
  (`assets/js/inteli-quiz.js`, `assets/js/inteli-zoom.js`, `assets/js/inteli-print.js`).
- **Extração dos autoestudos da Adalove** (`tools/extrair_autoestudos.py` →
  `docs/autoestudos-por-semana.md`).
- **Dados do case**: os cinco CSVs trimestrais do IBGE/SIDRA versionados em `dados/`
  (`tools/baixar_dados.py`, `dados/README.md`).
- **Documentos de planejamento**: `PLANO_DE_ENSINO.md` e `PLANEJAMENTO_AULA_A_AULA.md`, com os
  14 títulos conferidos caractere a caractere contra a Adalove.
- **Portal e validador de links**: `index.html` com os cards das 14 aulas agrupados por sprint, e
  `tools/check_links.py`.
- **Skills globais** (`inteli-course-design`, `inteli-deck-design`): ver seção "Skills globais"
  abaixo.
- **Agentes, hook e documentação do repositório**: `.claude/agents/construtor-aulas.md`,
  `.claude/agents/revisor-slides.md`, `.claude/settings.json`, `CLAUDE.md`, `README.md`, este
  arquivo.
- **Estilo das páginas de leitura** (`assets/css/inteli-material.css`): usado por `materiais/` e
  `referencias/`. Só tokens, nenhuma cor ou `font-family` literal. A TOC lateral sai do layout
  abaixo de 900px e o grid volta para uma coluna sem deixar buraco.
- **Aula 01 completa, os quatro artefatos** (`aulas/aula01.html`, `materiais/aula01.html`,
  `referencias/aula01.html`, `notebooks/aula01.ipynb`) mais as notas do professor
  (`docs/notas-do-professor/aula01.md`). Os quatro botões do card da Aula 01 no portal estão
  habilitados.
- **Aula 02 completa, os quatro artefatos** (`aulas/aula02.html`, `materiais/aula02.html`,
  `referencias/aula02.html`, `notebooks/aula02.ipynb`) mais as notas do professor
  (`docs/notas-do-professor/aula02.md`). O notebook dela é a fase 2 do CRISP-DM executada: mede os
  seis pilares de qualidade sobre as cinco séries, ainda sem pandas. Os quatro botões do card no
  portal estão habilitados.
- **Aula 04 completa, os quatro artefatos** (`aulas/aula04.html`, `materiais/aula04.html`,
  `referencias/aula04.html`, `notebooks/aula04.ipynb`) mais as notas do professor
  (`docs/notas-do-professor/aula04.md`) e as duas figuras
  (`tools/graficos_aula04.py`). O notebook constrói a base analítica que a Aula 05 recebe: junção
  das cinco séries, defasagens, sazonalidade codificada e padronização. Os quatro botões do card no
  portal estão habilitados. O deck tem 30 slides, incluindo dois blocos pedidos pelo professor
  depois da primeira versão: dez minutos de revisão das Semanas 01 a 03, para a Ponderada 1 de
  Computação, e onze minutos de hipóteses declaradas para a ART.5.
- **Aula 05 completa, os quatro artefatos** (`aulas/aula05.html`, `materiais/aula05.html`,
  `referencias/aula05.html`, `notebooks/aula05.ipynb`) mais as notas do professor
  (`docs/notas-do-professor/aula05.md`), as duas figuras (`tools/graficos_aula05.py`), a
  `docs/adrs/ADR-008` e a suíte `tools/tests/test_modelo_aula05.py`. O deck tem 31 slides. É o
  primeiro modelo preditivo do case: regressão de `abate_frangos` sobre a base analítica de 113
  linhas que a Aula 04 deixou pronta, com corte temporal de 8 trimestres (2024-T2 a 2026-T1),
  RMSE e MAPE contra três baselines, e o ciclo de overfitting e reprodutibilidade. Os quatro
  botões do card no portal estão habilitados.
- **Três achados da Aula 05, todos medidos antes de o primeiro slide ser escrito.** (1) O modelo
  ganha da baseline de coeficiente fixo por apenas **0,10 ponto percentual** de MAPE na última
  janela (1,60% contra 1,69%), e vence nas **doze janelas** consecutivas medidas, com média de
  2,18% contra 3,14%. É a aula que ensina que uma janela de oito trimestres não decide. (2) **Sem
  padronizar, o solver zera os coeficientes de sazonalidade**: as defasagens estão na casa de 1e9
  e `sen`/`cos` na de 1, o número de condição da matriz chega a 1,08e10, e a decomposição em
  valores singulares descarta as direções pequenas. Isso **contradiz parcialmente a Aula 04**,
  que afirmou que padronizar não muda as previsões de uma regressão sem regularização: a
  afirmação vale em álgebra exata e falha nesta base em ponto flutuante. O deck, o material e as
  notas do professor tratam a divergência abertamente. (3) O leite, que a H2 da Aula 04 mandou
  ficar de fora, **piora o MAPE de teste de 1,60% para 1,89%** e confirma a hipótese fora da
  amostra.
- **A segunda forma de vazamento do material da Aula 05 foi medida, e é inofensiva neste
  modelo.** Ajustar o `StandardScaler` sobre treino e teste juntos desloca a média do escalador
  em 12% de um desvio e devolve MAPE idêntico até a nona casa, porque regressão linear sem
  regularização é invariante a transformação afim das entradas. O achado veio de um teste de
  mutação: essa mutação passava nos oito testes originais. Em vez de escrever uma asserção que
  nunca falha (seção 8.2 da `inteli-course-design`), o teste passou a travar a invariância, e o
  material declara que a disciplina de `fit` só no treino vale por causa de KNN, SVM, regressão
  regularizada e PCA, que aparecem entre as Aulas 06 e 08.
- **A estatística da Aula 04 fecha o ciclo completo** (hipótese declarada, teste escolhido,
  decisão, consequência no projeto), com quatro testes sobre os CSVs reais: Shapiro-Wilk,
  Pearson, Kruskal-Wallis e teste t pareado. O achado que sustenta o bloco: a sazonalidade do
  leite **não** é detectada pelo teste sobre a série em nível (p = 0,0739) e aparece com p da
  ordem de 1e-06 depois de remover a tendência, porque a variação entre anos infla a variação
  dentro dos grupos. `tools/tests/test_hipoteses_aula04.py` trava as decisões, não só os números,
  e se pula sozinho onde não houver scipy.
- **ADRs** (`docs/adrs/ADR-001` a `ADR-007`): as sete decisões de arquitetura do acervo, para o
  fan-out não relitigar nenhuma. Motor Reveal.js, Platypi no lugar da Azurio, regressão tabular em
  base trimestral, case só com fonte aberta, os quatro artefatos por aula, as skills globais e a
  base analítica montada a partir das cinco séries do SIDRA.
- **Integração contínua** (`.github/workflows/validate.yml` e `.github/workflows/static.yml`):
  validação em push e pull_request (marca, links, layout, pytest e execução dos notebooks, mais um
  passo que reprova se a validação alterar arquivo versionado) e publicação da raiz do repositório
  no GitHub Pages a cada push em `main`.

**Com isso, as 16 tasks do plano estão implementadas.** O que falta do plano é só o portão de
saída, abaixo.

## Em andamento / não iniciado

- **Aula 01: revisão do professor no navegador.** É o portão de saída do plano e ainda não
  aconteceu. Os validadores passam, mas o que o professor aprovar na capa, na densidade dos
  slides e no tom do material é o que vira contrato para as 13 aulas seguintes. Ver "Achados
  abertos" abaixo: são justamente as decisões que dependem dele.
- **O site está no ar e atualizado.** `https://canaldoovidio.github.io/2026-2A-M03/` publica
  as Aulas 01, 02 e 03 com os quatro artefatos cada. A política de branch do ambiente
  `github-pages` foi corrigida pelo professor em 07/08/2026, e o `static.yml` passou a
  publicar normalmente a cada push em `main` (run 31142595526, 22s).

- **Aulas 06 a 14**: os cards dessas aulas no portal seguem com os quatro botões em
  `aria-disabled="true"`. As Aulas 01 a 05 já existem. A **Aula 06, em 01/09**, é a próxima da
  fila, abre a Sprint 3 e trata de aprendizado não supervisionado. O agente `construtor-aulas`
  existe para esse fan-out, mas as cinco primeiras aulas foram escritas sem ele, à mão, seguindo
  as mesmas skills.
- **O que a Aula 05 deixa marcado para as aulas seguintes.** As quatro séries defasadas em um
  trimestre derrubam o MAPE de teste para 1,14%, contra 1,60% do modelo de hoje, e ficaram de
  fora de propósito: entram como candidata declarada na Aula 07. O reajuste do modelo sobre a
  base completa, depois de a avaliação terminar, fica para a Aula 12 junto com o `Pipeline`. A
  repetição em janelas feita à mão hoje vira `TimeSeriesSplit` na Aula 10.

## Corrigido em 18/08/2026, junto com a Aula 04

- **A validação de CI estava vermelha desde a Aula 03.** O passo de execução dos notebooks
  instalava apenas `pandas`, e o notebook da Aula 03 passou a importar `matplotlib` e `seaborn` sem
  que a lista de dependências fosse atualizada junto (`ModuleNotFoundError: No module named
  'matplotlib'`). A lista saiu da linha de comando do workflow e virou `requirements-ci.txt`, com o
  motivo de cada pacote ao lado, como o próprio comentário do workflow já previa. A Aula 04
  acrescenta `scipy` e `scikit-learn`.
- **O roteiro da Aula 04 citava o Sindirações como segunda fonte da junção**, em
  `PLANEJAMENTO_AULA_A_AULA.md`, `PLANO_DE_ENSINO.md` e no resumo do card do portal, mas não existe
  série aberta do Sindirações em `dados/`. Os três documentos foram corrigidos, e o motivo está em
  `docs/adrs/ADR-007`.

## Corrigido em 24/08/2026, junto com a Aula 05

- **A validação de CI estava vermelha desde 19/08**, e a causa não era conteúdo: o slide 25 da
  Aula 04 tinha 58px de folga vertical no macOS e estourava 13px no Ubuntu do CI, porque as
  métricas de fonte diferem entre os dois sistemas e o mesmo parágrafo ocupa mais linhas no Linux.
  Os dois parágrafos do `side-by-side` foram encurtados de três para duas linhas cada, sem alterar
  nenhum número nem a conclusão do slide, e a folga subiu para 93px. Encolher a figura foi
  descartado: ela já está no piso de legibilidade (18px na tela a 900px de largura), e reduzi-la
  para 820px levaria os rótulos a 16px. A armadilha ficou registrada em `CLAUDE.md`.
- **O deck da Aula 05 passou limpo no Ubuntu na primeira tentativa** (31 slides, sem estouro,
  sobreposição ou título no logo). A menor folga vertical dele é de 84px e a menor folga entre
  título e logo é de 32px, contra 17px da Aula 04, que já passava.

## Achados abertos da revisão da Aula 04

Dois achados da revisão da Aula 04 que valem para o acervo inteiro, não só para ela:

1. **As figuras da Aula 02 têm fonte abaixo do piso de legibilidade em projeção.** Medido: com
   `dpi=160` e exibição entre 860px e 900px, um rótulo de N pontos chega à tela com cerca de N
   pixels, então os `fontsize` de 8,5 a 12 de `tools/graficos_aula02.py` chegam a projetar entre
   9px e 12px, contra o piso de 18px que o tema fixa para texto de slide. `tools/graficos_aula04.py`
   já parte de 18 pontos e traz a conta escrita no cabeçalho. Aplicar o mesmo ajuste às figuras da
   Aula 02 é trabalho pendente, e a Aula 03 usa figuras geradas em notebook, que precisam da mesma
   conferência.
2. **O cabeçalho das notas do professor usa uma construção que as diretivas de tom proíbem**
   ("Material de condução do encontro, não de distribuição ao aluno. Não é resumo do deck: são as
   perguntas..."). O texto é idêntico nas Aulas 01 a 04. A decisão de reescrever o cabeçalho nas
   quatro de uma vez é do professor. **A Aula 05 já nasceu na forma nova**, em conformidade com as
   diretivas, e registra a divergência no fim do próprio arquivo: alinhar as quatro anteriores é
   uma edição de dois minutos quando houver decisão.

## Achados abertos da revisão da Aula 01

Três achados da conferência da Aula 01 que são **decisão do professor**, não correção mecânica,
porque os três moram no tema compartilhado e valeriam para as 14 aulas:

1. **Espaço vazio na metade inferior dos slides de conteúdo.** O tema alinha o conteúdo ao topo
   da seção, então um slide com título e três cartões deixa cerca de 300px em branco embaixo. O
   comportamento é herdado: `aulas/_fixture-tema.html` faz igual. Fica assim, como respiro, ou o
   bloco de conteúdo passa a distribuir a altura?
2. **`.cover-eyebrow` não recebe o tamanho que o tema pede.** O tema declara
   `--escala-complementar` (14px) para a linha de olho da capa, mas `.reveal p` tem
   especificidade maior e o texto renderiza a 18px, medido com `getComputedStyle`. O CSS diz uma
   coisa e faz outra. Corrigir com o seletor composto `.cover-slide .cover-eyebrow` deixa a linha
   visivelmente menor na capa, então é mudança de aparência, não só de código.
3. **Centralização vertical se perde no PDF.** Nos slides `section-slide` e `end-slide` o
   conteúdo aparece centralizado na tela e colado no topo no PDF exportado. A causa é a regra
   `.reveal .slides section.present { display: flex !important; }` estar restrita a `.present`,
   classe que não existe no modo de impressão. Confirmado gerando o PDF de verdade com
   `Page.printToPDF`, não por captura de `?print-pdf`. O fundo dos slides está preservado (o bug
   antigo não voltou); é só o alinhamento.

## Skills globais

`inteli-course-design` e `inteli-deck-design` vivem em `~/.claude/skills/`, fora deste
repositório, de propósito: nasceram da fundação do acervo do 03 IN, mas descrevem metodologia
Inteli e identidade visual Inteli em geral, reutilizáveis em qualquer módulo futuro, não só neste.
Consequência prática: elas **não aparecem em `git log` nem em `git diff` deste repositório**, e
quem clonar o repositório em outra máquina precisa ter essas skills instaladas globalmente para os
agentes `construtor-aulas` e `revisor-slides` funcionarem como descrito. O `CLAUDE.md` aponta para
os caminhos exatos.

## Fora do git de propósito

- **`Turma.xlsx`**: a planilha oficial da Adalove, com dado pessoal de aluno (nome, presença,
  nota). Fonte de `PLANO_DE_ENSINO.md`, `docs/autoestudos-por-semana.md` e dos pesos de ART, mas
  nunca versionada. Regenerar os derivados publicáveis com `python3 tools/extrair_autoestudos.py`.
- **`TURMA-*-TAPI-*.pdf`** (o TAPI da Louis Dreyfus Company): tem seção de conteúdo restrito do
  parceiro. Fonte do escopo do case, nunca versionada.

Os dois estão listados em `.gitignore`, com o motivo documentado ali: o repositório é publicado
inteiro no GitHub Pages, então qualquer arquivo commitado fica público.

## Pendências abertas

- **Leitura complementar do professor, nas aulas 01 e 02.** A seção 2 de
  `referencias/aula01.html` e de `referencias/aula02.html` existe com a estrutura fixa que o
  fan-out replica, mas a curadoria do professor ainda não foi feita. Hoje elas listam as fontes
  efetivamente citadas no deck e no material (na Aula 01, a tabela 1092 do SIDRA e três páginas da
  documentação de Python; na Aula 02, as cinco tabelas do SIDRA, o guia do CRISP-DM, os seis
  pilares da DAMA UK e Stevens 1946). Substituir ou completar quando o professor indicar.
- **Um autoestudo oficial tem travessão em dash no título.** "Opcional: Riscos e benefícios da IA
  — AI4People (Floridi et al., 2018)", da Semana 01, citado em `referencias/aula02.html`. O
  caractere é proibido no texto que o acervo escreve, mas aqui é citação literal do título da
  Adalove: alterá-lo quebraria a conferência título por título contra
  `docs/autoestudos-por-semana.md`. Está preservado de propósito, com o motivo escrito na própria
  página, para ninguém "corrigir" depois.
- **`nbconvert` não está instalado no Python do sistema.** O Homebrew marca o ambiente como
  gerenciado externamente (PEP 668), então a execução do notebook da Aula 01 foi validada num
  venv descartável. O `validate.yml` instala `nbconvert` e `ipykernel` no runner, mas quem rodar a
  bateria localmente precisa de um venv próprio. **Feito em 18/08/2026:** a lista de dependências
  virou `requirements-ci.txt`, e o workflow instala a partir dele.
- **O notebook é versionado sem saída de execução, de propósito.** O plano previa
  `nbconvert --execute --inplace`, mas gravar a saída no arquivo entrega o gabarito: a célula do
  desafio imprime as respostas das duas primeiras perguntas, e a célula do `KeyError` mostra o
  traceback que o aluno deveria ler por conta própria. A validação, local e no CI, executa uma
  cópia fora da árvore de trabalho, e o `validate.yml` tem um passo final que reprova se algum
  arquivo versionado for alterado pela validação.
- **`--shots` do `check_slides.py` só salva PNG de slide com problema.** O plano supunha que ele
  fotografava todos os slides, e não é o caso: a conferência visual da Aula 01 foi feita com um
  script próprio de captura. Se a conferência a olho vai ser passo obrigatório de toda aula, vale
  dar ao validador uma opção que fotografe o deck inteiro.
- `python3 tools/check_slides.py` sem argumento agora encontra `aulas/aula01.html` e passa. O
  fixture do tema (`aulas/_fixture-tema.html`) continua fora da descoberta automática de
  propósito, porque começa com `_`; para medi-lo, passar o caminho explicitamente.

## Achados abertos da revisão da Aula 02 (07/08/2026)

Dois achados que a revisão independente levantou e que são **decisão do professor**, não conserto
mecânico. Nenhum bloqueou a publicação.

1. **A legenda do ciclo CRISP-DM fala em "duas voltas documentadas", e a fonte primária tem três.**
   A Figura 2 do guia CRISP-DM 1.0 confirma as duas setas duplas que o deck desenha (Negócio com
   Dados, Preparação com Modelagem), mas traz também uma terceira conexão interna, de sentido
   único, ligando Avaliação direto a Entendimento do Negócio, por dentro do círculo. O ponto
   pedagógico do slide continua verdadeiro, mas a contagem é leitura incompleta da própria fonte
   citada. Corrigir na próxima revisão do diagrama.
2. **32 slides podem não caber nos sete blocos de 15 minutos.** O bloco de qualidade e taxonomia
   passou de "seis pilares e taxonomia, com exercício" para seis unidades de conteúdo distintas,
   cada uma com fonte primária própria, antes de qualquer interação. É factível se o professor
   escolher quais diagramas narra em detalhe e quais só aponta. Decisão de condução, não de
   arquivo.

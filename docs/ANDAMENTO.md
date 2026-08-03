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
- **ADRs** (`docs/adrs/ADR-001` a `ADR-006`): as seis decisões de arquitetura do acervo, para o
  fan-out não relitigar nenhuma. Motor Reveal.js, Platypi no lugar da Azurio, regressão tabular em
  base trimestral, case só com fonte aberta, os quatro artefatos por aula e as skills globais.
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
- **O site está no ar, mas parado no estado da Aula 01.** `https://canaldoovidio.github.io/2026-2A-M03/`
  responde 200 e a Aula 01 está publicada; `aulas/aula02.html` responde 404.

  **Causa exata:** o ambiente `github-pages` tem política de branch customizada
  (`custom_branch_policies: true`) e a única branch autorizada a publicar é
  **`fundacao-e-aula01`**. O `static.yml` dispara em `main`, então o deploy é recusado pela regra de
  ambiente e o job falha em 3 segundos, sem nenhum passo executado. O único deploy bem-sucedido foi
  um `workflow_dispatch` manual em `fundacao-e-aula01`, feito antes do commit da Aula 02.

  **Correção (exige admin no repositório, como `canaldoovidio`):** em
  *Settings > Environments > github-pages > Deployment branches and tags*, adicionar `main` (ou
  trocar para "All branches"). Em *Settings > Pages*, deixar a origem em "GitHub Actions". E em
  *Settings > General*, trocar a branch padrão de `fundacao-e-aula01` para `main`.

  **Alternativa sem tocar em configuração:** trocar o gatilho de `static.yml` de `main` para
  `fundacao-e-aula01`. Funciona, mas deixa `main` sem publicar, o que é o inverso da convenção.

  Nota de ambiente: o `gh` desta máquina está autenticado como `josercf`, que não tem admin neste
  repositório (o `git push` funciona porque vai por SSH com a chave de `canaldoovidio`, ver o
  mapeamento de hosts em `~/.ssh/config`). Qualquer chamada de administração do repositório pelo
  `gh` responde 403 ou 404 até trocar a autenticação.
- **Aulas 03 a 14**: os cards dessas aulas no portal seguem com os quatro botões em
  `aria-disabled="true"`. A Aula 03 é em **11/08** e é a primeira da fila. O agente
  `construtor-aulas` existe para esse fan-out, mas as aulas 01 e 02 foram escritas sem ele, à mão,
  seguindo as mesmas skills.

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
  bateria localmente precisa de um venv próprio. Quando as dependências de notebook crescerem, na
  Aula 03 (pandas, numpy, matplotlib, seaborn), trocar a linha de `pip install` do workflow por um
  `requirements-ci.txt` em vez de continuar acumulando pacote no YAML.
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

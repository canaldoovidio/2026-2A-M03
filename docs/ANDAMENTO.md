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
- **Agentes, hook e documentação do repositório** (esta task): `.claude/agents/construtor-aulas.md`,
  `.claude/agents/revisor-slides.md`, `.claude/settings.json`, `CLAUDE.md`, `README.md`, este
  arquivo.

## Em andamento / não iniciado

Ordem do plano original:

- **ADRs** (`docs/adrs/`): seis decisões de arquitetura ainda não documentadas (motor Reveal.js
  em vez do motor próprio do IN02T26, Platypi no lugar da Azurio, regressão tabular em vez de
  série temporal, granularidade trimestral, os quatro artefatos por aula, skills globais).
- **Integração contínua** (`.github/workflows/validate.yml` e `.github/workflows/static.yml`):
  ainda não existem. Hoje não há publicação automática no GitHub Pages nem validação automática
  em push/PR; os três validadores e a suíte pytest só rodam localmente ou via hook.
- **Aula 01, o deck** (`aulas/aula01.html`): ainda não existe. `aulas/` só tem o fixture do tema.
- **Aula 01, material e referências** (`materiais/aula01.html`, `referencias/aula01.html`): ainda
  não existem. As pastas `materiais/` e `referencias/` **não existem no repositório**.
- **Aula 01, notebook e notas do professor** (`notebooks/aula01.ipynb`,
  `docs/perguntas-aula01.md`): ainda não existem. A pasta `notebooks/` **não existe no
  repositório**.
- **Aulas 02 a 14**: dependem do agente `construtor-aulas` (pronto a partir desta task) rodando
  em fan-out depois que a Aula 01 estabelecer o padrão-ouro.
- O card de cada aula em `index.html` continua com os quatro botões (`Slides`, `Material`,
  `Referências`, `Notebook`) em `aria-disabled="true"`, porque nenhum artefato de aula foi
  publicado ainda.

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

- Publicação no GitHub Pages ainda não está configurada (depende da task de Integração Contínua).
  O link do portal em `README.md` aponta para a URL esperada
  (`https://canaldoovidio.github.io/2026-2A-M03/`), que só fica no ar depois desse workflow
  existir.
- `python3 tools/check_slides.py` (sem argumento, sobre `aulas/`) reprova hoje com "nenhum deck
  encontrado", porque `aulas/` só tem o fixture do tema (que começa com `_` e é ignorado de
  propósito na descoberta automática) e a Aula 01 ainda não existe. Isso é o portão funcionando
  como projetado, não um bug: rodar o validador contra um arquivo específico
  (`python3 tools/check_slides.py aulas/_fixture-tema.html`) continua funcionando normalmente.

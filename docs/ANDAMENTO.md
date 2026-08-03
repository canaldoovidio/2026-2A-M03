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

## Em andamento / não iniciado

- **Aula 01: revisão do professor no navegador.** É o portão de saída do plano e ainda não
  aconteceu. Os validadores passam, mas o que o professor aprovar na capa, na densidade dos
  slides e no tom do material é o que vira contrato para as 13 aulas seguintes. Ver "Achados
  abertos" abaixo: são justamente as decisões que dependem dele.
- **ADRs** (`docs/adrs/`): seis decisões de arquitetura ainda não documentadas (motor Reveal.js
  em vez do motor próprio do IN02T26, Platypi no lugar da Azurio, regressão tabular em vez de
  série temporal, granularidade trimestral, os quatro artefatos por aula, skills globais).
- **Integração contínua** (`.github/workflows/validate.yml` e `.github/workflows/static.yml`):
  ainda não existem. Hoje não há publicação automática no GitHub Pages nem validação automática
  em push/PR; os validadores e a suíte pytest só rodam localmente ou via hook.
- **Aulas 02 a 14**: dependem do agente `construtor-aulas` rodando em fan-out depois que a
  revisão da Aula 01 fechar o padrão-ouro. Os cards dessas aulas no portal seguem com os quatro
  botões em `aria-disabled="true"`.

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

- **Leitura complementar do professor na Aula 01.** A seção 2 de `referencias/aula01.html` existe
  com a estrutura fixa que o fan-out replica, mas a curadoria do professor ainda não foi feita.
  Hoje ela lista as quatro fontes efetivamente citadas no deck (a tabela 1092 do SIDRA e três
  páginas da documentação de Python). Substituir ou completar quando o professor indicar.
- **Publicação no GitHub Pages** ainda não está configurada (depende da task de Integração
  Contínua). O link do portal em `README.md` aponta para a URL esperada
  (`https://canaldoovidio.github.io/2026-2A-M03/`), que só fica no ar depois desse workflow
  existir.
- **`nbconvert` não está instalado no Python do sistema.** O Homebrew marca o ambiente como
  gerenciado externamente (PEP 668), então a execução do notebook da Aula 01 foi validada num
  venv descartável. O workflow de CI precisa instalar `nbconvert` e `ipykernel`, e quem rodar a
  bateria localmente precisa de um venv.
- **O notebook é versionado sem saída de execução, de propósito.** O plano previa
  `nbconvert --execute --inplace`, mas gravar a saída no arquivo entrega o gabarito: a célula do
  desafio imprime as respostas das duas primeiras perguntas, e a célula do `KeyError` mostra o
  traceback que o aluno deveria ler por conta própria. A validação executa uma cópia, com
  `--output` apontando para fora do repositório. O workflow de CI precisa fazer o mesmo em vez de
  `--inplace`, senão o CI passa a sujar a árvore de trabalho.
- **`--shots` do `check_slides.py` só salva PNG de slide com problema.** O plano supunha que ele
  fotografava todos os slides, e não é o caso: a conferência visual da Aula 01 foi feita com um
  script próprio de captura. Se a conferência a olho vai ser passo obrigatório de toda aula, vale
  dar ao validador uma opção que fotografe o deck inteiro.
- `python3 tools/check_slides.py` sem argumento agora encontra `aulas/aula01.html` e passa. O
  fixture do tema (`aulas/_fixture-tema.html`) continua fora da descoberta automática de
  propósito, porque começa com `_`; para medi-lo, passar o caminho explicitamente.

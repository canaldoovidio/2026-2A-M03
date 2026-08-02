# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this
repository.

> **Retomando o trabalho?** `docs/ANDAMENTO.md` tem o estado atual: o que está pronto, o que está
> em andamento e as pendências abertas.

## O que é este repositório

Acervo didático do **Módulo 03 IN, Lógica para predição com inteligência artificial** (Graduação
Inteli, turma GRAD IN03 · 2026-2A · T25, Prof. Ovidio Lopes da Cruz Netto). Não é uma aplicação: é
um site estático de decks Reveal.js, materiais de apoio, páginas de referências e notebooks,
publicado no GitHub Pages. O que se edita é HTML, CSS, JS puro, Markdown e notebooks Jupyter.

Não existe build, bundler nem package manager de JavaScript na raiz. A única dependência de
execução é Python (Playwright para os validadores, openpyxl/pandas para os scripts de dados).

## Comandos

```bash
# Preview local (obrigatório servir por HTTP: os decks usam caminhos relativos assets/)
python3 -m http.server 8000        # a partir da raiz do repositório
# depois: http://localhost:8000/                    -> portal (index.html)
#         http://localhost:8000/aulas/aula01.html    -> deck da Aula 01 (quando existir)

# Exportar um deck em PDF: abrir a URL do deck com ?print-pdf e usar o botao de impressao
# injetado por assets/js/inteli-print.js (ou Ctrl/Cmd+P do navegador)
#         http://localhost:8000/aulas/aula01.html?print-pdf

# Validar fidelidade ao brandbook (paleta, tipografia, segmento, iconografia)
python3 tools/check_brand.py

# Validar layout dos decks (estouro de 1280x720, sobreposicao, titulo colidindo com o logo)
python3 tools/check_slides.py                    # todos os decks em aulas/
python3 tools/check_slides.py aulas/aula01.html   # um deck
python3 tools/check_slides.py --shots /tmp/shots  # com screenshot dos problemas

# Validar que todo link/src local do acervo resolve para um arquivo existente
python3 tools/check_links.py

# Suite de testes (validadores + extratores de dados)
python3 -m pytest tools/tests/ -v

# Regerar os cinco CSVs de dados/ a partir da API do SIDRA/IBGE (requer rede)
python3 tools/baixar_dados.py

# Regerar docs/autoestudos-por-semana.md a partir do Turma.xlsx (arquivo local, fora do git)
python3 tools/extrair_autoestudos.py > docs/autoestudos-por-semana.md
```

Deploy: publicação no GitHub Pages ainda não está automatizada neste repositório (workflow
previsto, ver `docs/ANDAMENTO.md`). Quando existir, publicará **o repositório inteiro** a cada
push em `main`: qualquer arquivo commitado fica público, por isso `Turma.xlsx` e o TAPI da Louis
Dreyfus Company estão no `.gitignore` de propósito (ver seção "Armadilhas conhecidas").

## Arquitetura de conteúdo: três camadas

Alterar o conteúdo de uma aula geralmente exige tocar em mais de uma camada, nesta ordem de
dependência:

1. **Planejamento** (raiz do repositório)
   - `PLANO_DE_ENSINO.md`: o case, as fontes de dados, a decisão de granularidade trimestral, o
     cronograma das 14 aulas com data e sprint, e os pesos de ART citados da Adalove.
   - `PLANEJAMENTO_AULA_A_AULA.md`: roteiro minuto a minuto de cada um dos 14 Encontros de
     Instrução.
   - Os dois são a **fonte da verdade** para data, título, escopo, autoestudo e peso de entrega.
     Nenhum artefato inventa o que deveria vir de um destes dois arquivos.

2. **Metodologia** (skills globais, fora deste repositório)
   - `~/.claude/skills/inteli-course-design/SKILL.md`: estrutura do encontro de 2h, a regra dos
     15 minutos, a aprendizagem em espiral, o case do parceiro como espinha dorsal, a amarração
     aula/sprint/ART/autoestudo e a anatomia dos quatro artefatos por aula.
   - `~/.claude/skills/inteli-deck-design/SKILL.md`: identidade visual Inteli, tipografia,
     grafismo isométrico, anatomia do deck Reveal.js e as armadilhas de layout já corrigidas neste
     acervo. Ler antes de tocar em qualquer slide ou no tema.
   - Ficam em `~/.claude/skills/`, não neste repositório, porque são reutilizáveis em qualquer
     módulo Inteli, não só no 03 IN (ver `docs/ANDAMENTO.md` para o porquê dessa escolha).

3. **Materiais** (este repositório)
   - `index.html`: portal com cards por aula, agrupados por sprint, ligando cada aula aos quatro
     artefatos.
   - `aulas/aulaNN.html`: um deck Reveal.js autocontido por aula.
   - `dados/`: os cinco CSVs trimestrais do IBGE/SIDRA que sustentam o case (ver seção "O case"
     abaixo e `dados/README.md`).
   - `assets/{css,js,img}/`: tema, scripts e imagens compartilhados por todos os decks.
   - `materiais/`, `referencias/` e `notebooks/`: ainda não existem neste repositório na
     fundação do acervo; são criados pelo agente `construtor-aulas` na primeira aula construída
     (ver `docs/ANDAMENTO.md`).

## O case: Louis Dreyfus Company

O módulo inteiro é ancorado num projeto com parceiro real. O TAPI da Louis Dreyfus Company (LDC)
pede um modelo preditivo de produção de proteína animal no Brasil, desdobrado em demanda de
ração e depois em macroingredientes, em três modelos encadeados. As cinco séries abertas do
IBGE/SIDRA que alimentam o case vivem em `dados/` (abate de bovinos, suínos e frangos, produção
de ovos e de leite), sempre em base **trimestral**: o TAPI pede previsão mensal, mas a fonte de
dados aberta só existe em trimestre, e esse descompasso é conteúdo de aula (Aula 02, CRISP-DM),
não um detalhe escondido. Detalhes completos, com a URL de cada tabela SIDRA e a checagem de
sanidade dos valores, estão em `dados/README.md`.

## Anatomia de um deck

Cada `aulas/aulaNN.html` é um arquivo único, sem build, que carrega Reveal.js 5.1.0 do jsDelivr,
`assets/css/inteli-brand.css`, `assets/css/inteli-theme.css` e `assets/css/inteli-print.css`.
Reveal é inicializado com `width: 1280, height: 720, center: false, margin: 0`: o tema fixa cada
`section` nesse tamanho, então **o conteúdo não rola** (o que não couber quebra o slide
visualmente). O deck de referência de cada classe do tema é `aulas/_fixture-tema.html`: qualquer
dúvida de markup se resolve abrindo esse arquivo, não reinventando.

A anatomia completa (ordem canônica dos 10 blocos de slide, classes disponíveis, markup de quiz
que funciona) está documentada em `~/.claude/skills/inteli-deck-design/SKILL.md` seção 7. Este
arquivo não repete isso.

## Armadilhas conhecidas

- **Slide que estoura os 720px não é detectável por `scrollHeight`.** A `section` tem altura
  fixa, então esse valor sempre retorna 720 mesmo com conteúdo vazando. Use
  `tools/check_slides.py`, que compara o retângulo de cada descendente com a área útil do slide.
- **A capa usa `conic-gradient`, nunca SVG recortado.** Trocar de técnica reintroduz um bug de
  empilhamento em Chrome headless, que é justamente o navegador dos validadores. Detalhes em
  `inteli-deck-design` seção 4.
- **Classe de estado (quiz respondido, fragment revelado) precisa vencer a especificidade da
  regra base do componente**, senão o DOM muda mas a tela não. Ver `inteli-deck-design` seção 8.1.
- **`tools/check_slides.py` é cego a estado pós-interação**: mede o deck com `page.goto` e nunca
  clica em nada. Responder o quiz e revelar os fragments é verificação manual, sempre.
- **Screenshot de `?print-pdf` não valida impressão.** Só aciona o layout empilhado do Reveal via
  JavaScript, nunca o `@media print` de verdade. Gerar o PDF de fato antes de validar.
- **`Turma.xlsx` e o TAPI da LDC nunca são commitados.** Têm dado pessoal de aluno e conteúdo
  restrito do parceiro, e o repositório é publicado inteiro no GitHub Pages. Ambos estão no
  `.gitignore`; o que entra no repositório são os derivados publicáveis
  (`PLANO_DE_ENSINO.md`, `PLANEJAMENTO_AULA_A_AULA.md`, `docs/autoestudos-por-semana.md`).
- **`v/all` na API do SIDRA mistura peso, número de informantes e percentuais na mesma tabela.**
  `tools/baixar_dados.py` sempre pede a variável específica de cada série. Ver `dados/README.md`.

A lista completa de armadilhas de layout e de verificação, com a causa raiz de cada uma, está em
`~/.claude/skills/inteli-deck-design/SKILL.md` seção 8 e em
`~/.claude/skills/inteli-course-design/SKILL.md` seção 8.

## Automação

- **`tools/check_brand.py`**: varre o acervo inteiro procurando cor literal fora do arquivo de
  tokens, cor fora da paleta oficial, cor de outro segmento institucional, `font-family` fora do
  arquivo de tokens e emoji.
- **`tools/check_slides.py`**: validador de layout via Playwright, abre cada deck em 1280x720 e
  reporta estouro, sobreposição de bloco ou título colidindo com o logo.
- **`tools/check_links.py`**: verifica que todo `href`/`src` local do acervo resolve para um
  arquivo que existe. Não checa link externo, para a rede não derrubar a validação.
- **`tools/tests/`**: suíte pytest dos validadores e dos extratores de dados
  (`python3 -m pytest tools/tests/ -v`).
- **Hook `PostToolUse`** (`.claude/settings.json`): dispara `check_slides.py` e `check_brand.py`
  automaticamente ao editar qualquer arquivo em `aulas/*.html`, em background, e só interrompe o
  fluxo quando um dos dois reprova.
- **Agente `construtor-aulas`** (`.claude/agents/`): constrói uma aula inteira (deck, material,
  referências, notebook e notas do professor), seguindo as duas skills globais e os documentos de
  planejamento. Ponto de partida para qualquer aula nova.
- **Agente `revisor-slides`** (`.claude/agents/`): revisa um deck contra layout, fidelidade ao
  brandbook, profundidade pedagógica, links e numeração de rodapé. Roda antes de todo commit de
  deck, sem precisar ser pedido: é a etapa que cobre o que os validadores automatizados não
  pegam (especificidade CSS de estado, estado pós-interação, impressão de verdade, fonte pequena
  demais para projeção).
- **`tools/baixar_dados.py`**: baixa e converte as cinco séries trimestrais do SIDRA/IBGE.
- **`tools/extrair_autoestudos.py`**: extrai do `Turma.xlsx` os autoestudos e Encontros de
  Instrução por semana, gerando `docs/autoestudos-por-semana.md`.

## Convenções editoriais

Regras válidas para deck, material de apoio, referências, notebook, portal e qualquer documento de
planejamento deste acervo. Detalhadas em `~/.claude/skills/inteli-course-design/SKILL.md` seção 7;
resumo aqui:

- Português do Brasil com **acentuação completa**.
- **Travessão em dash (o caractere U+2014) é proibido.** Usar dois-pontos, vírgula, parênteses ou
  hífen no lugar.
- **Emoji é proibido.** A iconografia da marca é o Google Material Symbols.
- **Peso de ART é sempre citado da fonte oficial** (`PLANO_DE_ENSINO.md`, que vem da Adalove),
  nunca calculado nem inventado.
- **Autoestudo é sempre citado de `docs/autoestudos-por-semana.md`, com título exato**, nunca
  inventado nem reescrito.
- Referências são numeradas na página de referências de cada aula.
- Dado sintético é proibido onde existir dado aberto real: todo exemplo numérico ancora nos CSVs
  reais de `dados/`.
- Commits em Conventional Commits, autor `canaldoovidio` (ver `docs/ANDAMENTO.md` para o comando
  exato de commit usado neste acervo).

# Design: acervo didático do Módulo 03 IN (2026-2A)

**Data:** 01/08/2026
**Status:** Aprovado
**Autor:** Prof. Ovidio Lopes da Cruz Netto
**Turma:** GRAD IN03 · 2026-2A · T25
**Repositório:** `git@github.com:canaldoovidio/2026-2A-M03.git`

---

## 1. Contexto

O Módulo 03 do curso de Inteligência Artificial (*Lógica para predição com inteligência
artificial*) tem 10 semanas, 5 sprints e **14 Encontros de Instrução** ministrados pelo Prof.
Ovidio. O módulo é ancorado em um projeto com parceiro real, a **Louis Dreyfus Company (LDC)**.

Existem dois acervos anteriores que servem de base:

- **`2026.1/IN02T26`**: Módulo 2 do Ciclo Comum. Traz a identidade Inteli, decks ricos em
  animação (terminal digitando, pipelines animados), material de apoio com TOC lateral e planos
  de ensino. Motor de slides próprio, sem processo de engenharia ao redor.
- **`FIAP/FIAP-2026-2-3SI`**: disciplina de Microservice and Web Engineering. Traz a camada de
  engenharia: skill de metodologia, agentes especializados, validador de layout com hook,
  ADRs, documentos de planejamento como fonte da verdade e portal em cards.

Este documento define como unir os dois: **o conteúdo e a identidade do Inteli, com o processo
de engenharia da FIAP**, agora com a identidade visual corrigida a partir do brandbook oficial.

## 2. Objetivos

1. Produzir o acervo completo das 14 aulas, com 4 artefatos por aula.
2. Estabelecer uma identidade visual **fiel ao Brandbook Inteli 2025**, substituindo a
   aproximação usada em 2026.1.
3. Criar duas skills globais reutilizáveis em qualquer módulo Inteli futuro.
4. Amarrar cada aula ao sprint, à entrega (ART) e aos autoestudos da Adalove correspondentes.
5. Garantir que o material seja verificável por automação, não por inspeção manual.

## 3. Não-objetivos

- Não construir o projeto dos alunos nem os notebooks de entrega das ARTs.
- Não hospedar bases de dados enviadas pela LDC. O repositório usa apenas fontes abertas.
- Não produzir material das disciplinas dos demais professores do módulo.
- Não migrar o acervo de 2026.1 para o novo padrão.

## 4. Fontes da verdade

| Fonte | Papel |
|---|---|
| `Turma.xlsx` | cronograma oficial: datas, títulos, semanas, tipos de atividade, autoestudos, ARTs e pesos |
| `TURMA-25-TAPI-MOD03 IN-Modelo-Preditivo-Louis-Dreifu.pdf` | escopo, dados, restrições e perguntas do parceiro |
| `INTELI - INSTITUCIONAL/MANUAL DA MARCA/Brandbook_Inteli_25_final (2).pdf` | identidade visual |
| `PLANO_DE_ENSINO.md` e `PLANEJAMENTO_AULA_A_AULA.md` | derivados dos anteriores; fonte da verdade para todo o material |

Regra: nenhum deck, portal ou notebook inventa data, título ou escopo. Tudo desce dos dois
documentos de planejamento, que por sua vez descem do `Turma.xlsx` e do TAPI.

## 5. Cronograma: 14 aulas em 5 sprints

| # | Data | Sprint | Aula | Camada da espiral sobre o case |
|---|---|---|---|---|
| 01 | 04/08 | 1 | Introdução ao Python | ler o CSV do SIDRA de abate bovino; tipos, listas, dicionários |
| 02 | 07/08 | 1 | Visão Geral de ML, IA e Ciência de Dados | enquadrar os 3 modelos do TAPI; CRISP-DM sobre o problema da LDC |
| 03 | 11/08 | 1 | Pandas, Numpy e bibliotecas gráficas | EDA das 5 séries de proteína animal |
| 04 | 19/08 | 2 | Pré-processamento e Feature Engineering | unir SIDRA e Sindirações; defasagens e sazonalidade |
| 05 | 24/08 | 2 | Aprendizado Supervisionado I | regressão da produção de frango; corte temporal treino/teste |
| 06 | 01/09 | 3 | Aprendizado Não Supervisionado I | clusterização de perfis de dieta e de meses |
| 07 | 04/09 | 3 | Aprendizado Supervisionado II | árvores e ensembles no Modelo 1; RMSE e MAPE |
| 08 | 10/09 | 3 | Aprendizado Não Supervisionado II | PCA nos drivers macroeconômicos |
| 09 | 15/09 | 4 | Problemas Comuns de Modelagem e mais Feature Engineering | vazamento temporal, dimensionalidade, nulos do IBGE |
| 10 | 17/09 | 4 | Hiperparâmetros e Explicabilidade | GridSearch, validação cruzada, SHAP, partial dependence |
| 11 | 24/09 | 4 | AutoML com PyCaret | comparar candidatos para os 3 modelos |
| 12 | 29/09 | 5 | Deploy de modelo e pipeline de processamento | `Pipeline` do scikit-learn, export do modelo, MLflow |
| 13 | 30/09 | 5 | Deploy de modelos de Machine Learning | app Streamlit com histórico vs. forecast e cenários |
| 14 | 06/10 | 5 | Revisão e Futuro | fechamento do módulo e horizontes |

### Marcos de projeto por sprint

| Sprint | Planning | Review | Entregas com peso |
|---|---|---|---|
| 1 | 03/08 | 14/08 | ART.1 Entendimento do negócio (6) · ART.2 UX parte 1 (3) |
| 2 | 17/08 | 28/08 | ART.3 Exploração, Pré-processamento e Hipóteses (5) · ART.4 UX parte 2 (3) · ART.5 Distribuição normal e teste de hipótese (4) |
| 3 | 31/08 | 11/09 | ART.6 Preparação dos Dados e Modelagem (6) |
| 4 | 14/09 | 25/09 | ART.7 Comparação de modelos (8) |
| 5 | 28/09 | 07/10 | Prova 02/10 (20) · ART.8 Modelo Final (4) · ART.9 Critérios de Publicação (3) · ART.10 Apresentação final (3) |

## 6. Case integrador: Louis Dreyfus Company

**Problema.** Prever a produção mensal de proteína animal no Brasil por categoria (aves, suínos,
bovinos, ovos, leite), converter essa produção em demanda de ração e desdobrar essa demanda nos
macroingredientes (milho, farelo de soja, sorgo, trigo, DDGS), com horizonte de 24 meses.

**Três modelos encadeados**, conforme o TAPI:

1. projeção de produção de proteína animal por categoria;
2. conversão de produção em demanda total de ração;
3. desdobramento da ração entre macroingredientes.

**Dados**: apenas fontes abertas, versionadas em `dados/`:

- IBGE/SIDRA: tabelas 1092 (bovinos), 1093 (suínos), 1094 (frangos), 7524 (ovos), 1086 (leite)
- Sindirações: boletins informativos do setor, 2021 a 2025

**Métricas.** RMSE e MAPE, comparados contra a abordagem de coeficientes estáticos que a LDC usa hoje.

**Explicabilidade.** SHAP e partial dependence plots são requisito do parceiro, não enfeite.

### A restrição que organiza o módulo

O TAPI proíbe explicitamente o uso de **modelos de séries temporais**. Logo, as aulas 04 a 07
precisam ensinar previsão de horizonte longo por **regressão tabular com features de defasagem,
janelas móveis e codificação de sazonalidade**, e a aula 09 precisa tratar vazamento temporal
com validação por corte de data em vez de embaralhamento aleatório. Essa é a decisão pedagógica
central do módulo e vale uma ADR própria.

## 7. Identidade visual

Todas as regras abaixo vêm do Brandbook Inteli 2025, com a página citada.

### 7.1 Paleta (p.66)

| Token | Nome | Hex |
|---|---|---|
| `--inteli-roxo` | Roxo | `#2e2640` |
| `--inteli-coral` | Coral | `#ff4545` |
| `--inteli-lilas` | Lilás | `#90a5e5` |
| `--inteli-verde` | Verde | `#89cea5` |
| `--inteli-verde-escuro` | Verde Escuro | `#066d73` |
| `--inteli-cinza-escuro` | Cinza Escuro | `#b2b6bf` |
| `--inteli-cinza-medio` | Cinza Médio | `#caced6` |
| `--inteli-cinza-claro` | Cinza Claro | `#e6eaeb` |
| `--inteli-branco` | Branco | `#ffffff` |

### 7.2 Segmento Graduação (p.68)

A paleta se subdivide por segmento. Este módulo é **Graduação**, cuja proporção é: branco e
cinzas como base, **verde e roxo como os dois blocos de peso**, coral apenas como filete de
destaque. Consequências para o tema:

- `--seg-base: #ffffff` e `--seg-superficie: #e6eaeb`
- `--seg-primaria: #2e2640` (roxo)
- `--seg-secundaria: #89cea5` (verde)
- `--seg-destaque: #ff4545` (coral), em área reduzida
- **Lilás e verde escuro não entram**: pertencem a Escolas e a Exec/Pós.

O CSS de 2026.1 tratava o verde como `--inteli-blue`, o que apagava seu papel de cor de peso do
segmento. Corrigido aqui.

### 7.3 Tipografia (p.69–74)

| Papel | Fonte oficial | O que usamos | Motivo |
|---|---|---|---|
| Títulos | Azurio Medium | **Platypi** | ver 7.3.1 |
| Texto | Manrope Regular a SemiBold | Manrope | Google Font, uso direto |
| Complementar | Space Mono | Space Mono | só detalhes; proibido em blocos de texto |

Hierarquia de referência do brandbook: título 55pt, texto 20pt, complementar 15pt, medidos em
página de 1920x1080. A razão entre os níveis é o que deve ser preservada. Reduzir tudo
proporcionalmente para um deck de 1280x720 levaria o corpo de texto a ~13px, ilegível em
projeção. **Adaptação adotada:** manter a hierarquia relativa e fixar um piso de 18px para
texto corrido no deck, documentado na skill de design.

Don'ts explícitos do brandbook, que o validador deve conseguir apontar: Azurio ou Platypi como
texto corrido, Space Mono como título, Space Mono como texto corrido, falta de contraste entre
título e texto.

#### 7.3.1 Platypi no lugar da Azurio

A Azurio é fonte licenciada e o repositório é público no GitHub Pages: empacotar os `.otf`
republicaria a fonte. O próprio brandbook (p.70) prevê a substituição pela **Platypi** "na
impossibilidade de uso em sistemas", por ser Google Font. A substituição é, portanto, o caminho
previsto pela marca, e não um contorno. Vira ADR.

Nota de contexto: o CSS de 2026.1 declarava `font-family: "Azurio", "Manrope", sans-serif` sem
nunca carregar a Azurio, então os títulos caíam em Manrope de forma silenciosa.

### 7.4 Grafismo (p.75–84)

Três faces isométricas em **120°**, representando liderança, tecnologia e negócios. Regras:

- sempre três módulos, ângulo de 120° nunca alterado;
- **nunca preencher as três faces** com conteúdo;
- proibido criar formas dentro das faces;
- texto sobre o grafismo apenas como detalhe curto;
- combinação do segmento Graduação: verde, roxo e cinza claro.

Implementação: SVG puro, sem imagem rasterizada, usado nas capas e nos slides de seção.

### 7.5 Marca (p.43–53)

- Positiva em fundos claros; negativa em fundos escuros; monocromática sobre cor ou imagem.
- Resguardo mínimo: a largura entre o "i" e o "n" da marca.
- Redução máxima digital: 20px.
- Proibido: outline, degradê, sombra, rotação, distorção, recomposição em outra tipografia e o
  uso da tipografia sem o símbolo.

Os vetores oficiais estão em PDF no acervo institucional e serão convertidos para SVG com
`pdftocairo -svg`. Isso encerra a dependência do PNG hospedado no Cloudinary usado em 2026.1.

### 7.6 Iconografia (p.88)

**Google Material Symbols**, traço linear leve e uniforme. Emojis ficam proibidos em decks,
portal, cards e favicon. O portal de 2026.1 usava emojis, o que está fora do brandbook.

## 8. Arquitetura do repositório

```
2026-2A-M03/
├── index.html                     portal: cards por aula agrupados por sprint
├── README.md
├── CLAUDE.md                      guia do repositório para agentes
├── PLANO_DE_ENSINO.md             fonte da verdade: ementa, cronograma, ARTs, espiral
├── PLANEJAMENTO_AULA_A_AULA.md    fonte da verdade: roteiro minuto a minuto das 14 aulas
├── aulas/aula01..14.html          decks Reveal.js
├── materiais/aula01..14.html      material de apoio
├── referencias/aula01..14.html    autoestudos da Adalove + curadoria do professor
├── notebooks/aula01..14.ipynb     laboratório executável no Colab
├── dados/                         CSVs do case (SIDRA e Sindirações)
├── assets/
│   ├── css/inteli-brand.css       tokens do brandbook, nada além disso
│   ├── css/inteli-theme.css       tema do deck, consome só os tokens
│   ├── css/inteli-print.css
│   ├── js/{inteli-quiz,inteli-zoom,inteli-print}.js
│   └── img/                       logo SVG (4 versões) e grafismos
├── tools/
│   ├── check_slides.py            validador de layout
│   ├── check_links.py             validador de links
│   └── tests/                     pytest dos validadores
├── docs/
│   ├── ANDAMENTO.md
│   ├── autoestudos-por-semana.md  extraído do Turma.xlsx
│   ├── notas-do-professor/        perguntas socráticas por aula, uso do professor
│   ├── adrs/
│   └── superpowers/{specs,plans}/
├── .claude/agents/{construtor-aulas.md,revisor-slides.md}
└── .github/workflows/{static.yml,validate.yml}
```

`assets/css/inteli-brand.css` contém apenas os tokens da seção 7. Nenhum outro arquivo declara
cor ou família tipográfica literal: tudo consome os tokens. Isso torna auditável a fidelidade à
marca.

## 9. Anatomia do deck

Reveal.js 5.1.0, `width: 1280, height: 720, center: false, margin: 0`. A `section` tem altura
fixa: **conteúdo que não cabe não rola, quebra o slide**.

Ordem canônica:

1. capa, com grafismo isométrico do segmento Graduação
2. agenda com horários do encontro
3. resgate da espiral: o que a aula anterior deixou pronto
4. o problema do case naquela aula
5. blocos teóricos, nenhum passando de 15 minutos sem interação
6. quiz de verificação
7. hands-on: o notebook da aula
8. o entregável da sprint que essa aula alimenta
9. referências numeradas
10. encerramento com copyright

Classes: `cover-slide`, `section-slide`, `content-slide`, `quiz-slide`, `exercise-slide`.
Blocos reutilizáveis: `concept-cards`, `side-by-side`, `slide-title-area`, `top-bar`,
`slide-footer`, `code-compact`.

## 10. Os 4 artefatos por aula

| Artefato | Caminho | Papel |
|---|---|---|
| Deck | `aulas/aulaXX.html` | o encontro de 1h45 |
| Material de apoio | `materiais/aulaXX.html` | conteúdo escrito, TOC lateral, navegação flutuante |
| Referências | `referencias/aulaXX.html` | autoestudos da Adalove da semana + curadoria do professor |
| Notebook | `notebooks/aulaXX.ipynb` | lab executável no Colab, sobre os dados do case |

A página de referências tem duas seções fixas: **Autoestudos da semana (Adalove)** e **Leitura
complementar do professor**, curada por aula.

Os autoestudos nunca são inventados. Eles são extraídos do `Turma.xlsx` para
`docs/autoestudos-por-semana.md` na Fase 1, e as páginas de referência consomem esse arquivo.
São 106 atividades do Prof. Ovidio distribuídas nas 10 semanas, entre autoestudos e encontros.

Além dos 4 artefatos públicos, cada aula gera um arquivo em `docs/notas-do-professor/`, com as
perguntas socráticas do encontro. É material de condução da aula, não de distribuição.

## 11. Portal

Cinco grupos, um por sprint, com a janela de datas no cabeçalho. Cada card traz badge da aula,
**data do encontro**, título, resumo e os quatro botões. Dentro de cada grupo, cards de contexto
sem botões marcam Sprint Planning, Sprint Review, Prova e entregas ART com prazo, situando a
aula no ritmo do projeto.

## 12. Skills globais

### `~/.claude/skills/inteli-course-design/SKILL.md`

Metodologia, reutilizável em qualquer módulo Inteli:

- estrutura do encontro: 08h–10h autoestudo, 10h00–10h15 daily, 10h15–12h00 metodologia ativa;
  nenhum bloco expositivo passa de 15 minutos sem interação;
- aprendizagem em espiral: toda aula resgata explicitamente a anterior;
- case do projeto-parceiro como espinha dorsal;
- amarração obrigatória aula ↔ sprint ↔ ART ↔ autoestudo;
- anatomia dos 4 artefatos;
- notas do professor com perguntas socráticas;
- convenções editoriais: pt-BR com acentuação completa, sem travessão em dash, sem emoji,
  referências numeradas, pesos de avaliação sempre citados da Adalove e nunca inventados.

### `~/.claude/skills/inteli-deck-design/SKILL.md`

Identidade visual e construção de apresentação, com cada regra citando a página do brandbook:

- paleta, segmentação por Graduação, tipografia e a substituição Azurio → Platypi;
- grafismo isométrico: construção, aplicação e don'ts;
- marca: versões, resguardo, redução máxima, usos incorretos;
- iconografia Material Symbols;
- anatomia do deck e componentes;
- piso de legibilidade para projeção;
- armadilhas de layout herdadas da FIAP: estouro invisível dos 720px, `position:absolute`,
  fragments não medidos, bloco de código junto de `concept-cards`;
- fluxo obrigatório: `check_slides.py` e agente `revisor-slides` antes de qualquer commit de deck;
- gráficos seguem a skill `dataviz`.

## 13. Agentes

- **`construtor-aulas`**: constrói uma aula inteira, os 4 artefatos, seguindo as duas skills.
  Ponto de partida para qualquer aula nova.
- **`revisor-slides`**: revisa um deck contra layout, fidelidade ao brandbook, profundidade
  pedagógica, links e numeração de rodapé. Roda antes de todo commit de deck, sem precisar ser pedido.

## 14. Automação e testes

| Item | O que faz |
|---|---|
| `tools/check_slides.py` | abre cada deck em 1280x720 via Playwright e reporta elemento fora da área útil ou sobreposto |
| `tools/check_links.py` | verifica que todo `href` do portal e dos materiais resolve |
| `tools/tests/` | suíte pytest dos dois validadores, com fixtures de layout quebrado |
| Hook `PostToolUse` | dispara o validador ao editar qualquer arquivo em `aulas/` |
| `.github/workflows/validate.yml` | roda os validadores e executa os notebooks com `nbconvert --execute` sobre os CSVs de `dados/` |
| `.github/workflows/static.yml` | publica o repositório no GitHub Pages a cada push em `main` |

Os notebooks precisam rodar do zero contra os dados versionados. Notebook que não executa em CI
é notebook quebrado na aula.

## 15. ADRs previstas

| ADR | Título |
|---|---|
| 001 | Reveal.js com tema Inteli no lugar do motor de slides próprio |
| 002 | Platypi como tipografia de título em substituição à Azurio |
| 003 | Regressão tabular com defasagens no lugar de séries temporais |
| 004 | Case ancorado em fontes abertas, sem bases enviadas pela LDC |
| 005 | Quatro artefatos por aula e o que cada um resolve |
| 006 | Skills de metodologia e de design como skills globais |

## 16. Faseamento

| Fase | Escopo | Janela |
|---|---|---|
| 1. Fundação | skills, tokens do brandbook, tema, logo SVG, grafismo, validadores com testes, agentes, portal, os dois documentos de planejamento, dados do case, ADRs 001–006 | 01–02/08 |
| 2. Padrão-ouro | Aula 01 completa, revisada pelo professor | 02–03/08 |
| 3. Fan-out | agente A: aulas 02–03 · B: 04–05 · C: 06–08 · D: 09–11 · E: 12–14 | a partir de 03/08 |
| 4. Fechamento | `revisor-slides` em todo o acervo, links, PDFs, publicação | contínuo |

A Aula 01 é em **04/08**, três dias após a escrita deste documento. As Fases 1 e 2 são o caminho
crítico. A Aula 02 é em 07/08, então o agente A entra logo após a validação do padrão-ouro; os
demais rodam em paralelo com folga.

## 17. Riscos

| Risco | Mitigação |
|---|---|
| Prazo da Aula 01 | Fases 1 e 2 concentradas; escopo da Aula 01 restrito ao essencial de Python sobre um CSV do SIDRA |
| Inconsistência visual entre decks gerados por agentes distintos | tokens únicos em `inteli-brand.css`, padrão-ouro aprovado antes do fan-out, `revisor-slides` obrigatório |
| Fontes de dados externas fora do ar durante a aula | CSVs baixados e versionados em `dados/`; notebooks nunca dependem de rede |
| Deriva entre portal, decks e cronograma | os dois documentos de planejamento como fonte da verdade e `check_links.py` no CI |
| Conteúdo do parceiro marcado como restrito | repositório usa apenas fontes abertas; bases da LDC ficam fora deste repositório |

## 18. Critérios de aceite

1. As 14 aulas têm os 4 artefatos, e todos os links do portal resolvem.
2. `check_slides.py` e `check_links.py` passam em todo o acervo.
3. Todos os notebooks executam em CI contra os dados versionados.
4. Nenhum arquivo declara cor ou família tipográfica fora de `inteli-brand.css`.
5. Nenhum emoji em deck, portal ou favicon.
6. Cada aula declara explicitamente o sprint, a ART que alimenta e os autoestudos da semana.
7. As duas skills globais existem e são citadas pelos agentes.
8. As seis ADRs estão escritas.

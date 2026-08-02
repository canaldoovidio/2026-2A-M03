# Módulo 03 IN &middot; Lógica para predição com inteligência artificial

Acervo didático do módulo, com os decks, materiais de apoio, páginas de referências e notebooks
das 14 aulas. Este documento é para o aluno; quem for editar o repositório deve começar pelo
`CLAUDE.md`.

## O módulo

| Campo | Valor |
|---|---|
| Módulo | 03 IN, Lógica para predição com inteligência artificial |
| Turma | GRAD IN03 &middot; 2026-2A &middot; T25 |
| Professor | Prof. Ovidio Lopes da Cruz Netto |
| Período | 03/08/2026 a 07/10/2026 |
| Duração | 10 semanas &middot; 5 sprints &middot; 14 Encontros de Instrução |

## O parceiro do case

O módulo inteiro é ancorado num projeto com a **Louis Dreyfus Company (LDC)**. O TAPI da LDC pede
um modelo preditivo de produção de proteína animal no Brasil, desdobrado em demanda de ração e
depois em macroingredientes (milho, farelo de soja, sorgo, trigo, DDGS), em três modelos
encadeados. As cinco séries abertas do IBGE/SIDRA que sustentam o case (abate de bovinos, suínos e
frangos, produção de ovos e de leite) estão versionadas em `dados/`, sempre em base **trimestral**:
detalhes em `dados/README.md`.

## Calendário das 14 aulas

Fonte oficial: `PLANEJAMENTO_AULA_A_AULA.md` e `PLANO_DE_ENSINO.md`. Qualquer divergência de data
ou título entre este calendário e a Adalove é erro deste README, não da Adalove.

| # | Data | Sprint | Aula |
|---|---|---|---|
| 01 | 04/08/2026 | 1 | Introdução ao Python |
| 02 | 07/08/2026 | 1 | Visão Geral do Aprendizado de Máquina, Inteligência Artificial e Ciência de Dados |
| 03 | 11/08/2026 | 1 | Introdução ao Pandas, Numpy e bibliotecas gráficas - Exploração de Dados |
| 04 | 19/08/2026 | 2 | Pré Processamento e Feature Engineering |
| 05 | 24/08/2026 | 2 | Aprendizado Supervisionado parte I |
| 06 | 01/09/2026 | 3 | Aprendizado Não Supervisionado - parte I |
| 07 | 04/09/2026 | 3 | Aprendizado Supervisionado - parte II |
| 08 | 10/09/2026 | 3 | Aprendizado Não Supervisionado Parte II |
| 09 | 15/09/2026 | 4 | Problemas Comuns com Modelagem de IA e mais Feature Engineering |
| 10 | 17/09/2026 | 4 | Hiperparâmetros e Explicabilidade do Modelo |
| 11 | 24/09/2026 | 4 | AutoML - Pycaret |
| 12 | 29/09/2026 | 5 | Deploy de modelo e criação de pipeline de processamento |
| 13 | 30/09/2026 | 5 | Deploy de modelos de Machine Learning |
| 14 | 06/10/2026 | 5 | Revisão e Futuro |

## Estrutura de pastas

```
.
├── index.html                     portal com os cards de cada aula, agrupados por sprint
├── PLANO_DE_ENSINO.md             ementa, cronograma, pesos de ART (fonte da verdade)
├── PLANEJAMENTO_AULA_A_AULA.md    roteiro minuto a minuto de cada encontro (fonte da verdade)
├── aulas/                         um deck Reveal.js por aula (aulaNN.html)
├── materiais/                     material de apoio de cada aula, com aprofundamento e TOC
├── referencias/                   autoestudos da semana + leitura complementar, por aula
├── notebooks/                     laboratório executável de cada aula, ancorado em dados/
├── dados/                         os cinco CSVs trimestrais do IBGE/SIDRA que sustentam o case
├── assets/                        CSS, JS e imagens do tema, compartilhados por todos os decks
└── docs/
    ├── autoestudos-por-semana.md  autoestudos e Encontros de Instrução, extraídos da Adalove
    └── ANDAMENTO.md               estado atual do acervo: o que está pronto e o que falta
```

`materiais/`, `referencias/` e `notebooks/` são criados conforme cada aula é construída; nem toda
aula tem os quatro artefatos publicados ainda (ver `docs/ANDAMENTO.md` para o estado atual).

## Portal

O portal deste acervo é publicado no GitHub Pages: <https://canaldoovidio.github.io/2026-2A-M03/>.
A publicação automática ainda não está configurada neste repositório (ver `docs/ANDAMENTO.md`);
até lá, abra `index.html` localmente, servido por HTTP (`python3 -m http.server` na raiz do
repositório), porque os decks usam caminhos relativos para `assets/`.

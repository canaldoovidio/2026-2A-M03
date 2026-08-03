# ADR-005: Quatro artefatos por aula, e o que cada um resolve

**Data:** 03/08/2026
**Status:** Aceita
**Decisores:** Prof. Ovidio Lopes da Cruz Netto

## Contexto

O acervo do Módulo 02 do Ciclo Comum (`2026.1/IN02T26`) produzia, por aula, um deck, um material
de apoio e um plano de ensino da aula. Na prática, o plano de ensino por aula acabou virando um
documento que ninguém lia depois de escrito: o roteiro que o professor usa vive num só documento
consolidado, não picado em 14 arquivos.

Ao mesmo tempo, faltava responder duas perguntas que apareciam em toda aula:

1. **"Onde estão os autoestudos desta semana?"** O aluno tinha a Adalove aberta num lado e o deck
   no outro, sem nada ligando os dois.
2. **"Onde eu rodo isso?"** O deck mostrava código que ninguém executava, e a prática dependia de
   o aluno digitar o que estava projetado.

## Decisão

Cada aula produz **quatro artefatos públicos**, mais um interno:

| Artefato | Caminho | O que resolve |
|---|---|---|
| Deck | `aulas/aulaNN.html` | o encontro de 1h45 em si |
| Material de apoio | `materiais/aulaNN.html` | o que o slide só pôde apontar, em texto corrido |
| Referências | `referencias/aulaNN.html` | a ponte com a Adalove e a curadoria do professor |
| Notebook | `notebooks/aulaNN.ipynb` | o laboratório executável sobre os dados do case |
| *(interno)* Notas do professor | `docs/notas-do-professor/aulaNN.md` | as perguntas socráticas do encontro |

O plano de ensino por aula do IN02T26 **sai**. O roteiro minuto a minuto das 14 aulas vive num
documento único, `PLANEJAMENTO_AULA_A_AULA.md`, que é fonte da verdade dos quatro artefatos.

## Motivações

- **Cada artefato tem um papel que os outros não cobrem.** O material de apoio não é o deck em
  prosa: onde o slide mostra um `KeyError` provocado de propósito, o material explica o que a
  mensagem diz e por que aquele erro é pedagógico. Se um artefato pudesse ser gerado dos outros, ele
  não deveria existir.
- **A página de referências fecha a amarração obrigatória com o autoestudo**, com título exato
  copiado de `docs/autoestudos-por-semana.md`. Autoestudo que não está lá não entra na página, o
  que impede inventar leitura.
- **O notebook garante que o código da aula roda.** Ele é executado em CI contra os CSVs
  versionados: notebook que não executa em CI é notebook quebrado na aula.
- **As notas do professor separam condução de distribuição.** Perguntas socráticas com resposta
  esperada e erro comum são material de quem conduz, e publicá-las junto entregaria o gabarito.
- **Quatro caminhos previsíveis viabilizam o fan-out.** O portal, o validador de links e o agente
  `construtor-aulas` dependem de `aulaNN` ser o mesmo número nas quatro pastas.

## Riscos conhecidos

| Risco | Mitigação |
|---|---|
| Quatro artefatos por aula, 14 aulas: 56 arquivos para manter em sincronia | Os quatro descem do mesmo documento de planejamento, e `tools/check_links.py` reprova link para artefato que não existe. |
| O material de apoio degenerar em cópia do deck | Está escrito na skill `inteli-course-design` (seção 6) e é item de revisão do agente `revisor-slides`. |
| A seção de leitura complementar ficar vazia nas 14 aulas | A seção nunca é omitida do HTML, mesmo sem curadoria: quando vazia, vira pendência registrada em `docs/ANDAMENTO.md`. |
| As notas do professor vazarem para o aluno | Ficam em `docs/`, fora do portal, e nenhum card aponta para elas. Ressalva: o repositório é público, então "interno" aqui significa "não divulgado", não "protegido". |

## Consequências

**Positivas.** O aluno tem um lugar para cada necessidade: assistir, ler, estudar antes e executar.
O professor tem o roteiro num só documento em vez de 14. A estrutura é replicável por agente, o que
é o que torna o fan-out das aulas 02 a 14 viável.

**Negativas.** É mais trabalho por aula que no acervo anterior, e o custo do fan-out cresce por
quatro. A Aula 01 levou o tempo de um padrão-ouro justamente para que as 13 seguintes possam copiar
a estrutura em vez de redecidi-la.

## ADRs relacionadas

- [ADR-001](ADR-001-reveal-js-com-tema-inteli.md): o motor do deck.
- [ADR-004](ADR-004-case-ancorado-em-fontes-abertas.md): o notebook lê sempre de `dados/`, nunca da
  rede.
- [ADR-006](ADR-006-skills-globais-de-metodologia-e-design.md): a anatomia dos quatro artefatos
  mora numa skill global.

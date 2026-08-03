# ADR-006: Skills de metodologia e de design como skills globais, não locais

**Data:** 03/08/2026
**Status:** Aceita
**Decisores:** Prof. Ovidio Lopes da Cruz Netto

## Contexto

A construção do acervo produziu dois corpos de conhecimento que os agentes `construtor-aulas` e
`revisor-slides` consomem:

- **Metodologia Inteli**: estrutura do Encontro de Instrução, regra dos 15 minutos, aprendizagem em
  espiral, amarração aula/sprint/ART/autoestudo, anatomia dos artefatos, convenções editoriais.
- **Identidade visual Inteli**: paleta, segmentação por Graduação, tipografia, grafismo isométrico,
  marca, iconografia, anatomia do deck e as armadilhas de layout já observadas.

Nenhum dos dois é específico do Módulo 03 IN. Os dois descrevem como o Inteli ensina e como o
Inteli se apresenta, e o professor tem outros módulos pela frente.

Havia duas opções: `.claude/skills/` neste repositório, ou `~/.claude/skills/`, fora dele.

## Decisão

As duas skills vivem em **`~/.claude/skills/`**, fora deste repositório:

- `~/.claude/skills/inteli-course-design/SKILL.md`
- `~/.claude/skills/inteli-deck-design/SKILL.md`

## Motivações

- **Reaproveitamento no próximo módulo.** Um módulo novo do Inteli nasce com metodologia e
  identidade prontas, sem copiar arquivo de repositório em repositório (e sem as duas cópias
  divergirem depois).
- **O escopo da skill é o Inteli, não o módulo.** Uma skill que descreve o brandbook institucional
  morando dentro do repositório de uma disciplina inverte a relação: sugere que a identidade é
  daquela disciplina.
- **O que é específico do módulo já tem lugar.** `CLAUDE.md`, os dois documentos de planejamento e
  estas ADRs são o conhecimento local. As skills cuidam do que é geral.

## Riscos conhecidos

| Risco | Mitigação |
|---|---|
| A skill sai de sincronia com o repositório (uma regra muda no tema e a skill continua descrevendo a antiga) | `CLAUDE.md` aponta para os caminhos exatos das duas skills, e os dois agentes as citam nominalmente. Toda lição nova aprendida no repositório é escrita na skill, não só no comentário do código. |
| Quem clonar o repositório em outra máquina não tem as skills, e os agentes degradam silenciosamente | Registrado em `docs/ANDAMENTO.md` e em `CLAUDE.md`. É a consequência mais séria desta decisão e não tem solução técnica dentro do repositório. |
| As skills não aparecem em `git log` nem em `git diff` deste repositório: mudanças nelas são invisíveis para quem revisa o acervo | Aceito. A alternativa (duplicar) trocaria invisibilidade por divergência, que é pior. |

## Consequências

**Positivas.** O próximo módulo Inteli começa com as duas skills prontas. As armadilhas já pagas
(especificidade de classe de estado, `?print-pdf` que não aciona `@media print`, `--window-size` que
não é viewport CSS, validador que aprova sem medir) ficam registradas onde serão lidas de novo, em
vez de num comentário de CSS deste repositório.

**Negativas.** Este repositório **não é autocontido**. Um clone limpo tem os agentes, mas não as
skills que eles mandam ler, e nada no clone falha de forma visível por causa disso: o agente
simplesmente revisa com menos critério. É o custo aceito, e está escrito no `ANDAMENTO.md` para quem
retomar o trabalho.

## ADRs relacionadas

- [ADR-001](ADR-001-reveal-js-com-tema-inteli.md) e
  [ADR-002](ADR-002-platypi-no-lugar-da-azurio.md): as decisões que a skill de design descreve.
- [ADR-005](ADR-005-quatro-artefatos-por-aula.md): a anatomia dos artefatos que a skill de
  metodologia descreve.

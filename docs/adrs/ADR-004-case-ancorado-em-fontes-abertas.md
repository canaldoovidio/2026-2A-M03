# ADR-004: Case ancorado em fontes abertas, sem bases enviadas pela LDC

**Data:** 03/08/2026
**Status:** Aceita
**Decisores:** Prof. Ovidio Lopes da Cruz Netto

## Contexto

O TAPI da Louis Dreyfus Company marca dados e resultados do projeto como **conteúdo restrito do
parceiro**. Ao mesmo tempo, este repositório é publicado inteiro no GitHub Pages: qualquer arquivo
commitado fica público, para sempre, inclusive se removido depois (fica no histórico do git).

O acervo precisa de dado real para as 14 aulas: dado sintético seria contraditório num módulo que
ensina qualidade de dado, e a skill `inteli-course-design` proíbe inventar série quando existe
série real disponível.

## Decisão

O acervo didático usa **apenas fontes abertas**, versionadas em `dados/`: as cinco séries do
IBGE/SIDRA (tabelas 1092, 1093, 1094, 7524 e 1086) e os boletins da Sindirações. Qualquer base
enviada pela LDC fica **fora deste repositório**, no repositório do projeto dos alunos.

Consequência operacional já implementada: `Turma.xlsx` (com nome, presença e nota de aluno) e o PDF
do TAPI estão em `.gitignore`, com o motivo escrito ali. O que vai para o repositório são os
derivados publicáveis: `PLANO_DE_ENSINO.md`, `PLANEJAMENTO_AULA_A_AULA.md` e
`docs/autoestudos-por-semana.md`.

## Motivações

- **Confidencialidade do parceiro.** Publicar dado marcado como restrito quebraria o acordo com a
  LDC, e um `git rm` posterior não resolveria: o commit fica no histórico.
- **Dado pessoal de aluno.** A planilha da Adalove tem nome, presença e nota. Ela é fonte de
  verdade do acervo e não pode ser versionada.
- **O acervo continua reprodutível.** Qualquer pessoa clona o repositório e roda os 14 notebooks
  do zero, sem precisar de acesso ao parceiro.
- **A aula não depende de rede.** Os CSVs estão versionados, então nenhum notebook baixa dado em
  tempo de aula. Se o SIDRA estiver fora do ar no dia, a aula acontece.

## Riscos conhecidos

| Risco | Mitigação |
|---|---|
| A série aberta não tem a granularidade que o parceiro pediu | É exatamente o assunto da [ADR-003](ADR-003-regressao-tabular-em-vez-de-series-temporais.md): a limitação virou conteúdo de aula. |
| Alguém commitar `Turma.xlsx` ou o TAPI por acidente | Os dois estão em `.gitignore` com o motivo documentado. O risco residual é `git add -f`, que não tem defesa técnica aqui. |
| Os derivados publicáveis saírem de sincronia com a planilha | `tools/extrair_autoestudos.py` regenera `docs/autoestudos-por-semana.md` a partir do `Turma.xlsx`, e o arquivo gerado avisa no topo que não deve ser editado à mão. |
| O SIDRA mudar o formato da API e `baixar_dados.py` parar de funcionar | Os CSVs versionados são a fonte de verdade do acervo; a regeneração é conveniência, não dependência. |

## Consequências

**Positivas.** O repositório pode ser público sem revisão jurídica caso a caso, e serve de vitrine
do trabalho do professor. O material é reprodutível por qualquer pessoa. Os alunos aprendem sobre
uma série real, com valor ausente real e granularidade real.

**Negativas.** O acervo didático e o projeto dos alunos ficam em repositórios diferentes, com dois
lugares para manter. E o exemplo de aula nunca é exatamente o dado que o aluno vai modelar na
entrega, o que exige, em cada aula, dizer explicitamente como a camada pública se liga à camada do
projeto.

## ADRs relacionadas

- [ADR-003](ADR-003-regressao-tabular-em-vez-de-series-temporais.md): a granularidade trimestral é
  consequência desta decisão.
- [ADR-005](ADR-005-quatro-artefatos-por-aula.md): o notebook, um dos quatro artefatos, lê sempre
  de `dados/`.

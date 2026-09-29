# ADR-016: A Aula 13 vira revisão para a Prova de 02/10, e o deploy com Streamlit passa para a Aula 14

**Data:** 28/09/2026
**Status:** Aceita
**Decisores:** Prof. Ovidio Lopes da Cruz Netto e José Romualdo

## Contexto

A Sprint 5 tem a Prova em 02/10/2026, com peso 20 na Adalove (`PLANO_DE_ENSINO.md`, seção 4), o
maior peso individual do módulo. O último Encontro de Instrução antes dela é a Aula 13, em
30/09/2026, registrada na Adalove como "Deploy de modelos de Machine Learning" e planejada para
montar o app Streamlit sobre o `app/modelo_aula12.joblib`.

O professor pediu que esse encontro seja uma revisão dos conteúdos de computação que caem na prova,
sem entregar as perguntas nem as respostas. A prova foi entregue ao acervo apenas como insumo de
escopo e fica fora do repositório, pelo mesmo motivo do `Turma.xlsx` e do TAPI: o repositório é
publicado inteiro no GitHub Pages.

Os conteúdos cobrados já foram dados entre as Aulas 02 e 11, alguns com pouco tempo de sala:
ETL, ELT, *data lake* e *data warehouse* ocuparam um slide da Aula 04, e sistemas de recomendação
foram um fecho conceitual de dez minutos na Aula 08 (`ADR-011`).

## Decisão

A Aula 13 dedica os 105 minutos de instrução a uma revisão em sala invertida dos conteúdos de
computação da prova, com exercícios ancorados no case da LDC, e o app Streamlit com histórico,
previsão e cenários passa para a Aula 14, em 06/10, junto com o fechamento do módulo.

## Motivações

- **Peso.** A prova vale 20, contra 3 da ART.9, que o app alimenta. A ART.9 fecha em 07/10, depois
  da Aula 14, então mover o app não tira o insumo da entrega.
- **Lacuna medida no próprio acervo.** Dois dos temas cobrados tiveram um slide ou dez minutos de
  sala. Uma revisão é o único ponto do calendário em que eles voltam antes da prova.
- **Sala invertida cabe no formato.** A revisão não precisa de conteúdo novo: o material de apoio e
  o notebook viram o estudo prévio, e a sala fica para votação, instrução por pares e correção
  cruzada.

## Regras que a revisão segue para não entregar a prova

1. **Nenhum cenário da prova é reaproveitado**, nem trocado de nome. Todo exercício usa o case da
   LDC, com números dos CSVs de `dados/` ou dos resultados já medidos no acervo.
2. **Nenhum número da prova aparece** em deck, material, notebook ou notas do professor.
3. **O deck lista temas, não questões.** Não informa quantas questões há por tema nem o formato de
   cada uma.
4. **O arquivo da prova nunca é copiado para o repositório.** Ele não está no `.gitignore` porque
   nunca esteve dentro da árvore de trabalho.

## Forma do app na Aula 14

O app entra como código versionado em `app/`, que roda na máquina de quem clonar o repositório, e
não é publicado como serviço externo. O acervo continua sendo site estático no GitHub Pages:
publicar o app exigiria decidir quem mantém o servidor, quem atualiza os CSVs e quem responde por
divergência de versão de biblioteca, e nenhuma dessas responsabilidades existe no módulo.

## Riscos conhecidos

- **O app Streamlit fica com um encontro de 105 minutos dividido com o fechamento do módulo.**
  Mitigação: a Aula 14 entrega o app pronto em `app/`, e a prática da dupla é adaptar e estender, em
  vez de escrever do zero.
- **O título da Adalove deixa de descrever o encontro de 30/09.** Mitigação: o título oficial
  continua nos documentos de planejamento e no portal, e o deck declara na capa que o encontro é a
  revisão para a prova.
- **Os autoestudos de Streamlit são da Semana 09 e o app é ensinado na Semana 10.** Mitigação: as
  referências da Aula 13 continuam listando esses autoestudos, que é a semana deles, e as da Aula 14
  apontam para elas.

## Consequências

- **Positivas:** a turma revisa, antes da prova, os dois temas que tiveram menos tempo de sala. O
  app chega ao encontro final já com o modelo exportado e recarregável, sem pressa de sprint.
- **Negativas:** a Aula 14 perde o ensaio cronometrado longo da apresentação final, que vira
  ensaio curto em dupla. A espiral da Aula 14 passa a resgatar a Aula 12 para o app, e não a Aula 13.

## ADRs relacionadas

- `ADR-011`: redução de sistemas de recomendação a fecho conceitual na Aula 08.
- `ADR-015`: o `Pipeline` exportado em `app/`, que a Aula 14 carrega no app.

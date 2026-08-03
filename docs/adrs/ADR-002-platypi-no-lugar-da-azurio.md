# ADR-002: Platypi como tipografia de título, em substituição à Azurio

**Data:** 03/08/2026
**Status:** Aceita
**Decisores:** Prof. Ovidio Lopes da Cruz Netto

## Contexto

O Brandbook Inteli 2025 (p.69) define **Azurio Medium** como a tipografia de título da marca. A
Azurio é uma fonte licenciada, distribuída em `.otf` no acervo institucional.

Este repositório é **público e publicado inteiro no GitHub Pages**. Empacotar os arquivos `.otf`
em `assets/` significaria republicar a fonte sob condições que a licença dela não permite. Não é
uma questão de conveniência: é redistribuição de fonte licenciada.

O próprio brandbook (p.70) prevê a situação e indica a substituta: a **Platypi**, "na
impossibilidade de uso em sistemas", por ser Google Font.

Contexto adicional que motivou olhar isso com atenção: o CSS do acervo de 2026.1 declarava
`font-family: "Azurio", "Manrope", sans-serif` sem nunca carregar a Azurio. Os títulos caíam em
Manrope silenciosamente, sem erro no console. O acervo tinha, na prática, uma tipografia de
título que ninguém escolheu.

## Decisão

Os títulos do acervo usam **Platypi**, carregada do Google Fonts, declarada uma única vez no token
`--fonte-titulo` em `assets/css/inteli-brand.css`.

## Motivações

- **É o caminho previsto pela marca**, não um contorno: a substituição está escrita na p.70 do
  brandbook.
- **Elimina a redistribuição indevida** de uma fonte licenciada num repositório público.
- **Elimina o fallback silencioso.** A fonte declarada é a fonte carregada, e
  `tools/check_brand.py` garante que nenhum outro arquivo do acervo declare `font-family`.
- Manrope (texto) e Space Mono (complementar) já são Google Fonts, então a família de título era
  a única peça fora do lugar.

## Riscos conhecidos

| Risco | Mitigação |
|---|---|
| A Platypi é serifada e a Azurio não: a capa muda de caráter | Validar a capa da Aula 01 com o professor antes do fan-out das 13 aulas restantes. É um dos itens do portão de saída do plano. |
| Alguém "corrigir" o token de volta para Azurio numa aula futura, achando que é mais fiel | O token mora num só arquivo, com o motivo em comentário, e o `check_brand.py` reprova `font-family` declarado fora dele. |
| Dependência do Google Fonts em tempo de apresentação | Se a rede cair, a cascata resolve para Georgia (serifada, mesmo caráter). Degrada sem quebrar o layout. |

## Consequências

**Positivas.** O acervo é publicável sem violar licença de fonte. A tipografia renderizada é a
tipografia decidida, verificável por `getComputedStyle` e protegida por validador. A hierarquia do
brandbook (título, texto, complementar) é preservada em razão, com piso de legibilidade de 18px
para projeção, adaptação nossa documentada na skill `inteli-deck-design`.

**Negativas.** O deck não é tipograficamente idêntico a uma peça institucional feita com Azurio.
Quem comparar lado a lado vai notar a serifa. É o preço de um repositório público.

## ADRs relacionadas

- [ADR-001](ADR-001-reveal-js-com-tema-inteli.md): o tema que aplica esta tipografia.
- [ADR-006](ADR-006-skills-globais-de-metodologia-e-design.md): a regra de citar a página do
  brandbook, e de separar citação literal de inferência nossa, vive na skill de design.

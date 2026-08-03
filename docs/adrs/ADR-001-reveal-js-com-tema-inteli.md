# ADR-001: Reveal.js com tema Inteli no lugar do motor de slides próprio

**Data:** 03/08/2026
**Status:** Aceita
**Decisores:** Prof. Ovidio Lopes da Cruz Netto

## Contexto

O acervo do Módulo 02 do Ciclo Comum (`2026.1/IN02T26`) usa um motor de slides escrito à mão:
cada deck traz o próprio HTML de navegação, o próprio controle de teclado e a própria lógica de
animação. O resultado é bonito e funciona, mas tem três consequências que só aparecem na escala
de 14 aulas:

1. **Cada deck reimplementa o motor.** Uma correção de navegação precisa ser aplicada 14 vezes.
2. **Não existe superfície para validar.** Sem um contrato de "um slide é uma `section` de
   1280x720", não há o que medir, e a única verificação possível é abrir cada deck no navegador.
3. **Não existe exportação para PDF.** O professor não tem como levar a aula impressa nem
   arquivar o material do encontro.

O acervo da FIAP (`FIAP/FIAP-2026-2-3SI`) usa Reveal.js e, justamente por isso, tem um validador
de layout que abre cada deck num navegador headless e mede se algum elemento estoura a área útil.

## Decisão

O acervo do Módulo 03 IN usa **Reveal.js 5.1.0** com um tema Inteli próprio
(`assets/css/inteli-theme.css`), em vez de um motor de slides escrito para este repositório.

## Motivações

- **Um contrato de layout mensurável.** Reveal.js fixa `width: 1280, height: 720, center: false,
  margin: 0`, e o tema dá altura fixa à `section`. Isso é o que torna possível
  `tools/check_slides.py`: conteúdo que não cabe não rola, e um elemento fora da área útil é
  detectável por medida, não por inspeção.
- **Exportação em PDF de graça.** O `?print-pdf` do próprio Reveal.js, mais
  `assets/css/inteli-print.css`, resolvem a impressão sem código nosso.
- **Fragments e navegação já resolvidos.** Nenhuma linha nossa cuida de teclado, hash de URL ou
  transição.
- **O que é nosso fica sendo só identidade e conteúdo.** O tema e as classes de slide são a única
  coisa que precisa ser mantida, e elas são CSS, não motor.

## Riscos conhecidos

| Risco | Mitigação |
|---|---|
| As animações do IN02T26 (terminal digitando, pipeline animado) não migram | O que era animação vira figura, bloco de código estático ou fragment do Reveal. Perde-se o efeito, mantém-se o conteúdo. |
| Dependência de CDN: sem rede, o deck não carrega | Aceito por ora. A sala do Inteli tem rede, e o PDF exportado é o plano B do professor. Se virar problema, versionar o Reveal em `assets/vendor/`. |
| O tema depende de detalhes internos do Reveal (por exemplo, o `style="display: block"` inline que ele escreve no slide ativo) | Registrado em comentário no próprio `inteli-theme.css`, junto com a correção. Uma atualização de major do Reveal exige rodar `check_slides.py` sobre o acervo inteiro antes de aceitar. |

## Consequências

**Positivas.** Existe validação automatizada de layout desde a fundação, e ela pegou defeitos
reais (estouro dos 720px, título colidindo com o logo). A impressão em PDF existe. Um deck novo
é só conteúdo dentro de classes que já existem, o que é o que viabiliza o fan-out das aulas 02 a
14 por agentes distintos sem deriva visual.

**Negativas.** O acervo fica menos "autoral" que o do IN02T26 e herda as armadilhas de
especificidade CSS do Reveal, todas documentadas na skill `inteli-deck-design`, seção 8. A
migração do acervo de 2026.1 para este padrão não está prevista (é não-objetivo declarado na
spec).

## ADRs relacionadas

- [ADR-002](ADR-002-platypi-no-lugar-da-azurio.md): a tipografia que este tema aplica.
- [ADR-005](ADR-005-quatro-artefatos-por-aula.md): o deck é um dos quatro artefatos por aula.
- [ADR-006](ADR-006-skills-globais-de-metodologia-e-design.md): as armadilhas deste motor moram
  numa skill global, não neste repositório.

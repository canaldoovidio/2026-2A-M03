# Fundação do acervo e Aula 01 padrão-ouro: plano de implementação

> **Para agentes:** SUB-SKILL OBRIGATÓRIA: usar `superpowers:subagent-driven-development`
> (recomendado) ou `superpowers:executing-plans` para executar tarefa a tarefa. Os passos usam
> checkbox (`- [ ]`) para rastreio.

**Goal:** Entregar a fundação técnica do acervo do Módulo 03 IN (tema fiel ao brandbook,
validadores, portal, documentos de planejamento, skills e agentes) e a Aula 01 completa como
padrão-ouro para o fan-out das 13 aulas restantes.

**Architecture:** Site estático sem build. Os decks são arquivos Reveal.js autocontidos que
consomem um único arquivo de tokens da marca. Toda regra do brandbook que dá para verificar em
código vira validador Python com suíte pytest, rodando em hook local e em CI. Os documentos de
planejamento são a fonte da verdade e o portal é gerado à mão a partir deles.

**Tech Stack:** HTML, CSS e JavaScript puro · Reveal.js 5.1.0 via jsDelivr · Python 3.11+ ·
pytest · Playwright (Chromium) · openpyxl · pandas · GitHub Pages.

## Global Constraints

Valem para toda tarefa deste plano.

- **Idioma:** português do Brasil com acentuação completa.
- **Travessão em dash (`—`) é proibido** em qualquer texto, código, comentário ou commit. Usar
  dois-pontos, vírgula, parênteses ou hífen.
- **Emoji é proibido** em deck, portal, material, referências, favicon e nome de arquivo. A
  iconografia da marca é o Google Material Symbols (Brandbook p.88).
- **Cor:** nenhum arquivo declara cor literal fora de `assets/css/inteli-brand.css`. Todo o resto
  consome `var(--inteli-*)` ou `var(--seg-*)`.
- **Paleta oficial (p.66), os únicos 9 hex permitidos:** `#2e2640` `#ff4545` `#90a5e5` `#89cea5`
  `#066d73` `#b2b6bf` `#caced6` `#e6eaeb` `#ffffff`.
- **Segmento Graduação (p.68):** `#90a5e5` (lilás, de Escolas) e `#066d73` (verde escuro, de
  Exec/Pós) **não podem ser usados** neste acervo.
- **Tipografia:** Platypi para títulos, Manrope para texto (regular a semibold), Space Mono só
  para detalhes pontuais. `font-family` só aparece em `inteli-brand.css`.
- **Legibilidade:** piso de 18px para texto corrido nos decks.
- **Deck:** Reveal.js 5.1.0, `width: 1280, height: 720, center: false, margin: 0`.
- **Commits:** Conventional Commits, escopo pela aula ou pelo componente. Autor obrigatório:
  `git -c user.name="canaldoovidio" -c user.email="canaldoovidio@users.noreply.github.com" commit`.
- **Fontes restritas:** `Turma.xlsx` e o PDF do TAPI estão no `.gitignore` e nunca são
  commitados. Os scripts leem deles no disco e produzem derivados versionáveis.

## Estrutura de arquivos

| Arquivo | Responsabilidade |
|---|---|
| `assets/css/inteli-brand.css` | tokens do brandbook, e nada além disso |
| `assets/css/inteli-theme.css` | tema do deck, consome só tokens |
| `assets/css/inteli-print.css` | modo de impressão do deck |
| `assets/js/inteli-quiz.js` | quizzes interativos |
| `assets/js/inteli-zoom.js` | zoom por teclado no deck |
| `assets/js/inteli-print.js` | botão que reabre o deck em `?print-pdf` |
| `assets/img/*.svg` | logo em 3 versões e grafismo do segmento |
| `tools/check_brand.py` | fidelidade ao brandbook |
| `tools/check_slides.py` | layout: estouro, sobreposição, título no logo |
| `tools/check_links.py` | todo href resolve |
| `tools/extrair_autoestudos.py` | `Turma.xlsx` para markdown |
| `tools/baixar_dados.py` | SIDRA para CSV versionado |
| `PLANO_DE_ENSINO.md` | fonte da verdade: ementa, cronograma, ARTs |
| `PLANEJAMENTO_AULA_A_AULA.md` | fonte da verdade: roteiro minuto a minuto |
| `index.html` | portal com cards por aula agrupados por sprint |
| `aulas/aula01.html` | deck da Aula 01 |
| `materiais/aula01.html` | material de apoio da Aula 01 |
| `referencias/aula01.html` | referências da Aula 01 |
| `notebooks/aula01.ipynb` | laboratório da Aula 01 |

---

## Task 1: Tokens da marca e validador de fidelidade

O validador vem junto com os tokens porque é ele que dá sentido à regra "cor só sai daqui".

**Files:**
- Create: `assets/css/inteli-brand.css`
- Create: `tools/check_brand.py`
- Test: `tools/tests/test_check_brand.py`
- Create: `tools/tests/__init__.py` (vazio)
- Create: `pytest.ini`

**Interfaces:**
- Consumes: nada.
- Produces: `tools/check_brand.py` expõe `varrer(raiz: str) -> list[dict]`, onde cada dict tem
  as chaves `arquivo: str`, `linha: int`, `regra: str`, `detalhe: str`. `regra` é um de
  `"cor-fora-da-paleta"`, `"cor-literal"`, `"fonte-fora-do-brand"`, `"cor-de-outro-segmento"`,
  `"emoji"`. `main() -> int` devolve 0 quando não há achado e 1 quando há.

- [ ] **Step 1: Criar o pytest.ini**

`pytest.ini`:

```ini
[pytest]
testpaths = tools/tests
python_files = test_*.py
```

- [ ] **Step 2: Escrever o teste que falha**

`tools/tests/test_check_brand.py`:

```python
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from check_brand import varrer  # noqa: E402


def _escrever(tmp_path, caminho, conteudo):
    destino = tmp_path / caminho
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(conteudo, encoding="utf-8")
    return destino


def _brand_valido(tmp_path):
    _escrever(tmp_path, "assets/css/inteli-brand.css", ":root { --inteli-roxo: #2e2640; }")


def test_paleta_valida_nao_acusa(tmp_path):
    _brand_valido(tmp_path)
    assert varrer(str(tmp_path)) == []


def test_hex_fora_da_paleta_no_brand_e_acusado(tmp_path):
    _escrever(tmp_path, "assets/css/inteli-brand.css", ":root { --x: #123456; }")
    achados = varrer(str(tmp_path))
    assert [a["regra"] for a in achados] == ["cor-fora-da-paleta"]
    assert achados[0]["linha"] == 1


def test_cor_literal_fora_do_brand_e_acusada(tmp_path):
    _brand_valido(tmp_path)
    _escrever(tmp_path, "assets/css/inteli-theme.css", ".capa { color: #2e2640; }")
    achados = varrer(str(tmp_path))
    assert [a["regra"] for a in achados] == ["cor-literal"]


def test_cor_literal_em_style_inline_e_acusada(tmp_path):
    _brand_valido(tmp_path)
    _escrever(tmp_path, "aulas/aula01.html", '<p style="color: #ffffff">oi</p>')
    achados = varrer(str(tmp_path))
    assert [a["regra"] for a in achados] == ["cor-literal"]


def test_ancora_com_letras_hex_nao_e_confundida_com_cor(tmp_path):
    _brand_valido(tmp_path)
    _escrever(tmp_path, "aulas/aula01.html", '<a href="#dados">dados</a>')
    assert varrer(str(tmp_path)) == []


def test_var_token_nao_e_acusado(tmp_path):
    _brand_valido(tmp_path)
    _escrever(tmp_path, "assets/css/inteli-theme.css", ".capa { color: var(--inteli-roxo); }")
    assert varrer(str(tmp_path)) == []


def test_font_family_fora_do_brand_e_acusada(tmp_path):
    _brand_valido(tmp_path)
    _escrever(tmp_path, "assets/css/inteli-theme.css", ".t { font-family: Arial; }")
    achados = varrer(str(tmp_path))
    assert [a["regra"] for a in achados] == ["fonte-fora-do-brand"]


def test_cor_de_outro_segmento_e_acusada_mesmo_no_brand(tmp_path):
    _escrever(tmp_path, "assets/css/inteli-brand.css", ":root { --lilas: #90a5e5; }")
    achados = varrer(str(tmp_path))
    assert [a["regra"] for a in achados] == ["cor-de-outro-segmento"]


def test_emoji_e_acusado(tmp_path):
    _brand_valido(tmp_path)
    _escrever(tmp_path, "index.html", "<h1>Aulas \U0001F4DA</h1>")
    achados = varrer(str(tmp_path))
    assert [a["regra"] for a in achados] == ["emoji"]


def test_seta_tipografica_nao_e_emoji(tmp_path):
    _brand_valido(tmp_path)
    _escrever(tmp_path, "index.html", "<p>Sprint 1 → Sprint 2</p>")
    assert varrer(str(tmp_path)) == []
```

- [ ] **Step 3: Rodar e confirmar que falha**

Run: `python3 -m pytest tools/tests/test_check_brand.py -v`
Expected: FAIL com `ModuleNotFoundError: No module named 'check_brand'`

- [ ] **Step 4: Escrever o validador**

`tools/check_brand.py`:

```python
#!/usr/bin/env python3
"""
Valida a fidelidade ao Brandbook Inteli 2025.

Cinco regras, cada uma amarrada a uma pagina do brandbook:

1. cor-fora-da-paleta   p.66  hex declarado no brand que nao esta na paleta oficial
2. cor-literal          p.66  cor literal declarada fora do arquivo de tokens
3. fonte-fora-do-brand  p.69  font-family declarado fora do arquivo de tokens
4. cor-de-outro-segmento p.68 lilas e verde escuro sao de Escolas e Exec/Pos
5. emoji                p.88  a iconografia da marca e o Material Symbols

Uso:
    python3 tools/check_brand.py
"""
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRAND = os.path.join("assets", "css", "inteli-brand.css")

PALETA = {
    "#2e2640", "#ff4545", "#90a5e5", "#89cea5", "#066d73",
    "#b2b6bf", "#caced6", "#e6eaeb", "#ffffff",
}
# p.68: pertencem a Escolas e a Exec/Pos, nao a Graduacao
OUTRO_SEGMENTO = {"#90a5e5", "#066d73"}

EXTENSOES = (".html", ".css", ".js")
IGNORAR = {".git", "node_modules", "__pycache__", ".ipynb_checkpoints"}

# Valor de declaracao CSS: tudo entre o ":" e o ";" ou o fim do bloco.
# Escanear hex solto daria falso positivo em href="#dados", cujas letras sao
# todas digitos hexadecimais validos.
DECLARACAO = re.compile(r"(?:^|[;{\"'])\s*[-a-zA-Z]+\s*:\s*([^;{}\"']*)")
HEX = re.compile(r"#[0-9a-fA-F]{3,8}\b")
FONT_FAMILY = re.compile(r"font-family\s*:")
# Blocos de emoji e simbolos pictograficos. As setas (U+2190 a U+21FF) ficam
# de fora de proposito: sao tipografia, nao emoji, e aparecem em textos como
# "Sprint 1 -> Sprint 2".
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿⬀-⯿️]")


def _normalizar(hexa):
    """Expande #abc para #aabbcc e baixa a caixa, para comparar com a paleta."""
    h = hexa.lower()
    if len(h) == 4:
        return "#" + "".join(c * 2 for c in h[1:])
    return h


def _arquivos(raiz):
    for pasta, subs, nomes in os.walk(raiz):
        subs[:] = [s for s in subs if s not in IGNORAR]
        for nome in sorted(nomes):
            if nome.endswith(EXTENSOES):
                caminho = os.path.join(pasta, nome)
                yield caminho, os.path.relpath(caminho, raiz)


def varrer(raiz):
    """Devolve a lista de achados. Lista vazia significa acervo fiel ao brandbook."""
    achados = []
    for caminho, rel in _arquivos(raiz):
        eh_brand = rel.replace(os.sep, "/") == BRAND.replace(os.sep, "/")
        with open(caminho, encoding="utf-8") as fh:
            linhas = fh.read().splitlines()

        for n, linha in enumerate(linhas, start=1):
            for valor in DECLARACAO.findall(linha):
                for bruto in HEX.findall(valor):
                    hexa = _normalizar(bruto)
                    if hexa in OUTRO_SEGMENTO:
                        achados.append({
                            "arquivo": rel, "linha": n,
                            "regra": "cor-de-outro-segmento",
                            "detalhe": "%s e do segmento Escolas ou Exec/Pos (p.68)" % bruto,
                        })
                    elif eh_brand and hexa not in PALETA:
                        achados.append({
                            "arquivo": rel, "linha": n,
                            "regra": "cor-fora-da-paleta",
                            "detalhe": "%s nao esta na paleta oficial (p.66)" % bruto,
                        })
                    elif not eh_brand:
                        achados.append({
                            "arquivo": rel, "linha": n,
                            "regra": "cor-literal",
                            "detalhe": "%s deveria vir de var(--inteli-*)" % bruto,
                        })

            if not eh_brand and FONT_FAMILY.search(linha):
                achados.append({
                    "arquivo": rel, "linha": n,
                    "regra": "fonte-fora-do-brand",
                    "detalhe": "font-family so pode ser declarado em %s" % BRAND,
                })

            achado_emoji = EMOJI.search(linha)
            if achado_emoji:
                achados.append({
                    "arquivo": rel, "linha": n, "regra": "emoji",
                    "detalhe": "%r: a iconografia da marca e o Material Symbols (p.88)"
                               % achado_emoji.group(0),
                })

    return achados


def main():
    achados = varrer(RAIZ)
    if not achados:
        print("Brandbook: paleta, tipografia, segmento e iconografia conferem.")
        return 0
    for a in achados:
        print("%s:%d  %s  %s" % (a["arquivo"], a["linha"], a["regra"], a["detalhe"]))
    print("\n%d violacao(oes) do brandbook." % len(achados))
    return 1


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 5: Rodar os testes**

Run: `python3 -m pytest tools/tests/test_check_brand.py -v`
Expected: os 10 testes passam, porque cada um monta o próprio acervo em `tmp_path`.
Se algum falhar, corrigir o validador antes de seguir.

- [ ] **Step 6: Escrever os tokens da marca**

`assets/css/inteli-brand.css`:

```css
/* Tokens do Brandbook Inteli 2025.
   Este e o unico arquivo do acervo autorizado a declarar cor e tipografia.
   Qualquer outro arquivo consome var(--inteli-*) ou var(--seg-*).
   Verificado por tools/check_brand.py. */

@import url("https://fonts.googleapis.com/css2?family=Platypi:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@24,400,0,0&display=swap");

:root {
  /* Paleta cromatica, p.66 */
  --inteli-roxo: #2e2640;
  --inteli-coral: #ff4545;
  --inteli-verde: #89cea5;
  --inteli-cinza-escuro: #b2b6bf;
  --inteli-cinza-medio: #caced6;
  --inteli-cinza-claro: #e6eaeb;
  --inteli-branco: #ffffff;

  /* Segmento Graduacao, p.68.
     Branco e cinzas como base, verde e roxo como blocos de peso,
     coral apenas como filete de destaque.
     Lilas e verde escuro pertencem a Escolas e a Exec/Pos e ficam de fora. */
  --seg-base: var(--inteli-branco);
  --seg-superficie: var(--inteli-cinza-claro);
  --seg-borda: var(--inteli-cinza-medio);
  --seg-primaria: var(--inteli-roxo);
  --seg-secundaria: var(--inteli-verde);
  --seg-destaque: var(--inteli-coral);
  --seg-texto: var(--inteli-roxo);
  --seg-texto-suave: var(--inteli-cinza-escuro);

  /* Tipografia, p.69 a p.74.
     A Azurio e licenciada e este repositorio e publico: o proprio brandbook
     (p.70) autoriza a Platypi como substituta por ser Google Font. */
  --fonte-titulo: "Platypi", Georgia, serif;
  --fonte-texto: "Manrope", system-ui, sans-serif;
  --fonte-mono: "Space Mono", monospace;

  /* Hierarquia. O brandbook (p.73) define 55/20/15pt em pagina de 1920x1080.
     A razao entre os niveis e preservada; o corpo sobe para 18px porque
     13px projetado nao se le do fundo da sala. */
  --escala-titulo: 44px;
  --escala-subtitulo: 26px;
  --escala-texto: 18px;
  --escala-complementar: 14px;
}
```

- [ ] **Step 7: Rodar o validador no acervo real**

Run: `python3 tools/check_brand.py`
Expected: `Brandbook: paleta, tipografia, segmento e iconografia conferem.` e código de saída 0.

Run: `python3 -m pytest tools/tests/test_check_brand.py -v`
Expected: 10 testes passando.

- [ ] **Step 8: Commit**

```bash
git add assets/css/inteli-brand.css tools/check_brand.py tools/tests/ pytest.ini
git -c user.name="canaldoovidio" -c user.email="canaldoovidio@users.noreply.github.com" \
  commit -m "feat(marca): tokens do brandbook e validador de fidelidade"
```

---

## Task 2: Logo e grafismo em SVG

**Files:**
- Create: `assets/img/inteli-logo-positiva.svg`
- Create: `assets/img/inteli-logo-negativa.svg`
- Create: `assets/img/inteli-logo-mono.svg`
- Create: `assets/img/inteli-grafismo-graduacao.svg`
- Test: `tools/tests/test_assets_marca.py`

**Interfaces:**
- Consumes: os tokens da Task 1 (só como referência de cor; os SVG carregam o hex nos atributos
  `fill`, que ficam **isentos** da regra `cor-literal` por não serem declaração CSS, já que
  `fill="#2e2640"` é atributo XML e não casa com o padrão `DECLARACAO`).
- Produces: quatro SVG com `viewBox` declarado, consumidos pelo tema (Task 3) e pelo portal
  (Task 9).

- [ ] **Step 1: Converter o vetor oficial da marca para SVG**

```bash
INST="/Users/joseromualdocostafilho/Projects/INTELI - INSTITUCIONAL"
mkdir -p assets/img
pdftocairo -svg "$INST/LOGO/Inteli + Assinatura/Inteli_SP_BR_01/Aberta/AF_Inteli_SP_BR_01.pdf" \
  /tmp/inteli-marca.svg
head -c 400 /tmp/inteli-marca.svg
```

- [ ] **Step 2: Conferir visualmente antes de aceitar**

```bash
pdftocairo -png -r 150 -singlefile \
  "$INST/LOGO/Inteli + Assinatura/Inteli_SP_BR_01/Aberta/AF_Inteli_SP_BR_01.pdf" /tmp/marca
```

Abrir `/tmp/marca.png` e conferir: o símbolo (as elipses que formam a esfera) precisa estar
íntegro e a palavra "inteli" precisa estar em curvas, não em texto com fonte referenciada.
Se o SVG trouxer `<text>` em vez de `<path>`, a fonte não vai existir no navegador do aluno:
nesse caso regerar com `pdftocairo -svg -nocenter` ou extrair o vetor da versão `.ai`.

Se a marca com assinatura ("Instituto de Tecnologia e Liderança / São Paulo Brasil") ficar
pesada demais para o rodapé do deck, usar `LOGO/LOGO INTELI/marca (3).ai` como origem da versão
sem assinatura. Documentar no commit qual origem foi usada.

- [ ] **Step 3: Produzir as três versões**

Salvar o resultado limpo como `assets/img/inteli-logo-positiva.svg`, com `fill="#2e2640"` nos
paths (versão para fundo claro, p.43).

`assets/img/inteli-logo-negativa.svg`: mesma geometria com `fill="#ffffff"` (fundo escuro, p.44).

`assets/img/inteli-logo-mono.svg`: mesma geometria com `fill="currentColor"`, para uso sobre
cor ou imagem (p.45).

Cada arquivo precisa ter `viewBox`, `xmlns="http://www.w3.org/2000/svg"` e nenhum atributo
`width`/`height` fixo, para escalar no rodapé e na capa.

- [ ] **Step 4: Escrever o grafismo do segmento Graduação**

Três faces isométricas em 120° (p.75 a p.78). A construção: um hexágono regular dividido em três
losangos a partir do centro. Para um hexágono de raio 100 centrado em (100, 100), os vértices
ficam em ângulos de 30°, 90°, 150°, 210°, 270° e 330°.

`assets/img/inteli-grafismo-graduacao.svg`:

```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" role="img"
     aria-label="Grafismo Inteli, segmento Graduacao">
  <title>Grafismo Inteli, tres faces em 120 graus</title>
  <!-- Face superior esquerda: verde. Face superior direita: roxo.
       Face inferior: cinza claro. Combinacao do segmento Graduacao, p.77.
       Os tres losangos partem do centro (100,100) para vertices do hexagono,
       o que garante os 120 graus exigidos na p.78. -->
  <polygon points="100,100 100,13.4 25,56.7 25,143.3" fill="#89cea5"/>
  <polygon points="100,100 100,13.4 175,56.7 175,143.3" fill="#2e2640"/>
  <polygon points="100,100 25,143.3 100,186.6 175,143.3" fill="#e6eaeb"/>
</svg>
```

Regra do brandbook que o desenho respeita e que nenhuma variação futura pode quebrar: as três
faces existem sempre, o ângulo de 120° nunca muda, e **nunca se preenche as três faces com
conteúdo** (p.82). No deck, texto sobre o grafismo é detalhe curto, nunca parágrafo.

- [ ] **Step 5: Escrever o teste dos assets**

`tools/tests/test_assets_marca.py`:

```python
import os
import xml.etree.ElementTree as ET

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IMG = os.path.join(RAIZ, "assets", "img")
SVG_NS = "{http://www.w3.org/2000/svg}"

PALETA = {"#2e2640", "#ff4545", "#89cea5", "#b2b6bf", "#caced6", "#e6eaeb", "#ffffff"}
ESPERADOS = [
    "inteli-logo-positiva.svg",
    "inteli-logo-negativa.svg",
    "inteli-logo-mono.svg",
    "inteli-grafismo-graduacao.svg",
]


def test_todos_os_assets_existem():
    for nome in ESPERADOS:
        assert os.path.isfile(os.path.join(IMG, nome)), nome


def test_todo_svg_tem_viewbox_e_escala():
    for nome in ESPERADOS:
        raiz = ET.parse(os.path.join(IMG, nome)).getroot()
        assert raiz.get("viewBox"), "%s sem viewBox" % nome
        assert raiz.get("width") is None, "%s com largura fixa" % nome
        assert raiz.get("height") is None, "%s com altura fixa" % nome


def test_todo_fill_esta_na_paleta():
    for nome in ESPERADOS:
        raiz = ET.parse(os.path.join(IMG, nome)).getroot()
        for el in raiz.iter():
            fill = (el.get("fill") or "").strip().lower()
            if not fill or fill in ("none", "currentcolor"):
                continue
            assert fill in PALETA, "%s: fill %s fora da paleta" % (nome, fill)


def test_logo_nao_usa_texto_com_fonte_externa():
    for nome in ESPERADOS[:3]:
        raiz = ET.parse(os.path.join(IMG, nome)).getroot()
        assert raiz.find(".//%stext" % SVG_NS) is None, \
            "%s tem <text>: a marca precisa estar em curvas" % nome


def test_grafismo_tem_exatamente_tres_faces():
    raiz = ET.parse(os.path.join(IMG, "inteli-grafismo-graduacao.svg")).getroot()
    faces = raiz.findall(".//%spolygon" % SVG_NS)
    assert len(faces) == 3, "o grafismo tem sempre tres modulos (p.77)"
    cores = {(f.get("fill") or "").lower() for f in faces}
    assert cores == {"#89cea5", "#2e2640", "#e6eaeb"}, \
        "combinacao do segmento Graduacao (p.77)"
```

- [ ] **Step 6: Rodar os testes**

Run: `python3 -m pytest tools/tests/test_assets_marca.py -v`
Expected: 5 testes passando.

Run: `python3 tools/check_brand.py`
Expected: sem achados. Se o SVG for acusado por `cor-literal`, é bug do validador: o padrão
`DECLARACAO` exige `:` e `fill="#2e2640"` não deveria casar. Corrigir o validador e o teste
correspondente na Task 1, não o SVG.

- [ ] **Step 7: Commit**

```bash
git add assets/img/ tools/tests/test_assets_marca.py
git -c user.name="canaldoovidio" -c user.email="canaldoovidio@users.noreply.github.com" \
  commit -m "feat(marca): logo em tres versoes e grafismo do segmento Graduacao"
```

---

## Task 3: Tema do deck

**Files:**
- Create: `assets/css/inteli-theme.css`
- Create: `assets/css/inteli-print.css`
- Create: `aulas/_fixture-tema.html`

**Interfaces:**
- Consumes: `assets/css/inteli-brand.css` (Task 1), `assets/img/*.svg` (Task 2).
- Produces: as classes de slide `cover-slide`, `section-slide`, `content-slide`, `quiz-slide`,
  `exercise-slide`, `end-slide` e os blocos `slide-title-area`, `accent-bar`, `concept-cards` /
  `concept-card`, `side-by-side`, `code-compact`, `top-bar`, `slide-footer` (com `footer-bar` e
  `footer-page`), `inteli-logo-header`. Todo deck das Tasks 14 e seguintes usa esses nomes.

- [ ] **Step 1: Escrever o tema**

O núcleo do tema, que decide se o validador de layout passa ou não. Escrever exatamente assim e
construir o resto em volta:

```css
/* Tema Reveal.js do segmento Graduacao.
   Nenhuma cor literal e nenhum font-family aqui: tudo vem de inteli-brand.css.
   Verificado por tools/check_brand.py. */

.reveal .slides section {
  /* Altura fixa: conteudo que nao cabe NAO rola, quebra o slide.
     E por isso que scrollHeight nao detecta estouro e o check_slides.py
     precisa medir o retangulo de cada descendente. */
  width: 1280px;
  height: 720px;
  padding: 44px 56px 72px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  text-align: left;
  background: var(--seg-base);
  color: var(--seg-texto);
}

.reveal p,
.reveal li {
  /* Piso de legibilidade para projecao. Nao reduzir para caber mais texto:
     se nao cabe, o slide tem conteudo demais. */
  font-size: var(--escala-texto);
  line-height: 1.5;
}

.reveal h2 { font-size: var(--escala-titulo); }
.reveal h3 { font-size: var(--escala-subtitulo); }

.accent-bar {
  width: 64px;
  height: 6px;
  background: var(--seg-secundaria);
  margin-bottom: 16px;
}

.inteli-logo-header {
  position: absolute;
  top: 28px;
  right: 28px;
  width: 96px;
  /* Resguardo da marca, p.51: a distancia minima e a largura entre o "i" e o
     "n". Para 96px de marca, 28px cobre com folga. Reduzir isso faz o titulo
     longo encostar no logo, defeito que o check_slides.py acusa como
     TITULO NO LOGO. */
}

.concept-cards { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }

.concept-card {
  background: var(--seg-superficie);
  border-top: 4px solid var(--seg-secundaria);
  border-radius: 10px;
  padding: 16px 18px;
}

.side-by-side { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }

.code-compact {
  /* Existe para o caso "bloco de codigo em slide que ja tem concept-cards".
     Sem isso o slide estoura os 720px. Manter o trecho em ate 18 linhas. */
  font-size: var(--escala-complementar);
  line-height: 1.35;
  max-height: 300px;
  overflow: hidden;
}

.slide-footer {
  position: absolute;
  left: 56px;
  right: 56px;
  bottom: 24px;
  display: flex;
  justify-content: space-between;
  font-size: var(--escala-complementar);
  color: var(--seg-texto-suave);
}
```

O resto das regras, todas igualmente verificáveis:

- `.reveal .slides section` fixa em `width: 1280px; height: 720px; padding: 44px 56px;`
- nenhum hex literal: só `var(--seg-*)` e `var(--inteli-*)`
- nenhum `font-family`: herdar de `body`, que já vem do brand
- `.reveal p, .reveal li { font-size: var(--escala-texto); }`, que é o piso de 18px
- `.reveal h2 { font-family` **não**: usar `--fonte-titulo` via uma regra em `inteli-brand.css`
  aplicada a `h1, h2, h3`. Se for preciso declarar família aqui, mover a declaração para o brand
  e consumir por herança. O validador da Task 1 é a autoridade.
- `.inteli-logo-header` posiciona `inteli-logo-positiva.svg` no canto superior direito, com
  margem mínima igual à largura entre o "i" e o "n" da marca (p.51). Na prática: `margin: 28px`
  para um logo de 96px de largura.
- `.cover-slide` usa `inteli-grafismo-graduacao.svg` como elemento de fundo, ocupando no máximo
  40% da largura e sem texto sobre as três faces (p.82).
- `.code-compact` reduz a fonte do bloco de código para `var(--escala-complementar)` e existe
  justamente para o caso "código em slide que já tem `concept-cards`".

- [ ] **Step 2: Escrever o CSS de impressão**

`assets/css/inteli-print.css`, ativado por `?print-pdf` do Reveal: `@page { size: 1280px 720px;
margin: 0 }`, `-webkit-print-color-adjust: exact` para preservar o roxo e o verde, e ocultar o
botão flutuante de impressão.

- [ ] **Step 3: Criar o deck de fixture**

`aulas/_fixture-tema.html`: um deck mínimo com um slide de cada classe, para o validador de
layout da Task 4 ter o que medir e para servir de referência viva do tema. O nome começa com
underscore para o portal não listá-lo.

Ele precisa conter, nesta ordem: `cover-slide` com o grafismo, `section-slide`, `content-slide`
com `concept-cards` de três cartões, `content-slide` com `side-by-side` e `code-compact`,
`quiz-slide` com uma pergunta e quatro opções, `exercise-slide`, `end-slide`.

Inicialização do Reveal, idêntica em todo deck:

```html
<script>
  Reveal.initialize({
    width: 1280, height: 720, center: false, margin: 0,
    hash: true, slideNumber: false, transition: 'fade'
  });
</script>
```

- [ ] **Step 4: Conferir no navegador**

```bash
python3 -m http.server 8000
```

Abrir `http://localhost:8000/aulas/_fixture-tema.html` e conferir slide a slide. Depois
`http://localhost:8000/aulas/_fixture-tema.html?print-pdf` e conferir que todos os slides
aparecem empilhados com as cores preservadas.

- [ ] **Step 5: Rodar o validador de marca**

Run: `python3 tools/check_brand.py`
Expected: sem achados. Se acusar `fonte-fora-do-brand`, mover a declaração para
`inteli-brand.css` conforme o Step 1.

- [ ] **Step 6: Commit**

```bash
git add assets/css/inteli-theme.css assets/css/inteli-print.css aulas/_fixture-tema.html
git -c user.name="canaldoovidio" -c user.email="canaldoovidio@users.noreply.github.com" \
  commit -m "feat(tema): tema Reveal.js do segmento Graduacao e deck de fixture"
```

---

## Task 4: Validador de layout

Porte do `tools/check_slides.py` do repositório da FIAP, que já resolveu três classes de defeito
que passam despercebidas: estouro dos 720px que o `scrollHeight` não detecta, bloco absoluto que
cobre o de cima sem estourar, e título que quebra por baixo do logo.

**Files:**
- Create: `tools/check_slides.py`
- Create: `tools/tests/fixture_layout.html`
- Test: `tools/tests/test_check_slides.py`

**Interfaces:**
- Consumes: `aulas/*.html` (Task 3 em diante).
- Produces: `checar(page, url, nome, shots_dir=None) -> int` (número de slides com problema) e
  `main() -> int`.

- [ ] **Step 1: Instalar as dependências**

```bash
python3 -m pip install playwright pytest
python3 -m playwright install chromium
```

- [ ] **Step 2: Portar o validador**

Copiar `/Users/joseromualdocostafilho/Projects/FIAP/FIAP-2026-2-3SI/tools/check_slides.py` para
`tools/check_slides.py` e aplicar exatamente três mudanças:

1. em `main()`, trocar `os.path.join(RAIZ, "aulas-1sem", "aulas")` por `os.path.join(RAIZ, "aulas")`
   e o prefixo `os.path.join("aulas-1sem", "aulas", f)` por `os.path.join("aulas", f)`;
2. filtrar os arquivos que começam com `_`, para o fixture do tema não entrar na varredura padrão:
   `if f.endswith(".html") and not f.startswith("_")`;
3. na mensagem de `TITULO NO LOGO`, trocar "logo da FIAP" por "logo do Inteli", e no seletor
   `[class*="logo-header"]` nada muda, porque a classe do tema é `inteli-logo-header` e casa.

O resto do arquivo, inclusive o `JS_MEDIR` inteiro e os comentários que explicam por que cada
checagem existe, é copiado sem alteração.

- [ ] **Step 3: Criar o fixture de layout quebrado**

`tools/tests/fixture_layout.html`: um deck com quatro sections, carregando o Reveal e o tema:

1. section limpa, que precisa passar;
2. section com um parágrafo de 3000 caracteres, que estoura os 720px;
3. section com dois filhos diretos, o segundo com `style="position:absolute; top:80px"`, que
   sobrepõe sem estourar;
4. section com `inteli-logo-header` e um `h2` de título longo o bastante para quebrar a segunda
   linha por baixo do logo.

- [ ] **Step 4: Escrever o teste**

`tools/tests/test_check_slides.py`:

```python
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import check_slides  # noqa: E402

sync_api = pytest.importorskip("playwright.sync_api")

FIXTURE = "tools/tests/fixture_layout.html"


@pytest.fixture(scope="module")
def servidor():
    """Sobe o servidor e o navegador uma vez para o modulo inteiro.

    Devolve (page, porta) em vez de pendurar a porta no objeto Page: Page do
    Playwright usa __slots__ em algumas versoes e a atribuicao falharia.
    """
    porta = check_slides.porta_livre()
    httpd = check_slides.servir(porta)
    with sync_api.sync_playwright() as p:
        navegador = p.chromium.launch()
        page = navegador.new_page(viewport={"width": 1280, "height": 720})
        try:
            yield page, porta
        finally:
            navegador.close()
    httpd.shutdown()


def _medir(servidor, caminho):
    page, porta = servidor
    page.goto("http://127.0.0.1:%d/%s" % (porta, caminho), wait_until="networkidle")
    page.wait_for_timeout(900)
    return page.evaluate(check_slides.JS_MEDIR)


def test_slide_limpo_nao_acusa(servidor):
    slides = _medir(servidor, FIXTURE)
    assert slides[0]["pior"] is None
    assert slides[0]["sobreposicoes"] == []
    assert slides[0]["colisoes"] == []


def test_estouro_e_detectado(servidor):
    slides = _medir(servidor, FIXTURE)
    assert slides[1]["pior"] is not None
    assert slides[1]["pior"]["abaixo"] > 2


def test_sobreposicao_sem_estouro_e_detectada(servidor):
    slides = _medir(servidor, FIXTURE)
    assert slides[2]["pior"] is None, "esse defeito nao estoura os 720px"
    assert slides[2]["sobreposicoes"], "e mesmo assim precisa ser acusado"


def test_titulo_por_baixo_do_logo_e_detectado(servidor):
    slides = _medir(servidor, FIXTURE)
    assert slides[3]["colisoes"], "titulo longo colidindo com o logo"


def test_fixture_do_tema_passa_limpo(servidor):
    slides = _medir(servidor, "aulas/_fixture-tema.html")
    sujos = [s for s in slides
             if s["pior"] or s["sobreposicoes"] or s["colisoes"]]
    assert sujos == [], "o deck de referencia do tema precisa passar limpo"
```

- [ ] **Step 5: Rodar os testes**

Run: `python3 -m pytest tools/tests/test_check_slides.py -v`
Expected: 5 testes passando. O último é o que importa: se o fixture do tema não passar limpo, o
tema da Task 3 tem defeito e precisa voltar.

- [ ] **Step 6: Commit**

```bash
git add tools/check_slides.py tools/tests/fixture_layout.html tools/tests/test_check_slides.py
git -c user.name="canaldoovidio" -c user.email="canaldoovidio@users.noreply.github.com" \
  commit -m "feat(tools): validador de layout dos decks portado da FIAP"
```

---

## Task 5: JavaScript do deck

**Files:**
- Create: `assets/js/inteli-quiz.js`
- Create: `assets/js/inteli-zoom.js`
- Create: `assets/js/inteli-print.js`
- Modify: `aulas/_fixture-tema.html` (carregar os três scripts)

**Interfaces:**
- Consumes: o markup de quiz definido aqui.
- Produces: o contrato de markup que todo deck usa:

```html
<div class="quiz-container">
  <ul class="quiz-options">
    <li data-correct="true"
        data-correct-msg="Certo: o corte e temporal, nao aleatorio."
        data-incorrect-msg="Nao: embaralhar vaza o futuro para o treino.">
      Separar treino e teste por data de corte
    </li>
  </ul>
</div>
```

- [ ] **Step 1: Escrever o inteli-quiz.js**

`assets/js/inteli-quiz.js`:

```javascript
// Quiz interativo dos decks. O JS nao declara cor nenhuma: as classes de
// estado (.certa, .errada, .revelada) sao estilizadas em inteli-theme.css,
// senao tools/check_brand.py acusa cor literal.
(function () {
  'use strict';

  function responder(quiz, opcao) {
    if (quiz.dataset.respondido === 'sim') return;
    quiz.dataset.respondido = 'sim';

    var certa = opcao.dataset.correct === 'true';
    opcao.classList.add(certa ? 'certa' : 'errada');

    if (!certa) {
      var gabarito = quiz.querySelector('[data-correct="true"]');
      if (gabarito) gabarito.classList.add('revelada');
    }

    var feedback = document.createElement('p');
    feedback.className = 'quiz-feedback';
    feedback.textContent = certa
      ? (opcao.dataset.correctMsg || 'Correto.')
      : (opcao.dataset.incorrectMsg || 'Nao e essa.');
    quiz.appendChild(feedback);
  }

  function ligar() {
    var quizzes = document.querySelectorAll('.quiz-container');
    for (var i = 0; i < quizzes.length; i++) {
      (function (quiz) {
        var opcoes = quiz.querySelectorAll('.quiz-options > li');
        for (var j = 0; j < opcoes.length; j++) {
          (function (opcao) {
            opcao.setAttribute('role', 'button');
            opcao.setAttribute('tabindex', '0');
            opcao.addEventListener('click', function () { responder(quiz, opcao); });
            opcao.addEventListener('keydown', function (e) {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                responder(quiz, opcao);
              }
            });
          })(opcoes[j]);
        }
      })(quizzes[i]);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', ligar);
  } else {
    ligar();
  }

  // Exposto para o inteli-print.js revelar o gabarito no modo de impressao
  window.IntelIQuiz = { responder: responder };
})();
```

Adicionar ao `inteli-theme.css` as três classes de estado, usando só tokens: `.certa` com borda
esquerda em `var(--seg-secundaria)`, `.errada` com borda esquerda em `var(--seg-destaque)`, e
`.revelada` com fundo `var(--seg-superficie)`.

- [ ] **Step 2: Escrever o inteli-zoom.js**

`+` e `-` ajustam `--escala-texto` do slide ativo em passos de 2px, `0` volta ao padrão. Serve
para a sala grande.

- [ ] **Step 3: Escrever o inteli-print.js**

Injeta um botão flutuante que reabre a URL atual com `?print-pdf`.

Atenção herdada da FIAP: em modo de impressão o script revela a resposta correta dos quizzes.
Escrever no topo do arquivo o comentário: `PDF gerado por aqui traz o gabarito e nao deve ser
distribuido antes da aula.`

- [ ] **Step 4: Carregar os três no fixture, nesta ordem**

```html
<script src="../assets/js/inteli-quiz.js"></script>
<script src="../assets/js/inteli-zoom.js"></script>
<script src="../assets/js/inteli-print.js"></script>
```

- [ ] **Step 5: Conferir no navegador**

Servir, abrir o fixture, clicar nas quatro opções do `quiz-slide` e confirmar: feedback correto
aparece, o quiz trava depois da primeira resposta, `+`/`-`/`0` mudam o corpo do texto, e o botão
de PDF abre o deck em `?print-pdf` com o gabarito revelado.

- [ ] **Step 6: Rodar os validadores**

Run: `python3 tools/check_brand.py && python3 -m pytest tools/tests/ -v`
Expected: tudo passando.

- [ ] **Step 7: Commit**

```bash
git add assets/js/ aulas/_fixture-tema.html
git -c user.name="canaldoovidio" -c user.email="canaldoovidio@users.noreply.github.com" \
  commit -m "feat(deck): quiz interativo, zoom por teclado e exportacao em PDF"
```

---

## Task 6: Extração dos autoestudos da Adalove

**Files:**
- Create: `tools/extrair_autoestudos.py`
- Create: `docs/autoestudos-por-semana.md` (gerado)
- Test: `tools/tests/test_extrair_autoestudos.py`

**Interfaces:**
- Consumes: `Turma.xlsx` no disco, fora do git.
- Produces: `extrair(caminho_xlsx: str) -> dict[str, dict]`, com a estrutura
  `{"Semana 01": {"autoestudos": [str, ...], "encontros": [{"data": "04/08/2026", "titulo": str}, ...]}}`,
  e `renderizar(dados: dict) -> str` devolvendo o markdown. Consumido pelas páginas de
  referência (Task 15 e o fan-out).

- [ ] **Step 1: Escrever o teste**

`tools/tests/test_extrair_autoestudos.py`:

```python
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extrair_autoestudos import extrair, renderizar  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
XLSX = os.path.join(RAIZ, "Turma.xlsx")

pytestmark = pytest.mark.skipif(
    not os.path.isfile(XLSX),
    reason="Turma.xlsx nao versionado; roda so na maquina do professor",
)


@pytest.fixture(scope="module")
def dados():
    return extrair(XLSX)


def test_dez_semanas(dados):
    assert sorted(dados) == ["Semana %02d" % n for n in range(1, 11)]


def test_quatorze_encontros_do_ovidio(dados):
    total = sum(len(s["encontros"]) for s in dados.values())
    assert total == 14


def test_primeiro_encontro_e_python_em_04_08(dados):
    primeiro = dados["Semana 01"]["encontros"][0]
    assert primeiro["data"] == "04/08/2026"
    assert primeiro["titulo"] == "Introdução ao Python"


def test_semana_04_tem_overfitting(dados):
    assert "Overfitting" in dados["Semana 04"]["autoestudos"]


def test_nenhum_nome_de_aluno_vaza_para_o_markdown(dados):
    texto = renderizar(dados)
    assert "Aluno_Nome" not in texto
    assert "Adalove Teste" not in texto


def test_markdown_tem_uma_secao_por_semana(dados):
    texto = renderizar(dados)
    for n in range(1, 11):
        assert "## Semana %02d" % n in texto
```

- [ ] **Step 2: Rodar e confirmar que falha**

Run: `python3 -m pytest tools/tests/test_extrair_autoestudos.py -v`
Expected: FAIL com `ModuleNotFoundError: No module named 'extrair_autoestudos'`

- [ ] **Step 3: Escrever o extrator**

`tools/extrair_autoestudos.py`. Regras de leitura, todas confirmadas na planilha real:

- a planilha tem uma linha por aluno e por atividade, então **deduplicar** pela tupla
  (semana, tipo, nome da atividade, data);
- filtrar `Atividade_Professor_Nome` contendo `"Ovidio"`;
- separar por `Atividade_Tipo`: `"Autoestudo"` vai para `autoestudos`, `"Encontro de Instrução"`
  vai para `encontros`;
- a coluna de data (`Atividade_Data_Inicio`) vem vazia nos autoestudos e preenchida nos encontros;
- ordenar os encontros por data, os autoestudos por nome;
- **nunca copiar coluna de aluno, nota, presença ou participação para o markdown.**

```python
#!/usr/bin/env python3
"""
Extrai do Turma.xlsx os autoestudos e encontros do Prof. Ovidio, por semana.

O Turma.xlsx tem dado pessoal de aluno (nome, presenca, nota) e por isso nao e
versionado. Este script produz o derivado publicavel: so semana, tipo, titulo e
data de atividade.

Uso:
    python3 tools/extrair_autoestudos.py > docs/autoestudos-por-semana.md
"""
import datetime
import os
import sys

import openpyxl

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PADRAO = os.path.join(RAIZ, "Turma.xlsx")
PROFESSOR = "Ovidio"


def _data(valor):
    if isinstance(valor, datetime.datetime):
        return valor.strftime("%d/%m/%Y")
    return str(valor).strip() if valor else ""


def extrair(caminho_xlsx):
    wb = openpyxl.load_workbook(caminho_xlsx, data_only=True, read_only=True)
    linhas = wb.worksheets[0].iter_rows(values_only=True)
    cab = [str(c).strip() for c in next(linhas)]
    i = {nome: pos for pos, nome in enumerate(cab)}

    vistos = set()
    dados = {}
    for linha in linhas:
        if linha[0] is None:
            continue
        professor = str(linha[i["Atividade_Professor_Nome"]] or "")
        if PROFESSOR not in professor:
            continue

        semana = str(linha[i["Atividade_Semana"]] or "").strip()
        tipo = str(linha[i["Atividade_Tipo"]] or "").strip()
        titulo = str(linha[i["Atividade_Nome"]] or "").strip()
        data = _data(linha[i["Atividade_Data_Inicio"]])

        chave = (semana, tipo, titulo, data)
        if chave in vistos:
            continue
        vistos.add(chave)

        registro = dados.setdefault(semana, {"autoestudos": [], "encontros": []})
        if tipo == "Autoestudo":
            registro["autoestudos"].append(titulo)
        elif tipo == "Encontro de Instrução":
            registro["encontros"].append({"data": data, "titulo": titulo})

    for registro in dados.values():
        registro["autoestudos"].sort()
        registro["encontros"].sort(key=lambda e: _chave_data(e["data"]))
    return dict(sorted(dados.items()))


def _chave_data(texto):
    dia, mes, ano = texto.split("/")
    return (ano, mes, dia)


def renderizar(dados):
    linhas = [
        "# Autoestudos e encontros por semana",
        "",
        "Gerado por `tools/extrair_autoestudos.py` a partir do `Turma.xlsx`.",
        "Nao editar a mao: rodar o script de novo quando a Adalove mudar.",
        "",
        "As paginas de `referencias/` consomem este arquivo. Autoestudo que nao",
        "esta aqui nao entra na pagina de referencias da aula.",
        "",
    ]
    for semana, registro in dados.items():
        linhas.append("## %s" % semana)
        linhas.append("")
        if registro["encontros"]:
            linhas.append("**Encontros de Instrução**")
            linhas.append("")
            for enc in registro["encontros"]:
                linhas.append("- %s: %s" % (enc["data"], enc["titulo"]))
            linhas.append("")
        if registro["autoestudos"]:
            linhas.append("**Autoestudos**")
            linhas.append("")
            for titulo in registro["autoestudos"]:
                linhas.append("- %s" % titulo)
            linhas.append("")
    return "\n".join(linhas)


def main():
    caminho = sys.argv[1] if len(sys.argv) > 1 else PADRAO
    if not os.path.isfile(caminho):
        print("Turma.xlsx nao encontrado em %s" % caminho, file=sys.stderr)
        return 1
    print(renderizar(extrair(caminho)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Rodar os testes**

Run: `python3 -m pytest tools/tests/test_extrair_autoestudos.py -v`
Expected: 6 testes passando.

- [ ] **Step 5: Gerar o markdown**

```bash
mkdir -p docs
python3 tools/extrair_autoestudos.py > docs/autoestudos-por-semana.md
grep -c '^- ' docs/autoestudos-por-semana.md
```

Expected: 106 itens no total (92 autoestudos e 14 encontros).

Conferir a olho que nenhum nome de aluno aparece no arquivo.

- [ ] **Step 6: Commit**

```bash
git add tools/extrair_autoestudos.py tools/tests/test_extrair_autoestudos.py \
        docs/autoestudos-por-semana.md
git -c user.name="canaldoovidio" -c user.email="canaldoovidio@users.noreply.github.com" \
  commit -m "feat(docs): extracao dos autoestudos da Adalove por semana"
```

---

## Task 7: Dados do case

**Files:**
- Create: `tools/baixar_dados.py`
- Create: `dados/*.csv` (gerados)
- Create: `dados/README.md`
- Test: `tools/tests/test_dados.py`

**Interfaces:**
- Consumes: API do SIDRA/IBGE.
- Produces: cinco CSV em `dados/`, com as colunas `periodo` (texto `AAAA-MM`), `valor` (float) e
  `unidade` (texto). Nomes exatos: `abate_bovinos.csv`, `abate_suinos.csv`, `abate_frangos.csv`,
  `producao_ovos.csv`, `producao_leite.csv`. Consumidos pelo notebook da Task 16 e por todo o
  fan-out.

- [ ] **Step 1: Escrever o baixador**

`tools/baixar_dados.py`. A API do SIDRA responde em
`https://apisidra.ibge.gov.br/values/t/{tabela}/n1/all/v/all/p/all`, devolvendo JSON em que a
**primeira linha é o cabeçalho com os rótulos** e as demais são os dados, com as chaves `D3C`
(código do período) e `V` (valor). Tabelas, conforme o TAPI:

| Tabela | Arquivo | Conteúdo |
|---|---|---|
| 1092 | `abate_bovinos.csv` | abate de bovinos |
| 1093 | `abate_suinos.csv` | abate de suínos |
| 1094 | `abate_frangos.csv` | abate de frangos |
| 7524 | `producao_ovos.csv` | produção de ovos de galinha |
| 1086 | `producao_leite.csv` | produção de leite cru |

```python
#!/usr/bin/env python3
"""
Baixa do SIDRA as series mensais de proteina animal do case da LDC.

Roda uma vez e versiona o resultado. Os notebooks leem do CSV, nunca da rede:
a aula nao pode depender de o IBGE estar no ar.

Uso:
    python3 tools/baixar_dados.py
"""
import csv
import json
import os
import sys
import urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(RAIZ, "dados")
URL = "https://apisidra.ibge.gov.br/values/t/%s/n1/all/v/all/p/all"

# Tabelas do SIDRA citadas no TAPI da Louis Dreyfus Company
SERIES = [
    ("1092", "abate_bovinos.csv"),
    ("1093", "abate_suinos.csv"),
    ("1094", "abate_frangos.csv"),
    ("7524", "producao_ovos.csv"),
    ("1086", "producao_leite.csv"),
]

# Marcadores do IBGE para dado ausente ou suprimido
AUSENTES = {"...", "..", "-", "X", "*", ""}


def baixar(tabela):
    with urllib.request.urlopen(URL % tabela, timeout=120) as resposta:
        return json.loads(resposta.read().decode("utf-8"))


def normalizar_periodo(codigo):
    """O SIDRA devolve AAAAMM; o contrato do acervo e AAAA-MM."""
    texto = str(codigo).strip()
    if len(texto) == 6 and texto.isdigit():
        return "%s-%s" % (texto[:4], texto[4:])
    return texto


def converter(bruto):
    texto = str(bruto).strip()
    if texto in AUSENTES:
        return ""
    return str(float(texto.replace(",", ".")))


def extrair_linhas(payload):
    """A primeira linha do JSON do SIDRA e o cabecalho com os rotulos."""
    cabecalho, *dados = payload
    unidade = cabecalho.get("MN", "") or cabecalho.get("MC", "")
    linhas = []
    for item in dados:
        periodo = normalizar_periodo(item.get("D3C") or item.get("D2C", ""))
        if not periodo:
            continue
        linhas.append({
            "periodo": periodo,
            "valor": converter(item.get("V", "")),
            "unidade": item.get("MN", unidade),
        })
    linhas.sort(key=lambda l: l["periodo"])
    return linhas


def main():
    os.makedirs(DESTINO, exist_ok=True)
    for tabela, nome in SERIES:
        print("baixando tabela %s para %s" % (tabela, nome))
        linhas = extrair_linhas(baixar(tabela))
        caminho = os.path.join(DESTINO, nome)
        with open(caminho, "w", encoding="utf-8", newline="") as fh:
            escritor = csv.DictWriter(fh, fieldnames=["periodo", "valor", "unidade"])
            escritor.writeheader()
            escritor.writerows(linhas)
        print("  %d linhas, de %s a %s"
              % (len(linhas), linhas[0]["periodo"], linhas[-1]["periodo"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

O nome da chave do período varia por tabela: em séries com duas dimensões o período vem em `D2C`
em vez de `D3C`, e o script já tenta as duas. Se alguma tabela devolver período vazio, inspecionar
a resposta com
`python3 -c "import json,urllib.request; print(json.loads(urllib.request.urlopen('https://apisidra.ibge.gov.br/values/t/1092/n1/all/v/all/p/all').read())[0])"`
e ajustar, registrando a diferença em `dados/README.md`.

**Verificação obrigatória antes de aceitar o resultado:** rodar
`python3 -c "import pandas; d=pandas.read_csv('dados/abate_bovinos.csv'); print(d.shape); print(d.head()); print(d.tail())"`
e conferir que a série cobre pelo menos 10 anos de dados mensais e termina em 2026. Se o formato
de resposta da API divergir do descrito acima, ajustar o parser e **registrar a diferença em
`dados/README.md`**, porque o fan-out inteiro depende desse contrato.

- [ ] **Step 2: Baixar**

```bash
mkdir -p dados
python3 tools/baixar_dados.py
ls -la dados/
```

- [ ] **Step 3: Escrever o README dos dados**

`dados/README.md`: para cada CSV, a tabela SIDRA de origem, a URL, a data do download, a unidade
e o período coberto. Mais o aviso: **os notebooks nunca acessam a rede**, leem daqui, porque a
aula não pode depender de o SIDRA estar no ar.

- [ ] **Step 4: Escrever o teste de integridade**

`tools/tests/test_dados.py`:

```python
import csv
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DADOS = os.path.join(RAIZ, "dados")

ESPERADOS = [
    "abate_bovinos.csv", "abate_suinos.csv", "abate_frangos.csv",
    "producao_ovos.csv", "producao_leite.csv",
]


def _ler(nome):
    with open(os.path.join(DADOS, nome), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def test_todos_os_csv_existem():
    for nome in ESPERADOS:
        assert os.path.isfile(os.path.join(DADOS, nome)), nome


def test_colunas_do_contrato():
    for nome in ESPERADOS:
        linhas = _ler(nome)
        assert set(linhas[0]) == {"periodo", "valor", "unidade"}, nome


def test_periodo_em_ano_mes_ordenado():
    for nome in ESPERADOS:
        periodos = [l["periodo"] for l in _ler(nome)]
        assert periodos == sorted(periodos), nome
        for p in periodos:
            ano, mes = p.split("-")
            assert len(ano) == 4 and 1 <= int(mes) <= 12, "%s: %s" % (nome, p)


def test_serie_cobre_ao_menos_dez_anos():
    for nome in ESPERADOS:
        assert len(_ler(nome)) >= 120, nome


def test_valores_sao_numericos_ou_vazios():
    for nome in ESPERADOS:
        for linha in _ler(nome):
            if linha["valor"] == "":
                continue
            float(linha["valor"])
```

- [ ] **Step 5: Rodar**

Run: `python3 -m pytest tools/tests/test_dados.py -v`
Expected: 5 testes passando.

- [ ] **Step 6: Commit**

```bash
git add tools/baixar_dados.py dados/ tools/tests/test_dados.py
git -c user.name="canaldoovidio" -c user.email="canaldoovidio@users.noreply.github.com" \
  commit -m "feat(dados): series do SIDRA versionadas para o case da LDC"
```

---

## Task 8: Documentos de planejamento

**Files:**
- Create: `PLANO_DE_ENSINO.md`
- Create: `PLANEJAMENTO_AULA_A_AULA.md`

**Interfaces:**
- Consumes: a seção 5 e a seção 6 da spec, `docs/autoestudos-por-semana.md` (Task 6).
- Produces: a fonte da verdade que o portal (Task 9) e todos os decks consomem. Nenhum outro
  arquivo pode inventar data, título ou escopo.

- [ ] **Step 1: Escrever o PLANO_DE_ENSINO.md**

Seções obrigatórias:

1. Identificação: módulo, turma GRAD IN03 2026-2A T25, professor, período de 03/08 a 07/10.
2. O case: Louis Dreyfus Company, os três modelos encadeados, as fontes de dados, as métricas
   RMSE e MAPE, e a restrição de não usar séries temporais.
3. Cronograma das 14 aulas: a tabela da seção 5 da spec, copiada na íntegra.
4. Sprints e entregas: a tabela de marcos da seção 5 da spec, com os pesos das ARTs **citados da
   Adalove**, nunca calculados nem inventados.
5. Matriz de rastreabilidade: para cada aula, quais autoestudos da semana ela pressupõe e qual
   ART ela alimenta.
6. A espiral: para cada aula, uma frase dizendo o que a aula anterior deixou pronto.

- [ ] **Step 2: Escrever o PLANEJAMENTO_AULA_A_AULA.md**

Para cada uma das 14 aulas, o roteiro do encontro no formato Inteli:

```
### Aula 01 - 04/08/2026 - Introdução ao Python  (Sprint 1)

08h00 - 10h00  Autoestudo
  Instalação do Python e Jupyter Notebooks em VS Code
  Migrando do Javascript para o Python
  Listas, Tuplas, Conjuntos e Dicionários em Python
  Aprendendo a ler erros em Python

10h00 - 10h15  Daily da equipe
  O que fiz, o que vou fazer, impedimentos.

10h15 - 12h00  Instrução em metodologia ativa
  10h15 - 10h30  Resgate: onde o modulo comeca e o que a LDC precisa prever
  10h30 - 10h50  O problema: um CSV do SIDRA com 15 anos de abate bovino
  ...
```

Regra dura, herdada da metodologia Inteli: **nenhum bloco expositivo passa de 15 minutos sem
interação direta dos alunos**. Se um bloco do roteiro passar disso, ele está errado e precisa ser
quebrado.

Os autoestudos citados em cada aula precisam existir em `docs/autoestudos-por-semana.md`, na
semana correspondente. Conferir um a um.

- [ ] **Step 3: Conferir a consistência com o cronograma**

```bash
grep -c '^### Aula' PLANEJAMENTO_AULA_A_AULA.md
```

Expected: 14.

Conferir que as 14 datas batem com a tabela do `PLANO_DE_ENSINO.md` e com
`docs/autoestudos-por-semana.md`.

- [ ] **Step 4: Commit**

```bash
git add PLANO_DE_ENSINO.md PLANEJAMENTO_AULA_A_AULA.md
git -c user.name="canaldoovidio" -c user.email="canaldoovidio@users.noreply.github.com" \
  commit -m "docs(planejamento): plano de ensino e roteiro aula a aula"
```

---

## Task 9: Portal e validador de links

**Files:**
- Create: `index.html`
- Create: `tools/check_links.py`
- Test: `tools/tests/test_check_links.py`

**Interfaces:**
- Consumes: `PLANO_DE_ENSINO.md` (Task 8), tokens (Task 1), assets (Task 2).
- Produces: `coletar(raiz: str) -> list[dict]` com as chaves `arquivo`, `linha`, `href`; e
  `quebrados(raiz: str) -> list[dict]`, o subconjunto cujo alvo local não existe.

- [ ] **Step 1: Escrever o teste do validador de links**

`tools/tests/test_check_links.py`:

```python
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from check_links import quebrados  # noqa: E402


def _escrever(tmp_path, caminho, conteudo):
    destino = tmp_path / caminho
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(conteudo, encoding="utf-8")


def test_link_para_arquivo_existente_passa(tmp_path):
    _escrever(tmp_path, "index.html", '<a href="aulas/aula01.html">Aula 1</a>')
    _escrever(tmp_path, "aulas/aula01.html", "<html></html>")
    assert quebrados(str(tmp_path)) == []


def test_link_para_arquivo_inexistente_e_acusado(tmp_path):
    _escrever(tmp_path, "index.html", '<a href="aulas/aula99.html">Aula 99</a>')
    achados = quebrados(str(tmp_path))
    assert len(achados) == 1
    assert achados[0]["href"] == "aulas/aula99.html"


def test_link_externo_e_ignorado(tmp_path):
    _escrever(tmp_path, "index.html", '<a href="https://sidra.ibge.gov.br/tabela/1092">IBGE</a>')
    assert quebrados(str(tmp_path)) == []


def test_ancora_e_ignorada(tmp_path):
    _escrever(tmp_path, "index.html", '<a href="#topo">topo</a>')
    assert quebrados(str(tmp_path)) == []


def test_query_string_nao_quebra_a_resolucao(tmp_path):
    _escrever(tmp_path, "index.html", '<a href="aulas/aula01.html?print-pdf">PDF</a>')
    _escrever(tmp_path, "aulas/aula01.html", "<html></html>")
    assert quebrados(str(tmp_path)) == []


def test_caminho_relativo_sobe_de_subpasta(tmp_path):
    _escrever(tmp_path, "aulas/aula01.html", '<a href="../index.html">voltar</a>')
    _escrever(tmp_path, "index.html", "<html></html>")
    assert quebrados(str(tmp_path)) == []
```

- [ ] **Step 2: Rodar e confirmar que falha**

Run: `python3 -m pytest tools/tests/test_check_links.py -v`
Expected: FAIL com `ModuleNotFoundError: No module named 'check_links'`

- [ ] **Step 3: Escrever o validador**

`tools/check_links.py`:

```python
#!/usr/bin/env python3
"""
Verifica que todo link local do acervo resolve para um arquivo que existe.

O portal e escrito a mao e aponta para quatro artefatos por aula, entao link
morto e a falha mais provavel do repositorio. Link externo nao e checado: a
rede nao pode derrubar o CI.

Uso:
    python3 tools/check_links.py
"""
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IGNORAR = {".git", "node_modules", "__pycache__", ".ipynb_checkpoints"}
EXTERNOS = ("http://", "https://", "mailto:", "tel:", "data:", "javascript:")

ATRIBUTO = re.compile(r"""(?:href|src)\s*=\s*["']([^"']+)["']""")


def coletar(raiz):
    """Todo link local declarado em href ou src, com arquivo e linha."""
    encontrados = []
    for pasta, subs, nomes in os.walk(raiz):
        subs[:] = [s for s in subs if s not in IGNORAR]
        for nome in sorted(nomes):
            if not nome.endswith(".html"):
                continue
            caminho = os.path.join(pasta, nome)
            with open(caminho, encoding="utf-8") as fh:
                for n, linha in enumerate(fh.read().splitlines(), start=1):
                    for href in ATRIBUTO.findall(linha):
                        alvo = href.strip()
                        if not alvo or alvo.startswith("#"):
                            continue
                        if alvo.lower().startswith(EXTERNOS):
                            continue
                        encontrados.append({
                            "arquivo": os.path.relpath(caminho, raiz),
                            "linha": n,
                            "href": alvo,
                            "base": pasta,
                        })
    return encontrados


def quebrados(raiz):
    """Subconjunto de coletar() cujo alvo nao existe no disco."""
    mortos = []
    for link in coletar(raiz):
        # Cortar query e ancora: aula01.html?print-pdf resolve para aula01.html
        alvo = link["href"].split("?")[0].split("#")[0]
        if not alvo:
            continue
        destino = os.path.normpath(os.path.join(link["base"], alvo))
        if not os.path.exists(destino):
            mortos.append({k: link[k] for k in ("arquivo", "linha", "href")})
    return mortos


def main():
    mortos = quebrados(RAIZ)
    if not mortos:
        print("Links: todos os alvos locais existem.")
        return 0
    for m in mortos:
        print("%s:%d  alvo inexistente: %s" % (m["arquivo"], m["linha"], m["href"]))
    print("\n%d link(s) quebrado(s)." % len(mortos))
    return 1


if __name__ == "__main__":
    sys.exit(main())
```

- [ ] **Step 4: Escrever o portal**

`index.html`. Estrutura: cabeçalho com o logo, o nome do módulo, o professor e o parceiro; e
cinco blocos, um por sprint, cada um com um cabeçalho `Sprint N · DD/MM a DD/MM` e a entrega da
sprint à direita.

Dentro de cada bloco, um grid de cards. Card de aula: badge `AULA NN`, data do encontro, título,
resumo de uma ou duas linhas e quatro botões (`Slides`, `Material`, `Referências`, `Notebook`).
Card de contexto, com estilo distinto e sem botões: Sprint Planning, Sprint Review, Prova e as
entregas ART com prazo.

Restrições: nenhuma cor literal, nenhum `font-family`, nenhum emoji. Ícones dos botões saem do
Material Symbols. Nas Tasks 9 a 13 só a Aula 01 tem artefatos, então os botões das aulas 02 a 14
ficam desabilitados (`aria-disabled="true"`, sem `href`), e o fan-out os habilita.

- [ ] **Step 5: Rodar todos os validadores**

Run: `python3 tools/check_links.py && python3 tools/check_brand.py && python3 -m pytest tools/tests/ -v`
Expected: tudo passando. Botão sem `href` não é link quebrado, é ausência de link.

- [ ] **Step 6: Conferir no navegador**

Servir e abrir `http://localhost:8000/`. Conferir os cinco grupos, as 14 datas e os cards de
contexto. Reduzir a janela para 900px e confirmar que o grid reflui sem quebrar.

- [ ] **Step 7: Commit**

```bash
git add index.html tools/check_links.py tools/tests/test_check_links.py
git -c user.name="canaldoovidio" -c user.email="canaldoovidio@users.noreply.github.com" \
  commit -m "feat(portal): cards por aula agrupados por sprint com validador de links"
```

---

## Task 10: Skills globais

**Files:**
- Create: `~/.claude/skills/inteli-course-design/SKILL.md`
- Create: `~/.claude/skills/inteli-deck-design/SKILL.md`

**Interfaces:**
- Consumes: as decisões das Tasks 1 a 9, que já estão em código.
- Produces: as duas skills que os agentes da Task 11 citam por nome.

- [ ] **Step 1: Escrever a inteli-course-design**

Frontmatter:

```markdown
---
name: inteli-course-design
description: Metodologia e arquitetura pedagógica para módulos de graduação do Inteli. Encontro de 2h com daily e metodologia ativa, aprendizagem em espiral, case do projeto-parceiro, amarração aula-sprint-ART-autoestudo, anatomia dos quatro artefatos por aula e convenções editoriais. Ler antes de criar ou reestruturar qualquer aula.
---
```

Conteúdo, conforme a seção 12 da spec: estrutura do encontro com os horários; a regra dos 15
minutos; a espiral; o case como espinha dorsal; a amarração obrigatória; os quatro artefatos; as
notas do professor; as convenções editoriais, incluindo a proibição do travessão em dash e do
emoji, e a regra de citar os pesos da Adalove sem inventar.

- [ ] **Step 2: Escrever a inteli-deck-design**

Frontmatter:

```markdown
---
name: inteli-deck-design
description: Identidade visual Inteli e construção de decks Reveal.js. Paleta oficial, segmentação por Graduação, tipografia com Platypi no lugar da Azurio, grafismo isométrico de 120 graus, uso da marca, iconografia Material Symbols, anatomia do deck e armadilhas de layout. Ler antes de escrever qualquer slide ou tocar no tema.
---
```

Toda regra cita a página do brandbook. Seções: paleta (p.66), segmento Graduação (p.68),
tipografia e a substituição Azurio para Platypi (p.69 a p.74), grafismo (p.75 a p.84), marca
(p.43 a p.53), iconografia (p.88), anatomia do deck, e as armadilhas.

As armadilhas, escritas como aviso e não como sugestão:

- slide que estoura os 720px **não é detectável por `scrollHeight`**, porque a section tem altura
  fixa. Usar `tools/check_slides.py`.
- `position: absolute` cobre o bloco de cima sem estourar nada. Preferir o fluxo normal.
- passar no validador não é o mesmo que o slide estar bom: ele mede o estado inicial e não vê
  fonte pequena demais nem figura espremida. Tirar screenshot de todo slide com bloco novo, SVG,
  iframe, fragment ou posicionamento absoluto.
- bloco de código junto de `concept-cards` estoura. Usar `code-compact` e no máximo 18 linhas.
- o `inteli-print.js` revela o gabarito dos quizzes: PDF exportado por ele não se distribui antes
  da aula.
- rodar o `revisor-slides` antes de commitar qualquer deck. Não é opcional e não precisa ser
  pedido.

- [ ] **Step 3: Conferir que as skills carregam**

```bash
ls -la ~/.claude/skills/inteli-course-design/SKILL.md ~/.claude/skills/inteli-deck-design/SKILL.md
head -5 ~/.claude/skills/inteli-deck-design/SKILL.md
```

Expected: frontmatter válido com `name` e `description` nas duas.

- [ ] **Step 4: Commit**

As skills vivem fora do repositório, então não há commit aqui. Registrar no `docs/ANDAMENTO.md`
(Task 11) que elas existem e onde.

---

## Task 11: Agentes, hook e documentação do repositório

**Files:**
- Create: `.claude/agents/construtor-aulas.md`
- Create: `.claude/agents/revisor-slides.md`
- Create: `.claude/settings.json`
- Create: `CLAUDE.md`
- Create: `README.md`
- Create: `docs/ANDAMENTO.md`

**Interfaces:**
- Consumes: as duas skills (Task 10) e os três validadores (Tasks 1, 4 e 9).
- Produces: os agentes que o fan-out usa.

- [ ] **Step 1: Escrever o agente construtor-aulas**

Constrói uma aula inteira, os quatro artefatos mais as notas do professor. O prompt precisa
mandar o agente: ler as duas skills antes de escrever qualquer coisa; ler o
`PLANEJAMENTO_AULA_A_AULA.md` na seção da aula; consumir os autoestudos de
`docs/autoestudos-por-semana.md`; ancorar todo exemplo nos CSV de `dados/`; e rodar
`check_brand.py`, `check_slides.py` e `check_links.py` antes de entregar.

- [ ] **Step 2: Escrever o agente revisor-slides**

Revisa um deck contra: layout (rodando o validador), fidelidade ao brandbook (rodando o
`check_brand.py` e conferindo o que o validador não vê, como fonte pequena e figura espremida),
profundidade pedagógica contra o roteiro, links e numeração de rodapé. Devolve achados
priorizados, não elogios.

- [ ] **Step 3: Escrever o hook**

`.claude/settings.json`, para o validador de layout disparar sozinho ao editar um deck:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "case \"$CLAUDE_TOOL_FILE_PATH\" in *aulas/*.html) python3 tools/check_slides.py \"$CLAUDE_TOOL_FILE_PATH\" && python3 tools/check_brand.py ;; esac"
          }
        ]
      }
    ]
  }
}
```

Conferir o nome da variável de ambiente do arquivo editado na versão do Claude Code em uso antes
de aceitar. Se o hook não disparar, testar editando `aulas/_fixture-tema.html` e observar a saída.

- [ ] **Step 4: Escrever o CLAUDE.md**

Guia do repositório, no mesmo espírito do da FIAP: o que é o repositório, os comandos (servir,
validar, exportar PDF), a arquitetura de conteúdo em três camadas (planejamento, metodologia,
materiais), o case, a anatomia do deck, as armadilhas conhecidas, a automação, e as convenções
editoriais. Precisa dizer, no topo, que `docs/ANDAMENTO.md` tem o estado atual.

- [ ] **Step 5: Escrever o README.md**

Voltado para o aluno: o módulo, o parceiro, o calendário das 14 aulas com data, a estrutura de
pastas e o link para o portal.

- [ ] **Step 6: Escrever o docs/ANDAMENTO.md**

Estado atual: o que está pronto, o que está em andamento, o que falta. Registrar que as skills
globais vivem em `~/.claude/skills/` e que o `Turma.xlsx` e o TAPI ficam fora do git de propósito.

- [ ] **Step 7: Commit**

```bash
git add .claude/ CLAUDE.md README.md docs/ANDAMENTO.md
git -c user.name="canaldoovidio" -c user.email="canaldoovidio@users.noreply.github.com" \
  commit -m "feat(agentes): construtor-aulas, revisor-slides, hook e guias do repositorio"
```

---

## Task 12: ADRs

**Files:**
- Create: `docs/adrs/ADR-001-reveal-js-com-tema-inteli.md`
- Create: `docs/adrs/ADR-002-platypi-no-lugar-da-azurio.md`
- Create: `docs/adrs/ADR-003-regressao-tabular-em-vez-de-series-temporais.md`
- Create: `docs/adrs/ADR-004-case-ancorado-em-fontes-abertas.md`
- Create: `docs/adrs/ADR-005-quatro-artefatos-por-aula.md`
- Create: `docs/adrs/ADR-006-skills-globais-de-metodologia-e-design.md`

**Interfaces:**
- Consumes: as decisões já implementadas nas Tasks 1 a 11.
- Produces: o registro das decisões, para o fan-out não relitigar nenhuma.

- [ ] **Step 1: Escrever as seis ADRs**

Estrutura mínima de cada uma, conforme a diretiva global: Data, Status, Decisores, Contexto,
Decisão em uma frase, Motivações, Riscos conhecidos com mitigação, Consequências positivas e
negativas, ADRs relacionadas.

Pontos que cada uma precisa registrar:

- **001:** o motor próprio do IN02T26 funciona, mas não tem validador e cada deck reimplementa o
  engine. Reveal.js traz `?print-pdf`, fragments e o validador da FIAP quase de graça. Risco: as
  animações do IN02T26 não migram; mitigação: o que era animação de terminal vira figura ou
  bloco de código estático.
- **002:** a Azurio é licenciada e o repositório é público; o brandbook (p.70) prevê a Platypi.
  Risco: a Platypi é serifada e a Azurio não, então a capa muda de caráter; mitigação: validar a
  capa com o professor na Aula 01 antes do fan-out.
- **003:** o TAPI proíbe séries temporais, mas o problema é de previsão mensal com horizonte de
  24 meses. Decisão: ensinar regressão tabular com defasagens, janelas móveis e sazonalidade
  codificada, e validar por corte de data. Risco: aluno aplicar `train_test_split` aleatório e
  vazar o futuro; mitigação: a Aula 09 trata vazamento temporal explicitamente e o notebook da
  Aula 05 já usa corte por data.
- **004:** o TAPI marca dados e resultados como conteúdo restrito, e o GitHub Pages publica o
  repositório inteiro. Decisão: o acervo usa só IBGE e Sindirações; bases enviadas pela LDC ficam
  no repositório do projeto dos alunos.
- **005:** deck, material, referências e notebook, e o que cada um resolve. Registrar que o plano
  de ensino por aula do IN02T26 saiu e a página de referências entrou.
- **006:** skills globais em `~/.claude/skills/` em vez de locais, para reaproveitar no próximo
  módulo. Risco: a skill sai de sincronia com o repositório; mitigação: o `CLAUDE.md` aponta para
  elas e o `revisor-slides` as cita.

- [ ] **Step 2: Commit**

```bash
git add docs/adrs/
git -c user.name="canaldoovidio" -c user.email="canaldoovidio@users.noreply.github.com" \
  commit -m "docs(adr): seis decisoes de arquitetura do acervo"
```

---

## Task 13: Integração contínua

**Files:**
- Create: `.github/workflows/validate.yml`
- Create: `.github/workflows/static.yml`

**Interfaces:**
- Consumes: os três validadores e a suíte pytest.
- Produces: o portão que impede publicar material quebrado.

- [ ] **Step 1: Escrever o workflow de validação**

`.github/workflows/validate.yml`, disparado em `push` e `pull_request`. Passos: checkout, Python
3.11, `pip install playwright pytest openpyxl pandas nbconvert jupyter`,
`python3 -m playwright install --with-deps chromium`, e então:

```bash
python3 tools/check_brand.py
python3 tools/check_links.py
python3 tools/check_slides.py
python3 -m pytest tools/tests/ -v
jupyter nbconvert --to notebook --execute --inplace notebooks/*.ipynb
```

O passo dos notebooks vai falhar enquanto não houver notebook: adicionar `|| true` **não** é a
saída. Condicionar o passo à existência de arquivo:
`if [ -n "$(ls -A notebooks/*.ipynb 2>/dev/null)" ]; then ... fi`.

O `test_extrair_autoestudos.py` já se pula sozinho no CI, porque o `Turma.xlsx` não é versionado.

- [ ] **Step 2: Escrever o workflow de publicação**

`.github/workflows/static.yml`: o mesmo padrão do IN02T26 e do repositório da FIAP, publicando o
repositório inteiro no GitHub Pages a cada push em `main`.

Escrever no topo do arquivo o comentário: `Publica o repositorio inteiro. Qualquer arquivo
commitado fica publico. Turma.xlsx e o TAPI estao no .gitignore por isso.`

- [ ] **Step 3: Rodar localmente o que o CI vai rodar**

```bash
python3 tools/check_brand.py && \
python3 tools/check_links.py && \
python3 tools/check_slides.py && \
python3 -m pytest tools/tests/ -v
```

Expected: tudo verde.

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/
git -c user.name="canaldoovidio" -c user.email="canaldoovidio@users.noreply.github.com" \
  commit -m "ci: validacao de marca, layout, links e notebooks"
```

---

## Task 14: Aula 01, o deck

Aqui acaba a fundação e começa o padrão-ouro. Este é o artefato que o professor revisa antes de
qualquer fan-out.

**Files:**
- Create: `aulas/aula01.html`
- Modify: `index.html` (habilitar o botão Slides da Aula 01)

**Interfaces:**
- Consumes: tema (Task 3), JS (Task 5), assets (Task 2), roteiro da Aula 01 no
  `PLANEJAMENTO_AULA_A_AULA.md` (Task 8), `dados/abate_bovinos.csv` (Task 7).
- Produces: o deck de referência que o `construtor-aulas` imita no fan-out.

- [ ] **Step 1: Ler as skills antes de escrever**

Carregar `inteli-course-design` e `inteli-deck-design`. Não começar pelo HTML.

- [ ] **Step 2: Escrever o deck**

`aulas/aula01.html`, seguindo a ordem canônica da seção 9 da spec. Conteúdo da Aula 01,
"Introdução ao Python", 04/08/2026, Sprint 1:

1. **Capa** com o grafismo do segmento, título, data e o nome do módulo.
2. **Agenda** com os horários do encontro, copiados do roteiro.
3. **Resgate**: primeira aula do módulo, então o resgate é o enquadramento: o que a LDC precisa
   prever e por que isso começa lendo um arquivo.
4. **O problema**: a LDC hoje projeta demanda de ração com coeficientes fixos. Mostrar o CSV de
   abate bovino com 15 anos de dados mensais e a pergunta: quanto de milho vai ser preciso em
   2027?
5. **Teoria**, em blocos de no máximo 15 minutos: tipos em Python; listas, tuplas, conjuntos e
   dicionários; ler um arquivo linha a linha; e ler erro de Python, que é autoestudo da semana e
   precisa aparecer.
6. **Quiz** de verificação, com o markup da Task 5.
7. **Hands-on**: o notebook da aula, com o link do Colab.
8. **O entregável**: a Sprint 1 fecha em 14/08 com a ART.1 (Entendimento do negócio) e a ART.2
   (UX parte 1). Dizer explicitamente o que desta aula entra ali.
9. **Referências** numeradas, apontando para `referencias/aula01.html`.
10. **Encerramento** com o copyright do professor.

Restrições que o validador vai cobrar: nenhuma cor literal, nenhum `font-family`, nenhum emoji,
nada estourando 1280x720, código em `code-compact` com no máximo 18 linhas.

- [ ] **Step 3: Rodar o validador de layout**

Run: `python3 tools/check_slides.py aulas/aula01.html`
Expected: `OK: nada estourando 1280x720, sem bloco sobreposto nem titulo no logo`

- [ ] **Step 4: Rodar o validador de marca**

Run: `python3 tools/check_brand.py`
Expected: sem achados.

- [ ] **Step 5: Tirar screenshot de todo slide com figura, SVG ou fragment**

Run: `python3 tools/check_slides.py aulas/aula01.html --shots /tmp/shots-aula01`

Abrir os PNG e conferir a olho. O validador mede o estado inicial e é cego para fonte pequena
demais e figura espremida: esse passo não é redundante.

- [ ] **Step 6: Rodar o revisor-slides**

Despachar o agente `revisor-slides` sobre `aulas/aula01.html`. Corrigir o que ele apontar antes
de commitar. Não é opcional.

- [ ] **Step 7: Habilitar o botão no portal**

Em `index.html`, no card da Aula 01, trocar o botão desabilitado de Slides por
`<a href="aulas/aula01.html">`.

Run: `python3 tools/check_links.py`
Expected: sem links quebrados.

- [ ] **Step 8: Commit**

```bash
git add aulas/aula01.html index.html
git -c user.name="canaldoovidio" -c user.email="canaldoovidio@users.noreply.github.com" \
  commit -m "feat(aula01): deck de introducao ao Python sobre a serie de abate do SIDRA"
```

---

## Task 15: Aula 01, material e referências

**Files:**
- Create: `materiais/aula01.html`
- Create: `referencias/aula01.html`
- Modify: `index.html` (habilitar os dois botões)

**Interfaces:**
- Consumes: tokens (Task 1), `docs/autoestudos-por-semana.md` (Task 6), o deck (Task 14).
- Produces: o par material mais referências que o fan-out replica.

- [ ] **Step 1: Escrever o material de apoio**

`materiais/aula01.html`, no padrão do IN02T26: cabeçalho com o título e a data, TOC lateral
fixa, navegação flutuante com os botões de voltar ao portal e ir para os slides, e o conteúdo
escrito em seções com âncora.

O material não é o roteiro do deck em prosa. Ele aprofunda o que o slide só pôde apontar: por que
dicionário resolve o problema de agrupar abate por mês, o que a mensagem de `KeyError` está
dizendo, e como o CSV do SIDRA representa mês ausente.

- [ ] **Step 2: Escrever a página de referências**

`referencias/aula01.html`, com as duas seções fixas.

**Autoestudos da semana (Adalove)**, copiados de `docs/autoestudos-por-semana.md`, Semana 01,
sem inventar nenhum. Os que se aplicam à Aula 01:

- Instalação do Python e Jupyter Notebooks em VS Code
- Migrando do Javascript para o Python
- Listas, Tuplas, Conjuntos e Dicionários em Python
- Aprendendo a ler erros em Python
- Melhor forma de aprender Python (Google Colab Notebook)
- Opcional: Listas e Tuplas, o que são e como usar estes Tipos Agregados em Python

**Leitura complementar do professor**: curadoria do professor, com o link e uma frase dizendo por
que aquilo está ali. Se o professor ainda não indicou nenhuma, a seção existe com uma linha
dizendo que será preenchida, e isso vira pendência no `docs/ANDAMENTO.md`. A seção não pode ser
omitida do HTML, porque o fan-out copia a estrutura.

- [ ] **Step 3: Rodar os validadores**

Run: `python3 tools/check_brand.py && python3 tools/check_links.py`
Expected: sem achados.

- [ ] **Step 4: Conferir no navegador**

Abrir os dois em 1440px e em 900px. A TOC lateral some abaixo de 900px por design; confirmar que
some sem deixar buraco no layout.

- [ ] **Step 5: Habilitar os botões e commitar**

```bash
git add materiais/aula01.html referencias/aula01.html index.html
git -c user.name="canaldoovidio" -c user.email="canaldoovidio@users.noreply.github.com" \
  commit -m "feat(aula01): material de apoio e pagina de referencias"
```

---

## Task 16: Aula 01, notebook e notas do professor

**Files:**
- Create: `notebooks/aula01.ipynb`
- Create: `docs/notas-do-professor/aula01.md`
- Modify: `index.html` (habilitar o botão Notebook)
- Modify: `docs/ANDAMENTO.md`

**Interfaces:**
- Consumes: `dados/abate_bovinos.csv` (Task 7).
- Produces: o notebook de referência do fan-out, que precisa executar de ponta a ponta em CI.

- [ ] **Step 1: Escrever o notebook**

`notebooks/aula01.ipynb`. Estrutura:

1. célula markdown de abertura: a aula, a data, o problema da LDC e o que o aluno vai ter feito
   ao final;
2. célula de dados: ler `../dados/abate_bovinos.csv` com a biblioteca padrão (`csv`), **sem
   pandas**, porque pandas é a Aula 03 e a espiral não pode furar;
3. tipos: contar linhas, converter `valor` para float, tratar o vazio;
4. listas e dicionários: agrupar o abate por ano e por mês;
5. ler erro: uma célula que **falha de propósito** com `KeyError`, com a mensagem explicada na
   célula markdown seguinte. Precisa ser a última linha da célula e estar marcada com
   `"tags": ["raises-exception"]` no metadata, senão o `nbconvert --execute` do CI quebra;
6. desafio: uma pergunta aberta que o aluno responde na própria célula.

Cabeçalho do notebook com o badge do Colab apontando para
`https://colab.research.google.com/github/canaldoovidio/2026-2A-M03/blob/main/notebooks/aula01.ipynb`.

O caminho relativo `../dados/` funciona no repositório mas não no Colab. Resolver com uma célula
que tenta o caminho local e cai para a URL raw do GitHub se ele não existir. Escrever essa célula
uma vez aqui, porque o fan-out inteiro vai copiá-la.

- [ ] **Step 2: Executar o notebook do zero**

```bash
jupyter nbconvert --to notebook --execute --inplace notebooks/aula01.ipynb
```

Expected: execução completa sem erro não tratado. Se a célula do `KeyError` derrubar a execução,
a tag `raises-exception` não foi aplicada.

- [ ] **Step 3: Escrever as notas do professor**

`docs/notas-do-professor/aula01.md`: as perguntas socráticas do encontro, na ordem do roteiro.
Não é resumo do deck. São as perguntas que o professor faz quando a sala trava, com a resposta
esperada e o erro comum que ela costuma revelar.

- [ ] **Step 4: Atualizar o ANDAMENTO**

Registrar em `docs/ANDAMENTO.md`: fundação concluída, Aula 01 completa e pronta para revisão do
professor, aulas 02 a 14 pendentes, e qualquer pendência aberta (por exemplo, a curadoria de
leitura complementar da Task 15).

- [ ] **Step 5: Rodar a bateria completa**

```bash
python3 tools/check_brand.py && \
python3 tools/check_links.py && \
python3 tools/check_slides.py && \
python3 -m pytest tools/tests/ -v && \
jupyter nbconvert --to notebook --execute --inplace notebooks/aula01.ipynb
```

Expected: tudo verde. É exatamente o que o CI vai rodar.

- [ ] **Step 6: Commit**

```bash
git add notebooks/aula01.ipynb docs/notas-do-professor/aula01.md index.html docs/ANDAMENTO.md
git -c user.name="canaldoovidio" -c user.email="canaldoovidio@users.noreply.github.com" \
  commit -m "feat(aula01): notebook do laboratorio e notas do professor"
```

---

## Portão de saída

Antes de escrever o plano do fan-out, a Aula 01 precisa ser revisada pelo professor no navegador,
não só pelos validadores. O que o professor aprova ali vira o contrato que os cinco agentes do
fan-out seguem: se a capa, a densidade dos slides ou o tom do material mudarem depois, muda em 14
lugares.

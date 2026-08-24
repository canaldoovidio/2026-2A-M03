"""Gera os quatro SVG animados da Aula 05, a partir dos CSVs reais do SIDRA.

Por que SVG inline, e nao <img src="x.svg">:

- um `.svg` carregado por `<img>` nao enxerga as custom properties do documento,
  entao ele precisaria de cor literal dentro do arquivo, o que
  `tools/check_brand.py` reprova. Inline, o SVG consome `var(--seg-*)` como
  qualquer outro elemento do deck.
- animacao declarativa (SMIL, `<animate>` e `<animateTransform>`) roda dentro do
  `<img>`, mas nao daria para herdar o tema. Inline resolve as duas coisas.

Por que SMIL e nao `@keyframes` CSS: o tema do deck e um arquivo compartilhado
pelas 14 aulas, e regra de animacao especifica de uma aula nao pertence a ele.
SMIL mantem a animacao dentro do proprio SVG, sem tocar em `inteli-theme.css`.

**O primeiro quadro precisa ser legivel sozinho.** O PDF exportado congela a
animacao no estado inicial, e o professor revisa a aula por ele. Por isso todo
`<animate>` aqui parte de um estado que ja mostra o essencial, e a animacao
acrescenta a leitura em vez de revela-la: nenhum SVG comeca vazio.

Dado real, nunca ilustrativo: as quatro figuras plotam as 113 linhas da base
analitica, as previsoes do modelo da aula e as bandas medidas em 21 origens de
previsao. Os numeros batem com `notebooks/aula05.ipynb` e com
`tools/tests/test_modelo_aula05.py`.

Uso:
    python3 tools/svg_aula05.py            # escreve os quatro blocos no deck
    python3 tools/svg_aula05.py --mostrar  # imprime, sem tocar no arquivo

O deck marca cada bloco com <!-- svg:nome --> e <!-- /svg:nome -->, e o script
substitui apenas o miolo, entao rodar de novo e idempotente.
"""
import os
import re
import sys

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECK = os.path.join(RAIZ, "aulas", "aula05.html")

SERIES = ["abate_bovinos", "abate_suinos", "abate_frangos",
          "producao_ovos", "producao_leite"]
ALVO = "abate_frangos"
FEATURES = ["frangos_lag1", "frangos_lag4", "sen", "cos"]
N_TESTE = 8

# A area util de um slide de conteudo, ja descontados titulo e rodape.
L, ALT = 1120, 340


def base_analitica():
    base = None
    for nome in SERIES:
        coluna = (pd.read_csv(os.path.join(RAIZ, "dados", nome + ".csv"))
                  [["periodo", "valor"]].rename(columns={"valor": nome}))
        base = coluna if base is None else base.merge(coluna, on="periodo", how="inner")
    base = base.sort_values("periodo").reset_index(drop=True)
    base["trimestre"] = base["periodo"].str[-1].astype(int)
    base["frangos_lag1"] = base[ALVO].shift(1)
    base["frangos_lag4"] = base[ALVO].shift(4)
    base["sen"] = np.sin(2 * np.pi * base["trimestre"] / 4)
    base["cos"] = np.cos(2 * np.pi * base["trimestre"] / 4)
    return base.dropna().reset_index(drop=True)


def treinar(base, n_treino):
    treino = base.iloc[:n_treino]
    escalador = StandardScaler().fit(treino[FEATURES].to_numpy(float))
    modelo = LinearRegression().fit(
        escalador.transform(treino[FEATURES].to_numpy(float)),
        treino[ALVO].to_numpy(float))
    return modelo, escalador


def prever_recursivo(base, modelo, escalador, n_treino, passos=N_TESTE):
    """Realimenta a propria previsao, que e o que o horizonte de 24 meses exige."""
    historico = list(base[ALVO].to_numpy(float)[:n_treino])
    saida = []
    for k in range(passos):
        tri = base["trimestre"].iloc[n_treino + k]
        x = np.array([[historico[-1], historico[-4],
                       np.sin(2 * np.pi * tri / 4), np.cos(2 * np.pi * tri / 4)]])
        y = float(modelo.predict(escalador.transform(x))[0])
        saida.append(y)
        historico.append(y)
    return np.array(saida)


def bandas_por_horizonte(base, origens=21):
    """Percentil 90 do erro relativo em cada horizonte, sobre varias origens."""
    por_h = {h: [] for h in range(1, N_TESTE + 1)}
    fim = len(base) - N_TESTE
    for n_treino in range(fim - origens + 1, fim + 1):
        modelo, escalador = treinar(base, n_treino)
        previsto = prever_recursivo(base, modelo, escalador, n_treino)
        real = base[ALVO].to_numpy(float)[n_treino:n_treino + N_TESTE]
        for h in range(N_TESTE):
            por_h[h + 1].append((previsto[h] - real[h]) / real[h] * 100)
    return {h: float(np.percentile(np.abs(v), 90)) for h, v in por_h.items()}


def _eixo(x1, y1, x2, y2):
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="var(--seg-borda)" '
            'stroke-width="2"/>' % (x1, y1, x2, y2))


def _texto(x, y, txt, tam=17, cor="var(--seg-texto)", anc="start", peso="400"):
    return ('<text x="%.1f" y="%.1f" font-size="%d" fill="%s" text-anchor="%s" '
            'font-weight="%s">%s</text>' % (x, y, tam, cor, anc, peso, txt))


# ---------------------------------------------------------------- 1. horizonte
def svg_horizonte(base):
    """O erro da previsao recursiva se acumula, e a banda alarga com o horizonte."""
    n_treino = len(base) - N_TESTE
    modelo, escalador = treinar(base, n_treino)
    previsto = prever_recursivo(base, modelo, escalador, n_treino)
    real = base[ALVO].to_numpy(float)[n_treino:]
    erro = (previsto - real) / real * 100
    banda = bandas_por_horizonte(base)
    periodos = list(base["periodo"])[n_treino:]

    esq, dir_, topo, base_y = 92, L - 30, 24, ALT - 54
    lim = 9.0                                    # +-9% cobre banda e erro
    px = lambda h: esq + (dir_ - esq) * (h - 1) / (N_TESTE - 1)
    py = lambda v: topo + (base_y - topo) * (lim - v) / (2 * lim)

    p = ['<svg viewBox="0 0 %d %d" width="100%%" height="%d" role="img" '
         'aria-label="A previsão recursiva erra cada vez mais longe do ponto de partida: '
         'o erro vai de -1,02%% no primeiro trimestre a -6,95%% no oitavo, e a banda de 90%% '
         'alarga de mais ou menos 4,17%% para mais ou menos 6,44%%">' % (L, ALT, ALT)]

    # banda: cresce com o horizonte, desenhada como area
    cima = " ".join("%.1f,%.1f" % (px(h), py(banda[h])) for h in range(1, N_TESTE + 1))
    baixo = " ".join("%.1f,%.1f" % (px(h), py(-banda[h]))
                     for h in range(N_TESTE, 0, -1))
    p.append('<polygon points="%s %s" fill="var(--seg-secundaria)" opacity="0.30">'
             '<animate attributeName="opacity" values="0.30;0.55;0.30" dur="4s" '
             'repeatCount="indefinite"/></polygon>' % (cima, baixo))
    p.append(_texto(dir_, topo + 14, "banda de 90% dos erros, medida em 21 origens", 16,
                    "var(--seg-texto)", "end"))

    # zero
    p.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="var(--seg-borda)" '
             'stroke-width="2" stroke-dasharray="6 5"/>' % (esq, py(0), dir_, py(0)))

    # eixos e rotulos
    p.append(_eixo(esq, topo, esq, base_y))
    for v in (-6, -3, 0, 3, 6):
        p.append(_texto(esq - 12, py(v) + 6, "%+d%%" % v, 16, "var(--seg-texto)", "end"))

    # linha do erro. A versao fraca fica sempre desenhada por baixo: o PDF congela
    # a animacao num instante qualquer, e sem ela a trajetoria sairia pela metade.
    pontos = " ".join("%.1f,%.1f" % (px(h), py(erro[h - 1]))
                      for h in range(1, N_TESTE + 1))
    p.append('<polyline points="%s" fill="none" stroke="var(--seg-destaque)" '
             'stroke-width="4" stroke-linejoin="round" opacity="0.28"/>' % pontos)
    p.append('<polyline points="%s" fill="none" stroke="var(--seg-destaque)" '
             'stroke-width="4" stroke-linejoin="round" pathLength="1" '
             'stroke-dasharray="1" stroke-dashoffset="1">'
             '<animate attributeName="stroke-dashoffset" from="1" to="0" dur="4s" '
             'repeatCount="indefinite"/></polyline>' % pontos)

    for h in range(1, N_TESTE + 1):
        atraso = 4.0 * (h - 1) / N_TESTE
        p.append('<circle cx="%.1f" cy="%.1f" r="7" fill="var(--seg-destaque)" '
                 'opacity="0.3"/>' % (px(h), py(erro[h - 1])))
        p.append('<circle cx="%.1f" cy="%.1f" r="7" fill="var(--seg-destaque)" '
                 'opacity="0"><animate attributeName="opacity" values="0;1;1;0" '
                 'keyTimes="0;%.3f;0.97;1" dur="4s" repeatCount="indefinite"/></circle>'
                 % (px(h), py(erro[h - 1]), min(0.95, atraso / 4.0 + 0.02)))
        p.append(_texto(px(h), base_y + 22, "h%d" % h, 16, "var(--seg-texto)", "middle"))
        p.append(_texto(px(h), base_y + 42, periodos[h - 1][2:], 15,
                        "var(--seg-texto)", "middle"))

    # os dois extremos, sempre visiveis (o PDF congela no primeiro quadro)
    p.append(_texto(px(1) + 14, py(erro[0]) - 14, "%.2f%%" % erro[0], 18,
                    "var(--seg-destaque)", "start", "700"))
    p.append(_texto(px(8) - 10, py(erro[7]) + 26, "%.2f%%" % erro[7], 18,
                    "var(--seg-destaque)", "end", "700"))
    p.append("</svg>")
    return "\n".join(p)


# ------------------------------------------------------------------- 2. corte
def svg_corte(base):
    """As 113 linhas em ordem: o corte por data contra o teste sorteado."""
    n = len(base)
    n_treino = n - N_TESTE
    _, sorteado = train_test_split(base, test_size=N_TESTE, random_state=42)
    idx_sorteado = sorted(int(i) for i in sorteado.index)

    esq, larg = 40, L - 80
    passo = larg / n
    y_top, y_bot, h = 74, 214, 46

    p = ['<svg viewBox="0 0 %d %d" width="100%%" height="%d" role="img" '
         'aria-label="As 113 linhas da base em ordem cronológica. No corte por data os oito '
         'trimestres de teste ficam juntos no fim da série; no sorteio aleatório eles se '
         'espalham por 29 anos, cada um cercado de vizinhos que ficaram no treino">'
         % (L, ALT, ALT)]

    def faixa(y, destaques, rotulo, detalhe):
        saida = [_texto(esq, y - 14, rotulo, 19, "var(--seg-texto)", "start", "700"),
                 _texto(esq + 320, y - 14, detalhe, 17)]
        for i in range(n):
            cor = ("var(--seg-destaque)" if i in destaques else "var(--seg-borda)")
            saida.append('<rect x="%.2f" y="%d" width="%.2f" height="%d" fill="%s" rx="1"/>'
                         % (esq + i * passo, y, max(passo - 1.1, 1.6), h, cor))
        return saida

    # o marcador vem primeiro, para as barras e os rotulos ficarem por cima dele
    p.append('<rect x="%.2f" y="%d" width="%.2f" height="%d" fill="var(--seg-primaria)" '
             'opacity="0.22" rx="2">'
             '<animate attributeName="x" values="%.1f;%.1f;%.1f" dur="9s" '
             'repeatCount="indefinite"/></rect>'
             % (esq, y_top - 6, max(passo + 2, 5), (y_bot + h) - (y_top - 6) + 6,
                esq, esq + larg - passo, esq))

    p += faixa(y_top, set(range(n_treino, n)), "corte por data",
               "os 8 de teste ficam juntos, no fim: extrapolar")
    p += faixa(y_bot, set(idx_sorteado), "train_test_split",
               "os 8 se espalham por 29 anos: interpolar")

    for i, rot in ((0, base["periodo"].iloc[0]), (n - 1, base["periodo"].iloc[-1])):
        p.append(_texto(esq + i * passo, y_bot + h + 26, rot, 16, "var(--seg-texto)",
                        "middle" if i else "start"))
    p.append(_texto(esq, ALT - 8,
                    "cada barra é um trimestre; em coral, os 8 reservados para teste", 16))
    p.append("</svg>")
    return "\n".join(p)


# --------------------------------------------------------- 3. minimos quadrados
def svg_minimos(base):
    """A reta gira ate minimizar a soma dos quadrados dos residuos."""
    x = base["frangos_lag1"].to_numpy(float) / 1e9
    y = base[ALVO].to_numpy(float) / 1e9
    modelo = LinearRegression().fit(x.reshape(-1, 1), y)
    a_fim, b_fim = float(modelo.coef_[0]), float(modelo.intercept_)
    a_ini, b_ini = 0.55, 1.05          # reta de partida, deliberadamente torta

    esq, dir_, topo, base_y = 96, L - 250, 26, ALT - 52
    x0, x1 = 0.8, 3.85
    px = lambda v: esq + (dir_ - esq) * (v - x0) / (x1 - x0)
    py = lambda v: base_y - (base_y - topo) * (v - x0) / (x1 - x0)

    p = ['<svg viewBox="0 0 %d %d" width="100%%" height="%d" role="img" '
         'aria-label="Dispersão do abate de frangos contra o abate do trimestre anterior, '
         'com uma reta que gira até minimizar a soma dos quadrados dos resíduos, chegando a '
         'inclinação 0,9952">' % (L, ALT, ALT)]
    p.append(_eixo(esq, topo, esq, base_y))
    p.append(_eixo(esq, base_y, dir_, base_y))

    # residuos: segmentos verticais do ponto ate a reta, encolhendo junto com ela
    for xi, yi in zip(x, y):
        y_ini, y_fim = a_ini * xi + b_ini, a_fim * xi + b_fim
        p.append('<line x1="%.1f" x2="%.1f" y1="%.1f" y2="%.1f" '
                 'stroke="var(--seg-destaque)" stroke-width="1.6" opacity="0.5">'
                 '<animate attributeName="y2" values="%.1f;%.1f;%.1f" dur="6s" '
                 'repeatCount="indefinite"/></line>'
                 % (px(xi), px(xi), py(yi), py(y_fim), py(y_ini), py(y_fim), py(y_ini)))
    for xi, yi in zip(x, y):
        p.append('<circle cx="%.1f" cy="%.1f" r="4.5" fill="var(--seg-primaria)" '
                 'opacity="0.85"/>' % (px(xi), py(yi)))

    p.append('<line x1="%.1f" x2="%.1f" y1="%.1f" y2="%.1f" stroke="var(--seg-texto)" '
             'stroke-width="4" stroke-linecap="round">'
             '<animate attributeName="y1" values="%.1f;%.1f;%.1f" dur="6s" '
             'repeatCount="indefinite"/>'
             '<animate attributeName="y2" values="%.1f;%.1f;%.1f" dur="6s" '
             'repeatCount="indefinite"/></line>'
             % (px(x0), px(x1), py(a_fim * x0 + b_fim), py(a_fim * x1 + b_fim),
                py(a_ini * x0 + b_ini), py(a_fim * x0 + b_fim), py(a_ini * x0 + b_ini),
                py(a_ini * x1 + b_ini), py(a_fim * x1 + b_fim), py(a_ini * x1 + b_ini)))

    p.append(_texto(esq - 12, topo + 14, "hoje", 17, "var(--seg-texto)", "end"))
    p.append(_texto(dir_, base_y + 30, "trimestre anterior", 17, "var(--seg-texto)", "middle"))
    lx = dir_ + 30
    p.append(_texto(lx, topo + 44, "cada risco coral", 17))
    p.append(_texto(lx, topo + 68, "é um resíduo, e a", 17))
    p.append(_texto(lx, topo + 92, "reta para onde a", 17))
    p.append(_texto(lx, topo + 116, "soma dos quadrados", 17))
    p.append(_texto(lx, topo + 140, "é menor.", 17))
    p.append(_texto(lx, topo + 184, ("inclinação: %.4f" % a_fim).replace(".", ","), 19,
                    "var(--seg-texto)", "start", "700"))
    p.append(_texto(lx, topo + 210, "113 trimestres reais", 16))
    p.append("</svg>")
    return "\n".join(p)


# ---------------------------------------------------------------- 4. as bandas
def svg_bandas(base):
    """A mesma banda em kg vale +-17% em 1998 e +-4% em 2026."""
    n_treino = len(base) - N_TESTE
    modelo, escalador = treinar(base, n_treino)
    treino = base.iloc[:n_treino]
    residuos = (treino[ALVO].to_numpy(float)
                - modelo.predict(escalador.transform(treino[FEATURES].to_numpy(float))))
    meia = 1.96 * residuos.std(ddof=len(FEATURES) + 1) / 1e9

    serie = base[ALVO].to_numpy(float) / 1e9
    n = len(serie)
    esq, dir_, topo, base_y = 78, L - 268, 28, ALT - 62
    ymax = 4.15
    px = lambda i: esq + (dir_ - esq) * i / (n - 1)
    py = lambda v: base_y - (base_y - topo) * v / ymax

    p = ['<svg viewBox="0 0 %d %d" width="100%%" height="%d" role="img" '
         'aria-label="A série de abate de frangos de 1998 a 2026 com uma banda de largura fixa '
         'de mais ou menos 150 milhões de quilogramas percorrendo-a. A mesma banda vale mais ou '
         'menos 17,02%% no início da série e mais ou menos 4,01%% no fim">' % (L, ALT, ALT)]
    p.append(_eixo(esq, topo, esq, base_y))
    for v in (1, 2, 3, 4):
        p.append(_texto(esq - 10, py(v) + 6, "%d" % v, 16, "var(--seg-texto)", "end"))
    p.append(_texto(esq - 10, topo - 6, "bi kg", 15, "var(--seg-texto)", "end"))

    linha = " ".join("%.1f,%.1f" % (px(i), py(v)) for i, v in enumerate(serie))
    p.append('<polyline points="%s" fill="none" stroke="var(--seg-primaria)" '
             'stroke-width="3"/>' % linha)

    # a banda de largura fixa, deslizando sobre a serie
    larg = 34.0
    valores_x = ";".join("%.1f" % (px(i) - larg / 2) for i in range(0, n, 4))
    valores_y = ";".join("%.1f" % (py(serie[i] + meia)) for i in range(0, n, 4))
    altura = abs(py(0) - py(2 * meia))
    p.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" '
             'fill="var(--seg-destaque)" opacity="0.45" rx="3">'
             '<animate attributeName="x" values="%s" dur="11s" repeatCount="indefinite"/>'
             '<animate attributeName="y" values="%s" dur="11s" repeatCount="indefinite"/>'
             '</rect>' % (px(0) - larg / 2, py(serie[0] + meia), larg, altura,
                          valores_x, valores_y))

    for i, rot in ((0, "1998"), (n - 1, "2026")):
        p.append(_texto(px(i), base_y + 24, rot, 16, "var(--seg-texto)", "middle"))

    lx = dir_ + 28
    p.append(_texto(lx, topo + 26, "a MESMA banda,", 17))
    p.append(_texto(lx, topo + 50, "±150 milhões de kg:", 17))
    p.append(_texto(lx, topo + 96, "em 1998", 17))
    p.append(_texto(lx, topo + 122, "±17,02%", 22, "var(--seg-destaque)", "start", "700"))
    p.append(_texto(lx, topo + 166, "em 2026", 17))
    p.append(_texto(lx, topo + 192, "±4,01%", 22, "var(--seg-texto)", "start", "700"))
    p.append(_texto(esq, ALT - 10,
                    "largura constante em quilos, incerteza relativa que muda o tempo todo", 16))
    p.append("</svg>")
    return "\n".join(p)


BLOCOS = {
    "horizonte": svg_horizonte,
    "corte": svg_corte,
    "minimos": svg_minimos,
    "bandas": svg_bandas,
}


def main():
    base = base_analitica()
    gerados = {nome: fn(base) for nome, fn in BLOCOS.items()}

    if "--mostrar" in sys.argv:
        for nome, svg in gerados.items():
            print("=" * 30, nome, "=" * 30)
            print(svg[:400], "...")
        return

    deck = open(DECK, encoding="utf-8").read()
    trocados = 0
    for nome, svg in gerados.items():
        padrao = re.compile(r"(<!-- svg:%s -->).*?(<!-- /svg:%s -->)" % (nome, nome),
                            re.S)
        if not padrao.search(deck):
            print("aviso: ancora <!-- svg:%s --> nao encontrada no deck" % nome)
            continue
        deck = padrao.sub(lambda m: m.group(1) + "\n" + svg + "\n        " + m.group(2),
                          deck)
        trocados += 1
    open(DECK, "w", encoding="utf-8").write(deck)

    if trocados != len(BLOCOS):
        raise SystemExit("apenas %d de %d blocos foram inseridos" % (trocados, len(BLOCOS)))
    print("%d SVG inseridos em aulas/aula05.html" % trocados)
    for nome, svg in gerados.items():
        print("  %-10s %5d caracteres" % (nome, len(svg)))


if __name__ == "__main__":
    main()

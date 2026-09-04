"""Gera as figuras da Aula 07 a partir dos CSVs mensais em dados/mensal/.

Duas figuras, cada uma sustentando um achado que a aula mede ao vivo sobre o
contraste entre alvo em nivel e alvo em razao para a arvore de decisao:

1. `aula07-teto-da-arvore.png`. Painel unico sobre os 24 meses de teste
   (2024-04 a 2026-03), com o real de `abate_frangos` em linha cheia e a
   previsao da arvore (`max_depth=3`) em linha escalonada (`steps-mid`), que
   se repete em patamares porque a arvore so pode prever a media de uma das
   suas 8 folhas. Duas linhas horizontais de referencia: o teto da arvore
   (a maior previsao que ela emite, 1.090.166.234, a media da folha mais
   alta) e o maximo do alvo visto no treino (1.226.709.256, em 2023-03). O
   alvo cresce ao longo do teste e a maior parte dele fica acima do teto: 23
   dos 24 meses, sombreados para tornar essa area visivel. E o achado por
   tras de H3: a arvore nao extrapola, entao ela erra sistematicamente para
   baixo quando a serie continua subindo depois do treino.

2. `aula07-nivel-versus-razao.png`. Dois paineis lado a lado sobre o mesmo
   eixo de tempo (os mesmos 24 meses de teste) e, de proposito, o mesmo
   limite de eixo y: a esquerda a arvore treinada com o alvo em nivel (MAPE
   7,66%), a direita a mesma arvore treinada com o alvo em razao sobre
   `lag12` e reconvertida a nivel (MAPE 3,86%). Compartilhar o eixo y e o que
   faz a diferenca de aderencia entre os dois paineis ser comparavel a olho
   nu: se cada painel escalasse sozinho, os dois erros pareceriam do mesmo
   tamanho, o oposto do que H4 declara.

Decisoes de forma, herdadas de `tools/graficos_aula06.py`:

- roxo #2e2640 como tinta (serie real), coral #ff4545 como destaque (previsao
  da arvore), cinza escuro #b2b6bf e verde #89cea5 como as duas linhas de
  referencia da Figura 1, cinza claro #e6eaeb no sombreamento. Todas as cinco
  cores vem dos tokens de `assets/css/inteli-brand.css`, comentadas abaixo com
  a origem de cada uma.
- nenhum valor interpolado ou inventado: as figuras plotam os CSVs de
  `dados/mensal/` e a arvore ajustada sobre eles, com a mesma logica de juncao,
  defasagem e corte temporal de `tools/tests/test_modelos_aula07.py` (Task 2)
  e de `.superpowers/sdd/2026-09-03-aula07/global-constraints.md`,
  reimplementada aqui de proposito em vez de importada: se as duas
  implementacoes divergirem, o acervo descobre. O notebook da aula reimplementa
  a mesma definicao pela mesma razao: precisa rodar sozinho no Colab.
- tamanho de fonte e largura de figura seguem a mesma conta de
  `tools/graficos_aula04.py` e `tools/graficos_aula06.py`: com dpi 160 e
  exibicao a 900px em 12 polegadas de largura, os tamanhos partem de 18, o
  piso de legibilidade que o tema fixa para texto de slide.

Uso: python3 tools/graficos_aula07.py   (requer matplotlib, pandas, numpy,
scikit-learn, listados em requirements-ci.txt)
"""
import calendar
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeRegressor

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MENSAL = os.path.join(RAIZ, "dados", "mensal")

# cores lidas de assets/css/inteli-brand.css (paleta da Graduacao, p.66/p.68)
TINTA = "#2e2640"          # --inteli-roxo: serie real
DESTAQUE = "#ff4545"       # --inteli-coral: previsao da arvore
REFERENCIA_1 = "#b2b6bf"   # --inteli-cinza-escuro: linha do teto da arvore
REFERENCIA_2 = "#89cea5"   # --inteli-verde: linha do maximo do treino
SOMBRA = "#e6eaeb"         # --inteli-cinza-claro: regiao acima do teto
FUNDO = "#ffffff"          # --inteli-branco

SERIES = ["abate_bovinos", "abate_suinos", "abate_frangos",
          "producao_ovos", "producao_leite"]
ALVO = "abate_frangos"
FEATURES = ["lag1", "lag12", "sen", "cos"]
N_TESTE = 24
SEMENTE = 42
BI = 1e9

plt.rcParams.update({
    "font.size": 18,
    "axes.edgecolor": REFERENCIA_1,
    "axes.labelcolor": TINTA,
    "text.color": TINTA,
    "xtick.color": TINTA,
    "ytick.color": TINTA,
    "figure.facecolor": FUNDO,
    "axes.facecolor": FUNDO,
})


def base_analitica():
    """Monta a base analitica da Aula 07: mesma definicao de
    global-constraints.md e de test_modelos_aula07.py, reimplementada aqui de
    proposito (ver docstring do modulo).

    Juncao interna das cinco series de dados/mensal/ por periodo, mais mes,
    dias do mes, sazonalidade (seno/cosseno), defasagens do alvo (1, 2, 3 e
    12 meses) e defasagem de 1 mes das outras quatro series. Linhas com
    qualquer valor ausente sao descartadas: sobram 339, de 1998-01 a 2026-03.
    """
    tabelas = {}
    for nome in SERIES:
        df = pd.read_csv(os.path.join(MENSAL, nome + ".csv"))
        tabelas[nome] = dict(zip(df["periodo"], df["valor"].astype(float)))
    periodos = sorted(set.intersection(*[set(t) for t in tabelas.values()]))

    col = {"periodo": periodos}
    for nome in SERIES:
        col[nome] = [tabelas[nome][p] for p in periodos]
    meses = [int(p.split("-")[1]) for p in periodos]
    col["mes"] = meses
    col["dias"] = [calendar.monthrange(int(p.split("-")[0]), m)[1]
                   for p, m in zip(periodos, meses)]
    col["sen"] = [np.sin(2 * np.pi * m / 12) for m in meses]
    col["cos"] = [np.cos(2 * np.pi * m / 12) for m in meses]

    def defasar(valores, k):
        return [None] * k + list(valores[:-k])

    for k in (1, 2, 3, 12):
        col["lag%d" % k] = defasar(col[ALVO], k)
    for nome in SERIES:
        if nome != ALVO:
            col[nome + "_lag1"] = defasar(col[nome], 1)

    manter = [i for i in range(len(periodos))
              if all(col[c][i] is not None for c in col)]
    base = {}
    for c in col:
        valores = [col[c][i] for i in manter]
        base[c] = valores if c == "periodo" else np.array(valores, dtype=float)
    return base


def _fatiar(base, alvo_em_razao):
    n = len(base["periodo"])
    corte = n - N_TESTE
    X = np.column_stack([base[f] for f in FEATURES])
    y = base[ALVO]
    alvo = y / base["lag12"] if alvo_em_razao else y
    return X[:corte], alvo[:corte], X[corte:], y[corte:], base["lag12"][corte:]


def ajustar_arvore(base, alvo_em_razao):
    """Ajusta a arvore de decisao (max_depth=3) e devolve real e previsto do
    teste, sempre reconvertidos a nivel."""
    Xtr, alvo_tr, Xte, yte, lag12te = _fatiar(base, alvo_em_razao)
    arvore = DecisionTreeRegressor(max_depth=3, random_state=SEMENTE)
    arvore.fit(Xtr, alvo_tr)
    previsto = arvore.predict(Xte)
    if alvo_em_razao:
        previsto = previsto * lag12te
    return arvore, yte, previsto


def mape(real, previsto):
    return float(np.mean(np.abs((real - previsto) / real)) * 100)


def teto_da_arvore(base, destino):
    """Figura 1: real contra previsao escalonada da arvore (alvo em nivel),
    com o teto da arvore e o maximo do treino como linhas de referencia."""
    n = len(base["periodo"])
    corte = n - N_TESTE
    periodos_teste = base["periodo"][corte:]
    arvore, yte, previsto = ajustar_arvore(base, alvo_em_razao=False)
    ytr = base[ALVO][:corte]

    teto = float(previsto.max())
    maximo_treino = float(ytr.max())
    idx_max_treino = int(np.argmax(ytr))
    periodo_max_treino = base["periodo"][idx_max_treino]
    acima_teto = int((yte > teto).sum())

    x = np.arange(N_TESTE)
    # 1600x900 a 150 dpi (interface da Task 3): figsize em polegadas e o
    # tamanho de pixel pedido dividido pelo dpi. Sem bbox_inches="tight" no
    # savefig, para o PNG final sair exatamente nesse tamanho.
    fig, eixo = plt.subplots(figsize=(1600 / 150, 900 / 150))

    eixo.plot(x, yte / BI, color=TINTA, linewidth=2.4, label="real", zorder=3)
    eixo.step(x, previsto / BI, where="mid", color=DESTAQUE, linewidth=2.4,
              label="previsão da árvore", zorder=3)

    # os rotulos das duas linhas de referencia vao para a legenda (rodape), em
    # vez de texto solto sobre o grafico: com o teto perto do minimo do eixo
    # y e o maximo do treino cruzado por varios picos do real, qualquer
    # posicao fixa de texto colide com a serie ou com os rotulos do eixo x em
    # algum mes. A legenda nao tem esse risco.
    eixo.axhline(teto / BI, color=REFERENCIA_1, linewidth=1.8, linestyle="--",
                 zorder=2, label="teto da árvore:\nmédia da folha mais alta")
    eixo.axhline(maximo_treino / BI, color=REFERENCIA_2, linewidth=1.8,
                 linestyle=":", zorder=2, label="máximo do treino,\n2023-03")
    eixo.fill_between(x, teto / BI, np.maximum(yte, teto) / BI,
                       color=SOMBRA, alpha=0.7, zorder=1)

    # a anotacao do sombreado vai no trecho de maior folga vertical acima do
    # teto, calculado a partir dos proprios dados (janela de 5 meses com a
    # maior folga minima), em vez de uma coordenada escolhida a olho.
    folga = (yte - teto) / BI
    janela = 2
    melhor_i, melhor_folga = janela, -1e9
    for i in range(janela, N_TESTE - janela):
        candidata = float(np.min(folga[i - janela:i + janela + 1]))
        if candidata > melhor_folga:
            melhor_folga, melhor_i = candidata, i
    y_anotacao = teto / BI + max(melhor_folga, 0.01) / 2
    eixo.annotate("23 dos 24 meses de teste\nestão aqui",
                  xy=(melhor_i, y_anotacao), fontsize=18, color=TINTA,
                  ha="center", va="center", zorder=4,
                  bbox={"facecolor": FUNDO, "edgecolor": "none", "pad": 4})

    rotulos_x = list(range(0, N_TESTE, 3))
    eixo.set_xticks(rotulos_x)
    eixo.set_xticklabels([periodos_teste[i] for i in rotulos_x], fontsize=18,
                          rotation=0)
    eixo.set_xlim(-0.5, N_TESTE - 0.5)
    eixo.set_ylabel("bilhões de kg\n(abate de frangos)", fontsize=18)
    eixo.spines[["top", "right"]].set_visible(False)
    eixo.tick_params(labelsize=18)
    eixo.legend(loc="upper center", bbox_to_anchor=(0.5, -0.22), ncol=2,
                fontsize=16, frameon=False, handletextpad=0.5,
                columnspacing=1.6, labelspacing=0.6)

    fig.subplots_adjust(left=0.15, right=0.98, top=0.96, bottom=0.37)
    fig.savefig(destino, dpi=150, facecolor=FUNDO)
    plt.close(fig)
    return {
        "teto": teto,
        "maximo_treino": maximo_treino,
        "periodo_max_treino": periodo_max_treino,
        "acima_teto": acima_teto,
        "yte": yte,
    }


def nivel_versus_razao(base, destino):
    """Figura 2: dois paineis lado a lado, mesmo eixo x e mesmo eixo y, alvo
    em nivel contra alvo em razao para a mesma arvore de decisao."""
    n = len(base["periodo"])
    corte = n - N_TESTE
    periodos_teste = base["periodo"][corte:]

    _, yte_nivel, p_nivel = ajustar_arvore(base, alvo_em_razao=False)
    _, yte_razao, p_razao = ajustar_arvore(base, alvo_em_razao=True)
    # yte_nivel e yte_razao sao o mesmo vetor de real: a razao so muda o alvo
    # de treino e a previsao, nao o real observado no teste.
    mape_nivel = mape(yte_nivel, p_nivel)
    mape_razao = mape(yte_razao, p_razao)

    x = np.arange(N_TESTE)
    # 1600x900 a 150 dpi, mesma conta da Figura 1.
    fig, (esq, dire) = plt.subplots(1, 2, figsize=(1600 / 150, 900 / 150),
                                     sharey=True)

    for eixo, previsto, titulo in (
        (esq, p_nivel, "alvo em nível, MAPE 7,66%"),
        (dire, p_razao, "alvo em razão, MAPE 3,86%"),
    ):
        eixo.plot(x, yte_nivel / BI, color=TINTA, linewidth=2.4, label="real",
                  zorder=2)
        eixo.step(x, previsto / BI, where="mid", color=DESTAQUE, linewidth=2.4,
                  label="previsão da árvore", zorder=2)
        eixo.set_title(titulo, fontsize=19, pad=10)
        eixo.spines[["top", "right"]].set_visible(False)
        eixo.tick_params(labelsize=18)
        rotulos_x = list(range(0, N_TESTE, 6))
        eixo.set_xticks(rotulos_x)
        eixo.set_xticklabels([periodos_teste[i] for i in rotulos_x], fontsize=18)
        eixo.set_xlim(-0.5, N_TESTE - 0.5)

    # os dois paineis TEM de compartilhar o limite de eixo y: sharey=True ja
    # garante isso, mas o limite fica reforcado aqui de forma explicita para
    # que a decisao nao dependa so do comportamento padrao do matplotlib.
    minimo = min((yte_nivel.min(), p_nivel.min(), p_razao.min())) / BI
    maximo = max((yte_nivel.max(), p_nivel.max(), p_razao.max())) / BI
    folga = (maximo - minimo) * 0.08
    esq.set_ylim(minimo - folga, maximo + folga)
    dire.set_ylim(minimo - folga, maximo + folga)

    esq.set_ylabel("bilhões de kg\n(abate de frangos)", fontsize=18)
    esq.legend(loc="upper left", fontsize=18, frameon=False)

    fig.tight_layout()
    fig.savefig(destino, dpi=150, facecolor=FUNDO)
    plt.close(fig)
    return mape_nivel, mape_razao


def main():
    base = base_analitica()
    saida = os.path.join(RAIZ, "assets", "img")

    resultado1 = teto_da_arvore(base, os.path.join(saida, "aula07-teto-da-arvore.png"))
    mape_nivel, mape_razao = nivel_versus_razao(
        base, os.path.join(saida, "aula07-nivel-versus-razao.png"))

    n = len(base["periodo"])
    corte = n - N_TESTE
    periodos_teste = base["periodo"][corte:]
    yte = resultado1["yte"]
    idx_max_teste = int(np.argmax(yte))

    print("base analítica: %d linhas, %s a %s" % (n, base["periodo"][0], base["periodo"][-1]))
    print("teste: %d meses, de %s a %s" % (N_TESTE, periodos_teste[0], periodos_teste[-1]))
    print("teto da árvore: %d" % round(resultado1["teto"]))
    print("máximo do alvo no treino: %d, em %s"
          % (round(resultado1["maximo_treino"]), resultado1["periodo_max_treino"]))
    print("máximo real no teste: %d, em %s"
          % (round(float(yte.max())), periodos_teste[idx_max_teste]))
    print("meses de teste acima do teto: %d de %d" % (resultado1["acima_teto"], N_TESTE))
    print("MAPE da árvore com alvo em nível: %.2f%%" % mape_nivel)
    print("MAPE da árvore com alvo em razão: %.2f%%" % mape_razao)

    for nome in ("aula07-teto-da-arvore.png", "aula07-nivel-versus-razao.png"):
        caminho = os.path.join(saida, nome)
        tamanho = os.path.getsize(caminho)
        print("%s: %d bytes" % (nome, tamanho))

    print("figuras gravadas em assets/img/")


if __name__ == "__main__":
    main()

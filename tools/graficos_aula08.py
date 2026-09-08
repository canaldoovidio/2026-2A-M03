"""Gera as três figuras da Aula 08 a partir dos CSVs versionados em dados/.

As três sustentam a tese única da aula: o critério interno da técnica não
supervisionada não é o critério do case.

1. `aula08-escolha-de-k.png`. Três painéis sobre a base de participação de cada
   trimestre no total do próprio ano, a mesma da Aula 06 (116 linhas, anos
   completos), um por critério e com o K que cada critério escolhe em destaque.
   A inércia, que é o Elbow Plot, tem o joelho em K=3 (queda de 25,1% de K=2
   para K=3 e de 14,3% de K=3 para K=4). A silhueta é máxima em K=2 (0,3785). A
   concordância com o trimestre do calendário só chega a 98,3% em K=4. Os três
   painéis apontam três valores diferentes, e os dois primeiros nunca apontam o
   terceiro.

2. `aula08-plano-pc2-pc3.png`. Os 315 meses de treino projetados no plano dos
   componentes 2 e 3 do PCA das 11 features. Nenhuma coluna da matriz é o número
   do mês, e os doze meses aparecem em ciclo: o centroide de cada mês está
   ligado ao do mês seguinte, e fevereiro fica isolado à esquerda, porque é o
   mês com menos dias. Agrupar esse plano em 12 grupos recupera o mês em 91,7%
   das linhas.

3. `aula08-corte-custa-mape.png`. MAPE de teste da regressão sobre os k
   primeiros componentes, de k=1 a k=11, contra a variância acumulada retida em
   cada k. A variância chega a 96,07% com quatro componentes, e o MAPE nesse
   ponto é 4,94%, acima dos 3,71% da baseline de coeficiente fixo da LDC. Só
   k=10 devolve os 3,32% do modelo do fecho da Aula 07.

Decisões de forma, herdadas de `tools/graficos_aula06.py` e
`tools/graficos_aula07.py`:

- roxo #2e2640 como tinta, coral #ff4545 como destaque, verde #89cea5 e cinza
  escuro #b2b6bf como referências, cinza médio #caced6 na nuvem de pontos e
  cinza claro #e6eaeb no sombreamento. As sete cores vêm dos tokens de
  `assets/css/inteli-brand.css`, com a origem comentada abaixo.
- nenhum valor interpolado ou inventado: as figuras plotam os CSVs de `dados/` e
  de `dados/mensal/` e as saídas dos modelos ajustados sobre eles, com a mesma
  lógica de junção, defasagem, participação no ano e corte temporal de
  `tools/tests/test_pca_aula08.py`, reimplementada aqui de propósito em vez de
  importada: se as duas implementações divergirem, o acervo descobre. O notebook
  da aula reimplementa a mesma definição pela mesma razão, porque precisa rodar
  sozinho no Colab.
- escalador e PCA são ajustados só nos 315 meses de treino, nunca na base
  inteira, conforme a `ADR-011`.
- 1600x900 a 150 dpi e corpo 18 em todo texto, que é o piso de legibilidade que
  o tema fixa para slide.

Uso: python3 tools/graficos_aula08.py   (requer matplotlib, pandas, numpy,
scikit-learn, listados em requirements-ci.txt)
"""
import calendar
import collections
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.linear_model import LinearRegression
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS = os.path.join(RAIZ, "dados")
MENSAL = os.path.join(DADOS, "mensal")

# cores lidas de assets/css/inteli-brand.css (paleta da Graduacao, p.66/p.68)
TINTA = "#2e2640"          # --inteli-roxo
DESTAQUE = "#ff4545"       # --inteli-coral
REFERENCIA_1 = "#b2b6bf"   # --inteli-cinza-escuro
REFERENCIA_2 = "#89cea5"   # --inteli-verde
NUVEM = "#caced6"          # --inteli-cinza-medio
SOMBRA = "#e6eaeb"         # --inteli-cinza-claro
FUNDO = "#ffffff"          # --inteli-branco

SERIES = ["abate_bovinos", "abate_suinos", "abate_frangos",
          "producao_ovos", "producao_leite"]
ALVO = "abate_frangos"
FEATURES = (["lag1", "lag2", "lag3", "lag12", "sen", "cos", "dias"]
            + [s + "_lag1" for s in SERIES if s != ALVO])
N_TESTE = 24
SEMENTE = 42
FAIXA_K = list(range(2, 9))

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


# --------------------------------------------------------------------------
# As duas bases


def base_trimestral():
    """Junção interna das cinco séries trimestrais, a base da Aula 06."""
    tabelas = {}
    for nome in SERIES:
        df = pd.read_csv(os.path.join(DADOS, nome + ".csv"))
        tabelas[nome] = dict(zip(df["periodo"], df["valor"].astype(float)))
    periodos = sorted(set.intersection(*[set(t) for t in tabelas.values()]))
    return {
        "periodos": periodos,
        "X": np.array([[tabelas[s][p] for s in SERIES] for p in periodos]),
        "anos": np.array([int(p[:4]) for p in periodos]),
        "tris": np.array([int(p[-1]) for p in periodos]),
    }


def participacao_no_ano(base):
    """Cada valor vira a fração que representa no total do próprio ano.

    Só entram anos com os quatro trimestres medidos, a mesma regra da Aula 06:
    2026 tem apenas o T1, e incluir ano incompleto faria o único trimestre dele
    valer 100% do ano. Sobram 116 linhas.
    """
    completos = {a for a in set(base["anos"].tolist())
                 if (base["anos"] == a).sum() == 4}
    mascara = np.array([a in completos for a in base["anos"]])
    X, anos = base["X"][mascara], base["anos"][mascara]
    saida = np.empty_like(X)
    for a in completos:
        linhas = anos == a
        saida[linhas] = X[linhas] / X[linhas].sum(axis=0)
    return saida, base["tris"][mascara]


def base_analitica():
    """Base analítica mensal da Aula 07: 339 linhas, de 1998-01 a 2026-03.

    Mesma definição de `tools/graficos_aula07.py` e de
    `tools/tests/test_pca_aula08.py`, reimplementada aqui de propósito (ver
    docstring do módulo).
    """
    tabelas = {}
    for nome in SERIES:
        df = pd.read_csv(os.path.join(MENSAL, nome + ".csv"))
        df = df[df["valor"].notna()]
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
    return {c: ([col[c][i] for i in manter] if c == "periodo"
                else np.array([col[c][i] for i in manter], dtype=float))
            for c in col}


def pca_do_treino(base):
    """Padroniza e ajusta o PCA só nos 315 meses de treino (ADR-011)."""
    corte = len(base["periodo"]) - N_TESTE
    X = np.column_stack([base[f] for f in FEATURES])
    escalador = StandardScaler().fit(X[:corte])
    Ztr, Zte = escalador.transform(X[:corte]), escalador.transform(X[corte:])
    return {
        "corte": corte,
        "Ztr": Ztr,
        "Zte": Zte,
        "pca": PCA().fit(Ztr),
        "razao_tr": (base[ALVO] / base["lag12"])[:corte],
        "yte": base[ALVO][corte:],
        "lag12te": base["lag12"][corte:],
        "meses_tr": base["mes"][:corte].astype(int),
    }


def _concordancia(rotulos, verdade):
    acertos = 0
    for c in set(rotulos.tolist()):
        do_cluster = verdade[rotulos == c]
        acertos += collections.Counter(do_cluster.tolist()).most_common(1)[0][1]
    return acertos / len(verdade)


def _mape(real, previsto):
    return float(np.mean(np.abs((real - previsto) / real)) * 100)


def _num(formato, *valores):
    """Formata número em pt-BR: vírgula como separador decimal."""
    return (formato % valores).replace(".", ",")


# --------------------------------------------------------------------------
# Figura 1


def escolha_de_k(destino):
    """Elbow Plot e silhueta contra a concordância com o calendário."""
    X, tris = participacao_no_ano(base_trimestral())
    padronizada = StandardScaler().fit_transform(X)

    inercia, silhueta, concordancia = {}, {}, {}
    for k in FAIXA_K:
        modelo = KMeans(n_clusters=k, n_init=50, random_state=SEMENTE).fit(padronizada)
        inercia[k] = modelo.inertia_
        silhueta[k] = silhouette_score(padronizada, modelo.labels_)
        concordancia[k] = _concordancia(modelo.labels_, tris)

    fig, eixos = plt.subplots(1, 3, figsize=(1600 / 150, 900 / 150))
    ks = FAIXA_K

    # um painel por critério, e não dois eixos y no mesmo painel: a silhueta e a
    # concordância caem em faixas numéricas parecidas (0,26 a 0,38 contra 25% a
    # 98%), e sobrepor as duas escalas fazia a linha do acaso passar rente à
    # curva de silhueta, sugerindo uma relação que não existe.
    # o deslocamento do rótulo K=n é por painel: em K=2 o rótulo acima do ponto
    # cairia sobre o número do eixo y, porque o ponto está no primeiro x.
    paineis = [
        (eixos[0], "inércia (Elbow Plot)", [inercia[k] for k in ks], 3, "o", (0, 26)),
        (eixos[1], "silhueta", [silhueta[k] for k in ks], 2, "o", (22, 12)),
        (eixos[2], "concordância com\no trimestre (%)",
         [100 * concordancia[k] for k in ks], 4, "s", (0, 26)),
    ]
    for eixo, rotulo, valores, destacado, marcador, deslocamento in paineis:
        eixo.plot(ks, valores, color=TINTA, linewidth=2.4, marker=marcador,
                  markersize=9, zorder=3)
        i = ks.index(destacado)
        eixo.plot([destacado], [valores[i]], color=DESTAQUE, marker=marcador,
                  markersize=18, zorder=4)
        eixo.annotate("K=%d" % destacado, xy=(destacado, valores[i]),
                      xytext=deslocamento, textcoords="offset points",
                      fontsize=18, color=DESTAQUE, ha="center", va="bottom",
                      zorder=5)
        eixo.set_xlabel("K", fontsize=18)
        eixo.set_ylabel(rotulo, fontsize=18)
        eixo.set_xticks(ks)
        eixo.tick_params(labelsize=18)
        eixo.spines[["top", "right"]].set_visible(False)

    eixos[0].set_ylim(120, 380)
    eixos[1].set_ylim(0.20, 0.46)
    eixos[1].set_yticks([0.25, 0.30, 0.35, 0.40])
    eixos[1].set_yticklabels([_num("%.2f", v) for v in (0.25, 0.30, 0.35, 0.40)])
    eixos[2].set_ylim(0, 118)
    eixos[2].set_yticks([25, 50, 75, 100])
    eixos[2].axhline(25, color=REFERENCIA_1, linewidth=1.6, linestyle=":", zorder=2)
    eixos[2].annotate("acaso: 25%", xy=(7.8, 25), xytext=(0, 8),
                      textcoords="offset points", fontsize=16,
                      color=REFERENCIA_1, ha="right", va="bottom", zorder=3)

    fig.subplots_adjust(left=0.115, right=0.99, top=0.93, bottom=0.16, wspace=0.52)
    fig.savefig(destino, dpi=150, facecolor=FUNDO)
    plt.close(fig)
    return {"inercia": inercia, "silhueta": silhueta, "concordancia": concordancia}


# --------------------------------------------------------------------------
# Figura 2


def plano_pc2_pc3(t, destino):
    """Os 315 meses de treino no plano dos componentes 2 e 3."""
    pca = t["pca"]
    plano = pca.transform(t["Ztr"])[:, 1:3]
    meses = t["meses_tr"]
    variancia = pca.explained_variance_ratio_

    rotulos = KMeans(n_clusters=12, n_init=50, random_state=SEMENTE).fit(plano).labels_
    acerto = _concordancia(rotulos, meses)

    fig, eixo = plt.subplots(figsize=(1600 / 150, 900 / 150))
    eixo.scatter(plano[:, 0], plano[:, 1], color=NUVEM, s=26, zorder=2)

    centroides = np.array([plano[meses == m].mean(axis=0) for m in range(1, 13)])
    ciclo = np.vstack([centroides, centroides[:1]])
    eixo.plot(ciclo[:, 0], ciclo[:, 1], color=REFERENCIA_1, linewidth=1.8,
              linestyle="--", zorder=3)
    for m in range(1, 13):
        x, y = centroides[m - 1]
        cor = DESTAQUE if m == 2 else TINTA
        eixo.scatter([x], [y], color=FUNDO, edgecolors=cor, s=560, linewidths=2.4,
                     zorder=4)
        eixo.annotate("%02d" % m, xy=(x, y), fontsize=18, color=cor, ha="center",
                      va="center", zorder=5)

    eixo.annotate("fevereiro, o mês\ncom menos dias",
                  xy=tuple(centroides[1]), xytext=(24, -70),
                  textcoords="offset points", fontsize=18, color=DESTAQUE,
                  ha="left", va="top", zorder=5,
                  arrowprops={"arrowstyle": "-", "color": DESTAQUE})
    eixo.set_xlabel(_num("componente 2 (%.2f%% da variância)", 100 * variancia[1]),
                    fontsize=18)
    eixo.set_ylabel(_num("componente 3\n(%.2f%% da variância)", 100 * variancia[2]),
                    fontsize=18)
    eixo.tick_params(labelsize=18)
    eixo.spines[["top", "right"]].set_visible(False)
    eixo.set_title(_num("Doze grupos neste plano recuperam o mês em %.1f%% dos "
                        "315 meses", 100 * acerto),
                   fontsize=18, color=TINTA, pad=14)

    fig.subplots_adjust(left=0.14, right=0.98, top=0.90, bottom=0.14)
    fig.savefig(destino, dpi=150, facecolor=FUNDO)
    plt.close(fig)
    return {"acerto": acerto,
            "silhueta_do_mes": float(silhouette_score(plano, meses))}


# --------------------------------------------------------------------------
# Figura 3


def corte_custa_mape(t, base, destino):
    """MAPE por número de componentes, contra a variância acumulada retida."""
    corte = t["corte"]
    fator = float(np.mean(base[ALVO][:corte] / base["lag12"][:corte]))
    baseline = _mape(t["yte"], base["lag12"][corte:] * fator)

    ks = list(range(1, len(FEATURES) + 1))
    mape, retida = {}, {}
    for k in ks:
        pca = PCA(n_components=k).fit(t["Ztr"])
        modelo = LinearRegression().fit(pca.transform(t["Ztr"]), t["razao_tr"])
        previsto = modelo.predict(pca.transform(t["Zte"])) * t["lag12te"]
        mape[k] = _mape(t["yte"], previsto)
        retida[k] = 100 * float(pca.explained_variance_ratio_.sum())

    fig, eixo = plt.subplots(figsize=(1600 / 150, 900 / 150))

    eixo.fill_between(ks, baseline, [max(mape[k], baseline) for k in ks],
                      color=SOMBRA, alpha=0.8, zorder=1)
    eixo.plot(ks, [mape[k] for k in ks], color=TINTA, linewidth=2.4, marker="o",
              markersize=9, label="MAPE de teste (eixo esquerdo)", zorder=4)
    eixo.axhline(baseline, color=REFERENCIA_2, linewidth=1.8, linestyle="--",
                 zorder=3, label=_num("baseline da LDC: %.2f%%", baseline))
    eixo.axhline(mape[len(FEATURES)], color=REFERENCIA_1, linewidth=1.8,
                 linestyle=":", zorder=3,
                 label=_num("11 features: %.2f%%", mape[len(FEATURES)]))
    eixo.plot([4], [mape[4]], color=DESTAQUE, marker="o", markersize=16, zorder=5)
    # três linhas curtas, e não duas longas: com duas, a segunda linha chegava
    # ao pico de MAPE em k=9 e cruzava a série.
    eixo.annotate(_num("quatro componentes retêm\n%.2f%% da variância e\ncustam "
                       "%.2f%% de MAPE", retida[4], mape[4]),
                  xy=(4, mape[4]), xytext=(26, 58), textcoords="offset points",
                  fontsize=18, color=DESTAQUE, ha="left", va="bottom", zorder=6,
                  bbox={"facecolor": FUNDO, "edgecolor": "none", "pad": 3},
                  arrowprops={"arrowstyle": "-", "color": DESTAQUE})
    eixo.set_xlabel("componentes usados na regressão", fontsize=18)
    eixo.set_ylabel("MAPE (%)", fontsize=18)
    eixo.set_xticks(ks)
    eixo.set_ylim(2.8, 7.4)
    eixo.set_yticks([3, 4, 5, 6, 7])
    eixo.tick_params(labelsize=18)
    eixo.spines[["top"]].set_visible(False)

    outro = eixo.twinx()
    outro.plot(ks, [retida[k] for k in ks], color=DESTAQUE, linewidth=2.4,
               marker="^", markersize=9, linestyle="-.",
               label="variância retida (eixo direito)", zorder=4)
    outro.set_ylim(60, 102)
    outro.set_ylabel("variância retida (%)", fontsize=18, color=TINTA)
    outro.tick_params(labelsize=18, colors=TINTA)
    outro.spines[["top"]].set_visible(False)

    linhas = eixo.get_lines()[:3] + outro.get_lines()[:1]
    eixo.legend(linhas, [l.get_label() for l in linhas], loc="upper center",
                bbox_to_anchor=(0.5, -0.18), ncol=2, fontsize=16, frameon=False,
                labelspacing=0.6, columnspacing=2.0, handletextpad=0.5,
                handlelength=1.8)

    fig.subplots_adjust(left=0.10, right=0.90, top=0.96, bottom=0.32)
    fig.savefig(destino, dpi=150, facecolor=FUNDO)
    plt.close(fig)
    return {"mape": mape, "retida": retida, "baseline": baseline}


def main():
    saida = os.path.join(RAIZ, "assets", "img")
    base = base_analitica()
    t = pca_do_treino(base)

    k = escolha_de_k(os.path.join(saida, "aula08-escolha-de-k.png"))
    print("Figura 1: aula08-escolha-de-k.png")
    print("  inércia   K=2 %.1f  K=3 %.1f  K=4 %.1f"
          % (k["inercia"][2], k["inercia"][3], k["inercia"][4]))
    print("  silhueta  K=2 %.4f  K=3 %.4f  K=4 %.4f"
          % (k["silhueta"][2], k["silhueta"][3], k["silhueta"][4]))
    print("  calendário K=2 %.1f%%  K=3 %.1f%%  K=4 %.1f%%"
          % tuple(100 * k["concordancia"][i] for i in (2, 3, 4)))

    p = plano_pc2_pc3(t, os.path.join(saida, "aula08-plano-pc2-pc3.png"))
    print("Figura 2: aula08-plano-pc2-pc3.png")
    print("  12 grupos recuperam o mês em %.1f%% das linhas" % (100 * p["acerto"]))
    print("  silhueta dos rótulos verdadeiros de mês: %.4f" % p["silhueta_do_mes"])

    c = corte_custa_mape(t, base, os.path.join(saida, "aula08-corte-custa-mape.png"))
    print("Figura 3: aula08-corte-custa-mape.png")
    print("  baseline da LDC: %.2f%%" % c["baseline"])
    for i in (1, 2, 4, 9, 10, 11):
        print("  k=%-2d MAPE %.2f%%  variância retida %.2f%%"
              % (i, c["mape"][i], c["retida"][i]))


if __name__ == "__main__":
    main()

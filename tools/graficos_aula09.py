"""Gera as três figuras da Aula 09 a partir dos CSVs de dados/mensal/.

1. `aula09-vazamento-por-modelo.png`. Dois painéis. À esquerda, o MAPE de teste
   de quatro modelos com corte por data e com sorteio aleatório (média de dez
   sementes): KNN, árvore e random forest melhoram artificialmente, e a
   regressão linear sobre a razão piora. À direita, o alvo médio do conjunto de
   teste em cada corte, que é a razão pela qual o RMSE não pode ser comparado
   entre os dois: 1,18 bilhão de quilogramas nos 24 últimos meses contra cerca
   de 0,76 bilhão nos 24 meses sorteados.

2. `aula09-baseline-majoritaria.png`. Acurácia da baseline que prevê sempre a
   classe majoritária contra a dos cinco classificadores, no alvo binário do
   case. Nenhum supera a baseline de 83,3%, e o Naive Bayes gaussiano cai para
   16,7%.

3. `aula09-imputacao.png`. Erro médio de cinco estratégias de imputação sobre
   16 meses mascarados do treino, medido contra o valor real que foi escondido:
   média 34,53%, mediana 34,38%, último valor 7,60%, interpolação linear 7,27% e
   mesmo mês do ano anterior corrigido pelo fator médio 4,44%.

Decisões de forma, herdadas de `tools/graficos_aula07.py` e
`tools/graficos_aula08.py`:

- roxo #2e2640 como tinta, coral #ff4545 como destaque, verde #89cea5 e cinza
  escuro #b2b6bf como referências, cinza médio #caced6 e cinza claro #e6eaeb nos
  fundos. As cores vêm dos tokens de `assets/css/inteli-brand.css`.
- nenhum valor interpolado ou inventado: tudo é medido sobre `dados/mensal/`,
  com a mesma lógica de junção, defasagem, corte temporal, mascaramento e alvo
  binário de `tools/tests/test_problemas_aula09.py`, reimplementada aqui de
  propósito: se as duas implementações divergirem, o acervo descobre.
- 1600x900 a 150 dpi e corpo 18 em todo texto, o piso de legibilidade do tema.
- separador decimal é vírgula, como em `tools/graficos_aula04.py`.

Uso: python3 tools/graficos_aula09.py   (requer matplotlib, pandas, numpy,
scikit-learn, listados em requirements-ci.txt)
"""
import calendar
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MENSAL = os.path.join(RAIZ, "dados", "mensal")

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
SEMENTES_SORTEIO = 10
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


def _num(formato, *valores):
    """Formata número em pt-BR: vírgula como separador decimal."""
    return (formato % valores).replace(".", ",")


def base_analitica():
    """Base analítica mensal da Aula 07: 339 linhas, de 1998-01 a 2026-03."""
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
    saida = {c: ([col[c][i] for i in manter] if c == "periodo"
                 else np.array([col[c][i] for i in manter], dtype=float))
             for c in col}
    saida["n"] = len(saida["periodo"])
    saida["corte"] = saida["n"] - N_TESTE
    saida["X"] = np.column_stack([saida[f] for f in FEATURES])
    return saida


def _mape(real, previsto):
    return float(np.mean(np.abs((real - previsto) / real)) * 100)


def _indices(base, aleatorio, semente):
    if not aleatorio:
        return np.arange(base["corte"]), np.arange(base["corte"], base["n"])
    return train_test_split(np.arange(base["n"]),
                            test_size=N_TESTE / base["n"], random_state=semente)


def _avaliar(base, fabrica, aleatorio, em_razao):
    y = base[ALVO]
    alvo = y / base["lag12"] if em_razao else y
    saida = []
    for semente in range(SEMENTES_SORTEIO if aleatorio else 1):
        itr, ite = _indices(base, aleatorio, semente)
        escalador = StandardScaler().fit(base["X"][itr])
        modelo = fabrica().fit(escalador.transform(base["X"][itr]), alvo[itr])
        previsto = modelo.predict(escalador.transform(base["X"][ite]))
        if em_razao:
            previsto = previsto * base["lag12"][ite]
        saida.append(_mape(y[ite], previsto))
    return float(np.mean(saida))


# --------------------------------------------------------------------------
# Figura 1


def vazamento_por_modelo(base, destino):
    modelos = [
        ("KNN\nk=5", lambda: KNeighborsRegressor(n_neighbors=5), False),
        ("árvore\nd=3", lambda: DecisionTreeRegressor(max_depth=3,
                                                      random_state=SEMENTE), False),
        ("random\nforest", lambda: RandomForestRegressor(n_estimators=300,
                                                         random_state=SEMENTE), False),
        ("regressão\nlinear", lambda: LinearRegression(), True),
    ]
    dados = [(rotulo, _avaliar(base, fab, False, razao), _avaliar(base, fab, True, razao))
             for rotulo, fab, razao in modelos]

    fig, (esq, dir_) = plt.subplots(1, 2, figsize=(1600 / 150, 900 / 150),
                                    gridspec_kw={"width_ratios": [2.4, 1]})

    x = np.arange(len(dados))
    largura = 0.36
    esq.bar(x - largura / 2, [d[1] for d in dados], largura, color=TINTA,
            label="corte por data", zorder=3)
    esq.bar(x + largura / 2, [d[2] for d in dados], largura, color=DESTAQUE,
            label="sorteio aleatório", zorder=3)
    for i, (_, honesto, sorteado) in enumerate(dados):
        esq.annotate(_num("%.2f", honesto), xy=(i - largura / 2, honesto),
                     xytext=(-2, 6), textcoords="offset points", fontsize=15,
                     color=TINTA, ha="center", va="bottom")
        esq.annotate(_num("%.2f", sorteado), xy=(i + largura / 2, sorteado),
                     xytext=(2, 6), textcoords="offset points", fontsize=15,
                     color=DESTAQUE, ha="center", va="bottom")
    esq.annotate("o único que\nnão melhora", xy=(len(dados) - 1 + largura / 2,
                                                  dados[-1][2]),
                 xytext=(0, 74), textcoords="offset points", fontsize=18,
                 color=TINTA, ha="center", va="bottom",
                 bbox={"facecolor": FUNDO, "edgecolor": "none", "pad": 2},
                 arrowprops={"arrowstyle": "-", "color": TINTA})
    esq.set_xticks(x)
    esq.set_xticklabels([d[0] for d in dados], fontsize=18)
    esq.set_xlabel("alvo em nível nos três primeiros, em razão no último",
                   fontsize=17)
    esq.set_ylabel("MAPE de teste (%)", fontsize=18)
    esq.set_ylim(0, 11.4)
    esq.tick_params(labelsize=18)
    esq.spines[["top", "right"]].set_visible(False)
    esq.legend(loc="upper center", bbox_to_anchor=(0.5, -0.25), ncol=2,
               fontsize=17, frameon=False, columnspacing=2.0)

    y = base[ALVO]
    media_temporal = float(y[base["corte"]:].mean())
    medias = []
    for semente in range(SEMENTES_SORTEIO):
        _, ite = _indices(base, True, semente)
        medias.append(float(y[ite].mean()))
    media_sorteada = float(np.mean(medias))

    dir_.bar([0], [media_temporal / BI], 0.55, color=TINTA, zorder=3)
    dir_.bar([1], [media_sorteada / BI], 0.55, color=DESTAQUE, zorder=3)
    for i, valor in enumerate((media_temporal, media_sorteada)):
        dir_.annotate(_num("%.2f", valor / BI), xy=(i, valor / BI),
                      xytext=(0, 6), textcoords="offset points", fontsize=17,
                      color=TINTA if i == 0 else DESTAQUE, ha="center", va="bottom")
    dir_.set_xticks([0, 1])
    dir_.set_xticklabels(["24 últimos\nmeses", "24 meses\nsorteados"], fontsize=17)
    dir_.set_ylabel("alvo médio do teste\n(bilhões de kg)", fontsize=18)
    dir_.set_ylim(0, 1.55)
    dir_.tick_params(labelsize=18)
    dir_.spines[["top", "right"]].set_visible(False)
    dir_.set_title("escala do teste", fontsize=18, color=TINTA, pad=12)
    dir_.set_xlabel("o RMSE não é\ncomparável", fontsize=17)

    fig.subplots_adjust(left=0.09, right=0.98, top=0.92, bottom=0.30, wspace=0.42)
    fig.savefig(destino, dpi=150, facecolor=FUNDO)
    plt.close(fig)
    return {"modelos": dados, "media_temporal": media_temporal,
            "media_sorteada": media_sorteada}


# --------------------------------------------------------------------------
# Figura 2


def baseline_majoritaria(base, destino):
    corte = base["corte"]
    alvo = (base[ALVO] > base["lag12"]).astype(int)
    escalador = StandardScaler().fit(base["X"][:corte])
    Ztr, Zte = escalador.transform(base["X"][:corte]), escalador.transform(base["X"][corte:])
    atr, ate = alvo[:corte], alvo[corte:]

    maioria = np.full(len(ate), int(atr.mean() > 0.5))
    linhas = [("prever sempre\n\"cresce\"", 100 * accuracy_score(ate, maioria), True)]
    modelos = [
        ("SVM RBF", SVC(kernel="rbf", random_state=SEMENTE)),
        ("árvore de entropia", DecisionTreeClassifier(criterion="entropy", max_depth=3,
                                                      random_state=SEMENTE)),
        ("SVM linear", SVC(kernel="linear", random_state=SEMENTE)),
        ("regressão logística", LogisticRegression(max_iter=2000, random_state=SEMENTE)),
        ("Naive Bayes", GaussianNB()),
    ]
    for rotulo, modelo in modelos:
        previsto = modelo.fit(Ztr, atr).predict(Zte)
        linhas.append((rotulo, 100 * accuracy_score(ate, previsto), False))

    fig, eixo = plt.subplots(figsize=(1600 / 150, 900 / 150))
    posicoes = np.arange(len(linhas))[::-1]
    for pos, (rotulo, valor, e_baseline) in zip(posicoes, linhas):
        eixo.barh([pos], [valor], 0.6, color=DESTAQUE if e_baseline else TINTA, zorder=3)
        eixo.annotate(_num("%.1f%%", valor), xy=(valor, pos), xytext=(8, 0),
                      textcoords="offset points", fontsize=18,
                      color=DESTAQUE if e_baseline else TINTA, ha="left", va="center")
    eixo.axvline(linhas[0][1], color=DESTAQUE, linewidth=1.8, linestyle="--", zorder=2)
    eixo.set_yticks(posicoes)
    eixo.set_yticklabels([l[0] for l in linhas], fontsize=18)
    eixo.set_xlabel("acurácia nos 24 meses de teste (%)", fontsize=18)
    eixo.set_xlim(0, 100)
    eixo.tick_params(labelsize=18)
    eixo.spines[["top", "right"]].set_visible(False)

    fig.subplots_adjust(left=0.28, right=0.94, top=0.96, bottom=0.14)
    fig.savefig(destino, dpi=150, facecolor=FUNDO)
    plt.close(fig)
    return {"linhas": linhas}


# --------------------------------------------------------------------------
# Figura 3


def imputacao(base, destino):
    corte = base["corte"]
    alvo = base[ALVO][:corte].copy()
    gerador = np.random.default_rng(SEMENTE)
    quantos = int(round(0.05 * corte))
    indices = np.sort(gerador.choice(np.arange(1, corte - 1), size=quantos, replace=False))
    verdade = alvo[indices]

    com_furo = alvo.copy()
    com_furo[indices] = np.nan
    ultimo = com_furo.copy()
    for i in range(1, len(ultimo)):
        if np.isnan(ultimo[i]):
            ultimo[i] = ultimo[i - 1]
    validos = ~np.isnan(com_furo)
    fator = float(np.nanmean(com_furo[12:] / alvo[:corte - 12]))

    estrategias = [
        ("média da série", np.full(quantos, np.nanmean(com_furo))),
        ("mediana da série", np.full(quantos, np.nanmedian(com_furo))),
        ("último valor medido", ultimo[indices]),
        ("interpolação linear", np.interp(indices, np.arange(corte)[validos],
                                          com_furo[validos])),
        ("mesmo mês do ano\nanterior, com fator", np.array([alvo[i - 12] * fator
                                                            for i in indices])),
    ]
    erros = [(rotulo, 100 * float(np.mean(np.abs((v - verdade) / verdade))))
             for rotulo, v in estrategias]

    fig, eixo = plt.subplots(figsize=(1600 / 150, 900 / 150))
    posicoes = np.arange(len(erros))[::-1]
    melhor = min(e[1] for e in erros)
    for pos, (rotulo, valor) in zip(posicoes, erros):
        cor = DESTAQUE if valor == melhor else TINTA
        eixo.barh([pos], [valor], 0.6, color=cor, zorder=3)
        eixo.annotate(_num("%.2f%%", valor), xy=(valor, pos), xytext=(8, 0),
                      textcoords="offset points", fontsize=18, color=cor,
                      ha="left", va="center")
    eixo.set_yticks(posicoes)
    eixo.set_yticklabels([e[0] for e in erros], fontsize=18)
    eixo.set_xlabel("erro médio nos %d meses mascarados (%%)" % quantos, fontsize=18)
    eixo.set_xlim(0, 42)
    eixo.tick_params(labelsize=18)
    eixo.spines[["top", "right"]].set_visible(False)

    fig.subplots_adjust(left=0.27, right=0.95, top=0.96, bottom=0.14)
    fig.savefig(destino, dpi=150, facecolor=FUNDO)
    plt.close(fig)
    return {"erros": erros, "mascarados": quantos, "fator": fator}


def main():
    saida = os.path.join(RAIZ, "assets", "img")
    base = base_analitica()

    v = vazamento_por_modelo(base, os.path.join(saida, "aula09-vazamento-por-modelo.png"))
    print("Figura 1: aula09-vazamento-por-modelo.png")
    for rotulo, honesto, sorteado in v["modelos"]:
        print("  %-30s data %.2f%%  sorteio %.2f%%"
              % (rotulo.replace("\n", " "), honesto, sorteado))
    print("  alvo médio do teste: temporal %.0f  sorteado %.0f"
          % (v["media_temporal"], v["media_sorteada"]))

    b = baseline_majoritaria(base, os.path.join(saida, "aula09-baseline-majoritaria.png"))
    print("Figura 2: aula09-baseline-majoritaria.png")
    for rotulo, valor, _ in b["linhas"]:
        print("  %-30s %.1f%%" % (rotulo.replace("\n", " "), valor))

    i = imputacao(base, os.path.join(saida, "aula09-imputacao.png"))
    print("Figura 3: aula09-imputacao.png (%d meses mascarados, fator %.5f)"
          % (i["mascarados"], i["fator"]))
    for rotulo, valor in i["erros"]:
        print("  %-34s %.2f%%" % (rotulo.replace("\n", " "), valor))


if __name__ == "__main__":
    main()

"""Mede os números da revisão da Aula 13 e gera as quatro figuras do deck.

A Aula 13 é a revisão, em sala invertida, dos conteúdos de computação da Prova
de 02/10 (`docs/adrs/ADR-016`). Ela não traz modelo novo: todo exercício ancora
no case da LDC, com números medidos aqui sobre os CSVs versionados, nunca
digitados de memória. `tools/tests/test_revisao_aula13.py` reimplementa as
mesmas contas de forma independente e trava cada número que o deck e o
material afirmam.

Duas bases, e cada número declara de qual veio:

- **mensal** (`dados/mensal/`): a base analítica das Aulas 07 a 12, 339 linhas
  de 1998-01 a 2026-03, treino de 315 meses e teste de 24 (2024-04 a 2026-03),
  onze features. É de onde saem vazamento, reapresentação, métricas de
  regressão e a matriz de confusão do alvo binário da Aula 09.
- **trimestral** (`dados/*.csv`): as cinco séries em `AAAA-TN`. É de onde sai a
  regressão linear simples do bloco 2 (abate de frangos sobre o abate de
  suínos do trimestre anterior), porque ela precisa de poucas observações para
  mostrar a fragilidade de teste pequeno.

As quatro figuras:

1. `aula13-dispersao.png`: os 116 trimestres, frangos contra suínos do
   trimestre anterior, com a reta ajustada no treino sorteado.
2. `aula13-cronologica.png`: a mesma reta ajustada até 2020-T1 e aplicada aos
   24 trimestres seguintes, contra o real. É o que o sorteio escondia.
3. `aula13-sementes.png`: o R2 de teste da regressão simples em 20 sementes,
   para três tamanhos de teste. Com 4 trimestres a estimativa varia de valor
   negativo a quase 1.
4. `aula13-reapresentacao.png`: o MAPE de dois modelos medido de três formas
   (dado não visto, dado de treino, e ajuste na base inteira avaliado num
   pedaço dela).

Decisões de forma, herdadas de `tools/graficos_aula10.py` a
`tools/graficos_aula12.py`: cores dos tokens de `assets/css/inteli-brand.css`,
1600x900 a 150 dpi, corpo 26 (a figura chega ao slide com cerca de 620px de
largura), vírgula decimal.

Uso: python3 tools/graficos_aula13.py            # gera as figuras e imprime os números
     python3 tools/graficos_aula13.py --numeros  # só imprime os números
"""
import calendar
import os
import sys

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import confusion_matrix, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeRegressor

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS = os.path.join(RAIZ, "dados")
MENSAL = os.path.join(DADOS, "mensal")
IMG = os.path.join(RAIZ, "assets", "img")

SERIES = ["abate_bovinos", "abate_suinos", "abate_frangos",
          "producao_ovos", "producao_leite"]
ALVO = "abate_frangos"
FEATURES = (["lag1", "lag2", "lag3", "lag12", "sen", "cos", "dias"]
            + [s + "_lag1" for s in SERIES if s != ALVO])
# As quatro outras séries no próprio mês do alvo: saem na mesma publicação
# que ele, então não existem no momento da previsão.
CONTEMPORANEAS = (["lag1", "lag2", "lag3", "lag12", "sen", "cos", "dias"]
                  + [s for s in SERIES if s != ALVO])
N_TESTE = 24
SEMENTE = 42
LIMIARES = (0.4, 0.5, 0.6, 0.7)


# ------------------------------------------------------------------ bases
def base_mensal():
    """A base analítica mensal das Aulas 07 a 12: 339 linhas, 315 de treino."""
    base = None
    for nome in SERIES:
        coluna = (pd.read_csv(os.path.join(MENSAL, nome + ".csv"))[["periodo", "valor"]]
                  .rename(columns={"valor": nome}))
        base = coluna if base is None else base.merge(coluna, on="periodo", how="inner")
    base = base.sort_values("periodo").reset_index(drop=True)
    base["mes"] = base["periodo"].str[-2:].astype(int)
    base["dias"] = [calendar.monthrange(int(p[:4]), int(p[-2:]))[1]
                    for p in base["periodo"]]
    base["sen"] = np.sin(2 * np.pi * base["mes"] / 12)
    base["cos"] = np.cos(2 * np.pi * base["mes"] / 12)
    for k in (1, 2, 3, 12):
        base["lag%d" % k] = base[ALVO].shift(k)
    for nome in SERIES:
        if nome != ALVO:
            base[nome + "_lag1"] = base[nome].shift(1)
    return base.dropna().reset_index(drop=True)


def base_trimestral():
    """Frangos e suínos por trimestre, com suínos do trimestre anterior."""
    def serie(nome, coluna):
        return (pd.read_csv(os.path.join(DADOS, nome + ".csv"))[["periodo", "valor"]]
                .rename(columns={"valor": coluna}))
    df = serie("abate_frangos", "frangos").merge(serie("abate_suinos", "suinos"),
                                                 on="periodo")
    df = df.sort_values("periodo").reset_index(drop=True)
    df["suinos_lag1"] = df["suinos"].shift(1)
    return df.dropna().reset_index(drop=True)


def mape(real, previsto):
    return float(np.mean(np.abs((real - previsto) / real)) * 100)


def _linear():
    return Pipeline([("escala", StandardScaler()), ("modelo", LinearRegression())])


def _floresta():
    return Pipeline([("escala", StandardScaler()),
                     ("modelo", RandomForestRegressor(n_estimators=300,
                                                      random_state=SEMENTE))])


# ------------------------------------------------------------------ medições
def medir_regressao_mensal(base=None):
    """Vazamento, identificador, reapresentação e métricas, na base mensal."""
    base = base_mensal() if base is None else base
    corte = len(base) - N_TESTE
    X, y = base[FEATURES].to_numpy(), base[ALVO].to_numpy()
    yt = y[corte:]
    m = {"linhas": len(base), "treino": corte,
         "primeiro_teste": base["periodo"].iloc[corte],
         "ultimo": base["periodo"].iloc[-1]}

    lin = _linear().fit(X[:corte], y[:corte])
    prev = lin.predict(X[corte:])
    erro = prev - yt
    m["mape"] = mape(yt, prev)
    m["mae_mi"] = float(np.mean(np.abs(erro)) / 1e6)
    m["vies_mi"] = float(np.mean(erro) / 1e6)
    m["rmse_mi"] = float(np.sqrt(np.mean(erro ** 2)) / 1e6)
    m["r2"] = float(r2_score(yt, prev))
    m["max_mi"] = float(np.max(np.abs(erro)) / 1e6)
    m["media_teste_mi"] = float(yt.mean() / 1e6)
    m["exatos"] = int(np.sum(prev == yt))
    m["superestimados"] = int(np.sum(erro > 0))
    # material, seção 4: deslocar as previsões para zerar o viés
    m["mae_sem_vies_mi"] = float(np.mean(np.abs(erro - erro.mean())) / 1e6)
    m["mape_treino_linear"] = mape(y[:corte], lin.predict(X[:corte]))
    m["mape_linear_tudo"] = mape(yt, _linear().fit(X, y).predict(X[corte:]))

    Xc = base[CONTEMPORANEAS].to_numpy()
    m["mape_contemporaneo"] = mape(yt, _linear().fit(Xc[:corte], y[:corte])
                                   .predict(Xc[corte:]))

    idx = np.arange(len(base)).reshape(-1, 1)
    arvore = DecisionTreeRegressor(random_state=SEMENTE).fit(idx[:corte], y[:corte])
    prev_idx = arvore.predict(idx[corte:])
    m["indice_treino"] = mape(y[:corte], arvore.predict(idx[:corte]))
    m["indice_teste"] = mape(yt, prev_idx)
    m["indice_distintos"] = int(np.unique(prev_idx).size)
    m["indice_valor_mi"] = float(prev_idx[0] / 1e6)

    flo = _floresta().fit(X[:corte], y[:corte])
    m["mape_floresta"] = mape(yt, flo.predict(X[corte:]))
    m["mape_treino_floresta"] = mape(y[:corte], flo.predict(X[:corte]))
    flo_tudo = _floresta().fit(X, y)
    m["mape_floresta_tudo"] = mape(yt, flo_tudo.predict(X[corte:]))
    m["mape_floresta_tudo_100"] = mape(y[-100:], flo_tudo.predict(X[-100:]))
    return m


def medir_classificacao(base=None):
    """O alvo binário da Aula 09: o abate do mês supera o mesmo mês do ano anterior."""
    base = base_mensal() if base is None else base
    corte = len(base) - N_TESTE
    X = base[FEATURES].to_numpy()
    alvo = (base[ALVO] > base["lag12"]).astype(int).to_numpy()
    escala = StandardScaler().fit(X[:corte])
    Ztr, Zte = escala.transform(X[:corte]), escala.transform(X[corte:])
    atr, ate = alvo[:corte], alvo[corte:]

    def contar(previsto):
        tn, fp, fn, tp = confusion_matrix(ate, previsto, labels=[0, 1]).ravel()
        return {"tp": int(tp), "fn": int(fn), "fp": int(fp), "tn": int(tn)}

    logistica = LogisticRegression(max_iter=2000, random_state=SEMENTE).fit(Ztr, atr)
    prev_log = logistica.predict(Zte)
    prob = logistica.predict_proba(Zte)[:, 1]
    svm = SVC(kernel="linear", random_state=SEMENTE).fit(Ztr, atr).predict(Zte)
    maioria = np.full(len(ate), int(atr.mean() > 0.5))

    return {
        "periodos": list(base["periodo"].iloc[corte:]),
        "real": ate.tolist(),
        "prev_logistica": prev_log.tolist(),
        "prob": prob.tolist(),
        "positivos_teste": int(ate.sum()),
        "logistica": contar(prev_log),
        "svm_linear": contar(svm),
        "baseline": contar(maioria),
        "limiares": {t: contar((prob >= t).astype(int)) for t in LIMIARES},
    }


def metricas(c):
    """Acurácia, precisão, revocação e F1 das duas classes, a partir das contagens."""
    tp, fn, fp, tn = c["tp"], c["fn"], c["fp"], c["tn"]
    total = tp + fn + fp + tn

    def razao(a, b):
        return a / b if b else 0.0

    prec, rev = razao(tp, tp + fp), razao(tp, tp + fn)
    prec0, rev0 = razao(tn, tn + fn), razao(tn, tn + fp)
    return {
        "acuracia": (tp + tn) / total,
        "precisao": prec, "revocacao": rev,
        "f1": razao(2 * prec * rev, prec + rev),
        "precisao_queda": prec0, "revocacao_queda": rev0,
        "f1_queda": razao(2 * prec0 * rev0, prec0 + rev0),
    }


def medir_regressao_simples(df=None):
    """Frangos sobre suínos do trimestre anterior, com as duas divisões."""
    df = base_trimestral() if df is None else df
    X, y = df[["suinos_lag1"]], df["frangos"]
    n = len(df)
    m = {"linhas": n, "primeiro": df["periodo"].iloc[0], "ultimo": df["periodo"].iloc[-1],
         "vazios": int(df[["frangos", "suinos"]].isna().sum().sum()),
         "r": float(np.corrcoef(df["suinos_lag1"], df["frangos"])[0, 1])}

    Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, random_state=SEMENTE)
    reta = LinearRegression().fit(Xtr, ytr)
    prev = reta.predict(Xte)
    m["teste"] = len(yte)
    m["inclinacao"] = float(reta.coef_[0])
    m["intercepto_mi"] = float(reta.intercept_ / 1e6)
    m["r2_aleatorio"] = float(r2_score(yte, prev))
    m["rmse_aleatorio_mi"] = float(np.sqrt(np.mean((yte - prev) ** 2)) / 1e6)

    k = len(yte)
    reta_c = LinearRegression().fit(X.iloc[:n - k], y.iloc[:n - k])
    prev_c = reta_c.predict(X.iloc[n - k:])
    m["corte_cronologico"] = df["periodo"].iloc[n - k]
    m["inclinacao_cronologica"] = float(reta_c.coef_[0])
    m["r2_cronologico"] = float(r2_score(y.iloc[n - k:], prev_c))
    m["rmse_cronologico_mi"] = float(np.sqrt(np.mean((y.iloc[n - k:] - prev_c) ** 2)) / 1e6)
    m["superestimados_cronologico"] = int(np.sum(prev_c > y.iloc[n - k:].to_numpy()))
    m["prev_cronologica"] = prev_c
    m["idx_teste_aleatorio"] = sorted(int(i) for i in Xte.index)

    sementes = {}
    for tamanho in (4, 8, 24):
        r2s = []
        for s in range(20):
            a, b, c, d = train_test_split(X, y, test_size=tamanho, random_state=s)
            r2s.append(float(r2_score(d, LinearRegression().fit(a, c).predict(b))))
        sementes[tamanho] = r2s
    m["sementes"] = sementes
    return m


def medir():
    return {"mensal": medir_regressao_mensal(), "classificacao": medir_classificacao(),
            "simples": medir_regressao_simples()}


def _num(formato, *valores):
    """Formata com vírgula decimal, como o resto do acervo."""
    return (formato % valores).replace(".", ",")


def imprimir(n):
    m, c, s = n["mensal"], n["classificacao"], n["simples"]
    print("base mensal      : %d linhas, treino %d, teste de %s a %s"
          % (m["linhas"], m["treino"], m["primeiro_teste"], m["ultimo"]))
    for chave in ("mape", "mae_mi", "vies_mi", "rmse_mi", "r2", "max_mi", "media_teste_mi",
                  "exatos", "superestimados", "mae_sem_vies_mi", "mape_treino_linear", "mape_linear_tudo",
                  "mape_contemporaneo", "indice_treino", "indice_teste", "indice_distintos",
                  "indice_valor_mi", "mape_floresta", "mape_treino_floresta",
                  "mape_floresta_tudo", "mape_floresta_tudo_100"):
        print("  %-24s %s" % (chave, m[chave]))
    print("classificação    : %d positivos em 24" % c["positivos_teste"])
    for nome in ("baseline", "logistica", "svm_linear"):
        print("  %-10s %s %s" % (nome, c[nome],
                                 {k: round(v, 4) for k, v in metricas(c[nome]).items()}))
    for t, cont in c["limiares"].items():
        print("  limiar %.1f %s" % (t, cont))
    print("regressão simples: %d trimestres, %s a %s" % (s["linhas"], s["primeiro"], s["ultimo"]))
    for chave in ("vazios", "r", "teste", "inclinacao", "intercepto_mi", "r2_aleatorio",
                  "rmse_aleatorio_mi", "corte_cronologico", "inclinacao_cronologica",
                  "r2_cronologico", "rmse_cronologico_mi", "superestimados_cronologico"):
        print("  %-24s %s" % (chave, s[chave]))
    for tamanho, r2s in s["sementes"].items():
        print("  teste %2d: R2 de %.4f a %.4f, mediana %.4f"
              % (tamanho, min(r2s), max(r2s), float(np.median(r2s))))


# ------------------------------------------------------------------ figuras
TINTA = "#2e2640"          # --inteli-roxo
DESTAQUE = "#ff4545"       # --inteli-coral
REFERENCIA_1 = "#b2b6bf"   # --inteli-cinza-escuro
REFERENCIA_2 = "#89cea5"   # --inteli-verde
NUVEM = "#caced6"          # --inteli-cinza-medio
FUNDO = "#ffffff"          # --inteli-branco


def _preparar():
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({
        "figure.facecolor": FUNDO, "axes.facecolor": FUNDO,
        "axes.edgecolor": REFERENCIA_1, "axes.labelcolor": TINTA,
        "text.color": TINTA, "xtick.color": TINTA, "ytick.color": TINTA,
        "font.size": 26, "axes.titlesize": 28, "legend.frameon": False,
    })
    return plt


def _sem_moldura(eixo):
    for lado in ("top", "right"):
        eixo.spines[lado].set_visible(False)


def _salvar(plt, fig, nome):
    os.makedirs(IMG, exist_ok=True)
    fig.savefig(os.path.join(IMG, nome), dpi=150, facecolor=FUNDO)
    plt.close(fig)


def figura_dispersao(plt, df, s):
    from matplotlib.ticker import FuncFormatter
    fig, ax = plt.subplots(figsize=(16, 9))
    x, y = df["suinos_lag1"] / 1e9, df["frangos"] / 1e9
    teste = set(s["idx_teste_aleatorio"])
    cor = [DESTAQUE if i in teste else TINTA for i in range(len(df))]
    ax.scatter(x, y, s=90, c=cor, alpha=0.85, edgecolors="none")
    grade = np.linspace(x.min(), x.max(), 50)
    ax.plot(grade, (s["inclinacao"] * grade * 1e9 + s["intercepto_mi"] * 1e6) / 1e9,
            color=REFERENCIA_2, lw=5)
    ax.set_xlabel("suínos no trimestre anterior (bilhões de kg)")
    ax.set_ylabel("frangos (bilhões de kg)")
    fmt = FuncFormatter(lambda v, _: _num("%.1f", v))
    ax.xaxis.set_major_formatter(fmt)
    ax.yaxis.set_major_formatter(fmt)
    ax.text(0.03, 0.93, _num("r = %.3f", s["r"]), transform=ax.transAxes, fontsize=30)
    ax.text(0.03, 0.83, "inclinação = " + _num("%.2f", s["inclinacao"]),
            transform=ax.transAxes, fontsize=30)
    ax.text(0.97, 0.07, "roxo: treino sorteado  ·  coral: teste sorteado",
            transform=ax.transAxes, ha="right", fontsize=24)
    _sem_moldura(ax)
    fig.tight_layout()
    _salvar(plt, fig, "aula13-dispersao.png")


def figura_cronologica(plt, df, s):
    from matplotlib.ticker import FuncFormatter
    fig, ax = plt.subplots(figsize=(16, 9))
    n, k = len(df), s["teste"]
    pos = np.arange(n)
    ax.plot(pos, df["frangos"] / 1e9, color=TINTA, lw=4, label="real")
    ax.plot(pos[n - k:], s["prev_cronologica"] / 1e9, color=DESTAQUE, lw=5,
            label="reta ajustada até o corte")
    ax.axvline(n - k - 0.5, color=REFERENCIA_1, lw=3, ls="--")
    ax.text(n - k - 1.5, 3.55, "corte: " + s["corte_cronologico"], ha="right", fontsize=24)
    anos = [i for i, p in enumerate(df["periodo"]) if p.endswith("T1") and int(p[:4]) % 5 == 0]
    ax.set_xticks(anos)
    ax.set_xticklabels([df["periodo"].iloc[i][:4] for i in anos])
    ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: _num("%.1f", v)))
    ax.set_ylabel("frangos (bilhões de kg)")
    ax.legend(loc="upper left")
    _sem_moldura(ax)
    fig.tight_layout()
    _salvar(plt, fig, "aula13-cronologica.png")


def figura_sementes(plt, s):
    fig, ax = plt.subplots(figsize=(16, 9))
    rotulos = []
    for j, (tamanho, r2s) in enumerate(sorted(s["sementes"].items())):
        jitter = np.linspace(-0.18, 0.18, len(r2s))
        ax.scatter(np.full(len(r2s), j) + jitter, r2s, s=160, color=TINTA, alpha=0.8,
                   edgecolors="none")
        ax.text(j + 0.24, min(r2s), "mínimo " + _num("%.2f", min(r2s)), va="center",
                fontsize=24, color=DESTAQUE)
        rotulos.append("%d trimestres" % tamanho)
    ax.axhline(0, color=REFERENCIA_1, lw=2)
    ax.set_xticks(range(len(rotulos)))
    ax.set_xticklabels(rotulos)
    ax.set_xlim(-0.5, len(rotulos) - 0.1)
    ax.set_ylabel("R² de teste")
    ax.set_xlabel("tamanho do teste sorteado (20 sementes cada)")
    ax.yaxis.set_major_formatter(__import__("matplotlib").ticker.FuncFormatter(
        lambda v, _: _num("%.1f", v)))
    _sem_moldura(ax)
    fig.tight_layout()
    _salvar(plt, fig, "aula13-sementes.png")


def figura_reapresentacao(plt, m):
    fig, ax = plt.subplots(figsize=(16, 9))
    linhas = [
        ("floresta: 24 meses não vistos", m["mape_floresta"], TINTA),
        ("floresta: os 315 meses de treino", m["mape_treino_floresta"], DESTAQUE),
        ("floresta: ajustada nas 339, medida nos 24", m["mape_floresta_tudo"], DESTAQUE),
        ("linear: 24 meses não vistos", m["mape"], TINTA),
        ("linear: ajustada nas 339, medida nos 24", m["mape_linear_tudo"], DESTAQUE),
    ]
    pos = np.arange(len(linhas))[::-1]
    ax.barh(pos, [l[1] for l in linhas], color=[l[2] for l in linhas], height=0.6)
    for p, (rot, val, _) in zip(pos, linhas):
        ax.text(val + 0.08, p, _num("%.2f%%", val), va="center", fontsize=26)
    ax.set_yticks(pos)
    ax.set_yticklabels([l[0] for l in linhas])
    ax.set_xlabel("MAPE (%)")
    ax.set_xlim(0, max(l[1] for l in linhas) * 1.22)
    ax.xaxis.set_major_formatter(__import__("matplotlib").ticker.FuncFormatter(
        lambda v, _: _num("%.0f", v)))
    _sem_moldura(ax)
    fig.tight_layout()
    _salvar(plt, fig, "aula13-reapresentacao.png")


def main(argv):
    numeros = medir()
    imprimir(numeros)
    if "--numeros" in argv:
        return 0
    plt = _preparar()
    df = base_trimestral()
    figura_dispersao(plt, df, numeros["simples"])
    figura_cronologica(plt, df, numeros["simples"])
    figura_sementes(plt, numeros["simples"])
    figura_reapresentacao(plt, numeros["mensal"])
    print("figuras gravadas em", os.path.relpath(IMG, RAIZ))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

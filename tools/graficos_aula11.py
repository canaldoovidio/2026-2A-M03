"""Gera as quatro figuras da Aula 11 a partir dos CSVs de dados/mensal/.

1. `aula11-quadro-de-referencia.png`. O MAPE de teste dos quatro modelos de
   referência do acervo mais o campeão do AutoML, nos mesmos 24 meses: a
   regressão linear em nível erra 2,86%, a mesma em razão 3,32%, a baseline de
   coeficiente fixo da LDC 3,71% e a floresta ajustada à mão na Aula 10 erra
   4,21%, que é o pior dos quatro. O campeão do `compare_models()` erra 2,84% e
   fica abaixo de todos.

   **O campeão desta figura é o do protocolo temporal**, com
   `fold_strategy=TimeSeriesSplit(5)` e `train_size=0.99`, e não o dos defaults.
   O motivo é comparabilidade: os quatro modelos de referência treinam com os
   315 meses inteiros, e o campeão dos defaults treinaria com 220 deles,
   sorteados. Pôr os dois no mesmo gráfico compararia família E volume de dado
   ao mesmo tempo. O campeão dos defaults erra 2,81%, quase o mesmo, e esse
   número aparece na figura 4, onde o protocolo é o assunto.

2. `aula11-leaderboard.png`. As dez primeiras linhas do leaderboard do PyCaret
   sobre o alvo em razão, pintadas por família: os oito primeiros colocados são
   modelos lineares, e só o nono e o décimo são de outra família. É o que
   sustenta a tese da aula, que o ganho veio de varrer a família e não de
   ajustar o candidato. A figura mantém a ordem do PyCaret de propósito, que é
   ordenada pelo **R2** e não pelo MAPE: por isso `br`, com 4,04%, aparece acima
   de `lasso`, com 4,03%.

3. `aula11-r2-engana.png`. Dois painéis, com os mesmos modelos e as mesmas
   features, mudando só o alvo. À esquerda, o R2 do leaderboard cai de cerca de
   0,98 em nível para cerca de 0,48 em razão. À direita, o MAPE dos mesmos
   modelos fica na mesma casa. O modelo não piorou: o alvo em razão tem menos
   variância a explicar, e o R2 é a fração dessa variância.

4. `aula11-estimativa-contra-teste.png`. O MAPE que o leaderboard estima contra
   o MAPE medido nos 24 meses de teste, com o fold default e com
   `TimeSeriesSplit(5)`. A estimativa temporal erra cerca de dois décimos de
   ponto, contra cerca de meio ponto da default.

Decisões de forma, herdadas de `tools/graficos_aula09.py` e
`tools/graficos_aula10.py`:

- roxo #2e2640 como tinta, coral #ff4545 como destaque, verde #89cea5 e cinza
  escuro #b2b6bf como referências, cinza médio #caced6 e cinza claro #e6eaeb nos
  fundos. As cores vêm dos tokens de `assets/css/inteli-brand.css`.
- nenhum valor interpolado ou inventado: tudo é medido sobre `dados/mensal/`,
  com a mesma lógica de junção, defasagem e corte temporal de
  `tools/tests/test_automl_aula11.py`, reimplementada aqui de propósito.
- 1600x900 a 150 dpi, e **corpo 26**, pelo motivo medido em
  `tools/graficos_aula10.py`: a figura chega ao slide com cerca de 620px de
  largura, e o corpo 18 do resto do acervo fica ilegível em projeção. Cada
  figura aqui já nasceu com poucos elementos de texto, pela mesma razão.
- separador decimal é vírgula, como em `tools/graficos_aula04.py`.

Uso: python3 tools/graficos_aula11.py   (requer matplotlib, pandas, numpy,
scikit-learn e pycaret==4.0.0a8, listados em requirements-ci.txt)
"""
import calendar
import os
import warnings

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler

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
FLORESTA_AULA10 = dict(n_estimators=600, max_depth=4, min_samples_leaf=5)

LINEARES = {"lr", "ridge", "lasso", "en", "lar", "llar", "br", "ard", "tr",
            "huber", "ransac", "par", "omp"}

plt.rcParams.update({
    "figure.facecolor": FUNDO,
    "axes.facecolor": FUNDO,
    "axes.edgecolor": REFERENCIA_1,
    "axes.labelcolor": TINTA,
    "text.color": TINTA,
    "xtick.color": TINTA,
    "ytick.color": TINTA,
    "font.size": 26,
    "axes.titlesize": 28,
    "legend.frameon": False,
})


def _num(formato, *valores):
    """Formata com vírgula decimal, como o resto do acervo."""
    return (formato % valores).replace(".", ",")


def _sem_moldura(eixo, lados=("top", "right")):
    for lado in lados:
        eixo.spines[lado].set_visible(False)


def base_analitica():
    """A base analítica mensal das Aulas 07 a 10: 339 linhas, 315 de treino."""
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


def _mape(real, previsto):
    return float(np.mean(np.abs((real - previsto) / real)) * 100)


def _partes(base):
    corte = len(base) - N_TESTE
    X = base[FEATURES]
    y = base[ALVO].to_numpy(dtype=float)
    lag12 = base["lag12"].to_numpy(dtype=float)
    return corte, X, y, lag12


def referencias(base):
    """Os quatro modelos de referência do acervo, no mesmo conjunto de teste."""
    corte, X, y, lag12 = _partes(base)
    razao = y / lag12
    escalador = StandardScaler().fit(X.iloc[:corte])
    Ztr = escalador.transform(X.iloc[:corte])
    Zte = escalador.transform(X.iloc[corte:])

    linear_nivel = LinearRegression().fit(Ztr, y[:corte])
    linear_razao = LinearRegression().fit(Ztr, razao[:corte])
    floresta = RandomForestRegressor(random_state=SEMENTE, **FLORESTA_AULA10)
    floresta.fit(X.iloc[:corte], razao[:corte])
    fator = float(np.mean(razao[:corte]))

    return [
        ("regressão linear,\nalvo em nível", _mape(y[corte:], linear_nivel.predict(Zte))),
        ("regressão linear,\nalvo em razão",
         _mape(y[corte:], linear_razao.predict(Zte) * lag12[corte:])),
        ("baseline\nda LDC", _mape(y[corte:], lag12[corte:] * fator)),
        ("floresta ajustada\nna Aula 10",
         _mape(y[corte:], floresta.predict(X.iloc[corte:]) * lag12[corte:])),
    ]


def experimento(base, em_razao, **kwargs):
    """Roda o compare_models do PyCaret sobre os 315 meses de treino."""
    from pycaret.regression import RegressionExperiment

    corte, X, y, lag12 = _partes(base)
    alvo = (y / lag12) if em_razao else y

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        exp = RegressionExperiment(session_id=SEMENTE, **kwargs)
        exp.fit(X.iloc[:corte], pd.Series(alvo[:corte], name="alvo"))
        resultado = exp.compare_models(n_select=5)

    quadro = exp.pull()
    campeao = resultado.models[0]
    previsto = np.asarray(campeao.predict(X.iloc[corte:]), dtype=float)
    if em_razao:
        previsto = previsto * lag12[corte:]
    return {
        "quadro": quadro,
        "ids": list(resultado.ranked_ids),
        "estimado": float(quadro.iloc[0]["MAPE"]) * 100,
        "r2": float(quadro.iloc[0]["R2"]),
        "teste": _mape(y[corte:], previsto),
        "treino_interno": len(exp.X_train),
    }


# --------------------------------------------------------------------- figura 1
def quadro_de_referencia(base, destino, campeao=None):
    """As quatro referências mais o campeão do AutoML, em ordem de erro."""
    itens = referencias(base)
    if campeao is not None:
        itens = itens + [("campeão do AutoML,\nnível e temporal", campeao)]
    itens.sort(key=lambda item: item[1])

    fig, eixo = plt.subplots(figsize=(16, 9))
    rotulos = [nome for nome, _ in itens]
    valores = [erro for _, erro in itens]
    cores = []
    for nome, _ in itens:
        if "AutoML" in nome:
            cores.append(REFERENCIA_2)
        elif "Aula 10" in nome:
            cores.append(DESTAQUE)
        else:
            cores.append(NUVEM)

    posicoes = np.arange(len(valores))
    eixo.bar(posicoes, valores, color=cores, edgecolor=TINTA, linewidth=0.8)
    for posicao, valor in zip(posicoes, valores):
        eixo.text(posicao, valor + 0.09, _num("%.2f%%", valor),
                  ha="center", va="bottom", fontsize=27)

    eixo.set_xticks(posicoes)
    eixo.set_xticklabels(rotulos, fontsize=22)
    eixo.set_ylabel("MAPE nos 24 meses de teste", fontsize=25)
    eixo.set_ylim(0, max(valores) * 1.30)
    eixo.set_yticks([0, 2, 4])
    eixo.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: _num("%.0f%%", v)))
    eixo.tick_params(axis="y", labelsize=24)
    _sem_moldura(eixo)

    fig.tight_layout()
    fig.savefig(destino, dpi=150, facecolor=FUNDO)
    plt.close(fig)
    return destino


# --------------------------------------------------------------------- figura 2
def leaderboard(quadro, ids, destino, quantas=10):
    """As dez primeiras linhas do leaderboard, pintadas por família."""
    linhas = quadro.head(quantas)
    nomes = [str(i) for i in ids[:quantas]] if len(ids) >= quantas else list(linhas["Model"])
    valores = [float(v) * 100 for v in linhas["MAPE"].to_numpy()[:quantas]]
    cores = [DESTAQUE if n in LINEARES else NUVEM for n in nomes]
    # o leaderboard vem ordenado pelo R2, e nao pelo MAPE: por isso br (4,04%)
    # aparece acima de lasso (4,03%). Manter a ordem do PyCaret de proposito,
    # que e a ordem que o aluno ve na tela

    fig, eixo = plt.subplots(figsize=(16, 9))
    posicoes = np.arange(len(valores))
    eixo.barh(posicoes, valores, color=cores, edgecolor=TINTA, linewidth=0.8)
    eixo.set_yticks(posicoes)
    eixo.set_yticklabels(nomes, fontsize=24)
    eixo.invert_yaxis()
    eixo.set_xlabel("MAPE estimado pelo leaderboard", fontsize=25)
    eixo.set_xlim(0, max(valores) * 1.22)
    eixo.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: _num("%.0f%%", v)))
    eixo.tick_params(axis="x", labelsize=24)
    for posicao, valor in zip(posicoes, valores):
        eixo.text(valor + max(valores) * 0.015, posicao, _num("%.2f%%", valor),
                  va="center", fontsize=22)

    legenda = [plt.Line2D([0], [0], color=DESTAQUE, linewidth=14, label="modelo linear"),
               plt.Line2D([0], [0], color=NUVEM, linewidth=14, label="os demais")]
    # dentro do eixo a legenda cobre as duas ultimas barras: ela sai para baixo
    eixo.legend(handles=legenda, loc="upper center", bbox_to_anchor=(0.5, -0.14),
                ncol=2, fontsize=24)
    _sem_moldura(eixo)

    fig.tight_layout()
    fig.savefig(destino, dpi=150, facecolor=FUNDO)
    plt.close(fig)
    return destino


# --------------------------------------------------------------------- figura 3
def r2_engana(em_nivel, em_razao, destino):
    """O R2 despenca ao trocar de alvo, e o MAPE dos mesmos modelos não."""
    fig, (esq, dir_) = plt.subplots(1, 2, figsize=(16, 9))
    rotulos = ["alvo em\nnível", "alvo em\nrazão"]
    posicoes = np.arange(2)

    valores_r2 = [em_nivel["r2"], em_razao["r2"]]
    esq.bar(posicoes, valores_r2, color=[NUVEM, DESTAQUE],
            edgecolor=TINTA, linewidth=0.8, width=0.55)
    for posicao, valor in zip(posicoes, valores_r2):
        esq.text(posicao, valor + 0.03, _num("%.3f", valor),
                 ha="center", va="bottom", fontsize=28)
    esq.set_xticks(posicoes)
    esq.set_xticklabels(rotulos, fontsize=24)
    esq.set_ylim(0, 1.22)
    esq.set_yticks([0, 0.5, 1.0])
    esq.tick_params(axis="y", labelsize=24)
    esq.set_title("O R2 despenca", pad=18, fontsize=27)
    _sem_moldura(esq)

    valores_mape = [em_nivel["estimado"], em_razao["estimado"]]
    dir_.bar(posicoes, valores_mape, color=[NUVEM, DESTAQUE],
             edgecolor=TINTA, linewidth=0.8, width=0.55)
    for posicao, valor in zip(posicoes, valores_mape):
        dir_.text(posicao, valor + 0.12, _num("%.2f%%", valor),
                  ha="center", va="bottom", fontsize=28)
    dir_.set_xticks(posicoes)
    dir_.set_xticklabels(rotulos, fontsize=24)
    dir_.set_ylim(0, max(valores_mape) * 1.35)
    dir_.set_yticks([0, 2, 4])
    dir_.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: _num("%.0f%%", v)))
    dir_.tick_params(axis="y", labelsize=24)
    dir_.set_title("O MAPE não muda de casa", pad=18, fontsize=27)
    _sem_moldura(dir_)

    fig.tight_layout(w_pad=3)
    fig.savefig(destino, dpi=150, facecolor=FUNDO)
    plt.close(fig)
    return destino


# --------------------------------------------------------------------- figura 4
def estimativa_contra_teste(default, temporal, destino):
    """O que o leaderboard estima contra o que o teste mede, nos dois folds."""
    fig, eixo = plt.subplots(figsize=(16, 9))
    grupos = [("fold default\n(KFold)", default), ("fold temporal\n(TimeSeriesSplit)", temporal)]
    largura = 0.32
    posicoes = np.arange(len(grupos))

    estimados = [g["estimado"] for _, g in grupos]
    testes = [g["teste"] for _, g in grupos]
    eixo.bar(posicoes - largura / 2, estimados, largura, color=NUVEM,
             edgecolor=TINTA, linewidth=0.8, label="estimado pelo leaderboard")
    eixo.bar(posicoes + largura / 2, testes, largura, color=TINTA,
             edgecolor=TINTA, linewidth=0.8, label="medido nos 24 meses de teste")

    for posicao, (estimado, teste) in enumerate(zip(estimados, testes)):
        eixo.text(posicao - largura / 2, estimado + 0.08, _num("%.2f%%", estimado),
                  ha="center", va="bottom", fontsize=25)
        eixo.text(posicao + largura / 2, teste + 0.08, _num("%.2f%%", teste),
                  ha="center", va="bottom", fontsize=25)
        diferenca = abs(estimado - teste)
        eixo.text(posicao, max(estimado, teste) + 0.62,
                  "erra " + _num("%.2f", diferenca) + " ponto",
                  ha="center", va="bottom", fontsize=26,
                  color=DESTAQUE if diferenca > 0.3 else REFERENCIA_2)

    eixo.set_xticks(posicoes)
    eixo.set_xticklabels([nome for nome, _ in grupos], fontsize=24)
    eixo.set_ylabel("MAPE", fontsize=25)
    eixo.set_ylim(0, max(estimados + testes) * 1.55)
    eixo.set_yticks([0, 2, 4])
    eixo.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: _num("%.0f%%", v)))
    eixo.tick_params(axis="y", labelsize=24)
    eixo.legend(loc="upper center", ncol=2, fontsize=24, bbox_to_anchor=(0.5, 1.02))
    _sem_moldura(eixo)

    fig.tight_layout()
    fig.savefig(destino, dpi=150, facecolor=FUNDO)
    plt.close(fig)
    return destino


def main():
    destino = os.path.join(RAIZ, "assets", "img")
    base = base_analitica()
    print("base: %d linhas, de %s a %s"
          % (len(base), base["periodo"].iloc[0], base["periodo"].iloc[-1]))

    print("rodando o compare_models tres vezes")
    em_nivel = experimento(base, em_razao=False)
    em_razao = experimento(base, em_razao=True)
    temporal = experimento(base, em_razao=True, train_size=0.99,
                           fold_strategy=TimeSeriesSplit(n_splits=5))
    print("  nivel, default:   topo %s, estimado %.2f%%, teste %.2f%%, R2 %.4f"
          % (em_nivel["ids"][0], em_nivel["estimado"], em_nivel["teste"], em_nivel["r2"]))
    print("  razao, default:   topo %s, estimado %.2f%%, teste %.2f%%, R2 %.4f"
          % (em_razao["ids"][0], em_razao["estimado"], em_razao["teste"], em_razao["r2"]))
    print("  razao, temporal:  topo %s, estimado %.2f%%, teste %.2f%%, R2 %.4f"
          % (temporal["ids"][0], temporal["estimado"], temporal["teste"], temporal["r2"]))

    # o campeao da figura 1 e o do protocolo temporal, para ser comparavel com
    # os quatro modelos de referencia, que treinam com os 315 meses inteiros
    nivel_temporal = experimento(base, em_razao=False, train_size=0.99,
                                 fold_strategy=TimeSeriesSplit(n_splits=5))
    print("  nivel, temporal:  topo %s, estimado %.2f%%, teste %.2f%%, treino %d"
          % (nivel_temporal["ids"][0], nivel_temporal["estimado"],
             nivel_temporal["teste"], nivel_temporal["treino_interno"]))

    print("gerando aula11-quadro-de-referencia.png")
    quadro_de_referencia(base, os.path.join(destino, "aula11-quadro-de-referencia.png"),
                         campeao=nivel_temporal["teste"])
    print("gerando aula11-leaderboard.png")
    leaderboard(em_razao["quadro"], em_razao["ids"],
                os.path.join(destino, "aula11-leaderboard.png"))
    print("gerando aula11-r2-engana.png")
    r2_engana(em_nivel, em_razao, os.path.join(destino, "aula11-r2-engana.png"))
    print("gerando aula11-estimativa-contra-teste.png")
    estimativa_contra_teste(em_razao, temporal,
                            os.path.join(destino, "aula11-estimativa-contra-teste.png"))
    print("pronto")


if __name__ == "__main__":
    main()

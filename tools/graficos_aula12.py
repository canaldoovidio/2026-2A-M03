"""Gera as três figuras da Aula 12 a partir dos CSVs de dados/mensal/.

1. `aula12-coeficiente-x-previsao.png`. Um painel em **eixo logarítmico**, com
   o deslocamento relativo dos onze coeficientes quando o modelo é reajustado
   de 315 para 339 meses (mediana de 17,2%, e `abate_bovinos_lag1` em 3.439%,
   trocando de sinal) e, separada por um vão, a pior das 24 previsões, em
   0,97%. As duas grandezas dividem o eixo de propósito, porque a afirmação da
   aula é sobre a razão entre elas.

   A primeira versão desta figura tinha dois painéis, com as 24 previsões barra
   a barra. Foi descartada na conferência da imagem: 35 barras em corpo 26
   sobrepõem os rótulos do eixo e cortam o título.

2. `aula12-colinearidade.png`. O VIF de cada feature, com a linha de 10, que é
   o limiar usual. Sete das onze passam dele e `lag1` chega a 69. É a causa
   medida da figura 1: features colineares deixam o modelo redistribuir peso
   entre elas sem mexer no ajuste.

3. `aula12-historico-previsao.png`. Os 36 últimos meses da série real e a
   previsão do modelo exportado nos 24 meses de teste. É a figura que a Aula 13
   transforma em tela de Streamlit, e serve aqui para mostrar o que o
   `.joblib` de 1,5 KB de fato entrega.

Decisões de forma, herdadas de `tools/graficos_aula10.py` e
`tools/graficos_aula11.py`:

- roxo #2e2640 como tinta, coral #ff4545 como destaque, verde #89cea5 e cinza
  escuro #b2b6bf como referências, cinza médio #caced6 e cinza claro #e6eaeb nos
  fundos. As cores vêm dos tokens de `assets/css/inteli-brand.css`.
- nenhum valor interpolado ou inventado: tudo é medido sobre `dados/mensal/`,
  com a mesma lógica de junção, defasagem e corte temporal de
  `tools/tests/test_pipeline_aula12.py`, reimplementada aqui de propósito.
- 1600x900 a 150 dpi, e corpo 26, pelo motivo medido em
  `tools/graficos_aula10.py`: a figura chega ao slide com cerca de 620px de
  largura, e o corpo 18 do resto do acervo fica ilegível em projeção.
- separador decimal é vírgula, como em `tools/graficos_aula04.py`.

Uso: python3 tools/graficos_aula12.py   (requer matplotlib, pandas, numpy e
scikit-learn, listados em requirements-ci.txt)
"""
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FuncFormatter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from exportar_modelo_aula12 import (ALVO, FEATURES, N_TESTE,  # noqa: E402
                                    base_analitica, novo_pipeline)
from sklearn.preprocessing import StandardScaler  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(RAIZ, "assets", "img")

# cores lidas de assets/css/inteli-brand.css (paleta da Graduacao, p.66/p.68)
TINTA = "#2e2640"          # --inteli-roxo
DESTAQUE = "#ff4545"       # --inteli-coral
REFERENCIA_1 = "#b2b6bf"   # --inteli-cinza-escuro
REFERENCIA_2 = "#89cea5"   # --inteli-verde
NUVEM = "#caced6"          # --inteli-cinza-medio
SOMBRA = "#e6eaeb"         # --inteli-cinza-claro
FUNDO = "#ffffff"          # --inteli-branco

# nomes curtos, para caber no eixo em corpo 26
CURTO = {
    "lag1": "lag1", "lag2": "lag2", "lag3": "lag3", "lag12": "lag12",
    "sen": "sen", "cos": "cos", "dias": "dias",
    "abate_bovinos_lag1": "bovinos", "abate_suinos_lag1": "suínos",
    "producao_ovos_lag1": "ovos", "producao_leite_lag1": "leite",
}

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


def _ajustes():
    """Os dois Pipelines que a aula compara, e os dados de teste."""
    base = base_analitica()
    corte = len(base) - N_TESTE
    X_tr, y_tr = base[FEATURES].to_numpy()[:corte], base[ALVO].to_numpy()[:corte]
    X_te, y_te = base[FEATURES].to_numpy()[corte:], base[ALVO].to_numpy()[corte:]
    X_full, y_full = base[FEATURES].to_numpy(), base[ALVO].to_numpy()

    avaliado = novo_pipeline().fit(X_tr, y_tr)
    producao = novo_pipeline().fit(X_full, y_full)
    return base, avaliado, producao, X_tr, X_te, y_te


def figura_coeficiente_x_previsao():
    base, avaliado, producao, X_tr, X_te, y_te = _ajustes()

    coef_a = avaliado.named_steps["modelo"].coef_
    coef_p = producao.named_steps["modelo"].coef_
    desloc_coef = np.abs((coef_p - coef_a) / coef_a) * 100
    trocou_sinal = np.sign(coef_a) != np.sign(coef_p)

    prev_a, prev_p = avaliado.predict(X_te), producao.predict(X_te)
    desloc_prev = np.abs((prev_p - prev_a) / prev_a) * 100

    # Um painel só, com os onze coeficientes e, separada por um vão, a maior
    # das 24 previsões. Duas escalas de barra no mesmo eixo logarítmico é o que
    # torna a razão entre as duas grandezas legível de uma vez. A versão em dois
    # painéis, com as 24 previsões barra a barra, foi descartada: 35 barras em
    # corpo 26 sobrepõem os rótulos e o slide fica ilegível em projeção.
    ordem = np.argsort(desloc_coef)
    posicoes = np.arange(len(FEATURES)) + 1.6   # o vão fica na posição 0 a 1
    fig, eixo = plt.subplots(figsize=(1600 / 150, 900 / 150), dpi=150)

    cores = [DESTAQUE if trocou_sinal[i] else TINTA for i in ordem]
    eixo.barh(posicoes, desloc_coef[ordem], color=cores, height=0.74)
    eixo.barh([0], [float(np.max(desloc_prev))], color=REFERENCIA_2, height=0.74)

    eixo.set_yticks(list(posicoes) + [0])
    eixo.set_yticklabels([CURTO[FEATURES[i]] for i in ordem]
                         + ["previsão\n(pior mês)"])
    eixo.tick_params(axis="y", labelsize=22)
    eixo.set_xscale("log")
    eixo.set_xlim(0.05, 90000)
    eixo.set_ylim(-0.8, len(FEATURES) + 1.4)
    # quatro marcas, e nao seis: com 1000% e 10000% no eixo os rotulos se
    # sobrepoem em corpo 22, e a figura chega ao slide com 620px de largura.
    eixo.set_xticks([0.1, 1, 10, 100, 1000])
    eixo.tick_params(axis="x", labelsize=22)
    eixo.xaxis.set_major_formatter(FuncFormatter(lambda v, _: _num("%g%%", v)))
    eixo.set_xlabel("deslocamento ao reajustar de 315 para 339 meses", fontsize=22)
    eixo.grid(axis="x", color=SOMBRA, linewidth=1)
    eixo.set_axisbelow(True)
    _sem_moldura(eixo)

    i_troca = int(np.argmax(desloc_coef))
    eixo.annotate("troca de sinal", xy=(desloc_coef[i_troca] * 1.4, len(FEATURES) + 0.6),
                  ha="left", va="center", fontsize=22, color=DESTAQUE)
    eixo.annotate(_num("%.2f%%", float(np.max(desloc_prev))),
                  xy=(float(np.max(desloc_prev)) * 1.4, 0),
                  ha="left", va="center", fontsize=22, color=TINTA)

    fig.tight_layout()
    destino = os.path.join(IMG, "aula12-coeficiente-x-previsao.png")
    fig.savefig(destino, facecolor=FUNDO)
    plt.close(fig)
    print("%-44s mediana dos coeficientes %s, maior previsao %s"
          % (os.path.basename(destino),
             _num("%.1f%%", float(np.median(desloc_coef))),
             _num("%.2f%%", float(np.max(desloc_prev)))))


def figura_colinearidade():
    base, _, _, X_tr, _, _ = _ajustes()

    C = np.corrcoef(StandardScaler().fit_transform(X_tr), rowvar=False)
    vif = np.diag(np.linalg.inv(C))
    ordem = np.argsort(vif)

    fig, eixo = plt.subplots(figsize=(1600 / 150, 900 / 150), dpi=150)
    cores = [DESTAQUE if vif[i] > 10 else NUVEM for i in ordem]
    eixo.barh([CURTO[FEATURES[i]] for i in ordem], vif[ordem],
              color=cores, height=0.72)
    eixo.axvline(10, color=TINTA, linewidth=2, linestyle="--")
    eixo.annotate("VIF 10, limiar usual", xy=(10, len(FEATURES) - 0.4),
                  xytext=(8, 0), textcoords="offset points",
                  ha="left", va="center", fontsize=22, color=TINTA)

    # fundo branco no rotulo: o valor de `bovinos` (7,4) cai exatamente sobre a
    # linha tracejada do limiar, e sem o bbox os dois se sobrepoem.
    for i, k in enumerate(ordem):
        eixo.text(vif[k] + 1.5, i, _num("%.1f", vif[k]),
                  va="center", fontsize=20, color=TINTA,
                  bbox=dict(facecolor=FUNDO, edgecolor="none", pad=1.5))

    eixo.set_xlim(0, 82)
    eixo.set_xlabel("fator de inflação da variância")
    eixo.grid(axis="x", color=SOMBRA, linewidth=1)
    eixo.set_axisbelow(True)
    _sem_moldura(eixo)

    fig.tight_layout()
    destino = os.path.join(IMG, "aula12-colinearidade.png")
    fig.savefig(destino, facecolor=FUNDO)
    plt.close(fig)
    print("%-44s %d features acima de 10, maior %s"
          % (os.path.basename(destino), int(np.sum(vif > 10)),
             _num("%.1f", float(np.max(vif)))))


def figura_historico_previsao():
    base, avaliado, producao, _, X_te, y_te = _ajustes()

    janela = 36
    recorte = base.iloc[-janela:]
    rotulos = recorte["periodo"].tolist()
    x = np.arange(janela)
    previsto = avaliado.predict(X_te)

    fig, eixo = plt.subplots(figsize=(1600 / 150, 900 / 150), dpi=150)
    eixo.plot(x, recorte[ALVO].to_numpy() / 1e9, color=TINTA, linewidth=3,
              label="produção medida pelo IBGE")
    eixo.plot(x[janela - N_TESTE:], previsto / 1e9, color=DESTAQUE, linewidth=3,
              linestyle="--", label="previsão do modelo exportado")
    eixo.axvline(janela - N_TESTE - 0.5, color=REFERENCIA_1, linewidth=2)
    eixo.annotate("início do teste", xy=(janela - N_TESTE - 0.5, eixo.get_ylim()[0]),
                  xytext=(8, 14), textcoords="offset points",
                  fontsize=20, color=TINTA)

    passo = 6
    eixo.set_xticks(x[::passo])
    eixo.set_xticklabels([rotulos[i] for i in range(0, janela, passo)], fontsize=20)
    eixo.set_ylabel("bilhões de quilogramas")
    # duas casas, e nao uma: a serie fica entre 1,05 e 1,31 bilhao, e com uma
    # casa as marcas 1,05 / 1,10 / 1,15 viram "1,1" tres vezes no eixo.
    eixo.yaxis.set_major_formatter(FuncFormatter(lambda v, _: _num("%.2f", v)))
    eixo.legend(loc="upper left", fontsize=22)
    eixo.grid(axis="y", color=SOMBRA, linewidth=1)
    eixo.set_axisbelow(True)
    _sem_moldura(eixo)

    fig.tight_layout()
    destino = os.path.join(IMG, "aula12-historico-previsao.png")
    fig.savefig(destino, facecolor=FUNDO)
    plt.close(fig)
    mape = float(np.mean(np.abs((y_te - previsto) / y_te)) * 100)
    print("%-44s MAPE de %s nos %d meses"
          % (os.path.basename(destino), _num("%.2f%%", mape), N_TESTE))


if __name__ == "__main__":
    figura_coeficiente_x_previsao()
    figura_colinearidade()
    figura_historico_previsao()

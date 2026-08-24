"""Gera as figuras da Aula 05 a partir dos CSVs trimestrais do SIDRA.

Tres figuras, cada uma sustentando um achado que a aula mede ao vivo:

1. `aula05-corte-temporal.png`. A serie de `abate_frangos` de 1998-T1 a 2026-T1
   com o corte de treino e teste marcado em 2024-T1. Sustenta o bloco da
   separacao por data: 105 trimestres treinam, 8 ficam reservados.

2. `aula05-historico-vs-previsao.png`. O zoom nos oito trimestres reservados,
   onde a previsao do modelo e a da baseline de coeficiente fixo aparecem contra
   o valor realizado. E a figura que a ART.4 pede como comunicacao visual do
   produto: historico contra previsao.

3. `aula05-janelas-modelo-vs-baseline.png`. O MAPE do modelo e o da baseline em
   doze cortes consecutivos, de 2021-T3 a 2024-T2. Sustenta o achado central da
   aula: na ultima janela isolada o modelo ganha da baseline por 0,10 ponto
   percentual, quase um empate, e ao repetir a medida em doze janelas o modelo
   vence em doze de doze, com media de 2,18% contra 3,14%. Uma janela nao
   decide; doze decidem.

Decisoes de forma, herdadas de `tools/graficos_aula04.py`:

- roxo #2e2640 como tinta, coral #ff4545 como destaque, verde #89cea5 como
  terceira serie, cinza medio #caced6 nos eixos.
- nenhum valor interpolado ou inventado: as figuras plotam os CSVs e as saidas
  do modelo ajustado sobre eles.
- tamanho de fonte calculado para a projecao, e a largura da figura faz parte
  dessa conta. Com dpi 160 e exibicao a 900px, um rotulo de N pontos chega a
  tela com N * 12,5 / largura_em_polegadas pixels. Nas 12 polegadas que o acervo
  usa desde a Aula 02, isso da quase exatamente N pixels, e por isso os tamanhos
  partem de 18, o piso de legibilidade que o tema fixa para texto de slide.
  Uma primeira versao destas figuras usava 16 polegadas de largura, e o mesmo
  rotulo de 17 pontos chegava a tela com 13px: a largura da figura encolhe a
  fonte tanto quanto o valor em pontos. A conta completa esta no cabecalho de
  `tools/graficos_aula04.py`.

Codificacao secundaria, e o motivo dela. A paleta institucional do segmento
Graduacao e fixa e nao pode ser trocada por conveniencia de grafico. Submetida
ao validador de paletas categoricas da skill `dataviz`, ela separa bem sob
daltonismo (o pior par adjacente da dE 14,0 em deuteranopia, acima do minimo de
8), mas o verde #89cea5 mede 1,79:1 de contraste contra o fundo branco, abaixo
do minimo de 3:1, e o validador exige relevo quando isso acontece. O relevo
adotado aqui e dupla codificacao: cada serie tem cor, estilo de traco (solido,
tracejado, pontilhado) e marcador (circulo, triangulo, quadrado) proprios, com
legenda sempre visivel. Nenhuma informacao da figura depende so da cor, que e o
que a regra protege. Rotulo direto na ponta da linha foi tentado e removido: com
as tres series a menos de 0,06 bilhao de kg de distancia no ultimo trimestre, os
tres rotulos se sobrepunham, e colisao de rotulo e defeito pior do que a
ausencia do rotulo.

Uso: python3 tools/graficos_aula05.py   (requer matplotlib, pandas, scikit-learn)
"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.preprocessing import StandardScaler

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TINTA = "#2e2640"
DESTAQUE = "#ff4545"
APOIO = "#89cea5"
SUAVE = "#caced6"
FUNDO = "#ffffff"

SERIES = ["abate_bovinos", "abate_suinos", "abate_frangos",
          "producao_ovos", "producao_leite"]
ALVO = "abate_frangos"
FEATURES = ["frangos_lag1", "frangos_lag4", "sen", "cos"]
N_TESTE = 8

plt.rcParams.update({
    "font.size": 18,
    "axes.edgecolor": SUAVE,
    "axes.labelcolor": TINTA,
    "text.color": TINTA,
    "xtick.color": TINTA,
    "ytick.color": TINTA,
    "figure.facecolor": FUNDO,
    "axes.facecolor": FUNDO,
})


def base_analitica():
    """Reconstroi a base analitica da Aula 04 a partir dos CSVs crus."""
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
    colunas = ["periodo", "trimestre"] + SERIES + FEATURES
    return base[colunas].dropna().reset_index(drop=True)


def ajustar(treino, teste):
    """Padroniza com fit so no treino, ajusta a regressao e preve nos dois."""
    escalador = StandardScaler().fit(treino[FEATURES].to_numpy(float))
    modelo = LinearRegression().fit(escalador.transform(treino[FEATURES].to_numpy(float)),
                                    treino[ALVO].to_numpy(float))
    return modelo.predict(escalador.transform(teste[FEATURES].to_numpy(float)))


def corte_temporal(base, destino):
    """A serie inteira, com a linha que separa treino de teste."""
    corte = len(base) - N_TESTE
    bi = 1e9   # bilhoes de quilogramas: o eixo cru traria 3.500.000.000
    fig, eixo = plt.subplots(figsize=(12, 4.6))

    x = np.arange(len(base))
    eixo.plot(x, base[ALVO] / bi, color=TINTA, linewidth=2)
    eixo.axvline(corte - 0.5, color=DESTAQUE, linewidth=2.5, linestyle="--")
    eixo.text(corte - 3, 1.05, "treino\n105 trimestres", ha="right", va="bottom",
              fontsize=19, color=TINTA)
    eixo.text(corte + 2, 1.05, "teste\n8 trimestres", ha="left", va="bottom",
              fontsize=19, color=DESTAQUE)
    rotulos = [i for i in range(len(base)) if base["periodo"].iloc[i].endswith("T1")
               and int(base["periodo"].iloc[i][:4]) % 6 == 0]
    eixo.set_xticks(rotulos)
    eixo.set_xticklabels([base["periodo"].iloc[i][:4] for i in rotulos], fontsize=19)
    eixo.set_ylabel("bilhões de kg", fontsize=19)
    eixo.set_xlim(-2, len(base) + 1)
    eixo.spines[["top", "right"]].set_visible(False)
    eixo.tick_params(labelsize=19)

    fig.tight_layout()
    fig.savefig(destino, dpi=160, facecolor=FUNDO)
    plt.close(fig)


def historico_vs_previsao(base, destino):
    """O zoom nos oito trimestres reservados: realizado, modelo e baseline."""
    corte = len(base) - N_TESTE
    treino, teste = base.iloc[:corte], base.iloc[corte:]
    previsto = ajustar(treino, teste)
    fator = float((treino[ALVO] / treino["frangos_lag4"]).mean())
    baseline = teste["frangos_lag4"].to_numpy(float) * fator

    bi = 1e9
    fig, eixo = plt.subplots(figsize=(12, 5.0))
    z = np.arange(N_TESTE)
    real = teste[ALVO].to_numpy(float) / bi
    eixo.plot(z, real, color=TINTA, linewidth=2.5, marker="o", markersize=10,
              label="realizado")
    eixo.plot(z, previsto / bi, color=DESTAQUE, linewidth=2.5, linestyle="--",
              marker="^", markersize=10, label="modelo, MAPE 1,60%")
    eixo.plot(z, baseline / bi, color=APOIO, linewidth=3, linestyle=":",
              marker="s", markersize=10, label="baseline, MAPE 1,69%")
    # o ano so aparece quando muda: repetir "2024" oito vezes colide os rotulos
    marcas, ano_anterior = [], None
    for periodo in teste["periodo"]:
        ano, tri = periodo[:4], periodo[-2:]
        marcas.append(tri if ano == ano_anterior else tri + "\n" + ano)
        ano_anterior = ano
    eixo.set_xticks(z)
    eixo.set_xticklabels(marcas, fontsize=19)
    eixo.set_xlim(-0.45, N_TESTE - 0.55)
    eixo.set_ylabel("bilhões de kg", fontsize=19)
    eixo.spines[["top", "right"]].set_visible(False)
    eixo.tick_params(labelsize=19)
    eixo.legend(fontsize=18, frameon=False, loc="upper left", handlelength=2.6,
                borderpad=0.2, labelspacing=0.35)

    fig.tight_layout()
    fig.savefig(destino, dpi=160, facecolor=FUNDO)
    plt.close(fig)
    return previsto, baseline, teste


def janelas(base, destino):
    """MAPE do modelo e da baseline em doze cortes consecutivos."""
    nomes, mod, bas = [], [], []
    for k in range(12, 0, -1):
        corte = len(base) - N_TESTE - k + 1
        treino, teste = base.iloc[:corte], base.iloc[corte:corte + N_TESTE]
        if len(teste) < N_TESTE:
            continue
        y = teste[ALVO].to_numpy(float)
        fator = float((treino[ALVO] / treino["frangos_lag4"]).mean())
        nomes.append(teste["periodo"].iloc[0])
        mod.append(mean_absolute_percentage_error(y, ajustar(treino, teste)) * 100)
        bas.append(mean_absolute_percentage_error(
            y, teste["frangos_lag4"].to_numpy(float) * fator) * 100)

    fig, eixo = plt.subplots(figsize=(12, 5.0))
    x = np.arange(len(nomes))
    eixo.plot(x, bas, color=APOIO, linewidth=3, linestyle=":", marker="s",
              markersize=10, label="baseline de coeficiente fixo")
    eixo.plot(x, mod, color=DESTAQUE, linewidth=2.5, marker="^", markersize=10,
              label="modelo de regressão")
    eixo.fill_between(x, mod, bas, color=SUAVE, alpha=0.45)
    eixo.annotate("na última janela\na diferença cai a 0,10 pp",
                  xy=(x[-1] - 0.08, (mod[-1] + bas[-1]) / 2), xytext=(x[-1] - 4.6, 1.12),
                  fontsize=18, color=TINTA, va="bottom",
                  arrowprops={"arrowstyle": "->", "color": TINTA, "linewidth": 1.6,
                              "connectionstyle": "arc3,rad=-0.15"})
    marcas, ano_anterior = [], None
    for nome in nomes:
        ano, tri = nome[:4], nome[-2:]
        marcas.append(tri if ano == ano_anterior else tri + "\n" + ano)
        ano_anterior = ano
    eixo.set_xticks(x)
    eixo.set_xticklabels(marcas, fontsize=18)
    eixo.set_xlim(-0.45, len(nomes) - 0.55)
    eixo.set_ylim(1.0, 4.4)
    eixo.set_ylabel("MAPE no teste (%)", fontsize=19)
    eixo.set_xlabel("primeiro trimestre da janela de teste", fontsize=18, labelpad=8)
    eixo.spines[["top", "right"]].set_visible(False)
    eixo.tick_params(labelsize=17)
    eixo.legend(fontsize=18, frameon=False, loc="upper right", handlelength=2.6,
                borderpad=0.2, labelspacing=0.35)

    fig.tight_layout()
    fig.savefig(destino, dpi=160, facecolor=FUNDO)
    plt.close(fig)
    return nomes, mod, bas


def main():
    base = base_analitica()
    saida = os.path.join(RAIZ, "assets", "img")
    corte_temporal(base, os.path.join(saida, "aula05-corte-temporal.png"))
    previsto, baseline, teste = historico_vs_previsao(
        base, os.path.join(saida, "aula05-historico-vs-previsao.png"))
    nomes, mod, bas = janelas(
        base, os.path.join(saida, "aula05-janelas-modelo-vs-baseline.png"))

    print("base analitica: %d linhas, %s a %s"
          % (len(base), base["periodo"].iloc[0], base["periodo"].iloc[-1]))
    y = teste[ALVO].to_numpy(float)
    print("teste: %s a %s" % (teste["periodo"].iloc[0], teste["periodo"].iloc[-1]))
    print("MAPE modelo   %.4f%%" % (mean_absolute_percentage_error(y, previsto) * 100))
    print("MAPE baseline %.4f%%" % (mean_absolute_percentage_error(y, baseline) * 100))
    print("janelas: modelo vence em %d de %d; media modelo %.2f%%, baseline %.2f%%"
          % (sum(1 for a, b in zip(mod, bas) if a < b), len(mod),
             float(np.mean(mod)), float(np.mean(bas))))
    print("margem por janela: min %.2f pp, max %.2f pp"
          % (min(b - a for a, b in zip(mod, bas)), max(b - a for a, b in zip(mod, bas))))
    print("figuras gravadas em assets/img/")


if __name__ == "__main__":
    main()

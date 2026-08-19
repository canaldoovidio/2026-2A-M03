"""Gera as figuras da Aula 04 a partir dos CSVs trimestrais do SIDRA.

Duas figuras, cada uma sustentando um achado que a aula mede ao vivo:

1. `aula04-correlacao-nivel-vs-diferenca.png`. A correlacao de Pearson entre
   `abate_frangos` e as outras quatro series fica entre +0,92 e +0,97 quando
   calculada sobre o nivel, e desaba para a faixa de -0,04 a +0,20 quando
   calculada sobre a primeira diferenca. As cinco series crescem no tempo, e a
   tendencia comum e quem produz a correlacao alta. E o conteudo do bloco de
   selecao de caracteristica, medido, nao afirmado.

2. `aula04-normalidade-frangos.png`. Histograma de `abate_frangos` com a normal
   de mesma media e mesmo desvio sobreposta, mais o grafico quantil-quantil. O
   Shapiro-Wilk rejeita normalidade (W=0,9462, p=0,00014). Sustenta a amarracao
   com a ART.5, que pede teste de hipotese sobre distribuicao normal.

Decisoes de forma, herdadas de `tools/graficos_aula02.py`:

- roxo #2e2640 como tinta, coral #ff4545 so como destaque, cinza medio #caced6
  nos eixos. A paleta do segmento Graduacao nao tem cinco cores categoricas
  distinguiveis entre si, entao nenhuma figura aqui codifica serie por cor:
  as series aparecem como rotulo no eixo, e a cor separa apenas as duas
  medidas que estao sendo contrastadas.
- nenhum valor interpolado ou inventado: as duas figuras plotam o que os CSVs
  contem.
- tamanho de fonte calculado para a projecao, nao para a leitura na tela do
  autor. As figuras sao salvas a dpi 160 e exibidas no deck com max-width
  entre 620px e 900px, o que impoe um fator de reducao de cerca de 0,5. Um
  rotulo em fontsize 9,5 chegaria a tela final com cerca de 11px, abaixo do
  piso de 18px que o tema fixa para texto de slide.

  A conta, para quem for mexer: com dpi 160, um rotulo de N pontos ocupa
  N * 160/72 pixels na imagem salva, e chega a tela multiplicado pela razao
  entre a largura de exibicao e a largura da imagem. Nas duas figuras aqui
  (1920px salvos, exibidos entre 860px e 900px), essa cadeia da quase
  exatamente N pixels na tela. Por isso os tamanhos partem de 18: e o piso do
  tema, lido diretamente em pontos.

Uso: python3 tools/graficos_aula04.py   (requer matplotlib, pandas, scipy)
"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TINTA = "#2e2640"
DESTAQUE = "#ff4545"
SUAVE = "#caced6"
FUNDO = "#ffffff"

SERIES = ["abate_bovinos", "abate_suinos", "abate_frangos",
          "producao_ovos", "producao_leite"]
ALVO = "abate_frangos"

base = None
for nome in SERIES:
    caminho = os.path.join(RAIZ, "dados", nome + ".csv")
    coluna = pd.read_csv(caminho)[["periodo", "valor"]].rename(columns={"valor": nome})
    base = coluna if base is None else base.merge(coluna, on="periodo", how="inner")


def _limpar(ax):
    for lado in ("top", "right"):
        ax.spines[lado].set_visible(False)
    for lado in ("left", "bottom"):
        ax.spines[lado].set_color(SUAVE)
        ax.spines[lado].set_linewidth(0.8)
    ax.tick_params(colors=TINTA, labelsize=18, length=4, width=1.0, color=SUAVE)
    ax.set_axisbelow(True)


# ---------------------------------------------------------------- figura 1
outras = [s for s in SERIES if s != ALVO]
diferencas = base[SERIES].diff().dropna()
r_nivel = [base[ALVO].corr(base[s]) for s in outras]
r_diff = [diferencas[ALVO].corr(diferencas[s]) for s in outras]

fig, ax = plt.subplots(figsize=(12, 5.6), dpi=160)
fig.patch.set_facecolor(FUNDO)
y = np.arange(len(outras))
altura = 0.36
ax.barh(y + altura / 2, r_nivel, height=altura, color=TINTA,
        label="sobre o nível da série", zorder=3)
ax.barh(y - altura / 2, r_diff, height=altura, color=DESTAQUE,
        label="sobre a primeira diferença", zorder=3)


def _rotular(posicoes, valores, cor):
    """Rotulo sempre do lado de fora da barra, inclusive quando ela e negativa."""
    for posicao, valor in zip(posicoes, valores):
        fora = valor + 0.018 if valor >= 0 else valor - 0.018
        alinhamento = "left" if valor >= 0 else "right"
        rotulo = ("%+.2f" % valor).replace(".", ",")
        ax.text(fora, posicao, rotulo, va="center", ha=alinhamento,
                color=cor, fontsize=19)


_rotular(y + altura / 2, r_nivel, TINTA)
_rotular(y - altura / 2, r_diff, DESTAQUE)
ax.set_yticks(y)
ax.set_yticklabels(outras)
ax.set_ylim(-0.75, len(outras) - 0.25)
ax.set_xlim(-0.22, 1.1)
ax.axvline(0, color=SUAVE, linewidth=0.8)
ax.grid(axis="x", color=SUAVE, linewidth=0.6, alpha=0.6)
_limpar(ax)
ax.set_title("Correlação de Pearson com abate_frangos:\n"
             "+0,93 a +0,97 em nível, -0,04 a +0,20 em primeira diferença",
             color=TINTA, fontsize=20, loc="left", pad=16)
ax.legend(frameon=False, loc="lower center", bbox_to_anchor=(0.5, -0.28),
          ncol=2, fontsize=18, labelcolor=TINTA)
fig.tight_layout()
fig.subplots_adjust(bottom=0.26)
destino = os.path.join(RAIZ, "assets", "img", "aula04-correlacao-nivel-vs-diferenca.png")
fig.savefig(destino, facecolor=FUNDO)
print("gravado:", destino)
for nome, rn, rd in zip(outras, r_nivel, r_diff):
    print("  %-16s nivel %+0.4f   diferenca %+0.4f" % (nome, rn, rd))

# ---------------------------------------------------------------- figura 2
valores = base[ALVO].to_numpy()
W, p = stats.shapiro(valores)

fig, (esq, dir_) = plt.subplots(1, 2, figsize=(12, 5.0), dpi=160)
fig.patch.set_facecolor(FUNDO)

esq.hist(valores / 1e9, bins=14, color=TINTA, edgecolor=FUNDO, linewidth=1.0, zorder=3)
grade = np.linspace(valores.min(), valores.max(), 300)
densidade = stats.norm.pdf(grade, valores.mean(), valores.std(ddof=1))
largura = (valores.max() - valores.min()) / 14
esq.plot(grade / 1e9, densidade * len(valores) * largura,
         color=DESTAQUE, linewidth=2, zorder=4)
esq.set_xlabel("bilhões de kg de carcaça por trimestre", color=TINTA, fontsize=18)
esq.set_ylabel("trimestres", color=TINTA, fontsize=18)
esq.grid(axis="y", color=SUAVE, linewidth=0.6, alpha=0.6)
_limpar(esq)
esq.set_title("Observado e a normal",
              color=TINTA, fontsize=19, loc="left", pad=12)

(osm, osr), (inclinacao, intercepto, _) = stats.probplot(valores, dist="norm")
dir_.scatter(osm, osr / 1e9, s=22, color=TINTA, zorder=3)
dir_.plot(osm, (inclinacao * osm + intercepto) / 1e9,
          color=DESTAQUE, linewidth=1.6, zorder=4)
dir_.set_xlabel("quantis teóricos da normal", color=TINTA, fontsize=18)
dir_.set_ylabel("quantis observados (bi kg)", color=TINTA, fontsize=18)
dir_.grid(color=SUAVE, linewidth=0.6, alpha=0.6)
_limpar(dir_)
dir_.set_title("Quantil-quantil",
               color=TINTA, fontsize=19, loc="left", pad=12)

fig.suptitle(("abate_frangos, 117 trimestres: Shapiro-Wilk W=%.4f, p=%.5f"
              % (W, p)).replace(".", ","),
             color=TINTA, fontsize=21, x=0.010, ha="left", y=0.99)
fig.tight_layout(rect=(0, 0, 1, 0.93), w_pad=4.0)
destino = os.path.join(RAIZ, "assets", "img", "aula04-normalidade-frangos.png")
fig.savefig(destino, facecolor=FUNDO)
print("gravado:", destino)
print("  Shapiro-Wilk W=%.4f p=%.6f" % (W, p))

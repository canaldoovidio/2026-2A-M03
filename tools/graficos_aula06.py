"""Gera as figuras da Aula 06 a partir dos CSVs trimestrais do SIDRA.

Duas figuras, cada uma sustentando um achado que a aula mede ao vivo sobre o
contraste entre agrupar niveis e agrupar participacao no ano:

1. `aula06-epocas-vs-trimestres.png`. Dois paineis lado a lado sobre o mesmo
   eixo de tempo (1997-T1 a 2026-T1), com `abate_frangos` ao fundo em cinza
   claro nos dois. No painel esquerdo, o ato 1: agrupar os niveis padronizados
   das cinco series com K=4 devolve quatro epocas contiguas no tempo (silhueta
   0,4795, concordancia de 26,5% com o trimestre do calendario, proxima do
   acaso de 25%). No painel direito, o ato 2: agrupar a participacao de cada
   trimestre no total do proprio ano, tambem com K=4, devolve o trimestre do
   calendario (silhueta 0,2853, concordancia de 98,3%, com 2008-T2 e 2008-T4
   como as duas excecoes). E a figura que sustenta o achado central da aula: a
   silhueta premia o agrupamento menos util.

2. `aula06-perfil-sazonal.png`. O perfil sazonal medio das cinco series (a
   participacao media de cada trimestre no total do ano), em barras agrupadas.
   Sustenta o achado complementar: leite tem pico no T4 enquanto as tres
   carnes tem pico no T3, e a amplitude sazonal do leite (3,85 p.p.) e mais
   que o triplo da do frango (1,10 p.p.).

Decisoes de forma, herdadas de `tools/graficos_aula05.py`:

- roxo #2e2640 como tinta, coral #ff4545 como destaque, verde #89cea5 como
  terceira serie, cinza medio #caced6 nos eixos.
- nenhum valor interpolado ou inventado: as figuras plotam os CSVs e o
  agrupamento K-means ajustado sobre eles, com a mesma logica de juncao e de
  participacao no ano de `tools/tests/test_clusters_aula06.py` (Task 1),
  reimplementada aqui de proposito em vez de importada: se as duas
  implementacoes divergirem, o acervo descobre.
- tamanho de fonte calculado para a projecao, e a largura da figura faz parte
  dessa conta. Com dpi 160 e exibicao a 900px, um rotulo de N pontos chega a
  tela com N * 12,5 / largura_em_polegadas pixels. Nas 12 polegadas que o
  acervo usa desde a Aula 02, isso da quase exatamente N pixels, e por isso os
  tamanhos partem de 18, o piso de legibilidade que o tema fixa para texto de
  slide. A conta completa esta no cabecalho de `tools/graficos_aula04.py`.

Decisao de representacao da Figura 1, painel direito. Os clusters do ato 2 se
alternam a cada trimestre ao longo de 29 anos (116 pontos): uma linha ou
marcador grosso conectando os pontos na ordem do tempo produziria um
zigue-zague ilegivel a essa escala, e uma faixa de fundo colorida por ponto
(testada e descartada) produz um efeito de codigo de barras que compete com os
proprios pontos. A representacao escolhida e marcador pequeno colorido pelo
cluster, sobre a serie de frangos ao fundo em cinza claro, sem linha
conectando os marcadores entre si: a serie cinza fornece o contexto de nivel,
a cor do marcador fornece o cluster, e nenhuma linha grossa precisa percorrer
116 trocas de cor. E o mesmo principio do painel esquerdo, so que com marcador
menor, porque a troca de cor e mais frequente.

Uso: python3 tools/graficos_aula06.py   (requer matplotlib, pandas,
numpy, scikit-learn)
"""
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TINTA = "#2e2640"
DESTAQUE = "#ff4545"
APOIO = "#89cea5"
SUAVE = "#caced6"
FUNDO = "#ffffff"

SERIES = ["abate_bovinos", "abate_suinos", "abate_frangos",
          "producao_ovos", "producao_leite"]
ROTULO_SERIE = {
    "abate_bovinos": "abate de\nbovinos",
    "abate_suinos": "abate de\nsuínos",
    "abate_frangos": "abate de\nfrangos",
    "producao_ovos": "produção de\novos",
    "producao_leite": "produção de\nleite",
}
ALVO = "abate_frangos"
K = 4
SEMENTE = 42

# paleta categorica dos quatro clusters, na ordem do trimestre majoritario
# de cada um (1, 2, 3, 4). Reaproveita tinta, destaque e apoio da Aula 05 mais
# um quarto tom (dourado) que nao colide com nenhum dos tres sob deuteranopia.
COR_TRIMESTRE = {1: TINTA, 2: APOIO, 3: DESTAQUE, 4: "#c9a227"}

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
    """Interseccao das cinco series por periodo, ordenada no tempo.

    Interseccao, e nao uniao: `producao_ovos` comeca em 1987-T1 e as outras
    quatro em 1997-T1. Mesma regra de juncao de `test_clusters_aula06.py`.
    """
    tabelas = {}
    for nome in SERIES:
        df = pd.read_csv(os.path.join(RAIZ, "dados", nome + ".csv"))
        tabelas[nome] = dict(zip(df["periodo"], df["valor"].astype(float)))
    periodos = sorted(set.intersection(*[set(t) for t in tabelas.values()]))
    matriz = np.array([[tabelas[s][p] for s in SERIES] for p in periodos])
    anos = np.array([int(p[:4]) for p in periodos])
    tris = np.array([int(p[-1]) for p in periodos])
    return {"periodos": periodos, "X": matriz, "anos": anos, "tris": tris}


def kmeans_rotulos(matriz):
    """Padroniza, agrupa com K=4 e devolve os rotulos alinhados ao trimestre.

    Os rotulos brutos do KMeans nao tem ordem semantica (o cluster "0" pode
    ser qualquer trimestre). Remapeia cada rotulo bruto para o trimestre do
    calendario que domina esse cluster, so para dar cor consistente as duas
    figuras: a metrica de concordancia usa a mesma regra de trimestre
    majoritario, sem depender desse remapeamento.
    """
    padronizada = StandardScaler().fit_transform(matriz)
    modelo = KMeans(n_clusters=K, n_init=50, random_state=SEMENTE).fit(padronizada)
    return modelo.labels_


def concordancia(rotulos, tris):
    """Fracao das linhas cobertas pelo trimestre majoritario de cada cluster."""
    acertos = 0
    for c in set(rotulos):
        do_cluster = tris[rotulos == c]
        acertos += max((do_cluster == t).sum() for t in (1, 2, 3, 4))
    return acertos / len(tris)


def trimestre_majoritario(rotulos, tris):
    """Mapa rotulo bruto -> trimestre do calendario que domina esse cluster."""
    mapa = {}
    for c in set(rotulos):
        do_cluster = tris[rotulos == c]
        mapa[c] = max((1, 2, 3, 4), key=lambda t: (do_cluster == t).sum())
    return mapa


def participacao_no_ano(base):
    """Cada valor vira a fracao que ele representa no total do proprio ano.

    So entram anos com os quatro trimestres medidos: 2026 tem so o T1, e um
    ano incompleto faria o unico trimestre valer 100% do ano.
    """
    completos = {a for a in set(base["anos"].tolist()) if (base["anos"] == a).sum() == 4}
    mascara = np.array([a in completos for a in base["anos"]])
    X = base["X"][mascara]
    anos = base["anos"][mascara]
    saida = np.empty_like(X)
    for a in completos:
        linhas = anos == a
        saida[linhas] = X[linhas] / X[linhas].sum(axis=0)
    periodos = [p for p, m in zip(base["periodos"], mascara) if m]
    return saida, anos, base["tris"][mascara], periodos


def epocas_vs_trimestres(base, destino):
    """Figura 1: dois paineis, ato 1 (niveis) contra ato 2 (participacao)."""
    bi = 1e9
    x = np.arange(len(base["periodos"]))
    frangos = base["X"][:, SERIES.index(ALVO)] / bi

    rotulos1 = kmeans_rotulos(base["X"])
    mapa1 = trimestre_majoritario(rotulos1, base["tris"])
    cores1 = [COR_TRIMESTRE[mapa1[r]] for r in rotulos1]

    X2, anos2, tris2, periodos2 = participacao_no_ano(base)
    rotulos2 = kmeans_rotulos(X2)
    mapa2 = trimestre_majoritario(rotulos2, tris2)
    idx2 = [base["periodos"].index(p) for p in periodos2]
    cores2 = [COR_TRIMESTRE[mapa2[r]] for r in rotulos2]

    fig, (esq, dire) = plt.subplots(1, 2, figsize=(12, 5.2), sharey=True)

    for eixo in (esq, dire):
        eixo.plot(x, frangos, color=SUAVE, linewidth=2, zorder=1)
        eixo.spines[["top", "right"]].set_visible(False)
        eixo.tick_params(labelsize=18)

    esq.scatter(x, frangos, c=cores1, s=32, zorder=2, linewidths=0)
    esq.set_title("Agrupando os níveis:\nquatro épocas", fontsize=19, pad=10)
    esq.set_ylabel("bilhões de kg (abate de frangos)", fontsize=18)

    # marcadores pequenos sobre a serie em cinza claro: com 116 trocas de cor
    # em 29 anos, uma linha ou marcador grosso conectando os pontos vira
    # borrao. O marcador pequeno preserva a leitura do nivel (a linha cinza)
    # e da cor do cluster (o marcador), sem tentar unir os 116 pontos.
    dire.scatter(x[idx2], frangos[idx2], c=cores2, s=20, zorder=2, linewidths=0)
    dire.set_title("Agrupando a participação no ano:\nquatro trimestres",
                    fontsize=19, pad=10)

    rotulos_x = [i for i in range(len(base["periodos"]))
                 if base["periodos"][i].endswith("T1")
                 and int(base["periodos"][i][:4]) % 6 == 0]
    for eixo in (esq, dire):
        eixo.set_xticks(rotulos_x)
        eixo.set_xticklabels([base["periodos"][i][:4] for i in rotulos_x], fontsize=18)
        eixo.set_xlim(-2, len(base["periodos"]) + 1)

    manejadores = [plt.Line2D([0], [0], marker="o", linestyle="", markersize=10,
                               markerfacecolor=COR_TRIMESTRE[t], markeredgewidth=0,
                               label="T%d" % t) for t in (1, 2, 3, 4)]
    fig.legend(handles=manejadores, ncol=4, fontsize=18, frameon=False,
               loc="lower center", bbox_to_anchor=(0.5, -0.02),
               handletextpad=0.5, columnspacing=1.4)

    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(destino, dpi=160, facecolor=FUNDO)
    plt.close(fig)
    return rotulos1, rotulos2, tris2, periodos2


def perfil_sazonal(base, destino):
    """Figura 2: participacao media de cada trimestre, por serie, em barras."""
    X, anos, tris, _ = participacao_no_ano(base)
    medias = np.array([X[tris == t].mean(axis=0) for t in (1, 2, 3, 4)]) * 100

    fig, eixo = plt.subplots(figsize=(12, 5.4))
    largura = 0.19
    posicoes_serie = np.arange(len(SERIES))
    # T3 e T4 aqui NAO usam a cor de destaque (coral): ela fica reservada para
    # marcar so a barra do T4 do leite. Se o T3 (ou o T4 das outras series)
    # usasse coral, a barra destacada colaria visualmente na vizinha da mesma
    # cor e o destaque desapareceria.
    cores_tri = [TINTA, APOIO, "#8b8394", "#c9a227"]

    for i, t in enumerate((1, 2, 3, 4)):
        deslocamento = (i - 1.5) * largura
        cores_barra = list(cores_tri[i] for _ in SERIES)
        i_leite = SERIES.index("producao_leite")
        if t == 4:
            cores_barra[i_leite] = DESTAQUE
        eixo.bar(posicoes_serie + deslocamento, medias[i], width=largura,
                 color=cores_barra, label="T%d" % t, zorder=2)

    eixo.axhline(25.0, color=TINTA, linewidth=1.6, linestyle="--", zorder=1)
    eixo.text(len(SERIES) - 0.55, 25.6, "25%: trimestre sem sazonalidade",
              fontsize=18, color=TINTA, ha="right", va="bottom", zorder=3,
              bbox={"facecolor": FUNDO, "edgecolor": "none", "pad": 2})

    eixo.set_xticks(posicoes_serie)
    eixo.set_xticklabels([ROTULO_SERIE[s] for s in SERIES], fontsize=18)
    eixo.set_ylabel("participação média no ano (%)", fontsize=18)
    eixo.spines[["top", "right"]].set_visible(False)
    eixo.tick_params(labelsize=18)
    eixo.set_ylim(0, 32)

    manejadores = [plt.Rectangle((0, 0), 1, 1, color=cores_tri[i]) for i in range(4)]
    eixo.legend(manejadores, ["T1", "T2", "T3", "T4"], fontsize=18, frameon=False,
                loc="upper left", ncol=4, handletextpad=0.5, columnspacing=1.2)

    fig.tight_layout()
    fig.savefig(destino, dpi=160, facecolor=FUNDO)
    plt.close(fig)
    return medias


def main():
    base = base_analitica()
    saida = os.path.join(RAIZ, "assets", "img")

    rotulos1, rotulos2, tris2, periodos2 = epocas_vs_trimestres(
        base, os.path.join(saida, "aula06-epocas-vs-trimestres.png"))
    medias = perfil_sazonal(base, os.path.join(saida, "aula06-perfil-sazonal.png"))

    print("base (ato 1): %d linhas, %s a %s"
          % (len(base["periodos"]), base["periodos"][0], base["periodos"][-1]))
    padronizada1 = StandardScaler().fit_transform(base["X"])
    from sklearn.metrics import silhouette_score
    silhueta1 = silhouette_score(padronizada1, rotulos1)
    conc1 = concordancia(rotulos1, base["tris"])
    print("ato 1: silhueta %.4f, concordância %.1f%%" % (silhueta1, conc1 * 100))

    print("base (ato 2): %d linhas, %s a %s" % (len(periodos2), periodos2[0], periodos2[-1]))
    X2, _, _, _ = participacao_no_ano(base)
    padronizada2 = StandardScaler().fit_transform(X2)
    silhueta2 = silhouette_score(padronizada2, rotulos2)
    conc2 = concordancia(rotulos2, tris2)
    print("ato 2: silhueta %.4f, concordância %.1f%%" % (silhueta2, conc2 * 100))

    mapa2 = trimestre_majoritario(rotulos2, tris2)
    fora = [p for p, r, t in zip(periodos2, rotulos2, tris2) if mapa2[r] != t]
    print("exceções do ato 2: %s" % fora)

    i_leite = SERIES.index("producao_leite")
    i_frango = SERIES.index("abate_frangos")
    amplitude_leite = medias[:, i_leite].max() - medias[:, i_leite].min()
    amplitude_frango = medias[:, i_frango].max() - medias[:, i_frango].min()
    print("pico do leite: T%d (%.2f%%)" % (int(np.argmax(medias[:, i_leite])) + 1,
                                            medias[:, i_leite].max()))
    print("amplitude leite %.2f p.p., amplitude frango %.2f p.p."
          % (amplitude_leite, amplitude_frango))
    print("figuras gravadas em assets/img/")


if __name__ == "__main__":
    main()

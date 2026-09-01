"""Gera as figuras da Aula 06 a partir dos CSVs trimestrais do SIDRA.

Duas figuras, cada uma sustentando um achado que a aula mede ao vivo sobre o
contraste entre agrupar niveis e agrupar participacao no ano:

1. `aula06-epocas-vs-trimestres.png`. Dois paineis lado a lado sobre o mesmo
   eixo de tempo (1997-T1 a 2026-T1), com `abate_frangos` ao fundo em cinza
   claro nos dois, cada um com a sua propria legenda porque os dois agrupam
   coisas diferentes:
   - Esquerda, o ato 1: agrupar os niveis padronizados das cinco series com
     K=4 devolve quatro epocas contiguas no tempo (silhueta 0,4795,
     concordancia de apenas 26,5% com o trimestre do calendario, proxima do
     acaso de 25%). Os clusters do ato 1 NAO sao trimestres -- e o proprio
     achado da aula --, entao a cor aqui nao pode usar rotulo T1 a T4: usa uma
     rampa sequencial de roxo (claro para escuro, uma epoca por degrau) e uma
     legenda com os quatro intervalos de tempo.
   - Direita, o ato 2: agrupar a participacao de cada trimestre no total do
     proprio ano, tambem com K=4, devolve o trimestre do calendario (silhueta
     0,2853, concordancia de 98,3%, com 2008-T2 e 2008-T4 como as duas
     excecoes). Aqui a cor E o trimestre, entao usa quatro matizes categoricas
     com legenda T1 a T4.
   E a figura que sustenta o achado central da aula: a silhueta premia o
   agrupamento menos util. A escolha de rampa monocromatica a esquerda contra
   matizes categoricas a direita tambem comunica sozinha que um agrupamento e
   ordenado no tempo e o outro nao.

2. `aula06-perfil-sazonal.png`. O desvio da participacao media de cada
   trimestre em relacao aos 25% que um trimestre sem sazonalidade nenhuma
   teria, em pontos percentuais, por serie. Sustenta o achado complementar:
   leite tem pico no T4 enquanto as tres carnes tem pico no T3, e a amplitude
   sazonal do leite (3,85 p.p.) e mais que o triplo da do frango (1,10 p.p.).
   Plotar o desvio em vez do nivel bruto (que fica todo entre 23% e 27%, com
   as cinco series quase identicas a olho nu) e o que faz esse achado
   aparecer: com o desvio, o leite passa a ter a barra mais alta e a mais
   baixa do grafico, e o frango fica visivelmente achatado perto de zero.

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

Paletas usadas e a checagem de contraste/daltonismo, no mesmo formato que
`tools/graficos_aula05.py` documenta para a paleta dele.

Paleta categorica dos quatro trimestres (T1 a T4), usada no painel direito da
Figura 1 e nos quatro grupos de barra da Figura 2: roxo #2e2640 (T1, a mesma
tinta do resto do acervo), verde #89cea5 (T2, a mesma terceira serie da Aula
05), azul #3d6cb3 (T3) e terracota #a05a2c (T4). Coral #ff4545 fica de fora
dessa paleta de proposito: ele marca so a barra do T4 do leite na Figura 2,
nunca uma categoria comum, porque usa-lo como uma entre quatro cores
equivalentes faria a barra destacada colar visualmente na vizinha da mesma cor
e o destaque desapareceria (foi exatamente o defeito da primeira versao desta
figura, corrigido nesta rodada). Submetida ao validador de paletas categoricas
da skill `dataviz` (`node scripts/validate_palette.js
"#2e2640,#89cea5,#3d6cb3,#a05a2c" --mode light --surface "#ffffff" --pairs
all`), a paleta separa bem sob daltonismo considerando TODOS os pares, nao so
os adjacentes: o pior par mede dE 20,2 sob protanopia (acima do minimo de 8) e
dE 22,7 sob visao normal (acima do minimo de 15). O validador tambem reprova
dois testes pensados para paletas totalmente livres (faixa de luminosidade e
piso de croma), porque #2e2640 e #89cea5 sao cores fixas do brandbook, nao
escolhas livres desta figura -- a mesma reprovacao aconteceria com a paleta de
tres cores ja publicada em `tools/graficos_aula05.py`, que usa as mesmas duas
cores e nunca foi cobrada por isso. O aviso que sobra, esse sim real: #89cea5
mede 1,84:1 de contraste contra o fundo branco, abaixo do minimo de 3:1 (o
mesmo numero que a Aula 05 ja documentou para a mesma cor), e por isso nenhuma
figura aqui depende so da cor do trimestre -- toda barra e todo marcador tem a
identidade reforcada por rotulo direto (legenda T1 a T4, nome da serie no
eixo, ou intervalo de datas).

Rampa sequencial usada no painel esquerdo da Figura 1, uma unica matiz de roxo
do claro ao escuro (`#b0abba, #847e91, #584f68, #2e2640`, essa ultima a mesma
tinta oficial): passa nos quatro testes do validador em modo ordinal
(`--ordinal`) -- luminosidade monotona, degrau minimo de 0,06 entre vizinhos,
2,24:1 de contraste no degrau mais claro (acima do piso de 2:1) e variacao de
matiz de so 4 graus. Por variar so em luminosidade dentro de uma unica matiz,
essa rampa nao depende de discriminacao de cor para ser lida e e segura sob
qualquer forma de daltonismo por construcao. E por isso que o painel esquerdo
usa rampa e nao quatro matizes categoricas: a propria forma da paleta ja diz
que ali o que importa e a ordem no tempo, nao a identidade de uma categoria.

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
I_LEITE = SERIES.index("producao_leite")
K = 4
SEMENTE = 42

# paleta categorica dos quatro trimestres do calendario (ato 2 e Figura 2).
# Coral fica de fora de proposito: ver docstring do modulo.
COR_TRIMESTRE = {1: TINTA, 2: APOIO, 3: "#3d6cb3", 4: "#a05a2c"}

# rampa sequencial (claro -> escuro) para os quatro clusters do ato 1, que NAO
# tem identidade de trimestre: a ordem e temporal, do cluster mais antigo ao
# mais recente. Ver docstring do modulo para a validacao desta rampa.
RAMPA_EPOCA = ["#b0abba", "#847e91", "#584f68", "#2e2640"]

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
    """Padroniza e agrupa com K=4. Os rotulos brutos nao tem ordem semantica."""
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
    """Mapa rotulo bruto -> trimestre do calendario que domina esse cluster.

    So faz sentido para o ato 2, onde a concordancia e alta (98,3%) e o
    trimestre majoritario e de fato a identidade do cluster. Usar isso no ato
    1 (concordancia de 26,5%, proxima do acaso) coloriria as epocas por ruido
    e rotularia como trimestre algo que a aula prova que nao e.
    """
    mapa = {}
    for c in set(rotulos):
        do_cluster = tris[rotulos == c]
        mapa[c] = max((1, 2, 3, 4), key=lambda t: (do_cluster == t).sum())
    return mapa


def ordem_temporal(rotulos):
    """Ordena os rotulos brutos do ato 1 pela posicao media no tempo.

    O ato 1 agrupa NIVEIS de uma serie crescente: a posicao media de cada
    cluster ao longo do eixo de tempo e o proprio criterio de ordem, da epoca
    mais antiga para a mais recente. E o que da sentido a rampa sequencial:
    o cluster de indice 0 aqui e sempre o mais antigo, nao um rotulo
    arbitrario do KMeans.
    """
    return sorted(set(rotulos), key=lambda c: np.mean(np.where(rotulos == c)[0]))


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
    """Figura 1: dois paineis, ato 1 (niveis) contra ato 2 (participacao).

    Os dois paineis tem legenda propria: o esquerdo agrupa epocas sem
    identidade de trimestre (rampa sequencial + intervalos de tempo), o
    direito agrupa trimestres de verdade (cores categoricas + T1 a T4).
    """
    bi = 1e9
    x = np.arange(len(base["periodos"]))
    frangos = base["X"][:, SERIES.index(ALVO)] / bi

    rotulos1 = kmeans_rotulos(base["X"])
    ordem1 = ordem_temporal(rotulos1)
    cor_por_cluster1 = {c: RAMPA_EPOCA[i] for i, c in enumerate(ordem1)}
    cores1 = [cor_por_cluster1[r] for r in rotulos1]
    intervalos1 = []
    for c in ordem1:
        idx = np.where(rotulos1 == c)[0]
        intervalos1.append("%s a %s" % (base["periodos"][idx.min()], base["periodos"][idx.max()]))

    X2, anos2, tris2, periodos2 = participacao_no_ano(base)
    rotulos2 = kmeans_rotulos(X2)
    mapa2 = trimestre_majoritario(rotulos2, tris2)
    idx2 = [base["periodos"].index(p) for p in periodos2]
    cores2 = [COR_TRIMESTRE[mapa2[r]] for r in rotulos2]

    fig, (esq, dire) = plt.subplots(1, 2, figsize=(12, 5.3), sharey=True)

    for eixo in (esq, dire):
        eixo.plot(x, frangos, color=SUAVE, linewidth=2, zorder=1)
        eixo.spines[["top", "right"]].set_visible(False)
        eixo.tick_params(labelsize=18)

    esq.scatter(x, frangos, c=cores1, s=32, zorder=2, linewidths=0)
    esq.set_title("Agrupando os níveis:\nquatro épocas", fontsize=19, pad=10)
    esq.set_ylabel("bilhões de kg\n(abate de frangos)", fontsize=18)

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

    manejadores_esq = [plt.Line2D([0], [0], marker="o", linestyle="", markersize=10,
                                   markerfacecolor=RAMPA_EPOCA[i], markeredgewidth=0,
                                   label=intervalos1[i]) for i in range(4)]
    esq.legend(handles=manejadores_esq, loc="upper center", bbox_to_anchor=(0.5, -0.17),
               ncol=2, fontsize=18, frameon=False, handletextpad=0.4,
               columnspacing=1.0, labelspacing=0.5)

    manejadores_dire = [plt.Line2D([0], [0], marker="o", linestyle="", markersize=10,
                                    markerfacecolor=COR_TRIMESTRE[t], markeredgewidth=0,
                                    label="T%d" % t) for t in (1, 2, 3, 4)]
    dire.legend(handles=manejadores_dire, loc="upper center", bbox_to_anchor=(0.5, -0.16),
                ncol=4, fontsize=18, frameon=False, handletextpad=0.5, columnspacing=1.4)

    # bbox_inches="tight" recorta a figura pela extensao real do que foi
    # desenhado (titulos, eixos e as duas legendas, que ficam fora da area do
    # eixo por causa do bbox_to_anchor negativo) em vez de reservar uma faixa
    # fixa de rodape via `rect` que sobra vazia quando a legenda cabe em menos
    # espaco do que o reservado. Ver docstring do modulo.
    fig.tight_layout()
    fig.savefig(destino, dpi=160, facecolor=FUNDO, bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    return rotulos1, rotulos2, tris2, periodos2


def perfil_sazonal(base, destino):
    """Figura 2: desvio da participacao de cada trimestre em relacao a 25%.

    25% e a participacao que um trimestre teria se a serie nao tivesse
    sazonalidade nenhuma (um quarto do ano, igual para os quatro). Plotar o
    desvio em vez do nivel bruto reexpressa os dados em torno dessa mesma
    linha de base (nao e truncar eixo: a linha de 25% ja estava desenhada na
    primeira versao da figura) e e o que faz a diferenca de amplitude entre
    leite e frango aparecer: em nivel bruto as cinco series ficam todas entre
    23% e 27%, visualmente identicas.
    """
    X, anos, tris, _ = participacao_no_ano(base)
    medias = np.array([X[tris == t].mean(axis=0) for t in (1, 2, 3, 4)]) * 100
    desvio = medias - 25.0

    fig, eixo = plt.subplots(figsize=(12, 5.6))
    largura = 0.19
    posicoes_serie = np.arange(len(SERIES))
    # T1-T4 usam a paleta categorica de trimestre (sem coral: ver docstring do
    # modulo). Coral marca so a barra do T4 do leite.
    cores_tri = [COR_TRIMESTRE[t] for t in (1, 2, 3, 4)]

    for i, t in enumerate((1, 2, 3, 4)):
        deslocamento = (i - 1.5) * largura
        cores_barra = list(cores_tri[i] for _ in SERIES)
        if t == 4:
            cores_barra[I_LEITE] = DESTAQUE
        eixo.bar(posicoes_serie + deslocamento, desvio[i], width=largura,
                 color=cores_barra, label="T%d" % t, zorder=2)

    eixo.axhline(0.0, color=TINTA, linewidth=1.6, zorder=1)
    eixo.text(len(SERIES) - 0.55, desvio.max() + 0.35,
              "0 p.p.: trimestre sem sazonalidade", fontsize=18, color=TINTA,
              ha="right", va="bottom", zorder=3,
              bbox={"facecolor": FUNDO, "edgecolor": "none", "pad": 2})

    eixo.set_xticks(posicoes_serie)
    eixo.set_xticklabels([ROTULO_SERIE[s] for s in SERIES], fontsize=18)
    eixo.set_ylabel("desvio em relação a 25%\n(pontos percentuais)", fontsize=18)
    eixo.spines[["top", "right"]].set_visible(False)
    eixo.tick_params(labelsize=18)
    limite = max(abs(desvio.min()), abs(desvio.max())) + 0.9
    eixo.set_ylim(-limite, limite)

    manejadores = [plt.Rectangle((0, 0), 1, 1, color=cores_tri[i]) for i in range(4)]
    eixo.legend(manejadores, ["T1", "T2", "T3", "T4"], fontsize=18, frameon=False,
                loc="upper left", ncol=4, handletextpad=0.5, columnspacing=1.2)

    fig.tight_layout()
    fig.savefig(destino, dpi=160, facecolor=FUNDO)
    plt.close(fig)
    return medias, desvio


def main():
    base = base_analitica()
    saida = os.path.join(RAIZ, "assets", "img")

    rotulos1, rotulos2, tris2, periodos2 = epocas_vs_trimestres(
        base, os.path.join(saida, "aula06-epocas-vs-trimestres.png"))
    medias, desvio = perfil_sazonal(base, os.path.join(saida, "aula06-perfil-sazonal.png"))

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

    ordem1 = ordem_temporal(rotulos1)
    for i, c in enumerate(ordem1):
        idx = np.where(rotulos1 == c)[0]
        print("época %d: %s a %s" % (i + 1, base["periodos"][idx.min()], base["periodos"][idx.max()]))

    i_frango = SERIES.index("abate_frangos")
    amplitude_leite = medias[:, I_LEITE].max() - medias[:, I_LEITE].min()
    amplitude_frango = medias[:, i_frango].max() - medias[:, i_frango].min()
    print("pico do leite: T%d (%.2f%%)" % (int(np.argmax(medias[:, I_LEITE])) + 1,
                                            medias[:, I_LEITE].max()))
    print("amplitude leite %.2f p.p., amplitude frango %.2f p.p."
          % (amplitude_leite, amplitude_frango))

    print("desvio em relação a 25% (p.p.):")
    for i, t in enumerate((1, 2, 3, 4)):
        print("  T%d: %s" % (t, ", ".join(
            "%s %+.2f" % (s, desvio[i, j]) for j, s in enumerate(SERIES))))

    print("figuras gravadas em assets/img/")


if __name__ == "__main__":
    main()

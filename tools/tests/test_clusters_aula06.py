"""Trava as conclusoes que a Aula 06 afirma sobre o agrupamento das cinco series.

A aula inteira e construida sobre um contraste: agrupar os trimestres pelos
NIVEIS de producao devolve epocas, e agrupar pela PARTICIPACAO de cada
trimestre no total do proprio ano devolve o trimestre do calendario. Se algum
CSV for regerado com dado novo do SIDRA e esse contraste desaparecer, o deck, o
material, o notebook e as notas do professor passam a ensinar algo que o dado
nao sustenta mais.

Como em `test_modelo_aula05.py`, o que se trava aqui sao as conclusoes:

1. agrupar os niveis nao recupera o trimestre (fica no acaso) e produz blocos
   contiguos no tempo;
2. agrupar a participacao no ano recupera o trimestre em mais de 95% das linhas;
3. a silhueta premia o agrupamento MENOS util, que e o achado central da aula;
4. as duas linhas que escapam do ato 2 sao as duas de 2008;
5. o leite tem pico no T4 enquanto as carnes tem pico no T3;
6. a amplitude sazonal do leite e mais que o triplo da do frango.

A ordem entre frango (1,08 p.p.) e ovos (1,06 p.p.) NAO e travada: os dois
estao a 0,02 ponto percentual um do outro, e afirmar qual e o menor seria ler
ruido como achado.

Precisa de numpy e scikit-learn, que estao no requirements-ci.txt. Sem eles o
arquivo inteiro se pula, e o CI continua cobrindo.

Cada assercao foi vista falhando ao menos uma vez, contra versoes
propositalmente quebradas do pipeline: remover a padronizacao do ato 2,
normalizar pelo total da serie inteira em vez de por ano, e usar K=3.
"""
import csv
import os

import pytest

np = pytest.importorskip("numpy")
sk_cluster = pytest.importorskip("sklearn.cluster")
sk_pre = pytest.importorskip("sklearn.preprocessing")
sk_met = pytest.importorskip("sklearn.metrics")

KMeans = sk_cluster.KMeans
StandardScaler = sk_pre.StandardScaler
silhouette_score = sk_met.silhouette_score

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DADOS = os.path.join(RAIZ, "dados")
SERIES = [
    "abate_bovinos",
    "abate_suinos",
    "abate_frangos",
    "producao_ovos",
    "producao_leite",
]
K = 4
SEMENTE = 42


def _ler(nome):
    caminho = os.path.join(DADOS, nome + ".csv")
    with open(caminho, encoding="utf-8") as f:
        return {linha["periodo"]: float(linha["valor"]) for linha in csv.DictReader(f)}


@pytest.fixture(scope="module")
def base():
    """Interseccao das cinco series por periodo, ordenada no tempo.

    Interseccao, e nao uniao: `producao_ovos` comeca em 1987-T1 e as outras
    quatro em 1997-T1. E a mesma regra de juncao que a Aula 04 usou.
    """
    colunas = {s: _ler(s) for s in SERIES}
    periodos = sorted(set.intersection(*[set(c) for c in colunas.values()]))
    matriz = np.array([[colunas[s][p] for s in SERIES] for p in periodos])
    anos = np.array([int(p[:4]) for p in periodos])
    tris = np.array([int(p[-1]) for p in periodos])
    return {"periodos": periodos, "X": matriz, "anos": anos, "tris": tris}


def _kmeans(matriz):
    padronizada = StandardScaler().fit_transform(matriz)
    modelo = KMeans(n_clusters=K, n_init=50, random_state=SEMENTE).fit(padronizada)
    return modelo.labels_, silhouette_score(padronizada, modelo.labels_)


def _concordancia(rotulos, tris):
    """Fracao das linhas cobertas pelo trimestre majoritario de cada cluster."""
    acertos = 0
    for c in set(rotulos):
        do_cluster = tris[rotulos == c]
        acertos += max((do_cluster == t).sum() for t in (1, 2, 3, 4))
    return acertos / len(tris)


def _participacao_no_ano(b):
    """Cada valor vira a fracao que ele representa no total do proprio ano.

    So entram anos com os quatro trimestres medidos: 2026 tem apenas o T1, e
    incluir um ano incompleto faria o unico trimestre dele valer 100% do ano.
    """
    completos = {a for a in set(b["anos"].tolist()) if (b["anos"] == a).sum() == 4}
    mascara = np.array([a in completos for a in b["anos"]])
    X = b["X"][mascara]
    anos = b["anos"][mascara]
    saida = np.empty_like(X)
    for a in completos:
        linhas = anos == a
        saida[linhas] = X[linhas] / X[linhas].sum(axis=0)
    return saida, anos, b["tris"][mascara], [p for p, m in zip(b["periodos"], mascara) if m]


def test_base_tem_117_trimestres_de_1997_a_2026(base):
    assert len(base["periodos"]) == 117
    assert base["periodos"][0] == "1997-T1"
    assert base["periodos"][-1] == "2026-T1"


def test_agrupar_niveis_nao_recupera_o_trimestre(base):
    """Ato 1. A tendencia domina a variancia, e o resultado fica no acaso.

    Com quatro grupos, o acaso e 25%. Medido: 26,5%.
    """
    rotulos, _ = _kmeans(base["X"])
    assert _concordancia(rotulos, base["tris"]) < 0.35


def test_agrupar_niveis_devolve_blocos_contiguos_no_tempo(base):
    """Ato 1. Cada cluster e um intervalo fechado da linha do tempo.

    A base esta ordenada, entao um cluster contiguo ocupa posicoes consecutivas.
    Tolera uma unica troca na fronteira, que e onde 2019-T3 e 2020-T2 se
    encavalam.
    """
    rotulos, _ = _kmeans(base["X"])
    for c in set(rotulos):
        posicoes = np.where(rotulos == c)[0]
        vao = posicoes.max() - posicoes.min() + 1
        assert vao - len(posicoes) <= 2, (c, vao, len(posicoes))


def test_agrupar_participacao_no_ano_recupera_o_trimestre(base):
    """Ato 2. Removida a tendencia, o algoritmo redescobre o calendario.

    Medido: 114 de 116 linhas, 98,3%.
    """
    X, _, tris, periodos = _participacao_no_ano(base)
    assert len(periodos) == 116
    rotulos, _ = _kmeans(X)
    assert _concordancia(rotulos, tris) > 0.95


def test_a_silhueta_premia_o_agrupamento_menos_util(base):
    """O achado central da aula.

    Ato 1 tem silhueta 0,4795 e nao serve para nada no case. Ato 2 tem 0,2853 e
    responde a pergunta. A metrica mede separacao, e separacao nao e utilidade.
    """
    _, silhueta_niveis = _kmeans(base["X"])
    X, _, _, _ = _participacao_no_ano(base)
    _, silhueta_participacao = _kmeans(X)
    assert silhueta_niveis > silhueta_participacao
    assert 0.40 < silhueta_niveis < 0.55
    assert 0.22 < silhueta_participacao < 0.35


def test_as_duas_excecoes_do_ato_2_sao_de_2008(base):
    """As unicas duas linhas que caem fora do proprio trimestre sao de 2008."""
    X, _, tris, periodos = _participacao_no_ano(base)
    rotulos, _ = _kmeans(X)
    majoritario = {}
    for c in set(rotulos):
        do_cluster = tris[rotulos == c]
        majoritario[c] = max((1, 2, 3, 4), key=lambda t: (do_cluster == t).sum())
    fora = [p for p, r, t in zip(periodos, rotulos, tris) if majoritario[r] != t]
    assert len(fora) == 2
    assert all(p.startswith("2008") for p in fora), fora


def test_leite_tem_pico_no_t4_e_as_carnes_no_t3(base):
    """O pico do leite esta um trimestre a frente do das carnes.

    E o achado que serve ao Modelo 2 do TAPI, que converte producao em demanda
    de racao.
    """
    X, _, tris, _ = _participacao_no_ano(base)
    medias = {t: X[tris == t].mean(axis=0) for t in (1, 2, 3, 4)}
    i_leite = SERIES.index("producao_leite")
    for nome in ("abate_bovinos", "abate_suinos", "abate_frangos"):
        i = SERIES.index(nome)
        assert max((1, 2, 3, 4), key=lambda t: medias[t][i]) == 3, nome
    assert max((1, 2, 3, 4), key=lambda t: medias[t][i_leite]) == 4


def test_leite_e_mais_de_tres_vezes_mais_sazonal_que_frango(base):
    """Amplitude medida: leite 3,94 p.p. e frango 1,08 p.p.

    A ordem entre frango (1,08) e ovos (1,06) nao entra: 0,02 ponto percentual
    de diferenca e ruido, e travar isso seria travar ruido.
    """
    X, _, tris, _ = _participacao_no_ano(base)
    medias = np.array([X[tris == t].mean(axis=0) for t in (1, 2, 3, 4)])
    amplitude = (medias.max(axis=0) - medias.min(axis=0)) * 100
    leite = amplitude[SERIES.index("producao_leite")]
    frango = amplitude[SERIES.index("abate_frangos")]
    assert leite > 3 * frango
    assert leite == max(amplitude)

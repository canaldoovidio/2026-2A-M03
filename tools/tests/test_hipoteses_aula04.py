"""Trava as decisoes dos testes de hipotese que a Aula 04 afirma.

O bloco de hipoteses do deck, a secao 9 do material de apoio, as notas do
professor e a secao 8 do notebook citam estatistica e valor-p de quatro testes
sobre os CSVs reais. Se algum CSV for regerado com dado novo do SIDRA, uma
decisao pode virar (rejeita passa a nao rejeitar), e os quatro artefatos passam
a ensinar uma conclusao que o dado nao sustenta mais.

Este arquivo trava as decisoes, nao apenas os numeros: o que a aula ensina e a
cadeia hipotese -> teste -> decisao -> consequencia, e e a decisao que precisa
sobreviver. Os valores-p sao conferidos por ordem de grandeza, com folga, para
o teste nao quebrar por diferenca de versao de scipy.

Precisa de scipy, que nao esta no Python do sistema mas esta no
requirements-ci.txt. Sem scipy o arquivo inteiro se pula, e o CI continua
cobrindo. Cada assercao aqui foi vista falhando ao menos uma vez, contra um CSV
alterado de proposito.
"""
import csv
import os

import pytest

np = pytest.importorskip("numpy")
stats = pytest.importorskip("scipy.stats")

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DADOS = os.path.join(RAIZ, "dados")

SERIES = ["abate_bovinos", "abate_suinos", "abate_frangos",
          "producao_ovos", "producao_leite"]
ALVO = "abate_frangos"


def _serie(nome):
    caminho = os.path.join(DADOS, nome + ".csv")
    with open(caminho, encoding="utf-8") as fh:
        return {linha["periodo"]: float(linha["valor"])
                for linha in csv.DictReader(fh) if linha["valor"]}


@pytest.fixture(scope="module")
def base():
    """A juncao inner das cinco series, como a aula monta."""
    series = {nome: _serie(nome) for nome in SERIES}
    comuns = sorted(set.intersection(*[set(s) for s in series.values()]))
    return {
        "periodo": comuns,
        "ano": [int(p[:4]) for p in comuns],
        "trimestre": [int(p[-1]) for p in comuns],
        **{nome: np.array([series[nome][p] for p in comuns]) for nome in SERIES},
    }


def test_h1_shapiro_rejeita_normalidade_nas_cinco(base):
    """H1: a serie vem de uma normal. As cinco rejeitam em nivel."""
    for nome in SERIES:
        W, p = stats.shapiro(base[nome])
        assert p < 0.01, (nome, p)
    W, p = stats.shapiro(base[ALVO])
    assert round(W, 4) == 0.9462
    assert p < 0.001


def test_h1_bovinos_deixa_de_rejeitar_na_primeira_diferenca(base):
    """A excecao que o deck e o material citam nominalmente."""
    _, p = stats.shapiro(np.diff(base["abate_bovinos"]))
    assert p > 0.05, p
    for nome in ["abate_suinos", ALVO, "producao_ovos", "producao_leite"]:
        _, p = stats.shapiro(np.diff(base[nome]))
        assert p < 0.05, (nome, p)


def test_h2_correlacao_decide_diferente_em_nivel_e_em_diferenca(base):
    """H2: a correlacao com frangos e zero. Rejeita em nivel, nao rejeita na diferenca."""
    r, p = stats.pearsonr(base[ALVO], base["producao_leite"])
    assert r > 0.95 and p < 1e-50, (r, p)

    rd, pd_ = stats.pearsonr(np.diff(base[ALVO]), np.diff(base["producao_leite"]))
    assert abs(rd) < 0.1, rd
    assert pd_ > 0.05, pd_


def test_h3_sazonalidade_do_leite_so_aparece_sem_a_tendencia(base):
    """O achado central: o mesmo teste decide diferente antes e depois de remover a tendencia."""
    tri = np.array(base["trimestre"])
    y = base["producao_leite"]

    grupos_nivel = [y[tri == k] for k in (1, 2, 3, 4)]
    _, p_nivel = stats.kruskal(*grupos_nivel)
    assert p_nivel > 0.05, p_nivel

    tempo = np.arange(len(y))
    coef = np.polyfit(tempo, y, 1)
    residuo = y - np.polyval(coef, tempo)
    grupos_residuo = [residuo[tri == k] for k in (1, 2, 3, 4)]
    _, p_residuo = stats.kruskal(*grupos_residuo)
    assert p_residuo < 1e-4, p_residuo


def test_h3b_teste_t_pareado_por_ano(base):
    """H3b: T4 e igual a T2. Leite rejeita com folga, e o efeito e o maior das cinco."""
    ano = np.array(base["ano"])
    tri = np.array(base["trimestre"])
    efeitos = {}
    for nome in SERIES:
        y = base[nome]
        anos_completos = sorted({a for a in ano
                                 if {2, 4} <= {t for a2, t in zip(ano, tri) if a2 == a}})
        t4 = np.array([y[(ano == a) & (tri == 4)][0] for a in anos_completos])
        t2 = np.array([y[(ano == a) & (tri == 2)][0] for a in anos_completos])
        t_stat, p = stats.ttest_rel(t4, t2)
        efeitos[nome] = ((t4 - t2).mean() / y.mean() * 100, t_stat, p, len(anos_completos))

    efeito, t_stat, p, n = efeitos["producao_leite"]
    assert n == 29
    assert round(efeito, 2) == 14.85
    assert t_stat > 15 and p < 1e-12

    efeito_frango, t_frango, p_frango, _ = efeitos["abate_frangos"]
    assert round(efeito_frango, 2) == 1.90
    assert p_frango < 0.05, p_frango       # significante
    assert efeito_frango < efeito / 5      # e ainda assim pequeno perto do leite

    assert max(efeitos, key=lambda k: efeitos[k][0]) == "producao_leite"

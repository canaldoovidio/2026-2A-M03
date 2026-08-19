"""Trava os numeros que a Aula 04 afirma, contra os CSVs reais de dados/.

O deck, o material de apoio, as notas do professor e o notebook da Aula 04
citam numeros medidos (117 e 157 linhas na juncao, 40 ausentes, correlacoes em
nivel e em primeira diferenca, amplitude sazonal). Se algum CSV for regerado
com dado novo do SIDRA, esses numeros mudam e os quatro artefatos passam a
mentir sem que nenhum validador de layout ou de marca perceba.

Este arquivo e o que percebe. Ele recalcula tudo do zero, com a biblioteca
padrao, sem pandas nem scipy: assim roda na mesma bateria dos outros
validadores, sem dependencia nova.

Cada assercao foi vista falhando ao menos uma vez, alterando de proposito o
valor esperado, antes de entrar aqui.
"""
import csv
import math
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DADOS = os.path.join(RAIZ, "dados")

SERIES = ["abate_bovinos", "abate_suinos", "abate_frangos",
          "producao_ovos", "producao_leite"]
ALVO = "abate_frangos"


def _serie(nome):
    """Devolve {periodo: valor} de um CSV de dados/."""
    caminho = os.path.join(DADOS, nome + ".csv")
    with open(caminho, encoding="utf-8") as fh:
        return {linha["periodo"]: float(linha["valor"])
                for linha in csv.DictReader(fh) if linha["valor"]}


def _base_inner():
    """A mesma juncao inner que a aula monta, como lista de dicionarios."""
    series = {nome: _serie(nome) for nome in SERIES}
    comuns = set(series[SERIES[0]])
    for nome in SERIES[1:]:
        comuns &= set(series[nome])
    return [dict({"periodo": p}, **{nome: series[nome][p] for nome in SERIES})
            for p in sorted(comuns)]


def _pearson(xs, ys):
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    vx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    vy = math.sqrt(sum((y - my) ** 2 for y in ys))
    return cov / (vx * vy)


def _diff(valores):
    return [b - a for a, b in zip(valores, valores[1:])]


def test_cobertura_de_cada_serie():
    """producao_ovos comeca dez anos antes das outras quatro."""
    esperado = {
        "abate_bovinos": (117, "1997-T1"),
        "abate_suinos": (117, "1997-T1"),
        "abate_frangos": (117, "1997-T1"),
        "producao_ovos": (157, "1987-T1"),
        "producao_leite": (117, "1997-T1"),
    }
    for nome, (n, primeiro) in esperado.items():
        serie = _serie(nome)
        assert len(serie) == n, nome
        assert min(serie) == primeiro, nome


def test_juncao_inner_e_outer():
    """117 linhas no inner, 157 no outer, 40 ausentes em quatro colunas."""
    series = {nome: set(_serie(nome)) for nome in SERIES}
    inner = set.intersection(*series.values())
    outer = set.union(*series.values())
    assert len(inner) == 117
    assert len(outer) == 157
    for nome in SERIES:
        faltando = len(outer - series[nome])
        assert faltando == (0 if nome == "producao_ovos" else 40), nome


def test_defasagem_custa_quatro_linhas():
    """shift(1) perde 1 linha e shift(4) perde 4, sobrando 113 de 117."""
    base = _base_inner()
    assert len(base) == 117
    lag1 = [None] + [linha[ALVO] for linha in base[:-1]]
    lag4 = [None] * 4 + [linha[ALVO] for linha in base[:-4]]
    assert sum(1 for v in lag1 if v is None) == 1
    assert sum(1 for v in lag4 if v is None) == 4
    completas = sum(1 for a, b in zip(lag1, lag4) if a is not None and b is not None)
    assert completas == 113


def test_correlacao_das_defasagens():
    """Leite e a unica serie em que lag4 bate lag1."""
    base = _base_inner()
    for nome in SERIES:
        valores = [linha[nome] for linha in base]
        r1 = _pearson(valores[1:], valores[:-1])
        r4 = _pearson(valores[4:], valores[:-4])
        lider = "lag4" if r4 > r1 else "lag1"
        assert lider == ("lag4" if nome == "producao_leite" else "lag1"), nome


def test_correlacao_cai_na_primeira_diferenca():
    """O achado central do Bloco 3: +0,92 a +0,98 em nivel, abaixo de +0,21 na diferenca."""
    base = _base_inner()
    alvo = [linha[ALVO] for linha in base]
    alvo_diff = _diff(alvo)
    for nome in SERIES:
        if nome == ALVO:
            continue
        valores = [linha[nome] for linha in base]
        r_nivel = _pearson(alvo, valores)
        r_diff = _pearson(alvo_diff, _diff(valores))
        assert r_nivel > 0.92, (nome, r_nivel)
        assert abs(r_diff) < 0.21, (nome, r_diff)


def test_numeros_citados_no_deck():
    """As quatro correlacoes impressas na figura do slide 18, com duas casas."""
    base = _base_inner()
    alvo = [linha[ALVO] for linha in base]
    alvo_diff = _diff(alvo)
    esperado = {
        "abate_bovinos": (0.93, 0.05),
        "abate_suinos": (0.97, 0.20),
        "producao_ovos": (0.94, 0.15),
        "producao_leite": (0.96, -0.04),
    }
    for nome, (n_esperado, d_esperado) in esperado.items():
        valores = [linha[nome] for linha in base]
        assert round(_pearson(alvo, valores), 2) == n_esperado, nome
        assert round(_pearson(alvo_diff, _diff(valores)), 2) == d_esperado, nome


def test_amplitude_sazonal_por_serie():
    """Leite e a serie mais sazonal (14,85 pp) e frango uma das menos (2,55 pp)."""
    base = _base_inner()
    amplitudes = {}
    for nome in SERIES:
        por_trimestre = {}
        for linha in base:
            por_trimestre.setdefault(linha["periodo"][-1], []).append(linha[nome])
        medias = [sum(v) / len(v) for v in por_trimestre.values()]
        geral = sum(linha[nome] for linha in base) / len(base)
        amplitudes[nome] = (max(medias) - min(medias)) / geral * 100

    assert round(amplitudes["producao_leite"], 2) == 14.85
    assert round(amplitudes["abate_frangos"], 2) == 2.55
    assert amplitudes["producao_leite"] == max(amplitudes.values())

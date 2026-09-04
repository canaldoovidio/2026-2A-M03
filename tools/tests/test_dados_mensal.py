"""Trava o contrato dos CSVs mensais e a reconciliacao com os trimestrais.

A base mensal existe porque as cinco tabelas do SIDRA trazem a classificacao
c12716 (Referencia temporal), com "No 1o mes", "No 2o mes" e "No 3o mes" alem
de "Total do trimestre". A ADR-010 registra a decisao; este arquivo trava o
resultado.

A reconciliacao e o teste que importa: se a soma dos tres meses nao devolver o
trimestre ja versionado em dados/, o mapeamento de mes esta errado e a serie
mensal esta silenciosamente deslocada no tempo.
"""
import csv
import os
import re
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DADOS = os.path.join(RAIZ, "dados")
MENSAL = os.path.join(DADOS, "mensal")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import baixar_dados  # noqa: E402

ESPERADOS = [
    "abate_bovinos.csv", "abate_suinos.csv", "abate_frangos.csv",
    "producao_ovos.csv", "producao_leite.csv",
]

# Ovos e leite vem em "Mil duzias" e "Mil litros". O IBGE arredonda cada mes
# de forma independente, entao a soma de tres valores arredondados nao precisa
# igualar o total trimestral arredondado. A divergencia observada e de 1
# unidade, uma parte em um milhao. As tres series de abate, em quilogramas,
# reconciliam sem nenhuma divergencia.
TOLERANCIA = {
    "abate_bovinos.csv": 0,
    "abate_suinos.csv": 0,
    "abate_frangos.csv": 0,
    "producao_ovos.csv": 1,
    "producao_leite.csv": 1,
}


def _ler(caminho):
    with open(caminho, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def test_todos_os_csv_mensais_existem():
    for nome in ESPERADOS:
        assert os.path.isfile(os.path.join(MENSAL, nome)), nome


def test_colunas_do_contrato():
    for nome in ESPERADOS:
        linhas = _ler(os.path.join(MENSAL, nome))
        assert set(linhas[0]) == {"periodo", "valor", "unidade"}, nome


def test_periodo_em_ano_mes_ordenado_e_sem_buraco():
    for nome in ESPERADOS:
        periodos = [l["periodo"] for l in _ler(os.path.join(MENSAL, nome))]
        assert periodos == sorted(periodos), nome
        assert len(periodos) == len(set(periodos)), nome
        for p in periodos:
            assert re.fullmatch(r"\d{4}-(0[1-9]|1[0-2])", p), (nome, p)
        # sem buraco: a contagem tem de bater com a distancia entre extremos
        def indice(p):
            ano, mes = p.split("-")
            return int(ano) * 12 + int(mes)
        assert indice(periodos[-1]) - indice(periodos[0]) + 1 == len(periodos), nome


def test_as_tres_series_de_abate_tem_351_linhas():
    for nome in ["abate_bovinos.csv", "abate_suinos.csv", "abate_frangos.csv"]:
        linhas = _ler(os.path.join(MENSAL, nome))
        assert len(linhas) == 351, nome
        assert linhas[0]["periodo"] == "1997-01", nome
        assert linhas[-1]["periodo"] == "2026-03", nome


def test_nenhum_valor_ausente():
    for nome in ESPERADOS:
        vazios = [l["periodo"] for l in _ler(os.path.join(MENSAL, nome)) if not l["valor"]]
        assert vazios == [], (nome, vazios[:5])


def test_soma_dos_tres_meses_reconcilia_com_o_trimestre():
    """O teste que prova que o mapeamento de mes esta certo."""
    for nome in ESPERADOS:
        trimestral = {l["periodo"]: float(l["valor"])
                      for l in _ler(os.path.join(DADOS, nome)) if l["valor"]}
        soma = {}
        for l in _ler(os.path.join(MENSAL, nome)):
            ano, mes = l["periodo"].split("-")
            chave = "%s-T%d" % (ano, (int(mes) - 1) // 3 + 1)
            soma[chave] = soma.get(chave, 0.0) + float(l["valor"])
        comuns = sorted(set(trimestral) & set(soma))
        assert len(comuns) >= 117, nome
        for chave in comuns:
            assert abs(trimestral[chave] - soma[chave]) <= TOLERANCIA[nome], \
                (nome, chave, trimestral[chave], soma[chave])


def test_as_series_de_abate_reconciliam_exatamente():
    """Separado de proposito: em quilogramas nao ha arredondamento, e uma
    divergencia de 1 kg ja seria sinal de mapeamento errado."""
    for nome in ["abate_bovinos.csv", "abate_suinos.csv", "abate_frangos.csv"]:
        trimestral = {l["periodo"]: float(l["valor"])
                      for l in _ler(os.path.join(DADOS, nome)) if l["valor"]}
        soma = {}
        for l in _ler(os.path.join(MENSAL, nome)):
            ano, mes = l["periodo"].split("-")
            chave = "%s-T%d" % (ano, (int(mes) - 1) // 3 + 1)
            soma[chave] = soma.get(chave, 0.0) + float(l["valor"])
        divergentes = [c for c in set(trimestral) & set(soma)
                       if trimestral[c] != soma[c]]
        assert divergentes == [], (nome, divergentes[:5])


def test_normalizar_periodo_mensal():
    assert baixar_dados.normalizar_periodo_mensal("202601", "115233") == "2026-01"
    assert baixar_dados.normalizar_periodo_mensal("202601", "115234") == "2026-02"
    assert baixar_dados.normalizar_periodo_mensal("202601", "115235") == "2026-03"
    assert baixar_dados.normalizar_periodo_mensal("202504", "115235") == "2025-12"
    assert baixar_dados.normalizar_periodo_mensal("202502", "115233") == "2025-04"

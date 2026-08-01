import csv
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DADOS = os.path.join(RAIZ, "dados")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import baixar_dados  # noqa: E402

ESPERADOS = [
    "abate_bovinos.csv", "abate_suinos.csv", "abate_frangos.csv",
    "producao_ovos.csv", "producao_leite.csv",
]


def _ler(nome):
    with open(os.path.join(DADOS, nome), encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def test_todos_os_csv_existem():
    for nome in ESPERADOS:
        assert os.path.isfile(os.path.join(DADOS, nome)), nome


def test_colunas_do_contrato():
    for nome in ESPERADOS:
        linhas = _ler(nome)
        assert set(linhas[0]) == {"periodo", "valor", "unidade"}, nome


def test_periodo_em_ano_trimestre_ordenado():
    for nome in ESPERADOS:
        periodos = [l["periodo"] for l in _ler(nome)]
        assert periodos == sorted(periodos), nome
        for p in periodos:
            ano, tri = p.split("-")
            assert len(ano) == 4 and ano.isdigit(), "%s: %s" % (nome, p)
            assert tri[0] == "T" and 1 <= int(tri[1:]) <= 4, "%s: %s" % (nome, p)


def test_serie_cobre_ao_menos_dez_anos():
    # Trimestral: 10 anos sao 40 periodos. A serie real passa de 100.
    for nome in ESPERADOS:
        assert len(_ler(nome)) >= 40, nome


def test_um_registro_por_periodo():
    # As tabelas tem dimensoes extras (tipo de rebanho, inspecao). Se o filtro
    # de "Total" falhar, o mesmo periodo aparece varias vezes com recortes
    # diferentes, e a serie fica silenciosamente errada.
    for nome in ESPERADOS:
        periodos = [l["periodo"] for l in _ler(nome)]
        assert len(periodos) == len(set(periodos)), nome


def test_valores_sao_numericos_ou_vazios():
    for nome in ESPERADOS:
        for linha in _ler(nome):
            if linha["valor"] == "":
                continue
            float(linha["valor"])


def test_unidade_unica_por_arquivo():
    # Cada arquivo precisa vir de uma unica variavel do SIDRA: misturar
    # variaveis (peso, percentual, numero de informantes) trocaria a unidade
    # no meio do arquivo sem dar erro nenhum.
    for nome in ESPERADOS:
        unidades = set(l["unidade"] for l in _ler(nome))
        assert len(unidades) == 1, "%s: unidades misturadas %s" % (nome, unidades)


def test_ordem_de_grandeza_plausivel():
    # Checagem de sanidade: se o parser pegasse "numero de informantes" em
    # vez da serie fisica real, os valores cairiam para a casa das centenas.
    limites_minimos = {
        "abate_bovinos.csv": 1e8,
        "abate_suinos.csv": 1e8,
        "abate_frangos.csv": 1e8,
        "producao_ovos.csv": 1e4,
        "producao_leite.csv": 1e5,
    }
    for nome, minimo in limites_minimos.items():
        valores = [float(l["valor"]) for l in _ler(nome) if l["valor"]]
        assert min(valores) >= minimo, "%s: valor abaixo do plausivel (%r)" % (nome, min(valores))


def _item_sidra(periodo, dimensao_total="Total", valor="100"):
    return {
        "V": valor,
        "D3C": periodo,
        "MN": "Quilogramas",
        "D4N": dimensao_total,
    }


def test_extrair_linhas_falha_quando_periodo_duplica_apos_filtro_total():
    # Se o filtro de dimensoes extras (e_linha_total) um dia parar de isolar
    # um unico recorte por periodo, o mesmo trimestre chegaria duas vezes
    # aqui, ambas marcadas como "Total". Isso precisa parar a geracao com
    # erro, nunca silenciosamente ficar so com a primeira ocorrencia.
    payload = [
        {"MN": "Quilogramas"},
        _item_sidra("199701", valor="100"),
        _item_sidra("199701", valor="200"),  # mesmo periodo, outro recorte
        _item_sidra("199702", valor="300"),
    ]
    with pytest.raises(ValueError) as excinfo:
        baixar_dados.extrair_linhas(payload)
    mensagem = str(excinfo.value)
    assert "1997-T1" in mensagem
    assert "2 linhas" in mensagem


def test_extrair_linhas_payload_limpo_um_registro_por_periodo():
    payload = [
        {"MN": "Quilogramas"},
        _item_sidra("199701", valor="100"),
        _item_sidra("199702", valor="200"),
    ]
    linhas = baixar_dados.extrair_linhas(payload)
    assert [l["periodo"] for l in linhas] == ["1997-T1", "1997-T2"]
    assert [l["valor"] for l in linhas] == ["100.0", "200.0"]


def test_converter_marcadores_de_ausencia_viram_vazio():
    for marcador in ["...", "..", "-", "X", "*", ""]:
        assert baixar_dados.converter(marcador) == ""


def test_converter_marcador_ausente_nao_vira_zero():
    # Zero entraria na media e contaminaria qualquer metrica de erro do
    # modelo; dado ausente precisa ficar vazio, nunca 0.0.
    assert baixar_dados.converter("...") != "0.0"


def test_converter_numero_normal():
    assert baixar_dados.converter("1234567") == "1234567.0"


def test_converter_numero_com_virgula_decimal():
    assert baixar_dados.converter("123,45") == "123.45"

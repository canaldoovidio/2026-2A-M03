import csv
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DADOS = os.path.join(RAIZ, "dados")

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

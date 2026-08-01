import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extrair_autoestudos import extrair, renderizar  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
XLSX = os.path.join(RAIZ, "Turma.xlsx")

pytestmark = pytest.mark.skipif(
    not os.path.isfile(XLSX),
    reason="Turma.xlsx nao versionado; roda so na maquina do professor",
)


@pytest.fixture(scope="module")
def dados():
    return extrair(XLSX)


def test_dez_semanas(dados):
    assert sorted(dados) == ["Semana %02d" % n for n in range(1, 11)]


def test_quatorze_encontros_do_ovidio(dados):
    total = sum(len(s["encontros"]) for s in dados.values())
    assert total == 14


def test_primeiro_encontro_e_python_em_04_08(dados):
    primeiro = dados["Semana 01"]["encontros"][0]
    assert primeiro["data"] == "04/08/2026"
    assert primeiro["titulo"] == "Introdução ao Python"


def test_semana_04_tem_overfitting(dados):
    assert "Overfitting" in dados["Semana 04"]["autoestudos"]


def test_nenhum_nome_de_aluno_vaza_para_o_markdown(dados):
    texto = renderizar(dados)
    assert "Aluno_Nome" not in texto
    assert "Adalove Teste" not in texto


def test_markdown_tem_uma_secao_por_semana(dados):
    texto = renderizar(dados)
    for n in range(1, 11):
        assert "## Semana %02d" % n in texto

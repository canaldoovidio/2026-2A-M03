import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from check_links import quebrados  # noqa: E402


def _escrever(tmp_path, caminho, conteudo):
    destino = tmp_path / caminho
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(conteudo, encoding="utf-8")


def test_link_para_arquivo_existente_passa(tmp_path):
    _escrever(tmp_path, "index.html", '<a href="aulas/aula01.html">Aula 1</a>')
    _escrever(tmp_path, "aulas/aula01.html", "<html></html>")
    assert quebrados(str(tmp_path)) == []


def test_link_para_arquivo_inexistente_e_acusado(tmp_path):
    _escrever(tmp_path, "index.html", '<a href="aulas/aula99.html">Aula 99</a>')
    achados = quebrados(str(tmp_path))
    assert len(achados) == 1
    assert achados[0]["href"] == "aulas/aula99.html"


def test_link_externo_e_ignorado(tmp_path):
    _escrever(tmp_path, "index.html", '<a href="https://sidra.ibge.gov.br/tabela/1092">IBGE</a>')
    assert quebrados(str(tmp_path)) == []


def test_ancora_e_ignorada(tmp_path):
    _escrever(tmp_path, "index.html", '<a href="#topo">topo</a>')
    assert quebrados(str(tmp_path)) == []


def test_query_string_nao_quebra_a_resolucao(tmp_path):
    _escrever(tmp_path, "index.html", '<a href="aulas/aula01.html?print-pdf">PDF</a>')
    _escrever(tmp_path, "aulas/aula01.html", "<html></html>")
    assert quebrados(str(tmp_path)) == []


def test_caminho_relativo_sobe_de_subpasta(tmp_path):
    _escrever(tmp_path, "aulas/aula01.html", '<a href="../index.html">voltar</a>')
    _escrever(tmp_path, "index.html", "<html></html>")
    assert quebrados(str(tmp_path)) == []

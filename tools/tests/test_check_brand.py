import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from check_brand import varrer  # noqa: E402


def _escrever(tmp_path, caminho, conteudo):
    destino = tmp_path / caminho
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(conteudo, encoding="utf-8")
    return destino


def _brand_valido(tmp_path):
    _escrever(tmp_path, "assets/css/inteli-brand.css", ":root { --inteli-roxo: #2e2640; }")


def test_paleta_valida_nao_acusa(tmp_path):
    _brand_valido(tmp_path)
    assert varrer(str(tmp_path)) == []


def test_hex_fora_da_paleta_no_brand_e_acusado(tmp_path):
    _escrever(tmp_path, "assets/css/inteli-brand.css", ":root { --x: #123456; }")
    achados = varrer(str(tmp_path))
    assert [a["regra"] for a in achados] == ["cor-fora-da-paleta"]
    assert achados[0]["linha"] == 1


def test_cor_literal_fora_do_brand_e_acusada(tmp_path):
    _brand_valido(tmp_path)
    _escrever(tmp_path, "assets/css/inteli-theme.css", ".capa { color: #2e2640; }")
    achados = varrer(str(tmp_path))
    assert [a["regra"] for a in achados] == ["cor-literal"]


def test_cor_literal_em_style_inline_e_acusada(tmp_path):
    _brand_valido(tmp_path)
    _escrever(tmp_path, "aulas/aula01.html", '<p style="color: #ffffff">oi</p>')
    achados = varrer(str(tmp_path))
    assert [a["regra"] for a in achados] == ["cor-literal"]


def test_ancora_com_letras_hex_nao_e_confundida_com_cor(tmp_path):
    _brand_valido(tmp_path)
    _escrever(tmp_path, "aulas/aula01.html", '<a href="#dados">dados</a>')
    assert varrer(str(tmp_path)) == []


def test_var_token_nao_e_acusado(tmp_path):
    _brand_valido(tmp_path)
    _escrever(tmp_path, "assets/css/inteli-theme.css", ".capa { color: var(--inteli-roxo); }")
    assert varrer(str(tmp_path)) == []


def test_font_family_fora_do_brand_e_acusada(tmp_path):
    _brand_valido(tmp_path)
    _escrever(tmp_path, "assets/css/inteli-theme.css", ".t { font-family: Arial; }")
    achados = varrer(str(tmp_path))
    assert [a["regra"] for a in achados] == ["fonte-fora-do-brand"]


def test_cor_de_outro_segmento_e_acusada_mesmo_no_brand(tmp_path):
    _escrever(tmp_path, "assets/css/inteli-brand.css", ":root { --lilas: #90a5e5; }")
    achados = varrer(str(tmp_path))
    assert [a["regra"] for a in achados] == ["cor-de-outro-segmento"]


def test_emoji_e_acusado(tmp_path):
    _brand_valido(tmp_path)
    _escrever(tmp_path, "index.html", "<h1>Aulas \U0001F4DA</h1>")
    achados = varrer(str(tmp_path))
    assert [a["regra"] for a in achados] == ["emoji"]


def test_seta_tipografica_nao_e_emoji(tmp_path):
    _brand_valido(tmp_path)
    _escrever(tmp_path, "index.html", "<p>Sprint 1 → Sprint 2</p>")
    assert varrer(str(tmp_path)) == []

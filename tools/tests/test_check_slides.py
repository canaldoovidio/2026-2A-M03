import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import check_slides  # noqa: E402

sync_api = pytest.importorskip("playwright.sync_api")

FIXTURE = "tools/tests/fixture_layout.html"


@pytest.fixture(scope="module")
def servidor():
    """Sobe o servidor e o navegador uma vez para o modulo inteiro.

    Devolve (page, porta) em vez de pendurar a porta no objeto Page: Page do
    Playwright usa __slots__ em algumas versoes e a atribuicao falharia.
    """
    porta = check_slides.porta_livre()
    httpd = check_slides.servir(porta)
    with sync_api.sync_playwright() as p:
        navegador = p.chromium.launch()
        page = navegador.new_page(viewport={"width": 1280, "height": 720})
        try:
            yield page, porta
        finally:
            navegador.close()
    httpd.shutdown()


def _medir(servidor, caminho):
    page, porta = servidor
    page.goto("http://127.0.0.1:%d/%s" % (porta, caminho), wait_until="networkidle")
    page.wait_for_timeout(900)
    return page.evaluate(check_slides.JS_MEDIR)


def test_slide_limpo_nao_acusa(servidor):
    slides = _medir(servidor, FIXTURE)
    assert slides[0]["pior"] is None
    assert slides[0]["sobreposicoes"] == []
    assert slides[0]["colisoes"] == []


def test_estouro_e_detectado(servidor):
    slides = _medir(servidor, FIXTURE)
    assert slides[1]["pior"] is not None
    assert slides[1]["pior"]["abaixo"] > 2


def test_sobreposicao_sem_estouro_e_detectada(servidor):
    slides = _medir(servidor, FIXTURE)
    assert slides[2]["pior"] is None, "esse defeito nao estoura os 720px"
    assert slides[2]["sobreposicoes"], "e mesmo assim precisa ser acusado"


def test_titulo_por_baixo_do_logo_e_detectado(servidor):
    slides = _medir(servidor, FIXTURE)
    assert slides[3]["colisoes"], "titulo longo colidindo com o logo"


def test_fixture_do_tema_passa_limpo(servidor):
    slides = _medir(servidor, "aulas/_fixture-tema.html")
    sujos = [s for s in slides
             if s["pior"] or s["sobreposicoes"] or s["colisoes"]]
    assert sujos == [], "o deck de referencia do tema precisa passar limpo"


# --- Regressao da rodada de correcao 1: falso-verde do parsing de --shots --

def test_parse_args_shots_sozinho_nao_vira_deck():
    """--shots DIR sem nenhum deck explicito continua sem decks: main() cai
    no ramo que varre aulas/. Sem essa garantia, DIR e tratado como o unico
    deck, o servidor devolve 404 e o validador aprova sem medir nada."""
    decks, shots_dir = check_slides._parse_args(["--shots", "/tmp/shots-regressao"])
    assert decks == []
    assert shots_dir == "/tmp/shots-regressao"


def test_parse_args_deck_mais_shots_nao_cria_deck_fantasma():
    """deck.html --shots DIR varre so aquele deck: DIR nao pode aparecer como
    um segundo deck fantasma na lista."""
    decks, shots_dir = check_slides._parse_args(
        ["aulas/aula01.html", "--shots", "/tmp/shots-regressao"]
    )
    assert decks == ["aulas/aula01.html"]
    assert shots_dir == "/tmp/shots-regressao"


def test_html_sem_sections_reprova(servidor):
    """checar() contra um HTML sem nenhuma <section> precisa devolver um
    valor diferente de zero: zero slides encontrados e um deck que nao
    carregou, nao um deck limpo. Reproduz por outro caminho o mesmo defeito
    do bug de parsing: 0 slides jamais pode significar sucesso."""
    page, porta = servidor
    resultado = check_slides.checar(
        page,
        "http://127.0.0.1:%d/tools/tests/fixture_sem_slides.html" % porta,
        "fixture_sem_slides.html",
    )
    assert resultado != 0


def test_url_404_reprova(servidor):
    """Reproducao direta do CRITICAL relatado: uma URL que devolve 404 (o
    mesmo efeito de tratar o diretorio de --shots como se fosse um deck) tem
    que reprovar, nunca imprimir sucesso silencioso."""
    page, porta = servidor
    resultado = check_slides.checar(
        page,
        "http://127.0.0.1:%d/tools/tests/nao-existe-de-proposito.html" % porta,
        "nao-existe-de-proposito.html",
    )
    assert resultado != 0

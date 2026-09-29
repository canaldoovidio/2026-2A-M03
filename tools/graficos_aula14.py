"""Gera as figuras da Aula 14 a partir dos CSVs de dados/mensal/ e do app.

1. `aula14-cenarios-estabilidade.png`. O efeito médio de um choque de +10% nas
   24 previsões de teste, lido em dois ajustes do mesmo modelo: o exportado
   (339 meses) e o avaliado (315 meses). Dois painéis, com escalas diferentes
   declaradas no título de cada um, porque o choque no patamar do frango move a
   previsão em cerca de 9,6% e os outros três ficam abaixo de 0,5%: num eixo só,
   os três menores viram uma linha.

   O que a figura mostra é a afirmação central do bloco de cenários: o choque
   no grupo de defasagens do frango dá 9,62% e 9,63% nos dois ajustes, e o
   choque só no abate de bovinos troca de sinal (+0,151% contra -0,005%).
   Cenário numa entrada isolada herda a instabilidade do coeficiente que a
   Aula 12 mediu.

2. `aula14-app-streamlit.png`. Captura de tela do app rodando de verdade, com
   `streamlit run app/app.py` num processo local e o Playwright abrindo a
   página, com o cenário de -10% no patamar do frango aplicado pelo teclado.
   Só é gerada com `--captura`, porque depende de Streamlit e de um Chromium
   do Playwright instalados.

Decisões de forma, herdadas de `tools/graficos_aula12.py`: roxo como tinta,
coral como destaque, verde e cinza escuro como referências; 1600x900 a 150 dpi
e corpo 26; separador decimal com vírgula; nada interpolado ou inventado, tudo
calculado por `app/logica.py`, que é o mesmo código que o app e o notebook
usam.

Uso:
    python3 tools/graficos_aula14.py              # figura 1
    python3 tools/graficos_aula14.py --captura    # figura 1 e a captura do app
"""
import os
import subprocess
import sys
import time
import urllib.request

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG = os.path.join(RAIZ, "assets", "img")
sys.path.insert(0, os.path.join(RAIZ, "app"))
import logica  # noqa: E402

# cores lidas de assets/css/inteli-brand.css (paleta da Graduacao, p.66/p.68)
TINTA = "#2e2640"          # --inteli-roxo
DESTAQUE = "#ff4545"       # --inteli-coral
REFERENCIA_1 = "#b2b6bf"   # --inteli-cinza-escuro
REFERENCIA_2 = "#89cea5"   # --inteli-verde
SOMBRA = "#e6eaeb"         # --inteli-cinza-claro
FUNDO = "#ffffff"          # --inteli-branco

CHOQUE = 10

plt.rcParams.update({
    "figure.facecolor": FUNDO,
    "axes.facecolor": FUNDO,
    "axes.edgecolor": REFERENCIA_1,
    "axes.labelcolor": TINTA,
    "xtick.color": TINTA,
    "ytick.color": TINTA,
    "text.color": TINTA,
    "font.size": 26,
    "axes.spines.top": False,
    "axes.spines.right": False,
})


def br(valor, casas):
    return logica.numero_br(valor, casas, sinal=True)


def medir():
    """Os quatro cenários da figura, nos dois ajustes. Mesmos números do teste."""
    base = logica.base_analitica()
    pipe = logica.carregar_pipeline()
    cenarios = [
        ("patamar", logica.CENARIOS["patamar_frango"]["colunas"]),
        ("outras 4", logica.CENARIOS["outras_proteinas"]["colunas"]),
        ("só lag1", ["lag1"]),
        ("só bovinos", logica.CENARIOS["so_bovinos"]["colunas"]),
    ]
    saida = []
    for rotulo, colunas in cenarios:
        estab = logica.estabilidade_do_cenario(pipe, base, colunas, CHOQUE)
        saida.append((rotulo, estab["exportado"], estab["avaliado"]))
    return saida


def figura_estabilidade(medidas):
    fig, (esq, dir_) = plt.subplots(1, 2, figsize=(16, 9), dpi=150,
                                    gridspec_kw={"width_ratios": [1, 2.4]})
    largura = 0.38

    rotulo, exp, av = medidas[0]
    esq.bar([-largura / 2], [exp], largura, color=DESTAQUE)
    esq.bar([largura / 2], [av], largura, color=TINTA)
    esq.text(-largura / 2, exp + 0.25, br(exp, 2), ha="center", va="bottom", fontsize=26)
    esq.text(largura / 2, av + 0.25, br(av, 2), ha="center", va="bottom", fontsize=26)
    esq.set_xticks([0], [rotulo])
    esq.set_ylim(0, 12)
    esq.set_yticks([0, 5, 10], ["0", "5", "10"])
    esq.set_ylabel("efeito médio (%)")
    esq.set_title("escala de 0 a 12%", fontsize=24, loc="left")

    pequenos = medidas[1:]
    for i, (rotulo, exp, av) in enumerate(pequenos):
        dir_.bar(i - largura / 2, exp, largura, color=DESTAQUE)
        dir_.bar(i + largura / 2, av, largura, color=TINTA)
        if (exp > 0) != (av > 0):
            dir_.annotate("troca de sinal", xy=(i, 0.30), ha="center", fontsize=24,
                          fontweight="bold", color=DESTAQUE)
        dir_.text(i - largura / 2, exp + 0.015, br(exp, 2), ha="center", va="bottom",
                  fontsize=24)
        casas = 3 if abs(av) < 0.01 else 2
        deslocamento = 0.015 if av >= 0 else -0.015
        dir_.text(i + largura / 2, av + deslocamento, br(av, casas), ha="center",
                  va="bottom" if av >= 0 else "top", fontsize=24)
    dir_.axhline(0, color=TINTA, linewidth=1.5)
    dir_.set_xticks(range(len(pequenos)), [m[0] for m in pequenos])
    dir_.set_ylim(-0.1, 0.55)
    dir_.set_yticks([0, 0.2, 0.4], ["0", "0,2", "0,4"])
    dir_.set_title("escala de -0,1 a 0,55%", fontsize=24, loc="left")

    handles = [plt.Rectangle((0, 0), 1, 1, color=DESTAQUE),
               plt.Rectangle((0, 0), 1, 1, color=TINTA)]
    fig.legend(handles, ["exportado, 339 meses", "avaliado, 315 meses"],
               loc="upper center", ncol=2, frameon=False, fontsize=26,
               bbox_to_anchor=(0.5, 1.0))
    fig.tight_layout(rect=(0, 0, 1, 0.9))
    destino = os.path.join(IMG, "aula14-cenarios-estabilidade.png")
    fig.savefig(destino)
    plt.close(fig)
    return destino


def captura_do_app(porta=8631):
    """Sobe o app com `streamlit run`, aplica o cenário e fotografa a página."""
    from playwright.sync_api import sync_playwright

    comando = [sys.executable, "-m", "streamlit", "run", os.path.join("app", "app.py"),
               "--server.headless", "true", "--server.port", str(porta),
               "--client.toolbarMode", "viewer",
               "--browser.gatherUsageStats", "false"]
    processo = subprocess.Popen(comando, cwd=RAIZ, stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL)
    try:
        url = "http://localhost:%d" % porta
        for _ in range(60):
            try:
                if urllib.request.urlopen(url + "/_stcore/health", timeout=1).read() == b"ok":
                    break
            except OSError:
                time.sleep(0.5)
        else:
            raise RuntimeError("o streamlit não respondeu em 30 segundos")

        with sync_playwright() as p:
            navegador = p.chromium.launch()
            pagina = navegador.new_page(viewport={"width": 1280, "height": 860},
                                        device_scale_factor=1.25)
            pagina.goto(url)
            pagina.wait_for_selector('[data-testid="stMetric"]', timeout=60000)
            pagina.wait_for_timeout(2000)
            controles = pagina.locator('[data-testid="stSidebar"] input[type="range"]')
            choque = controles.nth(1)
            choque.focus()
            for _ in range(10):
                choque.press("ArrowLeft")
            pagina.wait_for_timeout(4000)
            destino = os.path.join(IMG, "aula14-app-streamlit.png")
            pagina.screenshot(path=destino)
            navegador.close()
        return destino
    finally:
        processo.terminate()
        processo.wait(timeout=10)


def main():
    medidas = medir()
    for rotulo, exp, av in medidas:
        print("%-11s exportado %s%%   avaliado %s%%" % (rotulo, br(exp, 3), br(av, 3)))
    print(os.path.relpath(figura_estabilidade(medidas), RAIZ))
    if "--captura" in sys.argv:
        print(os.path.relpath(captura_do_app(), RAIZ))


if __name__ == "__main__":
    main()

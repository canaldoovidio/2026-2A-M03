"""Gera os quatro SVG animados da Aula 13, a partir dos números medidos.

Os números vêm de `tools/graficos_aula13.py`, que lê os CSVs de `dados/`, e as
mesmas contas estão travadas em `tools/tests/test_revisao_aula13.py`. Nenhum SVG
desenha dado ilustrativo:

1. `disponibilidade`: a linha do tempo de uma previsão do mês t. Cada coluna da
   base mensal acende no momento em que passa a existir, e o cursor para na
   linha do momento da previsão. As colunas que só existem depois dela são as
   que vazam.
2. `divisao`: os 116 trimestres da regressão simples, com os 24 de teste
   escolhidos por sorteio (`random_state=42`) e por data. Os R2 de teste das
   duas divisões aparecem no fim.
3. `matriz`: os 24 meses de teste da regressão logística da Aula 09 são
   classificados um a um, e cada um cai na sua célula da matriz de confusão.
4. `limiar`: as 24 probabilidades da mesma regressão logística, com o limiar
   passando por 0,4, 0,5, 0,6 e 0,7 e os erros de cada tipo marcados.

Por que CSS e não SMIL, como na Aula 05: o SMIL ignora `prefers-reduced-motion`,
e a Aula 13 precisava respeitar essa preferência. As regras de animação moram
num bloco `<style>` do próprio deck, e não no tema, pelo mesmo motivo da Aula
05: animação de uma aula não pertence ao tema das 14.

**O estado sem animação é o estado final.** Todo elemento é desenhado já no seu
estado final, e a animação só existe dentro de `section.present`. Na impressão,
no `?print-pdf` e com movimento reduzido nenhuma regra de animação se aplica, e
o slide mostra a leitura completa. O limiar, que é um ciclo, mostra o de 0,5.

Uso:
    python3 tools/svg_aula13.py            # escreve os quatro blocos no deck
    python3 tools/svg_aula13.py --mostrar  # imprime, sem tocar no arquivo

O deck marca cada bloco com <!-- svg:nome --> e <!-- /svg:nome -->, e o script
substitui apenas o miolo, então rodar de novo é idempotente.
"""
import os
import re
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from graficos_aula13 import (LIMIARES, base_trimestral,  # noqa: E402
                             medir_classificacao, medir_regressao_simples, metricas)

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECK = os.path.join(RAIZ, "aulas", "aula13.html")
L = 1120

MESES = ["jan", "fev", "mar", "abr", "mai", "jun",
         "jul", "ago", "set", "out", "nov", "dez"]


def _num(formato, *valores):
    return (formato % valores).replace(".", ",")


def _texto(x, y, txt, tam=18, cor="var(--seg-texto)", anc="start", peso="400", extra=""):
    return ('<text x="%.1f" y="%.1f" font-size="%d" fill="%s" text-anchor="%s" '
            'font-weight="%s"%s>%s</text>' % (x, y, tam, cor, anc, peso, extra, txt))


def _atraso(segundos):
    return ' style="animation-delay: %.2fs"' % segundos


# ---------------------------------------------------------------- 1. disponibilidade
def svg_disponibilidade():
    alt = 330
    esq, dir_ = 330, 1100
    marcos = [("t-12", 380), ("t-3", 560), ("t-2", 660), ("t-1", 760), ("t publicado", 980)]
    previsao = 870
    linhas = [
        ("sen, cos e dias do mês t", esq, "var(--seg-secundaria)"),
        ("lag12: frangos em t-12", 380, "var(--seg-secundaria)"),
        ("lag3: frangos em t-3", 560, "var(--seg-secundaria)"),
        ("lag2: frangos em t-2", 660, "var(--seg-secundaria)"),
        ("lag1 e as quatro séries em t-1", 760, "var(--seg-secundaria)"),
        ("as quatro séries no mês t", 980, "var(--seg-destaque)"),
        ("y: frangos no mês t", 980, "var(--seg-primaria)"),
    ]
    dur = 6.0
    p = ['<svg viewBox="0 0 %d %d" width="100%%" height="%d" role="img" '
         'aria-label="Linha do tempo de uma previsão do abate de frangos do mês t. O calendário '
         'existe desde sempre, as defasagens acendem uma a uma até o mês anterior, e o momento '
         'da previsão fica antes da publicação do mês t. As quatro outras séries do mês t e o '
         'próprio alvo só existem depois dessa linha.">' % (L, alt, alt)]
    topo, passo = 44, 36
    for i, (rotulo, inicio, cor) in enumerate(linhas):
        y = topo + i * passo
        p.append(_texto(20, y + 16, rotulo, tam=18))
        p.append('<rect x="%d" y="%d" width="%d" height="22" rx="4" fill="var(--seg-superficie)"/>'
                 % (esq, y, dir_ - esq))
        atraso = (inicio - esq) / (dir_ - esq) * dur
        p.append('<rect class="a13-acende" x="%d" y="%d" width="%d" height="22" rx="4" '
                 'fill="%s"%s/>' % (inicio, y, dir_ - inicio, cor, _atraso(atraso)))
    base_y = topo + len(linhas) * passo + 4
    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="var(--seg-borda)" stroke-width="2"/>'
             % (esq, base_y, dir_, base_y))
    for rotulo, x in marcos:
        p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="var(--seg-borda)" '
                 'stroke-width="2"/>' % (x, base_y, x, base_y + 8))
        p.append(_texto(x, base_y + 30, rotulo, tam=18, anc="middle"))
    p.append('<line x1="%d" y1="22" x2="%d" y2="%d" stroke="var(--seg-destaque)" '
             'stroke-width="3" stroke-dasharray="7 5"/>' % (previsao, previsao, base_y))
    p.append(_texto(previsao, 16, "momento da previsão", tam=18, anc="middle",
                    cor="var(--seg-destaque)", peso="700"))
    p.append('<line class="a13-cursor" x1="%d" y1="30" x2="%d" y2="%d" '
             'stroke="var(--seg-primaria)" stroke-width="3"/>' % (esq, esq, base_y))
    p.append('</svg>')
    return "\n".join(p)


# ---------------------------------------------------------------- 2. divisao
def svg_divisao(df, s):
    alt = 262
    esq, dir_ = 200, 1100
    n = len(df)
    w = (dir_ - esq) / n
    aleatorio = s["idx_teste_aleatorio"]
    cronologico = list(range(n - s["teste"], n))
    ordem = list(np.random.default_rng(7).permutation(aleatorio))

    p = ['<svg viewBox="0 0 %d %d" width="100%%" height="%d" role="img" '
         'aria-label="Os 116 trimestres da regressão simples em duas faixas. Na de cima, os 24 '
         'trimestres de teste são sorteados e ficam espalhados entre os de treino, com R2 de '
         'teste %s. Na de baixo, os 24 de teste são os últimos, a partir de %s, com R2 de '
         'teste %s.">' % (L, alt, alt, _num("%.2f", s["r2_aleatorio"]),
                           s["corte_cronologico"], _num("%.2f", s["r2_cronologico"]))]
    faixas = [("sorteio 80/20", 58, aleatorio, lambda i: 0.3 + ordem.index(i) * 0.12,
               "R² de teste " + _num("%.2f", s["r2_aleatorio"])),
              ("corte por data", 160, cronologico, lambda i: 3.6 + (i - cronologico[0]) * 0.06,
               "R² de teste " + _num("%.2f", s["r2_cronologico"]))]
    for rotulo, y, teste, atraso, r2 in faixas:
        p.append(_texto(20, y + 36, rotulo, tam=18, peso="700"))
        for i in range(n):
            if i in teste:
                p.append('<rect class="a13-acende" x="%.1f" y="%d" width="%.1f" height="60" '
                         'fill="var(--seg-destaque)"%s/>' % (esq + i * w, y, w - 1.4,
                                                             _atraso(atraso(i))))
            else:
                p.append('<rect x="%.1f" y="%d" width="%.1f" height="60" '
                         'fill="var(--seg-primaria)"/>' % (esq + i * w, y, w - 1.4))
        p.append(_texto(dir_, y - 10, r2, tam=18, anc="end", peso="700",
                        extra=' class="a13-acende"' + _atraso(5.2)))
    for ano in (2000, 2010, 2020):
        i = list(df["periodo"]).index("%d-T1" % ano)
        x = esq + i * w
        p.append('<line x1="%.1f" y1="224" x2="%.1f" y2="232" stroke="var(--seg-borda)" '
                 'stroke-width="2"/>' % (x, x))
        p.append(_texto(x, 254, str(ano), tam=18, anc="middle"))
    p.append(_texto(20, 20, "roxo: treino · coral: teste", tam=18))
    p.append('</svg>')
    return "\n".join(p)


# ---------------------------------------------------------------- 3. matriz
CLASSE = {(1, 1): "TP", (1, 0): "FN", (0, 1): "FP", (0, 0): "TN"}
COR = {"TP": "var(--seg-primaria)", "TN": "var(--seg-secundaria)",
       "FP": "var(--seg-destaque)", "FN": "var(--seg-destaque)"}
TINTA = {"TP": "var(--inteli-branco)", "TN": "var(--seg-texto)",
         "FP": "var(--seg-texto)", "FN": "var(--seg-texto)"}


def svg_matriz(c):
    alt = 318
    passo = 0.25
    reais, prevs, periodos = c["real"], c["prev_logistica"], c["periodos"]
    cont = c["logistica"]
    p = ['<svg viewBox="0 0 %d %d" width="100%%" height="%d" role="img" '
         'aria-label="Os 24 meses de teste da regressão logística, classificados um a um. '
         '%d TP, %d FN, %d FP e %d TN, com 20 meses reais de alta e 4 de queda.">'
         % (L, alt, alt, cont["tp"], cont["fn"], cont["fp"], cont["tn"])]
    # ladrilhos dos 24 meses
    for i, (per, r, pr) in enumerate(zip(periodos, reais, prevs)):
        classe = CLASSE[(r, pr)]
        x = 20 + (i % 6) * 96
        y = 20 + (i // 6) * 72
        ano, mes = per.split("-")
        fundo = COR[classe]
        estilo = ' stroke="var(--seg-destaque)" stroke-width="3"' if classe == "FN" else ""
        preench = "var(--seg-base)" if classe == "FN" else fundo
        p.append('<g class="a13-acende"%s>' % _atraso(i * passo))
        p.append('<rect x="%d" y="%d" width="88" height="62" rx="6" fill="%s"%s/>'
                 % (x, y, preench, estilo))
        tinta = "var(--seg-texto)" if classe == "FN" else TINTA[classe]
        p.append(_texto(x + 44, y + 25, "%s/%s" % (MESES[int(mes) - 1], ano[2:]),
                        tam=18, anc="middle", cor=tinta))
        p.append(_texto(x + 44, y + 51, classe, tam=20, anc="middle", cor=tinta, peso="700"))
        p.append('</g>')
    # matriz
    x0, y0, cw, ch = 720, 52, 150, 100
    p.append(_texto(x0 + cw, 22, "previsto", tam=18, anc="middle", peso="700"))
    p.append(_texto(x0 + cw / 2, 44, "alta", tam=18, anc="middle"))
    p.append(_texto(x0 + cw * 1.5, 44, "queda", tam=18, anc="middle"))
    p.append(_texto(x0 - 12, y0 + ch / 2 + 6, "real alta", tam=18, anc="end"))
    p.append(_texto(x0 - 12, y0 + ch * 1.5 + 6, "real queda", tam=18, anc="end"))
    celula = {"TP": (0, 0), "FN": (0, 1), "FP": (1, 0), "TN": (1, 1)}
    for classe, (lin, col) in celula.items():
        cx, cy = x0 + col * cw, y0 + lin * ch
        p.append('<rect x="%d" y="%d" width="%d" height="%d" fill="var(--seg-superficie)" '
                 'stroke="var(--seg-borda)" stroke-width="2"/>' % (cx, cy, cw, ch))
        p.append(_texto(cx + 10, cy + 22, classe, tam=18, peso="700"))
        k = 0
        for i, (r, pr) in enumerate(zip(reais, prevs)):
            if CLASSE[(r, pr)] != classe:
                continue
            px, py = cx + 70 + (k % 6) * 12, cy + 16 + (k // 6) * 12
            p.append('<circle class="a13-acende" cx="%d" cy="%d" r="4.5" fill="%s"%s/>'
                     % (px, py, COR[classe], _atraso(i * passo)))
            k += 1
        p.append(_texto(cx + cw / 2, cy + 84, str(cont[classe.lower()]), tam=30,
                        anc="middle", peso="700",
                        extra=' class="a13-acende"' + _atraso(24 * passo)))
    tot_real = [cont["tp"] + cont["fn"], cont["fp"] + cont["tn"]]
    tot_prev = [cont["tp"] + cont["fp"], cont["fn"] + cont["tn"]]
    for lin, v in enumerate(tot_real):
        p.append(_texto(x0 + 2 * cw + 14, y0 + lin * ch + ch / 2 + 7, str(v), tam=20, peso="700"))
    for col, v in enumerate(tot_prev):
        p.append(_texto(x0 + col * cw + cw / 2, y0 + 2 * ch + 28, str(v), tam=20,
                        anc="middle", peso="700"))
    p.append(_texto(x0 + 2 * cw + 14, y0 + 2 * ch + 28, "24", tam=20, peso="700"))
    p.append('</svg>')
    return "\n".join(p)


# ---------------------------------------------------------------- 4. limiar
def svg_limiar(c):
    alt = 250
    esq, dir_ = 150, 1090
    lo, hi = 0.2, 1.0
    px = lambda v: esq + (dir_ - esq) * (v - lo) / (hi - lo)  # noqa: E731
    prob, real = c["prob"], c["real"]
    lanes = {1: 70, 0: 150}
    p = ['<svg viewBox="0 0 %d %d" width="100%%" height="%d" role="img" '
         'aria-label="As 24 probabilidades de alta da regressão logística, em duas faixas pelo '
         'resultado real. O limiar passa por 0,4, 0,5, 0,6 e 0,7, e os erros de cada limiar '
         'ficam circulados.">' % (L, alt, alt)]
    p.append(_texto(20, lanes[1] + 6, "real alta", tam=18, peso="700"))
    p.append(_texto(20, lanes[0] + 6, "real queda", tam=18, peso="700"))
    base_y = 196
    p.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="var(--seg-borda)" stroke-width="2"/>'
             % (esq, base_y, dir_, base_y))
    for v in (0.2, 0.4, 0.6, 0.8, 1.0):
        p.append(_texto(px(v), base_y + 26, _num("%.1f", v), tam=18, anc="middle"))
    p.append(_texto(dir_, base_y + 50, "probabilidade de alta", tam=18, anc="end"))
    posicoes = []
    for pr, r in zip(prob, real):
        x = px(pr)
        # empilha verticalmente os pontos que cairiam a menos de 18px de outro
        vizinhos = sum(1 for (ox, _, _, orr) in posicoes if orr == r and abs(ox - x) < 18)
        y = lanes[r] + (-18 if vizinhos % 2 else 18) * ((vizinhos + 1) // 2)
        posicoes.append((x, y, pr, r))
        cor = "var(--seg-primaria)" if r == 1 else "var(--seg-destaque)"
        p.append('<circle cx="%.1f" cy="%.1f" r="8" fill="%s"/>' % (x, y, cor))
    for k, t in enumerate(LIMIARES):
        padrao = " a13-padrao" if abs(t - 0.5) < 1e-9 else ""
        cont = c["limiares"][t]
        met = metricas(cont)
        p.append('<g class="a13-etapa a13-etapa-%d%s">' % (k, padrao))
        x = px(t)
        p.append('<rect x="%.1f" y="30" width="%.1f" height="%d" fill="var(--seg-secundaria)" '
                 'opacity="0.25"/>' % (x, dir_ - x, base_y - 30))
        p.append('<line x1="%.1f" y1="24" x2="%.1f" y2="%d" stroke="var(--seg-primaria)" '
                 'stroke-width="3"/>' % (x, x, base_y))
        p.append(_texto(x, 18, "limiar " + _num("%.1f", t), tam=18, anc="middle", peso="700"))
        for (cx, cy, pr, r) in posicoes:
            erro = (r == 1 and pr < t) or (r == 0 and pr >= t)
            if erro:
                p.append('<circle cx="%.1f" cy="%.1f" r="13" fill="none" '
                         'stroke="var(--seg-destaque)" stroke-width="3"/>' % (cx, cy))
        # a leitura fica abaixo do eixo, à esquerda: no topo ela colidia com o
        # rótulo do limiar quando o limiar passa de 0,6
        p.append(_texto(esq, base_y + 50, "FP %d · FN %d · precisão %s · revocação %s"
                        % (cont["fp"], cont["fn"], _num("%.2f", met["precisao"]),
                           _num("%.2f", met["revocacao"])),
                        tam=18, anc="start", peso="700"))
        p.append('</g>')
    p.append('</svg>')
    return "\n".join(p)


def blocos():
    df = base_trimestral()
    simples = medir_regressao_simples(df)
    clf = medir_classificacao()
    return {
        "disponibilidade": svg_disponibilidade(),
        "divisao": svg_divisao(df, simples),
        "matriz": svg_matriz(clf),
        "limiar": svg_limiar(clf),
    }


def main(argv):
    gerados = blocos()
    if "--mostrar" in argv:
        for nome, svg in gerados.items():
            print("<!-- %s -->\n%s\n" % (nome, svg))
        return 0
    with open(DECK, encoding="utf-8") as fh:
        html = fh.read()
    for nome, svg in gerados.items():
        padrao = re.compile(r"(<!-- svg:%s -->)(.*?)(<!-- /svg:%s -->)" % (nome, nome), re.S)
        if not padrao.search(html):
            raise SystemExit("marcador <!-- svg:%s --> não encontrado no deck" % nome)
        html = padrao.sub(lambda m: m.group(1) + "\n" + svg + "\n" + m.group(3), html)
    with open(DECK, "w", encoding="utf-8") as fh:
        fh.write(html)
    print("quatro SVG escritos em", os.path.relpath(DECK, RAIZ))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

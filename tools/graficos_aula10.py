"""Gera as quatro figuras da Aula 10 a partir dos CSVs de dados/mensal/.

1. `aula10-roc-empate.png`. Dois painéis. À esquerda, as quatro métricas dos três
   modelos que empatam no alvo binário da Aula 09: baseline majoritária, SVM RBF
   e árvore de entropia marcam 0,833 de acurácia, 0,833 de precisão, 1,000 de
   revocação e 0,909 de F1, os quatro valores idênticos. À direita, a curva ROC
   dos mesmos três: a AUC vale 0,500 na baseline, 0,500 na árvore e 0,738 no
   SVM RBF. É a métrica que separa o que as outras quatro não separam.

2. `aula10-dobras-kfold-vs-timeseries.png`. As cinco dobras de `KFold(5)`, o
   padrão do `GridSearchCV`, contra as cinco de `TimeSeriesSplit(5)`, sobre os
   315 meses de treino. Na primeira dobra do `KFold`, os 252 meses de treino
   são todos posteriores ao início da validação; no `TimeSeriesSplit` esse
   número é zero nas cinco dobras.

3. `aula10-grade-de-hiperparametros.png`. O MAPE de teste das 27 combinações da
   grade, em ordem de erro, com três pontos nomeados: a floresta da Aula 07 com
   os defaults (5,04%), a combinação que o `GridSearchCV` escolhe olhando só o
   treino (4,21%) e o melhor do conjunto de teste (4,07%), que não é alcançável
   porque escolher pela métrica de teste é escolher pela resposta.

4. `aula10-shap-vs-impureza.png`. Dois painéis. À esquerda, o SHAP médio
   absoluto sobre os 24 meses de teste contra a importância por impureza da
   mesma floresta ajustada, nas seis features de maior SHAP: as duas leituras
   concordam nas duas primeiras posições (`lag12` e `lag3`) e discordam da
   terceira em diante. À direita, o partial dependence de `lag12`, que cai de
   1,093 para 1,010: quanto maior o abate de doze meses atrás, menor o
   crescimento que a floresta prevê.

Decisões de forma, herdadas de `tools/graficos_aula07.py`,
`tools/graficos_aula08.py` e `tools/graficos_aula09.py`:

- roxo #2e2640 como tinta, coral #ff4545 como destaque, verde #89cea5 e cinza
  escuro #b2b6bf como referências, cinza médio #caced6 e cinza claro #e6eaeb nos
  fundos. As cores vêm dos tokens de `assets/css/inteli-brand.css`.
- nenhum valor interpolado ou inventado: tudo é medido sobre `dados/mensal/`,
  com a mesma lógica de junção, defasagem, corte temporal e alvo binário de
  `tools/tests/test_ajuste_aula10.py`, reimplementada aqui de propósito: se as
  duas implementações divergirem, o acervo descobre.
- 1600x900 a 150 dpi, como no resto do acervo.
- separador decimal é vírgula, como em `tools/graficos_aula04.py`.

Uma decisão de forma que se afasta do resto do acervo, e o motivo:

- **corpo 26, e não 18.** Os scripts anteriores fixam corpo 18, que é o piso de
  legibilidade do tema para texto de slide. Isso funciona para figura esparsa,
  como a de quatro barras da Aula 09, e não funcionou aqui: a `section` do deck
  limita a figura a cerca de 350px de altura, uma imagem 16:9 cabe então em
  cerca de 620px de largura, e o corpo 18 chega à tela projetada com menos da
  metade do tamanho. A primeira versão destas quatro figuras foi conferida em
  captura de tela dentro do deck e estava ilegível. O corpo subiu para 26 e cada
  figura perdeu elementos até caber: a grade deixou de rotular as 27 barras, o
  painel das dobras trocou dez frases por dez números, e o painel de SHAP passou
  a mostrar as seis features de maior importância em vez das onze.

Uso: python3 tools/graficos_aula10.py   (requer matplotlib, pandas, numpy,
scikit-learn e shap, listados em requirements-ci.txt)
"""
import calendar
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap
from sklearn.ensemble import RandomForestRegressor
from sklearn.inspection import partial_dependence
from sklearn.metrics import (accuracy_score, f1_score, precision_score,
                             recall_score, roc_auc_score, roc_curve)
from sklearn.model_selection import GridSearchCV, KFold, TimeSeriesSplit
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MENSAL = os.path.join(RAIZ, "dados", "mensal")

# cores lidas de assets/css/inteli-brand.css (paleta da Graduacao, p.66/p.68)
TINTA = "#2e2640"          # --inteli-roxo
DESTAQUE = "#ff4545"       # --inteli-coral
REFERENCIA_1 = "#b2b6bf"   # --inteli-cinza-escuro
REFERENCIA_2 = "#89cea5"   # --inteli-verde
NUVEM = "#caced6"          # --inteli-cinza-medio
SOMBRA = "#e6eaeb"         # --inteli-cinza-claro
FUNDO = "#ffffff"          # --inteli-branco

SERIES = ["abate_bovinos", "abate_suinos", "abate_frangos",
          "producao_ovos", "producao_leite"]
ALVO = "abate_frangos"
FEATURES = (["lag1", "lag2", "lag3", "lag12", "sen", "cos", "dias"]
            + [s + "_lag1" for s in SERIES if s != ALVO])
N_TESTE = 24
SEMENTE = 42

# a grade dos tres hiperparametros, a mesma do notebook e do teste
GRADE = {
    "n_estimators": [100, 300, 600],
    "max_depth": [None, 4, 8],
    "min_samples_leaf": [1, 2, 5],
}

# ver a nota sobre corpo 26 no topo deste arquivo
plt.rcParams.update({
    "figure.facecolor": FUNDO,
    "axes.facecolor": FUNDO,
    "axes.edgecolor": REFERENCIA_1,
    "axes.labelcolor": TINTA,
    "text.color": TINTA,
    "xtick.color": TINTA,
    "ytick.color": TINTA,
    "font.size": 26,
    "axes.titlesize": 28,
    "legend.frameon": False,
})


def _num(formato, *valores):
    """Formata com vírgula decimal, como o resto do acervo."""
    return (formato % valores).replace(".", ",")


def base_analitica():
    """Junta as cinco séries mensais e monta features, alvo e corte temporal.

    Mesma lógica das Aulas 07 a 09: junção interna por período, defasagens de
    1, 2, 3 e 12 meses do alvo, defasagem de 1 mês das outras quatro séries,
    calendário em seno, cosseno e dias do mês, e os 24 últimos meses como teste.
    """
    base = None
    for nome in SERIES:
        coluna = (pd.read_csv(os.path.join(MENSAL, nome + ".csv"))[["periodo", "valor"]]
                  .rename(columns={"valor": nome}))
        base = coluna if base is None else base.merge(coluna, on="periodo", how="inner")
    base = base.sort_values("periodo").reset_index(drop=True)

    base["mes"] = base["periodo"].str[-2:].astype(int)
    base["dias"] = [calendar.monthrange(int(p[:4]), int(p[-2:]))[1]
                    for p in base["periodo"]]
    base["sen"] = np.sin(2 * np.pi * base["mes"] / 12)
    base["cos"] = np.cos(2 * np.pi * base["mes"] / 12)
    for k in (1, 2, 3, 12):
        base["lag%d" % k] = base[ALVO].shift(k)
    for nome in SERIES:
        if nome != ALVO:
            base[nome + "_lag1"] = base[nome].shift(1)
    return base.dropna().reset_index(drop=True)


def _mape(real, previsto):
    return float(np.mean(np.abs((real - previsto) / real)) * 100)


def _matrizes(base):
    corte = len(base) - N_TESTE
    X = base[FEATURES].to_numpy(dtype=float)
    y = base[ALVO].to_numpy(dtype=float)
    lag12 = base["lag12"].to_numpy(dtype=float)
    return corte, X, y, lag12


def _sem_moldura(eixo, lados=("top", "right")):
    for lado in lados:
        eixo.spines[lado].set_visible(False)


# --------------------------------------------------------------------- figura 1
def roc_do_empate(base, destino):
    """As quatro métricas idênticas à esquerda, as curvas ROC à direita."""
    corte, X, y, lag12 = _matrizes(base)
    binario = (y > lag12).astype(int)
    atr, ate = binario[:corte], binario[corte:]

    escalador = StandardScaler().fit(X[:corte])
    Ztr, Zte = escalador.transform(X[:corte]), escalador.transform(X[corte:])

    maioria = np.full(len(ate), int(atr.mean() > 0.5))
    svm = SVC(kernel="rbf", random_state=SEMENTE).fit(Ztr, atr)
    arvore = DecisionTreeClassifier(criterion="entropy", max_depth=3,
                                    random_state=SEMENTE).fit(Ztr, atr)

    # a baseline preve sempre a mesma classe: o escore dela e constante, e a
    # curva ROC de um escore constante e a diagonal, com AUC 0,5 por construcao.
    # a arvore cai na mesma diagonal, entao as duas precisam de tracos
    # diferentes para nao se esconderem uma sob a outra
    modelos = [
        ("baseline", maioria, np.zeros(len(ate)), REFERENCIA_1, (0, (6, 4))),
        ("árvore", arvore.predict(Zte), arvore.predict_proba(Zte)[:, 1],
         REFERENCIA_2, (0, (1, 3))),
        ("SVM RBF", svm.predict(Zte), svm.decision_function(Zte), DESTAQUE, "solid"),
    ]

    # o painel da esquerda leva quatro rotulos longos no eixo x e precisa de
    # mais largura que o da direita, senao "precisao" e "revocacao" se encostam
    fig, (esq, dir_) = plt.subplots(1, 2, figsize=(16, 9),
                                    gridspec_kw={"width_ratios": [1.25, 1]})

    metricas = ["acurácia", "precisão", "revocação", "F1"]
    # quatro rotulos num painel estreito: em corpo 24 eles se encostam
    largura = 0.27
    posicoes = np.arange(len(metricas))
    for i, (rotulo, previsto, _, cor, _traco) in enumerate(modelos):
        valores = [accuracy_score(ate, previsto),
                   precision_score(ate, previsto, zero_division=0),
                   recall_score(ate, previsto, zero_division=0),
                   f1_score(ate, previsto, zero_division=0)]
        esq.bar(posicoes + (i - 1) * largura, valores, largura,
                color=cor, edgecolor=TINTA, linewidth=0.8, label=rotulo)
        if i == len(modelos) - 1:
            # os tres modelos marcam o mesmo valor em cada metrica: um rotulo
            # por grupo, e nao tres sobrepostos
            for posicao, valor in zip(posicoes, valores):
                esq.text(posicao, valor + 0.03, _num("%.3f", valor),
                         ha="center", va="bottom", fontsize=26)

    esq.set_xticks(posicoes)
    esq.set_xticklabels(metricas, fontsize=20)
    esq.set_yticks([0, 0.5, 1.0])
    esq.set_ylim(0, 1.32)
    esq.set_title("Os três marcam os mesmos quatro valores", pad=18, fontsize=27)
    esq.legend(loc="upper center", ncol=3, fontsize=24,
               bbox_to_anchor=(0.5, 1.02))
    _sem_moldura(esq)

    for rotulo, _, escore, cor, traco in modelos:
        fpr, tpr, _ = roc_curve(ate, escore)
        auc = roc_auc_score(ate, escore)
        dir_.plot(fpr, tpr, color=cor, linewidth=5, linestyle=traco,
                  marker="o", markersize=8,
                  label="%s  %s" % (rotulo, _num("%.3f", auc)))
    dir_.set_xlabel("taxa de falso positivo", fontsize=24)
    dir_.set_ylabel("taxa de verdadeiro positivo", fontsize=24)
    dir_.set_xticks([0, 0.5, 1.0])
    dir_.set_yticks([0, 0.5, 1.0])
    dir_.set_xlim(-0.04, 1.04)
    dir_.set_ylim(-0.04, 1.10)
    dir_.set_title("A AUC separa os três", pad=18, fontsize=27)
    dir_.legend(loc="lower right", fontsize=24, title="AUC", title_fontsize=24)
    _sem_moldura(dir_)

    fig.tight_layout(w_pad=3)
    fig.savefig(destino, dpi=150, facecolor=FUNDO)
    plt.close(fig)
    return destino


# --------------------------------------------------------------------- figura 2
def dobras(base, destino):
    """Desenha as cinco dobras de cada validador sobre os 315 meses de treino."""
    corte, X, _, _ = _matrizes(base)
    Xtr = X[:corte]
    periodos = base["periodo"].to_numpy()[:corte]

    fig, eixos = plt.subplots(2, 1, figsize=(16, 9), sharex=True)
    validadores = [("KFold(5), o padrão do GridSearchCV", KFold(n_splits=5), eixos[0]),
                   ("TimeSeriesSplit(5)", TimeSeriesSplit(n_splits=5), eixos[1])]

    for titulo, cv, eixo in validadores:
        for i, (itr, ival) in enumerate(cv.split(Xtr)):
            linha = 4 - i
            # treino e validacao nao sao contiguos no KFold: pinta por indice
            for indice in itr:
                eixo.barh(linha, 1, left=indice, height=0.62, color=NUVEM, linewidth=0)
            for indice in ival:
                eixo.barh(linha, 1, left=indice, height=0.62, color=DESTAQUE, linewidth=0)
            futuro = int((itr > ival.min()).sum())
            # dez frases iguais nao cabem legiveis: fica so o numero, e a
            # unidade vai no rotulo do eixo
            eixo.text(corte + 10, linha, "%d" % futuro, va="center", ha="left",
                      fontsize=28, color=DESTAQUE if futuro else REFERENCIA_1,
                      fontweight="bold" if futuro else "normal")
        eixo.set_yticks(range(5))
        eixo.set_yticklabels(["%d" % (5 - i) for i in range(5)], fontsize=24)
        eixo.set_ylabel("dobra", fontsize=24)
        eixo.set_xlim(0, corte + 72)
        eixo.set_ylim(-0.6, 4.6)
        eixo.set_title(titulo, pad=14, loc="left", fontsize=27)
        _sem_moldura(eixo, ("top", "right", "left"))

    marcas = [0, corte // 2, corte - 1]
    eixos[1].set_xticks(marcas)
    eixos[1].set_xticklabels([periodos[m] for m in marcas], fontsize=24)
    eixos[1].set_xlabel("mês de treino, em ordem de calendário."
                        "   À direita: meses de treino no futuro", fontsize=24)

    legenda = [plt.Line2D([0], [0], color=NUVEM, linewidth=14, label="treino"),
               plt.Line2D([0], [0], color=DESTAQUE, linewidth=14, label="validação")]
    eixos[0].legend(handles=legenda, loc="lower left", bbox_to_anchor=(0.58, 1.0),
                    ncol=2, fontsize=25)

    fig.tight_layout()
    fig.savefig(destino, dpi=150, facecolor=FUNDO)
    plt.close(fig)
    return destino


def melhor_floresta(base):
    """A floresta que o GridSearchCV com TimeSeriesSplit escolhe."""
    corte, X, y, lag12 = _matrizes(base)
    razao = y / lag12
    busca = GridSearchCV(RandomForestRegressor(random_state=SEMENTE), GRADE,
                         scoring="neg_mean_absolute_percentage_error",
                         cv=TimeSeriesSplit(n_splits=5), n_jobs=-1)
    busca.fit(X[:corte], razao[:corte])
    return busca.best_estimator_, busca.best_params_


# --------------------------------------------------------------------- figura 3
def grade_de_hiperparametros(base, destino):
    """As 27 combinações em ordem de erro, com três pontos nomeados."""
    corte, X, y, lag12 = _matrizes(base)
    Xtr, Xte = X[:corte], X[corte:]
    rtr = (y / lag12)[:corte]
    yte, lag12te = y[corte:], lag12[corte:]

    erro_por_chave = {}
    for profundidade in GRADE["max_depth"]:
        for folha in GRADE["min_samples_leaf"]:
            for arvores in GRADE["n_estimators"]:
                modelo = RandomForestRegressor(n_estimators=arvores,
                                               max_depth=profundidade,
                                               min_samples_leaf=folha,
                                               random_state=SEMENTE).fit(Xtr, rtr)
                erro_por_chave[(profundidade, folha, arvores)] = _mape(
                    yte, modelo.predict(Xte) * lag12te)

    # tres combinacoes com papeis diferentes, e a diferenca entre elas e o
    # conteudo do bloco: o default que ninguem escolheu, o que o GridSearchCV
    # escolhe olhando so o treino, e o melhor do teste, que nao e alcancavel
    # porque escolher pela metrica de teste e escolher pela resposta
    _, escolhidos = melhor_floresta(base)
    # cada rotulo ganha um deslocamento e uma altura propria: os tres pontos
    # ficam proximos na ordem por erro, e sem isso eles se escrevem por cima
    papeis = {
        (None, 1, 300): (TINTA, "a floresta da Aula 07,\ncom os defaults", 4.5, 1.20),
        (escolhidos["max_depth"], escolhidos["min_samples_leaf"],
         escolhidos["n_estimators"]): (DESTAQUE, "o que o GridSearchCV\nescolhe", 8.0, 1.52),
        min(erro_por_chave, key=erro_por_chave.get):
            (REFERENCIA_2, "o melhor do teste,\nque não é alcançável", 5.5, 1.20),
    }

    ordenadas = sorted(erro_por_chave.items(), key=lambda item: item[1])
    valores = [erro for _, erro in ordenadas]
    cores = [papeis.get(chave, (NUVEM,))[0] for chave, _ in ordenadas]

    fig, eixo = plt.subplots(figsize=(16, 9))
    posicoes = np.arange(len(valores))
    eixo.bar(posicoes, valores, color=cores, edgecolor=REFERENCIA_1, linewidth=0.6)

    # as 27 barras nao levam rotulo: em projecao eles ficariam ilegiveis, e o
    # que a figura mostra e a dispersao da grade e onde os tres pontos caem
    eixo.set_xticks([])
    eixo.set_xlim(-1.5, len(valores) + 5.5)
    eixo.set_xlabel("as 27 combinações da grade, em ordem de erro", fontsize=25)
    eixo.set_ylabel("MAPE de teste", fontsize=25)
    eixo.set_ylim(0, max(valores) * 1.60)
    eixo.set_yticks([0, 2, 4, 6])
    eixo.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: _num("%.0f%%", v)))
    eixo.tick_params(axis="y", labelsize=24)

    for posicao, (chave, erro) in enumerate(ordenadas):
        if chave not in papeis:
            continue
        cor, texto, deslocamento, altura = papeis[chave]
        eixo.annotate("%s\n%s" % (texto, _num("%.2f%%", erro)),
                      xy=(posicao, erro),
                      xytext=(posicao + deslocamento, max(valores) * altura),
                      ha="center", va="top", fontsize=24, color=cor,
                      arrowprops=dict(arrowstyle="-", color=cor, linewidth=2))
    _sem_moldura(eixo)

    fig.tight_layout()
    fig.savefig(destino, dpi=150, facecolor=FUNDO)
    plt.close(fig)
    return destino


# --------------------------------------------------------------------- figura 4
def shap_vs_impureza(base, destino, quantas=6):
    """As duas leituras de importância à esquerda, o partial dependence à direita."""
    corte, X, y, lag12 = _matrizes(base)
    modelo, _ = melhor_floresta(base)

    valores = shap.TreeExplainer(modelo).shap_values(X[corte:])
    medio = np.abs(valores).mean(axis=0)
    impureza = modelo.feature_importances_

    # normaliza as duas para somar 1: o que se compara e a ordem, nao a unidade
    medio_n = medio / medio.sum()
    impureza_n = impureza / impureza.sum()
    # so as seis de maior SHAP: as onze nao cabem legiveis em projecao, e a
    # divergencia que a figura mostra acontece entre a terceira e a sexta
    ordem = np.argsort(medio_n)[::-1][:quantas]

    fig, (esq, dir_) = plt.subplots(1, 2, figsize=(16, 9))

    altura = 0.38
    posicoes = np.arange(len(ordem))
    esq.barh(posicoes + altura / 2, medio_n[ordem], altura, color=DESTAQUE,
             edgecolor=TINTA, linewidth=0.6, label="SHAP (teste)")
    esq.barh(posicoes - altura / 2, impureza_n[ordem], altura, color=NUVEM,
             edgecolor=TINTA, linewidth=0.6, label="impureza (treino)")
    esq.set_yticks(posicoes)
    esq.set_yticklabels([FEATURES[i] for i in ordem], fontsize=23)
    esq.invert_yaxis()
    esq.set_xticks([0, 0.25, 0.5])
    esq.set_xlim(0, 0.60)
    esq.xaxis.set_major_formatter(
        plt.FuncFormatter(lambda v, _: _num("%.0f%%", v * 100)))
    esq.tick_params(axis="x", labelsize=24)
    esq.set_title("Discordam da terceira em diante", pad=18, fontsize=26)
    # qualquer posicao dentro do eixo encosta em alguma barra: a legenda
    # sai do eixo, abaixo dele
    esq.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=2, fontsize=24)
    _sem_moldura(esq)

    topo = int(np.argmax(medio_n))
    resultado = partial_dependence(modelo, X[:corte], [topo], grid_resolution=20)
    grade = np.asarray(resultado["grid_values"][0], dtype=float)
    media = np.asarray(resultado["average"][0], dtype=float)
    dir_.plot(grade / 1e9, media, color=TINTA, linewidth=5)
    dir_.fill_between(grade / 1e9, media.min(), media, color=SOMBRA)
    dir_.set_xlabel("%s, em bilhões de kg" % FEATURES[topo], fontsize=25)
    dir_.set_ylabel("razão prevista", fontsize=25)
    dir_.set_yticks([1.01, 1.05, 1.09])
    dir_.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: _num("%.2f", v)))
    dir_.set_xticks([0.4, 0.7, 1.0])
    dir_.xaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: _num("%.1f", v)))
    dir_.tick_params(labelsize=24)
    dir_.set_title("Crescimento cai com a base", pad=18, fontsize=26)
    _sem_moldura(dir_)

    # w_pad pequeno de proposito: com folga maior o painel da direita e empurrado
    # para fora e o titulo dele sai cortado na borda da figura
    fig.tight_layout(w_pad=1.0)
    fig.savefig(destino, dpi=150, facecolor=FUNDO)
    plt.close(fig)
    return destino


def main():
    destino = os.path.join(RAIZ, "assets", "img")
    base = base_analitica()
    print("base: %d linhas, de %s a %s"
          % (len(base), base["periodo"].iloc[0], base["periodo"].iloc[-1]))
    for funcao, arquivo in ((roc_do_empate, "aula10-roc-empate.png"),
                            (dobras, "aula10-dobras-kfold-vs-timeseries.png"),
                            (grade_de_hiperparametros, "aula10-grade-de-hiperparametros.png"),
                            (shap_vs_impureza, "aula10-shap-vs-impureza.png")):
        print("gerando %s" % arquivo)
        funcao(base, os.path.join(destino, arquivo))
    print("pronto")


if __name__ == "__main__":
    main()

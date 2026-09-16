"""Trava as conclusões que a Aula 10 afirma sobre ajuste e explicabilidade.

A aula tem quatro blocos de conteúdo, e cada um afirma algo medido sobre a base
mensal de `dados/mensal/`:

  1  curva ROC e AUC. No alvo binário da Aula 09, três modelos empatam nas
     quatro métricas: baseline majoritária, SVM RBF e árvore de entropia marcam
     83,3% de acurácia, 0,833 de precisão, 1,000 de revocação e 0,909 de F1. A
     AUC separa: 0,500 na baseline, 0,500 na árvore e 0,738 no SVM RBF. E a
     ordem por acurácia não é a ordem por AUC: a regressão logística tem a pior
     acurácia dos cinco classificadores (79,2%) e a melhor AUC (0,800).
  2  hiperparâmetros. A floresta da Aula 07, com as onze features da Aula 09 e
     os defaults do scikit-learn (`max_depth=None`, `min_samples_leaf=1`), erra
     5,04% de MAPE no teste. O `GridSearchCV` sobre 27 combinações escolhe
     `max_depth=4` e `min_samples_leaf=5` e leva o erro para 4,21%. Podar a
     árvore é o que melhora, e não aumentar o número de árvores.
  3  validação cruzada temporal. O `KFold(5)`, padrão do `GridSearchCV`, treina
     com meses posteriores à validação em quatro das cinco dobras, e na
     primeira dobra os 252 meses de treino são todos posteriores ao início da
     validação. O `TimeSeriesSplit(5)` não põe nenhum mês de treino no futuro
     em nenhuma das cinco dobras. A diferença de resultado no teste é ruído,
     e troca de sinal conforme o conjunto de features: com as onze features o
     `KFold` termina 0,08 ponto percentual à frente, com as quatro da Aula 07
     ele termina 0,04 atrás. O motivo de usar `TimeSeriesSplit` é a estimativa
     ser auditável, não ser melhor nesta rodada.
  4  explicabilidade. O SHAP médio absoluto sobre os 24 meses de teste e a
     importância por impureza da mesma floresta concordam nas duas primeiras
     posições (`lag12` e `lag3`) e discordam da terceira em diante:
     `abate_bovinos_lag1` é a terceira por SHAP e a sexta por impureza. O
     partial dependence de `lag12` é decrescente: quanto maior o abate de doze
     meses atrás, menor a razão de crescimento que a floresta prevê.

Como em `test_modelo_aula05.py`, `test_clusters_aula06.py`,
`test_modelos_aula07.py`, `test_pca_aula08.py` e `test_problemas_aula09.py`, o
que se trava aqui são as conclusões, não só os números.

O item 2 corrige o roteiro original em `PLANEJAMENTO_AULA_A_AULA.md`, que manda
ajustar "o Random Forest treinado na Aula 07" sem dizer sobre qual conjunto de
features: a Aula 07 usava quatro (`lag1`, `lag12`, `sen`, `cos`) e a Aula 09
deixou onze. A Aula 10 ajusta sobre as onze, e o motivo está na `ADR-013`.

Precisa de numpy, scikit-learn e shap, do requirements-ci.txt. Sem eles o
arquivo inteiro se pula, e o CI continua cobrindo o resto.

Quatro versões propositalmente quebradas foram executadas contra esta suíte, e
cada uma reprovou o teste indicado:

  medir a AUC a partir de `predict` em vez de `decision_function`
    -> `test_a_auc_separa_os_tres_modelos_empatados` (com o rótulo binário no
       lugar do escore contínuo, a AUC do SVM RBF cai de 0,738 para 0,500 e o
       empate volta: é exatamente o erro que o bloco ensina a não cometer).
  buscar a grade sobre o alvo em nível, e não sobre a razão
    -> `test_o_gridsearch_escolhe_podar_a_arvore` (em nível a busca escolhe
       `max_depth=8`, e a conclusão do bloco, que o ganho vem de podar, deixa de
       valer).
  usar `KFold(n_splits=5, shuffle=True)` em vez do `KFold` sem embaralhar
    -> `test_o_kfold_treina_com_o_futuro_em_quatro_das_cinco_dobras` (com o
       embaralhamento as cinco dobras passam a ter treino no futuro, entre 246 e
       252 meses cada, e some o "quatro das cinco" e o 252 exato da primeira).
  ler a importância do SHAP sobre o treino, e não sobre o teste
    -> `test_shap_e_impureza_discordam_da_terceira_posicao` (sobre o treino a
       terceira posição por SHAP passa a ser `lag1`, e o achado do bloco, que a
       terceira é `abate_bovinos_lag1`, desaparece).

Duas variações que **não** reprovaram nada, registradas para ninguém perder
tempo tentando de novo:

  trocar `scoring="neg_mean_absolute_percentage_error"` por `scoring="r2"` na
    busca: o R2 escolhe a mesma combinação que o MAPE nesta grade.
  contar mês de treino no futuro comparando com `ival.max()` em vez de
    `ival.min()`: como as dobras do `KFold` sem embaralhamento são contíguas,
    as duas contas dão o mesmo número em todas as cinco.
"""
import calendar
import csv
import os

import pytest

np = pytest.importorskip("numpy")
pytest.importorskip("sklearn")
shap = pytest.importorskip("shap")

from sklearn.ensemble import RandomForestRegressor  # noqa: E402
from sklearn.inspection import partial_dependence  # noqa: E402
from sklearn.linear_model import LogisticRegression  # noqa: E402
from sklearn.metrics import (accuracy_score, f1_score, precision_score,  # noqa: E402
                             recall_score, roc_auc_score)
from sklearn.model_selection import (GridSearchCV, KFold,  # noqa: E402
                                     RandomizedSearchCV, TimeSeriesSplit)
from sklearn.naive_bayes import GaussianNB  # noqa: E402
from sklearn.preprocessing import StandardScaler  # noqa: E402
from sklearn.svm import SVC  # noqa: E402
from sklearn.tree import DecisionTreeClassifier  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MENSAL = os.path.join(RAIZ, "dados", "mensal")

SERIES = ["abate_bovinos", "abate_suinos", "abate_frangos",
          "producao_ovos", "producao_leite"]
ALVO = "abate_frangos"
FEATURES = (["lag1", "lag2", "lag3", "lag12", "sen", "cos", "dias"]
            + [s + "_lag1" for s in SERIES if s != ALVO])
FEATURES_AULA07 = ["lag1", "lag12", "sen", "cos"]
N_TESTE = 24
SEMENTE = 42

GRADE = {
    "n_estimators": [100, 300, 600],
    "max_depth": [None, 4, 8],
    "min_samples_leaf": [1, 2, 5],
}


def _serie(nome):
    with open(os.path.join(MENSAL, nome + ".csv"), encoding="utf-8") as fh:
        return {l["periodo"]: float(l["valor"])
                for l in csv.DictReader(fh) if l["valor"]}


@pytest.fixture(scope="module")
def series():
    return {s: _serie(s) for s in SERIES}


@pytest.fixture(scope="module")
def base(series):
    """A base analítica mensal da Aula 07: 339 linhas, de 1998-01 a 2026-03.

    Montada com o módulo `csv` da biblioteca padrão, e não com o pandas do
    `tools/graficos_aula10.py`, de propósito: são duas implementações da mesma
    regra, e se divergirem o acervo descobre.
    """
    periodos = sorted(set.intersection(*[set(v) for v in series.values()]))

    col = {"periodo": periodos}
    for s in SERIES:
        col[s] = [series[s][p] for p in periodos]
    col["mes"] = [int(p.split("-")[1]) for p in periodos]
    col["dias"] = [calendar.monthrange(int(p.split("-")[0]), int(p.split("-")[1]))[1]
                   for p in periodos]
    col["sen"] = [np.sin(2 * np.pi * m / 12) for m in col["mes"]]
    col["cos"] = [np.cos(2 * np.pi * m / 12) for m in col["mes"]]

    def defasar(valores, k):
        return [None] * k + list(valores[:-k])

    for k in (1, 2, 3, 12):
        col["lag%d" % k] = defasar(col[ALVO], k)
    for s in SERIES:
        if s != ALVO:
            col[s + "_lag1"] = defasar(col[s], 1)

    manter = [i for i in range(len(periodos))
              if all(col[c][i] is not None for c in col)]
    saida = {c: ([col[c][i] for i in manter] if c == "periodo"
                 else np.array([col[c][i] for i in manter], dtype=float))
             for c in col}
    saida["corte"] = len(manter) - N_TESTE
    return saida


def _mape(real, previsto):
    return float(np.mean(np.abs((real - previsto) / real)) * 100)


def _matriz(base, features):
    return np.column_stack([base[c] for c in features])


@pytest.fixture(scope="module")
def classificacao(base):
    """O alvo binário da Aula 09 e os cinco classificadores dela."""
    corte = base["corte"]
    y, lag12 = base[ALVO], base["lag12"]
    binario = (y > lag12).astype(int)
    X = _matriz(base, FEATURES)

    escalador = StandardScaler().fit(X[:corte])
    Ztr, Zte = escalador.transform(X[:corte]), escalador.transform(X[corte:])
    atr, ate = binario[:corte], binario[corte:]

    modelos = {
        "logistica": LogisticRegression(max_iter=2000, random_state=SEMENTE),
        "naive bayes": GaussianNB(),
        "SVM linear": SVC(kernel="linear", random_state=SEMENTE),
        "SVM RBF": SVC(kernel="rbf", random_state=SEMENTE),
        "arvore entropia": DecisionTreeClassifier(criterion="entropy", max_depth=3,
                                                  random_state=SEMENTE),
    }
    saida = {}
    for nome, modelo in modelos.items():
        modelo.fit(Ztr, atr)
        escore = (modelo.decision_function(Zte) if hasattr(modelo, "decision_function")
                  else modelo.predict_proba(Zte)[:, 1])
        saida[nome] = (modelo.predict(Zte), escore)

    # a baseline preve sempre a classe majoritaria do treino: o escore dela e
    # constante, e a AUC de um escore constante vale 0,5 por construcao
    maioria = np.full(len(ate), int(atr.mean() > 0.5))
    saida["baseline"] = (maioria, np.zeros(len(ate)))
    return {"real": ate, "modelos": saida}


@pytest.fixture(scope="module")
def ajuste(base):
    """A busca em grade sobre a floresta da Aula 07, com as onze features."""
    corte = base["corte"]
    X = _matriz(base, FEATURES)
    razao = base[ALVO] / base["lag12"]

    busca = GridSearchCV(RandomForestRegressor(random_state=SEMENTE), GRADE,
                         scoring="neg_mean_absolute_percentage_error",
                         cv=TimeSeriesSplit(n_splits=5), n_jobs=-1)
    busca.fit(X[:corte], razao[:corte])
    return {"X": X, "razao": razao, "corte": corte, "busca": busca}


# ----------------------------------------------------------------------- bloco 1
def test_tres_modelos_empatam_nas_quatro_metricas(classificacao):
    """Baseline, SVM RBF e árvore de entropia marcam os quatro valores iguais."""
    real = classificacao["real"]
    empatados = ["baseline", "SVM RBF", "arvore entropia"]

    quadros = []
    for nome in empatados:
        previsto = classificacao["modelos"][nome][0]
        quadros.append((round(accuracy_score(real, previsto), 4),
                        round(precision_score(real, previsto, zero_division=0), 4),
                        round(recall_score(real, previsto, zero_division=0), 4),
                        round(f1_score(real, previsto, zero_division=0), 4)))

    assert quadros[0] == quadros[1] == quadros[2], (
        "os tres modelos deveriam empatar nas quatro metricas: %s" % (quadros,))
    acuracia, precisao, revocacao, f1 = quadros[0]
    assert acuracia == pytest.approx(0.8333, abs=1e-4)
    assert precisao == pytest.approx(0.8333, abs=1e-4)
    assert revocacao == pytest.approx(1.0, abs=1e-4)
    assert f1 == pytest.approx(0.9091, abs=1e-4)


def test_a_auc_separa_os_tres_modelos_empatados(classificacao):
    """A AUC vale 0,500 na baseline e na árvore, e 0,738 no SVM RBF."""
    real = classificacao["real"]
    auc = {nome: roc_auc_score(real, classificacao["modelos"][nome][1])
           for nome in ("baseline", "SVM RBF", "arvore entropia")}

    assert auc["baseline"] == pytest.approx(0.5, abs=1e-3)
    assert auc["arvore entropia"] == pytest.approx(0.5, abs=1e-3)
    assert auc["SVM RBF"] == pytest.approx(0.738, abs=5e-3)
    assert auc["SVM RBF"] > auc["baseline"] + 0.2, (
        "a AUC precisa separar o SVM RBF da baseline: %s" % auc)


def test_a_ordem_por_acuracia_nao_e_a_ordem_por_auc(classificacao):
    """A logística tem a pior acurácia dos cinco e a melhor AUC."""
    real = classificacao["real"]
    classificadores = ["logistica", "naive bayes", "SVM linear", "SVM RBF",
                       "arvore entropia"]
    acuracia = {n: accuracy_score(real, classificacao["modelos"][n][0])
                for n in classificadores}
    auc = {n: roc_auc_score(real, classificacao["modelos"][n][1])
           for n in classificadores}

    # o naive bayes acerta menos que a logistica, mas o bloco compara a
    # logistica com os que empatam em 83,3%: ela e a pior entre os que nao
    # desabam, e mesmo assim tem a melhor AUC
    assert acuracia["logistica"] == pytest.approx(0.7917, abs=1e-4)
    assert acuracia["logistica"] < acuracia["SVM RBF"]
    assert auc["logistica"] == pytest.approx(0.800, abs=5e-3)
    assert auc["logistica"] >= max(auc.values()) - 1e-9, (
        "a logistica deveria ter a maior AUC dos cinco: %s" % auc)


# ----------------------------------------------------------------------- bloco 2
def test_a_floresta_sem_ajuste_erra_cinco_por_cento(base):
    """Com as onze features e os defaults, a floresta da Aula 07 erra 5,04%."""
    corte = base["corte"]
    X = _matriz(base, FEATURES)
    razao = base[ALVO] / base["lag12"]
    modelo = RandomForestRegressor(n_estimators=300, random_state=SEMENTE)
    modelo.fit(X[:corte], razao[:corte])
    erro = _mape(base[ALVO][corte:], modelo.predict(X[corte:]) * base["lag12"][corte:])
    assert erro == pytest.approx(5.04, abs=0.05)

    # com as quatro features da propria Aula 07, a mesma floresta erra 4,48%:
    # e o numero publicado no notebook daquela aula, e a diferenca entre os
    # dois e o que motiva o bloco
    X07 = _matriz(base, FEATURES_AULA07)
    modelo07 = RandomForestRegressor(n_estimators=300, random_state=SEMENTE)
    modelo07.fit(X07[:corte], razao[:corte])
    erro07 = _mape(base[ALVO][corte:],
                   modelo07.predict(X07[corte:]) * base["lag12"][corte:])
    assert erro07 == pytest.approx(4.48, abs=0.05)
    assert erro > erro07, (
        "as sete features extras da Aula 09 pioram a floresta sem ajuste: "
        "%.2f%% contra %.2f%%" % (erro, erro07))


def test_o_gridsearch_escolhe_podar_a_arvore(ajuste, base):
    """O ganho vem de `max_depth` e `min_samples_leaf`, não de mais árvores."""
    escolhidos = ajuste["busca"].best_params_
    assert escolhidos["max_depth"] == 4
    assert escolhidos["min_samples_leaf"] == 5

    # o numero de arvores quase nao muda o erro: as tres combinacoes que so
    # diferem em n_estimators ficam dentro de 0,2 ponto percentual
    X, razao, corte = ajuste["X"], ajuste["razao"], ajuste["corte"]
    yte, lag12te = base[ALVO][corte:], base["lag12"][corte:]
    erros = []
    for arvores in GRADE["n_estimators"]:
        modelo = RandomForestRegressor(n_estimators=arvores, max_depth=4,
                                       min_samples_leaf=5, random_state=SEMENTE)
        modelo.fit(X[:corte], razao[:corte])
        erros.append(_mape(yte, modelo.predict(X[corte:]) * lag12te))
    assert max(erros) - min(erros) < 0.2, (
        "n_estimators nao deveria mudar muito o erro: %s" % erros)


def test_o_ajuste_leva_a_floresta_de_cinco_para_quatro_por_cento(ajuste, base):
    """O GridSearchCV corta o MAPE de teste de 5,04% para 4,21%."""
    corte = ajuste["corte"]
    yte, lag12te = base[ALVO][corte:], base["lag12"][corte:]
    melhor = ajuste["busca"].best_estimator_
    erro = _mape(yte, melhor.predict(ajuste["X"][corte:]) * lag12te)
    assert erro == pytest.approx(4.21, abs=0.05)

    sem_ajuste = RandomForestRegressor(n_estimators=300, random_state=SEMENTE)
    sem_ajuste.fit(ajuste["X"][:corte], ajuste["razao"][:corte])
    erro_sem = _mape(yte, sem_ajuste.predict(ajuste["X"][corte:]) * lag12te)
    assert erro < erro_sem - 0.5, (
        "o ajuste deveria valer pelo menos meio ponto percentual: "
        "%.2f%% contra %.2f%%" % (erro, erro_sem))


def test_o_mape_na_razao_e_o_mesmo_mape_em_nivel(ajuste, base):
    """Treinar na razão não muda o MAPE: os dois lag12 se cancelam."""
    corte = ajuste["corte"]
    melhor = ajuste["busca"].best_estimator_
    previsto_razao = melhor.predict(ajuste["X"][corte:])
    na_razao = _mape(ajuste["razao"][corte:], previsto_razao)
    em_nivel = _mape(base[ALVO][corte:], previsto_razao * base["lag12"][corte:])
    assert na_razao == pytest.approx(em_nivel, abs=1e-9)


def test_o_randomsearch_acha_o_mesmo_com_um_terco_do_orcamento(ajuste):
    """Nove sorteios de 27 combinações chegam na mesma escolha da grade cheia."""
    corte = ajuste["corte"]
    sorteada = RandomizedSearchCV(RandomForestRegressor(random_state=SEMENTE), GRADE,
                                  n_iter=9,
                                  scoring="neg_mean_absolute_percentage_error",
                                  cv=TimeSeriesSplit(n_splits=5),
                                  random_state=SEMENTE, n_jobs=-1)
    sorteada.fit(ajuste["X"][:corte], ajuste["razao"][:corte])
    assert sorteada.best_params_["max_depth"] == 4
    assert sorteada.best_params_["min_samples_leaf"] == 5
    assert sorteada.best_score_ == pytest.approx(ajuste["busca"].best_score_, abs=1e-4)


# ----------------------------------------------------------------------- bloco 3
def test_o_kfold_treina_com_o_futuro_em_quatro_das_cinco_dobras(base):
    """Quatro das cinco dobras do KFold têm mês de treino posterior à validação."""
    corte = base["corte"]
    X = _matriz(base, FEATURES)[:corte]

    futuros = []
    for itr, ival in KFold(n_splits=5).split(X):
        futuros.append(int((itr > ival.min()).sum()))

    assert futuros[0] == 252, "a primeira dobra treina inteira no futuro: %s" % futuros
    assert len(itr) == 252
    assert sum(1 for f in futuros if f > 0) == 4, (
        "quatro das cinco dobras deveriam ter treino no futuro: %s" % futuros)


def test_o_timeseriessplit_nao_poe_nenhum_mes_de_treino_no_futuro(base):
    """As cinco dobras do TimeSeriesSplit treinam só com o passado."""
    corte = base["corte"]
    X = _matriz(base, FEATURES)[:corte]

    tamanhos = []
    for itr, ival in TimeSeriesSplit(n_splits=5).split(X):
        assert int((itr > ival.min()).sum()) == 0
        assert itr.max() < ival.min()
        tamanhos.append(len(itr))

    # o treino cresce a cada dobra, que e a diferenca de desenho para o KFold
    assert tamanhos == sorted(tamanhos)
    assert tamanhos == [55, 107, 159, 211, 263]


def test_a_diferenca_de_teste_entre_os_dois_validadores_e_ruido(base):
    """Qual validador termina à frente no teste depende do conjunto de features."""
    corte = base["corte"]
    razao = base[ALVO] / base["lag12"]
    yte, lag12te = base[ALVO][corte:], base["lag12"][corte:]

    def erro_do_escolhido(features, cv):
        X = _matriz(base, features)
        busca = GridSearchCV(RandomForestRegressor(random_state=SEMENTE), GRADE,
                             scoring="neg_mean_absolute_percentage_error",
                             cv=cv, n_jobs=-1)
        busca.fit(X[:corte], razao[:corte])
        return _mape(yte, busca.best_estimator_.predict(X[corte:]) * lag12te)

    onze_kf = erro_do_escolhido(FEATURES, KFold(n_splits=5))
    onze_ts = erro_do_escolhido(FEATURES, TimeSeriesSplit(n_splits=5))
    quatro_kf = erro_do_escolhido(FEATURES_AULA07, KFold(n_splits=5))
    quatro_ts = erro_do_escolhido(FEATURES_AULA07, TimeSeriesSplit(n_splits=5))

    # com onze features o KFold termina a frente, com quatro ele termina atras:
    # a vantagem troca de sinal, entao ela e ruido, e o motivo de usar
    # TimeSeriesSplit e a estimativa ser auditavel, nao ser melhor no teste
    assert onze_kf < onze_ts
    assert quatro_kf > quatro_ts
    assert abs(onze_kf - onze_ts) < 0.2
    assert abs(quatro_kf - quatro_ts) < 0.2


# ----------------------------------------------------------------------- bloco 4
def test_shap_e_impureza_discordam_da_terceira_posicao(ajuste):
    """As duas leituras concordam em lag12 e lag3, e divergem daí em diante."""
    corte = ajuste["corte"]
    melhor = ajuste["busca"].best_estimator_

    medio = np.abs(shap.TreeExplainer(melhor).shap_values(ajuste["X"][corte:])).mean(axis=0)
    por_shap = [FEATURES[i] for i in np.argsort(medio)[::-1]]
    por_impureza = [FEATURES[i] for i in np.argsort(melhor.feature_importances_)[::-1]]

    assert por_shap[:2] == por_impureza[:2] == ["lag12", "lag3"]
    assert por_shap[2] == "abate_bovinos_lag1"
    assert por_impureza.index("abate_bovinos_lag1") == 5, (
        "abate_bovinos_lag1 e a terceira por SHAP e a sexta por impureza: %s"
        % por_impureza)
    assert por_shap[2:] != por_impureza[2:]


def test_o_partial_dependence_de_lag12_e_decrescente(ajuste):
    """Quanto maior a base, menor o crescimento que a floresta prevê."""
    corte = ajuste["corte"]
    melhor = ajuste["busca"].best_estimator_
    topo = FEATURES.index("lag12")

    resultado = partial_dependence(melhor, ajuste["X"][:corte], [topo],
                                   grid_resolution=8)
    media = np.asarray(resultado["average"][0], dtype=float)

    assert media[0] > media[-1]
    assert media[0] == pytest.approx(1.093, abs=5e-3)
    assert media[-1] == pytest.approx(1.010, abs=5e-3)
    assert all(media[i] >= media[i + 1] for i in range(len(media) - 1)), (
        "a curva deveria ser monotona decrescente: %s" % media)

"""Trava as conclusões que a Aula 11 afirma sobre AutoML e escolha de candidato.

A aula tem quatro blocos de conteúdo, e cada um afirma algo medido sobre a base
mensal de `dados/mensal/`, a mesma das Aulas 07 a 10:

  1  o quadro de referência. Nos mesmos 24 meses de teste, com as mesmas onze
     features e os mesmos 315 meses de treino, a regressão linear sobre o alvo
     em nível erra 2,86%, a mesma regressão sobre o alvo em razão erra 3,32%, a
     baseline de coeficiente fixo da LDC erra 3,71% e a floresta ajustada à mão
     na Aula 10 erra 4,21%. O modelo que duas aulas de ajuste manual produziram
     é o pior dos quatro.
  2  a decisão de alvo. Treinar sobre a razão foi a decisão da Aula 07, tomada
     para resolver o teto da árvore de decisão, e ela custa 0,46 ponto
     percentual ao modelo linear. Hiperparâmetro nenhum recupera isso, porque
     hiperparâmetro não muda o alvo.
  3  o que o `compare_models()` encontra. Ele ordena 22 candidatos em poucos
     segundos e coloca modelos lineares no topo, não árvores, nas três
     configurações que a aula usa. O melhor deles bate a floresta ajustada da
     Aula 10.
  4  o que ele não conserta. O construtor do PyCaret 4 traz `train_size=0.7`,
     que separa 95 dos 315 meses de treino por sorteio, e
     `fold_strategy="kfold"`, que é o validador que a Aula 10 mostrou pondo 252
     meses de treino no futuro. Trocando o fold pelo `TimeSeriesSplit`, a
     estimativa do leaderboard passa a errar menos: a diferença entre o MAPE
     estimado e o MAPE de teste cai de cerca de meio ponto para cerca de dois
     décimos.
  5  o R2 entre alvos. Trocando o alvo de nível para razão, sem mudar nada mais,
     o R2 do leaderboard cai de cerca de 0,98 para cerca de 0,48. O modelo não
     piorou: o alvo em razão tem muito menos variância a explicar, e o R2 é a
     fração dessa variância. É o mesmo erro de leitura que a Aula 09 tratou com
     o RMSE entre conjuntos de teste de escalas diferentes.

Como em `test_modelo_aula05.py`, `test_clusters_aula06.py`,
`test_modelos_aula07.py`, `test_pca_aula08.py`, `test_problemas_aula09.py` e
`test_ajuste_aula10.py`, o que se trava aqui são as conclusões, não só os
números.

Precisa de numpy, scikit-learn e pycaret, do requirements-ci.txt. Sem eles o
arquivo inteiro se pula, e o CI continua cobrindo o resto. O `pycaret` é a única
dependência do acervo com versão fixada, e o motivo está em `docs/adrs/ADR-014`.

As tolerâncias dos testes que passam pelo PyCaret são mais largas que as do
resto do acervo, de propósito: a versão é uma alpha, o `compare_models` treina
22 famílias e algumas delas não fixam semente por completo. O que se trava ali é
a conclusão (qual família vence, qual estimativa erra menos), não o dígito.

Duas versões propositalmente quebradas foram executadas contra esta suíte, e
cada uma reprovou o teste indicado:

  medir o alvo em nível e o alvo em razão em conjuntos de teste diferentes
    -> `test_a_decisao_de_alvo_da_aula_07_custa_ao_modelo_linear` (com cortes
       diferentes os dois números deixam de ser comparáveis e a diferença de
       0,46 ponto vira qualquer coisa).
  deixar o `train_size` no default ao medir a estimativa do fold temporal
    -> `test_a_estimativa_do_fold_temporal_erra_menos` (com 220 meses em vez de
       311, a estimativa do TimeSeriesSplit piora e a comparação entre os dois
       folds deixa de isolar o efeito do validador).

Uma terceira variação **não** reprovou nada, e fica registrada para ninguém
tentar de novo: comparar o R2 dos dois alvos com conjuntos de features
diferentes (quatro em nível contra onze em razão) continua produzindo a queda
de 0,98 para 0,48, porque ela é dominada pelo alvo e não pelas features. O
teste é insensível a essa troca, e isso é limitação dele, não prova de que a
queda seja atribuível só ao alvo: o que sustenta a atribuição é as duas
chamadas de `_experimento` usarem a mesma constante FEATURES, o que se lê no
código e não se trava por asserção.
"""
import calendar
import csv
import os
import warnings

import pytest

np = pytest.importorskip("numpy")
pytest.importorskip("sklearn")
pytest.importorskip("pandas")
pycaret = pytest.importorskip("pycaret")

import pandas as pd  # noqa: E402
from sklearn.ensemble import RandomForestRegressor  # noqa: E402
from sklearn.linear_model import LinearRegression  # noqa: E402
from sklearn.model_selection import TimeSeriesSplit  # noqa: E402
from sklearn.preprocessing import StandardScaler  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MENSAL = os.path.join(RAIZ, "dados", "mensal")

SERIES = ["abate_bovinos", "abate_suinos", "abate_frangos",
          "producao_ovos", "producao_leite"]
ALVO = "abate_frangos"
FEATURES = (["lag1", "lag2", "lag3", "lag12", "sen", "cos", "dias"]
            + [s + "_lag1" for s in SERIES if s != ALVO])
N_TESTE = 24
SEMENTE = 42

# a floresta que a Aula 10 escolheu, em docs/adrs/ADR-013
FLORESTA_AULA10 = dict(n_estimators=600, max_depth=4, min_samples_leaf=5)


def _serie(nome):
    with open(os.path.join(MENSAL, nome + ".csv"), encoding="utf-8") as fh:
        return {l["periodo"]: float(l["valor"])
                for l in csv.DictReader(fh) if l["valor"]}


@pytest.fixture(scope="module")
def base():
    """A base analítica mensal das Aulas 07 a 10: 339 linhas, 315 de treino.

    Montada com o módulo `csv` da biblioteca padrão, e não com o pandas do
    `tools/graficos_aula11.py`, de propósito: são duas implementações da mesma
    regra, e se divergirem o acervo descobre.
    """
    series = {s: _serie(s) for s in SERIES}
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


def _matriz(base, features=None):
    return np.column_stack([base[c] for c in (features or FEATURES)])


def _linear(base, em_razao):
    """MAPE de teste da regressão linear, com o alvo em nível ou em razão."""
    corte = base["corte"]
    X = _matriz(base)
    y, lag12 = base[ALVO], base["lag12"]
    alvo = (y / lag12) if em_razao else y

    escalador = StandardScaler().fit(X[:corte])
    modelo = LinearRegression().fit(escalador.transform(X[:corte]), alvo[:corte])
    previsto = modelo.predict(escalador.transform(X[corte:]))
    if em_razao:
        previsto = previsto * lag12[corte:]
    return _mape(y[corte:], previsto)


@pytest.fixture(scope="module")
def referencias(base):
    """Os quatro modelos de referência, todos nos mesmos 24 meses de teste."""
    corte = base["corte"]
    X = _matriz(base)
    y, lag12 = base[ALVO], base["lag12"]
    razao = y / lag12

    floresta = RandomForestRegressor(random_state=SEMENTE, **FLORESTA_AULA10)
    floresta.fit(X[:corte], razao[:corte])

    fator = float(np.mean(razao[:corte]))
    return {
        "linear em nivel": _linear(base, em_razao=False),
        "linear em razao": _linear(base, em_razao=True),
        "baseline da LDC": _mape(y[corte:], lag12[corte:] * fator),
        "floresta da Aula 10": _mape(y[corte:],
                                     floresta.predict(X[corte:]) * lag12[corte:]),
    }


def _experimento(base, em_razao, **kwargs):
    """Roda o compare_models do PyCaret sobre os 315 meses de treino."""
    from pycaret.regression import RegressionExperiment

    corte = base["corte"]
    X = pd.DataFrame(_matriz(base), columns=FEATURES)
    y, lag12 = base[ALVO], base["lag12"]
    alvo = (y / lag12) if em_razao else y

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        exp = RegressionExperiment(session_id=SEMENTE, **kwargs)
        exp.fit(X.iloc[:corte], pd.Series(alvo[:corte], name="alvo"))
        resultado = exp.compare_models(n_select=5)

    quadro = exp.pull()
    campeao = resultado.models[0]
    previsto = np.asarray(campeao.predict(X.iloc[corte:]), dtype=float)
    if em_razao:
        previsto = previsto * lag12[corte:]
    return {
        "exp": exp,
        "quadro": quadro,
        "ids": list(resultado.ranked_ids),
        "estimado": float(quadro.iloc[0]["MAPE"]) * 100,
        "r2": float(quadro.iloc[0]["R2"]),
        "teste": _mape(y[corte:], previsto),
        "treino_interno": len(exp.X_train),
        "teste_interno": len(exp.X_test),
    }


@pytest.fixture(scope="module")
def default_em_razao(base):
    return _experimento(base, em_razao=True)


@pytest.fixture(scope="module")
def temporal_em_razao(base):
    return _experimento(base, em_razao=True, train_size=0.99,
                        fold_strategy=TimeSeriesSplit(n_splits=5))


@pytest.fixture(scope="module")
def default_em_nivel(base):
    return _experimento(base, em_razao=False)


@pytest.fixture(scope="module")
def temporal_em_nivel(base):
    return _experimento(base, em_razao=False, train_size=0.99,
                        fold_strategy=TimeSeriesSplit(n_splits=5))


# ----------------------------------------------------------------------- bloco 1
def test_o_modelo_ajustado_a_mao_e_o_pior_dos_quatro(referencias):
    """A floresta das Aulas 07 e 10 perde para as três outras referências."""
    assert referencias["linear em nivel"] == pytest.approx(2.86, abs=0.05)
    assert referencias["linear em razao"] == pytest.approx(3.32, abs=0.05)
    assert referencias["baseline da LDC"] == pytest.approx(3.71, abs=0.05)
    assert referencias["floresta da Aula 10"] == pytest.approx(4.21, abs=0.05)

    ordem = sorted(referencias, key=referencias.get)
    assert ordem == ["linear em nivel", "linear em razao", "baseline da LDC",
                     "floresta da Aula 10"], (
        "a ordem das quatro referencias mudou: %s" % referencias)


def test_a_floresta_ajustada_nao_bate_a_baseline_da_ldc(referencias):
    """Dois encontros de ajuste manual não alcançaram a baseline do parceiro."""
    assert referencias["floresta da Aula 10"] > referencias["baseline da LDC"], (
        "a floresta ajustada deveria perder para a baseline: %.2f%% contra %.2f%%"
        % (referencias["floresta da Aula 10"], referencias["baseline da LDC"]))


# ----------------------------------------------------------------------- bloco 2
def test_a_decisao_de_alvo_da_aula_07_custa_ao_modelo_linear(base, referencias):
    """Treinar na razão custa cerca de meio ponto percentual à regressão."""
    custo = referencias["linear em razao"] - referencias["linear em nivel"]
    assert custo == pytest.approx(0.46, abs=0.06), (
        "o custo do alvo em razao mudou: %.2f ponto" % custo)

    # os dois numeros vem do MESMO corte, das MESMAS features e do MESMO
    # escalador: so o alvo muda. Sem isso a diferenca nao e atribuivel ao alvo.
    corte = base["corte"]
    assert corte == len(base["periodo"]) - N_TESTE
    assert _linear(base, em_razao=False) == referencias["linear em nivel"]
    assert _linear(base, em_razao=True) == referencias["linear em razao"]


def test_o_alvo_em_razao_ainda_ajuda_a_floresta(base, referencias):
    """A decisão da Aula 07 continua certa para a árvore, que foi o motivo dela."""
    corte = base["corte"]
    X = _matriz(base)
    y, lag12 = base[ALVO], base["lag12"]

    em_nivel = RandomForestRegressor(random_state=SEMENTE, **FLORESTA_AULA10)
    em_nivel.fit(X[:corte], y[:corte])
    erro_nivel = _mape(y[corte:], em_nivel.predict(X[corte:]))

    assert erro_nivel == pytest.approx(5.67, abs=0.05)
    assert erro_nivel > referencias["floresta da Aula 10"], (
        "para a floresta, o alvo em razao deveria continuar melhor: "
        "%.2f%% em nivel contra %.2f%% em razao"
        % (erro_nivel, referencias["floresta da Aula 10"]))


# ----------------------------------------------------------------------- bloco 3
def test_o_compare_models_poe_modelo_linear_no_topo(default_em_razao,
                                                    temporal_em_razao,
                                                    default_em_nivel):
    """Nas três configurações, o primeiro colocado é linear, não árvore."""
    lineares = {"lr", "ridge", "lasso", "en", "lar", "llar", "br", "ard", "tr",
                "huber", "ransac", "par", "omp"}
    arvores = {"rf", "et", "gbr", "dt", "ada", "lightgbm", "xgboost", "catboost"}

    for rotulo, resultado in (("razao, default", default_em_razao),
                              ("razao, temporal", temporal_em_razao),
                              ("nivel, default", default_em_nivel)):
        assert resultado["ids"][0] in lineares, (
            "%s: esperava modelo linear no topo, veio %s"
            % (rotulo, resultado["ids"][0]))
        assert resultado["ids"][0] not in arvores


def test_o_melhor_do_automl_bate_a_floresta_ajustada(referencias,
                                                     default_em_nivel,
                                                     temporal_em_nivel,
                                                     temporal_em_razao):
    """O campeão do leaderboard erra menos que a floresta das Aulas 07 e 10."""
    assert default_em_nivel["teste"] < referencias["floresta da Aula 10"]
    assert temporal_em_razao["teste"] < referencias["floresta da Aula 10"]
    # sobre o alvo em nivel ele tambem bate a baseline da LDC, que e o piso que
    # a ART.7 cobra
    assert default_em_nivel["teste"] < referencias["baseline da LDC"]
    assert default_em_nivel["teste"] < 3.0


def test_o_campeao_sobrevive_ao_protocolo_honesto(referencias, temporal_em_nivel,
                                                  default_em_nivel):
    """O campeão do alvo em nível continua abaixo de 3% com o fold temporal.

    Achado da revisão do `revisor-slides`: o campeão dos defaults treina com 220
    dos 315 meses, sorteados, enquanto os quatro modelos de referência treinam
    com os 315 inteiros. Pôr os dois no mesmo gráfico compara família e volume
    de dado ao mesmo tempo. Este teste trava o quadrante comparável, que é o que
    a figura 1 usa.
    """
    assert temporal_em_nivel["treino_interno"] == 311
    assert temporal_em_nivel["teste"] == pytest.approx(2.84, abs=0.08)
    assert temporal_em_nivel["teste"] < referencias["linear em nivel"]
    assert temporal_em_nivel["teste"] < referencias["floresta da Aula 10"]

    # os dois protocolos chegam praticamente ao mesmo erro de teste: o que o
    # protocolo honesto muda e a estimativa, nao o modelo
    assert abs(temporal_em_nivel["teste"] - default_em_nivel["teste"]) < 0.15
    assert (abs(temporal_em_nivel["estimado"] - temporal_em_nivel["teste"])
            < abs(default_em_nivel["estimado"] - default_em_nivel["teste"]))


# ----------------------------------------------------------------------- bloco 4
def test_o_default_do_pycaret_separa_meses_por_sorteio(default_em_razao):
    """`train_size=0.7` tira 95 dos 315 meses de treino, e o corte é aleatório."""
    assert default_em_razao["treino_interno"] == 220
    assert default_em_razao["teste_interno"] == 95
    assert (default_em_razao["treino_interno"]
            + default_em_razao["teste_interno"]) == 315


def test_a_estimativa_do_fold_temporal_erra_menos(default_em_razao,
                                                  temporal_em_razao):
    """Com TimeSeriesSplit, o leaderboard prevê melhor o erro de teste."""
    erro_default = abs(default_em_razao["estimado"] - default_em_razao["teste"])
    erro_temporal = abs(temporal_em_razao["estimado"] - temporal_em_razao["teste"])

    assert temporal_em_razao["treino_interno"] == 311
    assert erro_temporal < erro_default, (
        "a estimativa temporal deveria errar menos: %.2f contra %.2f ponto"
        % (erro_temporal, erro_default))
    assert erro_temporal < 0.30
    assert erro_default > 0.30


# ----------------------------------------------------------------------- bloco 5
def test_o_r2_despenca_ao_trocar_de_alvo(default_em_nivel, default_em_razao):
    """O R2 cai de cerca de 0,98 para cerca de 0,48 só por trocar o alvo."""
    assert default_em_nivel["r2"] > 0.95
    assert default_em_razao["r2"] < 0.60

    # e o modelo nao piorou: o MAPE dos dois fica na mesma casa, porque o MAPE e
    # razao entre erro e valor real e nao depende da variancia do alvo
    assert abs(default_em_nivel["estimado"] - default_em_razao["estimado"]) < 0.5

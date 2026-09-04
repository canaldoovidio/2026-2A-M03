"""Trava as quatro hipoteses que a Aula 07 declara e testa em sala.

O deck, o material, as notas do professor e o notebook citam metricas de
modelos ajustados sobre dados/mensal/. Se um CSV for regerado com dado novo do
SIDRA, uma conclusao pode virar, e os quatro artefatos passam a ensinar algo
que o dado nao sustenta.

Como em test_hipoteses_aula04.py e test_modelo_aula05.py, o que se trava aqui
sao as conclusoes:

  H1  a granularidade do case nao e imposta pela fonte     -> test_dados_mensal.py
  H2  a arvore nao ganha da reta nem da baseline           -> falsa, medida aqui
  H3  a arvore perde porque nao extrapola tendencia        -> verdadeira
  H4  alvo em razao devolve a arvore a disputa             -> verdadeira

Mais dois achados que a aula usa e que precisam continuar valendo:

  5  padronizar piora o KNN nesta base, em todo k testado
  6  a regressao linear sobre a razao com 11 features bate a baseline da LDC

Precisa de numpy e scikit-learn, do requirements-ci.txt. Sem eles o arquivo
inteiro se pula, e o CI continua cobrindo o resto.

Cada assercao foi vista falhando ao menos uma vez, contra tres versoes
propositalmente quebradas: treinar a arvore no alvo em razao dentro do bloco de
H2 (derruba test_arvore_perde_da_reta_e_da_baseline), embaralhar as linhas antes
do corte temporal (derruba os testes de teto) e padronizar o KNN dentro do bloco
que afirma que padronizar piora (derruba test_padronizar_piora_o_knn).
"""
import calendar
import csv
import os

import pytest

np = pytest.importorskip("numpy")
pytest.importorskip("sklearn")

from sklearn.ensemble import RandomForestRegressor  # noqa: E402
from sklearn.linear_model import LinearRegression  # noqa: E402
from sklearn.neighbors import KNeighborsRegressor  # noqa: E402
from sklearn.preprocessing import StandardScaler  # noqa: E402
from sklearn.tree import DecisionTreeRegressor  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MENSAL = os.path.join(RAIZ, "dados", "mensal")

SERIES = ["abate_bovinos", "abate_suinos", "abate_frangos",
          "producao_ovos", "producao_leite"]
ALVO = "abate_frangos"
FEATURES = ["lag1", "lag12", "sen", "cos"]
FEATURES_FECHO = (["lag1", "lag2", "lag3", "lag12", "sen", "cos", "dias"]
                  + [s + "_lag1" for s in SERIES if s != ALVO])
N_TESTE = 24
SEMENTE = 42


def _serie(nome):
    caminho = os.path.join(MENSAL, nome + ".csv")
    with open(caminho, encoding="utf-8") as fh:
        return {l["periodo"]: float(l["valor"])
                for l in csv.DictReader(fh) if l["valor"]}


@pytest.fixture(scope="module")
def base():
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
    return saida


def _fatiar(dados, features, alvo_em_razao):
    n = len(dados["periodo"])
    corte = n - N_TESTE
    X = np.column_stack([dados[f] for f in features])
    y = dados[ALVO]
    alvo = y / dados["lag12"] if alvo_em_razao else y
    return (X[:corte], alvo[:corte], X[corte:], y[corte:], dados["lag12"][corte:])


def _ajustar(dados, features, modelo, alvo_em_razao=False, padronizar=False):
    Xtr, alvo_tr, Xte, yte, lag12te = _fatiar(dados, features, alvo_em_razao)
    if padronizar:
        escalador = StandardScaler().fit(Xtr)
        Xtr, Xte = escalador.transform(Xtr), escalador.transform(Xte)
    previsto = modelo.fit(Xtr, alvo_tr).predict(Xte)
    if alvo_em_razao:
        previsto = previsto * lag12te
    return yte, previsto


def _mape(real, previsto):
    return float(np.mean(np.abs((real - previsto) / real)) * 100)


def _rmse(real, previsto):
    return float(np.sqrt(np.mean((real - previsto) ** 2)))


def _baselines(dados):
    n = len(dados["periodo"])
    corte = n - N_TESTE
    fator = float(np.mean(dados[ALVO][:corte] / dados["lag12"][:corte]))
    return {
        "A": dados["lag1"][corte:],
        "B": dados["lag12"][corte:],
        "C": dados["lag12"][corte:] * fator,
    }, fator


# --------------------------------------------------------------------------
# A base


def test_base_tem_o_tamanho_que_a_aula_afirma(base):
    assert len(base["periodo"]) == 339
    assert base["periodo"][0] == "1998-01"
    assert base["periodo"][-1] == "2026-03"
    corte = len(base["periodo"]) - N_TESTE
    assert corte == 315
    assert base["periodo"][corte - 1] == "2024-03"
    assert base["periodo"][corte] == "2024-04"


# --------------------------------------------------------------------------
# Baselines


def test_a_baseline_da_ldc_e_a_melhor_das_tres(base):
    linhas, fator = _baselines(base)
    yte = base[ALVO][-N_TESTE:]
    mapes = {k: _mape(yte, v) for k, v in linhas.items()}
    assert mapes["C"] < mapes["B"] < mapes["A"]
    assert 6.5 < mapes["A"] < 7.0
    assert 4.9 < mapes["B"] < 5.3
    assert 3.5 < mapes["C"] < 3.9
    assert 1.05 < fator < 1.06


# --------------------------------------------------------------------------
# H2: a arvore nao ganha da reta nem da baseline


def test_arvore_perde_da_reta_e_da_baseline(base):
    """H2 e falsa. Este e o teste que a aula inteira depende de continuar
    falhando a hipotese: se a arvore passar a ganhar, o roteiro nao vale."""
    linhas, _ = _baselines(base)
    yte = base[ALVO][-N_TESTE:]
    _, p_arvore = _ajustar(
        base, FEATURES, DecisionTreeRegressor(max_depth=3, random_state=SEMENTE))
    _, p_reta = _ajustar(
        base, FEATURES, LinearRegression(), padronizar=True)

    mape_arvore = _mape(yte, p_arvore)
    mape_reta = _mape(yte, p_reta)
    mape_baseline = _mape(yte, linhas["C"])

    assert mape_arvore > mape_reta
    assert mape_arvore > mape_baseline
    assert 7.2 < mape_arvore < 8.1
    assert 4.0 < mape_reta < 4.5
    assert 100e6 < _rmse(yte, p_arvore) < 120e6


def test_a_floresta_melhora_a_arvore_e_ainda_perde_da_baseline(base):
    linhas, _ = _baselines(base)
    yte = base[ALVO][-N_TESTE:]
    _, p_arvore = _ajustar(
        base, FEATURES, DecisionTreeRegressor(max_depth=3, random_state=SEMENTE))
    _, p_floresta = _ajustar(
        base, FEATURES,
        RandomForestRegressor(n_estimators=300, random_state=SEMENTE))
    assert _mape(yte, p_floresta) < _mape(yte, p_arvore)
    assert _mape(yte, p_floresta) > _mape(yte, linhas["C"])
    assert 5.0 < _mape(yte, p_floresta) < 5.7


# --------------------------------------------------------------------------
# H3: o teto da arvore


def test_a_arvore_tem_teto_e_o_teste_esta_acima_dele(base):
    """H3 e verdadeira. A arvore preve a media da folha, entao a maior
    previsao possivel e a media da folha mais alta. O alvo cresce, e o teste
    fica quase todo acima desse teto."""
    Xtr, ytr, Xte, yte, _ = _fatiar(base, FEATURES, alvo_em_razao=False)
    arvore = DecisionTreeRegressor(max_depth=3, random_state=SEMENTE).fit(Xtr, ytr)
    previsto = arvore.predict(Xte)

    teto = float(previsto.max())
    assert teto < float(ytr.max()), "o teto e a media de uma folha, nao o maximo do treino"
    assert int((yte > teto).sum()) == 23
    assert int((yte > ytr.max()).sum()) == 5
    assert arvore.get_n_leaves() == 8
    assert 1.05e9 < teto < 1.13e9
    assert 1.29e9 < float(yte.max()) < 1.32e9


def test_a_arvore_preve_um_unico_valor_nos_24_meses(base):
    """O achado que o deck, o material e as notas do professor citam como o
    centro da aula: a arvore nao apenas tem teto, ela emite o MESMO numero do
    primeiro ao ultimo mes do teste.

    Ela tem 8 folhas, mas a janela de teste inteira cai na mesma folha. Sem
    este teste, o numero mais citado da aula seria o unico sem fonte travada,
    contra a regra do acervo de que todo numero de slide sai de um teste."""
    Xtr, ytr, Xte, yte, _ = _fatiar(base, FEATURES, alvo_em_razao=False)
    arvore = DecisionTreeRegressor(max_depth=3, random_state=SEMENTE).fit(Xtr, ytr)
    previsto = arvore.predict(Xte)

    distintos = set(previsto.round(6).tolist())
    assert len(distintos) == 1, (
        "a arvore deixou de emitir um unico valor no teste: %d valores "
        "distintos. O deck, o material e as notas do professor afirmam que e "
        "um so." % len(distintos)
    )
    assert len(previsto) == 24

    unico = float(previsto[0])
    assert 1.05e9 < unico < 1.13e9
    # o valor unico fica abaixo da media real do periodo, e por isso o erro e
    # sistematico e nao aleatorio
    desvio = (unico - float(yte.mean())) / float(yte.mean()) * 100
    assert -8.5 < desvio < -7.0, desvio


def test_a_reta_nao_tem_teto(base):
    """O contraste que explica H3: a reta extrapola, a arvore nao."""
    Xtr, ytr, _, _, _ = _fatiar(base, FEATURES, alvo_em_razao=False)
    _, p_reta = _ajustar(base, FEATURES, LinearRegression(), padronizar=True)
    assert float(p_reta.max()) > float(ytr.max())


# --------------------------------------------------------------------------
# H4: alvo em razao


def test_alvo_em_razao_corta_o_erro_da_arvore_pela_metade(base):
    """H4 e verdadeira."""
    yte = base[ALVO][-N_TESTE:]
    _, p_nivel = _ajustar(
        base, FEATURES, DecisionTreeRegressor(max_depth=3, random_state=SEMENTE))
    _, p_razao = _ajustar(
        base, FEATURES, DecisionTreeRegressor(max_depth=3, random_state=SEMENTE),
        alvo_em_razao=True)
    assert _mape(yte, p_razao) < _mape(yte, p_nivel) / 1.8
    assert 3.6 < _mape(yte, p_razao) < 4.1


def test_alvo_em_razao_melhora_todos_os_modelos_que_nao_extrapolam(base):
    yte = base[ALVO][-N_TESTE:]
    for rotulo, modelo, padronizar in [
        ("arvore", DecisionTreeRegressor(max_depth=3, random_state=SEMENTE), False),
        ("floresta", RandomForestRegressor(n_estimators=300, random_state=SEMENTE), False),
        ("knn padronizado", KNeighborsRegressor(n_neighbors=5), True),
        ("knn sem padronizar", KNeighborsRegressor(n_neighbors=5), False),
    ]:
        _, p_nivel = _ajustar(base, FEATURES, modelo, padronizar=padronizar)
        _, p_razao = _ajustar(base, FEATURES, modelo, alvo_em_razao=True,
                              padronizar=padronizar)
        assert _mape(yte, p_razao) < _mape(yte, p_nivel), rotulo


def test_a_reta_piora_com_alvo_em_razao(base):
    """A reta ja extrapolava, entao a razao tira dela informacao de nivel.
    O contraste impede a leitura de que razao e sempre melhor."""
    yte = base[ALVO][-N_TESTE:]
    _, p_nivel = _ajustar(base, FEATURES, LinearRegression(), padronizar=True)
    _, p_razao = _ajustar(base, FEATURES, LinearRegression(),
                          alvo_em_razao=True, padronizar=True)
    assert _mape(yte, p_razao) > _mape(yte, p_nivel)


# --------------------------------------------------------------------------
# Achado 5: padronizar piora o KNN nesta base


def test_padronizar_piora_o_knn(base):
    yte = base[ALVO][-N_TESTE:]
    for k in (3, 5, 10):
        _, com = _ajustar(base, FEATURES, KNeighborsRegressor(n_neighbors=k),
                          padronizar=True)
        _, sem = _ajustar(base, FEATURES, KNeighborsRegressor(n_neighbors=k),
                          padronizar=False)
        assert _mape(yte, sem) < _mape(yte, com), k


def test_sem_padronizar_a_distancia_e_so_das_defasagens(base):
    """O motivo medido do achado 5: sen e cos nao participam da distancia."""
    Xtr, _, _, _, _ = _fatiar(base, FEATURES, alvo_em_razao=False)
    variancias = Xtr.var(axis=0)
    participacao = variancias / variancias.sum()
    porcento = dict(zip(FEATURES, participacao * 100))
    assert porcento["lag1"] + porcento["lag12"] > 99.99
    assert porcento["sen"] < 1e-6
    assert porcento["cos"] < 1e-6


# --------------------------------------------------------------------------
# Achado 6: o modelo do fecho bate a baseline da LDC


def test_o_modelo_do_fecho_bate_a_baseline_da_ldc(base):
    linhas, _ = _baselines(base)
    yte = base[ALVO][-N_TESTE:]
    _, previsto = _ajustar(base, FEATURES_FECHO, LinearRegression(),
                           alvo_em_razao=True, padronizar=True)
    assert len(FEATURES_FECHO) == 11
    assert _mape(yte, previsto) < _mape(yte, linhas["C"])
    assert _rmse(yte, previsto) < _rmse(yte, linhas["C"])
    assert 3.1 < _mape(yte, previsto) < 3.5
    assert 44e6 < _rmse(yte, previsto) < 50e6


def test_o_fecho_ganha_de_todos_os_modelos_da_aula(base):
    yte = base[ALVO][-N_TESTE:]
    _, fecho = _ajustar(base, FEATURES_FECHO, LinearRegression(),
                        alvo_em_razao=True, padronizar=True)
    for modelo, razao, padronizar in [
        (DecisionTreeRegressor(max_depth=3, random_state=SEMENTE), True, False),
        (RandomForestRegressor(n_estimators=300, random_state=SEMENTE), True, False),
        (KNeighborsRegressor(n_neighbors=5), True, False),
        (LinearRegression(), False, True),
    ]:
        _, p = _ajustar(base, FEATURES, modelo, alvo_em_razao=razao,
                        padronizar=padronizar)
        assert _mape(yte, fecho) < _mape(yte, p)

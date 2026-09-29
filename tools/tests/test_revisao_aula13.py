"""Trava os números que a revisão da Aula 13 afirma, e impede que a aula entregue a prova.

A Aula 13 é a revisão, em sala invertida, dos conteúdos de computação da Prova
de 02/10 (`docs/adrs/ADR-016`). Ela não tem modelo novo: cada número do deck e do
material é uma medição sobre os CSVs de `dados/`, e esta suíte refaz as contas
de forma independente de `tools/graficos_aula13.py`, que gera as figuras.

Quatro grupos de teste:

  1  os números. Vazamento (2,86% contra 2,43%), identificador sequencial
     (0,00% no treino, 6,83% no teste, um só valor previsto), reapresentação
     (floresta de 5,70% para 1,31%, e 1,31% também medida em 100 meses),
     métricas de regressão (MAE 34,1, viés -12,1, RMSE 40,7, R2 0,54), a
     matriz da regressão logística (17, 3, 2, 2) com o deslocamento do
     limiar, e a regressão simples de frangos sobre suínos do trimestre
     anterior (r 0,971, R2 0,95 no sorteio e -5,81 por data).
  2  o texto. Cada número acima precisa aparecer no deck e no material com a
     mesma formatação, e os quatro SVG do deck precisam ser os que
     `tools/svg_aula13.py` gera hoje a partir dos dados.
  3  o notebook. Versionado sem saída, e a verificação do autodiagnóstico
     aceita a resposta certa e recusa a errada, com `AssertionError`.
  4  a prova. Nenhum arquivo da aula pode conter os cenários, os números ou a
     matriz de confusão da prova. A lista está codificada em base64 de
     propósito, para não publicar em claro o que ela protege, e cada padrão
     é conferido contra uma amostra própria, para o detector não ser um teste
     que nunca falha.

Versões propositalmente quebradas executadas contra esta suíte, e o teste que
reprovou cada uma:

  trocar "2,43%" por "2,34%" no título do slide 12 do deck
    -> `test_os_titulos_e_as_celulas_do_deck_saem_dos_dados`. A primeira versão
       desta suíte só procurava o número solto no texto, e essa mutação passava,
       porque "2,43%" também aparece na tabela do mesmo slide. Por isso existe o
       teste que monta título e célula a partir do valor calculado.
  escrever "triagem" num comentário de `materiais/aula13.html`
    -> `test_nenhum_arquivo_da_aula_contem_a_prova`.
  inverter um bit do resumo da q5 no notebook
    -> `test_o_autodiagnostico_aceita_o_certo_e_recusa_o_errado`.
  mudar o `random_state` do sorteio para 7 em `tools/svg_aula13.py`
    -> `test_os_svg_do_deck_estao_em_dia_com_os_dados`.

Precisa de numpy, pandas e scikit-learn, do requirements-ci.txt. Sem eles o
arquivo inteiro se pula.
"""
import base64
import calendar
import json
import os
import re
import sys

import pytest

np = pytest.importorskip("numpy")
pd = pytest.importorskip("pandas")
pytest.importorskip("sklearn")

from sklearn.ensemble import RandomForestRegressor  # noqa: E402
from sklearn.linear_model import LinearRegression, LogisticRegression  # noqa: E402
from sklearn.metrics import confusion_matrix, r2_score  # noqa: E402
from sklearn.model_selection import train_test_split  # noqa: E402
from sklearn.naive_bayes import GaussianNB  # noqa: E402
from sklearn.neighbors import KNeighborsRegressor  # noqa: E402
from sklearn.pipeline import Pipeline  # noqa: E402
from sklearn.preprocessing import StandardScaler  # noqa: E402
from sklearn.svm import SVC  # noqa: E402
from sklearn.tree import DecisionTreeRegressor  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DADOS = os.path.join(RAIZ, "dados")
DECK = os.path.join(RAIZ, "aulas", "aula13.html")
MATERIAL = os.path.join(RAIZ, "materiais", "aula13.html")
REFERENCIAS = os.path.join(RAIZ, "referencias", "aula13.html")
NOTEBOOK = os.path.join(RAIZ, "notebooks", "aula13.ipynb")
NOTAS = os.path.join(RAIZ, "docs", "notas-do-professor", "aula13.md")
ARQUIVOS_DA_AULA = [DECK, MATERIAL, REFERENCIAS, NOTEBOOK, NOTAS,
                    os.path.join(RAIZ, "tools", "graficos_aula13.py"),
                    os.path.join(RAIZ, "tools", "svg_aula13.py")]

SERIES = ["abate_bovinos", "abate_suinos", "abate_frangos",
          "producao_ovos", "producao_leite"]
ALVO = "abate_frangos"
FEATURES = (["lag1", "lag2", "lag3", "lag12", "sen", "cos", "dias"]
            + [s + "_lag1" for s in SERIES if s != ALVO])
N_TESTE = 24


def _ler(caminho):
    with open(caminho, encoding="utf-8") as fh:
        return fh.read()


def _mape(real, previsto):
    return float(np.mean(np.abs((real - previsto) / real)) * 100)


def _pipe(modelo):
    return Pipeline([("escala", StandardScaler()), ("modelo", modelo)])


@pytest.fixture(scope="module")
def mensal():
    base = None
    for nome in SERIES:
        c = (pd.read_csv(os.path.join(DADOS, "mensal", nome + ".csv"))[["periodo", "valor"]]
             .rename(columns={"valor": nome}))
        base = c if base is None else base.merge(c, on="periodo", how="inner")
    base = base.sort_values("periodo").reset_index(drop=True)
    mes = base["periodo"].str[-2:].astype(int)
    base["dias"] = [calendar.monthrange(int(p[:4]), int(p[-2:]))[1] for p in base["periodo"]]
    base["sen"], base["cos"] = np.sin(2 * np.pi * mes / 12), np.cos(2 * np.pi * mes / 12)
    for k in (1, 2, 3, 12):
        base["lag%d" % k] = base[ALVO].shift(k)
    for nome in SERIES:
        if nome != ALVO:
            base[nome + "_lag1"] = base[nome].shift(1)
    base = base.dropna().reset_index(drop=True)
    corte = len(base) - N_TESTE
    return {"base": base, "corte": corte, "X": base[FEATURES].to_numpy(),
            "y": base[ALVO].to_numpy()}


@pytest.fixture(scope="module")
def linear(mensal):
    c, X, y = mensal["corte"], mensal["X"], mensal["y"]
    return _pipe(LinearRegression()).fit(X[:c], y[:c])


@pytest.fixture(scope="module")
def classificacao(mensal):
    c, X, base = mensal["corte"], mensal["X"], mensal["base"]
    alvo = (base[ALVO] > base["lag12"]).astype(int).to_numpy()
    esc = StandardScaler().fit(X[:c])
    return {"Ztr": esc.transform(X[:c]), "Zte": esc.transform(X[c:]),
            "atr": alvo[:c], "ate": alvo[c:], "periodos": list(base["periodo"].iloc[c:])}


@pytest.fixture(scope="module")
def trimestral():
    """O mesmo código do slide 17, sobre os CSVs crus."""
    fr = pd.read_csv(os.path.join(DADOS, "abate_frangos.csv"))
    su = pd.read_csv(os.path.join(DADOS, "abate_suinos.csv"))
    df = fr.merge(su, on="periodo", suffixes=("_fr", "_su"))
    df["suinos_lag1"] = df["valor_su"].shift(1)
    return df.dropna()


def _contar(real, previsto):
    tn, fp, fn, tp = confusion_matrix(real, previsto, labels=[0, 1]).ravel()
    return int(tp), int(fn), int(fp), int(tn)


# ---------------------------------------------------------------- 1. números
def test_a_base_mensal_e_a_das_aulas_07_a_12(mensal):
    assert len(mensal["base"]) == 339
    assert mensal["corte"] == 315
    assert mensal["base"]["periodo"].iloc[315] == "2024-04"


def test_as_series_do_proprio_mes_vazam_e_melhoram_o_teste(mensal, linear):
    c, base, y = mensal["corte"], mensal["base"], mensal["y"]
    honesto = _mape(y[c:], linear.predict(mensal["X"][c:]))
    cols = FEATURES[:7] + [s for s in SERIES if s != ALVO]
    Xc = base[cols].to_numpy()
    vazado = _mape(y[c:], _pipe(LinearRegression()).fit(Xc[:c], y[:c]).predict(Xc[c:]))
    assert abs(honesto - 2.862) < 0.001
    assert abs(vazado - 2.426) < 0.001
    assert vazado < honesto


def test_o_numero_da_linha_memoriza_o_treino_e_nao_generaliza(mensal):
    c, y = mensal["corte"], mensal["y"]
    idx = np.arange(len(y)).reshape(-1, 1)
    arvore = DecisionTreeRegressor(random_state=42).fit(idx[:c], y[:c])
    prev = arvore.predict(idx[c:])
    assert _mape(y[:c], arvore.predict(idx[:c])) == 0.0
    assert abs(_mape(y[c:], prev) - 6.83) < 0.005
    assert np.unique(prev).size == 1
    assert abs(prev[0] / 1e6 - 1101.6) < 0.05


def test_medir_em_dado_ja_visto_e_otimista_e_o_tamanho_do_teste_nao_corrige(mensal, linear):
    c, X, y = mensal["corte"], mensal["X"], mensal["y"]

    def floresta():
        return _pipe(RandomForestRegressor(n_estimators=300, random_state=42))

    f = floresta().fit(X[:c], y[:c])
    f_tudo = floresta().fit(X, y)
    honesto, treino = _mape(y[c:], f.predict(X[c:])), _mape(y[:c], f.predict(X[:c]))
    tudo, tudo_100 = _mape(y[c:], f_tudo.predict(X[c:])), _mape(y[-100:], f_tudo.predict(X[-100:]))
    assert abs(honesto - 5.70) < 0.005
    assert abs(treino - 1.44) < 0.005
    assert abs(tudo - 1.31) < 0.005
    assert abs(tudo_100 - 1.31) < 0.005
    assert tudo < honesto / 4

    lin_treino = _mape(y[:c], linear.predict(X[:c]))
    lin_tudo = _mape(y[c:], _pipe(LinearRegression()).fit(X, y).predict(X[c:]))
    assert abs(lin_treino - 3.22) < 0.005
    assert abs(lin_tudo - 2.65) < 0.005
    # a ressalva do material: o erro de treino da linear fica ACIMA do de teste
    assert lin_treino > _mape(y[c:], linear.predict(X[c:]))


def test_as_metricas_de_regressao_do_modelo_da_aula_12(mensal, linear):
    c, y = mensal["corte"], mensal["y"]
    erro = linear.predict(mensal["X"][c:]) - y[c:]
    mae, vies = np.mean(np.abs(erro)) / 1e6, np.mean(erro) / 1e6
    rmse = np.sqrt(np.mean(erro ** 2)) / 1e6
    assert abs(mae - 34.05) < 0.01
    assert abs(vies - (-12.11)) < 0.01
    assert abs(rmse - 40.70) < 0.01
    assert rmse >= mae
    assert abs(r2_score(y[c:], y[c:] + erro) - 0.537) < 0.001
    assert abs(np.max(np.abs(erro)) / 1e6 - 90.17) < 0.01
    assert abs(y[c:].mean() / 1e6 - 1181.95) < 0.01
    assert int(np.sum(erro == 0)) == 0
    assert int(np.sum(erro > 0)) == 7
    assert abs(np.mean(np.abs(erro - erro.mean())) / 1e6 - 31.53) < 0.01


def test_a_matriz_da_logistica_e_o_empate_com_a_baseline(classificacao):
    Ztr, Zte, atr, ate = (classificacao[k] for k in ("Ztr", "Zte", "atr", "ate"))
    assert int(ate.sum()) == 20
    log = LogisticRegression(max_iter=2000, random_state=42).fit(Ztr, atr)
    assert _contar(ate, log.predict(Zte)) == (17, 3, 2, 2)
    assert _contar(ate, SVC(kernel="linear", random_state=42).fit(Ztr, atr).predict(Zte)) == (18, 2, 2, 2)
    assert _contar(ate, np.ones_like(ate)) == (20, 0, 4, 0)

    prob = log.predict_proba(Zte)[:, 1]
    esperado = {0.4: (19, 1, 3, 1), 0.5: (17, 3, 2, 2), 0.6: (13, 7, 2, 2), 0.7: (11, 9, 0, 4)}
    for t, cont in esperado.items():
        assert _contar(ate, (prob >= t).astype(int)) == cont, t


def test_os_seis_meses_do_slide_25_estao_certos(classificacao):
    log = LogisticRegression(max_iter=2000, random_state=42).fit(
        classificacao["Ztr"], classificacao["atr"])
    prev = dict(zip(classificacao["periodos"], log.predict(classificacao["Zte"])))
    real = dict(zip(classificacao["periodos"], classificacao["ate"]))
    nome = {1: "alta", 0: "queda"}
    deck = _ler(DECK)
    for mes, rotulo in [("2024-04", "abr/24"), ("2024-05", "mai/24"), ("2024-06", "jun/24"),
                        ("2025-02", "fev/25"), ("2025-08", "ago/25"), ("2025-10", "out/25")]:
        linha = "<tr><td>%s</td><td>%s</td><td>%s</td><td></td></tr>" % (
            rotulo, nome[int(real[mes])], nome[int(prev[mes])])
        assert linha in deck, mes


def test_a_regressao_simples_e_as_duas_divisoes(trimestral):
    df = trimestral
    assert len(df) == 116
    assert df["periodo"].iloc[0] == "1997-T2" and df["periodo"].iloc[-1] == "2026-T1"
    assert int(df[["valor_fr", "valor_su"]].isna().sum().sum()) == 0
    X, y = df[["suinos_lag1"]], df["valor_fr"]
    assert abs(np.corrcoef(df["suinos_lag1"], y)[0, 1] - 0.971) < 0.0005

    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2, random_state=42)
    reta = LinearRegression().fit(X_tr, y_tr)
    assert len(y_te) == 24 and len(y_tr) == 92
    assert abs(reta.coef_[0] - 2.29) < 0.005
    assert abs(reta.score(X_te, y_te) - 0.951) < 0.001
    assert abs(np.sqrt(np.mean((y_te - reta.predict(X_te)) ** 2)) / 1e6 - 179.2) < 0.05

    reta_c = LinearRegression().fit(X.iloc[:92], y.iloc[:92])
    prev_c = reta_c.predict(X.iloc[92:])
    assert df["periodo"].iloc[92] == "2020-T2"
    assert abs(reta_c.coef_[0] - 2.80) < 0.005
    assert abs(r2_score(y.iloc[92:], prev_c) - (-5.807)) < 0.001
    assert abs(np.sqrt(np.mean((y.iloc[92:] - prev_c) ** 2)) / 1e6 - 552.9) < 0.05
    assert int(np.sum(prev_c > y.iloc[92:].to_numpy())) == 24

    minimos = {}
    for tamanho in (4, 8, 24):
        r2s = []
        for s in range(20):
            a, b, c, d = train_test_split(X, y, test_size=tamanho, random_state=s)
            r2s.append(r2_score(d, LinearRegression().fit(a, c).predict(b)))
        minimos[tamanho] = min(r2s)
    assert abs(minimos[4] - (-0.25)) < 0.005
    assert abs(minimos[8] - 0.61) < 0.005
    assert abs(minimos[24] - 0.91) < 0.005


# ---------------------------------------------------------------- 2. texto
NO_DECK = ["2,86%", "2,43%", "0,00%", "6,83%", "1.101,6 milhões", "5,70%", "1,31%", "1.481 bytes",
           "34,1 milhões", "-12,1 milhões", "40,7 milhões", "0,54", "90,2", "0 de 24",
           "7 dos 24", "1.181,9", "83,3%", "79,2%", "17/19", "17/20", "0,87", "r de 0,971",
           "2,29", "0,95", "-5,81", "179,2", "552,9", "-0,25", "0,91", "116 trimestres",
           "2020-T1", "peso 20", "ART.8 Modelo Final, peso 4",
           "ART.9 Critérios de Publicação, peso 3"]
NO_MATERIAL = ["2,86%", "2,43%", "0,00%", "6,83%", "1.101,6 milhões", "5,70%", "1,44%", "3,22%",
               "1,31%", "2,65%", "34,1 milhões", "-12,1 milhões", "40,7 milhões", "0,54",
               "90,2", "31,5", "7 dos 24", "1.181,9", "0 de 24", "83,3%", "79,2%", "0,971",
               "2,29", "0,95", "-5,81", "2,80", "179,2", "552,9", "-0,25", "0,61", "0,91",
               "TP = 17", "FN = 3", "FP = 2", "TN = 2", "252 dos 252", "Prova 02/10, peso 20",
               "ART.8 Modelo Final, peso 4", "ART.9 Critérios de Publicação,\n        peso 3"]


def test_o_deck_afirma_os_numeros_medidos():
    deck = _ler(DECK)
    faltam = [n for n in NO_DECK if n not in deck]
    assert not faltam, faltam


def _v(valor, casas):
    return ("%.*f" % (casas, valor)).replace(".", ",")


def test_os_titulos_e_as_celulas_do_deck_saem_dos_dados(mensal, linear, classificacao, trimestral):
    """Mais forte que procurar o número solto: cada título e cada célula-chave é
    montado aqui a partir do valor calculado, e precisa existir exatamente assim."""
    deck = _ler(DECK)
    titulos = [t.strip() for t in re.findall(r"<h2>(.*?)</h2>", deck, re.S)]
    c, X, y, base = mensal["corte"], mensal["X"], mensal["y"], mensal["base"]

    cols = FEATURES[:7] + [s for s in SERIES if s != ALVO]
    Xc = base[cols].to_numpy()
    vazado = _mape(y[c:], _pipe(LinearRegression()).fit(Xc[:c], y[:c]).predict(Xc[c:]))
    f_tudo = _pipe(RandomForestRegressor(n_estimators=300, random_state=42)).fit(X, y)
    erro = linear.predict(X[c:]) - y[c:]

    df = trimestral
    Xs, ys = df[["suinos_lag1"]], df["valor_fr"]
    a, b, cc, d = train_test_split(Xs, ys, test_size=0.2, random_state=42)
    r2_ale = LinearRegression().fit(a, cc).score(b, d)
    r2_cro = LinearRegression().fit(Xs.iloc[:92], ys.iloc[:92]).score(Xs.iloc[92:], ys.iloc[92:])

    log = LogisticRegression(max_iter=2000, random_state=42).fit(
        classificacao["Ztr"], classificacao["atr"])
    ate = classificacao["ate"]
    tp, fn, fp, tn = _contar(ate, log.predict(classificacao["Zte"]))
    prob = log.predict_proba(classificacao["Zte"])[:, 1]
    tp7, fn7, fp7, tn7 = _contar(ate, (prob >= 0.7).astype(int))

    esperados = [
        "As séries do próprio mês levam o MAPE a %s%%" % _v(vazado, 2),
        "Medir em dado já visto leva a floresta a %s%%" % _v(_mape(y[c:], f_tudo.predict(X[c:])), 2),
        "Frangos e suínos defasados têm r de %s" % _v(np.corrcoef(df["suinos_lag1"], ys)[0, 1], 3),
        "A reta tem R² de %s no sorteio e %s por data" % (_v(r2_ale, 2), _v(r2_cro, 2)),
        "O modelo erra em média %s milhões de kg" % _v(np.mean(np.abs(erro)) / 1e6, 1),
        "A regressão logística acerta %d dos 24 meses" % (tp + tn),
        "Prever sempre alta dá %s%% e nenhuma queda" % _v(100 * ate.mean(), 1),
        "O limiar de 0,7 zera os FP e leva os FN a %d" % fn7,
    ]
    assert fp7 == 0
    for t in esperados:
        assert t in titulos, t

    for limiar in (0.4, 0.5, 0.6, 0.7):
        tp_, fn_, fp_, tn_ = _contar(ate, (prob >= limiar).astype(int))
        linha = "<tr><td>%s</td><td>%d</td><td>%d</td><td>%s</td><td>%s</td></tr>" % (
            _v(limiar, 1), fp_, fn_, _v(tp_ / (tp_ + fp_), 2), _v(tp_ / (tp_ + fn_), 2))
        assert linha in deck, linha
    assert "17/%d" % (tp + fp) in deck and "17/%d" % (tp + fn) in deck
    assert "<td>MAE</td><td>%s milhões de kg</td>" % _v(np.mean(np.abs(erro)) / 1e6, 1) in deck
    assert "<td>Viés</td><td>%s milhões de kg</td>" % _v(np.mean(erro) / 1e6, 1) in deck


def test_o_material_afirma_os_numeros_medidos():
    material = _ler(MATERIAL)
    faltam = [n for n in NO_MATERIAL if n not in material]
    assert not faltam, faltam


def test_os_pesos_citados_sao_os_do_plano_de_ensino():
    plano = _ler(os.path.join(RAIZ, "PLANO_DE_ENSINO.md"))
    for trecho in ("Prova 02/10 (20)", "ART.8 Modelo Final (4)",
                   "ART.9 Critérios de Publicação (3)"):
        assert trecho in plano


def test_os_autoestudos_sao_os_da_semana_09_com_titulo_exato():
    fonte = _ler(os.path.join(RAIZ, "docs", "autoestudos-por-semana.md"))
    semana = fonte.split("## Semana 09")[1].split("## Semana 10")[0]
    refs = _ler(REFERENCIAS)
    for titulo in ("How to Build a Machine Learning App using Streamlit",
                   "Streamlit 101 - A faster way to build and share data apps"):
        assert "- " + titulo in semana
        assert titulo in refs


def test_os_svg_do_deck_estao_em_dia_com_os_dados():
    sys.path.insert(0, os.path.join(RAIZ, "tools"))
    import svg_aula13
    deck = _ler(DECK)
    for nome, svg in svg_aula13.blocos().items():
        m = re.search(r"<!-- svg:%s -->\n(.*?)\n<!-- /svg:%s -->" % (nome, nome), deck, re.S)
        assert m, nome
        assert m.group(1) == svg, nome


def test_as_animacoes_param_sem_movimento_e_na_impressao():
    deck = _ler(DECK)
    estilo = deck.split("<style>")[1].split("</style>")[0]
    assert "prefers-reduced-motion: reduce" in estilo
    assert "@media print" in estilo
    assert "html.print-pdf" in estilo
    # toda regra de animacao vive dentro de section.present, entao o estado
    # sem animacao e o estado final
    for regra in re.findall(r"[^{}]*\{[^{}]*animation(?:-name)?\s*:[^{}]*\}", estilo):
        if "none" in regra:
            continue
        assert "section.present" in regra, regra
    assert deck.count("a13-etapa a13-etapa-") == 4
    assert deck.count(' a13-padrao"') == 1


# ---------------------------------------------------------------- 3. notebook
def test_o_notebook_e_versionado_sem_saida():
    nb = json.loads(_ler(NOTEBOOK))
    for c in nb["cells"]:
        if c["cell_type"] == "code":
            assert c["outputs"] == [] and c["execution_count"] is None


def _executar_celulas(indices, monkeypatch):
    monkeypatch.chdir(os.path.join(RAIZ, "notebooks"))
    monkeypatch.setenv("MPLBACKEND", "Agg")
    nb = json.loads(_ler(NOTEBOOK))
    codigo = [c for c in nb["cells"] if c["cell_type"] == "code"]
    ns = {}
    for i in indices:
        exec("".join(codigo[i]["source"]), ns)
    return ns


def test_o_autodiagnostico_aceita_o_certo_e_recusa_o_errado(mensal, classificacao, monkeypatch):
    ns = _executar_celulas([0, 1], monkeypatch)
    c, X, y, base = mensal["corte"], mensal["X"], mensal["y"], mensal["base"]

    idx = np.arange(len(y)).reshape(-1, 1)
    rf = RandomForestRegressor(n_estimators=300, random_state=42).fit(idx[:c], y[:c])
    knn = lambda: _pipe(KNeighborsRegressor(n_neighbors=5))  # noqa: E731
    erro_saz = base["lag12"].to_numpy()[c:] - y[c:]

    tri = None
    for nome in SERIES:
        s = (pd.read_csv(os.path.join(DADOS, nome + ".csv"))[["periodo", "valor"]]
             .rename(columns={"valor": nome}))
        tri = s if tri is None else tri.merge(s, on="periodo")
    tri["leite_lag1"] = tri["producao_leite"].shift(1)
    tri = tri.dropna().reset_index(drop=True)
    Xl, yl = tri[["leite_lag1"]], tri["abate_frangos"]
    a, b, cc, d = train_test_split(Xl, yl, test_size=0.2, random_state=42)

    Ztr, Zte, atr, ate = (classificacao[k] for k in ("Ztr", "Zte", "atr", "ate"))
    prob = LogisticRegression(max_iter=2000, random_state=42).fit(Ztr, atr).predict_proba(Zte)[:, 1]
    alta_08 = (prob >= 0.8).astype(int)

    certas = {
        "q1": "ACD",
        "q2": np.unique(rf.predict(idx[c:])).size,
        "q3": _mape(y[c:], knn().fit(X[:c], y[:c]).predict(X[c:])),
        "q4": _mape(y[c:], knn().fit(X, y).predict(X[c:])),
        "q5": np.mean(np.abs(erro_saz)) / 1e6,
        "q6": np.mean(erro_saz) / 1e6,
        "q7": "B",
        "q8": np.corrcoef(tri["leite_lag1"], yl)[0, 1],
        "q9": r2_score(d, LinearRegression().fit(a, cc).predict(b)),
        "q10": r2_score(yl.iloc[92:], LinearRegression().fit(Xl.iloc[:92], yl.iloc[:92])
                        .predict(Xl.iloc[92:])),
        "q11": "B",
        "q12": _contar(ate, GaussianNB().fit(Ztr, atr).predict(Zte)),
        "q13": int((alta_08 & ate).sum()) / int(ate.sum()),
        "q14": "C", "q15": "A", "q16": "D",
    }
    assert set(certas) == set(ns["GABARITO"])
    for chave, valor in certas.items():
        ns["verificar"](chave, valor)
    assert all(ns["RESULTADO"].values()) and len(ns["RESULTADO"]) == 16

    erradas = {"q1": "AB", "q2": 24, "q3": 5.29, "q5": 34.05, "q6": 53.9, "q7": "D",
               "q10": 0.78, "q12": (20, 0, 4, 0), "q14": "A", "q16": "C"}
    for chave, valor in erradas.items():
        with pytest.raises(AssertionError):
            ns["verificar"](chave, valor)

    # sem resposta, nada levanta: e o que o CI executa
    for chave in certas:
        ns["verificar"](chave, None)


# ---------------------------------------------------------------- 4. a prova
_PROIBIDOS = (
    "W1siXFxic29ub1xcYiIsICJvIGFwcCBkbyBzb25vIl0sIFsibW9kbyBkb3JtaXIiLCAibW9kbyBk"
    "b3JtaXIiXSwgWyJpbW9iaWxpIiwgInVtYSBpbW9iaWxpw6FyaWEiXSwgWyJcXGJhbHVndWUiLCAi"
    "byBhbHVndWVsIHBvciDDoXJlYSJdLCBbImVudHJlZ2EgZGUgY29taWRhIiwgInRlbXBvIGRlIGVu"
    "dHJlZ2EgZGUgY29taWRhIl0sIFsiXFxiZGVsaXZlcnlcXGIiLCAiZGVsaXZlcnkiXSwgWyJcXGJF"
    "UlBcXGIiLCAiZGFkb3MgZG8gRVJQIl0sIFsicmVkZXMgc29jaWFpcyIsICJyZWRlcyBzb2NpYWlz"
    "Il0sIFsic3RyZWFtaW5nIiwgInN0cmVhbWluZyJdLCBbIm1bw7p1XXNpY2EiLCAibcO6c2ljYSJd"
    "LCBbImZhaXhhIGV0W8OhYV1yaWEiLCAiZmFpeGEgZXTDoXJpYSJdLCBbImNhbmNlbGFtZW50byBk"
    "ZSBhc3NpbmF0dXJhIiwgImNhbmNlbGFtZW50byBkZSBhc3NpbmF0dXJhIl0sIFsiYXJ0aWdvcyBl"
    "c3BvcnRpdm9zIiwgImFydGlnb3MgZXNwb3J0aXZvcyJdLCBbImFuW8O6dV1uY2lvIiwgImludmVz"
    "dGltZW50byBlbSBhbsO6bmNpb3MiXSwgWyJ2ZW5kYXMgcG9yIHNlbWFuYSIsICJ2ZW5kYXMgcG9y"
    "IHNlbWFuYSJdLCBbImV4YW1lIGRlIHNhbmd1ZSIsICJleGFtZSBkZSBzYW5ndWUiXSwgWyJcXGJ0"
    "cmlhZ2VtXFxiIiwgInRyaWFnZW0iXSwgWyJcXGJwYWNpZW50ZXM/XFxiIiwgIjEwIHBhY2llbnRl"
    "cyJdLCBbImxhYm9yYXRbw7NvXXJpbyIsICJsYWJvcmF0w7NyaW8iXSwgWyJpbWFnZW5zIGRlIGZv"
    "cm5lY2Vkb3JlcyIsICJpbWFnZW5zIGRlIGZvcm5lY2Vkb3JlcyJdLCBbIlvDoWFddWRpb3M/IGRl"
    "IGF0ZW5kaW1lbnRvIiwgIsOhdWRpb3MgZGUgYXRlbmRpbWVudG8iXSwgWyIwWywuXTk5OCIsICJy"
    "ID0gMCw5OTgiXSwgWyIoPzwhW1xcZCwuXSkzWywuXTcxKD8hXFxkKSIsICIzLDcxIl0sIFsiMFss"
    "Ll0wNzgiLCAiMCwwNzgiXSwgWyI5NlssLl0wMCIsICI5NiwwMCJdLCBbIig/PCFbXFxkLC5dKTFc"
    "XC4yMDAoPyFbXFxkLF0pIiwgIjEuMjAwIGltw7N2ZWlzIl0sIFsiKD88IVtcXGQsLl0pMlxcLjAw"
    "MCg/IVtcXGQsXSkiLCAiMi4wMDAgcGVkaWRvcyJdLCBbIig/PCFbXFxkLC5dKTk1XFxzPyUiLCAi"
    "OTUlIl0sIFsiKD88IVtcXGQsLl0pMlxccz8lIiwgIjIlIl0sIFsiTUFFXFxzKig/Oj18aWd1YWwg"
    "YXxkZXzDqSlcXHMqNCg/IVtcXGQsLl0pIiwgIk1BRSBpZ3VhbCBhIDQiXSwgWyJcXChcXHMqNFxc"
    "cyosXFxzKjFcXHMqLFxccyoyXFxzKixcXHMqM1xccypcXCkiLCAiKDQsIDEsIDIsIDMpIl0sIFsi"
    "VFBcXFd7MSw0fTRcXGJbXlxcbl17MCw0MH1GTlxcV3sxLDR9MVxcYiIsICJUUCA9IDQsIEZOID0g"
    "MSJdXQ=="
)


def _padroes():
    return [(re.compile(p, re.I), amostra)
            for p, amostra in json.loads(base64.b64decode(_PROIBIDOS).decode("utf-8"))]


def _achados(texto):
    return [p.pattern for p, _ in _padroes() if p.search(texto)]


def test_o_detector_pega_cada_termo_da_prova():
    """O detector precisa conseguir falhar: cada padrão pega a própria amostra."""
    padroes = _padroes()
    assert len(padroes) >= 30
    for padrao, amostra in padroes:
        assert padrao.search(amostra), padrao.pattern
        assert padrao.pattern in _achados(_ler(DECK) + "\n" + amostra)


def test_nenhum_arquivo_da_aula_contem_a_prova():
    for caminho in ARQUIVOS_DA_AULA:
        achados = _achados(_ler(caminho))
        assert not achados, (os.path.relpath(caminho, RAIZ), achados)


def test_o_deck_lista_temas_e_nao_questoes():
    deck = _ler(DECK)
    assert not re.search(r"quest(ão|ões)\s+\d", deck, re.I)
    assert not re.search(r"\d+\s+quest(ão|ões)", deck, re.I)
    assert "Temas de computação da Prova de 02/10" in deck

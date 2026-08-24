"""Trava as conclusoes que a Aula 05 afirma sobre o primeiro modelo do case.

O deck, o material de apoio, as notas do professor e o notebook da Aula 05
citam metricas de um modelo ajustado sobre os CSVs reais. Se algum CSV for
regerado com dado novo do SIDRA, uma conclusao pode virar, e os quatro
artefatos passam a ensinar algo que o dado nao sustenta mais.

Como em `test_hipoteses_aula04.py`, o que se trava aqui sao as **conclusoes**,
e nao apenas os numeros:

1. o modelo ganha da baseline de coeficiente fixo no conjunto de teste;
2. o leite piora o erro fora da amostra, e por isso fica fora do modelo;
3. sem padronizar, os coeficientes de sazonalidade saem zerados por corte
   numerico, o que e o achado que contradiz parcialmente a Aula 04;
4. o modelo vence a baseline nas doze janelas medidas;
5. os residuos do modelo rejeitam normalidade.

Os valores sao conferidos com folga, por faixa, para o teste nao quebrar por
diferenca de versao de scikit-learn. As faixas sao estreitas o bastante para
falhar se a conclusao mudar.

Precisa de numpy, scipy e scikit-learn, que estao no requirements-ci.txt. Sem
eles o arquivo inteiro se pula, e o CI continua cobrindo.

Cada assercao aqui foi vista falhando ao menos uma vez, contra tres versoes
propositalmente quebradas do pipeline: embaralhar as linhas de treino, remover
a padronizacao e reduzir as doze janelas a uma. As tres derrubam pelo menos um
teste deste arquivo.

Uma quarta mutacao foi tentada e **nao** derruba nenhum teste: ajustar o
StandardScaler sobre treino e teste juntos, que e a segunda forma de vazamento
descrita no material de apoio. O motivo esta medido em
`test_vazamento_do_escalador_nao_muda_a_metrica_neste_modelo`, e nao e uma
falha de cobertura: regressao linear sem regularizacao e invariante a
transformacao afim das entradas, entao esse vazamento e inofensivo **neste**
modelo. Escrever um teste que fingisse detecta-lo produziria a assercao que
nunca falha, contra a qual a secao 8.2 da skill `inteli-course-design` adverte.
"""
import csv
import os

import pytest

np = pytest.importorskip("numpy")
pytest.importorskip("scipy.stats")
linear_model = pytest.importorskip("sklearn.linear_model")
preprocessing = pytest.importorskip("sklearn.preprocessing")
metrics = pytest.importorskip("sklearn.metrics")
from scipy import stats  # noqa: E402  (depois do importorskip, de proposito)

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DADOS = os.path.join(RAIZ, "dados")

SERIES = ["abate_bovinos", "abate_suinos", "abate_frangos",
          "producao_ovos", "producao_leite"]
ALVO = "abate_frangos"
FEATURES = ["frangos_lag1", "frangos_lag4", "sen", "cos"]
N_TESTE = 8


def _serie(nome):
    caminho = os.path.join(DADOS, nome + ".csv")
    with open(caminho, encoding="utf-8") as fh:
        return {linha["periodo"]: float(linha["valor"])
                for linha in csv.DictReader(fh) if linha["valor"]}


@pytest.fixture(scope="module")
def base():
    """A base analitica da Aula 04: juncao inner, defasagens e sazonalidade."""
    series = {nome: _serie(nome) for nome in SERIES}
    comuns = sorted(set.intersection(*[set(s) for s in series.values()]))

    colunas = {nome: np.array([series[nome][p] for p in comuns]) for nome in SERIES}
    trimestre = np.array([int(p[-1]) for p in comuns])

    alvo = colunas[ALVO]
    lag1 = np.concatenate([[np.nan], alvo[:-1]])
    lag4 = np.concatenate([[np.nan] * 4, alvo[:-4]])
    sen = np.sin(2 * np.pi * trimestre / 4)
    cos = np.cos(2 * np.pi * trimestre / 4)

    # dropna: as 4 primeiras linhas, que shift(4) consome
    corte = 4
    dados = {nome: v[corte:] for nome, v in colunas.items()}
    dados.update({
        "periodo": comuns[corte:],
        "frangos_lag1": lag1[corte:],
        "frangos_lag4": lag4[corte:],
        "sen": sen[corte:],
        "cos": cos[corte:],
    })
    return dados


def _matriz(dados, features, fatia):
    return np.column_stack([dados[f][fatia] for f in features])


def _ajustar(dados, features, n_treino, fatia_teste, padronizar=True):
    treino = slice(0, n_treino)
    X_tr = _matriz(dados, features, treino)
    X_te = _matriz(dados, features, fatia_teste)
    y_tr = dados[ALVO][treino]

    if padronizar:
        escalador = preprocessing.StandardScaler().fit(X_tr)
        X_tr, X_te = escalador.transform(X_tr), escalador.transform(X_te)

    modelo = linear_model.LinearRegression().fit(X_tr, y_tr)
    return modelo, modelo.predict(X_te), modelo.predict(X_tr)


def _mape(real, previsto):
    return float(metrics.mean_absolute_percentage_error(real, previsto)) * 100


def test_base_tem_o_tamanho_que_a_aula_afirma(base):
    """113 linhas, de 1998-T1 a 2026-T1, com 105 de treino e 8 de teste."""
    assert len(base["periodo"]) == 113
    assert base["periodo"][0] == "1998-T1"
    assert base["periodo"][-1] == "2026-T1"
    assert len(base["periodo"]) - N_TESTE == 105


def test_modelo_ganha_da_baseline_no_teste(base):
    """Conclusao central do Bloco 3: o modelo erra menos que o coeficiente fixo."""
    n = len(base["periodo"])
    n_treino = n - N_TESTE
    teste = slice(n_treino, n)

    _, previsto, _ = _ajustar(base, FEATURES, n_treino, teste)
    y_teste = base[ALVO][teste]

    treino = slice(0, n_treino)
    fator = float(np.mean(base[ALVO][treino] / base["frangos_lag4"][treino]))
    baseline = base["frangos_lag4"][teste] * fator

    mape_modelo = _mape(y_teste, previsto)
    mape_baseline = _mape(y_teste, baseline)

    assert mape_modelo < mape_baseline, "o modelo precisa ganhar da baseline no teste"
    assert 1.4 < mape_modelo < 1.8, mape_modelo
    assert 1.5 < mape_baseline < 1.9, mape_baseline
    assert 1.03 < fator < 1.07, fator


def test_baseline_sem_correcao_e_a_pior_das_tres(base):
    """Repetir o ano anterior sem fator erra mais que o dobro das outras duas."""
    n = len(base["periodo"])
    n_treino = n - N_TESTE
    teste = slice(n_treino, n)
    treino = slice(0, n_treino)
    y_teste = base[ALVO][teste]

    fator = float(np.mean(base[ALVO][treino] / base["frangos_lag4"][treino]))
    sem_correcao = _mape(y_teste, base["frangos_lag4"][teste])
    com_correcao = _mape(y_teste, base["frangos_lag4"][teste] * fator)
    persistencia = _mape(y_teste, base["frangos_lag1"][teste])

    assert sem_correcao > 2 * com_correcao
    assert sem_correcao > 2 * persistencia
    assert 4.2 < sem_correcao < 4.9, sem_correcao


def test_leite_piora_o_erro_fora_da_amostra(base):
    """A hipotese que a Aula 04 deixou aberta: o leite fica fora do modelo."""
    n = len(base["periodo"])
    n_treino = n - N_TESTE
    teste = slice(n_treino, n)
    y_teste = base[ALVO][teste]

    _, sem_leite, sem_leite_tr = _ajustar(base, FEATURES, n_treino, teste)
    _, com_leite, com_leite_tr = _ajustar(
        base, FEATURES + ["producao_leite"], n_treino, teste)

    y_treino = base[ALVO][slice(0, n_treino)]

    # a marca do overfitting: melhora no treino, piora no teste
    assert _mape(y_treino, com_leite_tr) < _mape(y_treino, sem_leite_tr)
    assert _mape(y_teste, com_leite) > _mape(y_teste, sem_leite)


def test_sem_padronizar_a_sazonalidade_e_zerada(base):
    """O achado que contradiz parcialmente a Aula 04, e o motivo numerico dele."""
    n = len(base["periodo"])
    n_treino = n - N_TESTE
    teste = slice(n_treino, n)

    cru, _, _ = _ajustar(base, FEATURES, n_treino, teste, padronizar=False)
    coef_sen, coef_cos = cru.coef_[2], cru.coef_[3]

    # zerados por corte numerico: irrisorios diante da escala do alvo (1e9)
    assert abs(coef_sen) < 1.0, coef_sen
    assert abs(coef_cos) < 1.0, coef_cos

    padronizado, _, _ = _ajustar(base, FEATURES, n_treino, teste, padronizar=True)
    escalador = preprocessing.StandardScaler().fit(
        _matriz(base, FEATURES, slice(0, n_treino)))
    na_escala_original = padronizado.coef_ / escalador.scale_

    # com padronizacao os mesmos coeficientes sao milhoes, nao decimos
    assert abs(na_escala_original[2]) > 1e6, na_escala_original[2]
    assert abs(na_escala_original[3]) > 1e6, na_escala_original[3]

    X_tr = _matriz(base, FEATURES, slice(0, n_treino))
    com_intercepto = np.column_stack([np.ones(len(X_tr)), X_tr])
    condicao_crua = np.linalg.cond(com_intercepto)
    condicao_padronizada = np.linalg.cond(
        np.column_stack([np.ones(len(X_tr)), escalador.transform(X_tr)]))

    assert condicao_crua > 1e8, condicao_crua
    assert condicao_padronizada < 100, condicao_padronizada


def test_modelo_vence_nas_doze_janelas(base):
    """A repeticao que sustenta a recomendacao ao parceiro (ADR-008)."""
    n = len(base["periodo"])
    vitorias, mapes_modelo, mapes_baseline = 0, [], []

    for k in range(12, 0, -1):
        n_treino = n - N_TESTE - k + 1
        teste = slice(n_treino, n_treino + N_TESTE)
        treino = slice(0, n_treino)

        _, previsto, _ = _ajustar(base, FEATURES, n_treino, teste)
        y_teste = base[ALVO][teste]
        fator = float(np.mean(base[ALVO][treino] / base["frangos_lag4"][treino]))

        m = _mape(y_teste, previsto)
        b = _mape(y_teste, base["frangos_lag4"][teste] * fator)
        mapes_modelo.append(m)
        mapes_baseline.append(b)
        vitorias += m < b

    assert vitorias == 12, "o modelo precisa vencer nas doze janelas"
    assert np.mean(mapes_modelo) < np.mean(mapes_baseline)
    assert 2.0 < np.mean(mapes_modelo) < 2.4, np.mean(mapes_modelo)
    assert 2.9 < np.mean(mapes_baseline) < 3.4, np.mean(mapes_baseline)


def test_residuos_rejeitam_normalidade(base):
    """Fecha o ciclo que a Aula 04 abriu: a suposicao recai sobre os residuos."""
    n = len(base["periodo"])
    n_treino = n - N_TESTE
    teste = slice(n_treino, n)

    _, _, previsto_treino = _ajustar(base, FEATURES, n_treino, teste)
    residuos = base[ALVO][slice(0, n_treino)] - previsto_treino

    W, p = stats.shapiro(residuos)
    assert p < 0.05, "a aula afirma que os residuos rejeitam normalidade (p=%.4f)" % p
    assert 0.94 < W < 0.99, W

    # propriedade dos minimos quadrados com intercepto, citada no material
    assert abs(residuos.mean()) < 1e-3 * residuos.std()


def test_coeficientes_de_defasagem_somam_perto_de_um(base):
    """O achado do Bloco 1, ajustado sobre as 113 linhas, sem padronizar."""
    n = len(base["periodo"])
    X = _matriz(base, FEATURES, slice(0, n))
    modelo = linear_model.LinearRegression().fit(X, base[ALVO])
    soma = modelo.coef_[0] + modelo.coef_[1]

    assert 0.97 < soma < 1.02, soma
    assert modelo.coef_[0] > modelo.coef_[1], "lag1 pesa mais que lag4"


def test_vazamento_do_escalador_nao_muda_a_metrica_neste_modelo(base):
    """Mede por que a disciplina de fit-so-no-treino se justifica por principio.

    Ajustar o escalador sobre treino e teste juntos desloca a media dele em mais
    de 10% de um desvio, e ainda assim o MAPE sai identico. Regressao linear sem
    regularizacao e invariante a transformacao afim das entradas: os
    coeficientes absorvem a mudanca de escala.

    O teste existe para travar a honestidade do material de apoio, que precisa
    dizer que aqui o efeito e nulo, e que a disciplina vale porque KNN, SVM,
    regressao regularizada e PCA nao tem essa invariancia.
    """
    n = len(base["periodo"])
    n_treino = n - N_TESTE
    teste = slice(n_treino, n)

    X_tr = _matriz(base, FEATURES, slice(0, n_treino))
    X_te = _matriz(base, FEATURES, teste)
    y_tr, y_te = base[ALVO][slice(0, n_treino)], base[ALVO][teste]

    so_treino = preprocessing.StandardScaler().fit(X_tr)
    com_teste = preprocessing.StandardScaler().fit(np.vstack([X_tr, X_te]))

    # o escalador de fato muda: a media anda mais de 10% de um desvio
    deslocamento = np.abs(com_teste.mean_ - so_treino.mean_) / so_treino.scale_
    assert deslocamento[:2].min() > 0.10, deslocamento

    correto = linear_model.LinearRegression().fit(so_treino.transform(X_tr), y_tr)
    vazado = linear_model.LinearRegression().fit(com_teste.transform(X_tr), y_tr)

    mape_correto = _mape(y_te, correto.predict(so_treino.transform(X_te)))
    mape_vazado = _mape(y_te, vazado.predict(com_teste.transform(X_te)))

    assert mape_correto == pytest.approx(mape_vazado, abs=1e-9), (
        "se este teste falhar, o modelo deixou de ser invariante a escala e o "
        "material de apoio precisa ser reescrito")


def _recursivo(base, modelo, escalador, n_treino, passos=N_TESTE):
    """Realimenta a propria previsao, como o horizonte de 24 meses exige."""
    historico = list(base[ALVO][:n_treino])
    saida = []
    for k in range(passos):
        tri = int(base["periodo"][n_treino + k][-1])
        x = np.array([[historico[-1], historico[-4],
                       np.sin(2 * np.pi * tri / 4), np.cos(2 * np.pi * tri / 4)]])
        y = float(modelo.predict(escalador.transform(x))[0])
        saida.append(y)
        historico.append(y)
    return np.array(saida)


def test_horizonte_de_verdade_erra_mais_que_um_passo(base):
    """A aula afirma 1,60% para um passo e 2,85% para o voo de oito trimestres."""
    n = len(base["periodo"])
    n_treino = n - N_TESTE
    teste = slice(n_treino, n)
    y_teste = base[ALVO][teste]

    modelo, _, _ = _ajustar(base, FEATURES, n_treino, teste)
    escalador = preprocessing.StandardScaler().fit(
        _matriz(base, FEATURES, slice(0, n_treino)))
    _, um_passo, _ = _ajustar(base, FEATURES, n_treino, teste)
    recursivo = _recursivo(base, modelo, escalador, n_treino)

    mape_um = _mape(y_teste, um_passo)
    mape_rec = _mape(y_teste, recursivo)

    assert mape_rec > mape_um, (
        "se o recursivo deixar de errar mais, o slide do horizonte perde o sentido")
    assert 1.4 < mape_um < 1.8, mape_um
    assert 2.5 < mape_rec < 3.2, mape_rec


def test_o_erro_recursivo_cresce_com_o_horizonte(base):
    """O SVG do horizonte mostra o erro indo de -1,02% a -6,95%."""
    n = len(base["periodo"])
    n_treino = n - N_TESTE
    modelo, _, _ = _ajustar(base, FEATURES, n_treino, slice(n_treino, n))
    escalador = preprocessing.StandardScaler().fit(
        _matriz(base, FEATURES, slice(0, n_treino)))
    previsto = _recursivo(base, modelo, escalador, n_treino)
    real = base[ALVO][slice(n_treino, n)]
    erro = (previsto - real) / real * 100

    assert abs(erro[-1]) > abs(erro[0]), "o erro do fim precisa superar o do comeco"
    assert erro[-1] < -5, erro[-1]
    assert -2 < erro[0] < 0, erro[0]
    # o modelo subestima quase sempre, que e o vies discutido no slide
    assert (erro < 0).sum() >= 7, erro


def test_banda_fixa_em_kg_muda_de_significado_ao_longo_da_serie(base):
    """A resposta a duvida da turma: largura constante, incerteza relativa que varia."""
    n = len(base["periodo"])
    n_treino = n - N_TESTE
    _, _, previsto_treino = _ajustar(base, FEATURES, n_treino, slice(n_treino, n))
    residuos = base[ALVO][slice(0, n_treino)] - previsto_treino
    meia = 1.96 * residuos.std(ddof=len(FEATURES) + 1)

    inicio = meia / base[ALVO][0] * 100
    fim = meia / base[ALVO][-1] * 100

    assert inicio > 4 * fim, (
        "a mesma banda precisa valer muito mais no comeco, senao o slide nao se sustenta")
    assert 15 < inicio < 19, inicio
    assert 3 < fim < 5, fim

    # e o residuo encolhe em proporcao, mesmo crescendo em quilos
    meio = n_treino // 2
    r1, r2 = residuos[:meio], residuos[meio:]
    n1 = base[ALVO][slice(0, meio)].mean()
    n2 = base[ALVO][slice(meio, n_treino)].mean()
    assert r2.std() > r1.std(), "em quilos o residuo cresce"
    assert r2.std() / n2 < r1.std() / n1, "em proporcao ele encolhe"

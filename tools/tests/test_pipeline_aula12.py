"""Trava as conclusões que a Aula 12 afirma sobre `Pipeline`, export e MLflow.

A aula tem três blocos de conteúdo, e cada um afirma algo medido sobre a base
mensal de `dados/mensal/`, a mesma das Aulas 07 a 11:

  1  o `Pipeline` não muda número nenhum. Encapsular `StandardScaler` e
     `LinearRegression` num `Pipeline` devolve previsão **idêntica bit a bit**
     ao passo a passo da Aula 11, e o mesmo MAPE de 2,8620% nos 24 meses de
     teste. O que o `Pipeline` acrescenta não é precisão: é impedir que a ordem
     seja executada errada, o que importa quando ele entra num validador que
     reparte o dado, como o `TimeSeriesSplit` da Aula 10.
  2  o reajuste sobre a base completa move muito o coeficiente e quase nada a
     previsão. Passar de 315 para 339 meses desloca os coeficientes numa
     mediana de 17,2%, e `abate_bovinos_lag1` **troca de sinal**. A previsão
     nos mesmos 24 meses se move 0,65% em média e no máximo 0,98%.
     A causa está medida no teste de colinearidade: vinte pares de features
     acima de r = 0,90 e VIF de até 69. Features colineares deixam o modelo
     redistribuir peso entre elas sem mexer no ajuste.
     A consequência é o gancho com a Aula 10: o que se entrega em produção é a
     previsão, e ela é estável; uma explicação baseada no coeficiente não é.
  3  a divergência de versão avisa e não impede. Um `Pipeline` gravado com
     scikit-learn 1.7.2 e carregado com 1.9.1 emite três
     `InconsistentVersionWarning`, um por estimador, e devolve previsão
     idêntica bit a bit. O que falha é o caminho inverso: no Python 3.14 não
     existe wheel de scikit-learn anterior à 1.7.2, então recriar o ambiente
     antigo não é uma opção disponível.

Como em `test_modelo_aula05.py`, `test_clusters_aula06.py`,
`test_modelos_aula07.py`, `test_pca_aula08.py`, `test_problemas_aula09.py`,
`test_ajuste_aula10.py` e `test_automl_aula11.py`, o que se trava aqui são as
conclusões, não só os números.

O teste do arquivo versionado (`app/modelo_aula12.joblib`) compara coeficientes
e previsões, e **nunca o hash do arquivo**: o pickle grava metadado de ambiente
e o mesmo modelo produz bytes diferentes em máquinas diferentes. O que precisa
ser reproduzível é o modelo, não o binário.

Precisa de numpy, pandas, scikit-learn e joblib, do requirements-ci.txt. Sem
eles o arquivo inteiro se pula, e o CI continua cobrindo o resto.

O `.joblib` gravado com a 1.7.2 **é versionado** (`app/modelo_aula12_sk172.joblib`),
justamente para o CI cobrir a afirmação de divergência de versão: gerá-lo na hora
exigiria um segundo interpretador. O teste se pula sozinho se o arquivo sumir, e o
procedimento para regerá-lo está em `docs/adrs/ADR-015`.

Três versões propositalmente quebradas foram executadas contra esta suíte, e
cada uma reprovou o teste indicado:

  exportar o Pipeline ajustado só nos 315 meses de treino, em vez da base inteira
    -> `test_o_modelo_exportado_e_o_reajustado_sobre_a_base_completa` (é o erro
       que deixa dado disponível parado fora do modelo de produção, e ele é
       silencioso: as previsões continuam boas).
  medir o modelo reajustado nos 24 meses de teste e publicar esse MAPE
    -> `test_o_mape_do_modelo_reajustado_nao_e_estimativa_honesta` (dá 2,65%,
       melhor que o 2,86% honesto, porque o modelo treinou com esses meses).
  ajustar o StandardScaler fora do Pipeline, sobre treino e teste juntos
    -> nenhum teste reprovou, e isso está registrado de propósito. A Aula 05 já
       tinha medido que essa mutação é inofensiva para regressão linear sem
       regularização, que é invariante a transformação afim das entradas. O
       `Pipeline` continua sendo a resposta certa, e o motivo é o da Aula 10
       (dentro de um `TimeSeriesSplit` o escalador precisa ser reajustado por
       dobra), não um ganho de MAPE nesta base. O material declara isso em vez
       de fingir um ganho que a medição não mostra.
"""
import calendar
import os
import warnings

import pytest

np = pytest.importorskip("numpy")
pytest.importorskip("sklearn")
pytest.importorskip("pandas")
joblib = pytest.importorskip("joblib")

import pandas as pd  # noqa: E402
from sklearn.linear_model import LinearRegression  # noqa: E402
from sklearn.pipeline import Pipeline  # noqa: E402
from sklearn.preprocessing import StandardScaler  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MENSAL = os.path.join(RAIZ, "dados", "mensal")
MODELO_VERSIONADO = os.path.join(RAIZ, "app", "modelo_aula12.joblib")

# gravado por um interpretador com scikit-learn 1.7.2, para o teste de
# divergencia de versao. Nao e versionado: ver o cabecalho e a ADR-015.
MODELO_1_7_2 = os.path.join(RAIZ, "app", "modelo_aula12_sk172.joblib")

SERIES = ["abate_bovinos", "abate_suinos", "abate_frangos",
          "producao_ovos", "producao_leite"]
ALVO = "abate_frangos"
FEATURES = (["lag1", "lag2", "lag3", "lag12", "sen", "cos", "dias"]
            + [s + "_lag1" for s in SERIES if s != ALVO])
N_TESTE = 24


def _base():
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


@pytest.fixture(scope="module")
def dados():
    base = _base()
    corte = len(base) - N_TESTE
    return {
        "base": base,
        "X_tr": base[FEATURES].to_numpy()[:corte],
        "y_tr": base[ALVO].to_numpy()[:corte],
        "X_te": base[FEATURES].to_numpy()[corte:],
        "y_te": base[ALVO].to_numpy()[corte:],
        "X_full": base[FEATURES].to_numpy(),
        "y_full": base[ALVO].to_numpy(),
    }


# --- bloco 1: o Pipeline nao muda numero nenhum ------------------------------

def test_a_base_e_a_mesma_das_aulas_07_a_11(dados):
    """339 linhas, 315 de treino, 24 de teste, onze features."""
    base = dados["base"]
    assert len(base) == 339
    assert len(FEATURES) == 11
    assert base["periodo"].iloc[0] == "1998-01"
    assert base["periodo"].iloc[-1] == "2026-03"
    assert base["periodo"].iloc[len(base) - N_TESTE] == "2024-04"


def test_o_pipeline_devolve_previsao_identica_ao_passo_a_passo(dados):
    """O Pipeline não melhora nem piora nada: ele reordena o mesmo cálculo.

    É a afirmação do primeiro bloco da aula. Se um dia esta igualdade deixar de
    ser exata, o slide que diz "idêntica bit a bit" precisa mudar junto.
    """
    escalador = StandardScaler().fit(dados["X_tr"])
    modelo = LinearRegression().fit(escalador.transform(dados["X_tr"]), dados["y_tr"])
    passo_a_passo = modelo.predict(escalador.transform(dados["X_te"]))

    pipe = Pipeline([("escala", StandardScaler()), ("modelo", LinearRegression())])
    pipe.fit(dados["X_tr"], dados["y_tr"])
    pelo_pipeline = pipe.predict(dados["X_te"])

    assert np.array_equal(passo_a_passo, pelo_pipeline)


def test_mandar_o_modelo_sem_o_escalador_erra_por_oito_ordens_de_grandeza(dados):
    """A previsão sai 231 milhões de vezes maior que o valor medido pelo IBGE.

    É a pergunta disparada do slide 4, e o número dela. O modelo foi ajustado
    sobre entradas padronizadas, e passar a base em unidades originais, na casa
    de 1e9, devolve 2,63e17 quilogramas de frango abatido num mês em que o IBGE
    mediu 1,19e9.

    O teste trava a ordem de grandeza, e não o dígito: o que a aula afirma é
    que o erro é absurdo e silencioso, e não que ele valha exatamente 231
    milhões de vezes.
    """
    escalador = StandardScaler().fit(dados["X_tr"])
    modelo = LinearRegression().fit(escalador.transform(dados["X_tr"]), dados["y_tr"])

    sem_escalador = modelo.predict(dados["X_te"])
    razao = float(np.mean(sem_escalador / dados["y_te"]))

    assert razao > 1e7
    assert _mape(dados["y_te"], sem_escalador) > 1e9
    assert np.log10(abs(razao)) == pytest.approx(8.4, abs=1.0)


def test_o_modelo_avaliado_erra_2_86_por_cento(dados):
    """O número que descreve o modelo, e o único honesto de publicar.

    É o mesmo 2,86% do quadro de referência da Aula 11 (`ADR-014`), medido no
    objeto que NÃO viu os 24 meses de teste.
    """
    pipe = Pipeline([("escala", StandardScaler()), ("modelo", LinearRegression())])
    pipe.fit(dados["X_tr"], dados["y_tr"])
    assert _mape(dados["y_te"], pipe.predict(dados["X_te"])) == pytest.approx(2.862, abs=0.01)


# --- bloco 2: o reajuste sobre a base completa -------------------------------

def _coeficientes(X, y):
    pipe = Pipeline([("escala", StandardScaler()), ("modelo", LinearRegression())])
    pipe.fit(X, y)
    return pipe, pipe.named_steps["modelo"].coef_


def test_o_reajuste_desloca_os_coeficientes(dados):
    """Mediana de 17,2% de deslocamento ao acrescentar 24 meses.

    Trava a ordem de grandeza, não o dígito: o que a aula afirma é que o
    deslocamento é grande, de dezenas de pontos percentuais, e não que ele vale
    exatamente 17,2%.
    """
    _, coef_tr = _coeficientes(dados["X_tr"], dados["y_tr"])
    _, coef_full = _coeficientes(dados["X_full"], dados["y_full"])

    relativo = np.abs((coef_full - coef_tr) / coef_tr) * 100
    assert float(np.median(relativo)) == pytest.approx(17.2, abs=3.0)
    assert float(np.median(relativo)) > 5.0


def test_um_coeficiente_troca_de_sinal_no_reajuste(dados):
    """`abate_bovinos_lag1` sai de negativo para positivo.

    É o slide mais forte da aula, e o que amarra a Aula 10: a mesma feature que
    o SHAP explicaria muda de direção quando chegam 24 meses novos, sem que a
    previsão se mexa.
    """
    _, coef_tr = _coeficientes(dados["X_tr"], dados["y_tr"])
    _, coef_full = _coeficientes(dados["X_full"], dados["y_full"])

    i = FEATURES.index("abate_bovinos_lag1")
    assert coef_tr[i] < 0 < coef_full[i]
    assert int(np.sum(np.sign(coef_tr) != np.sign(coef_full))) >= 1


def test_a_previsao_quase_nao_se_move_no_reajuste(dados):
    """Menos de 1% de diferença, contra os 17,2% dos coeficientes.

    O contraste entre este teste e os dois anteriores é o conteúdo do bloco.
    """
    pipe_tr, _ = _coeficientes(dados["X_tr"], dados["y_tr"])
    pipe_full, _ = _coeficientes(dados["X_full"], dados["y_full"])

    a = pipe_tr.predict(dados["X_te"])
    b = pipe_full.predict(dados["X_te"])
    relativo = np.abs((b - a) / a) * 100

    assert float(np.max(relativo)) < 1.0
    assert float(np.mean(relativo)) == pytest.approx(0.65, abs=0.2)


def test_a_colinearidade_explica_a_instabilidade(dados):
    """Vinte pares acima de r = 0,90 e VIF de até 69.

    Sem este teste, a aula afirmaria a causa sem tê-la medido. O VIF acima de
    10 é o limiar usual para declarar colinearidade preocupante, e sete das
    onze features passam dele.
    """
    Z = StandardScaler().fit_transform(dados["X_tr"])
    C = np.corrcoef(Z, rowvar=False)

    pares = sum(1 for i in range(len(FEATURES)) for j in range(i + 1, len(FEATURES))
                if abs(C[i, j]) > 0.90)
    assert pares >= 18

    vif = np.diag(np.linalg.inv(C))
    assert float(np.max(vif)) > 50.0
    assert int(np.sum(vif > 10.0)) >= 7


def test_padronizar_conserta_o_condicionamento_e_nao_a_colinearidade(dados):
    """3,2e9 para 28,5 no número de condição, e o VIF continua em 69.

    A distinção que impede a aula de repetir a Aula 05 errado: padronizar
    resolveu o problema numérico daquela aula, e não resolve este. São dois
    problemas diferentes com a mesma aparência.
    """
    cru = float(np.linalg.cond(dados["X_tr"]))
    padronizado = float(np.linalg.cond(StandardScaler().fit_transform(dados["X_tr"])))

    assert cru > 1e8
    assert padronizado < 100.0

    C = np.corrcoef(StandardScaler().fit_transform(dados["X_tr"]), rowvar=False)
    assert float(np.max(np.diag(np.linalg.inv(C)))) > 50.0


def test_o_mape_do_modelo_reajustado_nao_e_estimativa_honesta(dados):
    """2,65% contra 2,86%, e o menor dos dois é o que não vale.

    O modelo reajustado treinou com os 24 meses de teste. Medi-lo ali devolve
    um número melhor e sem significado, e publicá-lo seria exatamente o
    vazamento que a Aula 09 ensinou a reconhecer.
    """
    pipe_tr, _ = _coeficientes(dados["X_tr"], dados["y_tr"])
    pipe_full, _ = _coeficientes(dados["X_full"], dados["y_full"])

    honesto = _mape(dados["y_te"], pipe_tr.predict(dados["X_te"]))
    contaminado = _mape(dados["y_te"], pipe_full.predict(dados["X_te"]))

    assert honesto == pytest.approx(2.862, abs=0.01)
    assert contaminado == pytest.approx(2.649, abs=0.01)
    assert contaminado < honesto


# --- bloco 3: export e divergencia de versao ---------------------------------

def test_o_round_trip_do_joblib_preserva_a_previsao(dados, tmp_path):
    """Gravar e recarregar devolve previsão idêntica bit a bit."""
    pipe, _ = _coeficientes(dados["X_full"], dados["y_full"])
    destino = tmp_path / "pipe.joblib"
    joblib.dump(pipe, destino)

    assert np.array_equal(pipe.predict(dados["X_te"]),
                          joblib.load(destino).predict(dados["X_te"]))


def test_o_modelo_versionado_existe_e_e_pequeno():
    """`app/modelo_aula12.joblib` é commitado, e cabe no repositório.

    A Aula 13 carrega este arquivo. Ele tem cerca de 1,5 KB: onze coeficientes,
    onze médias e onze desvios. Se um dia passar de 100 KB, a decisão de
    versionar binário precisa ser reaberta (`docs/adrs/ADR-015`).
    """
    assert os.path.exists(MODELO_VERSIONADO), (
        "rode python3 tools/exportar_modelo_aula12.py")
    assert os.path.getsize(MODELO_VERSIONADO) < 100 * 1024


def test_o_modelo_exportado_e_o_reajustado_sobre_a_base_completa(dados):
    """O arquivo versionado tem os coeficientes da base inteira, não os do treino.

    É o teste que pega a mutação mais silenciosa desta aula: exportar o objeto
    avaliado em vez do reajustado continua produzindo previsões boas, e só a
    comparação de coeficiente denuncia.
    """
    versionado = joblib.load(MODELO_VERSIONADO)
    _, coef_tr = _coeficientes(dados["X_tr"], dados["y_tr"])
    _, coef_full = _coeficientes(dados["X_full"], dados["y_full"])

    coef_arquivo = versionado.named_steps["modelo"].coef_
    assert np.allclose(coef_arquivo, coef_full, rtol=1e-9)
    assert not np.allclose(coef_arquivo, coef_tr, rtol=1e-3)


def test_o_modelo_versionado_preve_os_24_meses(dados):
    """O arquivo commitado carrega e prevê, que é o contrato com a Aula 13."""
    versionado = joblib.load(MODELO_VERSIONADO)
    previsto = versionado.predict(dados["X_te"])

    assert previsto.shape == (N_TESTE,)
    assert np.all(previsto > 0)
    assert _mape(dados["y_te"], previsto) < 5.0


@pytest.mark.skipif(not os.path.exists(MODELO_1_7_2),
                    reason="o .joblib de referencia da 1.7.2 nao esta presente; ver ADR-015")
def test_a_divergencia_de_versao_avisa_e_nao_impede(dados):
    """Três `InconsistentVersionWarning`, e previsão idêntica bit a bit.

    A aula afirma que o aviso é a única coisa que denuncia a divergência, e que
    ele não interrompe nada. Este teste é o que sustenta a afirmação.
    """
    with warnings.catch_warnings(record=True) as capturados:
        warnings.simplefilter("always")
        antigo = joblib.load(MODELO_1_7_2)

    avisos = [a for a in capturados
              if a.category.__name__ == "InconsistentVersionWarning"]
    assert len(avisos) == 3
    assert "1.7.2" in str(avisos[0].message)

    # Compara com o binario versionado, e nao com um reajuste feito agora: o
    # reajuste depende do BLAS da maquina (o CI em Ubuntu diverge do macOS no
    # ultimo bit), enquanto os dois arquivos guardam os mesmos parametros e
    # preveem na mesma maquina. E isso que a aula afirma sobre a divergencia.
    atual = joblib.load(MODELO_VERSIONADO)
    assert np.array_equal(antigo.predict(dados["X_te"]), atual.predict(dados["X_te"]))

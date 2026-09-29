"""Trava cada número que o deck, o material e o notebook da Aula 14 afirmam.

A aula dá uma tela ao `Pipeline` exportado na Aula 12 e afirma quatro coisas
medidas, todas calculadas por `app/logica.py`, que é o mesmo código que o app
Streamlit e o notebook usam:

  1  o número de desempenho que acompanha o app é 2,86%, medido no objeto
     avaliado (315 meses). O exportado, medido nos mesmos 24 meses, dá 2,65%,
     e esse não aparece na tela.
  2  cenário sobre o grupo de defasagens do frango é estável entre os dois
     ajustes: +10% no patamar move a previsão em +9,62% no exportado e +9,63%
     no avaliado.
  3  cenário numa entrada isolada herda a instabilidade do coeficiente: +10% só
     no abate de bovinos do mês anterior dá +0,151% no exportado e -0,005% no
     avaliado, com sinal trocado; só no lag1, +0,24% contra +0,45%.
  4  o modelo não tem preço de milho: um cenário sobre entrada fora das onze
     features é recusado, e não silenciosamente ignorado.

Mais o contrato da tela: a previsão para 2026-04 (1,227 bilhão de kg), a
série escolhida que não é frango aparecendo sem previsão, e o aviso de sinal
trocado. A parte de tela usa `streamlit.testing.v1.AppTest` e se pula sozinha
sem Streamlit.

Versões propositalmente quebradas executadas contra esta suíte, e o teste que
reprovou cada uma:

  `mape_do_avaliado` medindo o pipeline exportado em vez do avaliado
    -> `test_o_app_publica_o_mape_do_avaliado` (devolve 2,65%).
  `aplicar_choque` ignorando em silêncio coluna fora de FEATURES
    -> `test_cenario_em_entrada_fora_do_modelo_e_recusado`.
  `aplicar_choque` alterando a matriz recebida no lugar
    -> `test_o_choque_nao_altera_a_matriz_original`.

O aviso de sinal trocado na tela não depende de marcação manual do cenário:
ele vem de `estabilidade_do_cenario`, que mede os dois ajustes a cada choque.
"""
import os
import sys

import pytest

np = pytest.importorskip("numpy")
pytest.importorskip("pandas")
pytest.importorskip("sklearn")
pytest.importorskip("joblib")

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(RAIZ, "app"))
sys.path.insert(0, os.path.join(RAIZ, "tools"))

import logica  # noqa: E402


@pytest.fixture(scope="module")
def base():
    return logica.base_analitica()


@pytest.fixture(scope="module")
def pipe():
    return logica.carregar_pipeline()


# --- a base e o modelo são os da Aula 12 --------------------------------------

def test_a_base_do_app_e_a_mesma_do_export_da_aula12(base):
    """`app/` reimplementa a base para não depender de `tools/`; as duas batem."""
    from exportar_modelo_aula12 import base_analitica as base_da_aula12

    referencia = base_da_aula12()
    assert len(base) == 339
    assert list(base["periodo"]) == list(referencia["periodo"])
    assert np.array_equal(base[logica.FEATURES].to_numpy(),
                          referencia[logica.FEATURES].to_numpy())


def test_o_teste_vai_de_2024_04_a_2026_03(pipe, base):
    teste = logica.prever_teste(pipe, base)
    assert len(teste) == 24
    assert teste["periodo"].iloc[0] == "2024-04"
    assert teste["periodo"].iloc[-1] == "2026-03"


# --- 1: o número que acompanha o app ------------------------------------------

def test_o_app_publica_o_mape_do_avaliado(base):
    assert logica.mape_do_avaliado(base) == pytest.approx(2.862, abs=0.005)


def test_o_exportado_nos_24_meses_da_2_65_e_esse_nao_e_o_publicado(pipe, base):
    teste = logica.prever_teste(pipe, base)
    contaminado = logica.mape(teste["real"], teste["previsto"])
    assert contaminado == pytest.approx(2.649, abs=0.005)
    assert contaminado < logica.mape_do_avaliado(base)


# --- 2 e 3: cenários ------------------------------------------------------------

def test_patamar_do_frango_e_estavel_entre_os_ajustes(pipe, base):
    estab = logica.estabilidade_do_cenario(pipe, base, "patamar_frango", 10)
    assert estab["exportado"] == pytest.approx(9.62, abs=0.01)
    assert estab["avaliado"] == pytest.approx(9.63, abs=0.01)
    assert estab["mesmo_sinal"]
    assert estab["diferenca_pp"] < 0.05


def test_outras_quatro_series_mantem_o_sinal(pipe, base):
    estab = logica.estabilidade_do_cenario(pipe, base, "outras_proteinas", 10)
    assert estab["exportado"] == pytest.approx(0.39, abs=0.01)
    assert estab["avaliado"] == pytest.approx(0.35, abs=0.01)
    assert estab["mesmo_sinal"]


def test_so_bovinos_troca_de_sinal_entre_os_ajustes(pipe, base):
    """O coeficiente que a Aula 12 viu trocar de sinal, lido como cenário."""
    estab = logica.estabilidade_do_cenario(pipe, base, "so_bovinos", 10)
    assert estab["exportado"] == pytest.approx(0.151, abs=0.002)
    assert estab["avaliado"] == pytest.approx(-0.005, abs=0.002)
    assert estab["exportado"] > 0 > estab["avaliado"]
    assert not estab["mesmo_sinal"]


def test_so_lag1_quase_dobra_entre_os_ajustes(pipe, base):
    estab = logica.estabilidade_do_cenario(pipe, base, ["lag1"], 10)
    assert estab["exportado"] == pytest.approx(0.24, abs=0.01)
    assert estab["avaliado"] == pytest.approx(0.45, abs=0.01)
    assert estab["avaliado"] / estab["exportado"] > 1.8


def test_a_soma_dos_coeficientes_das_defasagens_quase_nao_muda(pipe, base):
    """0,976 no exportado e 0,970 no avaliado: é o que torna o grupo estável.

    A partilha entre as quatro defasagens muda a cada reajuste (VIF de até 69,
    na Aula 12); a soma, que é o que um choque no grupo inteiro lê, não.
    """
    colunas = logica.CENARIOS["patamar_frango"]["colunas"]

    def soma(p):
        coef = p.named_steps["modelo"].coef_ / p.named_steps["escala"].scale_
        return float(sum(coef[logica.FEATURES.index(c)] for c in colunas))

    assert soma(pipe) == pytest.approx(0.976, abs=0.001)
    assert soma(logica.pipeline_avaliado(base)) == pytest.approx(0.970, abs=0.001)


def test_o_maior_erro_do_exportado_no_grafico_e_2025_05(pipe, base):
    teste = logica.prever_teste(pipe, base)
    pior = teste.loc[teste["erro_pct"].abs().idxmax()]
    assert pior["periodo"] == "2025-05"
    assert pior["erro_pct"] == pytest.approx(-6.51, abs=0.01)


def test_o_efeito_e_linear_no_choque(pipe, base):
    """Modelo linear: -10% é o espelho de +10%, e 20% é o dobro de 10%."""
    mais = logica.efeito_medio(pipe, base, "patamar_frango", 10)
    menos = logica.efeito_medio(pipe, base, "patamar_frango", -10)
    dobro = logica.efeito_medio(pipe, base, "patamar_frango", 20)
    assert menos == pytest.approx(-mais, rel=1e-9)
    assert dobro == pytest.approx(2 * mais, rel=1e-9)
    assert dobro == pytest.approx(19.249, abs=0.001)


def test_choque_zero_devolve_a_previsao_de_referencia(pipe, base):
    resultado = logica.prever_cenario(pipe, base, "patamar_frango", 0)
    assert np.array_equal(resultado["referencia"].to_numpy(), resultado["cenario"].to_numpy())


def test_o_choque_nao_altera_a_matriz_original(base):
    X = base[logica.FEATURES].to_numpy()
    copia = X.copy()
    logica.aplicar_choque(X, ["lag1"], 10)
    assert np.array_equal(X, copia)


# --- 4: o que o modelo não lê -------------------------------------------------

def test_cenario_em_entrada_fora_do_modelo_e_recusado(base):
    X = base[logica.FEATURES].to_numpy()
    with pytest.raises(ValueError, match="fora do modelo"):
        logica.aplicar_choque(X, ["preco_milho"], 10)


def test_milho_esta_declarado_fora_do_modelo():
    assert "Preço do milho" in logica.ENTRADAS_FORA_DO_MODELO
    assert not any("milho" in f for f in logica.FEATURES)
    for grupo in logica.CENARIOS.values():
        assert set(grupo["colunas"]) <= set(logica.FEATURES)


# --- a previsão do próximo mês ------------------------------------------------

def test_o_proximo_mes_usa_so_dado_medido(pipe):
    periodo, X = logica.features_do_proximo_mes()
    assert periodo == "2026-04"
    linha = dict(zip(logica.FEATURES, X[0]))
    assert linha["lag1"] == 1301022625.0          # 2026-03 em dados/mensal/abate_frangos.csv
    assert linha["dias"] == 30
    assert linha["abate_bovinos_lag1"] == 920748988.0

    periodo, valor = logica.prever_proximo_mes(pipe)
    assert valor == pytest.approx(1.2271e9, rel=1e-3)


def test_proximo_periodo_vira_o_ano():
    assert logica.proximo_periodo("2026-12") == "2027-01"
    assert logica.proximo_periodo("2026-03") == "2026-04"


# --- o que o gráfico recebe ---------------------------------------------------

def test_o_grafico_so_tem_previsao_nos_24_meses_de_teste(pipe, base):
    tabela = logica.tabela_do_grafico(pipe, base, 48, "patamar_frango", 0)
    assert set(tabela["curva"]) == {"Medido pelo IBGE", "Previsão do modelo"}
    assert (tabela["curva"] == "Previsão do modelo").sum() == 24
    assert (tabela["curva"] == "Medido pelo IBGE").sum() == 48

    com_choque = logica.tabela_do_grafico(pipe, base, 48, "patamar_frango", -10)
    assert (com_choque["curva"] == "Previsão sob o cenário").sum() == 24


def test_historico_de_outra_serie_fica_na_unidade_certa():
    series = logica.carregar_series()
    tabela, titulo = logica.tabela_do_historico(series["producao_leite"], 24)
    assert titulo == "mil litros por mês"
    assert tabela["valor"].iloc[-1] == 2244753.0
    tabela, titulo = logica.tabela_do_historico(series["abate_bovinos"], 24)
    assert titulo == "milhões de kg por mês"


def test_numero_br():
    assert logica.numero_br(2.8620136) == "2,86"
    assert logica.numero_br(1227063555.7, 0) == "1.227.063.556"
    assert logica.numero_br(-0.00535, 3, sinal=True) == "-0,005"


# --- a tela, com AppTest ------------------------------------------------------

@pytest.fixture(scope="module")
def app_test():
    testing = pytest.importorskip("streamlit.testing.v1")
    return testing.AppTest


def _abrir(app_test):
    at = app_test.from_file(os.path.join(RAIZ, "app", "app.py"), default_timeout=120)
    return at.run()


def test_a_tela_abre_sem_erro_e_mostra_os_tres_numeros(app_test):
    at = _abrir(app_test)
    assert not at.exception
    valores = {m.label: m.value for m in at.metric}
    assert valores["MAPE nos 24 meses de teste"] == "2,86%"
    assert valores["Meses de treino do modelo exportado"] == "339"
    assert valores["Previsão para 2026-04"] == "1,227 bi kg"


def test_a_tela_avisa_quando_o_cenario_troca_de_sinal(app_test):
    at = _abrir(app_test)
    at.sidebar.selectbox[1].set_value("so_bovinos")
    at.sidebar.slider[1].set_value(10)
    at.run()
    assert not at.exception
    assert len(at.warning) == 1
    assert "sinal oposto" in at.warning[0].value

    at.sidebar.selectbox[1].set_value("patamar_frango")
    at.run()
    assert len(at.warning) == 0
    assert any("+9,624%" in m.value for m in at.markdown)


def test_outra_serie_aparece_sem_previsao(app_test):
    at = _abrir(app_test)
    at.sidebar.selectbox[0].set_value("producao_ovos")
    at.run()
    assert not at.exception
    assert len(at.metric) == 0
    assert "sem previsão" in at.info[0].value

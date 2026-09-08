"""Trava as conclusões que a Aula 08 afirma sobre escolha de K e sobre PCA.

A aula tem uma tese única, medida nos dois blocos: o critério interno da
técnica não supervisionada (inércia, silhueta, variância explicada) não é o
critério do case (recuperar o calendário, prever com erro menor).

Bloco de escolha de K, sobre as duas bases trimestrais da Aula 06:

  1  na base de participação no ano, o Elbow aponta K=3 e a silhueta aponta
     K=2, e o K útil é 4 (98,3% de concordância com o trimestre);
  2  na base de níveis, a silhueta é máxima em K=2 e cai até K=8, enquanto a
     concordância com o calendário fica no acaso em todo K testado.

Bloco de PCA, sobre as 11 features da base mensal da Aula 07:

  3  PC1 concentra 68,21% da variância e é o nível comum das cinco séries;
  4  PC2 e PC3 carregam o calendário, e o plano deles recupera o mês em mais
     de 90% dos meses de treino, sem nunca receber o mês como coluna;
  5  cortar componentes piora a previsão e faz o modelo perder da baseline da
     LDC: com k <= 9 o MAPE fica acima de 3,71%, e só k=10 recupera os 3,32%
     das 11 features;
  6  o motivo do item 5 está nos coeficientes: PC9 e PC10, com 0,21% e 0,17%
     da variância, recebem coeficiente 22 e 27 vezes o do PC1;
  7  PCA completo é rotação, então k=11 devolve o MAPE das 11 features até a
     nona casa decimal, o que confirma a invariância medida na Aula 05: o que
     muda o resultado é o corte, não a rotação;
  8  sem padronizar, PC1 explica 96,72% e seus maiores pesos são as colunas em
     quilos, porque o desvio delas está em 1e8 contra 0,7 de `sen` e `cos`;
  9  a direção do efeito do corte depende do modelo: com quatro componentes o
     KNN de cinco vizinhos melhora (5,01% para 4,78%) enquanto a regressão
     linear piora (3,32% para 4,94%), e nenhum dos dois desce abaixo dos 3,71%
     da baseline da LDC. É o escopo de conclusão que a seção 13 de
     `materiais/aula08.html` e a `ADR-011` publicam.

Como em `test_modelo_aula05.py`, `test_clusters_aula06.py` e
`test_modelos_aula07.py`, o que se trava aqui são as conclusões, não só os
números: se um CSV for regerado com dado novo do SIDRA e uma conclusão virar, o
deck, o material, o notebook e as notas do professor passam a ensinar algo que
o dado não sustenta.

O ajuste do escalador e do PCA acontece **só no treino**, os 315 primeiros
meses, e não na base inteira. Não é detalhe de estilo: é a disciplina que a
Aula 05 estabeleceu e que a Aula 09 vai cobrar como vazamento temporal.

Precisa de numpy e scikit-learn, do requirements-ci.txt. Sem eles o arquivo
inteiro se pula, e o CI continua cobrindo o resto.

Quatro versões propositalmente quebradas foram executadas contra esta suíte, e
cada uma reprovou os testes indicados:

  ajustar escalador e PCA na base inteira, e não só no treino
    -> `test_pc1_e_o_nivel_comum_das_cinco_series` (PC1 vai de 68,21% para
       68,52%) e `test_cortar_componentes_faz_o_modelo_perder_da_baseline`
       (k=4 vai de 4,94% para 4,91%). As duas reprovam por margem estreita,
       porque o vazamento por escalador é pequeno neste modelo, como a Aula 05
       já havia medido. Quem afrouxar essas faixas perde a única barreira que
       existe aqui contra ajuste fora do treino.
  usar a base de níveis onde a aula usa a participação no ano
    -> os três testes do bloco de escolha de K.
  padronizar dentro do bloco que afirma o contrário
    -> `test_sem_padronizar_o_pc1_e_so_a_coluna_de_maior_desvio`.
  ignorar o k pedido e usar sempre os 11 componentes
    -> `test_cortar_componentes_faz_o_modelo_perder_da_baseline`.
"""
import calendar
import collections
import csv
import os

import pytest

np = pytest.importorskip("numpy")
pytest.importorskip("sklearn")

from sklearn.cluster import KMeans  # noqa: E402
from sklearn.decomposition import PCA  # noqa: E402
from sklearn.linear_model import LinearRegression  # noqa: E402
from sklearn.metrics import silhouette_score  # noqa: E402
from sklearn.neighbors import KNeighborsRegressor  # noqa: E402
from sklearn.preprocessing import StandardScaler  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DADOS = os.path.join(RAIZ, "dados")
MENSAL = os.path.join(DADOS, "mensal")

SERIES = ["abate_bovinos", "abate_suinos", "abate_frangos",
          "producao_ovos", "producao_leite"]
ALVO = "abate_frangos"
FEATURES = (["lag1", "lag2", "lag3", "lag12", "sen", "cos", "dias"]
            + [s + "_lag1" for s in SERIES if s != ALVO])
EM_QUILOS = ["lag1", "lag2", "lag3", "lag12"] + [s + "_lag1" for s in SERIES if s != ALVO]
DO_CALENDARIO = ["sen", "cos", "dias"]
N_TESTE = 24
SEMENTE = 42


def _ler(caminho):
    with open(caminho, encoding="utf-8") as fh:
        return {l["periodo"]: float(l["valor"])
                for l in csv.DictReader(fh) if l["valor"]}


# --------------------------------------------------------------------------
# As bases. A mensal repete a construção de test_modelos_aula07.py e a
# trimestral repete a de test_clusters_aula06.py, de propósito: a Aula 08 não
# inventa base nova, ela reusa as duas que as aulas anteriores deixaram prontas.


@pytest.fixture(scope="module")
def mensal():
    series = {s: _ler(os.path.join(MENSAL, s + ".csv")) for s in SERIES}
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
    return {c: ([col[c][i] for i in manter] if c == "periodo"
                else np.array([col[c][i] for i in manter], dtype=float))
            for c in col}


@pytest.fixture(scope="module")
def trimestral():
    colunas = {s: _ler(os.path.join(DADOS, s + ".csv")) for s in SERIES}
    periodos = sorted(set.intersection(*[set(c) for c in colunas.values()]))
    return {
        "X": np.array([[colunas[s][p] for s in SERIES] for p in periodos]),
        "anos": np.array([int(p[:4]) for p in periodos]),
        "tris": np.array([int(p[-1]) for p in periodos]),
    }


@pytest.fixture(scope="module")
def participacao(trimestral):
    """Cada valor vira a fração que representa no total do próprio ano.

    Só entram anos com os quatro trimestres medidos, a mesma regra da Aula 06:
    2026 tem apenas o T1, e incluir ano incompleto faria o único trimestre dele
    valer 100% do ano.
    """
    b = trimestral
    completos = {a for a in set(b["anos"].tolist()) if (b["anos"] == a).sum() == 4}
    mascara = np.array([a in completos for a in b["anos"]])
    X, anos = b["X"][mascara], b["anos"][mascara]
    saida = np.empty_like(X)
    for a in completos:
        linhas = anos == a
        saida[linhas] = X[linhas] / X[linhas].sum(axis=0)
    return {"X": saida, "tris": b["tris"][mascara]}


@pytest.fixture(scope="module")
def treino(mensal):
    """Matriz padronizada e PCA, ajustados só nos 315 meses de treino."""
    n = len(mensal["periodo"])
    corte = n - N_TESTE
    X = np.column_stack([mensal[f] for f in FEATURES])
    escalador = StandardScaler().fit(X[:corte])
    Ztr, Zte = escalador.transform(X[:corte]), escalador.transform(X[corte:])
    return {
        "corte": corte,
        "X": X,
        "Ztr": Ztr,
        "Zte": Zte,
        "pca": PCA().fit(Ztr),
        "razao_tr": (mensal[ALVO] / mensal["lag12"])[:corte],
        "yte": mensal[ALVO][corte:],
        "lag12te": mensal["lag12"][corte:],
        "meses_tr": np.array([int(p.split("-")[1]) for p in mensal["periodo"][:corte]]),
    }


def _kmeans(matriz, k):
    padronizada = StandardScaler().fit_transform(matriz)
    modelo = KMeans(n_clusters=k, n_init=50, random_state=SEMENTE).fit(padronizada)
    return modelo, silhouette_score(padronizada, modelo.labels_)


def _concordancia(rotulos, verdade):
    """Fração das linhas cobertas pelo rótulo majoritário de cada cluster."""
    acertos = 0
    for c in set(rotulos.tolist()):
        do_cluster = verdade[rotulos == c]
        acertos += collections.Counter(do_cluster.tolist()).most_common(1)[0][1]
    return acertos / len(verdade)


def _mape(real, previsto):
    return float(np.mean(np.abs((real - previsto) / real)) * 100)


def _mape_com_k(t, k):
    """MAPE de teste da regressão sobre os k primeiros componentes."""
    pca = PCA(n_components=k).fit(t["Ztr"])
    modelo = LinearRegression().fit(pca.transform(t["Ztr"]), t["razao_tr"])
    previsto = modelo.predict(pca.transform(t["Zte"])) * t["lag12te"]
    return _mape(t["yte"], previsto)


def _baseline_ldc(mensal, corte):
    """Baseline C da Aula 07: lag12 vezes o fator médio medido no treino."""
    fator = float(np.mean(mensal[ALVO][:corte] / mensal["lag12"][:corte]))
    return mensal["lag12"][corte:] * fator


# --------------------------------------------------------------------------
# Bloco 1. Escolha de K: os dois critérios apontam K diferente do útil.


def test_elbow_aponta_k3_na_base_de_participacao(participacao):
    """A queda de inércia despenca depois de K=3, não depois de K=4.

    É o que o Elbow Plot mostra em sala: 25,1% de queda de K=2 para K=3, e
    14,3% de K=3 para K=4. O joelho está em 3.
    """
    inercias = {k: _kmeans(participacao["X"], k)[0].inertia_ for k in range(2, 6)}
    queda_ate_3 = (inercias[2] - inercias[3]) / inercias[2]
    queda_ate_4 = (inercias[3] - inercias[4]) / inercias[3]
    queda_ate_5 = (inercias[4] - inercias[5]) / inercias[4]

    assert 0.24 < queda_ate_3 < 0.26
    assert 0.13 < queda_ate_4 < 0.15
    assert queda_ate_3 > 1.7 * queda_ate_4
    assert queda_ate_4 - queda_ate_5 < 0.03


def test_silhueta_aponta_k2_na_base_de_participacao(participacao):
    """A silhueta é máxima em K=2 e cai quando K vai para o valor útil."""
    silhuetas = {k: _kmeans(participacao["X"], k)[1] for k in range(2, 9)}

    assert max(silhuetas, key=silhuetas.get) == 2
    assert 0.375 < silhuetas[2] < 0.382
    assert 0.283 < silhuetas[4] < 0.288
    assert silhuetas[2] > silhuetas[4]


def test_o_k_util_e_4_e_nenhum_dos_dois_criterios_o_indica(participacao):
    """A conclusão central do bloco, e o motivo de a aula existir.

    O Elbow aponta 3, a silhueta aponta 2, e só K=4 recupera o trimestre do
    calendário. Nenhum dos dois critérios internos encontra o K que serve ao
    case.
    """
    concordancias = {}
    for k in (2, 3, 4):
        modelo, _ = _kmeans(participacao["X"], k)
        concordancias[k] = _concordancia(modelo.labels_, participacao["tris"])

    assert concordancias[4] > 0.98
    assert concordancias[3] < 0.80
    assert concordancias[2] < 0.55
    assert max(concordancias, key=concordancias.get) == 4


def test_na_base_de_niveis_nenhum_k_sai_do_acaso(trimestral):
    """Agrupar os níveis não recupera o calendário em nenhum K de 2 a 8.

    O acaso de K grupos equilibrados sobre quatro trimestres é 25%. A silhueta,
    que é maior aqui do que em qualquer K da base de participação, premia o
    agrupamento que não serve ao case.
    """
    for k in range(2, 9):
        modelo, silhueta = _kmeans(trimestral["X"], k)
        concordancia = _concordancia(modelo.labels_, trimestral["tris"])
        assert concordancia < 0.30, "K=%d saiu do acaso" % k
        assert silhueta > 0.42, "K=%d perdeu a silhueta alta" % k


# --------------------------------------------------------------------------
# Bloco 2. PCA sobre as 11 features da base mensal.


def test_pc1_e_o_nivel_comum_das_cinco_series(treino):
    """PC1 vale 68,21% da variância e pesa as oito colunas em quilos.

    Os pesos de `sen`, `cos` e `dias` no PC1 são desprezíveis: o primeiro
    componente é a tendência de 28 anos que as cinco séries compartilham, não
    o calendário.
    """
    pca = treino["pca"]
    assert 0.679 < pca.explained_variance_ratio_[0] < 0.685

    peso = dict(zip(FEATURES, np.abs(pca.components_[0])))
    for f in EM_QUILOS:
        assert peso[f] > 0.33, f
    for f in DO_CALENDARIO:
        assert peso[f] < 0.05, f


def test_quatro_componentes_chegam_a_95_por_cento(treino):
    """A conta que a dupla faz em sala: onze colunas, quatro direções."""
    acumulada = np.cumsum(treino["pca"].explained_variance_ratio_)
    assert acumulada[1] > 0.80
    assert acumulada[3] > 0.95
    assert int(np.searchsorted(acumulada, 0.95) + 1) == 4


def test_o_plano_pc2_pc3_recupera_o_mes_sem_receber_o_mes(treino):
    """PC2 e PC3 carregam o calendário, e o plano deles reencontra o mês.

    Nenhuma coluna da matriz é o número do mês: entram `sen`, `cos` e o número
    de dias. Agrupando os 315 meses de treino em 12 grupos no plano PC2xPC3, o
    grupo majoritário acerta o mês em mais de 90% das linhas.
    """
    pca = treino["pca"]
    peso2 = dict(zip(FEATURES, np.abs(pca.components_[1])))
    peso3 = dict(zip(FEATURES, np.abs(pca.components_[2])))
    assert peso2["dias"] > 0.6 and peso2["sen"] > 0.6
    assert peso3["cos"] > 0.8

    plano = pca.transform(treino["Ztr"])[:, 1:3]
    rotulos = KMeans(n_clusters=12, n_init=50, random_state=SEMENTE).fit(plano).labels_
    assert _concordancia(rotulos, treino["meses_tr"]) > 0.90
    assert silhouette_score(plano, treino["meses_tr"]) > 0.78


def test_cortar_componentes_faz_o_modelo_perder_da_baseline(treino, mensal):
    """O achado que a aula leva para a ART.6.

    O modelo do fecho da Aula 07, com as 11 features, tem MAPE de 3,32% contra
    3,71% da baseline de coeficiente fixo da LDC. Reduzir a dimensionalidade
    por PCA derruba essa vantagem: com quatro componentes, que retêm 96,07% da
    variância, o MAPE vai a 4,94% e o modelo perde da baseline.
    """
    baseline = _mape(treino["yte"], _baseline_ldc(mensal, treino["corte"]))
    assert 3.70 < baseline < 3.72

    cheio = _mape_com_k(treino, len(FEATURES))
    assert 3.31 < cheio < 3.33
    assert cheio < baseline

    for k in range(1, 10):
        assert _mape_com_k(treino, k) > baseline, "k=%d nao perdeu da baseline" % k

    assert 4.90 < _mape_com_k(treino, 2) < 4.95
    assert 4.92 < _mape_com_k(treino, 4) < 4.96
    assert 6.15 < _mape_com_k(treino, 9) < 6.25


def test_a_variancia_pequena_carrega_o_poder_preditivo(treino):
    """O motivo medido do teste anterior, e o ponto conceitual do bloco.

    PC9 e PC10 valem 0,21% e 0,17% da variância, e recebem os dois maiores
    coeficientes da regressão sobre a razão: 22 e 27 vezes o coeficiente do
    PC1, que vale 68,21% da variância. Variância pequena não é sinônimo de
    informação irrelevante.
    """
    pca = treino["pca"]
    coeficientes = LinearRegression().fit(
        pca.transform(treino["Ztr"]), treino["razao_tr"]).coef_

    variancia = pca.explained_variance_ratio_
    assert variancia[8] < 0.003 and variancia[9] < 0.002

    maiores = np.argsort(-np.abs(coeficientes))[:2].tolist()
    assert sorted(maiores) == [8, 9]
    assert abs(coeficientes[8]) > 20 * abs(coeficientes[0])
    assert abs(coeficientes[9]) > 25 * abs(coeficientes[0])


def test_pca_completo_e_rotacao_e_nao_muda_a_previsao(treino):
    """k=11 devolve o MAPE das 11 features, e isso confirma a Aula 05.

    A Aula 05 mediu que regressão linear sem regularização é invariante a
    transformação afim das entradas. Rodar PCA sem descartar componente é uma
    rotação, então a previsão tem de ser a mesma até a nona casa decimal. O que
    custa MAPE é o corte, não a rotação.
    """
    modelo = LinearRegression().fit(treino["Ztr"], treino["razao_tr"])
    sem_pca = _mape(treino["yte"],
                    modelo.predict(treino["Zte"]) * treino["lag12te"])
    assert abs(_mape_com_k(treino, len(FEATURES)) - sem_pca) < 1e-9


def test_a_direcao_do_efeito_do_corte_depende_do_modelo(treino, mensal):
    """O escopo da conclusão da aula, medido nos dois modelos.

    A seção 13 do material e a `ADR-011` afirmam que o corte de componentes não
    tem direção única: ele piora a regressão linear e melhora o KNN de cinco
    vizinhos. Sem este teste, essa é a única afirmação publicada da aula que
    nenhuma asserção sustenta.
    """
    def mape_knn(k):
        if k is None:
            Xtr, Xte = treino["Ztr"], treino["Zte"]
        else:
            pca = PCA(n_components=k).fit(treino["Ztr"])
            Xtr, Xte = pca.transform(treino["Ztr"]), pca.transform(treino["Zte"])
        modelo = KNeighborsRegressor(n_neighbors=5).fit(Xtr, treino["razao_tr"])
        return _mape(treino["yte"], modelo.predict(Xte) * treino["lag12te"])

    sem_pca = mape_knn(None)
    assert 4.98 < sem_pca < 5.04

    com_quatro = mape_knn(4)
    assert 4.75 < com_quatro < 4.81
    assert 5.18 < mape_knn(3) < 5.23
    assert 5.60 < mape_knn(2) < 5.66

    # no KNN o corte melhora, e na regressão linear o mesmo corte piora
    assert com_quatro < sem_pca
    assert _mape_com_k(treino, 4) > _mape_com_k(treino, len(FEATURES))

    # e nenhum dos dois desce abaixo da baseline de coeficiente fixo da LDC
    baseline = _mape(treino["yte"], _baseline_ldc(mensal, treino["corte"]))
    assert com_quatro > baseline
    assert _mape_com_k(treino, 4) > baseline


def test_sem_padronizar_o_pc1_e_so_a_coluna_de_maior_desvio(treino):
    """Espelha o achado de condicionamento da Aula 05.

    Sem padronizar, PC1 explica 96,72% da variância e seus maiores pesos são as
    colunas em quilos, cujo desvio está na casa de 1e8, contra 0,7 de `sen` e
    `cos`. O componente deixa de descrever a estrutura dos dados e passa a
    descrever a unidade de medida das colunas.
    """
    Xtr = treino["X"][:treino["corte"]]
    pca = PCA().fit(Xtr)
    assert pca.explained_variance_ratio_[0] > 0.96

    peso = dict(zip(FEATURES, np.abs(pca.components_[0])))
    tres_maiores = sorted(peso, key=peso.get, reverse=True)[:3]
    assert all(f in EM_QUILOS for f in tres_maiores)
    for f in DO_CALENDARIO:
        assert peso[f] < 1e-6, f

    desvios = dict(zip(FEATURES, Xtr.std(axis=0)))
    assert desvios["lag1"] > 1e8
    assert desvios["sen"] < 1.0

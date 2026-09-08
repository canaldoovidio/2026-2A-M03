"""Trava as conclusões que a Aula 09 afirma sobre os erros silenciosos de modelagem.

A aula tem cinco blocos de conteúdo, e cada um afirma algo medido sobre a base
mensal de `dados/mensal/`:

  1  vazamento temporal. O RMSE não pode ser comparado entre corte por data e
     sorteio aleatório, porque o alvo médio do teste sorteado é cerca de 35%
     menor que o dos 24 últimos meses. O MAPE, que não depende de escala,
     mostra a melhora artificial, e só nos modelos que memorizam vizinho: KNN,
     árvore e random forest melhoram com o sorteio, e a regressão linear sobre
     a razão não melhora.
  2  o mecanismo do vazamento. No sorteio, todo mês de teste tem um mês vizinho
     no treino; no corte por data, apenas um dos 24 tem.
  3  ausência de dado. A união das cinco séries mensais tem 471 meses e a
     interseção 351, então a junção interna descarta 25,5% dos períodos, e
     20,4% das células da matriz período por série estão vazias.
  4  imputação. Mascarando 5% dos meses de treino do alvo, a média e a mediana
     erram cerca de 34%, o último valor e a interpolação linear erram cerca de
     7%, e o mesmo mês do ano anterior corrigido pelo fator médio erra 4,44%.
  5  dimensionalidade. Indo de 2 para 11 features, a distância euclidiana média
     entre meses de treino cresce de 1,65 para 4,31, o KNN piora de 3,71% para
     5,01% de MAPE e a regressão linear melhora de 4,71% para 3,32%.
  6  classificação e desbalanceamento. Com o alvo binário do case (o abate do
     mês supera o mesmo mês do ano anterior), o treino tem 78,1% de positivos e
     o teste 83,3%. A baseline que prevê sempre a classe majoritária acerta
     83,3%, com revocação 1,000, e nenhum dos cinco classificadores supera essa
     acurácia. O Naive Bayes gaussiano cai para 16,7%.
  7  entropia. A raiz vale 0,7584 bits, o melhor corte é `lag12` com ganho de
     0,0632 bits, e os dois candidatos de calendário (`sen` e `dias`) ganham
     0,0043 e 0,0082 bits. A árvore com critério de entropia escolhe o mesmo
     corte que a conta à mão.

Como em `test_modelo_aula05.py`, `test_clusters_aula06.py`,
`test_modelos_aula07.py` e `test_pca_aula08.py`, o que se trava aqui são as
conclusões, não só os números.

O item 1 corrige o roteiro original em `PLANEJAMENTO_AULA_A_AULA.md`, que
prometia "a queda artificial de RMSE" no sorteio aleatório sem ressalva de
escala, e o item 3 corrige o bloco de `SimpleImputer`, roteirizado sobre "os
vazios da própria série" quando nenhum CSV versionado tem valor vazio. Os dois
motivos estão na `ADR-012`.

Precisa de numpy e scikit-learn, do requirements-ci.txt. Sem eles o arquivo
inteiro se pula, e o CI continua cobrindo o resto.

Três versões propositalmente quebradas foram executadas contra esta suíte, e
cada uma reprovou os testes indicados:

  medir o vazamento com o alvo em razão, e não em nível
    -> `test_sorteio_aleatorio_melhora_quem_memoriza` (com a razão, a melhora
       desaparece: a própria aula usa esse contraste, e ele está travado em
       `test_vazamento_nao_atinge_todo_modelo_igual`).
  mascarar valores em bloco contíguo, e não sorteados
    -> `test_estrategias_de_imputacao_ficam_nesta_ordem` (a interpolação linear
       deixa de ter vizinho medido e passa a errar como a média).
  padronizar antes de medir a distância média entre meses
    -> nenhuma: a suíte já mede sobre a matriz padronizada, e essa é a única
       leitura em que o crescimento de 1,65 para 4,31 vale. Fica registrado
       para ninguém "corrigir" o teste tirando a padronização.
"""
import calendar
import csv
import os

import pytest

np = pytest.importorskip("numpy")
pytest.importorskip("sklearn")

from sklearn.ensemble import RandomForestRegressor  # noqa: E402
from sklearn.linear_model import LinearRegression, LogisticRegression  # noqa: E402
from sklearn.metrics import accuracy_score, precision_score, recall_score  # noqa: E402
from sklearn.model_selection import train_test_split  # noqa: E402
from sklearn.naive_bayes import GaussianNB  # noqa: E402
from sklearn.neighbors import KNeighborsRegressor  # noqa: E402
from sklearn.preprocessing import StandardScaler  # noqa: E402
from sklearn.svm import SVC  # noqa: E402
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor  # noqa: E402

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MENSAL = os.path.join(RAIZ, "dados", "mensal")

SERIES = ["abate_bovinos", "abate_suinos", "abate_frangos",
          "producao_ovos", "producao_leite"]
ALVO = "abate_frangos"
FEATURES = (["lag1", "lag2", "lag3", "lag12", "sen", "cos", "dias"]
            + [s + "_lag1" for s in SERIES if s != ALVO])
N_TESTE = 24
SEMENTE = 42
SEMENTES_SORTEIO = 10


def _serie(nome):
    with open(os.path.join(MENSAL, nome + ".csv"), encoding="utf-8") as fh:
        return {l["periodo"]: float(l["valor"])
                for l in csv.DictReader(fh) if l["valor"]}


@pytest.fixture(scope="module")
def series():
    return {s: _serie(s) for s in SERIES}


@pytest.fixture(scope="module")
def base(series):
    """A base analítica mensal da Aula 07: 339 linhas, de 1998-01 a 2026-03."""
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
    saida["n"] = len(saida["periodo"])
    saida["corte"] = saida["n"] - N_TESTE
    saida["X"] = np.column_stack([saida[f] for f in FEATURES])
    return saida


def _mape(real, previsto):
    return float(np.mean(np.abs((real - previsto) / real)) * 100)


def _rmse(real, previsto):
    return float(np.sqrt(np.mean((real - previsto) ** 2)))


def _indices(base, aleatorio, semente):
    if not aleatorio:
        return np.arange(base["corte"]), np.arange(base["corte"], base["n"])
    return train_test_split(np.arange(base["n"]),
                            test_size=N_TESTE / base["n"], random_state=semente)


def _avaliar(base, fabrica, aleatorio, em_razao=False):
    """MAPE médio de teste, com corte por data ou média de 10 sorteios."""
    y = base[ALVO]
    alvo = y / base["lag12"] if em_razao else y
    saida = []
    for semente in range(SEMENTES_SORTEIO if aleatorio else 1):
        itr, ite = _indices(base, aleatorio, semente)
        escalador = StandardScaler().fit(base["X"][itr])
        modelo = fabrica().fit(escalador.transform(base["X"][itr]), alvo[itr])
        previsto = modelo.predict(escalador.transform(base["X"][ite]))
        if em_razao:
            previsto = previsto * base["lag12"][ite]
        saida.append(_mape(y[ite], previsto))
    return float(np.mean(saida))


# --------------------------------------------------------------------------
# Bloco 1. Vazamento temporal.


def test_rmse_nao_e_comparavel_entre_os_dois_cortes(base):
    """A ressalva que o roteiro original não fazia.

    O teste sorteado cai majoritariamente em anos antigos, quando o abate era
    muito menor, e o RMSE em quilogramas cai junto. Parte da "melhora" do
    sorteio é a escala do período sorteado, não habilidade do modelo.
    """
    y = base[ALVO]
    media_temporal = float(y[base["corte"]:].mean())
    medias = []
    for semente in range(SEMENTES_SORTEIO):
        _, ite = _indices(base, True, semente)
        medias.append(float(y[ite].mean()))
    media_sorteada = float(np.mean(medias))

    assert media_sorteada < 0.75 * media_temporal
    assert media_temporal > 1.15e9
    assert media_sorteada < 0.85e9

    # e o RMSE segue a escala: cai no sorteio até para a regressão linear, que
    # no MAPE não melhora nada (ver o teste seguinte).
    itr, ite = _indices(base, False, 0)
    escalador = StandardScaler().fit(base["X"][itr])
    modelo = LinearRegression().fit(escalador.transform(base["X"][itr]), y[itr])
    rmse_data = _rmse(y[ite], modelo.predict(escalador.transform(base["X"][ite])))

    rmses = []
    for semente in range(SEMENTES_SORTEIO):
        itr, ite = _indices(base, True, semente)
        escalador = StandardScaler().fit(base["X"][itr])
        modelo = LinearRegression().fit(escalador.transform(base["X"][itr]), y[itr])
        rmses.append(_rmse(y[ite], modelo.predict(escalador.transform(base["X"][ite]))))
    assert float(np.mean(rmses)) < rmse_data


def test_sorteio_aleatorio_melhora_quem_memoriza(base):
    """Com o alvo em nível, os três modelos que memorizam vizinho melhoram.

    São as melhoras artificiais que a aula demonstra ao vivo. O MAPE não
    depende de escala, então aqui a melhora é vazamento, e não o efeito de
    período medido no teste anterior.
    """
    casos = [
        ("KNN k=5", lambda: KNeighborsRegressor(n_neighbors=5), 7.64, 5.29),
        ("árvore d=3", lambda: DecisionTreeRegressor(max_depth=3, random_state=SEMENTE),
         8.81, 6.31),
        ("random forest", lambda: RandomForestRegressor(n_estimators=300,
                                                        random_state=SEMENTE), 5.70, 4.04),
    ]
    for rotulo, fabrica, esperado_data, esperado_sorteio in casos:
        honesto = _avaliar(base, fabrica, False)
        sorteado = _avaliar(base, fabrica, True)
        assert abs(honesto - esperado_data) < 0.15, rotulo
        assert abs(sorteado - esperado_sorteio) < 0.15, rotulo
        assert sorteado < honesto - 1.5, rotulo


def test_vazamento_nao_atinge_todo_modelo_igual(base):
    """A regressão linear sobre a razão não melhora com o sorteio.

    É o contraste que impede a aula de ensinar "sorteio sempre infla a métrica".
    O modelo do fecho da Aula 07 tem 3,32% com corte por data e 3,60% com
    sorteio: piora. Disciplina de corte por data é disciplina de protocolo, não
    conserto de um modelo específico.
    """
    honesto = _avaliar(base, lambda: LinearRegression(), False, em_razao=True)
    sorteado = _avaliar(base, lambda: LinearRegression(), True, em_razao=True)

    assert abs(honesto - 3.32) < 0.02
    assert abs(sorteado - 3.60) < 0.10
    assert sorteado > honesto


def test_no_sorteio_todo_mes_de_teste_tem_vizinho_no_treino(base):
    """O mecanismo do vazamento, contado mês a mês."""
    def com_vizinho(itr, ite):
        treino = set(itr.tolist())
        return sum(1 for t in ite.tolist() if (t - 1) in treino or (t + 1) in treino)

    itr, ite = _indices(base, False, 0)
    assert com_vizinho(itr, ite) == 1

    fracoes = []
    for semente in range(SEMENTES_SORTEIO):
        itr, ite = _indices(base, True, semente)
        fracoes.append(com_vizinho(itr, ite) / len(ite))
    assert min(fracoes) > 0.80
    assert float(np.mean(fracoes)) > 0.95


# --------------------------------------------------------------------------
# Bloco 2. Ausência de dado, e o que a junção interna descarta.


def test_a_juncao_interna_descarta_um_quarto_dos_periodos(series):
    """O contrato de ausência do case, medido, e não o `SimpleImputer` do roteiro.

    Nenhum CSV versionado tem valor vazio: a ausência real do acervo é de
    período, porque `producao_ovos` começa dez anos antes das outras quatro.
    """
    for nome, valores in series.items():
        assert all(v == v for v in valores.values()), nome

    uniao = set.union(*[set(v) for v in series.values()])
    intersecao = set.intersection(*[set(v) for v in series.values()])
    assert len(uniao) == 471
    assert len(intersecao) == 351
    descartada = (len(uniao) - len(intersecao)) / len(uniao)
    assert 0.25 < descartada < 0.26

    celulas = len(uniao) * len(SERIES)
    vazias = celulas - sum(len(v) for v in series.values())
    assert celulas == 2355
    assert vazias == 480
    assert 0.20 < vazias / celulas < 0.21

    assert len(series["producao_ovos"]) == 471
    for nome in SERIES:
        if nome != "producao_ovos":
            assert len(series[nome]) == 351, nome


def test_estrategias_de_imputacao_ficam_nesta_ordem(base):
    """Mascarando 5% do alvo no treino, a ordem de erro é sempre a mesma.

    Média e mediana erram cerca de 34%, porque a série cresce por 28 anos e a
    média global não descreve nenhum mês em particular. O último valor e a
    interpolação linear erram cerca de 7%. O mesmo mês do ano anterior
    corrigido pelo fator médio erra 4,44%, e é a única estratégia que usa a
    estrutura sazonal que as Aulas 04 a 08 já mediram.
    """
    corte = base["corte"]
    alvo = base[ALVO][:corte].copy()
    gerador = np.random.default_rng(SEMENTE)
    quantos = int(round(0.05 * corte))
    indices = np.sort(gerador.choice(np.arange(1, corte - 1), size=quantos,
                                     replace=False))
    verdade = alvo[indices]
    assert quantos == 16

    com_furo = alvo.copy()
    com_furo[indices] = np.nan

    ultimo = com_furo.copy()
    for i in range(1, len(ultimo)):
        if np.isnan(ultimo[i]):
            ultimo[i] = ultimo[i - 1]

    validos = ~np.isnan(com_furo)
    xs = np.arange(corte)
    fator = float(np.nanmean(com_furo[12:] / alvo[:corte - 12]))
    sazonal = np.array([alvo[i - 12] * fator for i in indices])

    erros = {
        "media": np.full(quantos, np.nanmean(com_furo)),
        "mediana": np.full(quantos, np.nanmedian(com_furo)),
        "ultimo": ultimo[indices],
        "interpolacao": np.interp(indices, xs[validos], com_furo[validos]),
        "sazonal": sazonal,
    }
    erro = {k: 100 * float(np.mean(np.abs((v - verdade) / verdade)))
            for k, v in erros.items()}

    assert 34.0 < erro["media"] < 35.0
    assert 34.0 < erro["mediana"] < 35.0
    assert 7.0 < erro["ultimo"] < 8.0
    assert 7.0 < erro["interpolacao"] < 7.5
    assert 4.0 < erro["sazonal"] < 4.6

    assert erro["sazonal"] < erro["interpolacao"] < erro["ultimo"]
    assert erro["ultimo"] < erro["mediana"] / 4


# --------------------------------------------------------------------------
# Bloco 3. Dimensionalidade.


def test_mais_features_afastam_os_meses_e_separam_os_dois_modelos(base):
    """A distância média cresce, e os dois modelos reagem em direções opostas.

    A medição é sobre a matriz padronizada, que é a única leitura em que o
    crescimento significa distribuição de dimensões e não unidade de coluna.
    """
    conjuntos = {
        2: ["lag1", "lag12"],
        4: ["lag1", "lag12", "sen", "cos"],
        7: ["lag1", "lag2", "lag3", "lag12", "sen", "cos", "dias"],
        11: FEATURES,
    }
    corte = base["corte"]
    y = base[ALVO]
    razao = y / base["lag12"]

    distancia, knn, regressao = {}, {}, {}
    for quantas, colunas in conjuntos.items():
        X = np.column_stack([base[c] for c in colunas])
        escalador = StandardScaler().fit(X[:corte])
        Ztr, Zte = escalador.transform(X[:corte]), escalador.transform(X[corte:])

        pares = np.linalg.norm(Ztr[:, None, :] - Ztr[None, :, :], axis=2)
        distancia[quantas] = float(pares[~np.eye(len(pares), dtype=bool)].mean())

        previsto = KNeighborsRegressor(n_neighbors=5).fit(
            Ztr, razao[:corte]).predict(Zte) * base["lag12"][corte:]
        knn[quantas] = _mape(y[corte:], previsto)

        previsto = LinearRegression().fit(
            Ztr, razao[:corte]).predict(Zte) * base["lag12"][corte:]
        regressao[quantas] = _mape(y[corte:], previsto)

    assert abs(distancia[2] - 1.65) < 0.05
    assert abs(distancia[11] - 4.31) < 0.05
    assert distancia[2] < distancia[4] < distancia[7] < distancia[11]

    assert abs(knn[2] - 3.71) < 0.05
    assert abs(knn[11] - 5.01) < 0.05
    assert knn[11] > knn[2]

    assert abs(regressao[2] - 4.71) < 0.05
    assert abs(regressao[11] - 3.32) < 0.02
    assert regressao[11] < regressao[2]


# --------------------------------------------------------------------------
# Bloco 4. Classificação e desbalanceamento.


@pytest.fixture(scope="module")
def classificacao(base):
    """Alvo binário do case: o abate do mês supera o mesmo mês do ano anterior."""
    corte = base["corte"]
    alvo = (base[ALVO] > base["lag12"]).astype(int)
    escalador = StandardScaler().fit(base["X"][:corte])
    return {
        "Ztr": escalador.transform(base["X"][:corte]),
        "Zte": escalador.transform(base["X"][corte:]),
        "atr": alvo[:corte],
        "ate": alvo[corte:],
    }


def test_o_alvo_binario_do_case_e_desbalanceado(classificacao):
    """78,1% de positivos no treino e 83,3% no teste."""
    atr, ate = classificacao["atr"], classificacao["ate"]
    assert abs(float(atr.mean()) - 0.781) < 0.005
    assert abs(float(ate.mean()) - 0.833) < 0.005
    assert int(atr.sum()) == 246
    assert int(ate.sum()) == 20


def test_nenhum_classificador_supera_a_baseline_majoritaria(classificacao):
    """A conclusão central do bloco, e o motivo de acurácia não servir aqui.

    Prever sempre "cresce" acerta 83,3% dos 24 meses de teste, com revocação
    1,000 e precisão 0,833. Nenhum dos cinco classificadores passa disso: a
    regressão logística fica abaixo, e os outros três empatam porque também
    preveem a classe majoritária quase sempre.
    """
    Ztr, Zte = classificacao["Ztr"], classificacao["Zte"]
    atr, ate = classificacao["atr"], classificacao["ate"]

    maioria = np.full(len(ate), int(atr.mean() > 0.5))
    base_acuracia = accuracy_score(ate, maioria)
    assert abs(base_acuracia - 0.8333) < 0.005
    assert recall_score(ate, maioria) == 1.0
    assert abs(precision_score(ate, maioria) - 0.8333) < 0.005

    modelos = {
        "logistica": LogisticRegression(max_iter=2000, random_state=SEMENTE),
        "naive_bayes": GaussianNB(),
        "svm_linear": SVC(kernel="linear", random_state=SEMENTE),
        "svm_rbf": SVC(kernel="rbf", random_state=SEMENTE),
        "arvore_entropia": DecisionTreeClassifier(criterion="entropy", max_depth=3,
                                                  random_state=SEMENTE),
    }
    acuracia = {}
    for nome, modelo in modelos.items():
        previsto = modelo.fit(Ztr, atr).predict(Zte)
        acuracia[nome] = accuracy_score(ate, previsto)
        assert acuracia[nome] <= base_acuracia + 1e-9, nome

    assert abs(acuracia["logistica"] - 0.7917) < 0.005
    assert abs(acuracia["svm_linear"] - 0.8333) < 0.005
    assert abs(acuracia["naive_bayes"] - 0.1667) < 0.005


def test_o_naive_bayes_erra_a_classe_majoritaria_inteira(classificacao):
    """16,7% de acurácia com precisão e revocação zero na classe positiva.

    O modelo não empata com a baseline: ele acerta apenas os quatro meses em que
    o abate caiu, e erra os vinte em que subiu. Serve de exemplo de modelo que
    a acurácia sozinha jamais explicaria.
    """
    previsto = GaussianNB().fit(classificacao["Ztr"], classificacao["atr"]).predict(
        classificacao["Zte"])
    ate = classificacao["ate"]

    assert accuracy_score(ate, previsto) < 0.20
    assert precision_score(ate, previsto, zero_division=0) == 0.0
    assert recall_score(ate, previsto, zero_division=0) == 0.0
    assert int((previsto == 0).sum()) >= 23


# --------------------------------------------------------------------------
# Bloco 5. Entropia à mão.


def test_a_conta_de_entropia_a_mao_bate_com_a_arvore(base, classificacao):
    """A raiz vale 0,7584 bits e o melhor corte é `lag12`, com 0,0632 bits.

    A conta é feita aqui varrendo todos os limiares de todas as features, e o
    resultado é o mesmo corte que `DecisionTreeClassifier(criterion="entropy")`
    escolhe. Os dois candidatos de calendário perdem: `sen` ganha 0,0043 bits e
    `dias` ganha 0,0082.
    """
    corte = base["corte"]
    alvo = classificacao["atr"]

    def entropia(p):
        if p <= 0 or p >= 1:
            return 0.0
        return float(-p * np.log2(p) - (1 - p) * np.log2(1 - p))

    raiz = entropia(float(alvo.mean()))
    assert abs(raiz - 0.7584) < 0.0005

    def melhor_ganho(coluna):
        valores = np.unique(coluna)
        limiares = (valores[:-1] + valores[1:]) / 2
        melhor = (None, None)
        for t in limiares:
            esq, dir_ = alvo[coluna <= t], alvo[coluna > t]
            if len(esq) == 0 or len(dir_) == 0:
                continue
            ponderada = (len(esq) * entropia(float(esq.mean()))
                         + len(dir_) * entropia(float(dir_.mean()))) / len(alvo)
            if melhor[0] is None or raiz - ponderada > melhor[0]:
                melhor = (raiz - ponderada, float(t))
        return melhor

    ganhos = {f: melhor_ganho(base[f][:corte]) for f in FEATURES}
    campeao = max(ganhos, key=lambda f: ganhos[f][0])

    assert campeao == "lag12"
    assert abs(ganhos["lag12"][0] - 0.0632) < 0.0005
    assert abs(ganhos["sen"][0] - 0.0043) < 0.0005
    assert abs(ganhos["dias"][0] - 0.0082) < 0.0005
    assert ganhos["lag12"][0] > 7 * ganhos["sen"][0]

    # a árvore, sem padronizar, escolhe o mesmo corte da conta à mão
    X = np.column_stack([base[f] for f in FEATURES])
    arvore = DecisionTreeClassifier(criterion="entropy", max_depth=3,
                                    random_state=SEMENTE).fit(X[:corte], alvo)
    no = arvore.tree_
    assert FEATURES[no.feature[0]] == "lag12"
    assert abs(no.threshold[0] - ganhos["lag12"][1]) < 3.0
    assert abs(no.impurity[0] - raiz) < 0.0005

    esquerdo, direito = no.children_left[0], no.children_right[0]
    assert int(no.n_node_samples[esquerdo]) == 144
    assert int(no.n_node_samples[direito]) == 171
    assert abs(no.impurity[esquerdo] - 0.4374) < 0.0005
    assert abs(no.impurity[direito] - 0.9123) < 0.0005


def test_o_corte_degenerado_de_dias_nao_separa_nada(base, classificacao):
    """`dias` tem quatro valores distintos, e o corte em 31 deixa tudo de um lado.

    Serve de contraexemplo no slide de escolha de corte: um limiar que não
    parte a amostra não tem ganho a medir.
    """
    coluna = base["dias"][:base["corte"]]
    assert sorted(set(coluna.tolist())) == [28.0, 29.0, 30.0, 31.0]
    assert int((coluna <= 31).sum()) == len(coluna)
    assert int((coluna > 31).sum()) == 0

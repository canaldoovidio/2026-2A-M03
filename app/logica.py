"""Lógica do app da Aula 14, sem Streamlit: tudo o que a tela mostra sai daqui.

Por que um módulo separado de `app.py`:

- a tela do Streamlit reexecuta o script inteiro a cada clique, e testar isso
  exige um navegador ou o `AppTest`. As contas que a tela exibe são funções
  puras, testáveis com `pytest` comum (`tools/tests/test_app_aula14.py`);
- o notebook da Aula 14 importa este mesmo módulo e roda cada conta sem abrir
  servidor nenhum, o que também funciona no Colab.

O que o módulo faz, em ordem:

1. `carregar_series` lê os cinco CSVs mensais de `dados/mensal/`.
2. `base_analitica` monta a base das Aulas 07 a 12: 339 linhas, onze features.
   É a mesma lógica de `tools/exportar_modelo_aula12.py`, reimplementada aqui
   de propósito para `app/` não depender de `tools/`; o teste confere que as
   duas produzem a mesma matriz, número a número.
3. `carregar_pipeline` abre o `app/modelo_aula12.joblib` da Aula 12.
4. `prever_teste` devolve os 24 meses de teste (2024-04 a 2026-03) com o valor
   medido pelo IBGE e a previsão do modelo exportado.
5. `prever_cenario` recalcula a mesma previsão com um choque percentual numa
   entrada que o modelo de fato usa.
6. `prever_proximo_mes` faz a única previsão genuinamente futura que o modelo
   consegue fazer sem prever as outras séries: o mês seguinte ao último do CSV.

Três cuidados de honestidade, que a Aula 14 ensina e que o código impõe:

- **O número de erro que acompanha o app é o do objeto avaliado** (315 meses de
  treino, 2,86% nos 24 meses de teste), e não o do objeto exportado. O
  exportado foi reajustado sobre as 339 linhas e já viu esses 24 meses: medi-lo
  ali dá 2,65%, que não é estimativa de nada (`docs/adrs/ADR-015`).
  `mape_do_avaliado` recalcula o número certo a partir dos CSVs.
- **As 24 previsões de teste são de um passo à frente**: cada mês usa o `lag1`
  real do mês anterior. Não é a previsão de 24 meses de uma vez que o TAPI da
  LDC pede. A Aula 05 mediu a diferença entre as duas coisas.
- **Cenário só existe sobre entrada que o modelo usa.** O modelo não tem preço
  de milho, câmbio nem preço de ração entre as onze features, então um controle
  de "preço do milho" na tela seria decoração: mexeria num número que o modelo
  nunca lê. `aplicar_choque` recusa qualquer entrada fora de `FEATURES`, e
  `ENTRADAS_FORA_DO_MODELO` lista o que ficou de fora e o que faltaria para
  entrar. Decisão registrada em `docs/adrs/ADR-017`.
"""
import calendar
import os

import numpy as np
import pandas as pd

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA_MENSAL = os.path.join(RAIZ, "dados", "mensal")
MODELO = os.path.join(RAIZ, "app", "modelo_aula12.joblib")

SERIES = ["abate_bovinos", "abate_suinos", "abate_frangos",
          "producao_ovos", "producao_leite"]
ALVO = "abate_frangos"
FEATURES = (["lag1", "lag2", "lag3", "lag12", "sen", "cos", "dias"]
            + [s + "_lag1" for s in SERIES if s != ALVO])
N_TESTE = 24

NOMES = {
    "abate_bovinos": "Abate de bovinos",
    "abate_suinos": "Abate de suínos",
    "abate_frangos": "Abate de frangos",
    "producao_ovos": "Produção de ovos",
    "producao_leite": "Produção de leite",
}

# Os cenários que o app oferece. Cada um é um choque percentual aplicado, ao
# mesmo tempo, a todas as colunas do grupo, nos 24 meses de teste.
#
# Os dois primeiros são grupos de propósito. A Aula 12 mediu VIF de até 69 entre
# as features: `lag1`, `lag2`, `lag3` e `lag12` dizem quase a mesma coisa, e o
# modelo reparte peso entre elas de um jeito que muda a cada reajuste. Um choque
# no grupo inteiro soma os coeficientes do grupo, e essa soma é estável; um
# choque numa coluna só lê um coeficiente isolado, que não é. O terceiro cenário
# existe para mostrar isso na tela. O aviso de instabilidade não vem de uma
# marcação neste dicionário: vem de `estabilidade_do_cenario`, que mede.
CENARIOS = {
    "patamar_frango": {
        "rotulo": "Patamar do frango (4 defasagens)",
        "colunas": ["lag1", "lag2", "lag3", "lag12"],
    },
    "outras_proteinas": {
        "rotulo": "Outras 4 séries no mês anterior",
        "colunas": ["abate_bovinos_lag1", "abate_suinos_lag1",
                    "producao_ovos_lag1", "producao_leite_lag1"],
    },
    "so_bovinos": {
        "rotulo": "Só bovinos no mês anterior",
        "colunas": ["abate_bovinos_lag1"],
    },
}

# O que um gestor da LDC pediria para variar e o modelo não lê. Aparece na tela
# só como aviso.
ENTRADAS_FORA_DO_MODELO = {
    "Preço do milho": (
        "não é feature do modelo. Entrar exige uma série aberta de preço (por "
        "exemplo, o indicador de milho do CEPEA), a defasagem com que o preço "
        "afeta o abate, e um modelo retreinado e reavaliado no mesmo corte "
        "temporal."),
    "Preço do farelo de soja": (
        "mesma situação do milho: não é feature, e o farelo pertence ao Modelo "
        "3 do TAPI, o dos macroingredientes, que vem depois deste."),
    "Câmbio e exportação": (
        "não estão em dados/. A série de exportação de frango existe em fonte "
        "aberta, mas nunca foi baixada nem avaliada no acervo."),
}


# ----------------------------------------------------------------- dados
def carregar_series(pasta=PASTA_MENSAL):
    """Os cinco CSVs mensais, cada um como DataFrame com `periodo` e `valor`."""
    series = {}
    for nome in SERIES:
        tabela = pd.read_csv(os.path.join(pasta, nome + ".csv"))
        series[nome] = tabela[["periodo", "valor", "unidade"]].copy()
    return series


def base_analitica(pasta=PASTA_MENSAL):
    """A base analítica mensal das Aulas 07 a 12: 339 linhas, de 1998-01 a 2026-03."""
    base = None
    for nome in SERIES:
        coluna = (pd.read_csv(os.path.join(pasta, nome + ".csv"))[["periodo", "valor"]]
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


def carregar_pipeline(caminho=MODELO):
    """O `Pipeline` exportado na Aula 12, reajustado sobre as 339 linhas."""
    import joblib
    return joblib.load(caminho)


def numero_br(valor, casas=2, sinal=False):
    """Formata com vírgula decimal e ponto de milhar, como no resto do acervo."""
    texto = ("{:+,.%df}" if sinal else "{:,.%df}") % casas
    return texto.format(valor).replace(",", "_").replace(".", ",").replace("_", ".")


def mape(real, previsto):
    real = np.asarray(real, dtype=float)
    previsto = np.asarray(previsto, dtype=float)
    return float(np.mean(np.abs((real - previsto) / real)) * 100)


# ----------------------------------------------------------------- previsão
def _teste(base):
    return base.iloc[len(base) - N_TESTE:].reset_index(drop=True)


def prever_teste(pipe, base):
    """Os 24 meses de teste: valor medido, previsão do modelo exportado e erro.

    Previsão de um passo à frente: cada linha usa as defasagens reais do próprio
    mês, então o erro de um mês não contamina o seguinte.
    """
    teste = _teste(base)
    previsto = pipe.predict(teste[FEATURES].to_numpy())
    return pd.DataFrame({
        "periodo": teste["periodo"],
        "real": teste[ALVO].to_numpy(dtype=float),
        "previsto": previsto,
        "erro_pct": (previsto - teste[ALVO].to_numpy(dtype=float))
        / teste[ALVO].to_numpy(dtype=float) * 100,
    })


def pipeline_avaliado(base):
    """O objeto avaliado da Aula 11: o mesmo Pipeline, ajustado só nos 315 meses."""
    from sklearn.linear_model import LinearRegression
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler

    corte = len(base) - N_TESTE
    pipe = Pipeline([("escala", StandardScaler()), ("modelo", LinearRegression())])
    return pipe.fit(base[FEATURES].to_numpy()[:corte], base[ALVO].to_numpy()[:corte])


def mape_do_avaliado(base):
    """O único MAPE honesto de publicar junto do app: 2,86%, medido fora da amostra."""
    teste = _teste(base)
    previsto = pipeline_avaliado(base).predict(teste[FEATURES].to_numpy())
    return mape(teste[ALVO].to_numpy(), previsto)


# ----------------------------------------------------------------- cenários
def aplicar_choque(X, colunas, choque_pct):
    """Multiplica as colunas indicadas por (1 + choque/100). Não altera `X`.

    Recusa coluna que não seja feature do modelo: é a trava que impede um
    controle de tela de mexer num número que o modelo nunca lê.
    """
    fora = [c for c in colunas if c not in FEATURES]
    if fora:
        raise ValueError(
            "entrada fora do modelo: %s. O Pipeline da Aula 12 só lê as onze "
            "features de FEATURES; um cenário sobre outra variável exige outra "
            "feature, outra fonte e outro modelo." % ", ".join(fora))
    novo = np.array(X, dtype=float, copy=True)
    for c in colunas:
        novo[:, FEATURES.index(c)] *= 1 + choque_pct / 100.0
    return novo


def prever_cenario(pipe, base, cenario, choque_pct):
    """A previsão dos 24 meses de teste, antes e depois do choque.

    `cenario` é uma chave de `CENARIOS` ou uma lista de colunas de `FEATURES`.
    Devolve um DataFrame com a previsão de referência, a previsão sob o
    cenário e o efeito em porcentagem, mês a mês.
    """
    colunas = CENARIOS[cenario]["colunas"] if isinstance(cenario, str) else list(cenario)
    teste = _teste(base)
    X = teste[FEATURES].to_numpy()
    referencia = pipe.predict(X)
    com_choque = pipe.predict(aplicar_choque(X, colunas, choque_pct))
    return pd.DataFrame({
        "periodo": teste["periodo"],
        "real": teste[ALVO].to_numpy(dtype=float),
        "referencia": referencia,
        "cenario": com_choque,
        "efeito_pct": (com_choque - referencia) / referencia * 100,
    })


def efeito_medio(pipe, base, cenario, choque_pct):
    """O efeito médio do cenário sobre as 24 previsões, em porcentagem."""
    return float(prever_cenario(pipe, base, cenario, choque_pct)["efeito_pct"].mean())


def estabilidade_do_cenario(pipe_exportado, base, cenario, choque_pct):
    """O mesmo cenário lido no modelo exportado e no avaliado.

    É o critério de publicação que a Aula 12 deixou para a ART.8 aplicado ao
    cenário: se dois ajustes do mesmo modelo, com 24 meses de diferença, dão
    efeitos de sinal oposto, o cenário não pode ir para a tela da LDC como
    afirmação sobre o mundo.
    """
    exportado = efeito_medio(pipe_exportado, base, cenario, choque_pct)
    avaliado = efeito_medio(pipeline_avaliado(base), base, cenario, choque_pct)
    mesmo_sinal = np.sign(exportado) == np.sign(avaliado)
    return {
        "exportado": exportado,
        "avaliado": avaliado,
        "mesmo_sinal": bool(mesmo_sinal),
        "diferenca_pp": abs(exportado - avaliado),
    }


# ----------------------------------------------------------------- gráfico
def _data(periodos):
    """AAAA-MM vira o primeiro dia do mês, para o eixo do gráfico ser temporal."""
    return pd.to_datetime(pd.Series(list(periodos)) + "-01")


def tabela_do_historico(tabela, meses):
    """Os últimos `meses` de uma série, no formato longo que o gráfico recebe.

    Devolve a tabela e o título do eixo. Séries em quilogramas vão para milhões
    de quilogramas, como a de frangos; ovos e leite ficam na unidade do IBGE.
    """
    recorte = tabela.tail(meses)
    unidade = recorte["unidade"].iloc[0]
    valores = recorte["valor"].to_numpy(dtype=float)
    if unidade == "Quilogramas":
        valores, titulo = valores / 1e6, "milhões de kg por mês"
    else:
        titulo = unidade.lower() + " por mês"
    return (pd.DataFrame({"data": _data(recorte["periodo"]), "valor": valores,
                          "curva": "Medido pelo IBGE"}), titulo)


def tabela_do_grafico(pipe, base, meses, cenario, choque_pct):
    """Histórico, previsão e, se houver choque, a previsão sob o cenário.

    Formato longo (`data`, `valor`, `curva`), em milhões de quilogramas. A
    previsão só existe nos 24 meses de teste: nenhuma linha é inventada fora
    deles.
    """
    historico = base.tail(meses)
    partes = [pd.DataFrame({"data": _data(historico["periodo"]),
                            "valor": historico[ALVO].to_numpy(dtype=float) / 1e6,
                            "curva": "Medido pelo IBGE"})]
    resultado = prever_cenario(pipe, base, cenario, choque_pct)
    partes.append(pd.DataFrame({"data": _data(resultado["periodo"]),
                                "valor": resultado["referencia"].to_numpy() / 1e6,
                                "curva": "Previsão do modelo"}))
    if choque_pct != 0:
        partes.append(pd.DataFrame({"data": _data(resultado["periodo"]),
                                    "valor": resultado["cenario"].to_numpy() / 1e6,
                                    "curva": "Previsão sob o cenário"}))
    return pd.concat(partes, ignore_index=True)


# ----------------------------------------------------------------- futuro
def proximo_periodo(periodo):
    ano, mes = int(periodo[:4]), int(periodo[-2:])
    ano, mes = (ano + 1, 1) if mes == 12 else (ano, mes + 1)
    return "%04d-%02d" % (ano, mes)


def features_do_proximo_mes(pasta=PASTA_MENSAL):
    """As onze features do mês seguinte ao último do CSV, todas já medidas.

    Funciona para exatamente um mês: as defasagens de 1, 2, 3 e 12 meses e o
    mês anterior das outras quatro séries existem no CSV. Dois meses adiante,
    `lag1` seria a própria previsão, e as outras séries precisariam de modelo
    próprio.
    """
    base = None
    for nome in SERIES:
        coluna = (pd.read_csv(os.path.join(pasta, nome + ".csv"))[["periodo", "valor"]]
                  .rename(columns={"valor": nome}))
        base = coluna if base is None else base.merge(coluna, on="periodo", how="inner")
    base = base.sort_values("periodo").reset_index(drop=True)

    alvo = base[ALVO].to_numpy(dtype=float)
    periodo = proximo_periodo(base["periodo"].iloc[-1])
    mes = int(periodo[-2:])
    linha = {
        "lag1": alvo[-1], "lag2": alvo[-2], "lag3": alvo[-3], "lag12": alvo[-12],
        "sen": np.sin(2 * np.pi * mes / 12),
        "cos": np.cos(2 * np.pi * mes / 12),
        "dias": calendar.monthrange(int(periodo[:4]), mes)[1],
    }
    for nome in SERIES:
        if nome != ALVO:
            linha[nome + "_lag1"] = float(base[nome].iloc[-1])
    return periodo, np.array([[linha[f] for f in FEATURES]], dtype=float)


def prever_proximo_mes(pipe, pasta=PASTA_MENSAL):
    """A previsão do mês seguinte ao último publicado pelo IBGE."""
    periodo, X = features_do_proximo_mes(pasta)
    return periodo, float(pipe.predict(X)[0])

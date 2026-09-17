"""Gera `app/modelo_aula12.joblib`, o Pipeline que a Aula 12 empacota.

O modelo é o vencedor da Aula 11 (`docs/adrs/ADR-014`): regressão linear sobre o
alvo em **nível**, com as onze features das Aulas 09 a 11, sobre a base mensal de
`dados/mensal/`. O que muda aqui, e é o conteúdo do bloco de export da aula, é
que o objeto exportado é **reajustado sobre as 339 linhas**, e não sobre os 315
meses de treino: a avaliação terminou na Aula 11, e o que vai para produção usa
todo o dado disponível.

Por que existe um script, em vez de o notebook gravar o arquivo: `app/` é
versionado e a Aula 13 carrega esse mesmo arquivo para dentro do app Streamlit.
Um binário commitado precisa ser reproduzível por um comando declarado, senão
ninguém consegue auditar de onde ele veio. `tools/tests/test_pipeline_aula12.py`
regenera o Pipeline do zero e compara com o arquivo versionado.

Determinismo: `LinearRegression` e `StandardScaler` não sorteiam nada, e a base
vem de CSVs versionados. Rodar o script duas vezes produz o mesmo modelo. O
arquivo `.joblib` em si pode diferir byte a byte entre execuções (o pickle grava
metadado do ambiente), por isso o teste compara **coeficientes e previsões**, e
nunca o hash do arquivo.

Uso: python3 tools/exportar_modelo_aula12.py
     (requer pandas, numpy, scikit-learn e joblib, de requirements-ci.txt)
"""
import calendar
import os

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MENSAL = os.path.join(RAIZ, "dados", "mensal")
DESTINO = os.path.join(RAIZ, "app", "modelo_aula12.joblib")

SERIES = ["abate_bovinos", "abate_suinos", "abate_frangos",
          "producao_ovos", "producao_leite"]
ALVO = "abate_frangos"
FEATURES = (["lag1", "lag2", "lag3", "lag12", "sen", "cos", "dias"]
            + [s + "_lag1" for s in SERIES if s != ALVO])
N_TESTE = 24


def base_analitica():
    """A base analítica mensal das Aulas 07 a 11: 339 linhas, 315 de treino.

    Reimplementada aqui de propósito, como em `tools/graficos_aula11.py`: o
    acervo não tem pacote compartilhado, e cada artefato precisa poder ser lido
    sozinho.
    """
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


def novo_pipeline():
    """O Pipeline da aula: padronizar e ajustar, num objeto só."""
    return Pipeline([
        ("escala", StandardScaler()),
        ("modelo", LinearRegression()),
    ])


def pipeline_de_producao(base=None):
    """O Pipeline reajustado sobre a base completa, que é o que se exporta."""
    base = base_analitica() if base is None else base
    return novo_pipeline().fit(base[FEATURES].to_numpy(), base[ALVO].to_numpy())


def mape(real, previsto):
    return float(np.mean(np.abs((real - previsto) / real)) * 100)


def main():
    base = base_analitica()
    corte = len(base) - N_TESTE
    treino, teste = base.iloc[:corte], base.iloc[corte:]

    avaliado = novo_pipeline().fit(treino[FEATURES].to_numpy(), treino[ALVO].to_numpy())
    mape_avaliado = mape(teste[ALVO].to_numpy(), avaliado.predict(teste[FEATURES].to_numpy()))

    producao = pipeline_de_producao(base)

    os.makedirs(os.path.dirname(DESTINO), exist_ok=True)
    joblib.dump(producao, DESTINO)

    print("base            : %d linhas, de %s a %s"
          % (len(base), base["periodo"].iloc[0], base["periodo"].iloc[-1]))
    print("modelo avaliado : %d meses de treino, MAPE de %.4f%% nos %d meses de teste"
          % (len(treino), mape_avaliado, N_TESTE))
    print("modelo exportado: %d meses de treino, reajustado depois de a avaliação terminar"
          % len(base))
    print("destino         : %s (%d bytes)"
          % (os.path.relpath(DESTINO, RAIZ), os.path.getsize(DESTINO)))
    print()
    print("O MAPE de %.4f%% é o número que descreve o modelo exportado, e ele foi medido"
          % mape_avaliado)
    print("no objeto AVALIADO, não neste. Medir o modelo reajustado nos mesmos 24 meses")
    print("daria um número menor e sem sentido: ele treinou com esses meses.")


if __name__ == "__main__":
    main()

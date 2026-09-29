"""App Streamlit da Aula 14: histórico, previsão e cenários do abate de frangos.

Rodar a partir da raiz do repositório:

    python3 -m pip install -r app/requirements.txt
    streamlit run app/app.py

O app carrega o `Pipeline` exportado na Aula 12 (`app/modelo_aula12.joblib`) e
os CSVs mensais de `dados/mensal/`. Nenhuma conta é feita aqui: tudo sai de
`app/logica.py`, que é testado sem Streamlit em `tools/tests/test_app_aula14.py`.
Este arquivo só decide o que aparece na tela e em que ordem.

O Streamlit reexecuta este script inteiro, de cima para baixo, a cada clique.
Por isso o modelo e a base ficam em cache: sem `st.cache_resource` e
`st.cache_data`, cada movimento do controle de cenário releria os cinco CSVs e
o `.joblib` do disco.
"""
import os
import sys

import altair as alt
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import logica  # noqa: E402

# Cores da paleta Inteli da Graduação (assets/css/inteli-brand.css). O
# Streamlit não lê as custom properties do acervo, então elas vêm por valor.
ROXO = "#2e2640"      # --inteli-roxo: o valor medido pelo IBGE
CORAL = "#ff4545"     # --inteli-coral: a previsão do modelo
VERDE = "#89cea5"     # --inteli-verde: a previsão sob o cenário

st.set_page_config(page_title="Abate de frangos: histórico e previsão",
                   layout="wide")


@st.cache_resource
def modelo():
    return logica.carregar_pipeline()


@st.cache_data
def base():
    return logica.base_analitica()


@st.cache_data
def series():
    return logica.carregar_series()


@st.cache_data
def mape_honesto():
    return logica.mape_do_avaliado(base())


def grafico(tabela, cores, titulo_y="milhões de kg por mês"):
    """Linhas por mês com o eixo vertical fora do zero.

    `st.line_chart` resolve o caso mínimo, e é o que o deck mostra. Aqui ele foi
    trocado por Altair por um motivo medido: o eixo do `st.line_chart` começa em
    zero, e um erro de 2,86% em 1,2 bilhão de quilogramas vira uma linha só.
    """
    ordem = list(cores)
    return (alt.Chart(tabela)
            .mark_line(strokeWidth=3)
            .encode(
                x=alt.X("data:T", title=None, axis=alt.Axis(format="%m/%Y")),
                y=alt.Y("valor:Q", title=titulo_y, axis=alt.Axis(format="d"),
                        scale=alt.Scale(zero=False)),
                color=alt.Color("curva:N", title=None,
                                scale=alt.Scale(domain=ordem, range=[cores[c] for c in ordem]),
                                legend=alt.Legend(orient="top", labelFontSize=14)),
                strokeDash=alt.condition(alt.datum.curva == "Previsão sob o cenário",
                                         alt.value([6, 4]), alt.value([1, 0])),
            )
            .properties(height=320))


st.title("Abate de frangos: histórico e previsão")
st.caption("Módulo 03 IN, Aula 14. Dados: IBGE/SIDRA, Pesquisa Trimestral do Abate de "
           "Animais, séries mensais (tabelas 1092, 1093, 1094, 7524 e 1086, classificação "
           "c12716). Modelo: o Pipeline exportado na Aula 12, regressão linear sobre onze "
           "features.")

with st.sidebar:
    st.header("Controles")
    escolha = st.selectbox("Série", logica.SERIES, index=logica.SERIES.index(logica.ALVO),
                           format_func=lambda s: logica.NOMES[s])
    meses = st.slider("Meses de histórico no gráfico", min_value=24, max_value=120,
                      value=48, step=12)
    st.divider()
    st.subheader("Cenário")
    chave = st.selectbox("Entrada do cenário", list(logica.CENARIOS),
                         format_func=lambda c: logica.CENARIOS[c]["rotulo"],
                         disabled=escolha != logica.ALVO)
    choque = st.slider("Choque na entrada (%)", min_value=-20, max_value=20, value=0, step=1,
                       disabled=escolha != logica.ALVO)

if escolha != logica.ALVO:
    st.info("Histórico, sem previsão. O modelo da Aula 12 prevê só o abate de frangos: "
            "esta série entra nele só como entrada defasada de um mês.")
    recorte, titulo = logica.tabela_do_historico(series()[escolha], meses)
    st.altair_chart(grafico(recorte, {"Medido pelo IBGE": ROXO}, titulo),
                    width="stretch")
    st.stop()

pipe = modelo()
b = base()
proximo, valor_proximo = logica.prever_proximo_mes(pipe)

col1, col2, col3 = st.columns(3)
col1.metric("MAPE nos 24 meses de teste", logica.numero_br(mape_honesto()) + "%")
col1.caption("Medido no objeto avaliado, treinado em %d meses e testado nos %d que não viu."
             % (len(b) - logica.N_TESTE, logica.N_TESTE))
col2.metric("Meses de treino do modelo exportado", "%d" % len(b))
col2.caption("Reajustado sobre a base inteira, de %s a %s, depois de a avaliação terminar."
             % (b["periodo"].iloc[0], b["periodo"].iloc[-1]))
col3.metric("Previsão para %s" % proximo, logica.numero_br(valor_proximo / 1e9, 3) + " bi kg")
col3.caption("O único mês futuro que o modelo prevê só com dado já medido.")

tabela = logica.tabela_do_grafico(pipe, b, meses, chave, choque)
cores = {"Medido pelo IBGE": ROXO, "Previsão do modelo": CORAL}
if choque != 0:
    cores["Previsão sob o cenário"] = VERDE
st.altair_chart(grafico(tabela, cores), width="stretch")
st.caption("As 24 previsões são de um passo à frente: cada mês usa o abate real do mês "
           "anterior. O erro mês a mês do gráfico é do modelo exportado, que já viu esses "
           "meses, e por isso não é o número de desempenho, que está no alto da página.")

st.subheader("Cenário")
st.write("O cenário aplica um choque percentual a entradas que o modelo lê, nos 24 meses de "
         "teste, e recalcula a previsão. É uma análise de sensibilidade do modelo: ela não "
         "prevê o que aconteceria na economia.")
if choque == 0:
    st.write("Mova o controle de choque, na barra lateral, para recalcular a previsão.")
else:
    estab = logica.estabilidade_do_cenario(pipe, b, chave, choque)
    st.write("Efeito médio nas 24 previsões: **%s%%** no modelo exportado e **%s%%** no "
             "modelo avaliado." % (logica.numero_br(estab["exportado"], 3, sinal=True),
                                   logica.numero_br(estab["avaliado"], 3, sinal=True)))
    if not estab["mesmo_sinal"]:
        st.warning("Os dois ajustes do mesmo modelo dão efeitos de sinal oposto. Este cenário "
                   "lê um coeficiente isolado, que a Aula 12 mediu como instável, e não pode "
                   "ir para a apresentação como afirmação sobre o mundo.")

with st.expander("Entradas que o modelo não usa, e o que faltaria para usar"):
    for nome, motivo in logica.ENTRADAS_FORA_DO_MODELO.items():
        st.write("**%s**: %s" % (nome, motivo))

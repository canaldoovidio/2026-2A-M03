#!/usr/bin/env python3
"""
Baixa do SIDRA/IBGE as series de proteina animal do case da LDC, em duas
granularidades.

Roda uma vez e versiona o resultado. Os notebooks leem do CSV, nunca da rede:
a aula nao pode depender de o IBGE estar no ar.

As tabelas sao da Pesquisa Trimestral do IBGE, e trazem a classificacao
c12716 (Referencia temporal) com quatro categorias: "Total do trimestre",
"No 1o mes", "No 2o mes" e "No 3o mes". Ou seja, a mesma tabela publica o
trimestre e os tres meses dele.

  dados/         serie trimestral, periodo AAAA-TN. Usada pelas Aulas 01 a 06.
  dados/mensal/  serie mensal, periodo AAAA-MM. Usada da Aula 07 em diante.

A versao trimestral continua sendo gerada porque quatro aulas publicadas leem
dela e citam achados medidos nela. A decisao esta em docs/adrs/ADR-010, que
revisa parcialmente a ADR-003.

Uso:
    python3 tools/baixar_dados.py
"""
import csv
import json
import os
import sys
import urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(RAIZ, "dados")

# https://apisidra.ibge.gov.br/values/t/{tabela}/n1/all/v/{variavel}/p/all
URL = "https://apisidra.ibge.gov.br/values/t/%s/n1/all/v/%s/p/all"

# Mesma URL, pedindo as tres categorias mensais da classificacao c12716
# (Referencia temporal) em vez do "Total do trimestre" que o filtro de
# e_linha_total seleciona por omissao.
URL_MENSAL = ("https://apisidra.ibge.gov.br/values/t/%s/n1/all/v/%s/p/all"
              "/c12716/115233,115234,115235")

DESTINO_MENSAL = os.path.join(DESTINO, "mensal")

# Categorias de c12716 e a posicao do mes dentro do trimestre.
POSICAO_DO_MES = {"115233": 1, "115234": 2, "115235": 3}

# Tabelas do SIDRA (Pesquisa Trimestral do Abate de Animais / Producao de
# Ovos e Leite) citadas no TAPI da Louis Dreyfus Company. A variavel foi
# escolhida para pegar a serie fisica real (peso, quantidade), nunca
# percentuais nem numero de informantes, que a mesma tabela tambem devolve.
SERIES = [
    ("1092", "285", "abate_bovinos.csv"),   # peso total das carcacas de bovinos
    ("1093", "285", "abate_suinos.csv"),    # peso total das carcacas de suinos
    ("1094", "285", "abate_frangos.csv"),   # peso total das carcacas de frangos
    ("7524", "29", "producao_ovos.csv"),    # quantidade de ovos produzidos
    ("1086", "282", "producao_leite.csv"),  # leite cru adquirido
]

# Marcadores do IBGE para dado ausente ou suprimido
AUSENTES = {"...", "..", "-", "X", "*", ""}

# Nomes das dimensoes extras (tipo de rebanho, tipo de inspecao, referencia
# temporal) que cada tabela pode trazer alem do periodo. So a linha "Total"
# nessas dimensoes representa a serie agregada do trimestre inteiro; sem
# esse filtro o mesmo periodo aparece repetido em varios recortes.
CHAVES_DIMENSAO = ["D4N", "D5N", "D6N"]


def baixar(url):
    with urllib.request.urlopen(url, timeout=120) as resposta:
        return json.loads(resposta.read().decode("utf-8"))


def normalizar_periodo(codigo):
    """O SIDRA devolve AAAATT (202504 = 4o trimestre de 2025).
    O contrato do acervo e AAAA-TN, entao 202504 vira 2025-T4."""
    texto = str(codigo).strip()
    if len(texto) == 6 and texto.isdigit():
        return "%s-T%d" % (texto[:4], int(texto[4:]))
    return texto


def normalizar_periodo_mensal(codigo_trimestre, codigo_referencia):
    """Converte trimestre do SIDRA mais posicao do mes para AAAA-MM.

    O SIDRA devolve o trimestre como AAAATT (202601 = 1o trimestre de 2026) e
    a posicao do mes como categoria de c12716 (115233 = "No 1o mes"). O mes
    civil e (trimestre - 1) * 3 + posicao, entao 202601 com 115233 vira
    2026-01, e 202504 com 115235 vira 2025-12."""
    texto = str(codigo_trimestre).strip()
    trimestre = int(texto[4:])
    mes = (trimestre - 1) * 3 + POSICAO_DO_MES[str(codigo_referencia).strip()]
    return "%s-%02d" % (texto[:4], mes)


def converter(bruto):
    texto = str(bruto).strip()
    if texto in AUSENTES:
        return ""
    return str(float(texto.replace(",", ".")))


def e_linha_total(item):
    """So aceita a linha se todas as dimensoes extras (tipo de rebanho,
    tipo de inspecao, referencia temporal) estiverem marcadas como 'Total'.
    Isso evita que o mesmo trimestre apareca varias vezes com recortes
    diferentes (por Bois/Vacas, Federal/Estadual, por mes dentro do
    trimestre etc)."""
    for chave in CHAVES_DIMENSAO:
        valor = item.get(chave)
        if valor is not None and not valor.startswith("Total"):
            return False
    return True


def extrair_linhas(payload):
    """A primeira linha do JSON do SIDRA e o cabecalho com os rotulos.

    Depois do filtro de 'Total' (e_linha_total), cada periodo so pode
    aparecer uma vez. Se aparecer mais de uma, o filtro nao isolou um unico
    recorte e o CSV sairia com o mesmo trimestre repetido em cortes
    diferentes, silenciosamente errado. Isso precisa parar a geracao, nao
    virar um CSV plausivel e errado: por isso levanta erro em vez de
    descartar a duplicata em silencio."""
    cabecalho, *dados = payload
    unidade = cabecalho.get("MN", "") or cabecalho.get("MC", "")
    linhas_por_periodo = {}
    contagem = {}
    for item in dados:
        if not e_linha_total(item):
            continue
        periodo = normalizar_periodo(item.get("D3C") or item.get("D2C", ""))
        if not periodo:
            continue
        contagem[periodo] = contagem.get(periodo, 0) + 1
        linhas_por_periodo.setdefault(periodo, {
            "periodo": periodo,
            "valor": converter(item.get("V", "")),
            "unidade": item.get("MN", unidade),
        })

    duplicados = {p: n for p, n in contagem.items() if n > 1}
    if duplicados:
        detalhe = ", ".join(
            "%s (%d linhas)" % (p, n) for p, n in sorted(duplicados.items())
        )
        raise ValueError(
            "periodo duplicado apos o filtro de 'Total': %s. "
            "O filtro de dimensoes extras (e_linha_total) deixou passar mais "
            "de um recorte para o mesmo periodo; corrija o filtro antes de "
            "aceitar o CSV." % detalhe
        )

    linhas = list(linhas_por_periodo.values())
    linhas.sort(key=lambda l: l["periodo"])
    return linhas


def e_linha_total_mensal(item, chave_referencia):
    """Como e_linha_total, mas deixa passar a dimensao de referencia temporal.

    Sem essa excecao o filtro descartaria justamente as tres categorias
    mensais, porque nenhuma delas comeca com 'Total'."""
    for chave in CHAVES_DIMENSAO:
        if chave == chave_referencia:
            continue
        valor = item.get(chave)
        if valor is not None and not valor.startswith("Total"):
            return False
    return True


def extrair_linhas_mensais(payload):
    """Mesma logica de extrair_linhas, no eixo mensal.

    A chave da referencia temporal e descoberta pelo rotulo do cabecalho, e
    nao fixada em D5N, porque a tabela 1092 tem uma dimensao a mais (tipo de
    rebanho bovino) e a de ovos tem finalidade da producao: a posicao da
    coluna muda de tabela para tabela."""
    cabecalho, *dados = payload
    unidade = cabecalho.get("MN", "") or cabecalho.get("MC", "")

    chave_ref_nome = None
    for chave, rotulo in cabecalho.items():
        if rotulo.startswith("Referência temporal (Código)"):
            chave_ref_codigo = chave
            chave_ref_nome = chave[:-1] + "N"
    if chave_ref_nome is None:
        raise ValueError(
            "a tabela nao trouxe a classificacao c12716 (Referencia "
            "temporal); sem ela nao ha serie mensal para extrair")

    chave_periodo = None
    for chave, rotulo in cabecalho.items():
        if rotulo.startswith("Trimestre (Código)"):
            chave_periodo = chave
    if chave_periodo is None:
        raise ValueError("a tabela nao trouxe a coluna de trimestre")

    linhas_por_periodo = {}
    contagem = {}
    for item in dados:
        if not e_linha_total_mensal(item, chave_ref_nome):
            continue
        codigo_ref = item.get(chave_ref_codigo)
        if str(codigo_ref) not in POSICAO_DO_MES:
            continue
        periodo = normalizar_periodo_mensal(item.get(chave_periodo), codigo_ref)
        contagem[periodo] = contagem.get(periodo, 0) + 1
        linhas_por_periodo.setdefault(periodo, {
            "periodo": periodo,
            "valor": converter(item.get("V", "")),
            "unidade": item.get("MN", unidade),
        })

    duplicados = {p: n for p, n in contagem.items() if n > 1}
    if duplicados:
        detalhe = ", ".join(
            "%s (%d linhas)" % (p, n) for p, n in sorted(duplicados.items())
        )
        raise ValueError(
            "periodo duplicado apos o filtro de 'Total': %s. "
            "O filtro de dimensoes extras deixou passar mais de um recorte "
            "para o mesmo mes; corrija o filtro antes de aceitar o CSV."
            % detalhe
        )

    linhas = list(linhas_por_periodo.values())
    linhas.sort(key=lambda l: l["periodo"])
    return linhas


def _escrever(caminho, linhas):
    with open(caminho, "w", encoding="utf-8", newline="") as fh:
        escritor = csv.DictWriter(fh, fieldnames=["periodo", "valor", "unidade"])
        escritor.writeheader()
        escritor.writerows(linhas)
    print("  %d linhas, de %s a %s"
          % (len(linhas), linhas[0]["periodo"], linhas[-1]["periodo"]))


def main():
    os.makedirs(DESTINO, exist_ok=True)
    os.makedirs(DESTINO_MENSAL, exist_ok=True)
    for tabela, variavel, nome in SERIES:
        print("baixando tabela %s (variavel %s) para %s" % (tabela, variavel, nome))
        _escrever(os.path.join(DESTINO, nome),
                  extrair_linhas(baixar(URL % (tabela, variavel))))
        print("baixando tabela %s (variavel %s) para mensal/%s" % (tabela, variavel, nome))
        _escrever(os.path.join(DESTINO_MENSAL, nome),
                  extrair_linhas_mensais(baixar(URL_MENSAL % (tabela, variavel))))


if __name__ == "__main__":
    sys.exit(main())

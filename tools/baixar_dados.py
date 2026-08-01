#!/usr/bin/env python3
"""
Baixa do SIDRA/IBGE as series trimestrais de proteina animal do case da LDC.

Roda uma vez e versiona o resultado. Os notebooks leem do CSV, nunca da rede:
a aula nao pode depender de o IBGE estar no ar.

As tabelas sao da Pesquisa Trimestral do IBGE. O periodo vem da API como
AAAATT (por exemplo 202504 = quarto trimestre de 2025) e este script converte
para o contrato do acervo, AAAA-TN (2025-T4). Nao existe versao mensal dessas
series: o TAPI pede previsao mensal, mas o dado aberto so existe em base
trimestral. Essa diferenca esta registrada em dados/README.md.

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


def baixar(tabela, variavel):
    url = URL % (tabela, variavel)
    with urllib.request.urlopen(url, timeout=120) as resposta:
        return json.loads(resposta.read().decode("utf-8"))


def normalizar_periodo(codigo):
    """O SIDRA devolve AAAATT (202504 = 4o trimestre de 2025).
    O contrato do acervo e AAAA-TN, entao 202504 vira 2025-T4."""
    texto = str(codigo).strip()
    if len(texto) == 6 and texto.isdigit():
        return "%s-T%d" % (texto[:4], int(texto[4:]))
    return texto


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


def main():
    os.makedirs(DESTINO, exist_ok=True)
    for tabela, variavel, nome in SERIES:
        print("baixando tabela %s (variavel %s) para %s" % (tabela, variavel, nome))
        linhas = extrair_linhas(baixar(tabela, variavel))
        caminho = os.path.join(DESTINO, nome)
        with open(caminho, "w", encoding="utf-8", newline="") as fh:
            escritor = csv.DictWriter(fh, fieldnames=["periodo", "valor", "unidade"])
            escritor.writeheader()
            escritor.writerows(linhas)
        print("  %d linhas, de %s a %s"
              % (len(linhas), linhas[0]["periodo"], linhas[-1]["periodo"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())

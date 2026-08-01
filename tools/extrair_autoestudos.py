#!/usr/bin/env python3
"""
Extrai do Turma.xlsx os autoestudos e encontros do Prof. Ovidio, por semana.

O Turma.xlsx tem dado pessoal de aluno (nome, presenca, nota) e por isso nao e
versionado. Este script produz o derivado publicavel: so semana, tipo, titulo e
data de atividade.

Uso:
    python3 tools/extrair_autoestudos.py > docs/autoestudos-por-semana.md
"""
import datetime
import os
import sys

import openpyxl

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PADRAO = os.path.join(RAIZ, "Turma.xlsx")
PROFESSOR = "Ovidio"


def _data(valor):
    if isinstance(valor, datetime.datetime):
        return valor.strftime("%d/%m/%Y")
    return str(valor).strip() if valor else ""


def extrair(caminho_xlsx):
    wb = openpyxl.load_workbook(caminho_xlsx, data_only=True, read_only=True)
    linhas = wb.worksheets[0].iter_rows(values_only=True)
    cab = [str(c).strip() for c in next(linhas)]
    i = {nome: pos for pos, nome in enumerate(cab)}

    vistos = set()
    dados = {}
    for linha in linhas:
        if linha[0] is None:
            continue
        professor = str(linha[i["Atividade_Professor_Nome"]] or "")
        if PROFESSOR not in professor:
            continue

        semana = str(linha[i["Atividade_Semana"]] or "").strip()
        tipo = str(linha[i["Atividade_Tipo"]] or "").strip()
        titulo = str(linha[i["Atividade_Nome"]] or "").strip()
        data = _data(linha[i["Atividade_Data_Inicio"]])

        chave = (semana, tipo, titulo, data)
        if chave in vistos:
            continue
        vistos.add(chave)

        registro = dados.setdefault(semana, {"autoestudos": [], "encontros": []})
        if tipo == "Autoestudo":
            registro["autoestudos"].append(titulo)
        elif tipo == "Encontro de Instrução":
            registro["encontros"].append({"data": data, "titulo": titulo})

    for registro in dados.values():
        registro["autoestudos"].sort()
        registro["encontros"].sort(key=lambda e: _chave_data(e["data"]))
    return dict(sorted(dados.items()))


def _chave_data(texto):
    dia, mes, ano = texto.split("/")
    return (ano, mes, dia)


def renderizar(dados):
    linhas = [
        "# Autoestudos e encontros por semana",
        "",
        "Gerado por `tools/extrair_autoestudos.py` a partir do `Turma.xlsx`.",
        "Nao editar a mao: rodar o script de novo quando a Adalove mudar.",
        "",
        "As paginas de `referencias/` consomem este arquivo. Autoestudo que nao",
        "esta aqui nao entra na pagina de referencias da aula.",
        "",
    ]
    for semana, registro in dados.items():
        linhas.append("## %s" % semana)
        linhas.append("")
        if registro["encontros"]:
            linhas.append("**Encontros de Instrução**")
            linhas.append("")
            for enc in registro["encontros"]:
                linhas.append("- %s: %s" % (enc["data"], enc["titulo"]))
            linhas.append("")
        if registro["autoestudos"]:
            linhas.append("**Autoestudos**")
            linhas.append("")
            for titulo in registro["autoestudos"]:
                linhas.append("- %s" % titulo)
            linhas.append("")
    return "\n".join(linhas)


def main():
    caminho = sys.argv[1] if len(sys.argv) > 1 else PADRAO
    if not os.path.isfile(caminho):
        print("Turma.xlsx nao encontrado em %s" % caminho, file=sys.stderr)
        return 1
    print(renderizar(extrair(caminho)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

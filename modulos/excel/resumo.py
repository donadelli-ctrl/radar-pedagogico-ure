"""
==========================================================
RADAR PEDAGÓGICO URE
MÓDULO: resumo.py
Versão: 1.3
==========================================================

Responsabilidade:
Gerar a aba RESUMO EXECUTIVO.
"""

import pandas as pd

from modulos.excel.formatacao import (
    CABECALHO_FILL,
    CABECALHO_FONT,
    CENTRO,
    ESQUERDA,
)


# ==========================================================
# RESUMO EXECUTIVO
# ==========================================================

def criar_resumo(writer, indicadores):
    """
    Cria a aba RESUMO EXECUTIVO.
    """

    resumo = pd.DataFrame(
        {
            "Indicador": [
                "Data de geração",
                "Avaliações utilizadas",
                "Total de escolas",
                "Participação ADE",
                "Participação PP1",
                "Participação PP2",
                "Média PP1",
                "Média PP2",
                "Escolas Prioritárias",
                "Escolas em Atenção",
                "Escolas Destaque",
                "Escolas sem dados",
            ],
            "Valor": [
                indicadores["DATA_GERACAO"].strftime(
                    "%d/%m/%Y %H:%M"
                ),
                ", ".join(
                    indicadores["AVALIACOES"]
                ),
                indicadores["TOTAL_ESCOLAS"],
                indicadores.get("PART_ADE"),
                indicadores.get("PART_PP1"),
                indicadores.get("PART_PP2"),
                indicadores.get("MEDIA_PP1"),
                indicadores.get("MEDIA_PP2"),
                indicadores["PRIORITARIA"],
                indicadores["ATENCAO"],
                indicadores["DESTAQUE"],
                indicadores["SEM_DADOS"],
            ],
        }
    )

    resumo.to_excel(
        writer,
        sheet_name="RESUMO EXECUTIVO",
        index=False,
    )

    ws = writer.sheets[
        "RESUMO EXECUTIVO"
    ]

    # ======================================================
    # CABEÇALHO
    # ======================================================

    for cell in ws[1]:

        cell.fill = CABECALHO_FILL
        cell.font = CABECALHO_FONT
        cell.alignment = CENTRO

    # ======================================================
    # ALINHAMENTO
    # ======================================================

    for linha in ws.iter_rows(
        min_row=2
    ):

        linha[0].alignment = ESQUERDA
        linha[1].alignment = CENTRO

    # ======================================================
    # PERCENTUAIS
    # ======================================================

    percentuais = {

        "Participação ADE",
        "Participação PP1",
        "Participação PP2",
        "Média PP1",
        "Média PP2",

    }

    for row in range(
        2,
        ws.max_row + 1,
    ):

        indicador = ws.cell(
            row=row,
            column=1,
        ).value

        if indicador in percentuais:

            ws.cell(
                row=row,
                column=2,
            ).number_format = "0.0%"

    # ======================================================
    # LARGURA DAS COLUNAS
    # ======================================================

    ws.column_dimensions[
        "A"
    ].width = 35

    ws.column_dimensions[
        "B"
    ].width = 25

    # ======================================================
    # FINALIZAÇÃO
    # ======================================================

    ws.freeze_panes = "A2"

    ws.auto_filter.ref = ws.dimensions
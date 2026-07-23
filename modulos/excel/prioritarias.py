"""
==========================================================
RADAR PEDAGÓGICO URE
MÓDULO: prioritarias.py
Versão: 1.3
==========================================================

Responsabilidade:
Gerar a aba ESCOLAS PRIORITÁRIAS.
"""

import pandas as pd

from modulos.excel.formatacao import (
    formatar_planilha,
)


# ==========================================================
# ESCOLAS PRIORITÁRIAS
# ==========================================================

def criar_prioritarias(writer, df: pd.DataFrame):
    """
    Cria a aba ESCOLAS PRIORITÁRIAS.
    """

    if df.empty:
        return

    if "SITUACAO" not in df.columns:
        return

    df_prioritarias = df[
        df["SITUACAO"]
        .astype(str)
        .str.contains(
            "PRIORIT",
            case=False,
            na=False,
        )
    ].copy()

    if df_prioritarias.empty:
        return

    # ------------------------------------------------------
    # Ordenação
    # ------------------------------------------------------

    colunas = []

    if "MEDIA_PP2" in df_prioritarias.columns:
        colunas.append("MEDIA_PP2")

    if "PART_PP2" in df_prioritarias.columns:
        colunas.append("PART_PP2")

    if "ESCOLA" in df_prioritarias.columns:
        colunas.append("ESCOLA")

    if colunas:

        df_prioritarias.sort_values(
            by=colunas,
            ascending=True,
            inplace=True,
        )

    # ------------------------------------------------------
    # Exportação
    # ------------------------------------------------------

    df_prioritarias.to_excel(
        writer,
        sheet_name="ESCOLAS PRIORITÁRIAS",
        index=False,
    )

    ws = writer.sheets[
        "ESCOLAS PRIORITÁRIAS"
    ]

    formatar_planilha(ws)
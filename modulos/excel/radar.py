"""
==========================================================
RADAR PEDAGÓGICO URE
MÓDULO: radar.py
Versão: 1.3
==========================================================

Responsabilidade:
Gerar a aba RADAR PEDAGÓGICO.
"""

import pandas as pd

from modulos.excel.formatacao import (
    formatar_planilha,
)


# ==========================================================
# RADAR PEDAGÓGICO
# ==========================================================

def criar_radar(writer, df):
    """
    Cria a aba RADAR PEDAGÓGICO.
    """

    if df.empty:
        return

    # ------------------------------------------------------
    # TESTE TEMPORÁRIO
    # ------------------------------------------------------

    # ------------------------------------------------------
    # EXPORTAÇÃO
    # ------------------------------------------------------

    df.to_excel(
        writer,
        sheet_name="RADAR PEDAGÓGICO",
        index=False,
    )

    ws = writer.sheets[
        "RADAR PEDAGÓGICO"
    ]

    formatar_planilha(ws)
"""
==========================================================
RADAR PEDAGÓGICO URE
MÓDULO: excel_final.py
Versão: 1.3
==========================================================

Responsabilidade:
Gerar o arquivo Excel do Radar Pedagógico.
"""

from io import BytesIO

import pandas as pd

from modulos.indicadores import calcular_indicadores

from modulos.excel.resumo import criar_resumo
from modulos.excel.radar import criar_radar
from modulos.excel.prioritarias import criar_prioritarias


# ==========================================================
# GERA EXCEL
# ==========================================================

def gerar_excel(df: pd.DataFrame) -> BytesIO:
    """
    Gera o arquivo Excel do Radar Pedagógico.
    """

    if df.empty:

        raise ValueError(
            "O DataFrame consolidado está vazio."
        )

    indicadores = calcular_indicadores(df)

    buffer = BytesIO()

    with pd.ExcelWriter(
        buffer,
        engine="openpyxl",
    ) as writer:

        criar_resumo(
            writer,
            indicadores,
        )

        criar_radar(
            writer,
            df,
        )

        criar_prioritarias(
            writer,
            df,
        )

    buffer.seek(0)

    return buffer
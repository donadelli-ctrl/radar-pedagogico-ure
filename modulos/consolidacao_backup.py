"""
==========================================================
RADAR PEDAGÓGICO URE
Módulo: consolidacao.py
==========================================================

Responsabilidade:
Consolidar todas as avaliações em uma única base.

Autor:
Projeto Radar Pedagógico URE
"""

import pandas as pd


# ==========================================================
# CONSOLIDAÇÃO
# ==========================================================

def consolidar_base(
    df_ADE,
    df_PP1=None,
    df_PP2=None,
    df_ADP=None,
    df_PP3=None,
):
    """
    Consolida todas as avaliações utilizando
    o nome da escola como chave.
    """

    if df_ADE is None:
        raise ValueError("A base ADE é obrigatória.")

    base = df_ADE.copy()

    arquivos = [
        df_PP1,
        df_PP2,
        df_ADP,
        df_PP3,
    ]

    for arquivo in arquivos:

        if arquivo is None:
            continue

        base = base.merge(
            arquivo,
            on="ESCOLA",
            how="left",
        )

    # ------------------------------------------------------
    # Organização das colunas
    # ------------------------------------------------------

    if "CIE" in base.columns:

        base = base.sort_values(
            by=["CIE", "ESCOLA"]
        )

    else:

        base = base.sort_values(
            by="ESCOLA"
        )

    base.reset_index(
        drop=True,
        inplace=True,
    )

    return base
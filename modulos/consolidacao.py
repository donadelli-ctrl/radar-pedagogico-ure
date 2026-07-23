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

from modulos.criterios import classificar_escola


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
    a ESCOLA como chave.
    """

    if df_ADE is None or df_ADE.empty:
        raise ValueError("A base ADE é obrigatória.")

    # Base principal
    base = df_ADE.copy()

    # Lista das avaliações
    avaliacoes = [
        df_PP1,
        df_PP2,
        df_ADP,
        df_PP3,
    ]

    # Faz o merge de cada avaliação
    for avaliacao in avaliacoes:

        if avaliacao is None:
            continue

        if avaliacao.empty:
            continue

        base = base.merge(
            avaliacao,
            on="ESCOLA",
            how="left",
        )

    # Ordenação
    if "ESCOLA" in base.columns:

        base.sort_values(
            by="ESCOLA",
            inplace=True,
        )

        base.reset_index(
            drop=True,
            inplace=True,
        )

        # ======================================================
        # SITUAÇÃO DA ESCOLA
        # ======================================================

        base["SITUACAO"] = base.apply(
            classificar_escola,
            axis=1,
            
        )    

    return base
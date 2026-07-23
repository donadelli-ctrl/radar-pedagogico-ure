"""
==========================================================
RADAR PEDAGÓGICO URE
Módulo: indicadores.py
Versão: 1.1
==========================================================

Responsabilidade:
Calcular os principais indicadores da URE.
"""

from datetime import datetime

import pandas as pd


# ==========================================================
# INDICADORES GERAIS
# ==========================================================

def calcular_indicadores(base: pd.DataFrame) -> dict:
    """
    Calcula os indicadores gerais da URE.

    Retorna um dicionário com todos os indicadores
    necessários para o Resumo Executivo.
    """

    indicadores = {}

    # ======================================================
    # INFORMAÇÕES GERAIS
    # ======================================================

    indicadores["DATA_GERACAO"] = datetime.now()

    indicadores["TOTAL_ESCOLAS"] = len(base)

    # ======================================================
    # AVALIAÇÕES DISPONÍVEIS
    # ======================================================

    avaliacoes = []

    for avaliacao in [
        "ADE",
        "PP1",
        "PP2",
        "ADP",
        "PP3",
    ]:

        coluna = f"PART_{avaliacao}"

        if coluna in base.columns:

            if base[coluna].notna().any():

                avaliacoes.append(avaliacao)

    indicadores["AVALIACOES"] = avaliacoes

    # ======================================================
    # PARTICIPAÇÃO MÉDIA
    # ======================================================

    for coluna in [

        "PART_ADE",
        "PART_PP1",
        "PART_PP2",
        "PART_ADP",
        "PART_PP3",

    ]:

        if coluna in base.columns:

            indicadores[coluna] = base[coluna].mean()

    # ======================================================
    # MÉDIAS GERAIS
    # ======================================================

    for coluna in [

        "MEDIA_PP1",
        "MEDIA_PP2",
        "MEDIA_ADP",
        "MEDIA_PP3",

    ]:

        if coluna in base.columns:

            indicadores[coluna] = base[coluna].mean()

    # ======================================================
    # SITUAÇÃO DAS ESCOLAS
    # ======================================================

    indicadores["PRIORITARIA"] = 0
    indicadores["ATENCAO"] = 0
    indicadores["DESTAQUE"] = 0
    indicadores["SEM_DADOS"] = 0

    if "SITUACAO" in base.columns:

        indicadores["PRIORITARIA"] = (
            base["SITUACAO"]
            .eq("PRIORITÁRIA")
            .sum()
        )

        indicadores["ATENCAO"] = (
            base["SITUACAO"]
            .eq("ATENÇÃO")
            .sum()
        )

        indicadores["DESTAQUE"] = (
            base["SITUACAO"]
            .eq("DESTAQUE")
            .sum()
        )

        indicadores["SEM_DADOS"] = (
            base["SITUACAO"]
            .eq("SEM DADOS")
            .sum()
        )

    # ======================================================
    # RETORNO
    # ======================================================

    return indicadores
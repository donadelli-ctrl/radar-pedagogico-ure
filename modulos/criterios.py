"""
==========================================================
RADAR PEDAGÓGICO URE
Módulo: criterios.py
==========================================================

Responsabilidade:
Classificar a situação pedagógica das escolas.
"""

import pandas as pd


# ==========================================================
# CLASSIFICAÇÃO
# ==========================================================

def classificar_escola(linha):
    """
    Classifica a escola em:

    - PRIORITÁRIA
    - ATENÇÃO
    - DESTAQUE
    """

    participacao = linha.get("PART_PP2")

    media = linha.get("MEDIA_PP2")

    # Caso ainda não exista PP2,
    # utiliza PP1

    if pd.isna(participacao):

        participacao = linha.get("PART_PP1")

    if pd.isna(media):

        media = linha.get("MEDIA_PP1")

    if pd.isna(participacao) or pd.isna(media):
        return "SEM DADOS"

    if participacao < 0.80 or media < 0.40:
        return "PRIORITÁRIA"

    if participacao < 0.90 or media < 0.60:
        return "ATENÇÃO"

    return "DESTAQUE"
# ==========================================================
# RADAR PEDAGÓGICO URE
# MÓDULO: leitor_pp.py
# ==========================================================

import pandas as pd


# ==========================================================
# LEITOR PP
# ==========================================================

def ler_PP(arquivo, avaliacao):

    """
    Lê os arquivos PP1, PP2, ADP e PP3
    da URE e devolve uma base padronizada.
    """

    df = pd.read_excel(arquivo)

    # ------------------------------------------------------
    # LIMPEZA DOS NOMES DAS COLUNAS
    # ------------------------------------------------------

    df.columns = [

        str(coluna).strip()

        for coluna in df.columns

    ]

    # ======================================================
    # BASE PADRONIZADA
    # ======================================================

    base = pd.DataFrame()

    # ------------------------------------------------------
    # IDENTIFICAÇÃO
    # ------------------------------------------------------

    base["CIE"] = df["CIE"]

    base["ESCOLA"] = df["ESCOLA"]

    # ------------------------------------------------------
    # TOTAL DE ESTUDANTES
    # ------------------------------------------------------

    base["TOTAL_ALUNOS"] = pd.to_numeric(

        df["Total Alunos"],

        errors="coerce"

    )

    # ------------------------------------------------------
    # PARTICIPAÇÃO
    # ------------------------------------------------------

    base[f"PART_{avaliacao}"] = pd.to_numeric(

        df["(%) de Participação"],

        errors="coerce"

    )

    # ------------------------------------------------------
    # MÉDIA GERAL
    # ------------------------------------------------------

    base[f"MEDIA_{avaliacao}"] = pd.to_numeric(

        df["(%) de Acertos"],

        errors="coerce"

    )

    # ------------------------------------------------------
    # PORTUGUÊS
    # ------------------------------------------------------

    base[f"PORT_{avaliacao}"] = pd.to_numeric(

        df["PORT"],

        errors="coerce"

    )

    # ------------------------------------------------------
    # MATEMÁTICA
    # ------------------------------------------------------

    base[f"MAT_{avaliacao}"] = pd.to_numeric(

        df["MAT"],

        errors="coerce"

    )

    return base
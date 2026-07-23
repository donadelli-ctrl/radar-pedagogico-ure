"""
==========================================================
RADAR PEDAGÓGICO URE
Módulo: leitor_ade.py
==========================================================

Responsabilidade:
Ler a planilha ADE e devolver um DataFrame padronizado.
"""

import pandas as pd

from modulos.utils import (
    localizar_coluna,
    padronizar_escola,
    converter_numero,
    validar_colunas,
)


# ==========================================================
# LEITURA DA ADE
# ==========================================================

def ler_ADE(arquivo):
    """
    Lê a planilha ADE e devolve um DataFrame padronizado.
    """

    # ------------------------------------------------------
    # Leitura da planilha
    # ------------------------------------------------------

    df = pd.read_excel(arquivo)

    print("\n===== ADE ORIGINAL =====")
    print(df.head(10))
    print("========================\n")

    df.columns = [str(col).strip() for col in df.columns]

    # ------------------------------------------------------
    # Validação
    # ------------------------------------------------------

    validar_colunas(
        df,
        [
            "CIE",
            "ESCOLA",
            "PARTICIPACAO",
        ],
    )

    # ------------------------------------------------------
    # Localiza colunas principais
    # ------------------------------------------------------

    col_cie = localizar_coluna(df, ["CIE"])

    col_escola = localizar_coluna(
        df,
        ["ESCOLA"],
    )

    col_part = localizar_coluna(
        df,
        [
            "PARTICIPACAO",
            "PARTICIPAÇÃO",
        ],
    )

    # ------------------------------------------------------
    # Monta a base
    # ------------------------------------------------------

    base = pd.DataFrame()

    base["CIE"] = (
        pd.to_numeric(
            df[col_cie],
            errors="coerce",
        )
        .astype("Int64")
    )

    base["ESCOLA"] = (
        df[col_escola]
        .apply(padronizar_escola)
    )

    base["PART_ADE"] = (
        df[col_part]
        .apply(converter_numero)
    )

    # ------------------------------------------------------
    # Língua Portuguesa
    # ------------------------------------------------------

    base["LP_ABAIXO"] = (
        df.iloc[:, 3]
        .apply(converter_numero)
    )

    base["LP_BASICO"] = (
        df.iloc[:, 4]
        .apply(converter_numero)
    )

    base["LP_PROFICIENTE"] = (
        df.iloc[:, 5]
        .apply(converter_numero)
    )

    # ------------------------------------------------------
    # Matemática
    # ------------------------------------------------------

    base["MAT_ABAIXO"] = (
        df.iloc[:, 6]
        .apply(converter_numero)
    )

    base["MAT_BASICO"] = (
        df.iloc[:, 7]
        .apply(converter_numero)
    )

    base["MAT_PROFICIENTE"] = (
        df.iloc[:, 8]
        .apply(converter_numero)
    )

    # ------------------------------------------------------
    # Remove linhas sem escola
    # ------------------------------------------------------

    # ------------------------------------------------------
    # Remove linhas inválidas
    # ------------------------------------------------------

    # Remove espaços
    base["ESCOLA"] = (
        base["ESCOLA"]
        .astype(str)
        .str.strip()
    )

    # Remove textos que representam vazio
    base = base[
        ~base["ESCOLA"].isin(
            [
                "",
                "NAN",
                "NONE",
                "<NA>",
            ]
        )
    ]

    # Remove registros sem CIE
    base = base[
        base["CIE"].notna()
    ]

    # Reinicia o índice
    base.reset_index(
        drop=True,
        inplace=True,
    )

    return base
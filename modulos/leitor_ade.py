"""
Responsabilidade:
Ler a planilha ADE e devolver um DataFrame padronizado.
"""

import pandas as pd

from modulos.utils import (
    localizar_coluna,
    padronizar_escola,
    converter_numero,
    validar_colunas,
    padronizar_texto,
)


# ==========================================================
# LOCALIZAÇÃO DAS COLUNAS ADE
# ==========================================================

def _localizar_colunas_nivel(df, nome_base):
    """
    Localiza as duas ocorrências de uma coluna da ADE.

    A estrutura atual da ADE possui:

        Abaixo do Básico
        Básico
        Proficiente

        Abaixo do Básico.1
        Básico.1
        Proficiente.1

    O primeiro conjunto corresponde a LP.
    O segundo conjunto corresponde a MAT.
    """

    resultado = []

    nome_padrao = padronizar_texto(nome_base)

    for coluna in df.columns:

        coluna_padrao = padronizar_texto(coluna)

        if coluna_padrao == nome_padrao:
            resultado.append(coluna)
            continue

        if coluna_padrao.startswith(nome_padrao + "."):
            resultado.append(coluna)

    return resultado


# ==========================================================
# LEITURA DA ADE
# ==========================================================

def ler_ADE(arquivo):
    """
    Lê a planilha ADE e devolve um DataFrame padronizado.

    Retorno:

        CIE
        ESCOLA
        PART_ADE

        LP_ABAIXO
        LP_BASICO
        LP_PROFICIENTE

        MAT_ABAIXO
        MAT_BASICO
        MAT_PROFICIENTE
    """

    # ------------------------------------------------------
    # Leitura da planilha
    # ------------------------------------------------------

    df = pd.read_excel(arquivo)

    # Padroniza apenas os nomes das colunas
    df.columns = [
        str(coluna).strip()
        for coluna in df.columns
    ]

    # ------------------------------------------------------
    # Validação das colunas principais
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
    # Localiza as colunas principais
    # ------------------------------------------------------

    col_cie = localizar_coluna(
        df,
        ["CIE"],
    )

    col_escola = localizar_coluna(
        df,
        ["ESCOLA"],
    )

    col_part = localizar_coluna(
        df,
        [
            "PARTICIPACAO",
            "PARTICIPAÇÃO",
            "(%) PARTICIPACAO",
            "(%) PARTICIPAÇÃO",
        ],
    )

    # ------------------------------------------------------
    # Localiza os dois conjuntos de níveis
    # ------------------------------------------------------

    col_ab = _localizar_colunas_nivel(
        df,
        "ABAIXO DO BÁSICO",
    )

    col_bas = _localizar_colunas_nivel(
        df,
        "BÁSICO",
    )

    col_prof = _localizar_colunas_nivel(
        df,
        "PROFICIENTE",
    )

    # ------------------------------------------------------
    # Validação da estrutura da ADE
    # ------------------------------------------------------

    if len(col_ab) < 2:
        raise ValueError(
            "A ADE não apresentou as duas colunas "
            "esperadas para 'Abaixo do Básico'."
        )

    if len(col_bas) < 2:
        raise ValueError(
            "A ADE não apresentou as duas colunas "
            "esperadas para 'Básico'."
        )

    if len(col_prof) < 2:
        raise ValueError(
            "A ADE não apresentou as duas colunas "
            "esperadas para 'Proficiente'."
        )

    # ------------------------------------------------------
    # Monta a base padronizada
    # ------------------------------------------------------

    base = pd.DataFrame()

    # ------------------------------------------------------
    # CIE
    # ------------------------------------------------------

    base["CIE"] = (
        pd.to_numeric(
            df[col_cie],
            errors="coerce",
        )
        .astype("Int64")
    )

    # ------------------------------------------------------
    # ESCOLA
    # ------------------------------------------------------

    base["ESCOLA"] = (
        df[col_escola]
        .apply(padronizar_escola)
    )

    # ------------------------------------------------------
    # PARTICIPAÇÃO
    # ------------------------------------------------------

    base["PART_ADE"] = (
        df[col_part]
        .apply(converter_numero)
    )

    # ------------------------------------------------------
    # LÍNGUA PORTUGUESA
    #
    # Primeiro conjunto encontrado na ADE
    # ------------------------------------------------------

    base["LP_ABAIXO"] = (
        df[col_ab[0]]
        .apply(converter_numero)
    )

    base["LP_BASICO"] = (
        df[col_bas[0]]
        .apply(converter_numero)
    )

    base["LP_PROFICIENTE"] = (
        df[col_prof[0]]
        .apply(converter_numero)
    )

    # ------------------------------------------------------
    # MATEMÁTICA
    #
    # Segundo conjunto encontrado na ADE
    # ------------------------------------------------------

    base["MAT_ABAIXO"] = (
        df[col_ab[1]]
        .apply(converter_numero)
    )

    base["MAT_BASICO"] = (
        df[col_bas[1]]
        .apply(converter_numero)
    )

    base["MAT_PROFICIENTE"] = (
        df[col_prof[1]]
        .apply(converter_numero)
    )

    # ------------------------------------------------------
    # LIMPEZA DOS REGISTROS
    # ------------------------------------------------------

    base["ESCOLA"] = (
        base["ESCOLA"]
        .astype(str)
        .str.strip()
    )

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

    # ------------------------------------------------------
    # Mantém somente registros com CIE válido
    # ------------------------------------------------------

    base = base[
        base["CIE"].notna()
    ]

    # ------------------------------------------------------
    # Remove duplicidades de escola/CIE
    # ------------------------------------------------------

    base = (
        base
        .drop_duplicates(
            subset=["CIE"],
            keep="first",
        )
    )

    # ------------------------------------------------------
    # Reinicia o índice
    # ------------------------------------------------------

    base.reset_index(
        drop=True,
        inplace=True,
    )

    return base
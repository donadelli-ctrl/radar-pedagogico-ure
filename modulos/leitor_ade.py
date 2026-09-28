"""
Responsabilidade:
Ler as planilhas ADE / 2ª AVD (ADP) e devolver
um DataFrame padronizado.

Estrutura das avaliações:

    Participação
    3 indicadores de LP
    3 indicadores de MAT

A primeira ocorrência dos níveis corresponde a LP.
A segunda ocorrência corresponde a MAT.

A identificação da escola ocorre pelo CIE.

Na 2ª AVD/ADP, o CIE pode estar no final do nome:

    NOME DA ESCOLA - 123456
"""

import re
import pandas as pd

from modulos.utils import (
    localizar_coluna,
    padronizar_escola,
    converter_numero,
    padronizar_texto,
)


# ==========================================================
# LOCALIZAÇÃO DAS COLUNAS DE NÍVEL
# ==========================================================

def _localizar_colunas_nivel(df, nome_base):

    resultado = []

    nome_padrao = padronizar_texto(
        nome_base
    )

    for coluna in df.columns:

        coluna_padrao = padronizar_texto(
            coluna
        )

        if coluna_padrao == nome_padrao:

            resultado.append(
                coluna
            )

            continue

        if coluna_padrao.startswith(
            nome_padrao + "."
        ):

            resultado.append(
                coluna
            )

    return resultado


# ==========================================================
# LOCALIZAÇÃO DA ESCOLA
# ==========================================================

def _localizar_escola(df):

    return localizar_coluna(
        df,
        [
            "ESCOLA",
            "Escola",
        ],
    )


# ==========================================================
# LOCALIZAÇÃO DA PARTICIPAÇÃO
# ==========================================================

def _localizar_participacao(df):

    candidatos = [

        "PARTICIPACAO",

        "PARTICIPAÇÃO",

        "(%) PARTICIPACAO",

        "(%) PARTICIPAÇÃO",

        "% PARTICIPACAO",

        "% PARTICIPAÇÃO",

    ]

    try:

        return localizar_coluna(
            df,
            candidatos,
        )

    except Exception:

        candidatos_normalizados = {
            padronizar_texto(
                candidato
            )
            for candidato in candidatos
        }

        for coluna in df.columns:

            if (
                padronizar_texto(
                    coluna
                )
                in candidatos_normalizados
            ):

                return coluna

    raise ValueError(
        "Coluna de participação não localizada."
    )


# ==========================================================
# LOCALIZAÇÃO DO CIE
# ==========================================================

def _localizar_cie(df):

    try:

        return localizar_coluna(
            df,
            ["CIE"],
        )

    except Exception:

        return None


# ==========================================================
# EXTRAÇÃO DO CIE
# ==========================================================

def _extrair_cie_da_escola(valor):

    if pd.isna(valor):

        return pd.NA

    texto = str(
        valor
    ).strip()

    # ------------------------------------------------------
    # Formato esperado:
    #
    # NOME DA ESCOLA - 123456
    # ------------------------------------------------------

    encontrado = re.search(
        r"-\s*(\d+)\s*$",
        texto,
    )

    if encontrado:

        return int(
            encontrado.group(1)
        )

    return pd.NA


# ==========================================================
# LEITURA DA ADE / ADP
# ==========================================================

def ler_ADE(arquivo):

    # ======================================================
    # LEITURA
    # ======================================================

    df = pd.read_excel(
        arquivo
    )

    df.columns = [
        str(coluna).strip()
        for coluna in df.columns
    ]


    # ======================================================
    # LOCALIZAÇÃO DAS COLUNAS
    # ======================================================

    col_escola = _localizar_escola(
        df
    )

    col_part = _localizar_participacao(
        df
    )

    col_cie = _localizar_cie(
        df
    )


    # ======================================================
    # NÍVEIS
    # ======================================================

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


    # ======================================================
    # VALIDAÇÃO
    # ======================================================

    if len(col_ab) < 2:

        raise ValueError(
            "A avaliação não apresentou as duas "
            "colunas de Abaixo do Básico."
        )


    if len(col_bas) < 2:

        raise ValueError(
            "A avaliação não apresentou as duas "
            "colunas de Básico."
        )


    if len(col_prof) < 2:

        raise ValueError(
            "A avaliação não apresentou as duas "
            "colunas de Proficiente."
        )


    # ======================================================
    # BASE
    # ======================================================

    base = pd.DataFrame()


    # ======================================================
    # CIE
    # ======================================================

    if col_cie is not None:

        base["CIE"] = pd.to_numeric(
            df[col_cie],
            errors="coerce",
        )

    else:

        base["CIE"] = (
            df[col_escola]
            .apply(
                _extrair_cie_da_escola
            )
        )

        base["CIE"] = pd.to_numeric(
            base["CIE"],
            errors="coerce",
        )


    # ======================================================
    # ESCOLA
    # ======================================================

    base["ESCOLA"] = (
        df[col_escola]
        .apply(
            padronizar_escola
        )
        .astype("string")
        .str.strip()
    )


    # ======================================================
    # PARTICIPAÇÃO
    # ======================================================

    base["PART_ADE"] = (
        df[col_part]
        .apply(
            converter_numero
        )
    )


    # ======================================================
    # LÍNGUA PORTUGUESA
    # ======================================================

    base["LP_ABAIXO"] = (
        df[col_ab[0]]
        .apply(
            converter_numero
        )
    )

    base["LP_BASICO"] = (
        df[col_bas[0]]
        .apply(
            converter_numero
        )
    )

    base["LP_PROFICIENTE"] = (
        df[col_prof[0]]
        .apply(
            converter_numero
        )
    )


    # ======================================================
    # MATEMÁTICA
    # ======================================================

    base["MAT_ABAIXO"] = (
        df[col_ab[1]]
        .apply(
            converter_numero
        )
    )

    base["MAT_BASICO"] = (
        df[col_bas[1]]
        .apply(
            converter_numero
        )
    )

    base["MAT_PROFICIENTE"] = (
        df[col_prof[1]]
        .apply(
            converter_numero
        )
    )


    # ======================================================
    # REMOVE LINHAS INVÁLIDAS
    # ======================================================

    base = base[
        base["ESCOLA"].notna()
    ]


    base = base[
        ~base["ESCOLA"]
        .astype(str)
        .str.upper()
        .isin(
            [
                "",
                "NAN",
                "NONE",
                "<NA>",
            ]
        )
    ]


    # ======================================================
    # REMOVE LINHA TÉCNICA
    # ======================================================

    base = base[
        ~base["ESCOLA"]
        .astype(str)
        .str.upper()
        .str.startswith(
            "FILTROS APLICADOS"
        )
    ]


    # ======================================================
    # IDENTIFICAÇÃO
    #
    # IMPORTANTE:
    #
    # Se houver CIE, ele será a identificação principal.
    #
    # A escola é utilizada apenas como apoio quando
    # não houver CIE.
    # ======================================================

    base["CHAVE_ESCOLA"] = (
        base["CIE"]
        .map(
            lambda valor:
                (
                    pd.NA
                    if pd.isna(valor)
                    else str(
                        int(valor)
                    )
                )
        )
        .astype("string")
    )


    # ======================================================
    # ESCOLAS SEM CIE
    # ======================================================

    sem_cie = (
        base["CHAVE_ESCOLA"]
        .isna()
    )


    base.loc[
        sem_cie,
        "CHAVE_ESCOLA",
    ] = (
        "ESCOLA_"
        +
        base.loc[
            sem_cie,
            "ESCOLA",
        ]
        .astype("string")
        .str.strip()
    )


    # ======================================================
    # REMOVE DUPLICIDADES
    #
    # O CIE é a identificação principal.
    # ======================================================

    base = (
        base
        .drop_duplicates(
            subset=[
                "CHAVE_ESCOLA"
            ],
            keep="first",
        )
    )


    # ======================================================
    # ORGANIZAÇÃO FINAL
    # ======================================================

    base.reset_index(
        drop=True,
        inplace=True,
    )


    return base
"""
Responsabilidade:
Consolidar todas as avaliações em uma única base.

Autor:
Projeto Radar Pedagógico URE
"""

import pandas as pd


# ==========================================================
# PREPARAÇÃO DE UMA AVALIAÇÃO
# ==========================================================

def _preparar_avaliacao(df, avaliacao):
    """
    Prepara uma avaliação para a consolidação.

    Cria uma chave única de identificação:

        CIE, quando disponível;
        ESCOLA, quando o CIE não estiver disponível.

    Retorna:
        CHAVE_ESCOLA
        CIE
        ESCOLA
        indicadores da avaliação
    """

    if df is None or df.empty:
        return None

    base = df.copy()

    avaliacao = str(avaliacao).strip().upper()

    # ------------------------------------------------------
    # Garantia das colunas de identificação
    # ------------------------------------------------------

    if "CIE" not in base.columns:
        base["CIE"] = pd.NA

    if "ESCOLA" not in base.columns:
        raise ValueError(
            f"A avaliação {avaliacao} não possui a coluna ESCOLA."
        )

    # ------------------------------------------------------
    # Normalização do CIE
    # ------------------------------------------------------

    base["CIE"] = pd.to_numeric(
        base["CIE"],
        errors="coerce",
    ).astype("Int64")

    # ------------------------------------------------------
    # Normalização da escola
    # ------------------------------------------------------

    base["ESCOLA"] = (
        base["ESCOLA"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # ------------------------------------------------------
    # Cria chave de consolidação
    #
    # CIE é a identificação principal.
    # Quando não houver CIE, utiliza ESCOLA.
    # ------------------------------------------------------

    base["CHAVE_ESCOLA"] = (
        base["CIE"]
        .astype("string")
    )

    base.loc[
        base["CIE"].isna(),
        "CHAVE_ESCOLA",
    ] = (
        "ESCOLA_"
        + base.loc[
            base["CIE"].isna(),
            "ESCOLA",
        ]
    )

    # ------------------------------------------------------
    # Remove possíveis duplicidades
    # ------------------------------------------------------

    base = (
        base
        .drop_duplicates(
            subset=["CHAVE_ESCOLA"],
            keep="first",
        )
    )

    # ------------------------------------------------------
    # Retorna base preparada
    # ------------------------------------------------------

    return base


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
    Consolida todas as avaliações em uma única base.

    A consolidação utiliza todas as escolas encontradas
    nas avaliações.

    Ordem:

        ADE
        PP1
        PP2
        ADP
        PP3

    A base NÃO fica limitada às escolas da ADE.

    Escolas novas encontradas posteriormente também
    são incorporadas.

    O CIE é a identificação principal.
    Quando o CIE não estiver disponível, a escola
    é utilizada como chave auxiliar.

    O cálculo do Farol, diagnóstico e encaminhamento
    NÃO ocorre nesta etapa.
    """

    avaliacoes = [
        ("ADE", df_ADE),
        ("PP1", df_PP1),
        ("PP2", df_PP2),
        ("ADP", df_ADP),
        ("PP3", df_PP3),
    ]

    bases_validas = []

    # ------------------------------------------------------
    # Prepara cada avaliação
    # ------------------------------------------------------

    for nome, dataframe in avaliacoes:

        if dataframe is None:
            continue

        if dataframe.empty:
            continue

        preparada = _preparar_avaliacao(
            dataframe,
            nome,
        )

        if preparada is not None:
            bases_validas.append(
                (nome, preparada)
            )

    # ------------------------------------------------------
    # Validação
    # ------------------------------------------------------

    if not bases_validas:
        raise ValueError(
            "Nenhuma avaliação válida foi encontrada."
        )

    # ------------------------------------------------------
    # Primeira base
    # ------------------------------------------------------

    nome_base, base = bases_validas[0]

    base = base.copy()

    # ------------------------------------------------------
    # Consolidação das avaliações seguintes
    # ------------------------------------------------------

    for nome_avaliacao, avaliacao in bases_validas[1:]:

        # --------------------------------------------------
        # Evita conflito nas colunas de identificação
        # --------------------------------------------------

        colunas_avaliacao = [
            coluna
            for coluna in avaliacao.columns
            if coluna not in [
                "CIE",
                "ESCOLA",
            ]
        ]

        avaliacao_merge = avaliacao[
            colunas_avaliacao
        ].copy()

        # --------------------------------------------------
        # Merge externo
        #
        # OUTER é fundamental:
        # escolas novas não são perdidas.
        # --------------------------------------------------

        base = base.merge(
            avaliacao_merge,
            on="CHAVE_ESCOLA",
            how="outer",
            suffixes=("", f"_{nome_avaliacao}"),
        )

        # --------------------------------------------------
        # Recupera CIE e ESCOLA quando necessário
        # --------------------------------------------------

        coluna_cie_avaliacao = f"CIE_{nome_avaliacao}"

        if coluna_cie_avaliacao in base.columns:

            base["CIE"] = base["CIE"].fillna(
                base[coluna_cie_avaliacao]
            )

            base.drop(
                columns=[coluna_cie_avaliacao],
                inplace=True,
            )

        coluna_escola_avaliacao = f"ESCOLA_{nome_avaliacao}"

        if coluna_escola_avaliacao in base.columns:

            base["ESCOLA"] = (
                base["ESCOLA"]
                .replace(
                    {
                        "NAN": pd.NA,
                        "NONE": pd.NA,
                        "<NA>": pd.NA,
                    }
                )
            )

            base["ESCOLA"] = base["ESCOLA"].fillna(
                base[coluna_escola_avaliacao]
            )

            base.drop(
                columns=[coluna_escola_avaliacao],
                inplace=True,
            )

    # ------------------------------------------------------
    # Normalização final do CIE
    # ------------------------------------------------------

    base["CIE"] = pd.to_numeric(
        base["CIE"],
        errors="coerce",
    ).astype("Int64")

    # ------------------------------------------------------
    # Normalização final da escola
    # ------------------------------------------------------

    base["ESCOLA"] = (
        base["ESCOLA"]
        .astype("string")
        .str.strip()
    )

    # ------------------------------------------------------
    # Ordenação
    # ------------------------------------------------------

    base.sort_values(
        by="ESCOLA",
        na_position="last",
        inplace=True,
    )

    # ------------------------------------------------------
    # Reinicia índice
    # ------------------------------------------------------

    base.reset_index(
        drop=True,
        inplace=True,
    )

    return base
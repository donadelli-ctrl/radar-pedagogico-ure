# ==========================================================
# RADAR PEDAGÓGICO URE
# MÓDULO: excel_final.py
# ==========================================================

import pandas as pd


# ==========================================================
# PAINEL GERAL
# ==========================================================

def gerar_painel(base):

    return base.copy()


# ==========================================================
# EVOLUÇÃO
# ==========================================================

def gerar_evolucao(base):

    evolucao = pd.DataFrame()

    if "ESCOLA" in base.columns:

        evolucao["ESCOLA"] = base["ESCOLA"]

    if "MEDIA_PP1" in base.columns:

        evolucao["PP1"] = base["MEDIA_PP1"]

    if "MEDIA_PP2" in base.columns:

        evolucao["PP2"] = base["MEDIA_PP2"]

    if "MEDIA_ADP" in base.columns:

        evolucao["ADP"] = base["MEDIA_ADP"]

    if "MEDIA_PP3" in base.columns:

        evolucao["PP3"] = base["MEDIA_PP3"]

    return evolucao


# ==========================================================
# PARTICIPAÇÃO
# ==========================================================

def gerar_participacao(base):

    participacao = pd.DataFrame()

    if "ESCOLA" in base.columns:

        participacao["ESCOLA"] = base["ESCOLA"]

    for coluna in [

        "PART_ADE",
        "PART_PP1",
        "PART_PP2",
        "PART_ADP",
        "PART_PP3",

    ]:

        if coluna in base.columns:

            participacao[coluna] = base[coluna]

    return participacao


# ==========================================================
# RANKING
# ==========================================================

def gerar_ranking(base):

    ranking = base.copy()

    if "MEDIA_PP3" in ranking.columns:

        ranking = ranking.sort_values(

            "MEDIA_PP3",

            ascending=False

        )

    elif "MEDIA_PP2" in ranking.columns:

        ranking = ranking.sort_values(

            "MEDIA_PP2",

            ascending=False

        )

    elif "MEDIA_PP1" in ranking.columns:

        ranking = ranking.sort_values(

            "MEDIA_PP1",

            ascending=False

        )

    ranking = ranking.reset_index(drop=True)

    ranking.insert(

        0,

        "POSIÇÃO",

        range(1, len(ranking) + 1)

    )

    return ranking


# ==========================================================
# RESUMO DA URE
# ==========================================================

def gerar_resumo(base, nome_ure):

    resumo = pd.DataFrame({

        "INDICADOR": [

            "URE",

            "TOTAL DE ESCOLAS",

        ],

        "VALOR": [

            nome_ure,

            len(base),

        ]

    })

    return resumo


# ==========================================================
# EXCEL
# ==========================================================

def gerar_excel(

    base,

    output,

    nome_ure,

):

    with pd.ExcelWriter(

        output,

        engine="openpyxl",

    ) as writer:

        gerar_painel(base).to_excel(

            writer,

            sheet_name="PAINEL_GERAL",

            index=False,

        )

        gerar_evolucao(base).to_excel(

            writer,

            sheet_name="EVOLUCAO",

            index=False,

        )

        gerar_participacao(base).to_excel(

            writer,

            sheet_name="PARTICIPACAO",

            index=False,

        )

        gerar_ranking(base).to_excel(

            writer,

            sheet_name="RANKING",

            index=False,

        )

        gerar_resumo(

            base,

            nome_ure,

        ).to_excel(

            writer,

            sheet_name="RESUMO_URE",

            index=False,

        )
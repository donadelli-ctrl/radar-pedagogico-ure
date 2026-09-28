"""
RADAR PEDAGÓGICO URE
MÓDULO: diagnostico.py

Responsabilidade:
    Gerar diagnóstico pedagógico e encaminhamento a partir dos indicadores.

Arquitetura:
    AVD1 → PP1 → PP2 → AVD2 → PP3

Regra específica da AVD1 e da AVD2:
    - O indicador diagnóstico utilizado é somente o percentual de estudantes
      no Abaixo do Básico em Língua Portuguesa e Matemática.
    - AVD1 é a avaliação diagnóstica inicial.
    - AVD2 é a avaliação diagnóstica de percurso, proveniente do arquivo ADP.
    - Os níveis Básico e Proficiente da ADP não participam da regra de análise.
    - Ausência de informação não é tratada como zero.
"""

import pandas as pd


# ==========================================================
# OBTÉM AVD1 — ABAIXO DO BÁSICO
# ==========================================================

def obter_avd1_abaixo(linha, componente):
    """
    Obtém o percentual de estudantes no Abaixo do Básico
    da avaliação diagnóstica inicial — AVD1.
    """

    componente = str(componente).strip().upper()

    if componente == "LP":
        colunas = [
            "LP_AVD1_ABAIXO_ANALISE",
            "LP_AVD1_ABAIXO",
            "LP_ABAIXO",
            "ADE_LP_ABAIXO",
        ]

    elif componente == "MAT":
        colunas = [
            "MAT_AVD1_ABAIXO_ANALISE",
            "MAT_AVD1_ABAIXO",
            "MAT_ABAIXO",
            "ADE_MAT_ABAIXO",
        ]

    else:
        return pd.NA

    for coluna in colunas:
        if coluna in linha.index and pd.notna(linha[coluna]):
            try:
                return float(linha[coluna])
            except (TypeError, ValueError):
                return pd.NA

    return pd.NA


# ==========================================================
# OBTÉM AVD2 — ABAIXO DO BÁSICO
# ==========================================================

def obter_avd2_abaixo(linha, componente):
    """
    Obtém o percentual de estudantes no Abaixo do Básico
    da avaliação diagnóstica de percurso — AVD2.

    AVD2 é proveniente do arquivo ADP.
    """

    componente = str(componente).strip().upper()

    if componente == "LP":
        colunas = [
            "LP_AVD2_ABAIXO_ANALISE",
            "LP_AVD2_ABAIXO",
            "LP_ADP_ABAIXO",
            "ADP_LP_ABAIXO",
            "ADP_ABAIXO_LP",
        ]

    elif componente == "MAT":
        colunas = [
            "MAT_AVD2_ABAIXO_ANALISE",
            "MAT_AVD2_ABAIXO",
            "MAT_ADP_ABAIXO",
            "ADP_MAT_ABAIXO",
            "ADP_ABAIXO_MAT",
        ]

    else:
        return pd.NA

    for coluna in colunas:
        if coluna in linha.index and pd.notna(linha[coluna]):
            try:
                return float(linha[coluna])
            except (TypeError, ValueError):
                return pd.NA

    return pd.NA


# ==========================================================
# DIAGNÓSTICO DE LÍNGUA PORTUGUESA
# ==========================================================

def diagnosticar_lp(linha):
    avd1_abaixo = obter_avd1_abaixo(linha, "LP")
    pp1 = linha.get("LP_PP1")
    pp2 = linha.get("LP_PP2")
    avd2_abaixo = obter_avd2_abaixo(linha, "LP")
    evolucao = linha.get("EVOLUCAO_LP")

    mensagens = []

    # ------------------------------------------------------
    # HISTÓRICO PP1 → PP2
    # ------------------------------------------------------

    if (
        pd.notna(avd1_abaixo)
        and pd.notna(pp2)
        and avd1_abaixo >= 0.50
        and pp2 < 0.50
    ):
        if pd.notna(evolucao) and evolucao < 0:
            mensagens.append(
                "Língua Portuguesa apresenta situação prioritária, "
                "com percentual elevado de estudantes no Abaixo do Básico "
                "na AVD1, desempenho inferior a 50% na PP2 "
                "e queda entre PP1 e PP2."
            )
        else:
            mensagens.append(
                "Língua Portuguesa apresenta percentual elevado de estudantes "
                "no Abaixo do Básico na AVD1 e desempenho inferior "
                "a 50% na PP2, exigindo atenção pedagógica."
            )

    elif (
        pd.notna(pp2)
        and pp2 < 0.50
        and pd.notna(evolucao)
        and evolucao > 0
    ):
        mensagens.append(
            "Língua Portuguesa apresenta desempenho inferior a 50% na PP2, "
            "porém registra evolução em relação à PP1, indicando avanço que "
            "precisa ser consolidado."
        )

    elif (
        pd.notna(pp2)
        and pp2 < 0.50
        and pd.notna(evolucao)
        and evolucao < 0
    ):
        mensagens.append(
            "Língua Portuguesa apresenta desempenho inferior a 50% na PP2 "
            "associado à queda em relação à PP1, indicando necessidade de "
            "intervenção pedagógica."
        )

    elif (
        pd.notna(pp2)
        and pp2 >= 0.50
        and pd.notna(evolucao)
        and evolucao < 0
    ):
        mensagens.append(
            "Língua Portuguesa apresenta resultado atual acima de 50%, "
            "porém registra queda em relação à PP1, indicando necessidade "
            "de acompanhamento."
        )

    elif pd.notna(evolucao) and evolucao >= 0.05:
        mensagens.append(
            "Língua Portuguesa apresenta evolução significativa entre as "
            "avaliações de desempenho, indicando avanço que pode ser "
            "sistematizado e consolidado."
        )

    elif pd.notna(evolucao) and evolucao > 0:
        mensagens.append(
            "Língua Portuguesa apresenta evolução entre as avaliações de "
            "desempenho, indicando avanço que deve ser acompanhado."
        )

    elif pd.notna(pp2) and pp2 >= 0.50:
        mensagens.append(
            "Língua Portuguesa apresenta resultado atual acima de 50%, "
            "sem sinal relevante de queda."
        )

    # ------------------------------------------------------
    # AVD2 — SOMENTE ABAIXO DO BÁSICO
    # ------------------------------------------------------

    if pd.notna(avd2_abaixo):

        if pd.notna(avd1_abaixo):

            diferenca = (
                float(avd2_abaixo)
                - float(avd1_abaixo)
            )

            if diferenca < 0:
                mensagens.append(
                    f"Na AVD2, Língua Portuguesa apresenta "
                    f"{avd2_abaixo:.1%} de estudantes no Abaixo do Básico, "
                    f"com redução de {abs(diferenca):.1%} em relação à AVD1."
                )

            elif diferenca > 0:
                mensagens.append(
                    f"Na AVD2, Língua Portuguesa apresenta "
                    f"{avd2_abaixo:.1%} de estudantes no Abaixo do Básico, "
                    f"com aumento de {diferenca:.1%} em relação à AVD1."
                )

            else:
                mensagens.append(
                    f"Na AVD2, Língua Portuguesa apresenta "
                    f"{avd2_abaixo:.1%} de estudantes no Abaixo do Básico, "
                    "mantendo o mesmo percentual observado na AVD1."
                )

        else:
            mensagens.append(
                f"Na AVD2, Língua Portuguesa apresenta "
                f"{avd2_abaixo:.1%} de estudantes no Abaixo do Básico."
            )

    return " ".join(mensagens)


# ==========================================================
# DIAGNÓSTICO DE MATEMÁTICA
# ==========================================================

def diagnosticar_mat(linha):
    avd1_abaixo = obter_avd1_abaixo(linha, "MAT")
    pp1 = linha.get("MAT_PP1")
    pp2 = linha.get("MAT_PP2")
    avd2_abaixo = obter_avd2_abaixo(linha, "MAT")
    evolucao = linha.get("EVOLUCAO_MAT")

    mensagens = []

    # ------------------------------------------------------
    # HISTÓRICO PP1 → PP2
    # ------------------------------------------------------

    if (
        pd.notna(avd1_abaixo)
        and pd.notna(pp2)
        and avd1_abaixo >= 0.50
        and pp2 < 0.50
    ):
        if pd.notna(evolucao) and evolucao < 0:
            mensagens.append(
                "Matemática apresenta situação prioritária, com percentual "
                "elevado de estudantes no Abaixo do Básico na AVD1, "
                "desempenho inferior a 50% na PP2 e queda entre PP1 e PP2."
            )
        else:
            mensagens.append(
                "Matemática apresenta percentual elevado de estudantes no "
                "Abaixo do Básico na AVD1 e desempenho inferior a 50% na "
                "PP2, exigindo atenção pedagógica."
            )

    elif (
        pd.notna(pp2)
        and pp2 < 0.50
        and pd.notna(evolucao)
        and evolucao > 0
    ):
        mensagens.append(
            "Matemática apresenta desempenho inferior a 50% na PP2, porém "
            "registra evolução em relação à PP1, indicando avanço que "
            "precisa ser consolidado."
        )

    elif (
        pd.notna(pp2)
        and pp2 < 0.50
        and pd.notna(evolucao)
        and evolucao < 0
    ):
        mensagens.append(
            "Matemática apresenta desempenho inferior a 50% na PP2 associado "
            "à queda em relação à PP1, indicando necessidade de intervenção pedagógica."
        )

    elif (
        pd.notna(pp2)
        and pp2 >= 0.50
        and pd.notna(evolucao)
        and evolucao < 0
    ):
        mensagens.append(
            "Matemática apresenta resultado atual acima de 50%, porém registra "
            "queda em relação à PP1, indicando necessidade de acompanhamento."
        )

    elif pd.notna(evolucao) and evolucao >= 0.05:
        mensagens.append(
            "Matemática apresenta evolução significativa entre as avaliações "
            "de desempenho, indicando avanço que pode ser sistematizado e consolidado."
        )

    elif pd.notna(evolucao) and evolucao > 0:
        mensagens.append(
            "Matemática apresenta evolução entre as avaliações de desempenho, "
            "indicando avanço que deve ser acompanhado."
        )

    elif pd.notna(pp2) and pp2 >= 0.50:
        mensagens.append(
            "Matemática apresenta resultado atual acima de 50%, "
            "sem sinal relevante de queda."
        )

    # ------------------------------------------------------
    # AVD2 — SOMENTE ABAIXO DO BÁSICO
    # ------------------------------------------------------

    if pd.notna(avd2_abaixo):

        if pd.notna(avd1_abaixo):

            diferenca = (
                float(avd2_abaixo)
                - float(avd1_abaixo)
            )

            if diferenca < 0:
                mensagens.append(
                    f"Na AVD2, Matemática apresenta "
                    f"{avd2_abaixo:.1%} de estudantes no Abaixo do Básico, "
                    f"com redução de {abs(diferenca):.1%} em relação à AVD1."
                )

            elif diferenca > 0:
                mensagens.append(
                    f"Na AVD2, Matemática apresenta "
                    f"{avd2_abaixo:.1%} de estudantes no Abaixo do Básico, "
                    f"com aumento de {diferenca:.1%} em relação à AVD1."
                )

            else:
                mensagens.append(
                    f"Na AVD2, Matemática apresenta "
                    f"{avd2_abaixo:.1%} de estudantes no Abaixo do Básico, "
                    "mantendo o mesmo percentual observado na AVD1."
                )

        else:
            mensagens.append(
                f"Na AVD2, Matemática apresenta "
                f"{avd2_abaixo:.1%} de estudantes no Abaixo do Básico."
            )

    return " ".join(mensagens)


# ==========================================================
# DIAGNÓSTICO GERAL
# ==========================================================

def gerar_diagnostico(linha):
    """
    Gera o diagnóstico pedagógico geral da escola.

    A existência de AVD2 permite análise diagnóstica mesmo
    quando a escola ainda não possui histórico completo.

    AVD1 e AVD2 são analisadas separadamente.
    """

    qtd = linha.get(
        "QTD_AVALIACOES",
        0,
    )

    if pd.isna(qtd):
        qtd = 0

    possui_avd1 = (
        pd.notna(
            obter_avd1_abaixo(
                linha,
                "LP",
            )
        )
        or
        pd.notna(
            obter_avd1_abaixo(
                linha,
                "MAT",
            )
        )
    )

    possui_avd2 = (
        pd.notna(
            obter_avd2_abaixo(
                linha,
                "LP",
            )
        )
        or
        pd.notna(
            obter_avd2_abaixo(
                linha,
                "MAT",
            )
        )
    )

    if qtd < 2 and not possui_avd1 and not possui_avd2:
        return (
            "Histórico avaliativo insuficiente para diagnóstico consolidado."
        )

    diagnosticos = []

    diagnostico_lp = diagnosticar_lp(linha)
    diagnostico_mat = diagnosticar_mat(linha)

    if diagnostico_lp:
        diagnosticos.append(
            diagnostico_lp
        )

    if diagnostico_mat:
        diagnosticos.append(
            diagnostico_mat
        )

    if not diagnosticos:
        return (
            "Não foram identificados sinais relevantes nos indicadores analisados."
        )

    return " | ".join(
        diagnosticos
    )


# ==========================================================
# ENCAMINHAMENTO DE LÍNGUA PORTUGUESA
# ==========================================================

def encaminhar_lp(linha):
    avd1_abaixo = obter_avd1_abaixo(linha, "LP")
    pp2 = linha.get("LP_PP2")
    avd2_abaixo = obter_avd2_abaixo(linha, "LP")
    evolucao = linha.get("EVOLUCAO_LP")

    encaminhamentos = []

    # ------------------------------------------------------
    # HISTÓRICO DE DESEMPENHO
    # ------------------------------------------------------

    if (
        pd.notna(avd1_abaixo)
        and pd.notna(pp2)
        and pd.notna(evolucao)
        and avd1_abaixo >= 0.50
        and pp2 < 0.50
        and evolucao < 0
    ):
        encaminhamentos.append(
            "Priorizar a análise das habilidades de Língua Portuguesa "
            "com menor desempenho, identificar os estudantes que permanecem "
            "em maior dificuldade e reorganizar as ações de recomposição."
        )

    elif (
        pd.notna(pp2)
        and pp2 < 0.50
        and pd.notna(evolucao)
        and evolucao > 0
    ):
        encaminhamentos.append(
            "Manter e fortalecer as estratégias adotadas em Língua Portuguesa, "
            "identificar as habilidades ainda fragilizadas e acompanhar a "
            "consolidação dos avanços."
        )

    elif (
        pd.notna(pp2)
        and pp2 < 0.50
        and pd.notna(evolucao)
        and evolucao < 0
    ):
        encaminhamentos.append(
            "Analisar as habilidades de Língua Portuguesa com menor desempenho, "
            "investigar os fatores associados à queda e reorganizar as ações pedagógicas."
        )

    elif (
        pd.notna(pp2)
        and pp2 >= 0.50
        and pd.notna(evolucao)
        and evolucao < 0
    ):
        encaminhamentos.append(
            "Acompanhar a queda observada em Língua Portuguesa, analisar as "
            "habilidades que apresentaram redução de desempenho e ajustar "
            "as estratégias pedagógicas."
        )

    elif pd.notna(evolucao) and evolucao >= 0.05:
        encaminhamentos.append(
            "Sistematizar as estratégias que contribuíram para a evolução em "
            "Língua Portuguesa e identificar práticas exitosas que possam ser compartilhadas."
        )

    # ------------------------------------------------------
    # AVD2
    # ------------------------------------------------------

    if pd.notna(avd2_abaixo):

        if (
            pd.notna(avd1_abaixo)
            and avd2_abaixo > avd1_abaixo
        ):
            encaminhamentos.append(
                "Na AVD2, priorizar as habilidades de Língua Portuguesa "
                "relacionadas ao Abaixo do Básico, identificar os estudantes "
                "em maior dificuldade e reforçar as ações de recomposição."
            )

        elif (
            pd.notna(avd1_abaixo)
            and avd2_abaixo < avd1_abaixo
        ):
            encaminhamentos.append(
                "Na AVD2, acompanhar a redução do Abaixo do Básico em Língua "
                "Portuguesa, identificar as estratégias que contribuíram "
                "para o avanço e consolidá-las."
            )

        else:
            encaminhamentos.append(
                "Na AVD2, acompanhar as habilidades de Língua Portuguesa "
                "ainda fragilizadas no Abaixo do Básico e verificar "
                "a consolidação dos resultados."
            )

    return " ".join(
        encaminhamentos
    )


# ==========================================================
# ENCAMINHAMENTO DE MATEMÁTICA
# ==========================================================

def encaminhar_mat(linha):
    avd1_abaixo = obter_avd1_abaixo(linha, "MAT")
    pp2 = linha.get("MAT_PP2")
    avd2_abaixo = obter_avd2_abaixo(linha, "MAT")
    evolucao = linha.get("EVOLUCAO_MAT")

    encaminhamentos = []

    # ------------------------------------------------------
    # HISTÓRICO DE DESEMPENHO
    # ------------------------------------------------------

    if (
        pd.notna(avd1_abaixo)
        and pd.notna(pp2)
        and pd.notna(evolucao)
        and avd1_abaixo >= 0.50
        and pp2 < 0.50
        and evolucao < 0
    ):
        encaminhamentos.append(
            "Priorizar a análise das habilidades de Matemática com menor "
            "desempenho, identificar os estudantes que permanecem em maior "
            "dificuldade e reorganizar as ações de recomposição."
        )

    elif (
        pd.notna(pp2)
        and pp2 < 0.50
        and pd.notna(evolucao)
        and evolucao > 0
    ):
        encaminhamentos.append(
            "Manter e fortalecer as estratégias adotadas em Matemática, "
            "identificar as habilidades ainda fragilizadas e acompanhar "
            "a consolidação dos avanços."
        )

    elif (
        pd.notna(pp2)
        and pp2 < 0.50
        and pd.notna(evolucao)
        and evolucao < 0
    ):
        encaminhamentos.append(
            "Analisar as habilidades de Matemática com menor desempenho, "
            "investigar os fatores associados à queda e reorganizar "
            "as ações pedagógicas."
        )

    elif (
        pd.notna(pp2)
        and pp2 >= 0.50
        and pd.notna(evolucao)
        and evolucao < 0
    ):
        encaminhamentos.append(
            "Acompanhar a queda observada em Matemática, analisar as "
            "habilidades que apresentaram redução de desempenho e ajustar "
            "as estratégias pedagógicas."
        )

    elif pd.notna(evolucao) and evolucao >= 0.05:
        encaminhamentos.append(
            "Sistematizar as estratégias que contribuíram para a evolução "
            "em Matemática e identificar práticas exitosas que possam ser compartilhadas."
        )

    # ------------------------------------------------------
    # AVD2
    # ------------------------------------------------------

    if pd.notna(avd2_abaixo):

        if (
            pd.notna(avd1_abaixo)
            and avd2_abaixo > avd1_abaixo
        ):
            encaminhamentos.append(
                "Na AVD2, priorizar as habilidades de Matemática relacionadas "
                "ao Abaixo do Básico, identificar os estudantes em maior "
                "dificuldade e reforçar as ações de recomposição."
            )

        elif (
            pd.notna(avd1_abaixo)
            and avd2_abaixo < avd1_abaixo
        ):
            encaminhamentos.append(
                "Na AVD2, acompanhar a redução do Abaixo do Básico em "
                "Matemática, identificar as estratégias que contribuíram "
                "para o avanço e consolidá-las."
            )

        else:
            encaminhamentos.append(
                "Na AVD2, acompanhar as habilidades de Matemática ainda "
                "fragilizadas no Abaixo do Básico e verificar "
                "a consolidação dos resultados."
            )

    return " ".join(
        encaminhamentos
    )


# ==========================================================
# ENCAMINHAMENTO GERAL
# ==========================================================

def gerar_encaminhamento(linha):
    qtd = linha.get(
        "QTD_AVALIACOES",
        0,
    )

    if pd.isna(qtd):
        qtd = 0

    possui_avd1 = (
        pd.notna(
            obter_avd1_abaixo(
                linha,
                "LP",
            )
        )
        or
        pd.notna(
            obter_avd1_abaixo(
                linha,
                "MAT",
            )
        )
    )

    possui_avd2 = (
        pd.notna(
            obter_avd2_abaixo(
                linha,
                "LP",
            )
        )
        or
        pd.notna(
            obter_avd2_abaixo(
                linha,
                "MAT",
            )
        )
    )

    if (
        qtd < 2
        and not possui_avd1
        and not possui_avd2
    ):
        return (
            "Acompanhar a participação nas próximas avaliações e constituir "
            "histórico suficiente para análise da evolução."
        )

    encaminhamentos = []

    encaminhamento_lp = encaminhar_lp(linha)
    encaminhamento_mat = encaminhar_mat(linha)

    if encaminhamento_lp:
        encaminhamentos.append(
            encaminhamento_lp
        )

    if encaminhamento_mat:
        encaminhamentos.append(
            encaminhamento_mat
        )

    if not encaminhamentos:
        return (
            "Manter o acompanhamento dos indicadores e das ações pedagógicas."
        )

    return " | ".join(
        encaminhamentos
    )


# ==========================================================
# APLICA DIAGNÓSTICO E ENCAMINHAMENTO
# ==========================================================

def aplicar_diagnostico(base):
    """
    Aplica diagnóstico e encaminhamento em cada linha da base.
    """

    if base is None or base.empty:
        return base

    resultado = base.copy()

    resultado["DIAGNOSTICO"] = resultado.apply(
        gerar_diagnostico,
        axis=1,
    )

    resultado["ENCAMINHAMENTO"] = resultado.apply(
        gerar_encaminhamento,
        axis=1,
    )

    return resultado

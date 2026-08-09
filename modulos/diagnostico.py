"""
Responsabilidade:
Gerar diagnóstico pedagógico e encaminhamento
a partir dos indicadores e do Farol URE V1.
"""

import pandas as pd


# ==========================================================
# DIAGNÓSTICO DE LÍNGUA PORTUGUESA
# ==========================================================

def diagnosticar_lp(linha):

    abaixo = linha.get("LP_ABAIXO")
    pp1 = linha.get("LP_PP1")
    pp2 = linha.get("LP_PP2")
    evolucao = linha.get("EVOLUCAO_LP")

    # ------------------------------------------------------
    # Problema persistente com queda
    # ------------------------------------------------------

    if (
        pd.notna(abaixo)
        and pd.notna(pp1)
        and pd.notna(pp2)
        and pd.notna(evolucao)
        and abaixo >= 0.50
        and pp2 < 0.50
        and evolucao < 0
    ):
        return (
            "Língua Portuguesa apresenta situação prioritária, "
            "com percentual elevado de estudantes no Abaixo do "
            "Básico no diagnóstico inicial, desempenho inferior "
            "a 50% na PP2 e queda entre PP1 e PP2."
        )

    # ------------------------------------------------------
    # Resultado baixo com evolução
    # ------------------------------------------------------

    if (
        pd.notna(pp2)
        and pp2 < 0.50
        and pd.notna(evolucao)
        and evolucao > 0
    ):
        return (
            "Língua Portuguesa apresenta desempenho inferior "
            "a 50% na PP2, porém registra evolução em relação "
            "à PP1, indicando avanço que precisa ser consolidado."
        )

    # ------------------------------------------------------
    # Resultado baixo com queda
    # ------------------------------------------------------

    if (
        pd.notna(pp2)
        and pp2 < 0.50
        and pd.notna(evolucao)
        and evolucao < 0
    ):
        return (
            "Língua Portuguesa apresenta desempenho inferior "
            "a 50% na PP2 associado à queda em relação à PP1, "
            "indicando necessidade de intervenção pedagógica."
        )

    # ------------------------------------------------------
    # Resultado adequado com queda
    # ------------------------------------------------------

    if (
        pd.notna(pp2)
        and pp2 >= 0.50
        and pd.notna(evolucao)
        and evolucao < 0
    ):
        return (
            "Língua Portuguesa apresenta resultado atual "
            "acima de 50%, porém registra queda em relação "
            "à PP1, indicando necessidade de acompanhamento."
        )

    # ------------------------------------------------------
    # Evolução significativa
    # ------------------------------------------------------

    if (
        pd.notna(evolucao)
        and evolucao >= 0.05
    ):
        return (
            "Língua Portuguesa apresenta evolução significativa "
            "entre PP1 e PP2, indicando avanço que pode ser "
            "sistematizado e consolidado."
        )

    # ------------------------------------------------------
    # Evolução positiva
    # ------------------------------------------------------

    if (
        pd.notna(evolucao)
        and evolucao > 0
    ):
        return (
            "Língua Portuguesa apresenta evolução entre PP1 "
            "e PP2, indicando avanço que deve ser acompanhado."
        )

    # ------------------------------------------------------
    # Resultado adequado
    # ------------------------------------------------------

    if (
        pd.notna(pp2)
        and pp2 >= 0.50
    ):
        return (
            "Língua Portuguesa apresenta resultado atual "
            "acima de 50%, sem sinal relevante de queda."
        )

    return ""


# ==========================================================
# DIAGNÓSTICO DE MATEMÁTICA
# ==========================================================

def diagnosticar_mat(linha):

    abaixo = linha.get("MAT_ABAIXO")
    pp1 = linha.get("MAT_PP1")
    pp2 = linha.get("MAT_PP2")
    evolucao = linha.get("EVOLUCAO_MAT")

    # ------------------------------------------------------
    # Problema persistente com queda
    # ------------------------------------------------------

    if (
        pd.notna(abaixo)
        and pd.notna(pp1)
        and pd.notna(pp2)
        and pd.notna(evolucao)
        and abaixo >= 0.50
        and pp2 < 0.50
        and evolucao < 0
    ):
        return (
            "Matemática apresenta situação prioritária, "
            "com percentual elevado de estudantes no Abaixo "
            "do Básico no diagnóstico inicial, desempenho "
            "inferior a 50% na PP2 e queda entre PP1 e PP2."
        )

    # ------------------------------------------------------
    # Resultado baixo com evolução
    # ------------------------------------------------------

    if (
        pd.notna(pp2)
        and pp2 < 0.50
        and pd.notna(evolucao)
        and evolucao > 0
    ):
        return (
            "Matemática apresenta desempenho inferior a 50% "
            "na PP2, porém registra evolução em relação à PP1, "
            "indicando avanço que precisa ser consolidado."
        )

    # ------------------------------------------------------
    # Resultado baixo com queda
    # ------------------------------------------------------

    if (
        pd.notna(pp2)
        and pp2 < 0.50
        and pd.notna(evolucao)
        and evolucao < 0
    ):
        return (
            "Matemática apresenta desempenho inferior a 50% "
            "na PP2 associado à queda em relação à PP1, "
            "indicando necessidade de intervenção pedagógica."
        )

    # ------------------------------------------------------
    # Resultado adequado com queda
    # ------------------------------------------------------

    if (
        pd.notna(pp2)
        and pp2 >= 0.50
        and pd.notna(evolucao)
        and evolucao < 0
    ):
        return (
            "Matemática apresenta resultado atual acima de 50%, "
            "porém registra queda em relação à PP1, indicando "
            "necessidade de acompanhamento."
        )

    # ------------------------------------------------------
    # Evolução significativa
    # ------------------------------------------------------

    if (
        pd.notna(evolucao)
        and evolucao >= 0.05
    ):
        return (
            "Matemática apresenta evolução significativa entre "
            "PP1 e PP2, indicando avanço que pode ser sistematizado "
            "e consolidado."
        )

    # ------------------------------------------------------
    # Evolução positiva
    # ------------------------------------------------------

    if (
        pd.notna(evolucao)
        and evolucao > 0
    ):
        return (
            "Matemática apresenta evolução entre PP1 e PP2, "
            "indicando avanço que deve ser acompanhado."
        )

    # ------------------------------------------------------
    # Resultado adequado
    # ------------------------------------------------------

    if (
        pd.notna(pp2)
        and pp2 >= 0.50
    ):
        return (
            "Matemática apresenta resultado atual acima de 50%, "
            "sem sinal relevante de queda."
        )

    return ""


# ==========================================================
# DIAGNÓSTICO GERAL
# ==========================================================

def gerar_diagnostico(linha):

    if linha.get("QTD_AVALIACOES", 0) < 2:

        return (
            "Histórico avaliativo insuficiente para "
            "diagnóstico consolidado."
        )

    diagnosticos = []

    diagnostico_lp = diagnosticar_lp(linha)

    diagnostico_mat = diagnosticar_mat(linha)

    if diagnostico_lp:
        diagnosticos.append(diagnostico_lp)

    if diagnostico_mat:
        diagnosticos.append(diagnostico_mat)

    if not diagnosticos:

        return (
            "Não foram identificados sinais relevantes "
            "nos indicadores analisados."
        )

    return " | ".join(diagnosticos)


# ==========================================================
# ENCAMINHAMENTO DE LÍNGUA PORTUGUESA
# ==========================================================

def encaminhar_lp(linha):

    abaixo = linha.get("LP_ABAIXO")
    pp2 = linha.get("LP_PP2")
    evolucao = linha.get("EVOLUCAO_LP")

    # Prioridade
    if (
        pd.notna(abaixo)
        and pd.notna(pp2)
        and pd.notna(evolucao)
        and abaixo >= 0.50
        and pp2 < 0.50
        and evolucao < 0
    ):
        return (
            "Priorizar a análise das habilidades de Língua "
            "Portuguesa com menor desempenho, identificar os "
            "estudantes que permanecem em maior dificuldade e "
            "reorganizar as ações de recomposição, acompanhando "
            "os resultados na próxima avaliação."
        )

    # Baixo + evolução
    if (
        pd.notna(pp2)
        and pp2 < 0.50
        and pd.notna(evolucao)
        and evolucao > 0
    ):
        return (
            "Manter e fortalecer as estratégias adotadas em "
            "Língua Portuguesa, identificar as habilidades "
            "ainda fragilizadas e acompanhar a consolidação "
            "dos avanços."
        )

    # Baixo + queda
    if (
        pd.notna(pp2)
        and pp2 < 0.50
        and pd.notna(evolucao)
        and evolucao < 0
    ):
        return (
            "Analisar as habilidades de Língua Portuguesa com "
            "menor desempenho, investigar os fatores associados "
            "à queda e reorganizar as ações pedagógicas."
        )

    # Acima de 50% + queda
    if (
        pd.notna(pp2)
        and pp2 >= 0.50
        and pd.notna(evolucao)
        and evolucao < 0
    ):
        return (
            "Acompanhar a queda observada em Língua Portuguesa, "
            "analisar as habilidades que apresentaram redução "
            "de desempenho e ajustar as estratégias pedagógicas."
        )

    # Evolução significativa
    if (
        pd.notna(evolucao)
        and evolucao >= 0.05
    ):
        return (
            "Sistematizar as estratégias que contribuíram para "
            "a evolução em Língua Portuguesa e identificar "
            "práticas exitosas que possam ser compartilhadas."
        )

    return ""


# ==========================================================
# ENCAMINHAMENTO DE MATEMÁTICA
# ==========================================================

def encaminhar_mat(linha):

    abaixo = linha.get("MAT_ABAIXO")
    pp2 = linha.get("MAT_PP2")
    evolucao = linha.get("EVOLUCAO_MAT")

    # Prioridade
    if (
        pd.notna(abaixo)
        and pd.notna(pp2)
        and pd.notna(evolucao)
        and abaixo >= 0.50
        and pp2 < 0.50
        and evolucao < 0
    ):
        return (
            "Priorizar a análise das habilidades de Matemática "
            "com menor desempenho, identificar os estudantes que "
            "permanecem em maior dificuldade e reorganizar as "
            "ações de recomposição, acompanhando os resultados "
            "na próxima avaliação."
        )

    # Baixo + evolução
    if (
        pd.notna(pp2)
        and pp2 < 0.50
        and pd.notna(evolucao)
        and evolucao > 0
    ):
        return (
            "Manter e fortalecer as estratégias adotadas em "
            "Matemática, identificar as habilidades ainda "
            "fragilizadas e acompanhar a consolidação dos avanços."
        )

    # Baixo + queda
    if (
        pd.notna(pp2)
        and pp2 < 0.50
        and pd.notna(evolucao)
        and evolucao < 0
    ):
        return (
            "Analisar as habilidades de Matemática com menor "
            "desempenho, investigar os fatores associados à "
            "queda e reorganizar as ações pedagógicas."
        )

    # Acima de 50% + queda
    if (
        pd.notna(pp2)
        and pp2 >= 0.50
        and pd.notna(evolucao)
        and evolucao < 0
    ):
        return (
            "Acompanhar a queda observada em Matemática, analisar "
            "as habilidades que apresentaram redução de desempenho "
            "e ajustar as estratégias pedagógicas."
        )

    # Evolução significativa
    if (
        pd.notna(evolucao)
        and evolucao >= 0.05
    ):
        return (
            "Sistematizar as estratégias que contribuíram para "
            "a evolução em Matemática e identificar práticas "
            "exitosas que possam ser compartilhadas."
        )

    return ""


# ==========================================================
# ENCAMINHAMENTO GERAL
# ==========================================================

def gerar_encaminhamento(linha):

    if linha.get("QTD_AVALIACOES", 0) < 2:

        return (
            "Acompanhar a participação nas próximas avaliações "
            "e constituir histórico suficiente para análise "
            "da evolução."
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
            "Manter o acompanhamento dos indicadores e "
            "das estratégias pedagógicas adotadas."
        )

    return " | ".join(encaminhamentos)


# ==========================================================
# APLICAÇÃO
# ==========================================================

def aplicar_diagnostico(base: pd.DataFrame) -> pd.DataFrame:

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
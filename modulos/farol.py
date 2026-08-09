"""
Responsabilidade:
Calcular o Farol URE V1.

Regra congelada:

PRIORITÁRIA:
    ADE Abaixo do Básico >= 50%
    +
    PP2 < 50%
    +
    PP2 < PP1

ATENÇÃO:
    Existe pelo menos um sinal de risco,
    mas a escola não atende aos três critérios
    de Prioritária.

FAVORÁVEL:
    Não apresenta sinal relevante de risco.

DESTAQUE DE EVOLUÇÃO:
    Indicador complementar, independente da situação
    principal do Farol.
"""

import pandas as pd


# ==========================================================
# PRIORIDADE POR COMPONENTE
# ==========================================================

def verificar_prioridade_linguaportuguesa(linha):
    """
    Verifica se a escola atende aos três critérios
    de Prioritária em Língua Portuguesa.
    """

    if pd.isna(linha.get("LP_ABAIXO")):
        return False

    if pd.isna(linha.get("LP_PP1")):
        return False

    if pd.isna(linha.get("LP_PP2")):
        return False

    return (
        linha["LP_ABAIXO"] >= 0.50
        and linha["LP_PP2"] < 0.50
        and linha["LP_PP2"] < linha["LP_PP1"]
    )


def verificar_prioridade_matematica(linha):
    """
    Verifica se a escola atende aos três critérios
    de Prioritária em Matemática.
    """

    if pd.isna(linha.get("MAT_ABAIXO")):
        return False

    if pd.isna(linha.get("MAT_PP1")):
        return False

    if pd.isna(linha.get("MAT_PP2")):
        return False

    return (
        linha["MAT_ABAIXO"] >= 0.50
        and linha["MAT_PP2"] < 0.50
        and linha["MAT_PP2"] < linha["MAT_PP1"]
    )


# ==========================================================
# SITUAÇÃO DE RISCO POR COMPONENTE
# ==========================================================

def verificar_risco_lingua_portuguesa(linha):
    """
    Identifica se existe pelo menos um sinal de risco
    em Língua Portuguesa.
    """

    sinais = []

    if pd.notna(linha.get("LP_PP2")):
        sinais.append(linha["LP_PP2"] < 0.50)

    if pd.notna(linha.get("EVOLUCAO_LP")):
        sinais.append(linha["EVOLUCAO_LP"] < 0)

    if pd.notna(linha.get("LP_ABAIXO")):
        sinais.append(linha["LP_ABAIXO"] >= 0.50)

    return any(sinais)


def verificar_risco_matematica(linha):
    """
    Identifica se existe pelo menos um sinal de risco
    em Matemática.
    """

    sinais = []

    if pd.notna(linha.get("MAT_PP2")):
        sinais.append(linha["MAT_PP2"] < 0.50)

    if pd.notna(linha.get("EVOLUCAO_MAT")):
        sinais.append(linha["EVOLUCAO_MAT"] < 0)

    if pd.notna(linha.get("MAT_ABAIXO")):
        sinais.append(linha["MAT_ABAIXO"] >= 0.50)

    return any(sinais)


# ==========================================================
# SITUAÇÃO PRINCIPAL DO FAROL
# ==========================================================

def classificar_farol(linha):
    """
    Classifica a situação principal da escola.

    Ordem de prioridade:

        PRIORITÁRIA
        ATENÇÃO
        FAVORÁVEL
        SEM HISTÓRICO
    """

    # ------------------------------------------------------
    # Sem histórico suficiente
    # ------------------------------------------------------

    if linha.get("QTD_AVALIACOES", 0) < 2:

        return "SEM HISTÓRICO"

    # ------------------------------------------------------
    # Prioridade
    # ------------------------------------------------------

    prioridade_lp = verificar_prioridade_linguaportuguesa(
        linha
    )

    prioridade_mat = verificar_prioridade_matematica(
        linha
    )

    if prioridade_lp or prioridade_mat:

        return "PRIORITÁRIA"

    # ------------------------------------------------------
    # Atenção
    # ------------------------------------------------------

    risco_lp = verificar_risco_lingua_portuguesa(
        linha
    )

    risco_mat = verificar_risco_matematica(
        linha
    )

    if risco_lp or risco_mat:

        return "ATENÇÃO"

    # ------------------------------------------------------
    # Favorável
    # ------------------------------------------------------

    return "FAVORÁVEL"


# ==========================================================
# COMPONENTE PRIORITÁRIO
# ==========================================================

def identificar_componentes(linha):
    """
    Identifica quais componentes apresentam situação
    prioritária ou sinal de atenção.
    """

    componentes_prioritarios = []
    componentes_atencao = []

    prioridade_lp = verificar_prioridade_linguaportuguesa(
        linha
    )

    prioridade_mat = verificar_prioridade_matematica(
        linha
    )

    risco_lp = verificar_risco_lingua_portuguesa(
        linha
    )

    risco_mat = verificar_risco_matematica(
        linha
    )

    if prioridade_lp:
        componentes_prioritarios.append(
            "LÍNGUA PORTUGUESA"
        )
    elif risco_lp:
        componentes_atencao.append(
            "LÍNGUA PORTUGUESA"
        )

    if prioridade_mat:
        componentes_prioritarios.append(
            "MATEMÁTICA"
        )
    elif risco_mat:
        componentes_atencao.append(
            "MATEMÁTICA"
        )

    if componentes_prioritarios:

        return " + ".join(
            componentes_prioritarios
        )

    if componentes_atencao:

        return " + ".join(
            componentes_atencao
        )

    return ""


# ==========================================================
# DESTAQUE DE EVOLUÇÃO
# ==========================================================

def identificar_evolucao(linha):
    """
    Identifica evolução significativa em pelo menos
    um dos componentes.

    Critério V1:
        evolução >= 5 pontos percentuais.
    """

    evolucoes = []

    if pd.notna(linha.get("EVOLUCAO_LP")):

        evolucoes.append(
            linha["EVOLUCAO_LP"]
        )

    if pd.notna(linha.get("EVOLUCAO_MAT")):

        evolucoes.append(
            linha["EVOLUCAO_MAT"]
        )

    if not evolucoes:

        return False

    return any(
        valor >= 0.05
        for valor in evolucoes
    )


# ==========================================================
# APLICAÇÃO DO FAROL
# ==========================================================

def aplicar_farol(base: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica o Farol URE V1 à base consolidada.

    Não altera os dados originais.
    """

    if base is None or base.empty:

        return base

    resultado = base.copy()

    # ------------------------------------------------------
    # Situação principal
    # ------------------------------------------------------

    resultado["FAROL_URE"] = resultado.apply(
        classificar_farol,
        axis=1,
    )

    # ------------------------------------------------------
    # Componentes envolvidos
    # ------------------------------------------------------

    resultado["COMPONENTE_FAROL"] = resultado.apply(
        identificar_componentes,
        axis=1,
    )

    # ------------------------------------------------------
    # Destaque de evolução
    # ------------------------------------------------------

    resultado["DESTAQUE_EVOLUCAO"] = resultado.apply(
        identificar_evolucao,
        axis=1,
    )

    return resultado
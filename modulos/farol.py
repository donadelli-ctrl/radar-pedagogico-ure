"""
RADAR PEDAGÓGICO URE
MÓDULO: farol.py

Responsabilidade:
    Calcular o Farol URE V1.

Arquitetura:
    AVD1 → PP1 → PP2 → AVD2 → PP3

Regra congelada:

PRIORITÁRIA:
    AVD1 Abaixo do Básico >= 50%
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

SEM HISTÓRICO:
    Não possui histórico suficiente para classificação.

DESTAQUE DE EVOLUÇÃO:
    Indicador complementar, independente da situação
    principal do Farol.

IMPORTANTE:
    AVD1 e AVD2 são provenientes do arquivo ADP.

    AVD1:
        LP_AVD1_ABAIXO_ANALISE
        MAT_AVD1_ABAIXO_ANALISE

    AVD2:
        LP_AVD2_ABAIXO_ANALISE
        MAT_AVD2_ABAIXO_ANALISE

    A classificação do Farol URE utiliza AVD1 como
    referência diagnóstica inicial.
"""

import pandas as pd


# ==========================================================
# OBTÉM O AVD1 ABAIXO DO BÁSICO
# ==========================================================

def obter_avd1_abaixo(
    linha,
    componente,
):
    """
    Obtém o percentual de estudantes Abaixo do Básico
    na avaliação diagnóstica inicial — AVD1.

    AVD1 é a referência diagnóstica inicial do Farol URE.

    Mantemos aliases antigos para compatibilidade com
    versões anteriores do projeto.
    """

    componente = (
        str(componente)
        .strip()
        .upper()
    )

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

        if coluna in linha.index:

            valor = linha[coluna]

            if pd.notna(valor):

                try:
                    return float(valor)

                except (
                    TypeError,
                    ValueError,
                ):

                    return pd.NA

    return pd.NA


# ==========================================================
# PRIORIDADE POR COMPONENTE
# ==========================================================

def verificar_prioridade_linguaportuguesa(
    linha,
):
    """
    Verifica se a escola atende aos três critérios
    de Prioritária em Língua Portuguesa.

    Critérios:

        1. AVD1 Abaixo do Básico >= 50%
        2. PP2 < 50%
        3. PP2 < PP1
    """

    lp_abaixo = obter_avd1_abaixo(
        linha,
        "LP",
    )

    lp_pp1 = linha.get(
        "LP_PP1",
        pd.NA,
    )

    lp_pp2 = linha.get(
        "LP_PP2",
        pd.NA,
    )

    # ------------------------------------------------------
    # Sem dados suficientes
    # ------------------------------------------------------

    if pd.isna(lp_abaixo):

        return False

    if pd.isna(lp_pp1):

        return False

    if pd.isna(lp_pp2):

        return False

    # ------------------------------------------------------
    # Regra congelada
    # ------------------------------------------------------

    return (
        lp_abaixo >= 0.50
        and lp_pp2 < 0.50
        and lp_pp2 < lp_pp1
    )


# ==========================================================
# PRIORIDADE EM MATEMÁTICA
# ==========================================================

def verificar_prioridade_matematica(
    linha,
):
    """
    Verifica se a escola atende aos três critérios
    de Prioritária em Matemática.

    Critérios:

        1. AVD1 Abaixo do Básico >= 50%
        2. PP2 < 50%
        3. PP2 < PP1
    """

    mat_abaixo = obter_avd1_abaixo(
        linha,
        "MAT",
    )

    mat_pp1 = linha.get(
        "MAT_PP1",
        pd.NA,
    )

    mat_pp2 = linha.get(
        "MAT_PP2",
        pd.NA,
    )

    # ------------------------------------------------------
    # Sem dados suficientes
    # ------------------------------------------------------

    if pd.isna(mat_abaixo):

        return False

    if pd.isna(mat_pp1):

        return False

    if pd.isna(mat_pp2):

        return False

    # ------------------------------------------------------
    # Regra congelada
    # ------------------------------------------------------

    return (
        mat_abaixo >= 0.50
        and mat_pp2 < 0.50
        and mat_pp2 < mat_pp1
    )


# ==========================================================
# SITUAÇÃO DE RISCO — LÍNGUA PORTUGUESA
# ==========================================================

def verificar_risco_lingua_portuguesa(
    linha,
):
    """
    Identifica se existe pelo menos um sinal de risco
    em Língua Portuguesa.

    Sinais considerados:

        - PP2 < 50%
        - evolução LP negativa
        - AVD1 Abaixo do Básico >= 50%

    A ausência de informação não é considerada risco.
    """

    sinais = []

    # ------------------------------------------------------
    # PP2
    # ------------------------------------------------------

    lp_pp2 = linha.get(
        "LP_PP2",
        pd.NA,
    )

    if pd.notna(lp_pp2):

        sinais.append(
            lp_pp2 < 0.50
        )

    # ------------------------------------------------------
    # Evolução
    # ------------------------------------------------------

    evolucao_lp = linha.get(
        "EVOLUCAO_LP",
        pd.NA,
    )

    if pd.notna(evolucao_lp):

        sinais.append(
            evolucao_lp < 0
        )

    # ------------------------------------------------------
    # AVD1
    # ------------------------------------------------------

    lp_abaixo = obter_avd1_abaixo(
        linha,
        "LP",
    )

    if pd.notna(lp_abaixo):

        sinais.append(
            lp_abaixo >= 0.50
        )

    return any(sinais)


# ==========================================================
# SITUAÇÃO DE RISCO — MATEMÁTICA
# ==========================================================

def verificar_risco_matematica(
    linha,
):
    """
    Identifica se existe pelo menos um sinal de risco
    em Matemática.

    Sinais considerados:

        - PP2 < 50%
        - evolução MAT negativa
        - AVD1 Abaixo do Básico >= 50%

    A ausência de informação não é considerada risco.
    """

    sinais = []

    # ------------------------------------------------------
    # PP2
    # ------------------------------------------------------

    mat_pp2 = linha.get(
        "MAT_PP2",
        pd.NA,
    )

    if pd.notna(mat_pp2):

        sinais.append(
            mat_pp2 < 0.50
        )

    # ------------------------------------------------------
    # Evolução
    # ------------------------------------------------------

    evolucao_mat = linha.get(
        "EVOLUCAO_MAT",
        pd.NA,
    )

    if pd.notna(evolucao_mat):

        sinais.append(
            evolucao_mat < 0
        )

    # ------------------------------------------------------
    # AVD1
    # ------------------------------------------------------

    mat_abaixo = obter_avd1_abaixo(
        linha,
        "MAT",
    )

    if pd.notna(mat_abaixo):

        sinais.append(
            mat_abaixo >= 0.50
        )

    return any(sinais)


# ==========================================================
# SITUAÇÃO PRINCIPAL DO FAROL
# ==========================================================

def classificar_farol(
    linha,
):
    """
    Classifica a situação principal da escola.

    Ordem:

        PRIORITÁRIA
        ATENÇÃO
        FAVORÁVEL
        SEM HISTÓRICO

    A classificação considera o histórico disponível
    até o momento da geração do Radar.
    """

    # ------------------------------------------------------
    # SEM HISTÓRICO
    # ------------------------------------------------------

    quantidade = linha.get(
        "QTD_AVALIACOES",
        0,
    )

    if pd.isna(quantidade):

        quantidade = 0

    if quantidade < 2:

        return "SEM HISTÓRICO"

    # ------------------------------------------------------
    # PRIORIDADE
    # ------------------------------------------------------

    prioridade_lp = (
        verificar_prioridade_linguaportuguesa(
            linha
        )
    )

    prioridade_mat = (
        verificar_prioridade_matematica(
            linha
        )
    )

    if prioridade_lp or prioridade_mat:

        return "PRIORITÁRIA"

    # ------------------------------------------------------
    # ATENÇÃO
    # ------------------------------------------------------

    risco_lp = (
        verificar_risco_lingua_portuguesa(
            linha
        )
    )

    risco_mat = (
        verificar_risco_matematica(
            linha
        )
    )

    if risco_lp or risco_mat:

        return "ATENÇÃO"

    # ------------------------------------------------------
    # FAVORÁVEL
    # ------------------------------------------------------

    return "FAVORÁVEL"


# ==========================================================
# COMPONENTES ENVOLVIDOS
# ==========================================================

def identificar_componentes(
    linha,
):
    """
    Identifica quais componentes apresentam situação
    prioritária ou sinal de atenção.

    Se houver prioridade:

        LÍNGUA PORTUGUESA
        e/ou
        MATEMÁTICA

    Caso não haja prioridade, mas exista risco:

        LÍNGUA PORTUGUESA
        e/ou
        MATEMÁTICA

    A prioridade é apresentada antes da atenção.
    """

    componentes_prioritarios = []

    componentes_atencao = []

    # ------------------------------------------------------
    # PRIORIDADE LP
    # ------------------------------------------------------

    prioridade_lp = (
        verificar_prioridade_linguaportuguesa(
            linha
        )
    )

    # ------------------------------------------------------
    # PRIORIDADE MAT
    # ------------------------------------------------------

    prioridade_mat = (
        verificar_prioridade_matematica(
            linha
        )
    )

    # ------------------------------------------------------
    # RISCO LP
    # ------------------------------------------------------

    risco_lp = (
        verificar_risco_lingua_portuguesa(
            linha
        )
    )

    # ------------------------------------------------------
    # RISCO MAT
    # ------------------------------------------------------

    risco_mat = (
        verificar_risco_matematica(
            linha
        )
    )

    # ------------------------------------------------------
    # COMPONENTE LP
    # ------------------------------------------------------

    if prioridade_lp:

        componentes_prioritarios.append(
            "LÍNGUA PORTUGUESA"
        )

    elif risco_lp:

        componentes_atencao.append(
            "LÍNGUA PORTUGUESA"
        )

    # ------------------------------------------------------
    # COMPONENTE MAT
    # ------------------------------------------------------

    if prioridade_mat:

        componentes_prioritarios.append(
            "MATEMÁTICA"
        )

    elif risco_mat:

        componentes_atencao.append(
            "MATEMÁTICA"
        )

    # ------------------------------------------------------
    # RETORNO
    # ------------------------------------------------------

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

def identificar_evolucao(
    linha,
):
    """
    Identifica evolução significativa em pelo menos
    um dos componentes.

    Critério V1:

        evolução >= 5 pontos percentuais.

    Como os valores são armazenados em escala decimal:

        5 pontos percentuais = 0.05
    """

    evolucoes = []

    # ------------------------------------------------------
    # LP
    # ------------------------------------------------------

    evolucao_lp = linha.get(
        "EVOLUCAO_LP",
        pd.NA,
    )

    if pd.notna(evolucao_lp):

        evolucoes.append(
            evolucao_lp
        )

    # ------------------------------------------------------
    # MAT
    # ------------------------------------------------------

    evolucao_mat = linha.get(
        "EVOLUCAO_MAT",
        pd.NA,
    )

    if pd.notna(evolucao_mat):

        evolucoes.append(
            evolucao_mat
        )

    # ------------------------------------------------------
    # Sem evolução disponível
    # ------------------------------------------------------

    if not evolucoes:

        return False

    # ------------------------------------------------------
    # Critério de destaque
    # ------------------------------------------------------

    return any(
        valor >= 0.05
        for valor in evolucoes
    )


# ==========================================================
# APLICAÇÃO DO FAROL
# ==========================================================

def aplicar_farol(
    base: pd.DataFrame,
) -> pd.DataFrame:
    """
    Aplica o Farol URE V1 à base consolidada.

    Não altera os dados originais.
    Retorna uma cópia da base com:

        FAROL_URE
        COMPONENTE_FAROL
        DESTAQUE_EVOLUCAO
    """

    if base is None or base.empty:

        return base

    # ------------------------------------------------------
    # Cópia de segurança
    # ------------------------------------------------------

    resultado = base.copy()

    # ------------------------------------------------------
    # Situação principal
    # ------------------------------------------------------

    resultado[
        "FAROL_URE"
    ] = resultado.apply(
        classificar_farol,
        axis=1,
    )

    # ------------------------------------------------------
    # Componentes envolvidos
    # ------------------------------------------------------

    resultado[
        "COMPONENTE_FAROL"
    ] = resultado.apply(
        identificar_componentes,
        axis=1,
    )

    # ------------------------------------------------------
    # Destaque de evolução
    # ------------------------------------------------------

    resultado[
        "DESTAQUE_EVOLUCAO"
    ] = resultado.apply(
        identificar_evolucao,
        axis=1,
    )

    return resultado
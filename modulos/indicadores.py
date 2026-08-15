"""
Responsabilidade:
Calcular os principais indicadores do Radar Pedagógico URE.

A função deste módulo é medir os dados.

A classificação do Farol, diagnóstico e encaminhamento
serão realizados em etapas posteriores.
"""

from datetime import datetime

import pandas as pd


# ==========================================================
# CONFIGURAÇÃO DAS AVALIAÇÕES
# ==========================================================

AVALIACOES = [
    "ADE",
    "PP1",
    "PP2",
    "ADP",
    "PP3",
]


# ==========================================================
# LOCALIZA A ÚLTIMA AVALIAÇÃO DISPONÍVEL
# ==========================================================

def obter_ultima_avaliacao(linha):
    """
    Identifica a última avaliação disponível para a escola.

    A ordem de prioridade é:

        PP3
        ADP
        PP2
        PP1
        ADE
    """

    for avaliacao in reversed(AVALIACOES):

        coluna_participacao = f"PART_{avaliacao}"

        if coluna_participacao in linha.index:

            valor = linha[coluna_participacao]

            if pd.notna(valor):
                return avaliacao

    return None


# ==========================================================
# EVOLUÇÃO
# ==========================================================

def calcular_evolucao(linha, componente):
    """
    Calcula a evolução entre as duas últimas avaliações
    disponíveis para o componente informado.

    Componente:
        LP
        MAT

    Retorno:
        diferença em pontos percentuais na escala decimal.

    Exemplo:

        PP1 = 0.40
        PP2 = 0.45

        evolução = +0.05
    """

    avaliacoes_disponiveis = []

    for avaliacao in [
        "PP1",
        "PP2",
        "ADP",
        "PP3",
    ]:

        coluna = f"{componente}_{avaliacao}"

        if coluna in linha.index:

            valor = linha[coluna]

            if pd.notna(valor):
                avaliacoes_disponiveis.append(
                    (avaliacao, float(valor))
                )

    if len(avaliacoes_disponiveis) < 2:
        return pd.NA

    anterior = avaliacoes_disponiveis[-2][1]
    atual = avaliacoes_disponiveis[-1][1]

    return atual - anterior


# ==========================================================
# EVOLUÇÃO DA PARTICIPAÇÃO
# ==========================================================

def calcular_evolucao_participacao(linha):
    """
    Calcula a evolução da participação entre as duas
    últimas avaliações disponíveis.
    """

    avaliacoes_disponiveis = []

    for avaliacao in AVALIACOES:

        coluna = f"PART_{avaliacao}"

        if coluna in linha.index:

            valor = linha[coluna]

            if pd.notna(valor):
                avaliacoes_disponiveis.append(
                    (avaliacao, float(valor))
                )

    if len(avaliacoes_disponiveis) < 2:
        return pd.NA

    anterior = avaliacoes_disponiveis[-2][1]
    atual = avaliacoes_disponiveis[-1][1]

    return atual - anterior


# ==========================================================
# INDICADORES POR ESCOLA
# ==========================================================

def calcular_indicadores_escolas(base: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula os indicadores individuais de cada escola.

    Esta função NÃO classifica o Farol.

    Ela apenas transforma os dados consolidados em
    indicadores objetivos que serão utilizados
    posteriormente pelo Farol, diagnóstico e encaminhamento.
    """

    if base is None or base.empty:
        return base

    resultado = base.copy()

    # ------------------------------------------------------
    # Última avaliação disponível
    # ------------------------------------------------------

    resultado["ULTIMA_AVALIACAO"] = resultado.apply(
        obter_ultima_avaliacao,
        axis=1,
    )

    # ------------------------------------------------------
    # Evolução de LP
    # ------------------------------------------------------

    resultado["EVOLUCAO_LP"] = resultado.apply(
        lambda linha: calcular_evolucao(
            linha,
            "LP",
        ),
        axis=1,
    )

    # ------------------------------------------------------
    # Evolução de MAT
    # ------------------------------------------------------

    resultado["EVOLUCAO_MAT"] = resultado.apply(
        lambda linha: calcular_evolucao(
            linha,
            "MAT",
        ),
        axis=1,
    )

    # ------------------------------------------------------
    # Evolução da participação
    # ------------------------------------------------------

    resultado["EVOLUCAO_PARTICIPACAO"] = (
        resultado.apply(
            calcular_evolucao_participacao,
            axis=1,
        )
    )

    # ------------------------------------------------------
    # Indicadores da última avaliação
    #
    # São preenchidos dinamicamente.
    # ------------------------------------------------------

    def obter_valor_ultima(linha, prefixo):
        avaliacao = linha["ULTIMA_AVALIACAO"]

        if not avaliacao:
            return pd.NA

        coluna = f"{prefixo}_{avaliacao}"

        if coluna not in linha.index:
            return pd.NA

        return linha[coluna]

    resultado["PARTICIPACAO_ATUAL"] = resultado.apply(
        lambda linha: obter_valor_ultima(
            linha,
            "PART",
        ),
        axis=1,
    )

    resultado["LP_ATUAL"] = resultado.apply(
        lambda linha: obter_valor_ultima(
            linha,
            "LP",
        ),
        axis=1,
    )

    resultado["MAT_ATUAL"] = resultado.apply(
        lambda linha: obter_valor_ultima(
            linha,
            "MAT",
        ),
        axis=1,
    )

    resultado["MEDIA_ATUAL"] = resultado.apply(
        lambda linha: obter_valor_ultima(
            linha,
            "MEDIA",
        ),
        axis=1,
    )

    # ------------------------------------------------------
    # Diferença LP x MAT na avaliação atual
    # ------------------------------------------------------

    resultado["DIF_LP_MAT_ATUAL"] = (
        resultado["LP_ATUAL"]
        - resultado["MAT_ATUAL"]
    )

    # ------------------------------------------------------
    # Quantidade de avaliações disponíveis
    # ------------------------------------------------------

    def contar_avaliacoes(linha):
        total = 0

        for avaliacao in AVALIACOES:

            coluna = f"PART_{avaliacao}"

            if coluna in linha.index:

                if pd.notna(linha[coluna]):
                    total += 1

        return total

    resultado["QTD_AVALIACOES"] = resultado.apply(
        contar_avaliacoes,
        axis=1,
    )

    # ------------------------------------------------------
    # Indicadores de presença de histórico
    # ------------------------------------------------------

    resultado["TEM_ADE"] = (
        resultado["PART_ADE"].notna()
        if "PART_ADE" in resultado.columns
        else False
    )

    resultado["TEM_PP1"] = (
        resultado["PART_PP1"].notna()
        if "PART_PP1" in resultado.columns
        else False
    )

    resultado["TEM_PP2"] = (
        resultado["PART_PP2"].notna()
        if "PART_PP2" in resultado.columns
        else False
    )

    resultado["TEM_ADP"] = (
        resultado["PART_ADP"].notna()
        if "PART_ADP" in resultado.columns
        else False
    )

    resultado["TEM_PP3"] = (
        resultado["PART_PP3"].notna()
        if "PART_PP3" in resultado.columns
        else False
    )

    # ------------------------------------------------------
    # Situação do histórico
    # ------------------------------------------------------

    def definir_historico(linha):

        quantidade = linha["QTD_AVALIACOES"]

        if quantidade <= 1:
            return "NOVA_NO_ACOMPANHAMENTO"

        if quantidade == 2:
            return "HISTORICO_INICIAL"

        return "HISTORICO_CONSOLIDADO"

    resultado["SITUACAO_HISTORICO"] = resultado.apply(
        definir_historico,
        axis=1,
    )

    return resultado


# ==========================================================
# INDICADORES GERAIS DA URE
# ==========================================================

def calcular_indicadores(base: pd.DataFrame) -> dict:
    """
    Calcula os indicadores gerais da URE.

    A função mantém o retorno em formato de dicionário
    para compatibilidade com o Resumo Executivo.

    A classificação do Farol NÃO é realizada aqui.
    """

    indicadores = {}

    if base is None or base.empty:

        indicadores["DATA_GERACAO"] = datetime.now()
        indicadores["TOTAL_ESCOLAS"] = 0
        indicadores["AVALIACOES"] = []

        return indicadores

    # ------------------------------------------------------
    # Informações gerais
    # ------------------------------------------------------

    indicadores["DATA_GERACAO"] = datetime.now()

    indicadores["TOTAL_ESCOLAS"] = len(base)

    # ------------------------------------------------------
    # Avaliações disponíveis
    # ------------------------------------------------------

    avaliacoes = []

    for avaliacao in AVALIACOES:

        coluna = f"PART_{avaliacao}"

        if coluna in base.columns:

            if base[coluna].notna().any():
                avaliacoes.append(avaliacao)

    indicadores["AVALIACOES"] = avaliacoes

    # ------------------------------------------------------
    # Participação média
    # ------------------------------------------------------

    for avaliacao in AVALIACOES:

        coluna = f"PART_{avaliacao}"

        if coluna in base.columns:

            indicadores[coluna] = (
                base[coluna].mean()
            )

    # ------------------------------------------------------
    # Médias gerais
    # ------------------------------------------------------

    for avaliacao in [
        "PP1",
        "PP2",
        "ADP",
        "PP3",
    ]:

        coluna = f"MEDIA_{avaliacao}"

        if coluna in base.columns:

            indicadores[coluna] = (
                base[coluna].mean()
            )

    # ------------------------------------------------------
    # Médias de LP
    # ------------------------------------------------------

    for avaliacao in [
        "PP1",
        "PP2",
        "ADP",
        "PP3",
    ]:

        coluna = f"LP_{avaliacao}"

        if coluna in base.columns:

            indicadores[coluna] = (
                base[coluna].mean()
            )

    # ------------------------------------------------------
    # Médias de MAT
    # ------------------------------------------------------

    for avaliacao in [
        "PP1",
        "PP2",
        "ADP",
        "PP3",
    ]:

        coluna = f"MAT_{avaliacao}"

        if coluna in base.columns:

            indicadores[coluna] = (
                base[coluna].mean()
            )

    # ------------------------------------------------------
    # Evolução média
    # ------------------------------------------------------

    if "EVOLUCAO_LP" in base.columns:

        indicadores["EVOLUCAO_MEDIA_LP"] = (
            pd.to_numeric(
                base["EVOLUCAO_LP"],
                errors="coerce",
            ).mean()
        )

    if "EVOLUCAO_MAT" in base.columns:

        indicadores["EVOLUCAO_MEDIA_MAT"] = (
            pd.to_numeric(
                base["EVOLUCAO_MAT"],
                errors="coerce",
            ).mean()
        )

    if "EVOLUCAO_PARTICIPACAO" in base.columns:

        indicadores["EVOLUCAO_MEDIA_PARTICIPACAO"] = (
            pd.to_numeric(
                base["EVOLUCAO_PARTICIPACAO"],
                errors="coerce",
            ).mean()
        )

    # ------------------------------------------------------
    # Histórico
    # ------------------------------------------------------

    if "SITUACAO_HISTORICO" in base.columns:

        indicadores["NOVAS_ESCOLAS"] = (
            base["SITUACAO_HISTORICO"]
            .eq("NOVA_NO_ACOMPANHAMENTO")
            .sum()
        )

        indicadores["HISTORICO_INICIAL"] = (
            base["SITUACAO_HISTORICO"]
            .eq("HISTORICO_INICIAL")
            .sum()
        )

        indicadores["HISTORICO_CONSOLIDADO"] = (
            base["SITUACAO_HISTORICO"]
            .eq("HISTORICO_CONSOLIDADO")
            .sum()
        )

    # ------------------------------------------------------
    # Compatibilidade temporária
    #
    # O Farol ainda não foi calculado.
    # Portanto, os contadores permanecem zerados.
    # ------------------------------------------------------

    indicadores["PRIORITARIA"] = 0
    indicadores["ATENCAO"] = 0
    indicadores["DESTAQUE"] = 0
    indicadores["SEM_DADOS"] = 0

    return indicadores
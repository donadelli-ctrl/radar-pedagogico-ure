"""
==========================================================
RADAR PEDAGÓGICO URE
MÓDULO: indicadores.py
Versão: 2.0
==========================================================

Responsabilidade:
Calcular os principais indicadores do Radar Pedagógico URE.

Este módulo mede os dados.

A classificação do Farol, diagnóstico e encaminhamento
são realizados em etapas próprias.

IMPORTANTE:

O Farol utilizado pelo Radar é o FAROL_URE.

O FAROL SARESP da Prova Paulista não é utilizado
para classificação da escola.
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

    Ordem:

        PP3
        ADP
        PP2
        PP1
        ADE
    """

    for avaliacao in reversed(AVALIACOES):

        coluna_participacao = (
            f"PART_{avaliacao}"
        )

        if coluna_participacao in linha.index:

            valor = linha[
                coluna_participacao
            ]

            if pd.notna(valor):

                return avaliacao

    return None


# ==========================================================
# EVOLUÇÃO
# ==========================================================

def calcular_evolucao(
    linha,
    componente,
):
    """
    Calcula a evolução entre as duas últimas
    avaliações disponíveis.

    Componente:

        LP
        MAT

    Retorno:

        diferença em escala decimal.

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

        coluna = (
            f"{componente}_{avaliacao}"
        )

        if coluna in linha.index:

            valor = linha[coluna]

            if pd.notna(valor):

                avaliacoes_disponiveis.append(
                    (
                        avaliacao,
                        float(valor),
                    )
                )

    if len(
        avaliacoes_disponiveis
    ) < 2:

        return pd.NA

    anterior = (
        avaliacoes_disponiveis[-2][1]
    )

    atual = (
        avaliacoes_disponiveis[-1][1]
    )

    return atual - anterior


# ==========================================================
# EVOLUÇÃO DA PARTICIPAÇÃO
# ==========================================================

def calcular_evolucao_participacao(
    linha,
):
    """
    Calcula a evolução da participação entre
    as duas últimas avaliações disponíveis.
    """

    avaliacoes_disponiveis = []

    for avaliacao in AVALIACOES:

        coluna = (
            f"PART_{avaliacao}"
        )

        if coluna in linha.index:

            valor = linha[coluna]

            if pd.notna(valor):

                avaliacoes_disponiveis.append(
                    (
                        avaliacao,
                        float(valor),
                    )
                )

    if len(
        avaliacoes_disponiveis
    ) < 2:

        return pd.NA

    anterior = (
        avaliacoes_disponiveis[-2][1]
    )

    atual = (
        avaliacoes_disponiveis[-1][1]
    )

    return atual - anterior


# ==========================================================
# INDICADORES POR ESCOLA
# ==========================================================

def calcular_indicadores_escolas(
    base: pd.DataFrame,
) -> pd.DataFrame:
    """
    Calcula os indicadores individuais de cada escola.

    Esta função NÃO classifica o Farol.

    Ela prepara os indicadores que serão utilizados
    pelo Farol, diagnóstico e encaminhamento.
    """

    if base is None or base.empty:

        return base

    resultado = base.copy()

    # ======================================================
    # ÚLTIMA AVALIAÇÃO DISPONÍVEL
    # ======================================================

    resultado[
        "ULTIMA_AVALIACAO"
    ] = resultado.apply(
        obter_ultima_avaliacao,
        axis=1,
    )

    # ======================================================
    # EVOLUÇÃO DE LP
    # ======================================================

    resultado[
        "EVOLUCAO_LP"
    ] = resultado.apply(
        lambda linha: calcular_evolucao(
            linha,
            "LP",
        ),
        axis=1,
    )

    # ======================================================
    # EVOLUÇÃO DE MAT
    # ======================================================

    resultado[
        "EVOLUCAO_MAT"
    ] = resultado.apply(
        lambda linha: calcular_evolucao(
            linha,
            "MAT",
        ),
        axis=1,
    )

    # ======================================================
    # EVOLUÇÃO DA PARTICIPAÇÃO
    # ======================================================

    resultado[
        "EVOLUCAO_PARTICIPACAO"
    ] = resultado.apply(
        calcular_evolucao_participacao,
        axis=1,
    )

    # ======================================================
    # VALOR DA ÚLTIMA AVALIAÇÃO
    # ======================================================

    def obter_valor_ultima(
        linha,
        prefixo,
    ):

        avaliacao = (
            linha["ULTIMA_AVALIACAO"]
        )

        if not avaliacao:

            return pd.NA

        coluna = (
            f"{prefixo}_{avaliacao}"
        )

        if coluna not in linha.index:

            return pd.NA

        return linha[coluna]

    # ------------------------------------------------------
    # PARTICIPAÇÃO ATUAL
    # ------------------------------------------------------

    resultado[
        "PARTICIPACAO_ATUAL"
    ] = resultado.apply(
        lambda linha: obter_valor_ultima(
            linha,
            "PART",
        ),
        axis=1,
    )

    # ------------------------------------------------------
    # LP ATUAL
    # ------------------------------------------------------

    resultado[
        "LP_ATUAL"
    ] = resultado.apply(
        lambda linha: obter_valor_ultima(
            linha,
            "LP",
        ),
        axis=1,
    )

    # ------------------------------------------------------
    # MAT ATUAL
    # ------------------------------------------------------

    resultado[
        "MAT_ATUAL"
    ] = resultado.apply(
        lambda linha: obter_valor_ultima(
            linha,
            "MAT",
        ),
        axis=1,
    )

    # ------------------------------------------------------
    # MÉDIA ATUAL
    # ------------------------------------------------------

    resultado[
        "MEDIA_ATUAL"
    ] = resultado.apply(
        lambda linha: obter_valor_ultima(
            linha,
            "MEDIA",
        ),
        axis=1,
    )

    # ======================================================
    # DIFERENÇA LP X MAT
    # ======================================================

    resultado[
        "DIF_LP_MAT_ATUAL"
    ] = (
        resultado["LP_ATUAL"]
        - resultado["MAT_ATUAL"]
    )

    # ======================================================
    # QUANTIDADE DE AVALIAÇÕES
    # ======================================================

    def contar_avaliacoes(
        linha,
    ):

        total = 0

        for avaliacao in AVALIACOES:

            coluna = (
                f"PART_{avaliacao}"
            )

            if coluna in linha.index:

                if pd.notna(
                    linha[coluna]
                ):

                    total += 1

        return total

    resultado[
        "QTD_AVALIACOES"
    ] = resultado.apply(
        contar_avaliacoes,
        axis=1,
    )

    # ======================================================
    # PRESENÇA DAS AVALIAÇÕES
    # ======================================================

    resultado["TEM_ADE"] = (
        resultado["PART_ADE"].notna()
        if "PART_ADE"
        in resultado.columns
        else False
    )

    resultado["TEM_PP1"] = (
        resultado["PART_PP1"].notna()
        if "PART_PP1"
        in resultado.columns
        else False
    )

    resultado["TEM_PP2"] = (
        resultado["PART_PP2"].notna()
        if "PART_PP2"
        in resultado.columns
        else False
    )

    resultado["TEM_ADP"] = (
        resultado["PART_ADP"].notna()
        if "PART_ADP"
        in resultado.columns
        else False
    )

    resultado["TEM_PP3"] = (
        resultado["PART_PP3"].notna()
        if "PART_PP3"
        in resultado.columns
        else False
    )

    # ======================================================
    # SITUAÇÃO DO HISTÓRICO
    # ======================================================

    def definir_historico(
        linha,
    ):

        quantidade = (
            linha["QTD_AVALIACOES"]
        )

        if quantidade <= 1:

            return (
                "NOVA_NO_ACOMPANHAMENTO"
            )

        if quantidade == 2:

            return (
                "HISTORICO_INICIAL"
            )

        return (
            "HISTORICO_CONSOLIDADO"
        )

    resultado[
        "SITUACAO_HISTORICO"
    ] = resultado.apply(
        definir_historico,
        axis=1,
    )

    return resultado


# ==========================================================
# INDICADORES GERAIS DA URE
# ==========================================================

def calcular_indicadores(
    base: pd.DataFrame,
) -> dict:
    """
    Calcula os indicadores gerais da URE.

    IMPORTANTE:

    A classificação principal é obtida diretamente
    da coluna FAROL_URE.

    O Farol SARESP da SEDUC não é utilizado.

    Também são calculados separadamente os destaques
    de evolução.
    """

    indicadores = {}

    # ======================================================
    # BASE VAZIA
    # ======================================================

    if base is None or base.empty:

        indicadores[
            "DATA_GERACAO"
        ] = datetime.now()

        indicadores[
            "TOTAL_ESCOLAS"
        ] = 0

        indicadores[
            "AVALIACOES"
        ] = []

        indicadores[
            "PRIORITARIA"
        ] = 0

        indicadores[
            "ATENCAO"
        ] = 0

        indicadores[
            "FAVORAVEL"
        ] = 0

        indicadores[
            "DESTAQUE_EVOLUCAO"
        ] = 0

        indicadores[
            "SEM_HISTORICO"
        ] = 0

        return indicadores

    # ======================================================
    # INFORMAÇÕES GERAIS
    # ======================================================

    indicadores[
        "DATA_GERACAO"
    ] = datetime.now()

    indicadores[
        "TOTAL_ESCOLAS"
    ] = len(base)

    # ======================================================
    # AVALIAÇÕES DISPONÍVEIS
    # ======================================================

    avaliacoes = []

    for avaliacao in AVALIACOES:

        coluna = (
            f"PART_{avaliacao}"
        )

        if coluna in base.columns:

            if base[
                coluna
            ].notna().any():

                avaliacoes.append(
                    avaliacao
                )

    indicadores[
        "AVALIACOES"
    ] = avaliacoes

    # ======================================================
    # PARTICIPAÇÃO MÉDIA
    # ======================================================

    for avaliacao in AVALIACOES:

        coluna = (
            f"PART_{avaliacao}"
        )

        if coluna in base.columns:

            indicadores[
                coluna
            ] = base[coluna].mean()

    # ======================================================
    # MÉDIAS GERAIS
    # ======================================================

    for avaliacao in [
        "PP1",
        "PP2",
        "ADP",
        "PP3",
    ]:

        coluna = (
            f"MEDIA_{avaliacao}"
        )

        if coluna in base.columns:

            indicadores[
                coluna
            ] = base[coluna].mean()

    # ======================================================
    # MÉDIAS DE LP
    # ======================================================

    for avaliacao in [
        "PP1",
        "PP2",
        "ADP",
        "PP3",
    ]:

        coluna = (
            f"LP_{avaliacao}"
        )

        if coluna in base.columns:

            indicadores[
                coluna
            ] = base[coluna].mean()

    # ======================================================
    # MÉDIAS DE MAT
    # ======================================================

    for avaliacao in [
        "PP1",
        "PP2",
        "ADP",
        "PP3",
    ]:

        coluna = (
            f"MAT_{avaliacao}"
        )

        if coluna in base.columns:

            indicadores[
                coluna
            ] = base[coluna].mean()

    # ======================================================
    # EVOLUÇÃO MÉDIA
    # ======================================================

    if "EVOLUCAO_LP" in base.columns:

        indicadores[
            "EVOLUCAO_MEDIA_LP"
        ] = pd.to_numeric(
            base["EVOLUCAO_LP"],
            errors="coerce",
        ).mean()

    if "EVOLUCAO_MAT" in base.columns:

        indicadores[
            "EVOLUCAO_MEDIA_MAT"
        ] = pd.to_numeric(
            base["EVOLUCAO_MAT"],
            errors="coerce",
        ).mean()

    if (
        "EVOLUCAO_PARTICIPACAO"
        in base.columns
    ):

        indicadores[
            "EVOLUCAO_MEDIA_PARTICIPACAO"
        ] = pd.to_numeric(
            base[
                "EVOLUCAO_PARTICIPACAO"
            ],
            errors="coerce",
        ).mean()

    # ======================================================
    # HISTÓRICO
    # ======================================================

    if (
        "SITUACAO_HISTORICO"
        in base.columns
    ):

        indicadores[
            "NOVAS_ESCOLAS"
        ] = (
            base[
                "SITUACAO_HISTORICO"
            ]
            .eq(
                "NOVA_NO_ACOMPANHAMENTO"
            )
            .sum()
        )

        indicadores[
            "HISTORICO_INICIAL"
        ] = (
            base[
                "SITUACAO_HISTORICO"
            ]
            .eq(
                "HISTORICO_INICIAL"
            )
            .sum()
        )

        indicadores[
            "HISTORICO_CONSOLIDADO"
        ] = (
            base[
                "SITUACAO_HISTORICO"
            ]
            .eq(
                "HISTORICO_CONSOLIDADO"
            )
            .sum()
        )

    # ======================================================
    # FAROL URE
    # ======================================================

    # Inicializa todos os contadores.

    indicadores[
        "PRIORITARIA"
    ] = 0

    indicadores[
        "ATENCAO"
    ] = 0

    indicadores[
        "FAVORAVEL"
    ] = 0

    indicadores[
        "SEM_HISTORICO"
    ] = 0

    # ------------------------------------------------------
    # Conta a situação principal do Farol
    # ------------------------------------------------------

    if "FAROL_URE" in base.columns:

        farol = (
            base["FAROL_URE"]
            .astype("string")
            .str.upper()
            .str.strip()
        )

        indicadores[
            "PRIORITARIA"
        ] = int(
            farol.eq(
                "PRIORITÁRIA"
            ).sum()
        )

        indicadores[
            "ATENCAO"
        ] = int(
            farol.eq(
                "ATENÇÃO"
            ).sum()
        )

        indicadores[
            "FAVORAVEL"
        ] = int(
            farol.eq(
                "FAVORÁVEL"
            ).sum()
        )

        indicadores[
            "SEM_HISTORICO"
        ] = int(
            farol.eq(
                "SEM HISTÓRICO"
            ).sum()
        )

    # ======================================================
    # DESTAQUE DE EVOLUÇÃO
    # ======================================================

    indicadores[
        "DESTAQUE_EVOLUCAO"
    ] = 0

    if (
        "DESTAQUE_EVOLUCAO"
        in base.columns
    ):

        indicadores[
            "DESTAQUE_EVOLUCAO"
        ] = int(
            base[
                "DESTAQUE_EVOLUCAO"
            ]
            .fillna(False)
            .astype(bool)
            .sum()
        )

    # ======================================================
    # COMPATIBILIDADE
    # ======================================================

    # Mantém a chave DESTAQUE para versões
    # anteriores do resumo.

    indicadores[
        "DESTAQUE"
    ] = indicadores[
        "DESTAQUE_EVOLUCAO"
    ]

    # Também disponibiliza SEM_DADOS
    # para compatibilidade com versões anteriores.

    indicadores[
        "SEM_DADOS"
    ] = indicadores[
        "SEM_HISTORICO"
    ]

    return indicadores
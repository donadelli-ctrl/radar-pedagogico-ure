# ==========================================================
# RADAR PEDAGÓGICO URE
# MÓDULO: indicadores.py
# Versão: 3.1
# Arquitetura: AVD1 + PP1 + PP2 + AVD2 + PP3
# ==========================================================

from datetime import datetime

import pandas as pd


AVALIACOES = ["AVD1", "PP1", "PP2", "AVD2", "PP3"]


# ==========================================================
# FUNÇÕES AUXILIARES
# ==========================================================

def _primeira_coluna_existente(linha, colunas):
    for coluna in colunas:
        if coluna in linha.index and pd.notna(linha[coluna]):
            return linha[coluna]

    return pd.NA


def _primeira_coluna_base(base, colunas):
    for coluna in colunas:
        if coluna in base.columns:
            return coluna

    return None


def _valor_numerico(valor):
    try:
        if pd.isna(valor):
            return pd.NA

        return float(valor)

    except (TypeError, ValueError):
        return pd.NA


# ==========================================================
# COMPATIBILIDADE DO ADP
# ==========================================================

def _garantir_participacao_avd2(base):
    """
    O arquivo ADP contém AVD1 + AVD2 no mesmo arquivo.

    O leitor_adp mantém a participação atual do ADP em
    PART_ADP. Para o histórico do Radar, essa participação
    corresponde à AVD2.

    Portanto:

        PART_ADP -> PART_AVD2

    somente quando PART_AVD2 ainda não existir.

    Não é criada PART_AVD1 artificialmente.
    """

    resultado = base.copy()

    if (
        "PART_AVD2" not in resultado.columns
        and "PART_ADP" in resultado.columns
    ):
        resultado["PART_AVD2"] = resultado["PART_ADP"]

    return resultado


# ==========================================================
# IDENTIFICAÇÃO DA EXISTÊNCIA DE CADA AVALIAÇÃO
# ==========================================================

def _tem_avaliacao(linha, avaliacao):
    """
    Identifica se a escola possui dados para determinada avaliação.

    IMPORTANTE:

    AVD1 e AVD2 estão no mesmo arquivo ADP e não possuem,
    necessariamente, uma coluna PART_AVD1/PART_AVD2 independente.

    Por isso a existência da avaliação é determinada pelos
    dados efetivamente disponíveis.

    Ausência de dados permanece ausência.
    """

    avaliacao = str(avaliacao).strip().upper()

    if avaliacao == "AVD1":

        colunas = [
            "LP_AVD1_ABAIXO",
            "MAT_AVD1_ABAIXO",
            "LP_AVD1_ABAIXO_ANALISE",
            "MAT_AVD1_ABAIXO_ANALISE",
        ]

    elif avaliacao == "AVD2":

        colunas = [
            "LP_AVD2_ABAIXO",
            "MAT_AVD2_ABAIXO",
            "LP_AVD2_ABAIXO_ANALISE",
            "MAT_AVD2_ABAIXO_ANALISE",
            "LP_ADP_ABAIXO",
            "MAT_ADP_ABAIXO",
            "ADP_LP_ABAIXO",
            "ADP_MAT_ABAIXO",
            "PART_AVD2",
            "PART_ADP",
        ]

    elif avaliacao in ("PP1", "PP2", "PP3"):

        colunas = [
            f"LP_{avaliacao}",
            f"MAT_{avaliacao}",
            f"MEDIA_{avaliacao}",
            f"PART_{avaliacao}",
        ]

    else:
        return False

    for coluna in colunas:

        if coluna not in linha.index:
            continue

        valor = linha[coluna]

        if pd.notna(valor):

            if isinstance(valor, str) and valor.strip() == "":
                continue

            return True

    return False


# ==========================================================
# ÚLTIMA AVALIAÇÃO
# ==========================================================

def obter_ultima_avaliacao(linha):
    """
    Retorna a última avaliação disponível na sequência:

        AVD1 → PP1 → PP2 → AVD2 → PP3

    A existência da avaliação não depende exclusivamente
    da participação.
    """

    for avaliacao in reversed(AVALIACOES):

        if _tem_avaliacao(linha, avaliacao):
            return avaliacao

    return None


# ==========================================================
# EVOLUÇÃO
# ==========================================================

def calcular_evolucao(linha, componente):
    valores = []

    for avaliacao in AVALIACOES:

        coluna = f"{componente}_{avaliacao}"

        if coluna not in linha.index:
            continue

        valor = _valor_numerico(
            linha[coluna]
        )

        if pd.notna(valor):
            valores.append(
                (
                    avaliacao,
                    valor,
                )
            )

    if len(valores) < 2:
        return pd.NA

    return (
        valores[-1][1]
        - valores[-2][1]
    )


def calcular_evolucao_participacao(linha):
    valores = []

    for avaliacao in AVALIACOES:

        coluna = f"PART_{avaliacao}"

        if coluna not in linha.index:
            continue

        valor = _valor_numerico(
            linha[coluna]
        )

        if pd.notna(valor):

            valores.append(
                (
                    avaliacao,
                    valor,
                )
            )

    if len(valores) < 2:
        return pd.NA

    return (
        valores[-1][1]
        - valores[-2][1]
    )


# ==========================================================
# ABAIXO DO BÁSICO — AVD1 / AVD2
# ==========================================================

def obter_abaixo_basico(
    linha,
    avaliacao,
    componente,
):
    """
    Obtém o Abaixo do Básico de AVD1 ou AVD2.
    """

    avaliacao = str(
        avaliacao
    ).strip().upper()

    componente = str(
        componente
    ).strip().upper()

    if avaliacao not in (
        "AVD1",
        "AVD2",
    ):
        return pd.NA

    if componente == "LP":

        colunas = [
            f"LP_{avaliacao}_ABAIXO"
        ]

        if avaliacao == "AVD2":

            colunas += [
                "LP_ADP_ABAIXO",
                "ADP_LP_ABAIXO",
                "ADP_ABAIXO_LP",
            ]

    elif componente == "MAT":

        colunas = [
            f"MAT_{avaliacao}_ABAIXO"
        ]

        if avaliacao == "AVD2":

            colunas += [
                "MAT_ADP_ABAIXO",
                "ADP_MAT_ABAIXO",
                "ADP_ABAIXO_MAT",
            ]

    else:
        return pd.NA

    return _primeira_coluna_existente(
        linha,
        colunas,
    )


# ==========================================================
# INDICADORES POR ESCOLA
# ==========================================================

def calcular_indicadores_escolas(
    base: pd.DataFrame,
) -> pd.DataFrame:

    if base is None or base.empty:
        return base

    resultado = _garantir_participacao_avd2(
        base
    )

    # ------------------------------------------------------
    # ÚLTIMA AVALIAÇÃO
    # ------------------------------------------------------

    resultado["ULTIMA_AVALIACAO"] = (
        resultado.apply(
            obter_ultima_avaliacao,
            axis=1,
        )
    )

    # ------------------------------------------------------
    # EVOLUÇÃO
    # ------------------------------------------------------

    resultado["EVOLUCAO_LP"] = (
        resultado.apply(
            lambda linha:
                calcular_evolucao(
                    linha,
                    "LP",
                ),
            axis=1,
        )
    )

    resultado["EVOLUCAO_MAT"] = (
        resultado.apply(
            lambda linha:
                calcular_evolucao(
                    linha,
                    "MAT",
                ),
            axis=1,
        )
    )

    resultado["EVOLUCAO_PARTICIPACAO"] = (
        resultado.apply(
            calcular_evolucao_participacao,
            axis=1,
        )
    )

    # ------------------------------------------------------
    # VALOR ATUAL
    # ------------------------------------------------------

    def obter_valor_ultima(
        linha,
        prefixo,
    ):

        avaliacao = linha[
            "ULTIMA_AVALIACAO"
        ]

        if not avaliacao:
            return pd.NA

        coluna = (
            f"{prefixo}_{avaliacao}"
        )

        if coluna not in linha.index:
            return pd.NA

        return linha[coluna]

    for nome, prefixo in [
        (
            "PARTICIPACAO_ATUAL",
            "PART",
        ),
        (
            "LP_ATUAL",
            "LP",
        ),
        (
            "MAT_ATUAL",
            "MAT",
        ),
        (
            "MEDIA_ATUAL",
            "MEDIA",
        ),
    ]:

        resultado[nome] = (
            resultado.apply(
                lambda linha,
                p=prefixo:
                    obter_valor_ultima(
                        linha,
                        p,
                    ),
                axis=1,
            )
        )

    # ------------------------------------------------------
    # AVD1
    # ------------------------------------------------------

    resultado[
        "LP_AVD1_ABAIXO_ANALISE"
    ] = resultado.apply(
        lambda linha:
            obter_abaixo_basico(
                linha,
                "AVD1",
                "LP",
            ),
        axis=1,
    )

    resultado[
        "MAT_AVD1_ABAIXO_ANALISE"
    ] = resultado.apply(
        lambda linha:
            obter_abaixo_basico(
                linha,
                "AVD1",
                "MAT",
            ),
        axis=1,
    )

    # ------------------------------------------------------
    # AVD2
    # ------------------------------------------------------

    resultado[
        "LP_AVD2_ABAIXO_ANALISE"
    ] = resultado.apply(
        lambda linha:
            obter_abaixo_basico(
                linha,
                "AVD2",
                "LP",
            ),
        axis=1,
    )

    resultado[
        "MAT_AVD2_ABAIXO_ANALISE"
    ] = resultado.apply(
        lambda linha:
            obter_abaixo_basico(
                linha,
                "AVD2",
                "MAT",
            ),
        axis=1,
    )

    # ------------------------------------------------------
    # DIFERENÇA LP x MAT
    # ------------------------------------------------------

    resultado[
        "DIF_LP_MAT_ATUAL"
    ] = (
        pd.to_numeric(
            resultado["LP_ATUAL"],
            errors="coerce",
        )
        -
        pd.to_numeric(
            resultado["MAT_ATUAL"],
            errors="coerce",
        )
    )

    # ------------------------------------------------------
    # QUANTIDADE DE AVALIAÇÕES
    # ------------------------------------------------------

    resultado[
        "QTD_AVALIACOES"
    ] = resultado.apply(
        lambda linha:
            sum(
                _tem_avaliacao(
                    linha,
                    avaliacao,
                )
                for avaliacao in AVALIACOES
            ),
        axis=1,
    )

    # ------------------------------------------------------
    # PRESENÇA EM CADA AVALIAÇÃO
    # ------------------------------------------------------

    for avaliacao in AVALIACOES:

        resultado[
            f"TEM_{avaliacao}"
        ] = resultado.apply(
            lambda linha,
            a=avaliacao:
                _tem_avaliacao(
                    linha,
                    a,
                ),
            axis=1,
        )

    # ------------------------------------------------------
    # SITUAÇÃO DO HISTÓRICO
    # ------------------------------------------------------

    def definir_historico(
        linha
    ):

        quantidade = int(
            linha[
                "QTD_AVALIACOES"
            ]
        )

        if quantidade <= 1:
            return "NOVA_NO_ACOMPANHAMENTO"

        if quantidade == 2:
            return "HISTORICO_INICIAL"

        return "HISTORICO_CONSOLIDADO"

    resultado[
        "SITUACAO_HISTORICO"
    ] = resultado.apply(
        definir_historico,
        axis=1,
    )

    return resultado


# ==========================================================
# INDICADORES GERAIS
# ==========================================================

def calcular_indicadores(
    base: pd.DataFrame,
) -> dict:

    indicadores = {
        "DATA_GERACAO": datetime.now(),
        "TOTAL_ESCOLAS": 0,
        "AVALIACOES": [],
    }

    if base is None or base.empty:
        return indicadores

    base = _garantir_participacao_avd2(
        base
    )

    indicadores[
        "TOTAL_ESCOLAS"
    ] = len(base)

    # ------------------------------------------------------
    # AVALIAÇÕES DISPONÍVEIS
    # ------------------------------------------------------

    base_indicadores = (
        calcular_indicadores_escolas(
            base
        )
    )

    for avaliacao in AVALIACOES:

        coluna = (
            f"PART_{avaliacao}"
        )

        possui = base_indicadores.apply(
            lambda linha,
            a=avaliacao:
                _tem_avaliacao(
                    linha,
                    a,
                ),
            axis=1,
        ).any()

        if possui:
            indicadores[
                "AVALIACOES"
            ].append(
                avaliacao
            )

        if coluna in base.columns:

            indicadores[
                coluna
            ] = pd.to_numeric(
                base[coluna],
                errors="coerce",
            ).mean()

    # ------------------------------------------------------
    # DIAGNÓSTICOS AVD1 / AVD2
    # ------------------------------------------------------

    campos_diagnosticos = {

        "ABAIXO_BASICO_LP_AVD1": [
            "LP_AVD1_ABAIXO",
            "LP_AVD1_ABAIXO_ANALISE",
        ],

        "ABAIXO_BASICO_MAT_AVD1": [
            "MAT_AVD1_ABAIXO",
            "MAT_AVD1_ABAIXO_ANALISE",
        ],

        "ABAIXO_BASICO_LP_AVD2": [
            "LP_AVD2_ABAIXO",
            "LP_AVD2_ABAIXO_ANALISE",
            "LP_ADP_ABAIXO",
            "ADP_LP_ABAIXO",
        ],

        "ABAIXO_BASICO_MAT_AVD2": [
            "MAT_AVD2_ABAIXO",
            "MAT_AVD2_ABAIXO_ANALISE",
            "MAT_ADP_ABAIXO",
            "ADP_MAT_ABAIXO",
        ],
    }

    for nome, colunas in (
        campos_diagnosticos.items()
    ):

        coluna = (
            _primeira_coluna_base(
                base,
                colunas,
            )
        )

        if coluna is not None:

            indicadores[
                nome
            ] = pd.to_numeric(
                base[coluna],
                errors="coerce",
            ).mean()

    # ------------------------------------------------------
    # MÉDIAS DAS PP
    # ------------------------------------------------------

    for avaliacao in [
        "PP1",
        "PP2",
        "PP3",
    ]:

        for prefixo in [
            "MEDIA",
            "LP",
            "MAT",
        ]:

            coluna = (
                f"{prefixo}_{avaliacao}"
            )

            if coluna in base.columns:

                indicadores[
                    coluna
                ] = pd.to_numeric(
                    base[coluna],
                    errors="coerce",
                ).mean()

    # ------------------------------------------------------
    # MÉDIAS DE EVOLUÇÃO
    # ------------------------------------------------------

    for coluna_base, nome in [

        (
            "EVOLUCAO_LP",
            "EVOLUCAO_MEDIA_LP",
        ),

        (
            "EVOLUCAO_MAT",
            "EVOLUCAO_MEDIA_MAT",
        ),

        (
            "EVOLUCAO_PARTICIPACAO",
            "EVOLUCAO_MEDIA_PARTICIPACAO",
        ),
    ]:

        if coluna_base in base_indicadores.columns:

            indicadores[
                nome
            ] = pd.to_numeric(
                base_indicadores[
                    coluna_base
                ],
                errors="coerce",
            ).mean()

    # ------------------------------------------------------
    # HISTÓRICO
    # ------------------------------------------------------

    if (
        "SITUACAO_HISTORICO"
        in base_indicadores.columns
    ):

        indicadores[
            "NOVAS_ESCOLAS"
        ] = int(
            base_indicadores[
                "SITUACAO_HISTORICO"
            ].eq(
                "NOVA_NO_ACOMPANHAMENTO"
            ).sum()
        )

        indicadores[
            "HISTORICO_INICIAL"
        ] = int(
            base_indicadores[
                "SITUACAO_HISTORICO"
            ].eq(
                "HISTORICO_INICIAL"
            ).sum()
        )

        indicadores[
            "HISTORICO_CONSOLIDADO"
        ] = int(
            base_indicadores[
                "SITUACAO_HISTORICO"
            ].eq(
                "HISTORICO_CONSOLIDADO"
            ).sum()
        )

    # ------------------------------------------------------
    # FAROL
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # DESTAQUES
    # ------------------------------------------------------

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

    indicadores[
        "DESTAQUE"
    ] = indicadores[
        "DESTAQUE_EVOLUCAO"
    ]

    indicadores[
        "SEM_DADOS"
    ] = indicadores[
        "SEM_HISTORICO"
    ]

    return indicadores

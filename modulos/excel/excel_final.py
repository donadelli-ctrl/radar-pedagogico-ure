# ==========================================================
# RADAR PEDAGÓGICO URE
# MÓDULO: excel_final.py
# Versão: 2.3
# Arquitetura: AVD1 + PP1 + PP2 + AVD2 + PP3
# ==========================================================

from io import BytesIO

import pandas as pd

from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

from modulos.indicadores import calcular_indicadores_escolas


# ==========================================================
# ESTILOS
# ==========================================================

CABECALHO_FILL = PatternFill(
    fill_type="solid",
    fgColor="1F4E79",
)

CABECALHO_FONT = Font(
    bold=True,
    color="FFFFFF",
)

CENTRO = Alignment(
    horizontal="center",
    vertical="center",
)

ESQUERDA = Alignment(
    horizontal="left",
    vertical="center",
)

COR_PRIORITARIA = PatternFill(
    fill_type="solid",
    fgColor="F4CCCC",
)

COR_ATENCAO = PatternFill(
    fill_type="solid",
    fgColor="FFF2CC",
)

COR_DESTAQUE = PatternFill(
    fill_type="solid",
    fgColor="D9EAD3",
)

COR_SEM_DADOS = PatternFill(
    fill_type="solid",
    fgColor="E6E6E6",
)

# Cores das classificações de desempenho
COR_FONTE_ABAIXO = "C00000"
COR_FONTE_BASICO = "BF9000"
COR_FONTE_ADEQUADO = "008000"
COR_FONTE_PROFICIENTE = "0070C0"



# ==========================================================
# COMPATIBILIDADE
# ==========================================================

def _garantir_colunas_adp(df):
    """
    Mantém compatibilidade caso algum arquivo/base antiga
    ainda apresente os nomes ADP.

    No resultado final, os dados da ADP ficam identificados
    como AVD2.
    """

    df = df.copy()

    mapa = {
        "LP_ADP_ABAIXO": "LP_AVD2_ABAIXO",
        "MAT_ADP_ABAIXO": "MAT_AVD2_ABAIXO",
        "PART_ADP": "PART_AVD2",
        "ADP_LP_ABAIXO": "LP_AVD2_ABAIXO",
        "ADP_MAT_ABAIXO": "MAT_AVD2_ABAIXO",
        "ADP_PART": "PART_AVD2",
    }

    for origem, destino in mapa.items():
        if destino not in df.columns and origem in df.columns:
            df[destino] = df[origem]

    return df


# ==========================================================
# FORMATAÇÃO DA PLANILHA
# ==========================================================

def _formatar_planilha(ws):
    """Formatação final da planilha pedagógica.

    Os cabeçalhos são amigáveis e usam quebra automática para que
    nenhum título técnico fique cortado. Textos longos permanecem
    na mesma linha da escola, dentro da própria célula.
    """

    # Cabeçalho
    for cell in ws[1]:
        cell.fill = CABECALHO_FILL
        cell.font = CABECALHO_FONT
        cell.alignment = Alignment(
            horizontal="center",
            vertical="center",
            wrap_text=True,
        )

    ws.row_dimensions[1].height = 42

    # Linhas de separação para melhorar a leitura visual.
    # A grade é discreta e mantém a planilha limpa, mas deixa
    # cada escola e cada bloco de informação visualmente separados.
    borda_grade = Border(
        left=Side(style="thin", color="D9E2F3"),
        right=Side(style="thin", color="D9E2F3"),
        top=Side(style="thin", color="D9E2F3"),
        bottom=Side(style="thin", color="D9E2F3"),
    )

    borda_cabecalho = Border(
        left=Side(style="thin", color="D9E2F3"),
        right=Side(style="thin", color="D9E2F3"),
        top=Side(style="thin", color="D9E2F3"),
        bottom=Side(style="medium", color="1F4E79"),
    )

    for cell in ws[1]:
        cell.border = borda_cabecalho

    for linha in ws.iter_rows(min_row=2):
        for cell in linha:
            cell.border = borda_grade

    for coluna in ws.columns:
        letra = get_column_letter(coluna[0].column)
        cabecalho = str(coluna[0].value or "").strip().upper()

        for cell in coluna[1:]:
            if cabecalho in ("DIAGNÓSTICO", "ENCAMINHAMENTO"):
                if isinstance(cell.value, str):
                    partes = [
                        parte.strip()
                        for parte in cell.value.replace(" | ", "\n").split("\n")
                        if parte.strip()
                    ]

                    blocos = []
                    for parte in partes:
                        inicio = parte.lower()

                        if inicio.startswith("língua portuguesa:") or inicio.startswith("matemática:"):
                            blocos.append(parte)
                        elif "matemática" in inicio and "língua portuguesa" not in inicio:
                            blocos.append(f"Matemática: {parte}")
                        else:
                            blocos.append(f"Língua Portuguesa: {parte}")

                    cell.value = "\n\n".join(blocos)

                cell.alignment = Alignment(
                    horizontal="left",
                    vertical="top",
                    wrap_text=True,
                )
            elif cabecalho == "ESCOLA":
                cell.alignment = Alignment(
                    horizontal="left",
                    vertical="center",
                    wrap_text=True,
                )
            else:
                cell.alignment = CENTRO

        # Larguras pensadas para leitura, sem deixar a planilha
        # excessivamente larga. Os cabeçalhos quebram em duas ou
        # mais linhas quando necessário.
        larguras = {
            "ESCOLA": 36,
            "DIAGNÓSTICO": 58,
            "ENCAMINHAMENTO": 58,
            "SITUAÇÃO PEDAGÓGICA": 22,
            "PARTICIPAÇÃO\nATUAL": 16,
            "PARTICIPAÇÃO ATUAL": 16,
            "EVOLUÇÃO\nLP": 14,
            "EVOLUÇÃO\nMAT": 14,
            "EVOLUÇÃO\nPARTICIPAÇÃO (p.p.)": 20,
            "LP – PP1": 13,
            "MAT – PP1": 13,
            "LP – PP2": 13,
            "MAT – PP2": 13,
            "LP – PP3": 13,
            "MAT – PP3": 13,
            "LP – AVD1\nABAIXO DO BÁSICO": 16,
            "MAT – AVD1\nABAIXO DO BÁSICO": 16,
            "LP – AVD2\nABAIXO DO BÁSICO": 16,
            "MAT – AVD2\nABAIXO DO BÁSICO": 16,
            "PART. – AVD1": 14,
            "PART. – PP1": 14,
            "PART. – PP2": 14,
            "PART. – AVD2": 14,
            "PART. – PP3": 14,
            "LP\nATUAL": 13,
            "MAT\nATUAL": 13,
            "MÉDIA\nATUAL": 13,
        }

        largura = larguras.get(cabecalho, 15)
        ws.column_dimensions[letra].width = largura

    # Altura das linhas: uma linha por escola, com espaço para os
    # textos de diagnóstico/encaminhamento.
    tem_texto = any(
        str(ws.cell(1, c).value or "").strip().upper()
        in {"DIAGNÓSTICO", "ENCAMINHAMENTO"}
        for c in range(1, ws.max_column + 1)
    )

    if tem_texto:
        for linha in range(2, ws.max_row + 1):
            ws.row_dimensions[linha].height = 120

    # Percentuais
    percentuais = {
        "PART. – AVD1",
        "PART. – PP1",
        "PART. – PP2",
        "PART. – AVD2",
        "PART. – PP3",
        "PARTICIPAÇÃO ATUAL",
        "PARTICIPAÇÃO\nATUAL",
        "LP – AVD1\nABAIXO DO BÁSICO",
        "MAT – AVD1\nABAIXO DO BÁSICO",
        "LP – AVD2\nABAIXO DO BÁSICO",
        "MAT – AVD2\nABAIXO DO BÁSICO",
        "EVOLUÇÃO\nLP",
        "EVOLUÇÃO\nMAT",
        "EVOLUÇÃO\nPARTICIPAÇÃO (p.p.)",
        "LP – PP1",
        "MAT – PP1",
        "LP – PP2",
        "MAT – PP2",
        "LP – PP3",
        "MAT – PP3",
        "LP\nATUAL",
        "MAT\nATUAL",
        "MÉDIA\nATUAL",
    }

    for coluna in ws.columns:
        cabecalho = str(coluna[0].value or "").strip().upper()
        if cabecalho in percentuais:
            for cell in coluna[1:]:
                if isinstance(cell.value, (int, float)):
                    cell.number_format = "0.0%"

    ws.freeze_panes = "B2"
    ws.auto_filter.ref = ws.dimensions


# ==========================================================
# ORDENAÇÃO DAS COLUNAS
# ==========================================================

def _ordenar_colunas(df):
    """Seleciona e renomeia somente as informações pedagógicas.

    As colunas técnicas continuam no DataFrame durante o processamento,
    mas não aparecem na planilha final.
    """

    desejadas = [
        "ESCOLA",
        "LP_AVD1_ABAIXO",
        "MAT_AVD1_ABAIXO",
        "PART_AVD1",
        "LP_PP1",
        "MAT_PP1",
        "PART_PP1",
        "LP_PP2",
        "MAT_PP2",
        "PART_PP2",
        "LP_AVD2_ABAIXO",
        "MAT_AVD2_ABAIXO",
        "PART_AVD2",
        "LP_PP3",
        "MAT_PP3",
        "PART_PP3",
        "EVOLUCAO_LP",
        "EVOLUCAO_MAT",
        "EVOLUCAO_PARTICIPACAO",
        "PARTICIPACAO_ATUAL",
        "LP_ATUAL",
        "MAT_ATUAL",
        "MEDIA_ATUAL",
        "FAROL_URE",
        "DIAGNOSTICO",
        "ENCAMINHAMENTO",
    ]

    presentes = [c for c in desejadas if c in df.columns]
    resultado = df[presentes].copy()

    nomes = {
        "LP_AVD1_ABAIXO": "LP – AVD1\nAbaixo do Básico",
        "MAT_AVD1_ABAIXO": "MAT – AVD1\nAbaixo do Básico",
        "PART_AVD1": "PART. – AVD1",
        "LP_PP1": "LP – PP1",
        "MAT_PP1": "MAT – PP1",
        "PART_PP1": "PART. – PP1",
        "LP_PP2": "LP – PP2",
        "MAT_PP2": "MAT – PP2",
        "PART_PP2": "PART. – PP2",
        "LP_AVD2_ABAIXO": "LP – AVD2\nAbaixo do Básico",
        "MAT_AVD2_ABAIXO": "MAT – AVD2\nAbaixo do Básico",
        "PART_AVD2": "PART. – AVD2",
        "LP_PP3": "LP – PP3",
        "MAT_PP3": "MAT – PP3",
        "PART_PP3": "PART. – PP3",
        "EVOLUCAO_LP": "EVOLUÇÃO\nLP",
        "EVOLUCAO_MAT": "EVOLUÇÃO\nMAT",
        "EVOLUCAO_PARTICIPACAO": "EVOLUÇÃO\nPARTICIPAÇÃO (p.p.)",
        "PARTICIPACAO_ATUAL": "PARTICIPAÇÃO\nATUAL",
        "LP_ATUAL": "LP\nATUAL",
        "MAT_ATUAL": "MAT\nATUAL",
        "MEDIA_ATUAL": "MÉDIA\nATUAL",
        "FAROL_URE": "SITUAÇÃO PEDAGÓGICA",
        "DIAGNOSTICO": "DIAGNÓSTICO",
        "ENCAMINHAMENTO": "ENCAMINHAMENTO",
    }

    return resultado.rename(columns=nomes)


# ==========================================================
# CORES DOS RESULTADOS DE DESEMPENHO
# ==========================================================

def _aplicar_cor_desempenho(cell):
    """
    Colore a fonte conforme a classificação do desempenho:

        < 50%       Abaixo do Básico — vermelho
        50%–69,9%   Básico — amarelo forte
        70%–89,9%   Adequado — verde
        >= 90%      Proficiente — azul

    A regra é aplicada somente aos indicadores de desempenho,
    não aos percentuais de Abaixo do Básico da AVD1/AVD2 nem
    às colunas de participação.
    """

    if not isinstance(cell.value, (int, float)):
        return

    valor = float(cell.value)

    if valor < 0.50:
        cell.font = Font(
            color=COR_FONTE_ABAIXO,
            bold=True,
        )

    elif valor < 0.70:
        cell.font = Font(
            color=COR_FONTE_BASICO,
            bold=True,
        )

    elif valor < 0.90:
        cell.font = Font(
            color=COR_FONTE_ADEQUADO,
            bold=True,
        )

    else:
        cell.font = Font(
            color=COR_FONTE_PROFICIENTE,
            bold=True,
        )


def _formatar_classificacao_desempenho(ws):
    """Aplica as cores aos indicadores de desempenho.

    AVD1/AVD2 abaixo do básico e participações não recebem essa
    classificação, pois representam proporções de estudantes e não
    desempenho da escola.
    """

    colunas_desempenho = {
        "LP – PP1",
        "MAT – PP1",
        "LP – PP2",
        "MAT – PP2",
        "LP – PP3",
        "MAT – PP3",
        "LP\nATUAL",
        "MAT\nATUAL",
        "MÉDIA\nATUAL",
    }

    indices = {
        str(cell.value).strip().upper(): cell.column
        for cell in ws[1]
        if cell.value is not None
    }

    for nome_coluna in colunas_desempenho:
        coluna = indices.get(nome_coluna)
        if coluna is None:
            continue
        for linha in range(2, ws.max_row + 1):
            _aplicar_cor_desempenho(
                ws.cell(row=linha, column=coluna)
            )


# ==========================================================
# RESUMO EXECUTIVO
# ==========================================================

# ==========================================================
# PAINEL GERAL / RESUMO EXECUTIVO
# ==========================================================

def _avaliacoes_disponiveis(df):
    """
    Identifica somente as avaliações que realmente possuem dados
    na base. Isso evita, por exemplo, mostrar PP3 como utilizada
    quando o arquivo PP3 ainda não foi carregado.
    """

    regras = {
        "AVD1": [
            "LP_AVD1_ABAIXO",
            "MAT_AVD1_ABAIXO",
        ],
        "PP1": [
            "LP_PP1",
            "MAT_PP1",
            "PART_PP1",
        ],
        "PP2": [
            "LP_PP2",
            "MAT_PP2",
            "PART_PP2",
        ],
        "AVD2": [
            "LP_AVD2_ABAIXO",
            "MAT_AVD2_ABAIXO",
            "PART_AVD2",
        ],
        "PP3": [
            "LP_PP3",
            "MAT_PP3",
            "PART_PP3",
        ],
    }

    disponiveis = []

    for avaliacao, colunas in regras.items():

        for coluna in colunas:

            if coluna not in df.columns:
                continue

            if df[coluna].notna().any():
                disponiveis.append(
                    avaliacao
                )
                break

    return disponiveis


def _valor_media(df, coluna):
    if coluna not in df.columns:
        return None

    serie = pd.to_numeric(
        df[coluna],
        errors="coerce",
    ).dropna()

    if serie.empty:
        return None

    return float(serie.mean())


def _criar_painel_resumo(df, indicadores):
    """
    Monta um painel gerencial horizontal, priorizando comparativos.

    Blocos:
        1. Panorama geral
        2. Participação por avaliação
        3. Comparativo AVD1 x AVD2 do Abaixo do Básico
        4. Situação pedagógica das escolas

    Quando uma informação não existe na fonte, ela é apresentada
    como "Não disponível", sem transformar ausência em zero.
    """

    data_geracao = indicadores.get(
        "DATA_GERACAO"
    )

    if data_geracao is not None:
        data_formatada = data_geracao.strftime(
            "%d/%m/%Y %H:%M"
        )
    else:
        data_formatada = ""

    avaliacoes = _avaliacoes_disponiveis(
        df
    )

    avaliacoes_texto = ", ".join(
        str(item)
        for item in avaliacoes
    )

    if not avaliacoes_texto:
        avaliacoes_texto = (
            "Nenhuma avaliação disponível"
        )

    participacoes = []

    for avaliacao in [
        "AVD1",
        "PP1",
        "PP2",
        "AVD2",
        "PP3",
    ]:

        coluna = f"PART_{avaliacao}"

        valor = _valor_media(
            df,
            coluna,
        )

        participacoes.append(
            (
                avaliacao,
                valor,
            )
        )

    lp_avd1 = _valor_media(
        df,
        "LP_AVD1_ABAIXO",
    )

    lp_avd2 = _valor_media(
        df,
        "LP_AVD2_ABAIXO",
    )

    mat_avd1 = _valor_media(
        df,
        "MAT_AVD1_ABAIXO",
    )

    mat_avd2 = _valor_media(
        df,
        "MAT_AVD2_ABAIXO",
    )

    def variacao(
        inicial,
        final,
    ):

        if inicial is None or final is None:
            return None

        return final - inicial

    situacoes = [
        (
            "PRIORITÁRIAS",
            indicadores.get(
                "PRIORITARIA",
                0,
            ),
        ),
        (
            "ATENÇÃO",
            indicadores.get(
                "ATENCAO",
                0,
            ),
        ),
        (
            "FAVORÁVEIS",
            indicadores.get(
                "FAVORAVEL",
                0,
            ),
        ),
        (
            "SEM HISTÓRICO",
            indicadores.get(
                "SEM_HISTORICO",
                0,
            ),
        ),
    ]

    return {
        "data_geracao": data_formatada,
        "avaliacoes": avaliacoes_texto,
        "total_escolas": indicadores.get(
            "TOTAL_ESCOLAS",
            len(df),
        ),
        "participacoes": participacoes,
        "diagnostico": [
            (
                "Língua Portuguesa",
                lp_avd1,
                lp_avd2,
                variacao(
                    lp_avd1,
                    lp_avd2,
                ),
            ),
            (
                "Matemática",
                mat_avd1,
                mat_avd2,
                variacao(
                    mat_avd1,
                    mat_avd2,
                ),
            ),
        ],
        "situacoes": situacoes,
    }


def _escrever_painel_resumo(
    writer,
    painel,
):
    """
    Escreve o painel geral em blocos horizontais,
    facilitando a comparação entre avaliações.
    """

    # Cria a aba vazia para podermos formatá-la diretamente.
    pd.DataFrame().to_excel(
        writer,
        sheet_name="RESUMO EXECUTIVO",
        index=False,
    )

    ws = writer.sheets[
        "RESUMO EXECUTIVO"
    ]

    # ------------------------------------------------------
    # TÍTULO
    # ------------------------------------------------------

    ws.merge_cells(
        "A1:Q1"
    )

    titulo = ws["A1"]
    titulo.value = (
        "RADAR PEDAGÓGICO URE — "
        "PAINEL GERAL"
    )
    titulo.fill = CABECALHO_FILL
    titulo.font = Font(
        bold=True,
        color="FFFFFF",
        size=14,
    )
    titulo.alignment = CENTRO

    # ------------------------------------------------------
    # BLOCO 1 — PANORAMA GERAL
    # ------------------------------------------------------

    ws.merge_cells(
        "A3:B3"
    )

    ws["A3"] = "PANORAMA GERAL"
    ws["A3"].fill = CABECALHO_FILL
    ws["A3"].font = CABECALHO_FONT
    ws["A3"].alignment = CENTRO

    panorama = [
        (
            "Data de geração",
            painel["data_geracao"],
        ),
        (
            "Total de escolas",
            painel["total_escolas"],
        ),
        (
            "Avaliações utilizadas",
            painel["avaliacoes"],
        ),
    ]

    for indice, (
        indicador,
        valor,
    ) in enumerate(
        panorama,
        start=4,
    ):

        ws.cell(
            row=indice,
            column=1,
            value=indicador,
        )

        ws.cell(
            row=indice,
            column=2,
            value=valor,
        )

        ws.cell(
            row=indice,
            column=1,
        ).alignment = ESQUERDA

        ws.cell(
            row=indice,
            column=2,
        ).alignment = CENTRO

    # ------------------------------------------------------
    # BLOCO 2 — PARTICIPAÇÃO
    # ------------------------------------------------------

    ws.merge_cells(
        "D3:I3"
    )

    ws["D3"] = (
        "COMPARATIVO DE PARTICIPAÇÃO"
    )
    ws["D3"].fill = CABECALHO_FILL
    ws["D3"].font = CABECALHO_FONT
    ws["D3"].alignment = CENTRO

    headers = [
        "AVD1",
        "PP1",
        "PP2",
        "AVD2",
        "PP3",
    ]

    for coluna, avaliacao in enumerate(
        headers,
        start=4,
    ):

        cell = ws.cell(
            row=4,
            column=coluna,
            value=avaliacao,
        )

        cell.fill = PatternFill(
            fill_type="solid",
            fgColor="D9EAF7",
        )

        cell.font = Font(
            bold=True,
            color="1F1F1F",
        )

        cell.alignment = CENTRO

    for coluna, (
        avaliacao,
        valor,
    ) in enumerate(
        painel["participacoes"],
        start=4,
    ):

        cell = ws.cell(
            row=5,
            column=coluna,
        )

        if valor is None:
            cell.value = (
                "Não disponível"
            )
        else:
            cell.value = valor
            cell.number_format = "0.0%"

        cell.alignment = CENTRO

    ws.merge_cells(
        "D6:I6"
    )

    ws["D6"] = (
        "A participação AVD1 será exibida "
        "somente quando houver esse dado "
        "separado na fonte."
    )
    ws["D6"].alignment = Alignment(
        horizontal="left",
        vertical="center",
        wrap_text=True,
    )
    ws["D6"].font = Font(
        italic=True,
        color="666666",
        size=9,
    )

    # ------------------------------------------------------
    # BLOCO 3 — AVD1 x AVD2
    # ------------------------------------------------------

    ws.merge_cells(
        "D8:G8"
    )

    ws["D8"] = (
        "COMPARATIVO AVD1 × AVD2 — "
        "ABAIXO DO BÁSICO"
    )
    ws["D8"].fill = CABECALHO_FILL
    ws["D8"].font = CABECALHO_FONT
    ws["D8"].alignment = CENTRO

    comparativo_headers = [
        "Componente",
        "AVD1",
        "AVD2",
        "Variação (p.p.)",
    ]

    for coluna, valor in enumerate(
        comparativo_headers,
        start=4,
    ):

        cell = ws.cell(
            row=9,
            column=coluna,
            value=valor,
        )

        cell.fill = PatternFill(
            fill_type="solid",
            fgColor="D9EAF7",
        )

        cell.font = Font(
            bold=True,
        )

        cell.alignment = CENTRO

    for linha, dados in enumerate(
        painel["diagnostico"],
        start=10,
    ):

        componente, avd1, avd2, variacao = dados

        ws.cell(
            row=linha,
            column=4,
            value=componente,
        )

        for coluna, valor in [
            (5, avd1),
            (6, avd2),
            (7, variacao),
        ]:

            cell = ws.cell(
                row=linha,
                column=coluna,
            )

            if valor is None:
                cell.value = (
                    "Não disponível"
                )
            else:
                cell.value = valor
                cell.number_format = "0.0%"

            cell.alignment = CENTRO

        ws.cell(
            row=linha,
            column=4,
        ).alignment = ESQUERDA

    # ------------------------------------------------------
    # BLOCO 4 — SITUAÇÃO PEDAGÓGICA
    # ------------------------------------------------------

    ws.merge_cells(
        "J3:K3"
    )

    ws["J3"] = (
        "SITUAÇÃO PEDAGÓGICA"
    )
    ws["J3"].fill = CABECALHO_FILL
    ws["J3"].font = CABECALHO_FONT
    ws["J3"].alignment = CENTRO

    ws["J4"] = "Situação"
    ws["K4"] = "Escolas"

    for coluna in [10, 11]:

        cell = ws.cell(
            row=4,
            column=coluna,
        )

        cell.fill = PatternFill(
            fill_type="solid",
            fgColor="D9EAF7",
        )

        cell.font = Font(
            bold=True,
        )

        cell.alignment = CENTRO

    for linha, (
        situacao,
        quantidade,
    ) in enumerate(
        painel["situacoes"],
        start=5,
    ):

        ws.cell(
            row=linha,
            column=10,
            value=situacao,
        )

        ws.cell(
            row=linha,
            column=11,
            value=quantidade,
        )

        ws.cell(
            row=linha,
            column=10,
        ).alignment = ESQUERDA

        ws.cell(
            row=linha,
            column=11,
        ).alignment = CENTRO

    # ------------------------------------------------------
    # LARGURAS
    # ------------------------------------------------------

    larguras = {
        "A": 24,
        "B": 24,
        "C": 3,
        "D": 24,
        "E": 14,
        "F": 14,
        "G": 17,
        "H": 14,
        "I": 14,
        "J": 22,
        "K": 12,
        "L": 3,
        "M": 3,
        "N": 3,
        "O": 3,
        "P": 3,
        "Q": 3,
    }

    for coluna, largura in larguras.items():
        ws.column_dimensions[
            coluna
        ].width = largura

    # ------------------------------------------------------
    # ALTURAS
    # ------------------------------------------------------

    ws.row_dimensions[1].height = 26
    ws.row_dimensions[3].height = 22
    ws.row_dimensions[6].height = 32

    ws.freeze_panes = "A4"

    # ------------------------------------------------------
    # FILTRO NÃO É NECESSÁRIO NO PAINEL
    # ------------------------------------------------------

    ws.auto_filter.ref = None


# ==========================================================
# ESCOLAS PRIORITÁRIAS
# ==========================================================

def _criar_prioritarias(df):

    coluna_farol = (
        "FAROL_URE"
        if "FAROL_URE" in df.columns
        else "SITUAÇÃO PEDAGÓGICA"
        if "SITUAÇÃO PEDAGÓGICA" in df.columns
        else None
    )

    if coluna_farol is None:
        return df.iloc[0:0].copy()

    mask = (
        df[coluna_farol]
        .astype("string")
        .str.upper()
        .str.contains(
            "PRIORIT",
            na=False,
        )
    )

    return df.loc[mask].copy()


# ==========================================================
# FORMATAÇÃO DO FAROL
# ==========================================================

def _formatar_farol(ws):

    cabecalhos = {
        cell.value: cell.column
        for cell in ws[1]
    }

    coluna = cabecalhos.get("SITUAÇÃO PEDAGÓGICA")

    if not coluna:
        return

    for row in range(
        2,
        ws.max_row + 1,
    ):

        cell = ws.cell(
            row=row,
            column=coluna,
        )

        valor = str(
            cell.value or ""
        ).strip().upper()

        if valor == "PRIORITÁRIA":
            cell.fill = COR_PRIORITARIA

        elif valor == "ATENÇÃO":
            cell.fill = COR_ATENCAO

        elif valor == "FAVORÁVEL":
            cell.fill = COR_DESTAQUE

        elif valor == "SEM HISTÓRICO":
            cell.fill = COR_SEM_DADOS


# ==========================================================
# GERAÇÃO DO EXCEL
# ==========================================================

def gerar_excel(df: pd.DataFrame) -> BytesIO:

    if df is None or df.empty:
        raise ValueError(
            "O DataFrame consolidado está vazio."
        )

    df = df.copy()

    # ------------------------------------------------------
    # Compatibilidade de nomes antigos
    # ------------------------------------------------------

    df = _garantir_colunas_adp(df)

    # ------------------------------------------------------
    # INDICADORES
    # ------------------------------------------------------
    # Mantemos uma cópia interna com os nomes técnicos para que
    # os cálculos e o painel continuem usando os campos originais.
    # A renomeação amigável acontece somente na apresentação final.
    # ------------------------------------------------------

    df_interno = calcular_indicadores_escolas(df)

    # ------------------------------------------------------
    # ORGANIZAÇÃO FINAL DA APRESENTAÇÃO
    # ------------------------------------------------------

    df = _ordenar_colunas(df_interno)

    # ------------------------------------------------------
    # CRIA ARQUIVO
    # ------------------------------------------------------

    buffer = BytesIO()

    with pd.ExcelWriter(
        buffer,
        engine="openpyxl",
    ) as writer:

        # ==================================================
        # RESUMO EXECUTIVO / PAINEL GERAL
        # ==================================================

        indicadores_resumo = {
            "DATA_GERACAO": pd.Timestamp.now().to_pydatetime(),
            "AVALIACOES": _avaliacoes_disponiveis(
                df
            ),
            "TOTAL_ESCOLAS": len(df_interno),
        }

        if "FAROL_URE" in df_interno.columns:

            farol = (
                df_interno["FAROL_URE"]
                .astype("string")
                .str.upper()
                .str.strip()
            )

            indicadores_resumo["PRIORITARIA"] = int(
                farol.eq("PRIORITÁRIA").sum()
            )

            indicadores_resumo["ATENCAO"] = int(
                farol.eq("ATENÇÃO").sum()
            )

            indicadores_resumo["FAVORAVEL"] = int(
                farol.eq("FAVORÁVEL").sum()
            )

            indicadores_resumo["SEM_HISTORICO"] = int(
                farol.eq("SEM HISTÓRICO").sum()
            )

        else:

            indicadores_resumo["PRIORITARIA"] = 0
            indicadores_resumo["ATENCAO"] = 0
            indicadores_resumo["FAVORAVEL"] = 0
            indicadores_resumo["SEM_HISTORICO"] = 0

        for avaliacao in [
            "AVD1",
            "PP1",
            "PP2",
            "AVD2",
            "PP3",
        ]:

            coluna = f"PART_{avaliacao}"

            if coluna in df_interno.columns:
                indicadores_resumo[coluna] = pd.to_numeric(
                    df_interno[coluna],
                    errors="coerce",
                ).mean()

        painel = _criar_painel_resumo(
            df_interno,
            indicadores_resumo,
        )

        _escrever_painel_resumo(
            writer,
            painel,
        )

        # ==================================================
        # RADAR PEDAGÓGICO
        # ==================================================

        df.to_excel(
            writer,
            sheet_name="RADAR PEDAGÓGICO",
            index=False,
        )

        ws = writer.sheets[
            "RADAR PEDAGÓGICO"
        ]

        _formatar_planilha(ws)
        _formatar_classificacao_desempenho(ws)
        _formatar_farol(ws)

        # ==================================================
        # ESCOLAS PRIORITÁRIAS
        # ==================================================

        prioritarias = _criar_prioritarias(df)

        prioritarias.to_excel(
            writer,
            sheet_name="ESCOLAS PRIORITÁRIAS",
            index=False,
        )

        ws_p = writer.sheets[
            "ESCOLAS PRIORITÁRIAS"
        ]

        _formatar_planilha(ws_p)
        _formatar_classificacao_desempenho(ws_p)
        _formatar_farol(ws_p)

    buffer.seek(0)

    return buffer

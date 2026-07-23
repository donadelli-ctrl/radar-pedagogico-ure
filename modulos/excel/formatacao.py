"""
==========================================================
RADAR PEDAGÓGICO URE
MÓDULO: formatacao.py
Versão: 1.3
Status: HOMOLOGADO
==========================================================

Responsabilidade:
Centralizar toda a formatação das planilhas Excel.
"""

from openpyxl.styles import (
    Font,
    PatternFill,
    Alignment,
)

from openpyxl.utils import get_column_letter


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


# ==========================================================
# CORES DA SITUAÇÃO
# ==========================================================

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

# ==========================================================
# CORES DOS GRUPOS DE AVALIAÇÃO
# ==========================================================

COR_GERAL = PatternFill(
    fill_type="solid",
    fgColor="1F4E79",
)

COR_ADE = PatternFill(
    fill_type="solid",
    fgColor="70AD47",
)

COR_PP1 = PatternFill(
    fill_type="solid",
    fgColor="FFD966",
)

COR_PP2 = PatternFill(
    fill_type="solid",
    fgColor="F4B183",
)

COR_ADP = PatternFill(
    fill_type="solid",
    fgColor="C9A0DC",
)

COR_PP3 = PatternFill(
    fill_type="solid",
    fgColor="9DC3E6",
)

COR_SITUACAO = PatternFill(
    fill_type="solid",
    fgColor="C00000",
)

# ==========================================================
# FORMATAR PLANILHA
# ==========================================================

def formatar_planilha(ws):
    """
    Aplica toda a formatação padrão às planilhas
    do Radar Pedagógico.
    """

    # ======================================================
    # CABEÇALHO
    # ======================================================
     
    for cell in ws[1]:

        cabecalho = str(
            cell.value
        ).strip().upper()

        # ----------------------------------------------
        # Cor do grupo
        # ----------------------------------------------

        if cabecalho in ("CIE", "ESCOLA"):

            cell.fill = COR_GERAL

        elif "ADE" in cabecalho:

            cell.fill = COR_ADE

        elif "PP1" in cabecalho:

            cell.fill = COR_PP1

        elif "PP2" in cabecalho:

            cell.fill = COR_PP2

        elif "ADP" in cabecalho:

            cell.fill = COR_ADP

        elif "PP3" in cabecalho:

            cell.fill = COR_PP3

        elif cabecalho == "SITUACAO":

            cell.fill = COR_SITUACAO

        else:

            cell.fill = CABECALHO_FILL

        cell.font = CABECALHO_FONT
        cell.alignment = CENTRO

    # ======================================================
    # CORPO
    # ======================================================

    PREFIXOS_PERCENTUAIS = (
        "PART_",
        "MEDIA_",
        "LP_",
        "MAT_",
    )

    for coluna in ws.columns:

        letra = get_column_letter(
            coluna[0].column
        )

        cabecalho = str(
            coluna[0].value
        ).strip().upper()

        maior = len(cabecalho)

        for cell in coluna:

            if cell.row > 1:

                if cabecalho == "ESCOLA":

                    cell.alignment = ESQUERDA

                else:

                    cell.alignment = CENTRO

                if (
                    cabecalho.startswith(
                        PREFIXOS_PERCENTUAIS
                    )
                    and isinstance(
                        cell.value,
                        (int, float),
                    )
                ):

                    cell.number_format = "0.0%"

            valor = (
                ""
                if cell.value is None
                else str(cell.value)
            )

            if len(valor) > maior:

                maior = len(valor)

        # ==================================================
        # LARGURA DAS COLUNAS
        # ==================================================

        if cabecalho == "CIE":

            largura = 10

        elif cabecalho == "ESCOLA":

            largura = 45

        elif cabecalho.startswith("PART"):

            largura = 12

        elif cabecalho.startswith("MEDIA"):

            largura = 10

        elif cabecalho.startswith("LP"):

            largura = 10

        elif cabecalho.startswith("MAT"):

            largura = 10

        elif cabecalho.startswith("FAROL"):

            largura = 8

        elif cabecalho == "SITUACAO":

            largura = 18

        else:

            largura = min(
                maior + 3,
                40,
            )

        ws.column_dimensions[
            letra
        ].width = largura

    # ======================================================
    # SITUAÇÃO
    # ======================================================

    for coluna in ws.columns:

        cabecalho = str(
            coluna[0].value
        ).strip().upper()

        if cabecalho != "SITUACAO":

            continue

        for cell in coluna[1:]:

            valor = str(
                cell.value
            ).upper()

            if "PRIORIT" in valor:

                cell.fill = COR_PRIORITARIA

            elif "ATEN" in valor:

                cell.fill = COR_ATENCAO

            elif "DESTAQUE" in valor:

                cell.fill = COR_DESTAQUE

            elif "SEM DADOS" in valor:

                cell.fill = COR_SEM_DADOS

    # ======================================================
    # FINALIZAÇÃO
    # ======================================================

    ws.freeze_panes = "C2"

    ws.auto_filter.ref = ws.dimensions
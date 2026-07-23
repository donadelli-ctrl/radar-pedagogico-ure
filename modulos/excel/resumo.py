"""
==========================================================
RADAR PEDAGÓGICO URE
MÓDULO: resumo.py
Versão: 3.0
==========================================================

Responsabilidade:
Gerar a aba RESUMO EXECUTIVO.
"""

from openpyxl.styles import (
    Font,
    PatternFill,
    Alignment,
    Border,
    Side,
)

from modulos.excel.formatacao import (
    CABECALHO_FILL,
)

# ==========================================================
# ESTILOS
# ==========================================================

FONTE_TITULO = Font(
    name="Aptos",
    size=16,
    bold=True,
    color="FFFFFF",
)

FONTE_SUBTITULO = Font(
    name="Aptos",
    size=11,
    bold=True,
)

FONTE_TEXTO = Font(
    name="Aptos",
    size=10,
)

FONTE_NUMERO = Font(
    name="Aptos",
    size=14,
    bold=True,
)

CENTRO = Alignment(
    horizontal="center",
    vertical="center",
)

ESQUERDA = Alignment(
    horizontal="left",
    vertical="center",
)

DIREITA = Alignment(
    horizontal="right",
    vertical="center",
)

BORDA = Border(
    left=Side(style="thin", color="DDDDDD"),
    right=Side(style="thin", color="DDDDDD"),
    top=Side(style="thin", color="DDDDDD"),
    bottom=Side(style="thin", color="DDDDDD"),
)

FUNDO_CARTAO = PatternFill(
    fill_type="solid",
    fgColor="F8F9FA",
)

# ==========================================================
# FUNÇÕES AUXILIARES
# ==========================================================

def criar_cartao(ws, col_inicio, linha, emoji, titulo, valor):
    """
    Cria um cartão de indicador.
    """

    col_fim = chr(ord(col_inicio) + 1)

    ws.merge_cells(f"{col_inicio}{linha}:{col_fim}{linha}")
    ws.merge_cells(f"{col_inicio}{linha+1}:{col_fim}{linha+1}")
    ws.merge_cells(f"{col_inicio}{linha+2}:{col_fim}{linha+2}")

    c1 = ws[f"{col_inicio}{linha}"]
    c2 = ws[f"{col_inicio}{linha+1}"]
    c3 = ws[f"{col_inicio}{linha+2}"]

    c1.value = emoji
    c2.value = titulo
    c3.value = valor

    c1.font = Font(size=18)
    c2.font = FONTE_SUBTITULO
    c3.font = FONTE_NUMERO

    c1.alignment = CENTRO
    c2.alignment = CENTRO
    c3.alignment = CENTRO

    for r in range(linha, linha + 3):

        for coluna in (col_inicio, col_fim):

            celula = ws[f"{coluna}{r}"]

            celula.fill = FUNDO_CARTAO
            celula.border = BORDA

# ==========================================================
# RESUMO EXECUTIVO
# ==========================================================

def criar_resumo(writer, indicadores):

    ws = writer.book.create_sheet(
        "RESUMO EXECUTIVO"
    )

    # ======================================================
    # CONFIGURAÇÃO DA PLANILHA
    # ======================================================

    ws.sheet_view.showGridLines = False

    ws.freeze_panes = "A5"

    # ======================================================
    # LARGURA DAS COLUNAS
    # ======================================================

    larguras = {
        "A": 18,
        "B": 18,
        "C": 18,
        "D": 18,
        "E": 18,
        "F": 18,
        "G": 18,
        "H": 18,
    }

    for coluna, largura in larguras.items():
        ws.column_dimensions[coluna].width = largura

    # ======================================================
    # ALTURA DAS LINHAS
    # ======================================================

    ws.row_dimensions[1].height = 28
    ws.row_dimensions[2].height = 22
    ws.row_dimensions[5].height = 24

    # ======================================================
    # TÍTULO
    # ======================================================

    ws.merge_cells("A1:H1")

    titulo = ws["A1"]

    titulo.value = "RADAR PEDAGÓGICO URE"

    titulo.font = FONTE_TITULO

    titulo.fill = CABECALHO_FILL

    titulo.alignment = CENTRO

    # ======================================================
    # SUBTÍTULO
    # ======================================================

    ws.merge_cells("A2:H2")

    subtitulo = ws["A2"]

    subtitulo.value = "PAINEL EXECUTIVO"

    subtitulo.font = FONTE_SUBTITULO

    subtitulo.alignment = CENTRO

    # ======================================================
    # DADOS DA GERAÇÃO
    # ======================================================

    ws["A4"] = "Data de geração"

    ws["A4"].font = FONTE_SUBTITULO

    ws["B4"] = indicadores["DATA_GERACAO"].strftime(
        "%d/%m/%Y %H:%M"
    )

    ws["B4"].font = FONTE_TEXTO

    ws["E4"] = "Avaliações"

    ws["E4"].font = FONTE_SUBTITULO

    ws["F4"] = ", ".join(
        indicadores["AVALIACOES"]
    )

    ws["F4"].font = FONTE_TEXTO

    # ======================================================
    # CARTÕES SUPERIORES
    # ======================================================

    criar_cartao(
        ws,
        "A",
        6,
        "🏫",
        "TOTAL DE ESCOLAS",
        indicadores["TOTAL_ESCOLAS"],
    )

    criar_cartao(
        ws,
        "C",
        6,
        "🔴",
        "PRIORITÁRIAS",
        indicadores["PRIORITARIA"],
    )

    criar_cartao(
        ws,
        "E",
        6,
        "🟡",
        "ATENÇÃO",
        indicadores["ATENCAO"],
    )

    criar_cartao(
        ws,
        "G",
        6,
        "🟢",
        "DESTAQUE",
        indicadores["DESTAQUE"],
    )
    # ======================================================
    # PARTICIPAÇÃO
    # ======================================================

    ws["A11"] = "📊 PARTICIPAÇÃO"

    ws["A11"].font = FONTE_SUBTITULO

    ws["A11"].alignment = ESQUERDA

    participacao = [

        ("ADE", indicadores.get("PART_ADE")),
        ("PP1", indicadores.get("PART_PP1")),
        ("PP2", indicadores.get("PART_PP2")),

    ]

    linha = 12

    for nome, valor in participacao:

        ws[f"A{linha}"] = nome

        ws[f"B{linha}"] = valor

        ws[f"A{linha}"].font = FONTE_TEXTO
        ws[f"B{linha}"].font = FONTE_NUMERO

        ws[f"B{linha}"].alignment = DIREITA

        if valor is not None:
            ws[f"B{linha}"].number_format = "0.0%"

        linha += 1

    # ======================================================
    # MÉDIAS GERAIS
    # ======================================================

    ws["E11"] = "📚 MÉDIAS GERAIS"

    ws["E11"].font = FONTE_SUBTITULO

    ws["E11"].alignment = ESQUERDA

    medias = [

        ("PP1", indicadores.get("MEDIA_PP1")),
        ("PP2", indicadores.get("MEDIA_PP2")),

    ]

    linha = 12

    for nome, valor in medias:

        ws[f"E{linha}"] = nome

        ws[f"F{linha}"] = valor

        ws[f"E{linha}"].font = FONTE_TEXTO
        ws[f"F{linha}"].font = FONTE_NUMERO

        ws[f"F{linha}"].alignment = DIREITA

        if valor is not None:
            ws[f"F{linha}"].number_format = "0.0%"

        linha += 1

    # ======================================================
    # CLASSIFICAÇÃO
    # ======================================================

    ws["A17"] = "🚦 CLASSIFICAÇÃO"

    ws["A17"].font = FONTE_SUBTITULO

    classificacao = [

        ("🔴 Prioritárias", indicadores["PRIORITARIA"]),
        ("🟡 Atenção", indicadores["ATENCAO"]),
        ("🟢 Destaque", indicadores["DESTAQUE"]),
        ("⚪ Sem dados", indicadores["SEM_DADOS"]),

    ]

    linha = 18

    for texto, valor in classificacao:

        ws[f"A{linha}"] = texto

        ws[f"B{linha}"] = valor

        ws[f"A{linha}"].font = FONTE_TEXTO
        ws[f"B{linha}"].font = FONTE_NUMERO

        ws[f"B{linha}"].alignment = DIREITA

        linha += 1

    # ======================================================
    # ACABAMENTO DOS BLOCOS
    # ======================================================

    for linha in range(11, 15):

        for coluna in ("A", "B", "E", "F"):

            celula = ws[f"{coluna}{linha}"]

            celula.border = BORDA

            if linha > 11:
                celula.fill = FUNDO_CARTAO

    for linha in range(17, 22):

        for coluna in ("A", "B"):

            celula = ws[f"{coluna}{linha}"]

            celula.border = BORDA

            if linha > 17:
                celula.fill = FUNDO_CARTAO

        # ======================================================
    # ALINHAMENTOS
    # ======================================================

    for linha in range(12, 15):

        ws[f"A{linha}"].alignment = ESQUERDA
        ws[f"B{linha}"].alignment = DIREITA

        ws[f"E{linha}"].alignment = ESQUERDA
        ws[f"F{linha}"].alignment = DIREITA

    for linha in range(18, 22):

        ws[f"A{linha}"].alignment = ESQUERDA
        ws[f"B{linha}"].alignment = DIREITA

        # ======================================================
    # RODAPÉ
    # ======================================================

    ws.merge_cells("A24:H24")

    rodape = ws["A24"]

    rodape.value = (
        "RADAR PEDAGÓGICO URE • Versão 3.0"
    )

    rodape.font = Font(
        name="Aptos",
        size=9,
        italic=True,
        color="808080",
    )

    rodape.alignment = CENTRO

    # ======================================================
    # LINHAS DE SEPARAÇÃO
    # ======================================================

    for coluna in range(1, 9):

        ws.cell(
            row=10,
            column=coluna,
        ).border = Border(
            bottom=Side(
                style="medium",
                color="D9D9D9",
            )
        )

        ws.cell(
            row=16,
            column=coluna,
        ).border = Border(
            bottom=Side(
                style="medium",
                color="D9D9D9",
            )
        )

    # ======================================================
    # VISUALIZAÇÃO
    # ======================================================

    ws.sheet_view.zoomScale = 90

    ws.sheet_view.showGridLines = False
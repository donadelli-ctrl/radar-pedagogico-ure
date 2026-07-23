"""
==========================================================
RADAR PEDAGÓGICO URE
MÓDULO: radar.py
Versão: 1.4
==========================================================

Responsabilidade:
Gerar a aba RADAR PEDAGÓGICO.
"""

from modulos.excel.formatacao import (
    formatar_planilha,
)


# ==========================================================
# FUNÇÃO AUXILIAR
# ==========================================================

def gerar_farol(situacao):
    """
    Retorna o farol conforme a situação da escola.
    """

    texto = str(situacao).upper()

    if "PRIORIT" in texto:
        return "🔴"

    elif "ATEN" in texto:
        return "🟡"

    elif "DESTAQUE" in texto:
        return "🟢"

    else:
        return "⚪"


# ==========================================================
# RADAR PEDAGÓGICO
# ==========================================================

def criar_radar(writer, df):
    """
    Cria a aba RADAR PEDAGÓGICO.
    """

    if df.empty:
        return

    # ------------------------------------------------------
    # CRIA COLUNA FAROL
    # ------------------------------------------------------

    if "SITUACAO" in df.columns:

        # evita erro caso o radar seja gerado novamente
        if "FAROL" in df.columns:
            df.drop(columns=["FAROL"], inplace=True)

        indice = df.columns.get_loc("SITUACAO")

        df.insert(
            indice,
            "FAROL",
            df["SITUACAO"].apply(gerar_farol),
        )

    # ------------------------------------------------------
    # EXPORTAÇÃO
    # ------------------------------------------------------

    df.to_excel(
        writer,
        sheet_name="RADAR PEDAGÓGICO",
        index=False,
    )

    ws = writer.sheets["RADAR PEDAGÓGICO"]

    formatar_planilha(ws)
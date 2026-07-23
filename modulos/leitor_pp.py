"""
==========================================================
RADAR PEDAGÓGICO URE
Módulo: leitor_pp.py
==========================================================

Responsabilidade:
Ler arquivos da Prova Paulista (PP1, PP2, ADP e PP3)
e devolver um DataFrame padronizado.
"""

import pandas as pd

from modulos.utils import (
    localizar_coluna,
    padronizar_escola,
    converter_numero,
)


# ==========================================================
# LEITOR DA PROVA PAULISTA
# ==========================================================

def ler_PP(arquivo, avaliacao):
    """
    Lê uma avaliação (PP1, PP2, ADP ou PP3)
    e devolve um DataFrame padronizado.
    """

    if arquivo is None:
        return None

    # ------------------------------------------------------
    # Leitura
    # ------------------------------------------------------

    df = pd.read_excel(arquivo)

    df.columns = [str(col).strip() for col in df.columns]

    # ------------------------------------------------------
    # Localização das colunas
    # ------------------------------------------------------

    col_escola = localizar_coluna(
        df,
        [
            "ESCOLAS",
            "ESCOLA",
        ],
    )

    col_part = localizar_coluna(
        df,
        [
            "PARTICIPAÇÃO",
            "PARTICIPACAO",
        ],
    )

    col_media = localizar_coluna(
        df,
        [
            "ACERTOS",
        ],
    )

    col_mat = localizar_coluna(
        df,
        [
            "MAT",
        ],
    )

    col_lp = localizar_coluna(
        df,
        [
            "PORT",
        ],
    )

    # O Farol pode não existir
    col_farol = localizar_coluna(
        df,
        [
            "FAROL SARESP",
            "FAROL",
        ],
    )

    # ------------------------------------------------------
    # Validação
    # ------------------------------------------------------

    faltando = []

    if col_escola is None:
        faltando.append("ESCOLA")

    if col_part is None:
        faltando.append("PARTICIPAÇÃO")

    if col_media is None:
        faltando.append("ACERTOS")

    if col_mat is None:
        faltando.append("MAT")

    if col_lp is None:
        faltando.append("PORT")

    if faltando:

        raise ValueError(
            "As seguintes colunas não foram encontradas:\n\n"
            + "\n".join(faltando)
        )

    # ------------------------------------------------------
    # Base padronizada
    # ------------------------------------------------------

    base = pd.DataFrame()

    base["ESCOLA"] = (
        df[col_escola]
        .apply(padronizar_escola)
    )

    base[f"PART_{avaliacao}"] = (
        df[col_part]
        .apply(converter_numero)
    )

    base[f"MEDIA_{avaliacao}"] = (
        df[col_media]
        .apply(converter_numero)
    )

    base[f"LP_{avaliacao}"] = (
        df[col_lp]
        .apply(converter_numero)
    )

    base[f"MAT_{avaliacao}"] = (
        df[col_mat]
        .apply(converter_numero)
    )

    # ------------------------------------------------------
    # Farol (opcional)
    # ------------------------------------------------------

    if col_farol is not None:

        base[f"FAROL_{avaliacao}"] = (
            df[col_farol]
            .apply(converter_numero)
            .astype("Int64")
        )

    else:

        base[f"FAROL_{avaliacao}"] = pd.Series(
            [pd.NA] * len(base),
            dtype="Int64",
        )

    # ------------------------------------------------------
    # Limpeza
    # ------------------------------------------------------

    base.dropna(
        subset=["ESCOLA"],
        inplace=True,
    )

    base.reset_index(
        drop=True,
        inplace=True,
    )

    return base
"""
Responsabilidade:
Ler arquivos da Prova Paulista (PP1, PP2, ADP e PP3)
e devolver um DataFrame padronizado.
"""

import re
import pandas as pd

from modulos.utils import (
    localizar_coluna,
    padronizar_escola,
    converter_numero,
)


# ==========================================================
# EXTRAÇÃO DO CIE
# ==========================================================

def extrair_cie(valor):
    """
    Extrai o CIE quando ele aparece no final do nome da escola.

    Exemplo:

        ALTIMIRA PINKE PROFESSORA - 916024
        ↓
        916024

    Quando não for possível identificar o CIE,
    retorna <NA>.
    """

    if pd.isna(valor):
        return pd.NA

    texto = str(valor).strip()

    encontrado = re.search(
        r"-\s*(\d+)\s*$",
        texto,
    )

    if not encontrado:
        return pd.NA

    try:
        return int(encontrado.group(1))
    except (ValueError, TypeError):
        return pd.NA


# ==========================================================
# LEITOR DA PROVA PAULISTA
# ==========================================================

def ler_PP(arquivo, avaliacao):
    """
    Lê uma avaliação da Prova Paulista:

        PP1
        PP2
        ADP
        PP3

    e devolve um DataFrame padronizado.

    Estrutura principal:

        CIE
        ESCOLA
        PART_{avaliacao}
        MEDIA_{avaliacao}
        LP_{avaliacao}
        MAT_{avaliacao}

    Quando a avaliação possuir Farol SARESP de origem,
    ele será preservado separadamente como:

        FAROL_SEDUC_{avaliacao}

    Esse indicador NÃO é utilizado para calcular
    o Farol da URE.
    """

    if arquivo is None:
        return None

    avaliacao = str(avaliacao).strip().upper()

    avaliacoes_validas = {
        "PP1",
        "PP2",
        "ADP",
        "PP3",
    }

    if avaliacao not in avaliacoes_validas:
        raise ValueError(
            "Avaliação inválida. "
            "Utilize PP1, PP2, ADP ou PP3."
        )

    # ------------------------------------------------------
    # Leitura
    # ------------------------------------------------------

    df = pd.read_excel(arquivo)

    df.columns = [
        str(coluna).strip()
        for coluna in df.columns
    ]

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
            "(%) DE PARTICIPAÇÃO",
            "(%) PARTICIPAÇÃO",
            "PARTICIPAÇÃO",
            "PARTICIPACAO",
        ],
    )

    col_media = localizar_coluna(
        df,
        [
            "(%) DE ACERTOS",
            "(%) ACERTOS",
            "ACERTOS",
        ],
    )

    col_mat = localizar_coluna(
        df,
        [
            "MAT",
            "MATEMÁTICA",
            "MATEMATICA",
        ],
    )

    col_lp = localizar_coluna(
        df,
        [
            "PORT",
            "PORTUGUÊS",
            "PORTUGUES",
            "LP",
            "LÍNGUA PORTUGUESA",
            "LINGUA PORTUGUESA",
        ],
    )

    # ------------------------------------------------------
    # Farol SARESP original
    #
    # Pode existir na PP2, mas não necessariamente
    # nas demais avaliações.
    # ------------------------------------------------------

    col_farol = localizar_coluna(
        df,
        [
            "FAROL SARESP",
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
            "As seguintes colunas não foram encontradas "
            f"na avaliação {avaliacao}:\n\n"
            + "\n".join(faltando)
        )

    # ------------------------------------------------------
    # Base padronizada
    # ------------------------------------------------------

    base = pd.DataFrame()

    # ------------------------------------------------------
    # CIE
    # ------------------------------------------------------

    base["CIE"] = (
        df[col_escola]
        .apply(extrair_cie)
        .astype("Int64")
    )

    # ------------------------------------------------------
    # ESCOLA
    # ------------------------------------------------------

    base["ESCOLA"] = (
        df[col_escola]
        .apply(padronizar_escola)
    )

    # ------------------------------------------------------
    # PARTICIPAÇÃO
    # ------------------------------------------------------

    base[f"PART_{avaliacao}"] = (
        df[col_part]
        .apply(converter_numero)
    )

    # ------------------------------------------------------
    # MÉDIA / % DE ACERTOS
    # ------------------------------------------------------

    base[f"MEDIA_{avaliacao}"] = (
        df[col_media]
        .apply(converter_numero)
    )

    # ------------------------------------------------------
    # LÍNGUA PORTUGUESA
    # ------------------------------------------------------

    base[f"LP_{avaliacao}"] = (
        df[col_lp]
        .apply(converter_numero)
    )

    # ------------------------------------------------------
    # MATEMÁTICA
    # ------------------------------------------------------

    base[f"MAT_{avaliacao}"] = (
        df[col_mat]
        .apply(converter_numero)
    )

    # ------------------------------------------------------
    # FAROL SARESP DE ORIGEM
    #
    # Preserva o valor original da SEDUC.
    #
    # NÃO participa do cálculo do nosso Farol da URE.
    # ------------------------------------------------------

    if col_farol is not None:

        base[f"FAROL_SEDUC_{avaliacao}"] = (
            pd.to_numeric(
                df[col_farol],
                errors="coerce",
            )
            .astype("Int64")
        )

    # ------------------------------------------------------
    # LIMPEZA
    # ------------------------------------------------------

    base["ESCOLA"] = (
    base["ESCOLA"]
    .astype(str)
    .str.strip()

    )

    # ------------------------------------------------------
    # Remove registros administrativos da planilha
    # ------------------------------------------------------

    marcadores_invalidos = [
        "",
        "NAN",
        "NONE",
        "<NA>",
        "TOTAL",
    ]

    base = base[
        ~base["ESCOLA"].isin(marcadores_invalidos)
    ]

    # Remove a linha que contém informações dos filtros
    base = base[
        ~base["ESCOLA"].str.startswith(
            "FILTROS APLICADOS",
            na=False,
        )
    ]

    # ------------------------------------------------------
    # Remove registros sem CIE somente quando
    # a identificação não estiver disponível.
    #
    # A escola continua sendo mantida porque,
    # em avaliações futuras, podemos receber arquivos
    # sem o CIE no nome.
    # ------------------------------------------------------

    # ------------------------------------------------------
    # Remove duplicidades
    # ------------------------------------------------------

    base = (
        base
        .drop_duplicates(
            subset=["CIE", "ESCOLA"],
            keep="first",
        )
    )

    # ------------------------------------------------------
    # Ordenação
    # ------------------------------------------------------

    base = base.sort_values(
        by="ESCOLA",
        kind="stable",
    )

    # ------------------------------------------------------
    # Reinicia o índice
    # ------------------------------------------------------

    base.reset_index(
        drop=True,
        inplace=True,
    )

    return base
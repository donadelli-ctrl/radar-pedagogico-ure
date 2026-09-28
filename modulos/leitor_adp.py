# ==========================================================
# RADAR PEDAGÓGICO URE
# MÓDULO: leitor_adp.py
# LEITOR OFICIAL DO ARQUIVO ADP
#
# Estrutura:
# AVD1 + AVD2
#
# Futuramente:
# AVD1 + AVD2 + AVD3
# ==========================================================

import re
import pandas as pd


# ==========================================================
# NORMALIZAÇÃO DO CIE
# ==========================================================

def _normalizar_cie(valor):

    if pd.isna(valor):
        return pd.NA

    texto = str(valor).strip()

    if texto == "":
        return pd.NA

    # Ex.: "47797.0"
    try:
        numero = float(texto)

        if numero.is_integer():
            return str(int(numero))

    except Exception:
        pass

    # Ex.: "JOSE PEDRO DE MORAES - 47797"
    numeros = re.findall(r"\d+", texto)

    if numeros:
        return numeros[-1]

    return pd.NA


# ==========================================================
# NORMALIZAÇÃO DO NOME DA ESCOLA
# ==========================================================

def _normalizar_escola(valor):

    if pd.isna(valor):
        return pd.NA

    texto = str(valor).strip().upper()

    if texto == "":
        return pd.NA

    # Remove o CIE no final do nome
    texto = re.sub(
        r"\s*-\s*\d+\s*$",
        "",
        texto,
    )

    # Espaços duplicados
    texto = re.sub(
        r"\s+",
        " ",
        texto,
    )

    return texto.strip()


# ==========================================================
# CONVERSÃO PARA PERCENTUAL
# ==========================================================

def _pct(valor):

    if pd.isna(valor):
        return pd.NA

    if isinstance(valor, str):

        texto = valor.strip()

        if texto == "":
            return pd.NA

        texto = texto.replace("%", "")
        texto = texto.replace(".", "").replace(",", ".")

        try:
            valor = float(texto)

        except Exception:
            return pd.NA

    try:

        numero = float(valor)

        # 31,3 → 31,3%
        if numero > 1:
            numero = numero / 100

        return numero

    except Exception:

        return pd.NA


# ==========================================================
# LOCALIZAÇÃO DOS BLOCOS
# ==========================================================

def _definir_estrutura(numero_colunas):

    # ------------------------------------------------------
    # AVD1 + AVD2
    #
    # 0  Escola
    # 1  Participação
    # 2  Variação participação
    #
    # LP
    # 3  AVD1 Abaixo
    # 4  AVD1 Básico
    # 5  AVD1 Proficiente
    #
    # 6  AVD2 Abaixo
    # 7  Variação
    # 8  AVD2 Básico
    # 9  AVD2 Proficiente
    #
    # MAT
    # 10 AVD1 Abaixo
    # 11 AVD1 Básico
    # 12 AVD1 Proficiente
    #
    # 13 AVD2 Abaixo
    # 14 Variação
    # 15 AVD2 Básico
    # 16 AVD2 Proficiente
    # ------------------------------------------------------

    if numero_colunas < 17:

        raise ValueError(
            "A aba 'Export' do arquivo ADP não possui "
            "as 17 colunas mínimas esperadas para AVD1 + AVD2."
        )

    estrutura = {

        "LP_AVD1_ABAIXO": 3,
        "LP_AVD2_ABAIXO": 6,

        "MAT_AVD1_ABAIXO": 10,
        "MAT_AVD2_ABAIXO": 13,
    }

    # ------------------------------------------------------
    # AVD3
    #
    # Se futuramente o mesmo arquivo passar a trazer:
    #
    # LP AVD3 = posições 10 a 13
    # MAT AVD1 = posições 14 a 16
    # MAT AVD2 = posições 17 a 20
    # MAT AVD3 = posições 21 a 24
    #
    # então teremos 25 colunas.
    # ------------------------------------------------------

    if numero_colunas >= 25:

        estrutura.update({

            "LP_AVD3_ABAIXO": 10,

            "MAT_AVD1_ABAIXO": 14,
            "MAT_AVD2_ABAIXO": 17,
            "MAT_AVD3_ABAIXO": 21,

        })

        ultima_avaliacao = "AVD3"

    else:

        ultima_avaliacao = "AVD2"

    return estrutura, ultima_avaliacao


# ==========================================================
# LEITURA DO ADP
# ==========================================================

def ler_ADP(arquivo):

    """
    Lê o arquivo ADP oficial da URE.

    Atualmente:
        AVD1 + AVD2

    Futuramente:
        AVD1 + AVD2 + AVD3

    As avaliações permanecem separadas no DataFrame.
    """

    if arquivo is None:

        return pd.DataFrame()

    if hasattr(arquivo, "seek"):

        arquivo.seek(0)

    # ------------------------------------------------------
    # LEITURA DA ABA OFICIAL
    # ------------------------------------------------------

    df = pd.read_excel(
        arquivo,
        sheet_name="Export",
        header=0,
    )

    if df.empty:

        return pd.DataFrame()

    # ------------------------------------------------------
    # ESTRUTURA
    # ------------------------------------------------------

    estrutura, ultima_avaliacao = _definir_estrutura(
        len(df.columns)
    )

    # ------------------------------------------------------
    # REMOVE LINHAS QUE NÃO REPRESENTAM ESCOLAS
    # ------------------------------------------------------

    primeira_coluna = df.columns[0]

    texto_primeira_coluna = (
        df[primeira_coluna]
        .astype(str)
        .str.upper()
        .str.strip()
    )

    mascara = ~texto_primeira_coluna.str.startswith(
        (
            "FILTROS APLICADOS",
            "TOTAL",
            "OBSERVAÇÃO",
            "OBSERVACOES",
        ),
        na=False,
    )

    df = df.loc[mascara].copy()

    # ------------------------------------------------------
    # DATAFRAME DE SAÍDA
    # ------------------------------------------------------

    out = pd.DataFrame(
        index=df.index
    )

    # ------------------------------------------------------
    # ESCOLA ORIGINAL
    # ------------------------------------------------------

    out["ESCOLA_ORIGINAL"] = df.iloc[:, 0]

    # ------------------------------------------------------
    # CIE
    # ------------------------------------------------------

    out["CIE"] = (
        out["ESCOLA_ORIGINAL"]
        .map(_normalizar_cie)
        .astype("string")
    )

    # ------------------------------------------------------
    # NOME DA ESCOLA
    # ------------------------------------------------------

    out["ESCOLA"] = (
        out["ESCOLA_ORIGINAL"]
        .map(_normalizar_escola)
        .astype("string")
    )

    # ------------------------------------------------------
    # PARTICIPAÇÃO
    #
    # O arquivo oficial possui uma coluna única de participação.
    # Ela representa a avaliação diagnóstica mais recente
    # disponível no arquivo.
    # ------------------------------------------------------

    out[
        f"PART_{ultima_avaliacao}"
    ] = (
        df.iloc[:, 1]
        .map(_pct)
    )

    # Compatibilidade
    out["PART_ADP"] = (
        out[f"PART_{ultima_avaliacao}"]
    )

    # ------------------------------------------------------
    # INDICADORES DE AVD1 / AVD2 / AVD3
    # ------------------------------------------------------

    for nome_coluna, posicao in estrutura.items():

        if posicao >= len(df.columns):

            continue

        out[nome_coluna] = (
            df.iloc[:, posicao]
            .map(_pct)
        )

    # ------------------------------------------------------
    # ALIAS ADP
    #
    # ADP = última avaliação diagnóstica disponível.
    # Atualmente = AVD2.
    # Futuramente = AVD3.
    # ------------------------------------------------------

    for componente in (
        "LP",
        "MAT",
    ):

        coluna_atual = (
            f"{componente}_{ultima_avaliacao}_ABAIXO"
        )

        if coluna_atual in out.columns:

            out[
                f"{componente}_ADP_ABAIXO"
            ] = out[coluna_atual]

    # ------------------------------------------------------
    # LIMPEZA
    # ------------------------------------------------------

    out = out[
        out["ESCOLA"].notna()
        &
        (
            out["ESCOLA"]
            .astype(str)
            .str.strip()
            != ""
        )
    ].copy()

    # ------------------------------------------------------
    # REMOVE DUPLICIDADES
    # ------------------------------------------------------

    if out["CIE"].notna().any():

        out = (
            out
            .drop_duplicates(
                subset=["CIE"],
                keep="first",
            )
        )

    else:

        out = (
            out
            .drop_duplicates(
                subset=["ESCOLA"],
                keep="first",
            )
        )

    # ------------------------------------------------------
    # RESET
    # ------------------------------------------------------

    out = out.reset_index(
        drop=True
    )

    return out
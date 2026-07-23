"""
==========================================================
RADAR PEDAGÓGICO URE
Módulo: utils.py
==========================================================

Funções auxiliares utilizadas em todo o projeto.
"""

import re
import pandas as pd


# ==========================================================
# PADRONIZAÇÃO DE TEXTO
# ==========================================================

def padronizar_texto(valor):
    """
    Remove espaços extras e converte para MAIÚSCULO.
    """

    if pd.isna(valor):
        return ""

    texto = str(valor).strip().upper()

    texto = re.sub(r"\s+", " ", texto)

    return texto


# ==========================================================
# PADRONIZAÇÃO DAS ESCOLAS
# ==========================================================

def padronizar_escola(valor):
    """
    Padroniza o nome da escola.

    Remove o código CIE quando ele aparece
    no final do nome da escola.

    Exemplo:
    ALTIMIRA PINKE PROFESSORA - 916024
        ↓
    ALTIMIRA PINKE PROFESSORA
    """

    texto = padronizar_texto(valor)

    texto = re.sub(r"\s*-\s*\d+\s*$", "", texto)

    return texto


# ==========================================================
# CONVERSÃO NUMÉRICA
# ==========================================================

def converter_numero(valor):
    """
    Converte qualquer valor para float.

    Aceita:
        45,6
        45.6
        "45,6%"
    """

    if pd.isna(valor):
        return None

    texto = (
        str(valor)
        .replace("%", "")
        .replace(",", ".")
        .strip()
    )

    try:
        return float(texto)
    except Exception:
        return None


# ==========================================================
# LOCALIZAÇÃO DE COLUNAS
# ==========================================================

def localizar_coluna(df, nomes):
    """
    Localiza uma coluna pelo nome.

    Aceita correspondência exata ou parcial.
    """

    colunas = {
        padronizar_texto(col): col
        for col in df.columns
    }

    # Procura correspondência exata
    for nome in nomes:

        chave = padronizar_texto(nome)

        if chave in colunas:
            return colunas[chave]

    # Procura correspondência parcial
    for nome in nomes:

        chave = padronizar_texto(nome)

        for coluna_padrao, coluna_original in colunas.items():

            if chave in coluna_padrao:
                return coluna_original

    return None


# ==========================================================
# VALIDAÇÃO
# ==========================================================

def validar_colunas(df, obrigatorias):
    """
    Verifica se todas as colunas obrigatórias existem.
    """

    faltando = []

    for coluna in obrigatorias:

        if localizar_coluna(df, [coluna]) is None:
            faltando.append(coluna)

    if faltando:

        raise ValueError(
            "Colunas não encontradas:\n\n"
            + "\n".join(faltando)
        )
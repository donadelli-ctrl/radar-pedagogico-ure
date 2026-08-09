"""
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
    Converte valores numéricos e percentuais para a
    escala decimal utilizada internamente pelo Radar.

    Exemplos:

        80       → 0.80
        80%      → 0.80
        "80%"    → 0.80
        "80,5%"  → 0.805
        0.80     → 0.80
        "0,80"   → 0.80
        45,6     → 0.456

    Valores entre 0 e 1 são preservados.
    Valores maiores que 1 são interpretados como percentual.
    """

    if pd.isna(valor):
        return None

    # Caso já seja número
    if isinstance(valor, (int, float)):
        numero = float(valor)

        if 0 <= numero <= 1:
            return numero

        if numero > 1:
            return numero / 100

        return None

    texto = str(valor).strip()

    if not texto:
        return None

    possui_percentual = "%" in texto

    texto = (
        texto
        .replace("%", "")
        .replace(" ", "")
        .replace(",", ".")
    )

    try:
        numero = float(texto)
    except (ValueError, TypeError):
        return None

    if numero < 0:
        return None

    # Se veio explicitamente como percentual
    if possui_percentual:
        return numero / 100

    # Valores já na escala decimal
    if 0 <= numero <= 1:
        return numero

    # Valores acima de 1 são tratados como percentual
    return numero / 100


# ==========================================================
# LOCALIZAÇÃO DE COLUNAS
# ==========================================================

def localizar_coluna(df, nomes):
    """
    Localiza uma coluna pelo nome.

    Aceita correspondência exata ou parcial.
    """

    colunas = {
        padronizar_texto(coluna): coluna
        for coluna in df.columns
    }

    # ------------------------------------------------------
    # Correspondência exata
    # ------------------------------------------------------

    for nome in nomes:

        chave = padronizar_texto(nome)

        if chave in colunas:
            return colunas[chave]

    # ------------------------------------------------------
    # Correspondência parcial
    # ------------------------------------------------------

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
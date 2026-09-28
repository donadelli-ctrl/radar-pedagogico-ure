# ==========================================================
# RADAR PEDAGÓGICO URE
# MÓDULO: consolidacao.py
# VERSÃO 3.0
# AVD1 + PP1 + PP2 + AVD2 + PP3
# AVD1 e AVD2 são fornecidas pelo arquivo ADP
# ==========================================================

import re
import unicodedata

import pandas as pd


# ==========================================================
# NORMALIZAÇÃO DO CIE
# ==========================================================

def _normalizar_cie(serie):
    """
    Normaliza o CIE para uma representação textual estável.

    Exemplos:

        47797       -> "47797"
        47797.0     -> "47797"
        "47797"     -> "47797"
        "47797.0"   -> "47797"
        vazio       -> <NA>

    Também tenta recuperar CIEs que estejam armazenados
    como texto com pequenos caracteres adicionais.
    """

    def converter(valor):

        if pd.isna(valor):
            return pd.NA

        texto = str(valor).strip()

        if texto == "":
            return pd.NA

        # Primeiro tenta conversão numérica normal
        try:
            numero = float(texto)

            if numero.is_integer():
                return str(int(numero))

        except Exception:
            pass

        # Caso esteja como texto, procura somente os dígitos
        numeros = re.sub(r"\D", "", texto)

        if numeros:
            return numeros

        return pd.NA

    return serie.map(converter).astype("string")


# ==========================================================
# NORMALIZAÇÃO DO NOME DA ESCOLA
# ==========================================================

def _normalizar_escola(serie):
    """
    Normaliza o nome da escola para facilitar o cruzamento.

    A normalização:

    - remove espaços extras;
    - coloca em maiúsculas;
    - remove acentos;
    - remove pontuação desnecessária;
    - padroniza algumas formas comuns de identificação
      de escolas estaduais.

    O nome original não é usado como chave de forma literal.
    """

    def normalizar(valor):

        if pd.isna(valor):
            return pd.NA

        texto = str(valor).strip().upper()

        if texto == "":
            return pd.NA

        # Remove acentos
        texto = unicodedata.normalize(
            "NFKD",
            texto,
        )

        texto = "".join(
            caractere
            for caractere in texto
            if not unicodedata.combining(caractere)
        )

        # Padroniza pontuação
        texto = texto.replace("&", " E ")

        texto = re.sub(
            r"[^\w\s]",
            " ",
            texto,
        )

        # Remove prefixos muito comuns
        texto = re.sub(
            r"^\s*E\s*E\s+",
            "",
            texto,
        )

        texto = re.sub(
            r"^\s*EE\s+",
            "",
            texto,
        )

        texto = re.sub(
            r"^\s*ESCOLA\s+ESTADUAL\s+",
            "",
            texto,
        )

        texto = re.sub(
            r"^\s*ESCOLA\s+ESTADUAL\s*",
            "",
            texto,
        )

        # Espaços extras
        texto = re.sub(
            r"\s+",
            " ",
            texto,
        ).strip()

        return texto

    return serie.map(normalizar).astype("string")


# ==========================================================
# CRIAÇÃO DA CHAVE DO NOME
# ==========================================================

def _criar_chave_escola(serie):
    """
    Cria uma chave estável para o nome da escola.
    """

    return (
        _normalizar_escola(serie)
        .fillna("")
        .str.strip()
    )


# ==========================================================
# PREPARAÇÃO DA ADP
# ==========================================================

def _normalizar_colunas_adp(df):
    """
    Padroniza o arquivo oficial ADP, que contém AVD1 e AVD2.

    O leitor oficial já entrega:

        PART_ADP
        LP_AVD1_ABAIXO
        LP_AVD2_ABAIXO
        MAT_AVD1_ABAIXO
        MAT_AVD2_ABAIXO

    Os aliases LP_ADP_ABAIXO e MAT_ADP_ABAIXO são mantidos apenas
    para compatibilidade com módulos antigos e representam AVD2.
    """

    if df is None:
        return None

    base = df.copy()

    # Compatibilidade com possíveis nomes antigos de participação.
    if "PART_ADP" not in base.columns:
        for origem in ("ADP_PART", "PART_ADE"):
            if origem in base.columns:
                base["PART_ADP"] = base[origem]
                break

    # Compatibilidade com formatos antigos de AVD1/ADE.
    if "LP_AVD1_ABAIXO" not in base.columns:
        for origem in ("LP_ABAIXO", "ADE_LP_ABAIXO"):
            if origem in base.columns:
                base["LP_AVD1_ABAIXO"] = base[origem]
                break

    if "MAT_AVD1_ABAIXO" not in base.columns:
        for origem in ("MAT_ABAIXO", "ADE_MAT_ABAIXO"):
            if origem in base.columns:
                base["MAT_AVD1_ABAIXO"] = base[origem]
                break

    # Compatibilidade com formatos antigos em que ADP significava AVD2.
    if "LP_AVD2_ABAIXO" not in base.columns:
        for origem in (
            "LP_ADP_ABAIXO",
            "ADP_LP_ABAIXO",
            "ADP_ABAIXO_LP",
        ):
            if origem in base.columns:
                base["LP_AVD2_ABAIXO"] = base[origem]
                break

    if "MAT_AVD2_ABAIXO" not in base.columns:
        for origem in (
            "MAT_ADP_ABAIXO",
            "ADP_MAT_ABAIXO",
            "ADP_ABAIXO_MAT",
        ):
            if origem in base.columns:
                base["MAT_AVD2_ABAIXO"] = base[origem]
                break

    # Aliases legados: ADP representa AVD2.
    if "LP_ADP_ABAIXO" not in base.columns and "LP_AVD2_ABAIXO" in base.columns:
        base["LP_ADP_ABAIXO"] = base["LP_AVD2_ABAIXO"]

    if "MAT_ADP_ABAIXO" not in base.columns and "MAT_AVD2_ABAIXO" in base.columns:
        base["MAT_ADP_ABAIXO"] = base["MAT_AVD2_ABAIXO"]

    return base


# ==========================================================
# PREPARAÇÃO DE UMA AVALIAÇÃO
# ==========================================================

def _preparar_avaliacao(
    df,
    avaliacao,
):
    """
    Prepara uma avaliação para a consolidação.

    Identificação:

        1. CIE
        2. nome da escola

    O arquivo ADP é convertido automaticamente para os nomes
    próprios de AVD1 e AVD2.
    """

    if df is None or df.empty:
        return None

    base = df.copy()

    nome_avaliacao = (
        str(avaliacao)
        .strip()
        .upper()
    )

    # ======================================================
    # ADP
    # ======================================================

    if nome_avaliacao == "ADP":
        base = _normalizar_colunas_adp(
            base
        )

    # ======================================================
    # GARANTE ESCOLA
    # ======================================================

    if "ESCOLA" not in base.columns:

        raise ValueError(
            f"A avaliação {nome_avaliacao} "
            "não possui a coluna ESCOLA."
        )

    # ======================================================
    # GARANTE CIE
    # ======================================================

    if "CIE" not in base.columns:
        base["CIE"] = pd.NA

    # ======================================================
    # NORMALIZA IDENTIFICAÇÃO
    # ======================================================

    base["CIE"] = _normalizar_cie(
        base["CIE"]
    )

    base["ESCOLA"] = _normalizar_escola(
        base["ESCOLA"]
    )

    # ======================================================
    # CRIA CHAVES
    # ======================================================

    base["CHAVE_CIE"] = (
        base["CIE"]
    )

    base["CHAVE_NOME"] = _criar_chave_escola(
        base["ESCOLA"]
    )

    # ======================================================
    # REMOVE LINHAS SEM IDENTIFICAÇÃO
    # ======================================================

    base = base[
        (
            base["CHAVE_CIE"].notna()
        )
        |
        (
            base["CHAVE_NOME"].notna()
            &
            (
                base["CHAVE_NOME"] != ""
            )
        )
    ].copy()

    # ======================================================
    # REMOVE DUPLICIDADES INTERNAS
    # ======================================================

    possui_cie = (
        base["CHAVE_CIE"].notna()
    )

    com_cie = (
        base.loc[
            possui_cie
        ]
        .drop_duplicates(
            subset=["CHAVE_CIE"],
            keep="first",
        )
    )

    sem_cie = (
        base.loc[
            ~possui_cie
        ]
        .drop_duplicates(
            subset=["CHAVE_NOME"],
            keep="first",
        )
    )

    base = pd.concat(
        [
            com_cie,
            sem_cie,
        ],
        ignore_index=True,
    )

    base.reset_index(
        drop=True,
        inplace=True,
    )

    return base


# ==========================================================
# LOCALIZAÇÃO POR CIE
# ==========================================================

def _encontrar_indice_por_cie(
    base,
    cie,
):
    """
    Procura uma escola pelo CIE.
    """

    if pd.isna(cie):
        return None

    correspondencias = base.index[
        base["CIE"]
        .astype("string")
        == str(cie)
    ]

    if len(correspondencias) > 0:
        return correspondencias[0]

    return None


# ==========================================================
# LOCALIZAÇÃO POR NOME
# ==========================================================

def _encontrar_indice_por_nome(
    base,
    escola,
):
    """
    Procura uma escola pelo nome normalizado.
    """

    if pd.isna(escola):
        return None

    nome = str(
        escola
    ).strip().upper()

    if nome == "":
        return None

    nomes_base = (
        _normalizar_escola(
            base["ESCOLA"]
        )
    )

    correspondencias = base.index[
        nomes_base == nome
    ]

    if len(correspondencias) > 0:
        return correspondencias[0]

    return None


# ==========================================================
# GARANTE IDENTIFICAÇÃO DA ESCOLA
# ==========================================================

def _garantir_identificacao(
    base,
    avaliacao,
):
    """
    Para cada escola da avaliação:

        1. procura pelo CIE;
        2. se não encontrar, procura pelo nome;
        3. se não encontrar, cria uma nova escola.

    Isso permite:

        - manter escolas existentes;
        - incorporar escolas novas;
        - cruzar ADP sem CIE;
        - completar CIE posteriormente.
    """

    mapa_indices = {}

    for indice_avaliacao, linha in avaliacao.iterrows():

        cie = linha.get(
            "CIE",
            pd.NA,
        )

        escola = linha.get(
            "ESCOLA",
            pd.NA,
        )

        # ==================================================
        # PRIMEIRA TENTATIVA: CIE
        # ==================================================

        indice_base = _encontrar_indice_por_cie(
            base,
            cie,
        )

        # ==================================================
        # SEGUNDA TENTATIVA: NOME
        # ==================================================

        if indice_base is None:

            indice_base = _encontrar_indice_por_nome(
                base,
                escola,
            )

        # ==================================================
        # ESCOLA NOVA
        # ==================================================

        if indice_base is None:

            nova_linha = {
                coluna: pd.NA
                for coluna in base.columns
            }

            nova_linha["CIE"] = cie
            nova_linha["ESCOLA"] = escola

            base.loc[
                len(base)
            ] = nova_linha

            indice_base = base.index[-1]

        # ==================================================
        # COMPLETA CIE
        # ==================================================

        cie_atual = base.at[
            indice_base,
            "CIE",
        ]

        if (
            pd.isna(cie_atual)
            and not pd.isna(cie)
        ):

            base.at[
                indice_base,
                "CIE",
            ] = cie

        # ==================================================
        # COMPLETA ESCOLA
        # ==================================================

        escola_atual = base.at[
            indice_base,
            "ESCOLA",
        ]

        if (
            pd.isna(escola_atual)
            or str(
                escola_atual
            ).strip() == ""
        ):

            base.at[
                indice_base,
                "ESCOLA",
            ] = escola

        mapa_indices[
            indice_avaliacao
        ] = indice_base

    return (
        base,
        mapa_indices,
    )


# ==========================================================
# ADICIONA UMA AVALIAÇÃO
# ==========================================================

def _adicionar_avaliacao(
    base,
    avaliacao,
    nome_avaliacao,
):
    """
    Adiciona os dados de uma avaliação à base.

    O cruzamento ocorre:

        CIE → nome da escola.

    Todos os dados próprios da avaliação são preservados.
    """

    if avaliacao is None or avaliacao.empty:
        return base

    # ======================================================
    # GARANTE IDENTIFICAÇÃO
    # ======================================================

    base, mapa_indices = _garantir_identificacao(
        base,
        avaliacao,
    )

    # ======================================================
    # COLUNAS DE DADOS
    # ======================================================

    colunas_excluidas = {
        "CIE",
        "ESCOLA",
        "CHAVE_CIE",
        "CHAVE_NOME",
    }

    colunas_dados = [
        coluna
        for coluna in avaliacao.columns
        if coluna not in colunas_excluidas
    ]

    # ======================================================
    # ADICIONA COLUNAS
    # ======================================================

    for coluna in colunas_dados:

        if coluna not in base.columns:

            base[coluna] = pd.NA

        # ==================================================
        # COPIA OS VALORES
        # ==================================================

        for indice_avaliacao, valor in (
            avaliacao[
                coluna
            ].items()
        ):

            if indice_avaliacao not in mapa_indices:
                continue

            indice_base = mapa_indices[
                indice_avaliacao
            ]

            # Só grava o valor da avaliação.
            base.at[
                indice_base,
                coluna,
            ] = valor

    return base


# ==========================================================
# CONSOLIDAÇÃO PRINCIPAL
# ==========================================================

def consolidar_base(
    df_ADE=None,
    df_PP1=None,
    df_PP2=None,
    df_ADP=None,
    df_PP3=None,
):
    """
    Consolida o Radar Pedagógico URE.

    Fluxo pedagógico:

        AVD1 → PP1 → PP2 → AVD2 → PP3

    IMPORTANTE:

    - AVD1 e AVD2 estão no mesmo arquivo ADP.
    - Portanto, df_ADE NÃO é utilizado como fonte de AVD1.
    - O parâmetro df_ADE é mantido apenas para compatibilidade
      com versões anteriores do app.
    - AVD1 vem de df_ADP["LP_AVD1_ABAIXO"] e
      df_ADP["MAT_AVD1_ABAIXO"].
    - AVD2 vem de df_ADP["LP_AVD2_ABAIXO"] e
      df_ADP["MAT_AVD2_ABAIXO"].
    - PP1, PP2 e PP3 são incorporados separadamente.
    - Ausência de informação permanece como NA.
    - Ausência de informação NÃO é transformada em zero.
    - O cruzamento das escolas ocorre preferencialmente pelo CIE
      e, quando necessário, pelo nome normalizado.
    """

    # ======================================================
    # COMPATIBILIDADE COM VERSÕES ANTERIORES
    # ======================================================

    # O Radar atual não utiliza um arquivo ADE separado
    # para alimentar AVD1, pois AVD1 já está dentro do ADP.
    #
    # Mantemos o parâmetro df_ADE para evitar quebra de chamadas
    # antigas do app durante a transição da arquitetura.

    _ = df_ADE

    # ======================================================
    # AVALIAÇÕES QUE PARTICIPAM DA CONSOLIDAÇÃO
    # ======================================================

    avaliacoes = [
        ("ADP", df_ADP),
        ("PP1", df_PP1),
        ("PP2", df_PP2),
        ("PP3", df_PP3),
    ]

    bases_validas = []

    # ======================================================
    # PREPARAÇÃO DOS ARQUIVOS
    # ======================================================

    for nome, dataframe in avaliacoes:

        if dataframe is None:
            continue

        if dataframe.empty:
            continue

        preparada = _preparar_avaliacao(
            dataframe,
            nome,
        )

        if preparada is not None and not preparada.empty:

            bases_validas.append(
                (
                    nome,
                    preparada,
                )
            )

    # ======================================================
    # VERIFICA SE EXISTE PELO MENOS UMA FONTE
    # ======================================================

    if not bases_validas:

        raise ValueError(
            "Nenhuma avaliação válida foi encontrada "
            "para realizar a consolidação."
        )

    # ======================================================
    # BASE INICIAL
    # ======================================================

    base = pd.DataFrame(
        columns=[
            "CIE",
            "ESCOLA",
        ]
    )

    # ======================================================
    # INCORPORAÇÃO DAS AVALIAÇÕES
    # ======================================================
    #
    # Ordem de integração:
    #
    # ADP → PP1 → PP2 → PP3
    #
    # Dentro do ADP já existem:
    #
    # AVD1
    # AVD2
    #
    # Portanto, não criamos essas avaliações novamente.
    #
    # ======================================================

    for nome_avaliacao, avaliacao in bases_validas:

        base = _adicionar_avaliacao(
            base,
            avaliacao,
            nome_avaliacao,
        )

    # ======================================================
    # NORMALIZAÇÃO FINAL DA IDENTIFICAÇÃO
    # ======================================================

    base["CIE"] = _normalizar_cie(
        base["CIE"]
    )

    base["ESCOLA"] = _normalizar_escola(
        base["ESCOLA"]
    )

    # ======================================================
    # REMOVE LINHAS SEM IDENTIFICAÇÃO
    # ======================================================

    base = base[
        base["CIE"].notna()
        |
        (
            base["ESCOLA"].notna()
            &
            base["ESCOLA"]
            .astype("string")
            .str.strip()
            .ne("")
        )
    ].copy()

    # ======================================================
    # REMOVE DUPLICIDADES POR CIE
    # ======================================================

    linhas_com_cie = (
        base[
            base["CIE"].notna()
        ]
        .drop_duplicates(
            subset=["CIE"],
            keep="first",
        )
    )

    # ======================================================
    # ESCOLAS SEM CIE
    # ======================================================

    linhas_sem_cie = (
        base[
            base["CIE"].isna()
        ]
        .drop_duplicates(
            subset=["ESCOLA"],
            keep="first",
        )
    )

    # ======================================================
    # RECOMPÕE A BASE
    # ======================================================

    base = pd.concat(
        [
            linhas_com_cie,
            linhas_sem_cie,
        ],
        ignore_index=True,
    )

    # ======================================================
    # ORDENAÇÃO
    # ======================================================

    base.sort_values(
        by="ESCOLA",
        na_position="last",
        inplace=True,
    )

    # ======================================================
    # RESET DO ÍNDICE
    # ======================================================

    base.reset_index(
        drop=True,
        inplace=True,
    )

    return base

# ==========================================================
# RADAR PEDAGÓGICO URE
# APP PRINCIPAL
# ==========================================================

import streamlit as st


from modulos.leitor_ade import ler_ADE
from modulos.leitor_pp import ler_PP
from modulos.consolidacao import consolidar_base
from modulos.excel.excel_final import gerar_excel
from modulos.indicadores import calcular_indicadores_escolas
from modulos.farol import aplicar_farol
from modulos.diagnostico import aplicar_diagnostico


# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="Radar Pedagógico URE",
    page_icon="📊",
    layout="wide",
)


# ==========================================================
# IDENTIDADE VISUAL
# ==========================================================

st.markdown(
    """
    <style>

    /* =====================================================
       FUNDO
       ===================================================== */

    .stApp {
        background-color: #F4F7F9;
        color: #111111;
    }

    .block-container {
        padding-top: 1.4rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }


    /* =====================================================
       TEXTO GERAL
       ===================================================== */

    p,
    span,
    label,
    div {
        color: #111111;
    }


    /* =====================================================
       CABEÇALHO PRINCIPAL
       ===================================================== */

    .radar-titulo {
        background-color: #D5EAF3;
        border-left: 7px solid #4A94B8;
        border-radius: 10px;
        padding: 18px 25px;
        margin-bottom: 20px;
    }

    .radar-titulo h1 {
        color: #111111 !important;
        font-size: 34px;
        font-weight: 700;
        margin: 0;
        padding: 0;
        line-height: 1.2;
    }

    .radar-titulo p {
        color: #222222 !important;
        font-size: 15px;
        margin: 6px 0 0 0;
    }


    /* =====================================================
       TÍTULOS DAS SEÇÕES
       ===================================================== */

    .secao-titulo {
        background-color: #D9EDF5;
        border-left: 5px solid #4A94B8;
        border-radius: 8px;
        padding: 10px 15px;
        margin-top: 16px;
        margin-bottom: 10px;
        color: #111111 !important;
        font-size: 17px;
        font-weight: 700;
    }


    /* =====================================================
       TEXTO DE ORIENTAÇÃO
       ===================================================== */

    .orientacao {
        color: #222222 !important;
        font-size: 14px;
        margin-top: 0;
        margin-bottom: 12px;
    }


    /* =====================================================
       LABEL DOS CAMPOS
       ===================================================== */

    label {
        color: #111111 !important;
        font-weight: 600 !important;
    }


    /* =====================================================
       CAMPO DE TEXTO
       ===================================================== */

    [data-testid="stTextInput"] input {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        border: 1px solid #9BBCCA !important;
        border-radius: 7px;
    }

    [data-testid="stTextInput"] input::placeholder {
        color: #666666 !important;
    }

    [data-testid="stTextInput"] input:focus {
        border-color: #397E9E !important;
        box-shadow: 0 0 0 1px #397E9E !important;
    }


    /* =====================================================
       FILE UPLOADER
       ===================================================== */

    [data-testid="stFileUploader"] {
        background-color: #FFFFFF;
        border: 1px solid #B5CFDA;
        border-radius: 8px;
        padding: 7px;
    }

    [data-testid="stFileUploader"] section {
        background-color: #EEF6F9;
        border-radius: 6px;
    }

    [data-testid="stFileUploader"] button {
        background-color: #FFFFFF !important;
        color: #111111 !important;
        border: 1px solid #8EAFBC !important;
    }


    /* =====================================================
       BOTÃO GERAR
       ===================================================== */

    div.stButton > button {
        width: 100%;
        min-height: 48px;
        border-radius: 8px;
        border: none;
        background-color: #3F89AC;
        color: #FFFFFF !important;
        font-size: 16px;
        font-weight: 700;
    }

    div.stButton > button:hover {
        background-color: #286F91;
        color: #FFFFFF !important;
    }


    /* =====================================================
       BOTÃO DOWNLOAD
       ===================================================== */

    div.stDownloadButton > button {
        width: 100%;
        min-height: 48px;
        border-radius: 8px;
        border: 2px solid #3F89AC;
        background-color: #D5EAF3;
        color: #111111 !important;
        font-size: 16px;
        font-weight: 700;
    }

    div.stDownloadButton > button:hover {
        background-color: #C1E0EC;
        color: #111111 !important;
    }


    /* =====================================================
       MENSAGENS
       ===================================================== */

    [data-testid="stAlert"] {
        border-radius: 8px;
    }


    /* =====================================================
       REMOVE DIVISORES
       ===================================================== */

    hr {
        display: none !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# CABEÇALHO
# ==========================================================

st.markdown(
    """
    <div class="radar-titulo">
        <h1>📊 Radar Pedagógico URE</h1>
        <p>
            Painel Gerencial das Escolas da URE
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# IDENTIFICAÇÃO DA URE
# ==========================================================

st.markdown(
    """
    <div class="secao-titulo">
        🏫 Identificação da URE
    </div>
    """,
    unsafe_allow_html=True,
)

nome_ure = st.text_input(
    "Nome da URE",
    placeholder="Ex.: Pirassununga",
)


# ==========================================================
# ARQUIVOS
# ==========================================================

st.markdown(
    """
    <div class="secao-titulo">
        📁 Arquivos das Avaliações
    </div>

    <div class="orientacao">
        Selecione os arquivos das avaliações disponíveis.
    </div>
    """,
    unsafe_allow_html=True,
)


arquivo_ADE = st.file_uploader(
    "ADE — Avaliação Diagnóstica",
    type=["xlsx"],
)


arquivo_PP1 = st.file_uploader(
    "PP1 — Prova Paulista 1",
    type=["xlsx"],
)


arquivo_PP2 = st.file_uploader(
    "PP2 — Prova Paulista 2",
    type=["xlsx"],
)


arquivo_ADP = st.file_uploader(
    "ADP — Avaliação Diagnóstica Processual",
    type=["xlsx"],
)


arquivo_PP3 = st.file_uploader(
    "PP3 — Prova Paulista 3",
    type=["xlsx"],
)


# ==========================================================
# GERAÇÃO
# ==========================================================

st.markdown(
    """
    <div class="secao-titulo">
        📊 Geração do Radar
    </div>
    """,
    unsafe_allow_html=True,
)


if st.button(
    "🚀 GERAR RADAR",
    use_container_width=True,
):

    if arquivo_ADE is None:

        st.error(
            "Selecione o arquivo ADE."
        )

        st.stop()

    with st.spinner(
        "Gerando Radar Pedagógico..."
    ):

        # ==================================================
        # LEITURA
        # ==================================================

        df_ADE = ler_ADE(
            arquivo_ADE
        )

        df_PP1 = (
            ler_PP(
                arquivo_PP1,
                "PP1",
            )
            if arquivo_PP1
            else None
        )

        df_PP2 = (
            ler_PP(
                arquivo_PP2,
                "PP2",
            )
            if arquivo_PP2
            else None
        )

        df_ADP = (
            ler_PP(
                arquivo_ADP,
                "ADP",
            )
            if arquivo_ADP
            else None
        )

        df_PP3 = (
            ler_PP(
                arquivo_PP3,
                "PP3",
            )
            if arquivo_PP3
            else None
        )

        # ==================================================
        # CONSOLIDAÇÃO
        # ==================================================

        base = consolidar_base(
            df_ADE,
            df_PP1,
            df_PP2,
            df_ADP,
            df_PP3,
        )

        # ==================================================
        # INDICADORES
        # ==================================================

        base = calcular_indicadores_escolas(
            base
        )

        # ==================================================
        # FAROL URE
        # ==================================================

        base = aplicar_farol(
            base
        )

        # ==================================================
        # DIAGNÓSTICO
        # ==================================================

        base = aplicar_diagnostico(
            base
        )

        # ==================================================
        # EXCEL
        # ==================================================

        output = gerar_excel(
            base
        )

    # ======================================================
    # NOME DO ARQUIVO
    # ======================================================

    nome_arquivo = "RADAR_URE"

    if nome_ure.strip():

        nome_arquivo = (
            f"RADAR_"
            f"{nome_ure.upper().replace(' ', '_')}"
        )

    st.success(
        "Radar gerado com sucesso!"
    )

    st.download_button(
        label="⬇ BAIXAR RADAR",
        data=output,
        file_name=f"{nome_arquivo}.xlsx",
        mime=(
            "application/vnd.openxmlformats-"
            "officedocument.spreadsheetml.sheet"
        ),
        use_container_width=True,
    )
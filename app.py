# ==========================================================
# RADAR PEDAGÓGICO URE
# APP PRINCIPAL
# ==========================================================

import streamlit as st


from modulos.leitor_ade import ler_ADE
from modulos.leitor_pp import ler_PP
from modulos.consolidacao import consolidar_base
from modulos.excel.excel_final import gerar_excel


# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="Radar Pedagógico URE",
    page_icon="📊",
    layout="wide",
)

# ==========================================================
# CABEÇALHO
# ==========================================================

st.title("📊 Radar Pedagógico URE")

st.caption("Painel Gerencial das Escolas da URE")

st.divider()

# ==========================================================
# IDENTIFICAÇÃO
# ==========================================================

nome_ure = st.text_input(
    "Nome da URE",
    placeholder="Ex.: Pirassununga"
)

st.divider()

# ==========================================================
# ARQUIVOS
# ==========================================================

st.subheader("Arquivos")

arquivo_ADE = st.file_uploader(
    "ADE",
    type=["xlsx"]
)

arquivo_PP1 = st.file_uploader(
    "PP1",
    type=["xlsx"]
)

arquivo_PP2 = st.file_uploader(
    "PP2",
    type=["xlsx"]
)

arquivo_ADP = st.file_uploader(
    "ADP",
    type=["xlsx"]
)

arquivo_PP3 = st.file_uploader(
    "PP3",
    type=["xlsx"]
)

st.divider()

# ==========================================================
# BOTÃO
# ==========================================================

if st.button(
    "🚀 GERAR RADAR",
    use_container_width=True
):

    if arquivo_ADE is None:

        st.error("Selecione o arquivo ADE.")

        st.stop()

    with st.spinner("Gerando Radar Pedagógico..."):    

        # ======================================================
        # LEITURA DOS ARQUIVOS
        # ======================================================

        df_ADE = ler_ADE(arquivo_ADE)

        df_PP1 = ler_PP(arquivo_PP1, "PP1") if arquivo_PP1 else None

        df_PP2 = ler_PP(arquivo_PP2, "PP2") if arquivo_PP2 else None

        df_ADP = ler_PP(arquivo_ADP, "ADP") if arquivo_ADP else None

        df_PP3 = ler_PP(arquivo_PP3, "PP3") if arquivo_PP3 else None

        # ======================================================
        # CONSOLIDAÇÃO
        # ======================================================

        base = consolidar_base(
            df_ADE,
            df_PP1,
            df_PP2,
            df_ADP,
            df_PP3,
        )

        
        # ======================================================
        # GERA EXCEL
        # ======================================================

        output = gerar_excel(base)  

    # ======================================================
    # DOWNLOAD
    # ======================================================

    nome_arquivo = "RADAR_URE"

    if nome_ure.strip():

        nome_arquivo = (
            f"RADAR_{nome_ure.upper().replace(' ', '_')}"
        )

    st.success("Radar gerado com sucesso!")

    st.download_button(
        label="⬇ BAIXAR RADAR",
        data=output,
        file_name=f"{nome_arquivo}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )
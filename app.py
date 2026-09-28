# ==========================================================
# RADAR PEDAGÓGICO URE
# APP PRINCIPAL
# ==========================================================

import streamlit as st

from modulos.leitor_adp import ler_ADP
from modulos.leitor_pp import ler_PP
from modulos.consolidacao import consolidar_base
from modulos.indicadores import calcular_indicadores_escolas
from modulos.farol import aplicar_farol
from modulos.diagnostico import aplicar_diagnostico
from modulos.excel.excel_final import gerar_excel


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(
    page_title="Radar Pedagógico URE",
    page_icon="📊",
    layout="wide",
)


# ==========================================================
# TÍTULO
# ==========================================================

st.title("📊 Radar Pedagógico URE")
st.caption("Painel Gerencial das Escolas da URE")

st.divider()


# ==========================================================
# NOME DA URE
# ==========================================================

nome_ure = st.text_input(
    "Nome da URE",
    placeholder="Ex.: Pirassununga",
)

st.divider()


# ==========================================================
# ARQUIVOS
# ==========================================================

st.subheader("Arquivos")

arquivo_PP1 = st.file_uploader(
    "PP1",
    type=["xlsx"],
)

arquivo_PP2 = st.file_uploader(
    "PP2",
    type=["xlsx"],
)

arquivo_ADP = st.file_uploader(
    "ADP – AVD1 + AVD2",
    type=["xlsx"],
)

arquivo_PP3 = st.file_uploader(
    "PP3",
    type=["xlsx"],
)

st.divider()


# ==========================================================
# GERAR RADAR
# ==========================================================

if st.button(
    "🚀 GERAR RADAR",
    use_container_width=True,
):

    # ------------------------------------------------------
    # VALIDAÇÃO
    # ------------------------------------------------------

    if arquivo_ADP is None:
        st.error(
            "Selecione o arquivo ADP contendo os dados "
            "da AVD1 e da AVD2."
        )
        st.stop()

    # ------------------------------------------------------
    # PROCESSAMENTO
    # ------------------------------------------------------

    try:

        with st.spinner(
            "Gerando Radar Pedagógico..."
        ):

            # ==============================================
            # LEITURA DO ADP
            # ==============================================

            # O arquivo ADP contém AVD1 + AVD2.
            df_ADP = ler_ADP(arquivo_ADP)

            # ==============================================
            # LEITURA PP1
            # ==============================================

            df_PP1 = (
                ler_PP(
                    arquivo_PP1,
                    "PP1",
                )
                if arquivo_PP1 is not None
                else None
            )

            # ==============================================
            # LEITURA PP2
            # ==============================================

            df_PP2 = (
                ler_PP(
                    arquivo_PP2,
                    "PP2",
                )
                if arquivo_PP2 is not None
                else None
            )

            # ==============================================
            # LEITURA PP3
            # ==============================================

            df_PP3 = (
                ler_PP(
                    arquivo_PP3,
                    "PP3",
                )
                if arquivo_PP3 is not None
                else None
            )

            # ==============================================
            # CONSOLIDAÇÃO
            # ==============================================

            # IMPORTANTE:
            # O ADP deve entrar em df_ADP.
            #
            # A sequência interna do Radar permanece:
            #
            # AVD1 → PP1 → PP2 → AVD2 → PP3
            #
            # AVD1 e AVD2 já estão dentro do ADP.

            base = consolidar_base(
                df_ADE=None,
                df_PP1=df_PP1,
                df_PP2=df_PP2,
                df_ADP=df_ADP,
                df_PP3=df_PP3,
            )

            # ==============================================
            # INDICADORES
            # ==============================================

            base = calcular_indicadores_escolas(
                base
            )

            # ==============================================
            # FAROL URE
            # ==============================================

            base = aplicar_farol(
                base
            )

            # ==============================================
            # DIAGNÓSTICO
            # ==============================================

            base = aplicar_diagnostico(
                base
            )

            # ==============================================
            # GERAÇÃO DO EXCEL
            # ==============================================

            output = gerar_excel(
                base
            )

    except Exception as erro:

        st.error(
            "Ocorreu um erro durante a geração do Radar."
        )

        st.exception(erro)

        st.stop()

    # ======================================================
    # NOME DO ARQUIVO
    # ======================================================

    nome_arquivo = "RADAR_URE"

    if nome_ure.strip():

        nome_arquivo = (
            f"RADAR_"
            f"{nome_ure.strip().upper().replace(' ', '_')}"
        )

    # ======================================================
    # RESULTADO
    # ======================================================

    st.success(
        "Radar gerado com sucesso!"
    )

    st.download_button(
        label="⬇ BAIXAR RADAR",
        data=output,
        file_name=f"{nome_arquivo}.xlsx",
        mime=(
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        ),
        use_container_width=True,
    )
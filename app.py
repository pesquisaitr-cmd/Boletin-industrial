import os
import streamlit as st
from src.pptx_engine import processar_relatorio

st.set_page_config(page_title="Gerador - Boletim Industrial", layout="centered")

st.title("📊 Gerador do Boletim Industrial")
st.write("Selecione os parâmetros para compilar o relatório completo de 36 páginas.")

with st.form("form_relatorio"):
    col1, col2 = st.columns(2)
    with col1:
        edicao_atual = st.text_input("Edição Atual", value="45")
        edicao_anterior = st.text_input("Edição Anterior", value="44")
    with col2:
        periodo_atual = st.selectbox("Período", ["1T26", "2T26", "3T26", "4T26"], index=1)
    
    btn_gerar = st.form_submit_button("🔥 Gerar Relatório Automatizado")

if btn_gerar:
    mapa_dados = {
        "1T26": periodo_atual,
        "1º Trimestre": f"{periodo_atual[0]}º Trimestre",
        "EDICAO_ANTERIOR": edicao_anterior,
        "EDICAO_ATUAL": edicao_atual,
        "44": edicao_anterior,
        "45": edicao_atual
    }
    
    caminho_template = "templates/modelo-boletim.pptx"
    
    if os.path.exists(caminho_template):
        pptx_processado = processar_relatorio(caminho_template, mapa_dados)
        nome_download = f"Boletim_Industrial_{edicao_atual}_{periodo_atual}.pptx"
        
        st.success("✅ Relatório gerado com sucesso!")
        st.download_button(
            label="📥 Baixar Boletim em PPTX",
            data=pptx_processado,
            file_name=nome_download,
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
    else:
        st.error(f"Arquivo '{caminho_template}' não encontrado no repositório.")

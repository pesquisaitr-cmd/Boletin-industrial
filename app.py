import os
import streamlit as st
from src.pptx_engine import processar_relatorio
from src.bigquery import buscar_dados_boletim

st.set_page_config(page_title="Gerador - Boletim Industrial", layout="centered")

st.title("📊 Gerador do Boletim Industrial")
st.write("Conectado ao BigQuery para extração automática dos indicadores.")

with st.form("form_relatorio"):
    col1, col2 = st.columns(2)
    with col1:
        edicao_atual = st.text_input("Edição Atual", value="45")
        edicao_anterior = st.text_input("Edição Anterior", value="44")
    with col2:
        periodo_atual = st.selectbox("Período no BigQuery", ["1T26", "2T26", "3T26", "4T26"], index=1)
    
    btn_gerar = st.form_submit_button("🔥 Buscar no BigQuery e Gerar PPTX")

if btn_gerar:
    with st.spinner(f"🔍 Consultando BigQuery para o período {periodo_atual}..."):
        dados_bigquery = buscar_dados_boletim(periodo=periodo_atual)
    
    mapa_dados = {
        f"Edição {edicao_anterior}": f"Edição {edicao_atual}",
        f"{edicao_anterior}ª": f"{edicao_atual}ª",
        "1T26": periodo_atual,
        "1º Trimestre": f"{periodo_atual[0]}º Trimestre",
    }
    
    # Atualiza o mapa de substituição com os valores do BigQuery
    mapa_dados.update(dados_bigquery)
    
    caminho_template = "templates/modelo-boletim.pptx"
    
    if os.path.exists(caminho_template):
        pptx_processado = processar_relatorio(caminho_template, mapa_dados)
        
        st.success(f"✅ Dados do BigQuery integrados com sucesso!")
        st.download_button(
            label="📥 Baixar Boletim Atualizado em PPTX",
            data=pptx_processado,
            file_name=f"Boletim_Industrial_{edicao_atual}_{periodo_atual}.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
    else:
        st.error(f"Arquivo '{caminho_template}' não encontrado.")

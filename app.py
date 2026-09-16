import os
import streamlit as st
from src.pptx_engine import processar_relatorio
from src.scrapers import obter_dados_2t26  # Importa a consulta das fontes

st.set_page_config(page_title="Gerador - Boletim Industrial", layout="centered")

st.title("📊 Gerador do Boletim Industrial")

with st.form("form_relatorio"):
    edicao_atual = st.text_input("Edição Atual", value="45")
    periodo_atual = st.selectbox("Período", ["1T26", "2T26", "3T26", "4T26"], index=1)
    btn_gerar = st.form_submit_button("🔥 Consultar Fontes e Gerar Relatório")

if btn_gerar:
    st.info("📡 Consultando fontes externas de dados (BCB, IBGE, CNI, Infomet)...")
    
    # 1. Busca os dados reais atualizados
    dados_externos = obter_dados_2t26()
    
    # 2. Consolida o mapa de substituição textual e numérica
    mapa_dados = {
        "1T26": periodo_atual,
        "1º Trimestre": "2º Trimestre",
        "Edição 44": f"Edição {edicao_atual}",
    }
    # Mescla os dados das fontes externas no mapa do relatório
    mapa_dados.update(dados_externos)
    
    caminho_template = "templates/modelo-boletim.pptx"
    
    if os.path.exists(caminho_template):
        pptx_processado = processar_relatorio(caminho_template, mapa_dados)
        
        st.success("✅ Consultas concluídas e relatório montado!")
        st.download_button(
            label="📥 Baixar Boletim Atualizado em PPTX",
            data=pptx_processado,
            file_name=f"Boletim_Industrial_{edicao_atual}_{periodo_atual}.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )

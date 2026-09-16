import os
import streamlit as st
from src.pptx_engine import processar_relatorio

st.set_page_config(page_title="Gerador - Boletim Industrial", layout="centered")

st.title("📊 Gerador do Boletim Industrial")
st.write("Configure os parâmetros da nova edição para atualizar o relatório de 36 páginas.")

with st.form("form_relatorio"):
    col1, col2 = st.columns(2)
    with col1:
        edicao_atual = st.text_input("Edição Atual (Nova)", value="45")
        edicao_anterior = st.text_input("Edição Anterior (Para substituir)", value="44")
    with col2:
        periodo_atual = st.selectbox("Novo Período de Referência", ["1T26", "2T26", "3T26", "4T26"], index=1)
        periodo_anterior = st.text_input("Período Anterior no Modelo", value="1T26")
    
    btn_gerar = st.form_submit_button("🔥 Gerar Relatório Automatizado")

if btn_gerar:
    # Mapeamento abrangente de variações textuais nos 36 slides
    mapa_dados = {
        # Substituição da Edição
        f"Edição {edicao_anterior}": f"Edição {edicao_atual}",
        f"{edicao_anterior}ª Edição": f"{edicao_atual}ª Edição",
        f"{edicao_anterior}ª": f"{edicao_atual}ª",
        
        # Substituição do Período/Trimestre
        periodo_anterior: periodo_atual,
        "1º Trimestre": "2º Trimestre" if "2T" in periodo_atual else ("3º Trimestre" if "3T" in periodo_atual else "4º Trimestre"),
        "1º trimestre": "2º trimestre" if "2T" in periodo_atual else ("3º trimestre" if "3T" in periodo_atual else "4º trimestre"),
        "primeiro trimestre": "segundo trimestre" if "2T" in periodo_atual else "trimestre",
    }
    
    caminho_template = "templates/modelo-boletim.pptx"
    
    if os.path.exists(caminho_template):
        st.info("Processando os 36 slides e aplicando as substituições...")
        pptx_processado = processar_relatorio(caminho_template, mapa_dados)
        nome_download = f"Boletim_Industrial_{edicao_atual}_{periodo_atual}.pptx"
        
        st.success(f"✅ Relatório da Edição {edicao_atual} ({periodo_atual}) gerado com sucesso!")
        st.download_button(
            label="📥 Baixar Boletim Atualizado em PPTX",
            data=pptx_processado,
            file_name=nome_download,
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
    else:
        st.error(f"Arquivo '{caminho_template}' não encontrado no repositório.")

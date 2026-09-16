import os
import streamlit as st
from src.pptx_engine import processar_relatorio
from src.scrapers import obter_todos_os_dados

st.set_page_config(page_title="Gerador - Boletim Industrial", layout="centered")

st.title("📊 Gerador do Boletim Industrial")
st.write("Atualize os marcadores e execute a consulta às fontes de dados (BCB, CNI, Infomet).")

with st.form("form_relatorio"):
    col1, col2 = st.columns(2)
    with col1:
        edicao_atual = st.text_input("Edição Atual (Nova)", value="45")
        edicao_anterior = st.text_input("Edição Anterior no Modelo", value="44")
    with col2:
        periodo_atual = st.selectbox("Novo Período", ["1T26", "2T26", "3T26", "4T26"], index=1)
        periodo_anterior = st.text_input("Período Anterior no Modelo", value="1T26")
    
    btn_gerar = st.form_submit_button("🔥 Executar Consultas e Gerar PPTX")

if btn_gerar:
    with st.spinner("📡 Consultando APIs e scraping de dados (IBC-Br, CNI, Infomet)..."):
        dados_coletados = obter_todos_os_dados()
    
    # Monta o dicionário completo com marcadores de edição, período e dados de web scraping
    mapa_dados = {
        f"Edição {edicao_anterior}": f"Edição {edicao_atual}",
        f"edicao {edicao_anterior}": f"edicao {edicao_atual}",
        f"{edicao_anterior}ª": f"{edicao_atual}ª",
        f"Nº {edicao_anterior}": f"Nº {edicao_atual}",
        periodo_anterior: periodo_atual,
        "1º Trimestre": "2º Trimestre" if "2T" in periodo_atual else "Trimestre",
        "1º trimestre": "2º trimestre" if "2T" in periodo_atual else "trimestre",
    }
    
    # Injeta os valores obtidos do web scraping no mapa de substituição
    mapa_dados.update(dados_coletados)
    
    caminho_template = "templates/modelo-boletim.pptx"
    
    if os.path.exists(caminho_template):
        pptx_processado = processar_relatorio(caminho_template, mapa_dados)
        nome_download = f"Boletim_Industrial_{edicao_atual}_{periodo_atual}.pptx"
        
        st.success(f"✅ Relatório da Edição {edicao_atual} ({periodo_atual}) compilado com sucesso!")
        st.download_button(
            label="📥 Baixar Boletim Atualizado em PPTX",
            data=pptx_processado,
            file_name=nome_download,
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
    else:
        st.error(f"Arquivo '{caminho_template}' não encontrado.")

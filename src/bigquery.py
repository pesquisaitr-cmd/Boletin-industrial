import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account

def conectar_bigquery():
    """Autentica no BigQuery usando os secrets do Streamlit."""
    try:
        credentials = service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"]
        )
        client = bigquery.Client(
            credentials=credentials, 
            project=credentials.project_id
        )
        return client
    except Exception as e:
        st.error(f"Erro ao conectar ao BigQuery: {e}")
        return None

def buscar_dados_boletim(periodo="2T26"):
    """
    Consulta as tabelas do BigQuery e retorna um dicionário 
    com todos os valores atualizados para o período solicitado.
    """
    client = conectar_bigquery()
    if not client:
        return {}

    # Ajuste o nome do dataset e da tabela conforme sua estrutura no GCP
    query = f"""
        SELECT chave_indicador, valor_indicador 
        FROM `{client.project}.dataset_boletim.tb_indicadores`
        WHERE periodo = '{periodo}'
    """
    
    try:
        query_job = client.query(query)
        resultados = query_job.result()
        
        # Converte as linhas do banco em dicionário de substituição
        dados_mapeados = {row.chave_indicador: str(row.valor_indicador) for row in resultados}
        return dados_mapeados
    except Exception as e:
        st.warning(f"Não foi possível carregar dados do BigQuery para {periodo}: {e}")
        return {}

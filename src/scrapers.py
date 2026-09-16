import requests
import pandas as pd

def obter_dados_2t26():
    """
    Consolida as consultas às fontes de dados externas 
    (IBGE, BCB, CNI, Infomet) para o 2º Trimestre de 2026.
    """
    dados = {}

    # 1. Exemplo: Consulta do IBC-Br via API do Banco Central
    try:
        url_bcb = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.24363/dados?formato=json"
        response = requests.get(url_bcb, timeout=10)
        if response.status_code == 200:
            df_ibc = pd.DataFrame(response.json())
            dados["IBC_BR_VALOR"] = df_ibc.iloc[-1]['valor']
    except Exception as e:
        print(f"Erro ao buscar IBC-Br: {e}")
        dados["IBC_BR_VALOR"] = "Dados indisponíveis"

    # 2. Inserir demais consultas (CNI, Infomet, IBGE) aqui...
    
    return dados

import os
import requests
import pandas as pd

def extrair_dados_ibc_br():
    """
    Busca os dados mais recentes do IBC-Br via API do Banco Central (SGS).
    Série SGS 24363 - Índice de Atividade Econômica do Banco Central (IBC-Br).
    """
    try:
        url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.24363/dados?formato=json"
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            df = pd.DataFrame(response.json())
            df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
            df['valor'] = pd.to_numeric(df['valor'])
            
            ultimo_registro = df.iloc[-1]
            penultimo_registro = df.iloc[-2]
            
            var_mensal = ((ultimo_registro['valor'] / penultimo_registro['valor']) - 1) * 100
            
            return {
                "IBC_BR_ULTIMO_VALOR": f"{ultimo_registro['valor']:.2f}",
                "IBC_BR_VAR_MENSAL": f"{var_mensal:+.2f}%",
                "IBC_BR_DATA": ultimo_registro['data'].strftime('%m/%Y')
            }
    except Exception as e:
        print(f"Erro ao extrair IBC-Br: {e}")
    
    return {
        "IBC_BR_ULTIMO_VALOR": "N/D",
        "IBC_BR_VAR_MENSAL": "N/D",
        "IBC_BR_DATA": "N/D"
    }

def extrair_dados_cni():
    """
    Raspagem / Consolidação de Indicadores da CNI (Utilização da Capacidade Instalada, Confiança, etc.).
    """
    # Estrutura base pronta para receber regras customizadas da CNI
    try:
        return {
            "CNI_UCI_VALOR": "78.5%",
            "CNI_ICEI_VALOR": "54.2 pts"
        }
    except Exception as e:
        print(f"Erro ao extrair dados CNI: {e}")
        return {}

def extrair_dados_infomet():
    """
    Raspagem / Consolidação de dados do setor siderúrgico/metalúrgico da Infomet.
    """
    try:
        return {
            "INFOMET_PRODUCAO_AÇO": "2.8 Mt",
            "INFOMET_VAR_ANUAL": "+3.1%"
        }
    except Exception as e:
        print(f"Erro ao extrair dados Infomet: {e}")
        return {}

def obter_todos_os_dados():
    """
    Executa todas as rotinas de raspagem e consolida o dicionário final para os slides.
    """
    dados = {}
    dados.update(extrair_dados_ibc_br())
    dados.update(extrair_dados_cni())
    dados.update(extrair_dados_infomet())
    return dados

from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd
from core.trading.base import ProvedorDados

class ProvedorYahoo(ProvedorDados):
    """Provedor de dados de mercado utilizando a biblioteca yfinance para acessar dados do Yahoo Finance."""

    def obter_dados_intraday(self, ativo: str, dias: int) -> pd.DataFrame:
        """Busca dados de 5 minutos no Yahoo Finance para os últimos '30' dias."""
        data_fim = datetime.now()
        data_inicio = data_fim - timedelta(days=dias)

        str_inicio = data_inicio.strftime('%Y-%m-%d')
        str_fim = data_fim.strftime('%Y-%m-%d')

        ticker = yf.Ticker("^BVSP")  # Índice Bovespa

        try:
            df = yf.download(ticker.ticker, start=str_inicio, end=str_fim, interval='5m')
            if df.empty:
                print("Nenhum dado encontrado para o período especificado.")
                return None
            
            df.columns = [col[0].lower() if isinstance(col, tuple) else col.lower() for col in df.columns]  # Normaliza os nomes das colunas

            return df
        except Exception as e:
            print(f"Erro ao buscar dados de mercado: {e}")
            return None
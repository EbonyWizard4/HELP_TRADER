"""core/trading/base.py: Define as interfaces para estratégias de trading e provedores de dados."""
from abc import ABC, abstractmethod
import pandas as pd

class EstrategiaTrading(ABC):
    """Contrato que todo setup é obrigado a seguir (principio OCP/LSP)"""
    @abstractmethod
    def executar(self, df) -> dict:
        """Recebe um DataFrame e retorna um dicionário com os resultados/metricas do backtest"""
        pass

class ProvedorDados(ABC):
    """Contrato para busca de dados no mercado (principio DIP)"""
    @abstractmethod
    def obter_dados_intraday(self, ativo: str, dias: int) -> pd.DataFrame:
        """Busca os dados do mercado e retorna um DataFrame personalizado"""
        pass
"""core/trading/base.py: Define as interfaces abstratas para filtros de sinais e provedores de dados."""
from abc import ABC, abstractmethod
import pandas as pd

class FiltroSinal(ABC):
    """Contrato puramente para identificar gatilhos de entrada (Princípios OCP/LSP)."""
    
    @abstractmethod
    def tem_sinal_compra(self, df: pd.DataFrame, idx: int) -> bool:
        """Retorna True se o setup autoriza a compra no candle de índice 'idx'."""
        pass


class ProvedorDados(ABC):
    """Contrato para busca e padronização de dados de mercado (Princípio DIP)."""
    
    @abstractmethod
    def obter_dados_intraday(self, ativo: str, dias: int) -> pd.DataFrame:
        """Busca os dados do mercado e retorna um DataFrame padronizado."""
        pass
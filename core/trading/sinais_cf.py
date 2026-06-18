# core/trading/sinais_cf.py
from core.trading.base import FiltroSinal

class SinalCandleForca(FiltroSinal):
    def tem_sinal_compra(self, df, idx) -> bool:
        # Lógica pura se o candle anterior foi uma barra de força
        corpo_anterior = df['corpo'].iloc[idx-1].item()
        media_corpo = df['media_corpo'].iloc[idx-2].item()
        fechamento_alta = df['close'].iloc[idx-1].item() > df['open'].iloc[idx-1].item()
        return corpo_anterior > (media_corpo * 1.8) and fechamento_alta
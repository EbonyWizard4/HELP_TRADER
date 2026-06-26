# core/trading/sinais_91.py
from core.trading.base import FiltroSinal

class Sinal91(FiltroSinal):
    def tem_sinal_compra(self, df, idx) -> bool:
        # Lógica matemática pura da virada da média no candle anterior
        media_retrasada_caindo = df['mme9'].iloc[idx-2].item() < df['mme9'].iloc[idx-3].item()
        media_anterior_subindo = df['mme9'].iloc[idx-1].item() > df['mme9'].iloc[idx-2].item()
        return media_retrasada_caindo and media_anterior_subindo
    
    def tem_sinal_venda(self, df, idx) -> bool:
        # Lógica matemática pura da virada da média no candle anterior
        media_retrasada_subindo = df['mme9'].iloc[idx-2].item() > df['mme9'].iloc[idx-3].item()
        media_anterior_caindo = df['mme9'].iloc[idx-1].item() < df['mme9'].iloc[idx-2].item()
        return media_retrasada_subindo and media_anterior_caindo
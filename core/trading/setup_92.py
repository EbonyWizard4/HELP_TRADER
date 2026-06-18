import pandas as pd
from core.trading.base import FiltroSinal
from core.trading.indicator import calcula_mme9
from core.trading.sinais_91 import Sinal91

class Setup92(Sinal91):
    """ Implementação do setup 92 de Compra do Lary Willians. """

    def executar(self, df: pd.DataFrame) -> dict:
        """ Aplica o setup 92 de Venda e calcula as estatísticas de acerto. """
        
        if df is None or df.empty:
            return None
        
        df = calcula_mme9(df)

        total_sinais = 0
        gains = 0
        losses = 0

        # Varreduras dos candles
        for i in range(2, len(df)):
            media_subindo = df['mme9'].iloc[i-1].item() > df['mme9'].iloc[i-2].item()
            fechamento_menor_que_anterior = df['close'].iloc[i-1].item() < df['close'].iloc[i-2].item()

            if media_subindo and fechamento_menor_que_anterior:
                total_sinais += 1

                preco_entrada = float(df['high'].iloc[i-1].item())
                stop_loss = float(df['low'].iloc[i-1].item())

                risco =  preco_entrada - stop_loss
                alvo_gain = preco_entrada + (risco * 1.5)

                for j in range(i, min(i + 20, len(df))):
                    maxima_atual = float(df['high'].iloc[j].item())
                    minima_atual = float(df['low'].iloc[j].item())
                    if minima_atual <= stop_loss:
                        losses += 1
                        break
                    elif maxima_atual >= alvo_gain:
                        gains += 1
                        break

        return self._consolidar_resultados(df, total_sinais, gains, losses)
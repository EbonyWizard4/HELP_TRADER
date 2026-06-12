import pandas as pd
from core.trading.base import EstrategiaTrading
from core.trading.indicator import calcula_mme9

class Setup91(EstrategiaTrading):
    """ Implementação do setup 91 de Compra do Lary Willians. """

    def executar(self, df: pd.DataFrame) -> dict:
        """ Aplica o setup 91 de Compra e calcula as estatísticas de acerto. """
        
        if df is None or df.empty:
            return None
        
        df = calcula_mme9(df)

        total_sinais = 0
        gains = 0
        losses = 0

        # Varreduras dos candles
        for i in range(3, len(df)):
            media_retrasada_caindo = df['mme9'].iloc[i-2].item() < df['mme9'].iloc[i-3].item()
            media_anterior_subindo = df['mme9'].iloc[i-1].item() > df['mme9'].iloc[i-2].item()

            if media_retrasada_caindo and media_anterior_subindo:
                total_sinais += 1

                preco_entrada = float(df['high'].iloc[i-1].item())
                stop_loss = float(df['low'].iloc[i-1].item())

                risco = preco_entrada - stop_loss
                alvo_gain = preco_entrada + risco

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
    
    def _consolidar_resultados(self, df: pd.DataFrame, total_sinais: int, gains: int, losses: int) -> dict:

        # Consolidação dos resultados para a tela.
        total_candles = len(df)
        abertura_inicial = float(df['open'].iloc[0].item())
        fechamento_final = float(df['close'].iloc[-1].item())
        variacao_pontos = fechamento_final - abertura_inicial
        tendencia = "Alta" if variacao_pontos > 0 else "Baixa" if variacao_pontos < 0 else "Neutra"
        taxa_acerto = (gains / total_sinais) * 100 if total_sinais > 0 else 0

        return {
            "total_candles": total_candles,
            "abertura_inicial": round(abertura_inicial, 2),
            "fechamento_final": round(fechamento_final, 2),
            "variacao_pontos": round(variacao_pontos, 2),
            "tendencia": tendencia,
            "total_sinais": total_sinais,
            "gains": gains,
            "losses": losses,
            "taxa_acerto": round(taxa_acerto, 2)
        }
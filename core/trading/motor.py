"""core/trading/motor.py: Motor de execução centralizado para simulação de backtests."""
import pandas as pd

class MotorBacktest:
    def __init__(self, filtros: list, risco_retorno: float = 2.0):
        self.filtros = filtros  # Recebe a lista de sinais (ex: [Sinal91()])
        self.proporcao_alvo = risco_retorno

    def executar(self, df: pd.DataFrame) -> dict:
        """Varre o histórico aplicando os filtros e gerenciando o risco."""
        if df is None or df.empty:
            return None

        # Garante os cálculos básicos para os filtros funcionarem
        df['mme9'] = df['close'].ewm(span=9, adjust=False).mean()
        df['corpo'] = (df['close'] - df['open']).abs()
        df['media_corpo'] = df['corpo'].rolling(window=20).mean()

        total_sinais = 0
        gains = 0
        losses = 0

        # Loop de simulação (centralizado e único!)
        for i in range(20, len(df)):
            # Se todos os filtros derem sinal True no candle 'i'
            if all(filtro.tem_sinal_compra(df, i) for filtro in self.filtros):
                total_sinais += 1
                
                preco_entrada = float(df['high'].iloc[i-1].item())
                stop_loss = float(df['low'].iloc[i-1].item())
                risco = preco_entrada - stop_loss
                alvo_gain = preco_entrada + (risco * self.proporcao_alvo)
                
                for j in range(i, min(i + 20, len(df))):
                    if float(df['low'].iloc[j].item()) <= stop_loss:
                        losses += 1
                        break
                    elif float(df['high'].iloc[j].item()) >= alvo_gain:
                        gains += 1
                        break

        return self._consolidar(df, total_sinais, gains, losses)

    def _consolidar(self, df, total_sinais, gains, losses):
        total_candles = len(df)
        abertura_inicial = float(df['open'].iloc[0].item())
        fechamento_final = float(df['close'].iloc[-1].item())
        variacao_pontos = fechamento_final - abertura_inicial
        taxa = (gains / total_sinais * 100) if total_sinais > 0 else 0
        
        return {
            "total_candles": total_candles,
            "abertura_inicial": round(abertura_inicial, 2),
            "fechamento_final": round(fechamento_final, 2),
            "variacao_pontos": round(variacao_pontos, 2),
            "tendencia": "Alta" if variacao_pontos >= 0 else "Baixa",
            "total_sinais": total_sinais,
            "gains": gains,
            "losses": losses,
            "taxa_acerto": round(taxa, 2)
        }
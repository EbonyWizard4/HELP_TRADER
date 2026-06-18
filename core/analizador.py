from datetime import datetime, timedelta
import yfinance as yf
import pandas as pd

def analisar_mini_indice():
    # 1. Definição do período (Máximo de 60 dias para dados de 5m no Yahoo)
    # Vamos pegar os últimos 30 dias para vir um histórico bem encorpado
    data_fim = datetime.now()
    data_inicio = data_fim - timedelta(days=30)
    
    str_inicio = data_inicio.strftime('%Y-%m-%d')
    str_fim = data_fim.strftime('%Y-%m-%d')
    
    # Ticker do Índice Bovespa no Yahoo Finance
    ticker = "^BVSP"
    
    try:
        # 2. Download dos dados de 5 minutos pelo Yahoo
        df = yf.download(tickers=ticker, start=str_inicio, end=str_fim, interval="5m")
        
        if df.empty:
            print("⚠️ DataFrame do Yahoo veio vazio.")
            return None

        # Limpeza de colunas (o Yahoo às vezes retorna MultiIndex ou letras maiúsculas)
        df.columns = [col[0].lower() if isinstance(col, tuple) else col.lower() for col in df.columns]

    except Exception as e:
        print(f"❌ Erro ao buscar dados no Yahoo Finance: {e}")
        return None

    # ==========================================
    # O MOTOR MATEMÁTICO DO ROBÔ (SETUP 9.1)
    # ==========================================
    # Cálculo da Média Móvel Exponencial de 9 períodos
    df['mme9'] = df['close'].ewm(span=9, adjust=False).mean()

    total_sinais = 0
    gains = 0
    losses = 0

    # Varredura dos candles
    for i in range(3, len(df)):
        # .item() é usado aqui para garantir que estamos pegando o número puro do Pandas
        media_retrasada_caindo = df['mme9'].iloc[i-2].item() < df['mme9'].iloc[i-3].item()
        media_anterior_subindo = df['mme9'].iloc[i-1].item() > df['mme9'].iloc[i-2].item()

        if media_retrasada_caindo and media_anterior_subindo:
            total_sinais += 1
            
            preco_entrada = float(df['high'].iloc[i-1].item())
            stop_loss = float(df['low'].iloc[i-1].item())
            
            risco = preco_entrada - stop_loss
            alvo_gain = preco_entrada + risco
            
            # Rastreia as próximas barras (até 20 candles para frente)
            for j in range(i, min(i + 20, len(df))):
                maxima_atual = float(df['high'].iloc[j].item())
                minima_atual = float(df['low'].iloc[j].item())

                if minima_atual <= stop_loss:
                    losses += 1
                    break
                elif maxima_atual >= alvo_gain:
                    gains += 1
                    break

    # 3. Métricas gerais para renderizar na tela
    total_candles = len(df)
    abertura_inicial = float(df['open'].iloc[0].item())
    fechamento_final = float(df['close'].iloc[-1].item())
    variacao_pontos = fechamento_final - abertura_inicial
    tendencia = "Alta" if variacao_pontos >= 0 else "Baixa"
    
    taxa_acerto = (gains / total_sinais * 100) if total_sinais > 0 else 0

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
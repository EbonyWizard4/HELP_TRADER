from datetime import datetime, timedelta
import yfinance as yf

def analizar_miniindice():
    # Definie o período: Data atual menos 1 dia e 30 dias para trás
    end_date = datetime.now() - timedelta(days=1)
    start_date = end_date - timedelta(days=30)

    # Formata as datas para o formato aceito pelo yfinance
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    # Tiker do contrato continuo do mini índice no yfinance
    ticker = 'WIN=F' 

    # Baixa os dados intraday do mini índice candles de 5 minutos
    df = yf.download(ticker, start=start_date_str, end=end_date_str, interval='5m')

    if df.empty:
        print("Nenhum dado encontrado para o período especificado.")
        return
    
    # Processamento dos dados solicitados
    total_candles = len(df)

    # Valores de abertura inicial e fechamento final
    # Usamos o .item() para extrair o valor númerico puro do DataFrame
    abertura_inicial = float(df['Open'].iloc[0].item())
    fechamento_final = float(df['Close'].iloc[-1].item())

    # Calculo do resultado do período
    resultado_periodo = fechamento_final - abertura_inicial
    tendencia = "Alta" if resultado_periodo > 0 else "Baixa" if resultado_periodo < 0 else "Neutra"

    return {
        "total_candles": total_candles,
        "abertura_inicial": abertura_inicial,
        "fechamento_final": fechamento_final,
        "resultado_periodo": resultado_periodo,
        "tendencia": tendencia
    }
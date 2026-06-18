"""core/trading/__init__.py: Fábrica que mapeia os sinais da tela e entrega o motor configurado."""
from core.trading.motor import MotorBacktest
from core.trading.sinais_91 import Sinal91  # Adapte o nome do seu arquivo de sinal se necessário

def obter_estrategia(nome: str):
    """Monta o Motor de Backtest com os filtros selecionados na tela."""
    if nome == "9.1":
        # Retorna o Motor contendo apenas o filtro do 9.1
        return MotorBacktest(filtros=[Sinal91()])
    
    # Se não mapear nada, devolve o motor padrão com 9.1
    return MotorBacktest(filtros=[Sinal91()])
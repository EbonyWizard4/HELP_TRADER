"""core/trading/__init__.py: Fábrica que mapeia os sinais da tela e entrega o motor configurado."""
from core.trading.motor import MotorBacktest
from core.trading.sinais_91 import Sinal91
from core.trading.sinais_cf import SinalCF

# Mapeamento estático: associa a string do HTML com a classe do Filtro
MAPA_SINAIS = {
    "9.1": Sinal91,
    "candle_forca": SinalCF
}

def obter_motor_configurado(setups_selecionados: list, risco_retorno: str) -> MotorBacktest:
    """
    Instancia dinamicamente os filtros baseados nas escolhas do usuário
    e injeta tudo dentro do Motor Centralizado com o risco escolhido.
    """
    filtros_instanciados = []
    
    # 1. Converte as strings do HTML em objetos de Filtro Reais
    for nome in setups_selecionados:
        if nome in MAPA_SINAIS:
            classe_filtro = MAPA_SINAIS[nome]
            filtros_instanciados.append(classe_filtro()) # Instancia o objeto (ex: Sinal91())
            
    # 2. Se o usuário desmarcar tudo por acidente, garante pelo menos o 9.1 ativo
    if not filtros_instanciados:
        filtros_instanciados = [Sinal91()]
        
    # 3. Trata o valor do risco que vem como string do HTML para float
    try:
        risco_float = float(risco_retorno)
    except (ValueError, TypeError):
        risco_float = 2.0 # Valor padrão de segurança
        
    # 4. Retorna o Motor com as peças de Lego encaixadas!
    return MotorBacktest(filtros=filtros_instanciados, risco_retorno=risco_float)
from core.trading.setup_91 import Setup91
from core.trading.setup_92 import Setup92

# Um catálogo de estratégias mapeadas por uma string simples
ESTRATEGIAS = {
    "9.1": Setup91(),
    "9.2": Setup92()
}

def obter_estrategia(nome: str):
    return ESTRATEGIAS.get(nome, Setup91())
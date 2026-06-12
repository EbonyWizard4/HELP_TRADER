from flask import Flask, render_template, request, Blueprint
# importando modulos especializados.
from core.services.market_data import buscar_dados_mercado
from core.trading.indicator import calcula_mme9
from core.trading.setup_91 import executar_backtest_91

from core.analizador import analisar_mini_indice

# Blueprint main
main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    dados = None

    if request.method == 'POST':
        # 1. Buscar os dados do mercado (infra estrutura)
        df_bruto = buscar_dados_mercado(dias=30)

        # 2. Calcular os indicadores (matemática)
        df_com_indicadores = calcula_mme9(df_bruto)

        # 3. Executar o backtest do setup 91 (lógica de trading)
        dados = executar_backtest_91(df_com_indicadores)

    return render_template('index.html', resultado=dados)

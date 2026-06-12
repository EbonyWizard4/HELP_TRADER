from flask import Flask, render_template, request, Blueprint
# importando modulos especializados.
from core.services.market_data import ProvedorYahoo
from core.trading import obter_estrategia

# Blueprint main
main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    dados = None
    setup_selecionado = "9.1" # Padrão inicial.

    if request.method == 'POST':
        # Capturar o setup selecionado pelo usuário.
        setup_selecionado = request.form.get('setup', '9.1')

        # Inversão da dependencia (DPI) - Instanciando o provedor pela interface.
        provedor = ProvedorYahoo()
        # 1. Buscar os dados do mercado (infra estrutura)
        df_bruto = provedor.obter_dados_intraday(ativo='^BVSP', dias=30)  

        # Principio do aberto/fechado (OCP) - Buscar a estratégia pelo catalogo.
        estrategia = obter_estrategia(setup_selecionado)

        # Executar o backtest da estratégia sem saber as regras internas, apenas a interface.
        dados = estrategia.executar(df_bruto)

    return render_template('index.html', resultado=dados, setup=setup_selecionado)

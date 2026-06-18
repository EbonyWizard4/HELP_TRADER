'''core/routes.py - Define as rotas principais da aplicação, incluindo a página inicial e a rota de exportação de PDF.'''
from datetime import datetime
from flask import Blueprint, render_template, request, send_file
from core.services.market_data import ProvedorYahoo
from core.trading import obter_motor_configurado  # Atualizado o import da fábrica
from core.services.report_generator import GeradorRelatorioPDF

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    setups_ativos = ['9.1'] # Padrão inicial
    risco_ativo = '2.0'
    
    if request.method == 'POST':
        # Captura a lista de checkboxes marcados (ex: ['9.1', 'candle_forca'])
        setups_ativos = request.form.getlist('setups')
        risco_ativo = request.form.get('risco', '2.0')
        
        provedor = ProvedorYahoo()
        df_bruto = provedor.obter_dados_intraday(ativo="IBOV", dias=30)
        
        # Invocamos a nossa fábrica dinâmica do SOLID
        motor = obter_motor_configurado(setups_ativos, risco_ativo)
        resultado = motor.executar(df_bruto)
        
    return render_template('index.html', resultado=resultado, setups=setups_ativos, risco=risco_ativo)


@main_bp.route('/exportar', methods=['POST'])
def exportar_pdf():
    """Rota especializada em capturar os dados da tela e disparar o download do PDF."""
    setups_ativos = request.form.getlist('setups')
    risco_ativo = request.form.get('risco', '2.0')
    resumo_texto = request.form.get('resumo', '')
    
    provedor = ProvedorYahoo()
    df_bruto = provedor.obter_dados_intraday(ativo="IBOV", dias=30)
    
    motor = obter_motor_configurado(setups_ativos, risco_ativo)
    resultado = motor.executar(df_bruto)
    
    if not resultado:
        return "Erro ao processar dados para o PDF", 400
        
    # Texto amigável para o título do PDF indicando a confluência ativa
    nome_setup_composto = " + ".join(setups_ativos).upper() if setups_ativos else "NENHUM"
    
    pdf_buffer = GeradorRelatorioPDF.gerar_pdf_backtest(
        ativo="IBOV",
        nome_setup=f"{nome_setup_composto} (Alvo {risco_ativo}x)",
        resultados=resultado,
        resumo_usuario=resumo_texto
    )
    
    nome_arquivo = f"Relatorio_Backtest_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=nome_arquivo,
        mimetype='application/pdf'
    )
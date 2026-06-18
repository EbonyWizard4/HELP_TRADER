'''core/routes.py - Define as rotas principais da aplicação, incluindo a página inicial e a rota de exportação de PDF.'''
from flask import Blueprint, render_template, request, send_file
from core.services.market_data import ProvedorYahoo
from core.trading import obter_estrategia
from core.services.report_generator import GeradorRelatorioPDF # Importa o gerador

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    setup_selecionado = "9.1"
    
    if request.method == 'POST':
        setup_selecionado = request.form.get('setup', '9.1')
        
        provedor = ProvedorYahoo()
        df_bruto = provedor.obter_dados_intraday(ativo="IBOV", dias=30)
        
        estrategia = obter_estrategia(setup_selecionado)
        resultado = estrategia.executar(df_bruto)
        
    return render_template('index.html', resultado=resultado, setup=setup_selecionado)


@main_bp.route('/exportar', methods=['POST'])
def exportar_pdf():
    """Rota especializada em capturar os dados da tela e disparar o download do PDF."""
    setup_selecionado = request.form.get('setup', '9.1')
    resumo_texto = request.form.get('resumo', '')
    
    # Executa rapidamente o backtest para garantir a fidelidade dos dados atuais
    provedor = ProvedorYahoo()
    df_bruto = provedor.obter_dados_intraday(ativo="IBOV", dias=30)
    estrategia = obter_estrategia(setup_selecionado)
    resultado = estrategia.executar(df_bruto)
    
    if not resultado:
        return "Erro ao processar dados para o PDF", 400
        
    # Gera o PDF usando o nosso serviço do SOLID
    pdf_buffer = GeradorRelatorioPDF.gerar_pdf_backtest(
        ativo="IBOV",
        nome_setup=setup_selecionado,
        resultados=resultado,
        resumo_usuario=resumo_texto
    )
    
    # Envia o arquivo de volta para o navegador do usuário
    nome_arquivo = f"Relatorio_Setup_{setup_selecionado.replace('.', '')}_{datetime.now().strftime('%Y%m%d')}.pdf"
    
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=nome_arquivo,
        mimetype='application/pdf'
    )
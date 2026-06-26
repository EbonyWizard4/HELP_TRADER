import os
from io import BytesIO
from datetime import datetime
from xhtml2pdf import pisa

class GeradorRelatorioPDF:
    """Serviço responsável por transformar métricas de trade em relatórios PDF profissionais."""
    
    @staticmethod
    def gerar_pdf_backtest(ativo: str, nome_setup: str, resultados: dict, resumo_usuario: str = "") -> BytesIO:
        """Gera um PDF em memória (BytesIO) para o Flask enviar direto para download."""
        
        data_atual = datetime.now().strftime('%d/%m/%Y %H:%M')
        
        # HTML customizado com CSS inline focado na renderização do PDF
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                @page {{
                    size: a4;
                    margin: 2cm;
                }}
                body {{
                    font-family: 'Helvetica', 'Arial', sans-serif;
                    color: #1e293b;
                }}
                .header {{
                    border-bottom: 2px solid #2563eb;
                    padding-bottom: 10px;
                    margin-bottom: 20px;
                }}
                .titulo {{
                    font-size: 24px;
                    font-weight: bold;
                    color: #1e3a8a;
                }}
                .subtitulo {{
                    font-size: 12px;
                    color: #64748b;
                }}
                .section-titulo {{
                    font-size: 16px;
                    font-weight: bold;
                    color: #0f172a;
                    margin-top: 20px;
                    margin-bottom: 10px;
                    border-bottom: 1px solid #e2e8f0;
                    padding-bottom: 5px;
                }}
                .resumo-box {{
                    background-color: #f8fafc;
                    border-left: 4px solid #cbd5e1;
                    padding: 12px;
                    font-style: italic;
                    margin-bottom: 20px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-bottom: 20px;
                }}
                th {{
                    background-color: #2563eb;
                    color: white;
                    text-align: left;
                    padding: 8px;
                    font-size: 12px;
                }}
                td {{
                    padding: 8px;
                    border-bottom: 1px solid #e2e8f0;
                    font-size: 12px;
                }}
                .destaque {{
                    font-weight: bold;
                    color: #2563eb;
                }}
                .gain {{ color: #16a34a; font-weight: bold; }}
                .loss {{ color: #dc2626; font-weight: bold; }}
            </style>
        </head>
        <body>

            <div class="header">
                <div class="titulo">Help_trader • Diário de Bordo</div>
                <div class="subtitulo">Relatório de Evolução de Modelo Matemático — Gerado em: {data_atual}</div>
            </div>

            <div class="section-titulo">1. Identificação do Experimento</div>
            <table>
                <tr>
                    <td><strong>Ativo Analisado:</strong> {ativo}</td>
                    <td><strong>Estratégia Utilizada:</strong> Setup {nome_setup}</td>
                </tr>
            </table>

            <div class="section-titulo">2. Notas de Evolução e Insights</div>
            <div class="resumo-box">
                {resumo_usuario if resumo_usuario else "Nenhuma nota inserida para esta rodada de testes."}
            </div>

            <div class="section-titulo">3. Métricas de Mercado (Janela de 30 dias)</div>
            <table>
                <tr>
                    <td><strong>Total de Candles (5m):</strong> {resultados['total_candles']}</td>
                    <td><strong>Tendência Macro:</strong> {resultados['tendencia']} ({resultados['variacao_pontos']} pts)</td>
                </tr>
                <tr>
                    <td><strong>Abertura Período:</strong> {resultados['abertura_inicial']} pts</td>
                    <td><strong>Fechamento Período:</strong> {resultados['fechamento_final']} pts</td>
                </tr>
            </table>

            <div class="section-titulo">4. Performance da Estratégia</div>
            <table>
                <thead>
                    <tr>
                        <th>Métrica</th>
                        <th>Resultado Obtido</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Total de Sinais Armados</td>
                        <td class="destaque">{resultados['total_sinais']}</td>
                    </tr>
                    <tr>
                        <td>Operações com GAIN (Alvo atingido)</td>
                        <td class="gain">{resultados['gains']}</td>
                    </tr>
                    <tr>
                        <td>Operações com LOSS (Stop atingido)</td>
                        <td class="loss">{resultados['losses']}</td>
                    </tr>
                    <tr>
                        <td><strong>Taxa de Acerto Final</strong></td>
                        <td class="destaque" style="font-size: 14px;">{resultados['taxa_acerto']}%</td>
                    </tr>
                    <tr style="background-color: #f8fafc;">
                        <td><strong>Saldo Final Acumulado</strong></td>
                        <td class="{'gain' if resultados['saldo_estrategia'] >= 0 else 'loss'}" style="font-size: 14px;">
                            {'+' if resultados['saldo_estrategia'] >= 0 else ''}{resultados['saldo_estrategia']} pts
                        </td>
                    </tr>
                </tbody>
            </table>

        </body>
        </html>
        """
        
        # Cria um buffer na memória para o PDF
        pdf_buffer = BytesIO()
        
        # Executa a conversão do HTML para PDF dentro do buffer
        pisa_status = pisa.CreatePDF(BytesIO(html_content.encode("utf-8")), dest=pdf_buffer)
        
        if pisa_status.err:
            print("❌ Erro ao renderizar o PDF via pisa")
            return None
            
        pdf_buffer.seek(0)
        return pdf_buffer
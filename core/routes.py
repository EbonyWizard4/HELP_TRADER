from flask import Flask, render_template, request, Blueprint, jsonify
from core.analizador import analisar_mini_indice

# Blueprint main
main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    dados = None

    if request.method == 'POST':
        # Quando o botão for clicado, executa a função de análise
        dados = analisar_mini_indice()

    return render_template('index.html', resultado=dados)

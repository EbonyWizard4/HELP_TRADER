from flask import Flask, render_template, request, redirect, url_for
from analizador import analisar_mini_indice

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    dados_analise = None

    if request.method == 'POST':
        # Quando o botão for clicado, executa a função de análise
        dados_analise = analisar_mini_indice()
    return render_template('index.html', resultado=dados_analise)

if __name__ == '__main__':
    # roda o servidor em modo de desenvolvimento
    app.run(debug=True)
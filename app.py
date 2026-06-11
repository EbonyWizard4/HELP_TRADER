from flask import Flask, render_template, request, redirect, url_url_for
from analizador import analizar_miniindice

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    dados_analise = None

    if request.method == 'POST':
        # Quando o botão for clicado, executa a função de análise
        dados_analise = analizar_miniindice()
    return render_template('index.html', resultado=dados_analise)

if __name__ == '__main__':
    # roda o servidor em modo de desenvolvimento
    app.run(debug=True)
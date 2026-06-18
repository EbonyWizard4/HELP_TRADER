from core import create_app

# Liga a fabrica e pega a instancia da aplicação
app = create_app()

# Roda a aplicação localmente
if __name__ == '__main__':
    # Roda a aplicação em modo debug
    app.run(debug=True) 
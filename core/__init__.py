import os
from flask import Flask

def create_app():
    # Definir o caminho para o diretório 'templates' e 'static'
    template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

    app = Flask(__name__, template_folder=template_dir)

    # Configuração da chave secreta para sessões (importante para segurança)
    app.config['SECRET_KEY'] = 'dev_key_suport_trader'  # Substitua por uma chave secreta real

    # Importar os blueprints das rotas    from .routes import main_bp
    from core.routes import main_bp
    app.register_blueprint(main_bp) 
    return app

from flask import Flask
from dotenv import load_dotenv
from src.routes.sessions import sessions
from src.routes.clients import clients
from src.routes.histories import histories
from src.routes.pages import pages
import os

load_dotenv() # Inicializando las variables de entorno

app = Flask(__name__)

# Rutas para la sección de autenticaciones y contraseñas
app.register_blueprint(sessions)

# Rutas para la sección de paginas
app.register_blueprint(pages)

# Rutas para la sección de clientes
app.register_blueprint(clients)

# Rutas para la sección de historiales
app.register_blueprint(histories)


# Configuraciones almacenadas en variables de entorno
app.secret_key = os.getenv('SECRET_KEY')

app.port = os.getenv('PORT')


if __name__ == "__main__":
    app.run()
